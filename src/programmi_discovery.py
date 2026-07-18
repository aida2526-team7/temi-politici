"""Discovery dei documenti diretti dei partiti (layer 1: "cosa dicono").

Trova gli URL dei programmi elettorali e dei comunicati sui siti ufficiali dei
partiti, sia nella versione corrente sia nelle copie storiche della Wayback
Machine, e li salva come metadata JSONL.

Questo modulo fa SOLO discovery. Il download e l'estrazione del testo sono di
`src/harvester.py`, il motore condiviso con il layer 3 (stampa): i metadata
prodotti qui hanno il formato che `harvester.scrape_metas` si aspetta
(url/domain/seendate/title), più i campi propri del layer 1.

  src/programmi_discovery.py  -> data/raw/programmi_urls.jsonl      (QUESTO modulo)
  src/programmi_fulltext.py   -> data/raw/programmi_fulltext.jsonl  (driver + harvester)

Il tipo del documento (`tipo_documento`) e' un'etichetta di provenienza
strutturale, non un tema: i temi restano competenza del topic model.
"""

from __future__ import annotations

import json
import re
import time
import unicodedata
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse
from xml.etree import ElementTree

import requests
from bs4 import BeautifulSoup


CDX_ENDPOINT = "https://web.archive.org/cdx/search/cdx"

# Ultimo segmento del path che identifica la pagina-programma di un partito.
PROGRAM_STEMS = frozenset({
    "programma", "programmi", "il programma", "i programmi", "il nostro programma",
    "programma elettorale", "programma di governo", "manifesto", "il manifesto",
    "manifesto elettorale", "programma politico",
})

# Testo del link che identifica un programma anche quando l'URL non lo dice.
PROGRAM_ANCHORS = frozenset({
    "programma", "programmi", "il programma", "il nostro programma",
    "programma elettorale", "leggi il programma", "scarica il programma",
    "manifesto", "il manifesto", "programma di governo",
})

# Termini che nel nome di un PDF indicano un programma.
PROGRAM_FILE_TERMS = ("programma", "programmi", "manifesto")

# Pagine di servizio: le uniche che NON sono comunicazione politica.
#
# Il sito di un partito e' comunicazione diretta per definizione: il default e'
# 'comunicato', non 'altro'. Filtrare i comunicati richiedendo che contengano
# termini programmatici li perderebbe quasi tutti, perche' un comunicato parla di
# qualsiasi cosa (un'autostrada, una sede inaugurata) senza mai dire "programma".
SERVICE_TERMS = (
    "privacy", "cookie", "statuto", "tesseramento", "tessera", "donazione",
    "donazioni", "regolamento", "informativa", "credits", "sitemap",
    "note legali", "accessibilita", "contatti", "newsletter", "iscriviti",
    "login", "area riservata", "carrello", "shop",
)

# Host non di produzione, da escludere anche se sotto un dominio di partito.
IGNORE_HOST_PREFIXES = ("test.", "staging.", "stage.", "dev.", "preprod.", "preview.")

# Estensioni che non sono documenti testuali: immagini, media, archivi, fogli.
BLOCKED_EXTENSIONS = frozenset({
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".ico", ".bmp", ".tiff",
    ".mp3", ".mp4", ".avi", ".mov", ".wmv", ".mkv", ".wav", ".ogg", ".webm",
    ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2",
    ".xls", ".xlsx", ".csv", ".ppt", ".pptx", ".doc", ".docx",
    ".woff", ".woff2", ".ttf", ".eot", ".css", ".js", ".json", ".xml", ".rss",
})

SCORE_PROGRAMMA = 100
SCORE_COMUNICATO = 10
SCORE_ALTRO = 0
SCORE_BONUS_PDF = 10
SCORE_BONUS_ANNO = 5

ELECTION_YEARS = ("2018", "2019", "2022", "2024", "2026")


# --- normalizzazione ------------------------------------------------------

def normalize_url(url: str) -> str:
    """URL senza fragment, con host minuscolo e senza slash ripetuti."""
    parsed = urlparse(url.strip())
    path = re.sub(r"/{2,}", "/", parsed.path or "/")
    return urlunparse((parsed.scheme or "https", parsed.netloc.lower(), path, "", parsed.query, ""))


def canonical_key(url: str) -> str:
    """Chiave che identifica la stessa pagina a prescindere da schema e www.

    Le copie Wayback sono quasi sempre http://, le pagine correnti https://:
    senza questa chiave la stessa pagina risulterebbe due documenti diversi.
    """
    parsed = urlparse(normalize_url(url))
    host = parsed.netloc
    if host.startswith("www."):
        host = host[4:]
    path = parsed.path.rstrip("/")
    return f"{host}{path}{('?' + parsed.query) if parsed.query else ''}"


def normalize_text(value: str) -> str:
    """Testo minuscolo, senza accenti, con i separatori ridotti a spazi.

    Serve a confrontare i segmenti di URL ('programma-elettorale') e il testo dei
    link con gli stessi termini.
    """
    decomposed = unicodedata.normalize("NFKD", value.lower())
    stripped = "".join(char for char in decomposed if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", " ", stripped).strip()


def has_word(normalized: str, term: str) -> bool:
    """Match con confini di parola: 'cronoprogramma' non contiene 'programma'."""
    return re.search(rf"(?<!\w){re.escape(term)}(?!\w)", normalized) is not None


def host_of(url: str) -> str:
    return urlparse(url).netloc.lower()


def host_in_domains(host: str, domains) -> bool:
    """True se l'host appartiene a uno dei domini, sottodomini inclusi.

    Stessa regola di BLOCK_DOMAINS in mediacloud_spike.py. Gli host non di
    produzione (test., staging., ...) restano fuori.
    """
    host = host.lower()
    if host.startswith("www."):
        host = host[4:]
    if any(host.startswith(prefix) for prefix in IGNORE_HOST_PREFIXES):
        return False
    return any(host == domain or host.endswith("." + domain) for domain in domains)


def path_segments(url: str) -> list[str]:
    return [segment for segment in urlparse(url).path.split("/") if segment]


def _stem_and_extension(url: str) -> tuple[str, str]:
    segments = path_segments(url)
    if not segments:
        return "", ""
    last = segments[-1]
    if "." not in last:
        return last, ""
    stem, _, extension = last.rpartition(".")
    return stem, f".{extension.lower()}"


def is_supported_document(url: str) -> bool:
    """HTML e PDF sono documenti; immagini, media e fogli di calcolo no."""
    _, extension = _stem_and_extension(url)
    return extension not in BLOCKED_EXTENSIONS


# --- tipizzazione e punteggio ---------------------------------------------

def document_type(url: str, anchor: str = "") -> str:
    """Classifica un URL in programma / comunicato / altro.

    E' provenienza strutturale, non un tema: dice da dove viene il documento, non
    di cosa parla. I temi restano competenza del topic model.

    - `programma`: documento programmatico. Pochi per partito, preziosi.
    - `comunicato`: qualsiasi altro contenuto del sito. E' il default, perche' il
      sito di un partito e' comunicazione diretta.
    - `altro`: pagine di servizio e homepage. Si scartano.
    """
    segments = path_segments(url)
    if not segments:
        return "altro"  # homepage: indice, non un documento

    path_normalized = normalize_text(urlparse(url).path)
    anchor_normalized = normalize_text(anchor)
    blob = f"{path_normalized} {anchor_normalized}".strip()

    if any(has_word(blob, term) for term in SERVICE_TERMS):
        return "altro"

    stem, extension = _stem_and_extension(url)
    stem_normalized = normalize_text(stem)

    if stem_normalized in PROGRAM_STEMS:
        return "programma"
    if anchor_normalized in PROGRAM_ANCHORS:
        return "programma"
    if extension == ".pdf" and any(has_word(stem_normalized, term) for term in PROGRAM_FILE_TERMS):
        return "programma"
    return "comunicato"


def score_candidate(url: str, anchor: str = "") -> int:
    """Punteggio di pertinenza. Sostituisce l'ordinamento alfabetico, che
    riempiva i posti disponibili con i comunicati in ordine di lettera."""
    tipo = document_type(url, anchor)
    score = {"programma": SCORE_PROGRAMMA, "comunicato": SCORE_COMUNICATO}.get(tipo, SCORE_ALTRO)
    if score == SCORE_ALTRO:
        return score
    _, extension = _stem_and_extension(url)
    if extension == ".pdf":
        score += SCORE_BONUS_PDF
    if any(year in url for year in ELECTION_YEARS):
        score += SCORE_BONUS_ANNO
    return score


def select_candidates(candidates: list[dict], max_programmi: int, max_comunicati: int) -> list[dict]:
    """Seleziona con budget separati per tipo.

    I programmi hanno un budget proprio: non competono con i comunicati, che sono
    ordini di grandezza piu' numerosi (7.728 URL nella sitemap di un partito
    reale). Senza budget separati i comunicati riempirebbero i posti e il
    programma resterebbe fuori.

    I comunicati si ordinano per `lastmod` decrescente: i piu' recenti. E' un
    criterio di campionamento esplicito, e allinea il layer 1 alla finestra
    temporale del corpus stampa. Gli 'altro' non vengono raccolti.
    """
    def with_score(candidate: dict) -> int:
        return candidate.get("score", score_candidate(candidate["url"], candidate.get("anchor", "")))

    def subset(tipo: str) -> list[dict]:
        return [c for c in candidates if c.get("tipo_documento") == tipo]

    programmi = subset("programma")
    programmi.sort(key=lambda c: (-with_score(c), c["url"]))

    # sort stabile applicato in ordine inverso di priorita': lastmod domina.
    comunicati = subset("comunicato")
    comunicati.sort(key=lambda c: c["url"])
    comunicati.sort(key=with_score, reverse=True)
    comunicati.sort(key=lambda c: c.get("lastmod") or "", reverse=True)

    return programmi[:max_programmi] + comunicati[:max_comunicati]


# --- sitemap e link -------------------------------------------------------

def _child_text(element, name: str) -> str:
    for child in element:
        if child.tag.endswith("}" + name) or child.tag == name:
            return (child.text or "").strip()
    return ""


def parse_sitemap(content: bytes) -> tuple[list[str], list[dict]]:
    """Legge una sitemap XML con la stdlib.

    Ritorna (sitemap annidate, pagine), dove ogni pagina e' {loc, lastmod}.
    `lastmod` serve a ordinare i comunicati per data: senza, la selezione
    ricadrebbe sull'ordine alfabetico.

    Usa ElementTree e non BeautifulSoup(..., 'xml'): quest'ultimo richiede lxml,
    che non e' tra le dipendenze del progetto e fallirebbe in silenzio.
    """
    try:
        root = ElementTree.fromstring(content)
    except ElementTree.ParseError:
        return [], []

    is_index = root.tag.endswith("sitemapindex")
    sitemaps: list[str] = []
    pages: list[dict] = []
    for element in root:
        location = _child_text(element, "loc")
        if not location:
            continue
        if is_index:
            sitemaps.append(location)
        else:
            pages.append({"loc": location, "lastmod": _child_text(element, "lastmod")})
    return sitemaps, pages


def extract_links(html: str, base_url: str) -> list[tuple[str, str]]:
    """Link della pagina come (url assoluto, testo del link)."""
    soup = BeautifulSoup(html, "html.parser")
    links: list[tuple[str, str]] = []
    seen: set[str] = set()
    for tag in soup.select("a[href], iframe[src], embed[src], object[data]"):
        target = tag.get("href") or tag.get("src") or tag.get("data") or ""
        if not target:
            continue
        url = normalize_url(urljoin(base_url, target))
        if url in seen:
            continue
        seen.add(url)
        links.append((url, tag.get_text(" ", strip=True)))
    return links


# --- Wayback --------------------------------------------------------------

def cdx_params(domain: str, dal: int, al: int, limit: int) -> dict:
    """Parametri per l'indice CDX.

    Il filtro regex e' case-insensitive: senza (?i) i PDF chiamati
    'Programma_Elettorale.pdf' sarebbero invisibili. Il campionamento mensile e'
    fatto da sample_monthly lato client, quindi qui si collassa solo sul digest
    (copie identiche consecutive).
    """
    return {
        "url": domain,
        "matchType": "domain",
        "from": str(dal),
        "to": str(al),
        "output": "json",
        "fl": "timestamp,original,mimetype,statuscode,digest",
        "filter": [
            "statuscode:200",
            "!mimetype:warc/revisit",
            "original:(?i).*(programma|manifesto|proposte|agenda).*",
        ],
        "collapse": ["digest"],
        "limit": str(limit),
    }


def parse_cdx_rows(rows: list) -> list[dict]:
    """Converte la risposta CDX (prima riga = intestazione) in dizionari."""
    if not rows or len(rows) < 2:
        return []
    header = rows[0]
    return [dict(zip(header, row)) for row in rows[1:]]


def sample_monthly(captures: list[dict]) -> list[dict]:
    """Al massimo una copia per URL e per mese: l'ultima del mese.

    Contiene il numero di richieste senza perdere le versioni: di un programma
    interessa l'evoluzione, non la copia giornaliera.
    """
    grouped: dict[tuple[str, str], list[dict]] = {}
    for capture in captures:
        key = (canonical_key(capture["original"]), capture["timestamp"][:6])
        grouped.setdefault(key, []).append(capture)
    sampled = []
    for items in grouped.values():
        items.sort(key=lambda item: item["timestamp"])
        sampled.append(items[-1])
    return sorted(sampled, key=lambda item: item["timestamp"])


def wayback_seendate(timestamp: str) -> str:
    """Timestamp Wayback -> ISO 8601, lo stesso formato di seendate nel layer 3."""
    return datetime.strptime(timestamp, "%Y%m%d%H%M%S").isoformat()


def wayback_url(timestamp: str, original: str) -> str:
    """URL della copia archiviata, contenuto originale non riscritto (id_)."""
    return f"https://web.archive.org/web/{timestamp}id_/{original}"


# --- rete -----------------------------------------------------------------

def build_session(user_agent: str) -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": user_agent, "Accept-Language": "it-IT,it;q=0.9"})
    return session


def fetch(session: requests.Session, url: str, timeout: int, pause: float,
          allow_403: bool = False, method: str = "GET", **kwargs):
    """GET con pausa e un solo retry. Ritorna la Response o None.

    Non insiste sui 4xx (tranne 429): una pagina che non c'e' non comparira' al
    secondo tentativo.

    `allow_403` restituisce anche le risposte 403 invece di None: serve a chi deve
    distinguere "risorsa assente" da "bot rifiutato" (es. la challenge di
    Cloudflare). Di default resta fuori, perche' per scaricare un documento un 403
    e' un fallimento come un altro.

    `method="HEAD"` verifica che una risorsa esista senza scaricarla: su 68 PDF da
    qualche MB la differenza e' fra secondi e minuti.
    """
    for attempt in range(2):
        try:
            time.sleep(pause)
            response = session.request(method, url, timeout=timeout, **kwargs)
            if response.status_code == 200:
                return response
            if response.status_code == 429:
                time.sleep(30 * (attempt + 1))
                continue
            if response.status_code == 403 and allow_403:
                return response
            if 400 <= response.status_code < 500:
                return None
        except requests.RequestException:
            pass
    return None


def collect_sitemap_pages(session, root_url, domains, config) -> list[dict]:
    """Pagine trovate nelle sitemap del sito, seguendo le sitemap annidate.

    Ogni pagina e' {loc, lastmod}.
    """
    base = f"{urlparse(root_url).scheme}://{urlparse(root_url).netloc}"
    queue = [urljoin(base, "/sitemap_index.xml"), urljoin(base, "/sitemap.xml")]
    visited: set[str] = set()
    pages: list[dict] = []
    while queue and len(visited) < config["max_sitemaps"]:
        sitemap_url = queue.pop(0)
        if sitemap_url in visited:
            continue
        visited.add(sitemap_url)
        response = fetch(session, sitemap_url, config["timeout"], config["pause"])
        if response is None:
            continue
        nested, found = parse_sitemap(response.content)
        queue.extend(nested)
        pages.extend(page for page in found if host_in_domains(host_of(page["loc"]), domains))
    return pages


def collect_page_links(session, url, domains, config) -> list[tuple[str, str]]:
    """Link interni di una pagina, con il testo del link."""
    response = fetch(session, url, config["timeout"], config["pause"])
    if response is None:
        return []
    return [
        (link, anchor)
        for link, anchor in extract_links(response.text, response.url)
        if host_in_domains(host_of(link), domains)
    ]


def collect_wayback_captures(session, domain, config) -> list[dict]:
    """Copie storiche di un dominio, una per URL e per mese."""
    params = cdx_params(domain, config["dal"], config["al"], config["max_wayback"])
    response = fetch(session, CDX_ENDPOINT, config["timeout"], config["pause"], params=params)
    if response is None:
        return []
    try:
        rows = response.json()
    except ValueError:
        return []
    return sample_monthly(parse_cdx_rows(rows))


def discover_party(session, party: dict, config: dict) -> list[dict]:
    """Metadata dei documenti di un partito: correnti e storici."""
    domains = frozenset(domain.lower() for domain in party["domini"])
    candidates: dict[str, dict] = {}

    def add(url: str, anchor: str, fonte: str, seendate: str, acquisition: str,
            lastmod: str = "") -> None:
        url = normalize_url(url)
        if not is_supported_document(url) or not host_in_domains(host_of(url), domains):
            return
        tipo = document_type(url, anchor)
        if tipo == "altro":
            return
        key = f"{canonical_key(url)}|{seendate}"
        if key in candidates:
            # Un URL puo' arrivare sia dalla sitemap sia da un link: tiene il
            # lastmod, che solo la sitemap conosce.
            if lastmod and not candidates[key].get("lastmod"):
                candidates[key]["lastmod"] = lastmod
            return
        candidates[key] = {
            "url": acquisition,
            "domain": host_of(url).removeprefix("www."),
            "seendate": seendate,
            "title": "",
            "partito_id": party["id"],
            "coalizione": party.get("coalizione", ""),
            "tipo_documento": tipo,
            "fonte": fonte,
            "url_originale": url,
            "anchor": anchor,
            "lastmod": lastmod,
            "score": score_candidate(url, anchor),
        }

    oggi = datetime.now().isoformat(timespec="seconds")

    # Correnti: seed espliciti (mai filtrati: se sono in configurazione, li vogliamo),
    # sitemap e link della homepage.
    for seed in party["url"]:
        seed_url = normalize_url(seed)
        if is_supported_document(seed_url) and path_segments(seed_url):
            add(seed_url, "il programma", "corrente", oggi, seed_url)

    for root_url in party["url"]:
        for page in collect_sitemap_pages(session, root_url, domains, config):
            add(page["loc"], "", "corrente", oggi, page["loc"], page.get("lastmod", ""))
        for link, anchor in collect_page_links(session, root_url, domains, config):
            add(link, anchor, "corrente", oggi, link)

    correnti = select_candidates(
        [c for c in candidates.values() if c["fonte"] == "corrente"],
        config["max_programmi"],
        config["max_comunicati"],
    )

    # Storici: Wayback, una copia per URL e per mese.
    storici: list[dict] = []
    if config.get("wayback", True):
        wayback_candidates: dict[str, dict] = {}
        for domain in domains:
            for capture in collect_wayback_captures(session, domain, config):
                original = capture["original"]
                if not is_supported_document(original):
                    continue
                if not host_in_domains(host_of(original), domains):
                    continue
                tipo = document_type(original)
                if tipo == "altro":
                    continue
                timestamp = capture["timestamp"]
                key = f"{canonical_key(original)}|{timestamp}"
                wayback_candidates[key] = {
                    "url": wayback_url(timestamp, original),
                    "domain": host_of(original).removeprefix("www."),
                    "seendate": wayback_seendate(timestamp),
                    "title": "",
                    "partito_id": party["id"],
                    "coalizione": party.get("coalizione", ""),
                    "tipo_documento": tipo,
                    "fonte": "wayback",
                    "url_originale": original,
                    "anchor": "",
                    # Per le copie storiche la data della cattura e' il criterio
                    # di ordinamento: la sitemap di allora non c'e' piu'.
                    "lastmod": wayback_seendate(timestamp),
                    "score": score_candidate(original),
                }
        storici = select_candidates(
            list(wayback_candidates.values()),
            config["max_programmi_wayback"],
            config["max_comunicati_wayback"],
        )

    return correnti + storici


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_metadata(records: list[dict], out_path: Path) -> Path:
    """Scrive i metadata in JSONL, il formato che harvester.scrape_metas legge."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    return out_path


def discover(config: dict, parties: list[dict], session=None) -> list[dict]:
    """Discovery su tutti i partiti selezionati."""
    session = session or build_session(config["user_agent"])
    records: list[dict] = []
    for party in parties:
        found = discover_party(session, party, config)
        records.extend(found)
        print(f"  {party['id']:20s} {len(found):4d} documenti "
              f"({sum(1 for r in found if r['tipo_documento'] == 'programma')} programmi)")
    return records
