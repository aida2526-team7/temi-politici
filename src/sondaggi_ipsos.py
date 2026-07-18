"""Ingest della salienza dei temi per l'Italia da Ipsos (stage sondaggi).

Fonte: la pagina Ipsos Italia `sondaggi-politici-oggi`, che riporta ogni mese la
sezione "Le preoccupazioni degli italiani" tratta da "What Worries the World".
I numeri sono nel TESTO della pagina (non nei grafici), quindi estraibili senza
OCR:

    In Italia, crimine e violenza (37%), ... Seguono: healthcare (35%, +1 punto),
    disoccupazione (34%, +4 punti), inflazione (30%, -4 punti) e tasse (26%,
    -3 punti). ... Fonte: What Worries The World, June 2026

Il PDF globale mensile di Ipsos NON va bene: contiene solo la media mondiale, non
l'Italia.

Approccio PROSPETTICO. La pagina italiana espone solo il mese corrente, e lo
storico NON e' recuperabile: la Wayback Machine ha archiviato solo il guscio JS
della pagina, senza i numeri (verificato: 1 mese su 7 snapshot). Quindi il dataset
si costruisce nel tempo, eseguendo l'ingest ogni mese e accumulando (vedi
aggiorna_dataset). E' una scelta dichiarata: un dataset che cresce in avanti, non
una serie retrospettiva.

Questo e' uno stage a se': produce numeri e date (`data, istituto, tema, valore`),
NON testo. La correlazione con i temi della stampa e' un passo a valle.

Limiti noti:
- la pagina cita in chiaro solo i ~5 temi principali; la lista completa sta nel
  grafico-immagine, non estratta qui;
- i dati Ipsos sono proprietari: versionare il dataset accumulato richiede la
  revisione di compliance gia' prevista dal progetto.
"""

from __future__ import annotations

import re
from datetime import datetime

CDX_ENDPOINT = "https://web.archive.org/cdx/search/cdx"

# Mesi in inglese e italiano -> numero (la riga "Fonte" e' spesso in inglese).
MESI = {
    "january": 1, "gennaio": 1, "february": 2, "febbraio": 2, "march": 3, "marzo": 3,
    "april": 4, "aprile": 4, "may": 5, "maggio": 5, "june": 6, "giugno": 6,
    "july": 7, "luglio": 7, "august": 8, "agosto": 8, "september": 9, "settembre": 9,
    "october": 10, "ottobre": 10, "november": 11, "novembre": 11, "december": 12, "dicembre": 12,
}

# Etichette Ipsos -> chiave tema normalizzata. La pagina mescola italiano e inglese
# ("healthcare" resta in inglese anche nella versione italiana). La chiave e'
# quella su cui poi si aggancia la tassonomia comune con la stampa.
TEMA_NORM = {
    "crimine e violenza": "criminalita",
    "criminalita": "criminalita",
    "criminalità": "criminalita",
    "healthcare": "sanita",
    "sanita": "sanita",
    "sanità": "sanita",
    "disoccupazione": "disoccupazione",
    "inflazione": "inflazione",
    "costo della vita": "inflazione",
    "tasse": "tasse",
    "poverta": "poverta",
    "povertà e disuguaglianza sociale": "poverta",
    "immigrazione": "immigrazione",
    "controllo dell'immigrazione": "immigrazione",
    "istruzione": "istruzione",
    "cambiamento climatico": "clima",
    "corruzione": "corruzione",
    "corruzione finanziaria/politica": "corruzione",
    "terrorismo": "terrorismo",
}


def _norm(label: str) -> str:
    return re.sub(r"\s+", " ", label.lower()).strip(" .,:;")


def strip_tags(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html)
    text = text.replace("&nbsp;", " ").replace("&amp;", "&")
    return re.sub(r"\s+", " ", text).strip()


def mese_rilevazione(text: str) -> str | None:
    """Mese della rilevazione da 'Fonte: What Worries The World, June 2026' -> '2026-06'."""
    m = re.search(r"what worries the world[,\s]+([a-zà-ù]+)\s+(\d{4})", text, re.I)
    if not m:
        return None
    mese = MESI.get(m.group(1).lower())
    return f"{m.group(2)}-{mese:02d}" if mese else None


def estrai_preoccupazioni(html: str) -> dict | None:
    """Salienza dei temi Italia dalla sezione 'preoccupazioni degli italiani'.

    Ritorna {'mese': '2026-06', 'temi': [{'tema','tema_norm','valore'}, ...]}
    oppure None se la sezione non c'e' in questo snapshot.
    """
    text = strip_tags(html)
    low = text.lower()

    # Delimita il blocco: da "In Italia," fino a "Fonte: What Worries...". E'
    # necessario, perche' la pagina ha altre sezioni con altre percentuali
    # (direzione del Paese, ottimismo economico, Trump) che non vanno raccolte.
    inizio = low.find("in italia,")
    if inizio < 0:
        return None
    coda = low.find("what worries the world", inizio)
    fine = coda + 60 if coda > 0 else inizio + 700
    blocco = text[inizio:fine]

    mese = mese_rilevazione(text[inizio:fine + 40]) or mese_rilevazione(text)
    if not mese:
        return None

    temi = []
    visti = set()
    for label, valore in re.findall(r"([A-Za-zÀ-ù][A-Za-zÀ-ù '/]{2,40}?)\s*\((\d{1,2})%", blocco):
        chiave = _norm(label)
        norm = _match_tema(chiave)
        # scarta code di frase catturate ("seguono", "rappresenta", "e"): non
        # corrispondono a nessun tema noto.
        if norm is None or norm in visti:
            continue
        visti.add(norm)
        # tema pulito = la variante nota, non l'eventuale congiunzione iniziale
        tema_pulito = next(k for k in TEMA_NORM if TEMA_NORM[k] == norm and chiave.endswith(k))
        temi.append({"tema": tema_pulito, "tema_norm": norm, "valore": int(valore)})

    return {"mese": mese, "temi": temi} if temi else None


def _match_tema(chiave: str) -> str | None:
    """Tema normalizzato dalla frase catturata, ignorando congiunzioni iniziali
    ('e tasse' -> tasse). Confronto per suffisso sulle etichette note."""
    if chiave in TEMA_NORM:
        return TEMA_NORM[chiave]
    for etichetta, norm in TEMA_NORM.items():
        if chiave.endswith(" " + etichetta) or chiave == etichetta:
            return norm
    return None


def snapshot_wayback(session, url: str, dal: int, al: int, timeout: int, pause: float) -> list[dict]:
    """Snapshot distinti (per contenuto) dell'URL nel periodo. Riusa CDX come il layer 1."""
    from src.programmi_discovery import fetch

    params = {
        "url": url, "from": f"{dal}0101", "to": f"{al}1231", "output": "json",
        "fl": "timestamp,original,statuscode,digest",
        "filter": "statuscode:200", "collapse": "digest",
    }
    response = fetch(session, CDX_ENDPOINT, timeout, pause, params=params)
    if response is None:
        return []
    try:
        rows = response.json()
    except ValueError:
        return []
    if len(rows) < 2:
        return []
    header = rows[0]
    return [dict(zip(header, r)) for r in rows[1:]]


def wayback_url(timestamp: str, original: str) -> str:
    return f"https://web.archive.org/web/{timestamp}id_/{original}"


def record(mese: str, tema: dict, url_fonte: str) -> dict:
    return {
        "data": mese,
        "istituto": "Ipsos",
        "indagine": "What Worries the World",
        "tema": tema["tema"],
        "tema_norm": tema["tema_norm"],
        "valore": tema["valore"],
        "unita": "pct_menzioni",
        "paese": "Italia",
        "fonte": "ipsos_it",
        "estrazione": "testo",
        "url_fonte": url_fonte,
    }


CAMPI = ["data", "istituto", "indagine", "paese", "tema", "tema_norm",
         "valore", "unita", "fonte", "estrazione", "url_fonte"]


def raccogli_corrente(session, config: dict) -> list[dict]:
    """Lettura del mese corrente dalla pagina live. E' la fonte primaria.

    L'approccio e' prospettico: questa pagina espone solo il mese in corso, quindi
    il dataset si costruisce nel tempo eseguendo l'ingest ogni mese. Lo storico
    retrospettivo NON e' recuperabile da qui: la Wayback Machine non ha archiviato
    il contenuto caricato via JavaScript (vedi raccogli_storico).
    """
    from src.programmi_discovery import fetch

    url_fonte = f"https://www.{config['url']}"
    response = fetch(session, url_fonte, config["timeout"], config["pause"])
    if response is None:
        return []
    lettura = estrai_preoccupazioni(response.text)
    if not lettura:
        return []
    return [record(lettura["mese"], tema, url_fonte) for tema in lettura["temi"]]


def raccogli_storico(session, config: dict) -> list[dict]:
    """Tentativo best-effort di recupero da Wayback. Recupera poco: molti snapshot
    hanno solo il guscio JS senza i numeri. Utile solo per rimediare un mese
    occasionale, non per una serie."""
    from src.programmi_discovery import fetch

    per_mese: dict[str, dict] = {}
    for snap in snapshot_wayback(session, config["url"], config["dal"], config["al"],
                                 config["timeout"], config["pause"]):
        acquisizione = wayback_url(snap["timestamp"], snap["original"])
        response = fetch(session, acquisizione, config["timeout"], config["pause"])
        if response is None:
            continue
        lettura = estrai_preoccupazioni(response.text)
        if lettura and lettura["mese"] not in per_mese:
            per_mese[lettura["mese"]] = (lettura, acquisizione)

    records = []
    for mese in sorted(per_mese):
        lettura, url_fonte = per_mese[mese]
        records.extend(record(mese, tema, url_fonte) for tema in lettura["temi"])
    return records


def carica_dataset(path) -> list[dict]:
    import csv
    from pathlib import Path

    path = Path(path)
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def aggiorna_dataset(nuovi: list[dict], path) -> tuple[int, int]:
    """Fonde i nuovi record col dataset esistente, deduplicando per
    (data, istituto, indagine, tema_norm). Ritorna (aggiunti, totale).

    E' il meccanismo dell'accumulo prospettico: ri-eseguire lo stesso mese non
    duplica; un mese nuovo si aggiunge in coda.
    """
    import csv
    from pathlib import Path

    def chiave(r: dict) -> tuple:
        return (r["data"], r["istituto"], r["indagine"], r["tema_norm"])

    esistenti = carica_dataset(path)
    indice = {chiave(r) for r in esistenti}
    aggiunti = [r for r in nuovi if chiave(r) not in indice]

    combinati = esistenti + aggiunti
    combinati.sort(key=lambda r: (r["data"], r["istituto"], -int(r["valore"])))

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CAMPI)
        writer.writeheader()
        writer.writerows(combinati)
    return len(aggiunti), len(combinati)
