"""Intenzioni di voto dal registro ufficiale dei sondaggi politico-elettorali.

Fonte: <https://www.sondaggipoliticoelettorali.it>, il registro della Presidenza
del Consiglio dove per legge ogni sondaggio pubblicato va depositato. Stessa
scelta fatta per gli altri layer: fonte ufficiale, non aggregatori.

Il sito è un'applicazione ASP.NET WebForms, quindi niente API. Serve una sessione
(un cookie preso dalla home) e ogni passo è un postback che rimanda `__VIEWSTATE`.
Il percorso è: ricerca → riga → scheda *Domande* → singola domanda.

Due filtri, non uno. Il campo *Titolo* del registro è testo libero scritto dal
sondaggista: un sondaggio intitolato «intenzioni di voto» può contenere qualsiasi
domanda, e uno intitolato altrimenti può contenerle. Quindi si filtra due volte —
sul titolo per ridurre le richieste al sito, e sul **testo della domanda** per
decidere davvero. Il testo completo è già nella lista delle domande: le domande si
aprono una per una solo quando servono.

## La normalizzazione

Le percentuali depositate non sommano a 100 e non sommano allo stesso numero fra
istituti: ognuno include a modo suo indecisi, astenuti e «non si esprime». Una
serie costruita sui valori grezzi confronterebbe basi diverse.

Le quote di partito vengono quindi **rinormalizzate a 100 sui soli partiti
riconosciuti**, che è la base con cui i sondaggi vengono normalmente citati. Il
valore grezzo resta nel record accanto a quello normalizzato, insieme alla somma
grezza: senza quella non si può giudicare quanto la normalizzazione abbia spostato.
"""

from __future__ import annotations

import re
import time
import unicodedata

import requests

BASE = "https://www.sondaggipoliticoelettorali.it/"
LISTA = BASE + "ListaSondaggi.aspx?st=SONDAGGI"
SCHEDA = BASE + "GestioneSondaggio.aspx"

# I dieci partiti seguiti dal layer 3, con le grafie che gli istituti usano nel
# registro. Le chiavi sono le stesse di src/mediacloud_spike.py: e' cio' che
# permette di appaiare la serie dei sondaggi alla copertura stampa.
#
# L'ordine conta: si prova prima il pattern piu' lungo. "Lega" nuda dopo "Lega
# Salvini Premier", altrimenti la prima vince e la seconda non si vede mai.
PARTITI: dict[str, tuple[str, ...]] = {
    "FdI / Meloni": (r"fratelli\s*d.?\s*italia", r"\bfdi\b"),
    "PD / Schlein": (r"partito\s+democratico", r"\bpd\b"),
    "Lega / Salvini": (r"lega\s+salvini\s+premier", r"\blega\b"),
    "M5S / Conte": (r"movimento\s*5\s*stelle", r"\bm5s\b", r"movimento\s+cinque\s+stelle"),
    "Forza Italia / Tajani": (r"forza\s+italia", r"\bfi\b"),
    "AVS / Fratoianni-Bonelli": (r"alleanza\s+verdi\s*(?:e\s*)?sinistra", r"\bavs\b",
                                 r"verdi\s*[-e/]\s*sinistra"),
    "Azione / Calenda": (r"\bazione\b",),
    "Italia Viva / Renzi": (r"italia\s+viva", r"\biv\b"),
    "+Europa": (r"\+\s*europa", r"piu.\s*europa", r"più\s*europa"),
    "Futuro Nazionale / Vannacci": (r"futuro\s+nazionale",),
}

# Voci che non sono partiti e non entrano nella base di normalizzazione.
NON_PARTITO = re.compile(
    r"non\s+si\s+esprim|non\s+indica|indecis|astensione|astenut|non\s+voterebbe|"
    r"bianca|nulla|non\s+so|non\s+saprei|non\s+risponde|\baltr[oi]\b|totale",
    re.I,
)

# Una domanda e' di intenzione di voto se il testo lo dice. Il registro non ha un
# campo tipizzato, quindi questa e' l'unica presa che c'e'.
#
# Le formule sono tre, una per istituto, e vanno coperte tutte:
#   NOTO       «Se domani si dovesse votare per le elezioni politiche, lei quale
#               lista voterebbe?»
#   Ipsos Doxa «Se si votasse oggi, per quale lista voterebbe alla Camera?»
#   SWG        «Se dovesse votare oggi alle elezioni nazionali, a quale dei
#               seguenti partiti darebbe il suo voto?»
#
# Il pattern e' volutamente largo: chi decide davvero e' `e_intenzione_di_voto`,
# che pretende anche almeno quattro partiti fra le risposte. Un filtro stretto qui
# perde rilevazioni in silenzio, che e' il danno peggiore.
DOMANDA_VOTO = re.compile(
    r"\bse\b.{0,40}\bvot(?:asse|are|erebbe|era)|"
    r"intenzion\w*\s+di\s+voto|"
    r"quale\s+(?:lista|partito|coalizione)\s+voterebbe|"
    r"voterebbe\s+alla\s+camera|"
    r"a\s+quale\s+dei\s+seguenti\s+partiti|"
    r"darebbe\s+il\s+suo\s+voto|"
    r"per\s+quale\s+(?:lista|partito)",
    re.I | re.S,
)

# `_generation` non e' un campo ASP.NET standard: e' del sito, e senza di esso il
# postback della singola domanda rimbalza sulla prima scheda invece di aprirla.
_CAMPI_STATO = ("__VIEWSTATE", "__VIEWSTATEGENERATOR", "__EVENTVALIDATION", "_generation")


def normalizza(testo: str) -> str:
    testo = unicodedata.normalize("NFD", testo.lower())
    testo = "".join(c for c in testo if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", testo).strip()


def riconosci_partito(etichetta: str) -> str | None:
    """Il partito dietro l'etichetta di una risposta, o None se non e' un partito."""
    if NON_PARTITO.search(etichetta):
        return None
    norm = normalizza(etichetta)
    for partito, pattern in PARTITI.items():
        for p in pattern:
            if re.search(p, norm):
                return partito
    return None


# Lo stesso istituto deposita sotto grafie diverse: "SWG S.p.A." e "SWG s.p.A"
# sono la stessa SWG, ma raggruppando per stringa diventano due serie. Conta,
# perche' l'effetto istituto e' il confondente principale di questa serie e per
# toglierlo bisogna sapere chi ha fatto cosa.
def normalizza_istituto(nome: str) -> str:
    ridotto = re.sub(r"\b(s\.?p\.?a\.?|s\.?r\.?l\.?|srls|societa)\b", "", nome, flags=re.I)
    ridotto = re.sub(r"[^\w\s]", " ", ridotto)
    return re.sub(r"\s+", " ", ridotto).strip().title()


def stato(html: str) -> dict[str, str]:
    """I campi nascosti che ASP.NET pretende indietro a ogni postback."""
    valori = {}
    for campo in _CAMPI_STATO:
        trovato = re.search(rf'(?:id|name)="{campo}"[^>]*value="([^"]*)"', html)
        if trovato:
            valori[campo] = trovato.group(1)
    return valori


def apri_sessione(user_agent: str) -> requests.Session:
    sessione = requests.Session()
    sessione.headers["User-Agent"] = user_agent
    sessione.get(BASE + "Home.aspx?st=HOME", timeout=60)
    return sessione


def postback(sessione, url: str, html: str, campi: dict, timeout: int, pausa: float,
             tentativi: int = 4):
    """Un passo di navigazione, con la pazienza che un sito della PA merita.

    Il registro chiude la connessione se lo si incalza: `ConnectionResetError` non
    e' un errore da propagare, e' il server che chiede di rallentare. Si aspetta e
    si riprova, raddoppiando.
    """
    dati = stato(html)
    dati.update({"__EVENTTARGET": "", "__EVENTARGUMENT": ""})
    dati.update(campi)
    for tentativo in range(1, tentativi + 1):
        time.sleep(pausa)
        try:
            return sessione.post(url, data=dati, timeout=timeout)
        except (requests.ConnectionError, requests.Timeout):
            if tentativo == tentativi:
                raise
            time.sleep(pausa * 4 * 2 ** tentativo)
    raise RuntimeError("irraggiungibile")


def _valori_input(html: str, pattern: str) -> list[tuple[str, str]]:
    """Coppie (name, value) degli input submit che corrispondono al pattern."""
    trovati = []
    for tag in re.finditer(r"<input[^>]*>", html, re.I):
        testo = tag.group(0)
        nome = re.search(r'name="([^"]+)"', testo)
        valore = re.search(r'value="([^"]*)"', testo)
        if nome and valore and re.search(pattern, nome.group(1)):
            trovati.append((nome.group(1), _dehtml(valore.group(1))))
    return trovati


def _dehtml(testo: str) -> str:
    for a, b in (("&#39;", "'"), ("&amp;", "&"), ("&quot;", '"'),
                 ("&lt;", "<"), ("&gt;", ">"), ("&nbsp;", " ")):
        testo = testo.replace(a, b)
    return testo.strip()


def domanda_mostrata(html: str) -> str:
    """Il testo della domanda di cui la scheda sta mostrando la risposta.

    La scheda *Domande* rende insieme l'elenco delle domande e il dettaglio di
    una di esse. Quale sia va letto, non assunto: per i sondaggi con una domanda
    sola coincide, per gli altri no.
    """
    trovato = re.search(r'id="[^"]*ReadOnly_Domanda"[^>]*>(.*?)</p>', html, re.S)
    return _dehtml(re.sub(r"<[^>]+>", " ", trovato.group(1))) if trovato else ""


def pagine_totali(html: str) -> int:
    trovato = re.search(r"Pagina\s+\d+\s+di\s+(\d+)", re.sub(r"<[^>]+>", " ", html))
    return int(trovato.group(1)) if trovato else 1


def campi_ricerca(config: dict) -> dict:
    return {
        "ctl00$Contenuto$sbxAutore": "Contiene",
        "ctl00$Contenuto$Autore": "",
        "ctl00$Contenuto$sbxCommittente": "Contiene",
        "ctl00$Contenuto$Committente": "",
        "ctl00$Contenuto$DataRealizzazioneDa": config["data_da"],
        "ctl00$Contenuto$DataRealizzazioneA": config["data_a"],
        "ctl00$Contenuto$Titolo": config["titolo"],
    }


def metadati(html: str) -> dict:
    """Realizzatore, committente e periodo di rilevazione dalla scheda del sondaggio."""
    def campo(nome: str) -> str:
        # `ReadOnly_` esclude le etichette, che si chiamano `..._lbl<Campo>`.
        trovato = re.search(rf'id="[^"]*ReadOnly_{nome}"[^>]*>(.*?)</(?:p|span)>', html, re.S)
        return _dehtml(re.sub(r"<[^>]+>", " ", trovato.group(1))) if trovato else ""

    return {
        "titolo": campo("Titolo"),
        "realizzatore": campo("Realizzatore"),
        "committente": campo("Committente"),
        "data_da": campo("DataRealizzazioneDa"),
        "data_a": campo("DataRealizzazioneA"),
        "campione": campo("Campione_Intervistati"),
        "rappresentativita": campo("Rappresentativa_Campione"),
    }


# Un valore: un numero, eventualmente con un decimale e un segno di percentuale.
# `-` da solo vale «questo partito non c'era in questo scenario».
_VALORE = re.compile(r"^(?:\d{1,3}(?:[.,]\d+)?\s*%?|[-–]|%)$")


def risposte(html: str) -> list[tuple[str, list[float | None]]]:
    """Le righe della risposta come (etichetta, valori).

    Il registro salva le risposte come testo libero con un a capo per riga:
    «Fratelli d'Italia 29,5<br />Partito Democratico 21,8<br />…».

    I valori sono una **lista** perche' parecchi istituti depositano piu' colonne
    sulla stessa riga: scenari alternativi («Vannacci nel centrodestra» contro
    «Vannacci autonomo»), oppure il confronto con la rilevazione precedente. Chi
    legge decide quale colonna prendere, e sa quante ce n'erano.
    """
    blocco = re.search(r'id="[^"]*_Risposta"[^>]*>(.*?)</p>', html, re.S)
    if not blocco:
        return []
    righe = []
    for riga in re.split(r"<br\s*/?>|\n", blocco.group(1)):
        pulita = _dehtml(re.sub(r"<[^>]+>", " ", riga))
        if not pulita:
            continue
        # I numeri si prendono **da destra**. Prenderli da sinistra spezzava
        # «Movimento 5 Stelle 12,5» sul 5 del nome: l'etichetta diventava
        # «Movimento», che non e' nessun partito, e il M5S spariva da ogni
        # rilevazione di chi non scrive la sigla.
        parole = pulita.split()
        taglio = len(parole)
        while taglio > 0 and _VALORE.match(parole[taglio - 1]):
            taglio -= 1
        etichetta = " ".join(parole[:taglio]).strip(" .:-–\t")
        # Il trattino tiene il posto: «FUTURO NAZIONALE - 6,0» vuol dire assente
        # nel primo scenario e 6,0 nel secondo. Scartarlo invece di segnarlo
        # sposterebbe la colonna, e la colonna e' cio' che distingue uno scenario
        # dall'altro.
        valori = [None if p in ("-", "–") else float(p.replace(",", ".").rstrip("%"))
                  for p in parole[taglio:] if p != "%"]
        if not etichetta or not valori:
            continue
        righe.append((etichetta, valori))
    return righe


def normalizza_quote(righe: list[tuple[str, list[float | None]]],
                     colonna: int = 0) -> tuple[dict[str, dict], float]:
    """Da etichette grezze a quote per partito, rinormalizzate a 100.

    Restituisce anche la somma grezza dei soli partiti riconosciuti: e' il numero
    che dice quanto la normalizzazione ha spostato, e senza di esso la quota
    normalizzata non e' giudicabile.
    """
    grezzi: dict[str, float] = {}
    for etichetta, valori in righe:
        partito = riconosci_partito(etichetta)
        if partito is None or colonna >= len(valori) or valori[colonna] is None:
            continue
        valore = valori[colonna]
        # Se un istituto spezza una coalizione in due righe che ricadono sullo
        # stesso partito, si sommano: e' la stessa lista.
        grezzi[partito] = grezzi.get(partito, 0.0) + valore

    base = sum(grezzi.values())
    if base <= 0:
        return {}, 0.0
    return (
        {p: {"grezzo": v, "normalizzato": 100.0 * v / base} for p, v in grezzi.items()},
        base,
    )


def e_intenzione_di_voto(domanda: str, righe: list[tuple[str, list[float | None]]],
                         min_partiti: int = 4) -> bool:
    """Domanda di intenzione di voto: lo dice il testo, lo confermano le risposte.

    Il testo da solo non basta - «per quale partito» compare anche in domande
    retrospettive - e le risposte da sole nemmeno, perche' un sondaggio di
    gradimento elenca gli stessi partiti. Servono entrambi.
    """
    if not DOMANDA_VOTO.search(domanda):
        return False
    riconosciuti = {riconosci_partito(e) for e, _ in righe}
    return len({p for p in riconosciuti if p}) >= min_partiti
