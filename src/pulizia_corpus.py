"""Pulizia del corpus stampa: toglie il boilerplate e i duplicati (layer silver).

Perche' esiste
--------------
Il primo giro di TF-IDF + NMF ha prodotto 12 topic di cui 7 erano template di
testate: "in evidenza", "riproduzione riservata copyright ansa", "vai all
articolo su raiplay", "agenzia vista", "edicola digitale chi siamo". Non e' un
difetto dell'NMF: quelle stringhe sono il testo piu' regolare del corpus, quindi
sono anche la struttura piu' forte che una fattorizzazione puo' trovare.

Il boilerplate NON si riconosce guardando una pagina alla volta. Su
adnkronos.com/internazionale/japanese/* il corpo dell'articolo e' renderizzato in
JS: nell'HTML servito non c'e' articolo, trafilatura restituisce la spalla "in
Evidenza" e la restituisce come contenuto legittimo (739 caratteri, sopra la
soglia dell'harvester). Nessun controllo di pagina puo' accorgersene.

Si riconosce guardando il corpus: la stessa riga che compare in meta' dei
documenti di un dominio e' il suo template, non una notizia. Questo modulo lavora
li'.

Cosa fa, in ordine
------------------
1. `righe_template`  — per ogni dominio, le righe che ricorrono in una quota
   eccessiva dei suoi documenti;
2. `togli_boilerplate` — le rimuove dal testo, documento per documento;
3. `dedup_testo`     — scarta i documenti che, ripulito il template, risultano
   identici a uno gia' visto (la spalla di Adnkronos produceva 3.095 record con
   lo stesso identico estratto);
4. `ricontrolla_lingua` — rilegge la lingua sul testo pulito. Prima veniva
   rilevata sul chrome: 40 articoli con titolo in caratteri non latini erano
   passati come "it" perche' il menu attorno era italiano.

Ogni passo restituisce anche cosa ha tolto e perche': senza quello la pulizia e'
una cancellazione non verificabile, e il progetto chiede il contrario.

Il modulo non tocca `data/raw`. Il bronze resta com'e' scaricato.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from collections import Counter, defaultdict


# Un dominio con pochi documenti non permette di distinguere un template da una
# coincidenza: due articoli che iniziano uguale non sono un menu.
MIN_DOC_PER_DOMINIO = 20

# Quota di documenti di un dominio oltre la quale una riga e' template. Al 30%
# nessun contenuto reale sopravvive per caso: nemmeno la cronaca piu' ripetitiva
# ripete la stessa frase in un terzo degli articoli della testata.
QUOTA_TEMPLATE = 0.30

# Le formule d'agenzia ("riproduzione riservata") attraversano i domini: chi ne
# ha pochi documenti non le vedrebbe con la regola per dominio.
QUOTA_TEMPLATE_GLOBALE = 0.02

# ...ma "attraversa i domini" e' la condizione che rende globale una riga, non la
# sola frequenza. Senza questo vincolo, su un corpus piccolo il 2% e' meno di un
# documento e ogni riga diventa template: la pulizia svuoterebbe tutto.
MIN_DOMINI_GLOBALE = 3

# Sotto questa dimensione la regola globale non si applica affatto: una quota
# calcolata su poche decine di documenti non e' una frequenza, e' un caso.
MIN_DOC_CORPUS = 200

# Righe cortissime ("Ansa", "Foto") sono rumore comunque; righe lunghe e ripetute
# sono quasi sempre disclaimer legali, che vanno tolti allo stesso modo.
MIN_CARATTERI_RIGA = 3


# Firme di UTF-8 letto come ISO-8859-1: "piu'" diventa "piÃ¹", "e'" diventa "Ã¨".
# Ne bastano poche per riconoscere il caso senza falsi positivi - "Ã" seguita da
# un carattere della fascia alta non compare in italiano corretto.
_MOJIBAKE = re.compile(r"Ã[\x80-\xbf]|â€[\x80-\x9f]|Â[\xa0-\xbf]")


def ripara_codifica(testo: str) -> str:
    """Rimette a posto il testo salvato con la codifica sbagliata.

    `requests` ripiega su ISO-8859-1 per i `text/*` quando il server non dichiara
    il charset (RFC 2616), e su pagine italiane il risultato e' "piÃ¹" al posto di
    "piu'".

    Non e' cosmetico: il lessico dei macrotemi toglie i diacritici per far
    combaciare "sanita'" e "sanita", e "sanitÃ " non combacia con nessuno dei due.

    Misurato su 25.000 articoli: l'1,3% porta il difetto, ma solo lo 0,27% e'
    **riparabile**. Nell'altro 1,00% l'estrazione ha perso i byte di continuazione
    - "L'inno" e' salvato come "Linno" con una sola "a" circonflessa - e
    l'informazione non c'e' piu'. Per quelli non si puo' fare niente a valle: il
    fix vero e' in `harvester.fetch_response`, che impedisce il problema a monte.

    La riparazione e' l'inverso esatto dell'errore - ricodifica in latin-1 e
    ridecodifica in UTF-8 - e si applica solo se il testo porta le firme del
    problema. Se il giro non riesce, si tiene l'originale: meglio un testo brutto
    di un testo perso.
    """
    if not testo or not _MOJIBAKE.search(testo):
        return testo
    try:
        riparato = testo.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return testo
    return riparato if not _MOJIBAKE.search(riparato) else testo


def normalizza_riga(riga: str) -> str:
    """Forma confrontabile di una riga: minuscole, senza accenti, spazi singoli.

    Serve a far collassare "In Evidenza" e "in evidenza" sulla stessa chiave: il
    template di un sito cambia capitalizzazione fra le pagine, non sostanza.
    """
    riga = unicodedata.normalize("NFKD", riga.lower())
    riga = "".join(c for c in riga if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", riga).strip()


def _righe(testo: str) -> list[str]:
    """Righe non vuote e abbastanza lunghe da essere confrontabili."""
    return [r for r in (riga.strip() for riga in (testo or "").splitlines())
            if len(r) >= MIN_CARATTERI_RIGA]


def righe_template(records, quota=QUOTA_TEMPLATE, quota_globale=QUOTA_TEMPLATE_GLOBALE,
                   min_doc=MIN_DOC_PER_DOMINIO):
    """Righe da considerare template, per dominio e globali.

    Ritorna (per_dominio, globali, diagnostica):
      - per_dominio: {dominio: {riga_normalizzata: frazione_documenti}}
      - globali:     {riga_normalizzata: frazione_documenti}
      - diagnostica: conteggi utili al report

    Una riga si conta UNA volta per documento: un menu ripetuto tre volte nella
    stessa pagina non deve pesare piu' di un menu che compare una volta sola.
    """
    doc_per_dominio: Counter = Counter()
    righe_per_dominio: dict[str, Counter] = defaultdict(Counter)
    righe_globali: Counter = Counter()
    domini_per_riga: dict[str, set] = defaultdict(set)

    for record in records:
        dominio = record.get("domain") or ""
        doc_per_dominio[dominio] += 1
        viste = {normalizza_riga(r) for r in _righe(record.get("text", ""))}
        for riga in viste:
            righe_per_dominio[dominio][riga] += 1
            righe_globali[riga] += 1
            domini_per_riga[riga].add(dominio)

    totale = len(records)
    per_dominio = {}
    for dominio, conteggi in righe_per_dominio.items():
        n = doc_per_dominio[dominio]
        if n < min_doc:
            continue          # troppo pochi documenti per dire che e' un template
        soglia = quota * n
        template = {riga: quanti / n for riga, quanti in conteggi.items() if quanti >= soglia}
        if template:
            per_dominio[dominio] = template

    # Tre condizioni insieme: frequente, su un corpus abbastanza grande da poterla
    # misurare, e presente su piu' testate. E' l'ultima a distinguere una formula
    # d'agenzia da una frase che una singola redazione ripete spesso — quella la
    # prende gia' la regola per dominio, con una soglia molto piu' alta.
    globali = {}
    if totale >= MIN_DOC_CORPUS:
        globali = {riga: quanti / totale for riga, quanti in righe_globali.items()
                   if quanti >= quota_globale * totale
                   and len(domini_per_riga[riga]) >= MIN_DOMINI_GLOBALE}

    diagnostica = {
        "documenti": totale,
        "domini": len(doc_per_dominio),
        "domini_con_template": len(per_dominio),
        "domini_sotto_soglia": sum(1 for n in doc_per_dominio.values() if n < min_doc),
        "righe_template_globali": len(globali),
    }
    return per_dominio, globali, diagnostica


def togli_boilerplate(record, per_dominio, globali):
    """Testo del record senza le righe template. Ritorna (testo, righe_tolte)."""
    template_dominio = per_dominio.get(record.get("domain") or "", {})
    tenute, tolte = [], 0
    for riga in _righe(record.get("text", "")):
        chiave = normalizza_riga(riga)
        if chiave in template_dominio or chiave in globali:
            tolte += 1
            continue
        tenute.append(riga)
    return "\n".join(tenute), tolte


def impronta(testo: str) -> str:
    """Hash del testo normalizzato: uguale sse il contenuto e' lo stesso.

    Sull'URL non basta: 3.095 URL diversi di Adnkronos servivano lo stesso identico
    testo, e la dedup per URL li ha fatti passare tutti.
    """
    normalizzato = re.sub(r"\s+", " ", normalizza_riga(testo))
    return hashlib.sha1(normalizzato.encode("utf-8")).hexdigest()


def dedup_testo(records, campo="text"):
    """Scarta i record il cui testo e' gia' comparso. Ritorna (tenuti, scartati).

    Tiene il primo incontrato nell'ordine dato: l'ordine del file e' stabile,
    quindi la scelta e' riproducibile senza bisogno di un seed.
    """
    viste: dict[str, str] = {}
    tenuti, scartati = [], []
    for record in records:
        chiave = impronta(record.get(campo, ""))
        if chiave in viste:
            scartati.append(record)
            continue
        viste[chiave] = record.get("url", "")
        tenuti.append(record)
    return tenuti, scartati


def ricontrolla_lingua(records, campo="text"):
    """Rilegge `language` sul testo ripulito. Ritorna quanti record cambiano.

    Prima la lingua veniva rilevata sul testo cosi' com'era uscito
    dall'estrazione, chrome compreso: una pagina giapponese circondata da un menu
    italiano risultava "it" e superava il filtro del classificatore.
    """
    try:
        from langdetect import DetectorFactory, detect
        DetectorFactory.seed = 0
    except ImportError:
        return 0

    cambiati = 0
    for record in records:
        testo = (record.get(campo) or "").strip()
        try:
            lingua = detect(testo[:1000]) if testo else "unknown"
        except Exception:
            lingua = "unknown"
        if lingua != record.get("language"):
            cambiati += 1
        record["language"] = lingua
    return cambiati


def pulisci(records, quota=QUOTA_TEMPLATE, quota_globale=QUOTA_TEMPLATE_GLOBALE,
            min_doc=MIN_DOC_PER_DOMINIO, min_chars=300):
    """Pipeline completa. Ritorna (record_puliti, report).

    `min_chars` e' applicato DOPO la pulizia: un documento che era fatto solo di
    template resta senza niente, ed e' esattamente cio' che va tolto.
    """
    # PRIMA di tutto il resto: se il testo e' mal codificato, anche il
    # riconoscimento dei template lavora su stringhe sbagliate e non le raggruppa.
    riparati = 0
    for record in records:
        for campo in ("title", "text"):
            originale = record.get(campo) or ""
            corretto = ripara_codifica(originale)
            if corretto != originale:
                record[campo] = corretto
                riparati += 1
        record["chars"] = len(record.get("text") or "")

    per_dominio, globali, diagnostica = righe_template(
        records, quota=quota, quota_globale=quota_globale, min_doc=min_doc)

    righe_tolte_totali = 0
    for record in records:
        testo, tolte = togli_boilerplate(record, per_dominio, globali)
        record["text"] = testo
        record["chars"] = len(testo)
        righe_tolte_totali += tolte

    svuotati = [r for r in records if r["chars"] < min_chars]
    con_testo = [r for r in records if r["chars"] >= min_chars]
    tenuti, duplicati = dedup_testo(con_testo)
    lingue_cambiate = ricontrolla_lingua(tenuti)

    report = {
        **diagnostica,
        "campi_codifica_riparati": riparati,
        "righe_template_rimosse": righe_tolte_totali,
        "scartati_senza_testo": len(svuotati),
        "scartati_duplicati": len(duplicati),
        "lingua_corretta": lingue_cambiate,
        "documenti_finali": len(tenuti),
        "lingue_finali": dict(Counter(r.get("language") for r in tenuti).most_common(8)),
        "template_per_dominio": {
            dominio: sorted(righe.items(), key=lambda x: -x[1])[:10]
            for dominio, righe in sorted(
                per_dominio.items(), key=lambda x: -len(x[1]))[:20]
        },
        "template_globali": sorted(globali.items(), key=lambda x: -x[1])[:20],
    }
    return tenuti, report
