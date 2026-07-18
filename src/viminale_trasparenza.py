"""Programmi elettorali dal portale "Elezioni trasparenti" del Viminale (layer 1).

La legge 165/2017 obbliga il Ministero dell'Interno a pubblicare, per ogni lista
che si presenta, il programma elettorale depositato. E' una fonte migliore dei
siti dei partiti sotto ogni aspetto: autorevole, completa per definizione, con
data certa, e senza bisogno di indovinare quale PDF sia il programma.

Questo modulo fa SOLO discovery: produce i metadata nel formato che
`harvester.scrape_metas` si aspetta. Il download e l'estrazione del testo restano
di `src/harvester.py`.

Le due consultazioni disponibili usano schemi DIVERSI:

- politiche 2022: indice JSON, ogni documento etichettato da `tp_doc` (2 = programma);
- politiche 2018: pagina HTML statica, i documenti sono etichettati dal testo del
  link ("Programma"). Il nome del file NON e' affidabile: convivono
  `7_Progr_Elettorale.pdf`, `8_Progr_Eelettorale.pdf` (refuso nell'originale),
  `14_Progr_Politico.pdf`, `28_Programma.pdf`. Filtrare per nome ne troverebbe 8
  su 37; filtrare per etichetta li trova tutti.

Le europee 2019/2024 hanno la sezione trasparenza ma NON pubblicano i programmi
(nessun allegato di tipo programma): l'obbligo dell'art. 14-bis del DPR 361/1957
riguarda le politiche.
"""

from __future__ import annotations

import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup


BASE = "https://dait.interno.gov.it"

# tp_doc nello schema JSON del Viminale.
TP_DOC_PROGRAMMA = 2

# Etichetta del link nello schema HTML 2018.
LABEL_PROGRAMMA = "programma"

# Solo PDF: e' l'unico formato che sappiamo leggere (pypdf). Nel 2022 una lista ha
# depositato un .doc, che per giunta risponde 404.
ESTENSIONI_AMMESSE = (".pdf",)

CONSULTAZIONI = {
    "politiche2022": {
        "schema": "json",
        "index": f"{BASE}/documenti/trasparenza/POLITICHE_20220925/POLITICHE_20220925.json",
        "documenti": f"{BASE}/documenti/trasparenza/POLITICHE_20220925/Documenti",
        "data_elezione": "2022-09-25",
    },
    "politiche2018": {
        "schema": "html",
        "index": f"{BASE}/elezioni/trasparenza/politiche2018",
        "documenti": f"{BASE}/documenti/trasparenza/politiche2018/Doc",
        "data_elezione": "2018-03-04",
    },
}


def _clean(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def formato_ammesso(url: str) -> bool:
    return url.lower().rsplit("/", 1)[-1].endswith(ESTENSIONI_AMMESSE)


def carica_mappatura(path) -> dict:
    """Mappatura lista depositata -> partiti, validata a mano dal gruppo."""
    import json

    dati = json.loads(path.read_text(encoding="utf-8"))
    return {k: v for k, v in dati.items() if not k.startswith("_")}


def partiti_della_lista(lista: str, consultazione: str, mappatura: dict) -> list[str]:
    """Partiti a cui attribuire il programma di una lista.

    Restituisce una LISTA perche' una coalizione deposita un solo programma per
    piu' partiti: AZIONE - ITALIA VIVA - CALENDA vale per `azione` e `italia_viva`,
    ALLEANZA VERDI E SINISTRA per `europa_verde` e `sinistra_italiana`.

    Non si emette un record per partito: `harvester.scrape_metas` deduplica per
    URL, quindi il secondo record verrebbe scartato in silenzio. Il documento
    resta uno, con piu' attribuzioni — come nel layer 3, dove un articolo puo'
    contare per piu' partiti (vedi AGENTS.md sezione 5).

    Lista vuota = documento non attribuito a nessuno dei partiti seguiti: resta
    nel corpus, ma fuori dai conteggi per partito.
    """
    return mappatura.get(consultazione, {}).get(_clean(lista), [])


def parse_json_index(payload: dict, consultazione: str, mappatura: dict) -> list[dict]:
    """Programmi dall'indice JSON (schema 2022).

    Nota: esiste un campo `f_progr` dal nome invitante, ma e' `null` per tutte le
    liste (nella pagina la colonna e' commentata). I programmi stanno in `e_file`,
    filtrati per tp_doc.
    """
    documenti_base = CONSULTAZIONI[consultazione]["documenti"]
    data_elezione = CONSULTAZIONI[consultazione]["data_elezione"]
    records = []
    visti: set[str] = set()
    for lista in payload.get("contrass", []):
        for allegato in lista.get("e_file") or []:
            if allegato.get("tp_doc") != TP_DOC_PROGRAMMA:
                continue
            # `l_fasc` NON entra nel path: e' un attributo della lista, non una
            # cartella. Verificato sul server: .../Documenti/65/<file> risponde
            # 200, .../Documenti/65/A/<file> e .../Documenti/65/A<file> danno 404.
            # Il JavaScript del portale costruisce l'URL con il fascicolo, ed e'
            # per questo che quella riga e' commentata nell'originale.
            url = f"{documenti_base}/{lista['n_ord']}/{allegato['f_doc']}"
            if not formato_ammesso(url):
                continue
            # Una lista con piu' fascicoli (A/B) ripete lo stesso programma.
            if url in visti:
                continue
            visti.add(url)
            records.append(_record(url, _clean(lista.get("partito", "")),
                                   consultazione, data_elezione, mappatura))
    return records


def parse_html_index(html: str, consultazione: str, mappatura: dict) -> list[dict]:
    """Programmi dalla pagina HTML statica (schema 2018).

    Il criterio e' il testo del link, non il nome del file: e' l'etichetta
    ufficiale con cui il Viminale qualifica il documento.
    """
    data_elezione = CONSULTAZIONI[consultazione]["data_elezione"]
    soup = BeautifulSoup(html, "html.parser")
    records = []
    visti: set[str] = set()
    for tag in soup.select('a[href*="/documenti/trasparenza/"]'):
        etichetta = _clean(tag.get_text(" ", strip=True)).lower()
        if etichetta != LABEL_PROGRAMMA:
            continue
        url = urljoin(BASE, tag.get("href"))
        if not formato_ammesso(url):
            continue
        partito = _partito_da_riga(tag)
        # Nel 2018 il fascicolo E' una cartella (Doc/14, Doc/14A, Doc/14B) — al
        # contrario del 2022, dove non entra nel path. La stessa lista deposita lo
        # stesso programma per piu' circoscrizioni: stesso nome file, cartelle
        # diverse. Gli URL sono distinti, quindi deduplicare per URL non basta:
        # la chiave e' (lista, nome del file).
        chiave = f"{partito}|{url.rsplit('/', 1)[-1]}"
        if chiave in visti:
            continue
        visti.add(chiave)
        records.append(_record(url, partito, consultazione, data_elezione, mappatura))
    return records


def _partito_da_riga(tag) -> str:
    """Nome della lista: sta nella riga di tabella che contiene il link."""
    riga = tag.find_parent("tr")
    if riga is None:
        return ""
    celle = [_clean(cella.get_text(" ", strip=True)) for cella in riga.find_all("td")]
    testuali = [cella for cella in celle if len(cella) > 3 and cella.lower() != LABEL_PROGRAMMA]
    return testuali[0] if testuali else ""


def _record(url: str, partito: str, consultazione: str, data_elezione: str,
            mappatura: dict) -> dict:
    """Metadata nel formato di harvester.scrape_metas (url/domain/seendate/title).

    `partiti` e' una lista, non un id singolo: vedi partiti_della_lista.
    """
    partiti = partiti_della_lista(partito, consultazione, mappatura)
    return {
        "url": url,
        "domain": "dait.interno.gov.it",
        "seendate": f"{data_elezione}T00:00:00",
        "title": partito,
        "partiti": partiti,
        "partito_lista": partito,
        "coalizione": len(partiti) > 1,
        "tipo_documento": "programma",
        "fonte": "viminale",
        "consultazione": consultazione,
    }


def discover_programmi(session, config: dict, mappatura: dict, consultazioni=None) -> list[dict]:
    """Programmi di tutte le consultazioni richieste."""
    from src.programmi_discovery import fetch

    selected = consultazioni or list(CONSULTAZIONI)
    records: list[dict] = []
    for nome in selected:
        meta = CONSULTAZIONI[nome]
        response = fetch(session, meta["index"], config["timeout"], config["pause"])
        if response is None:
            print(f"  {nome:16s} indice non raggiungibile: {meta['index']}")
            continue
        if meta["schema"] == "json":
            try:
                found = parse_json_index(response.json(), nome, mappatura)
            except ValueError:
                print(f"  {nome:16s} indice JSON illeggibile")
                continue
        else:
            found = parse_html_index(response.text, nome, mappatura)
        attribuiti = sum(1 for r in found if r["partiti"])
        print(f"  {nome:16s} {len(found):3d} programmi ({attribuiti} attribuiti ai partiti seguiti)")
        records.extend(found)
    return records
