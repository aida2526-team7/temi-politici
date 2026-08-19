"""Layer 2 — produzione legislativa: i progetti di legge della Camera.

E' il layer "cosa fanno" di docs/politica-3d.md, e finora non esisteva. Senza,
l'ipotesi H1 (scostamento fra temi dichiarati in campagna e temi dei DDL
presentati) non e' verificabile: manca uno dei due termini del confronto.

Fonte: endpoint SPARQL pubblico https://dati.camera.it/sparql (Virtuoso).
Nessuno scraping — i dati sono pubblicati come linked open data.

Schema di uscita, allineato agli altri layer (`url, title, text, seendate,
domain, chars, language`) piu' i campi propri:

    numero            identificativo dell'atto (dc:identifier)
    legislatura       18 | 19
    iniziativa        parlamentare | governativa | popolare | regionale | CNEL
    primo_firmatario  etichetta del deputato proponente
    gruppo            gruppo parlamentare del primo firmatario alla presentazione

Il testo tematizzabile e' il TITOLO dell'atto: alla Camera il titolo di un
progetto di legge e' una frase descrittiva completa ("Modifiche al codice della
strada in materia di..."), non un'etichetta. E' cio' su cui si fa inferenza
tematica, come previsto dal piano (`ddl-classifier` su titolo + abstract).

Trappole misurate sull'endpoint
-------------------------------
- Virtuoso ha un tetto di righe per risposta: le query vanno paginate con
  LIMIT/OFFSET, altrimenti la risposta arriva troncata SENZA errore. E' il modo
  peggiore di sbagliare, perche' sembra funzionare.
- L'ordinamento e' obbligatorio quando si pagina: senza ORDER BY, due pagine
  consecutive possono ripetere o saltare righe.
- La legislatura si indica con l'URI completo
  <http://dati.camera.it/ocd/legislatura.rdf/repubblica_19>, non con il numero.
"""

from __future__ import annotations

import html
import re
import time

import requests


ENDPOINT = "https://dati.camera.it/sparql"

# Legislature della finestra 2018-2026 dichiarata nel piano.
LEGISLATURE = {
    18: "http://dati.camera.it/ocd/legislatura.rdf/repubblica_18",
    19: "http://dati.camera.it/ocd/legislatura.rdf/repubblica_19",
}

# Virtuoso tronca le risposte lunghe senza dirlo: si pagina sempre.
PAGINA = 1000

HEADERS = {
    "Accept": "application/sparql-results+json",
    # Un endpoint pubblico di un'istituzione: ci si presenta.
    "User-Agent": "temi-politici/1.0 (progetto universitario AIDA, Unimib)",
}

# Paginazione PER CHIAVE, non per OFFSET.
#
# Misurato: con OFFSET 10000 l'endpoint risponde 500. Virtuoso, per servire un
# offset profondo, deve ricostruire e riordinare tutto il risultato a ogni
# richiesta, e su questo join con quattro OPTIONAL sfonda il tetto di lavoro.
#
# Con il filtro sull'ultimo URI visto ogni richiesta parte da dove si era
# arrivati: costo costante per pagina invece che crescente. In piu' e' stabile —
# l'OFFSET su un risultato non materializzato puo' ripetere o saltare righe.
QUERY = """
PREFIX ocd:  <http://dati.camera.it/ocd/>
PREFIX dc:   <http://purl.org/dc/elements/1.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?atto ?numero ?titolo ?data ?iniziativa ?firmatario ?gruppo
WHERE {
  ?atto a ocd:atto ;
        dc:type "Progetto di Legge" ;
        ocd:rif_leg <%(legislatura)s> ;
        dc:title ?titolo .
  FILTER (STR(?atto) > "%(dopo)s")
  OPTIONAL { ?atto dc:identifier ?numero }
  OPTIONAL { ?atto dc:date ?data }
  OPTIONAL { ?atto ocd:iniziativa ?iniziativa }
  OPTIONAL {
    ?atto ocd:primo_firmatario ?deputato .
    ?deputato rdfs:label ?firmatario .
    OPTIONAL { ?deputato ocd:aderisce ?adesione . ?adesione rdfs:label ?gruppo }
  }
}
ORDER BY ?atto
LIMIT %(limite)d
"""


def interroga(query, endpoint=ENDPOINT, timeout=180, tentativi=3):
    """Una query SPARQL -> lista di dizionari piatti {variabile: valore}.

    Ritenta sugli errori di rete: un endpoint pubblico ha picchi di carico, e
    perdere 40 minuti di paginazione per un timeout non ha senso.
    """
    ultimo_errore = None
    for tentativo in range(tentativi):
        try:
            risposta = requests.get(
                endpoint,
                params={"query": query, "format": "application/sparql-results+json"},
                headers=HEADERS,
                timeout=timeout,
            )
            risposta.raise_for_status()
            bindings = risposta.json()["results"]["bindings"]
            return [{k: v["value"] for k, v in riga.items()} for riga in bindings]
        except Exception as errore:            # rete, timeout, JSON malformato
            ultimo_errore = errore
            time.sleep(2 * (tentativo + 1))    # backoff lineare, l'endpoint e' pubblico
    raise RuntimeError(f"Query fallita dopo {tentativi} tentativi: {ultimo_errore}")


def scarica_legislatura(legislatura, pagina=PAGINA, endpoint=ENDPOINT, verbose=True,
                        interrogatore=interroga):
    """Tutti i progetti di legge di una legislatura, paginando.

    `interrogatore` e' iniettabile: i test verificano la paginazione senza
    toccare la rete.

    Nota sul confine di pagina: se le righe di un atto cadono a cavallo fra due
    pagine, il filtro `> ultimo` scarta quelle rimaste. Nessun atto si perde —
    la prima riga di ogni atto arriva sempre, ed e' l'unica che `normalizza`
    tiene — ma per quell'atto `righe_accorpate` risulta piu' basso del vero.
    """
    if legislatura not in LEGISLATURE:
        raise ValueError(f"Legislatura non prevista: {legislatura}. "
                         f"Disponibili: {sorted(LEGISLATURE)}")
    uri = LEGISLATURE[legislatura]
    righe, dopo = [], ""
    while True:
        query = QUERY % {"legislatura": uri, "limite": pagina, "dopo": dopo}
        blocco = interrogatore(query, endpoint)
        if not blocco:
            break
        righe.extend(blocco)
        if verbose:
            print(f"  legislatura {legislatura}: {len(righe):,} righe", flush=True)
        if len(blocco) < pagina:      # ultima pagina
            break
        ultimo = blocco[-1]["atto"]
        if ultimo == dopo:            # l'ordinamento non avanza: meglio fermarsi
            raise RuntimeError(f"Paginazione bloccata su {ultimo}: pagina troppo "
                               f"piccola per il numero di righe per atto.")
        dopo = ultimo
    return righe


# Il titolo arriva prefissato dal proponente: 'SCHULLIAN ed altri: "Introduzione
# dell'articolo..."' oppure 'PROPOSTA DI LEGGE D'INIZIATIVA POPOLARE: "Misure
# a sostegno..."'. Il prefisso e' metadato — chi propone sta gia' in
# `primo_firmatario` — e in un topic model diventerebbe rumore: i cognomi dei
# deputati piu' prolifici formerebbero un topic per conto loro.
_PREFISSO_PROPONENTE = re.compile(r'^.{0,120}?:\s*[""«"]')
# In coda restano la virgoletta di chiusura e talvolta il numero dell'atto
# ripetuto fra parentesi: '..." (1)'. Nessuno dei due e' l'oggetto della legge.
_CODA = re.compile(r'[""»"]?\s*(?:\(\d+\))?\s*$')
_VIRGOLETTA_INIZIALE = re.compile(r'^[""«"]\s*')
# La data arriva come 20221013, non come 2022-10-13.
_DATA_COMPATTA = re.compile(r"^(\d{4})(\d{2})(\d{2})$")
# L'etichetta del gruppo porta in coda la data di adesione: "MISTO (18.10.2022)".
_DATA_ADESIONE = re.compile(r"\s*\(\d{2}\.\d{2}\.\d{4}\)\s*$")


def pulisci_titolo(titolo):
    """Oggetto del progetto di legge, senza entita' HTML ne' prefisso proponente."""
    titolo = html.unescape(titolo or "")
    titolo = re.sub(r"<[^>]+>", "", titolo)          # <em>, <br> e simili
    titolo = re.sub(r"\s+", " ", titolo).strip()
    senza_prefisso = _PREFISSO_PROPONENTE.sub("", titolo)
    # Se il taglio non lascia niente, il prefisso era tutto il titolo: si tiene
    # l'originale, meglio un titolo sporco che un record vuoto.
    if len(senza_prefisso) >= 20:
        titolo = senza_prefisso
    titolo = _VIRGOLETTA_INIZIALE.sub("", titolo)
    return _CODA.sub("", titolo).strip()


def normalizza_data(valore):
    """20221013 -> 2022-10-13. Lascia stare cio' che e' gia' in un altro formato."""
    valore = (valore or "").strip()
    trovata = _DATA_COMPATTA.match(valore)
    return f"{trovata[1]}-{trovata[2]}-{trovata[3]}" if trovata else valore[:10]


def pulisci_gruppo(valore):
    """"MISTO (18.10.2022)" -> "MISTO". La data di adesione non e' il gruppo."""
    return _DATA_ADESIONE.sub("", (valore or "").strip())


def normalizza(righe, legislatura):
    """Righe SPARQL -> record nello schema condiviso dai layer.

    Un atto puo' tornare su piu' righe (piu' adesioni a gruppi nel tempo del
    primo firmatario): si tiene la prima, e si registra quante ne sono state
    accorpate, perche' un'aggregazione silenziosa e' un dato inventato.
    """
    per_atto: dict[str, dict] = {}
    for riga in righe:
        chiave = riga.get("atto", "")
        if chiave in per_atto:
            per_atto[chiave]["righe_accorpate"] += 1
            continue
        titolo = pulisci_titolo(riga.get("titolo"))
        per_atto[chiave] = {
            "url": chiave,
            "domain": "dati.camera.it",
            "seendate": normalizza_data(riga.get("data")),
            "title": titolo,
            # Il titolo E' il testo tematizzabile: alla Camera e' una frase
            # descrittiva completa, non un'etichetta.
            "text": titolo,
            "chars": len(titolo),
            "language": "it",
            "numero": riga.get("numero", ""),
            "legislatura": legislatura,
            "iniziativa": riga.get("iniziativa", ""),
            # Il nome del deputato porta appesa la legislatura: si tiene solo il nome.
            "primo_firmatario": (riga.get("firmatario") or "").split(",")[0].strip(),
            "gruppo": pulisci_gruppo(riga.get("gruppo")),
            "righe_accorpate": 1,
        }
    return list(per_atto.values())
