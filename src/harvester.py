"""
FULL-TEXT engine: from a list of URLs (metadata) to the clean article text.
Hand-made scraper (no Scrapy), reusable and decoupled from the URL source.

- Input: METADATA (dict with at least 'url'), passed by whoever does the discovery.
  In this project that is mediacloud_fulltext.py (Media Cloud). The engine does NOT
  know where the URLs come from: the same methods serve any source.
- Full text: requests + BeautifulSoup + trafilatura (boilerplate removal),
  concurrently via ThreadPoolExecutor (what Scrapy would do in its middlewares).
- Enrichment: language (langdetect) per article.
- Provenance: every record carries `estrazione`, saying how its text was read
  ("trafilatura" | "fallback_p" for HTML, "nativa" for a PDF with a text layer).
  Records marked "fallback_p" contain site chrome, not an article: filter them
  out before any text analysis.
- Output: JSON Lines, one article per line.

Public API: scrape_metas(metas, out=..., workers=..., min_chars=...).
"""

# --- imports --------------------------------------------------------------
import requests        # HTTP (install with: pip install requests)
import json            # stdlib: dict <-> JSON text
import time            # stdlib: pauses with time.sleep()
from bs4 import BeautifulSoup   # BeautifulSoup: HTML parsing (pip install beautifulsoup4)
# ThreadPoolExecutor: runs several functions "in parallel" on multiple threads;
# as_completed: iterates results as they FINISH (not in submission order).
from concurrent.futures import ThreadPoolExecutor, as_completed

# Real-browser User-Agent: many outlets reject "script-like" User-Agents.
HEADERS = {"User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/126.0.0.0 Safari/537.36")}

# --- configuration --------------------------------------------------------
WORKERS = 24                    # concurrent downloads (I/O-bound: worth raising)
MIN_CHARS = 200                 # drop empty / paywall / placeholder pages
OUT = "articoli_fulltext.jsonl"  # default; drivers pass a specific 'out'
# -------------------------------------------------------------------------

# requests.Session(): ONE object reused for all calls. Keeps the connection open
# (faster) and remembers headers/cookies. Better than a "bare" requests.get() each time.
session = requests.Session()
session.headers.update(HEADERS)   # .update() merges this dict into the default headers


def fetch_response(url, retries=1, timeout=12):
    """Download a URL and return the whole Response (or None on failure).

    Why the Response and not just the text: a PDF is bytes. r.text would decode
    them as if they were a string and destroy the file. Callers that need bytes
    read r.content; callers that need HTML read r.text.
    """
    for i in range(retries + 1):
        try:
            r = session.get(url, timeout=timeout)
            if r.status_code == 200:
                # requests falls back to ISO-8859-1 for text/* whenever the server
                # omits the charset (RFC 2616). On Italian pages that turns "più"
                # into "piÃ¹" and "è" into "Ã¨": 1.3% of the corpus carries it.
                # It is not cosmetic — the macrotema lexicon strips diacritics to
                # match "sanità" and "sanita", and "sanitÃ " matches neither — and
                # only a fifth of it is repairable after the fact, because the
                # extraction drops the C1 continuation bytes and the information
                # is gone. Fixing it here is the only complete fix.
                # apparent_encoding sniffs the bytes instead of guessing.
                if r.encoding and r.encoding.lower() in ("iso-8859-1", "latin-1"):
                    if "charset" not in r.headers.get("Content-Type", "").lower():
                        r.encoding = r.apparent_encoding or "utf-8"
                return r
        except requests.RequestException:
            pass
        time.sleep(1 + i)
    return None


def fetch(url, retries=1):
    """Download an article's HTML, with retry + backoff. Uses the Session.

    Short timeout and a single retry: for full text a page that does not answer in
    ~12s is not worth the wait (there are thousands of URLs, many dead or very slow).

    Kept as-is (returns the body as a string) so existing callers do not change.
    """
    r = fetch_response(url, retries)
    return r.text if r is not None else None   # None = "I failed" (see scrape_one)


def is_pdf(content, content_type=""):
    """True if these bytes are a PDF.

    Checks the magic number first and the Content-Type second: a URL can serve a
    PDF without saying so in the path (and vice versa). The electoral programmes
    of the Interior Ministry are all PDFs.
    """
    if content[:5] == b"%PDF-":
        return True
    return "pdf" in (content_type or "").lower()


def extract_pdf_text(content):
    """Text of a PDF, or "" if it cannot be read.

    Returns "" instead of raising: a malformed file must not stop a run of
    hundreds of documents. scrape_one already drops records without text.

    Note: a scanned PDF has no selectable text and yields "" here. That is not a
    bug, it is the OCR case, which this project does not cover.
    """
    try:
        from pypdf import PdfReader
        from io import BytesIO
        reader = PdfReader(BytesIO(content))
        return "\n".join((page.extract_text() or "") for page in reader.pages).strip()
    except Exception:
        return ""


def parse_pdf(content, meta):
    """Extract the fields from a PDF. Same schema as parse() for HTML.

    The layer-1 corpus must be readable by the same code as the layer-3 one:
    same keys, same meaning.
    """
    text = extract_pdf_text(content)
    return {
        "url": meta.get("url"),
        "domain": meta.get("domain"),
        "seendate": meta.get("seendate"),
        # A PDF has no <title>: the title comes from the metadata (for the
        # Viminale programmes, the name of the deposited list).
        "title": meta.get("title", ""),
        "meta_description": None,       # no such thing in a PDF; key kept for schema parity
        "text": text,
        "chars": len(text),
        # Same field as the HTML path, PDF vocabulary: "nativa" = the file has a
        # real text layer. A scan yields "" here; programmi_fulltext.py then
        # overwrites this with "ocr" or "fallita".
        "estrazione": "nativa" if text else "",
    }


def _extract_body(html, soup):
    """Article body AND how it was obtained. Returns the tuple (text, estrazione).

    Two paths, and everything downstream needs to tell them apart:

    - "trafilatura": the real article body, boilerplate (menu, cookie banner,
      'related articles', footer, newsletter) already dropped;
    - "fallback_p": trafilatura found no body, so we join all the page's <p>.
      That text IS the site chrome. It is kept because a dirty record beats a
      lost URL, but it must not reach a topic model unfiltered.

    Why the flag: without it the two are indistinguishable in the JSONL, and the
    chrome is the most regular text in the whole corpus. NMF then models the page
    templates instead of the themes -- "in evidenza", "riproduzione riservata",
    "vai all'articolo" came out as 7 of our 12 topics.

    On favor_recall (was True, now dropped): it made trafilatura return
    chrome-ish text instead of nothing, which then got labelled clean. Letting
    those pages fall through to the flagged path is more useful than keeping them
    mislabelled.
    """
    try:
        import trafilatura
        body = trafilatura.extract(
            html,
            include_comments=False,   # drop reader comments
            include_tables=False,     # drop tables (often side data)
        )
        if body:
            return body, "trafilatura"
    except Exception:
        pass   # not installed or tricky page -> fallback below
    # FALLBACK: all the <p>. Dirty text beats nothing, as long as it says so.
    return "\n".join(p.get_text(" ", strip=True) for p in soup.find_all("p")), "fallback_p"


def get_meta_description(soup):
    """Page meta description: <meta name='description'> or, as a fallback, og:description.
    A light metadata signal (1-2 sentences) useful for theme detection without full text."""
    for attrs in ({"name": "description"}, {"property": "og:description"}):
        tag = soup.find("meta", attrs=attrs)
        if tag and tag.get("content"):
            return tag.get("content").strip()
    return None


def parse(html, meta):
    """Extract the fields from a page. Returns a dict (it becomes a JSONL line)."""
    soup = BeautifulSoup(html, "html.parser")   # 'soup' = navigable tree of the HTML
    # CLEAN body via trafilatura (with flagged <p> fallback): see _extract_body.
    text, estrazione = _extract_body(html, soup)
    # Returns a dict. .get("x") reads a field of the input metadata;
    # if missing, .get returns None without error.
    return {
        "url": meta.get("url"),
        "domain": meta.get("domain"),
        # 'language' is added by scrape_metas (langdetect on the text).
        "seendate": meta.get("seendate"),
        # CONDITIONAL EXPRESSION (ternary): A if condition else B.
        # If there is a <title> use it, otherwise fall back to the metadata title.
        "title": (soup.title.string or "").strip() if soup.title
                 else meta.get("title", ""),
        "meta_description": get_meta_description(soup),   # light metadata signal (see theme detection)
        "text": text,
        "chars": len(text),             # len() = length (here number of characters)
        # HOW the text was read: "trafilatura" (clean body) or "fallback_p"
        # (all the <p>, i.e. site chrome). Filter on this before any NLP.
        "estrazione": estrazione,
    }


def scrape_one(meta):
    """Download + extract ONE document. Returns the dict, or None if anything fails.

    Two branches: PDF (electoral programmes, layer 1) and HTML (everything else).
    The HTML path is unchanged — same parse(), same result — so the layer-3
    pipeline behaves exactly as before.
    """
    r = fetch_response(meta["url"])
    if r is None:
        return None
    try:
        if is_pdf(r.content, r.headers.get("content-type", "")):
            return parse_pdf(r.content, meta)
        return parse(r.text, meta)
    except Exception:                   # a malformed site must not stop everything
        return None


def scrape_metas(metas, out=OUT, workers=WORKERS, min_chars=MIN_CHARS):
    """From a list of METADATA (dict with at least 'url') -> full text (+ language).

    It is the core of the harvester, decoupled from the source: it does NOT know
    where the URLs come from. The discovery driver passes them (here
    mediacloud_fulltext.py, which reads the URLs produced by mediacloud_spike.py).
    Returns the list of saved records.
    """
    # 1) dedup by URL (the same page can arrive from different slices/languages).
    # A set() is a collection with NO duplicates and very fast lookup:
    # perfect for remembering the URLs already seen.
    seen, uniq = set(), []
    for m in metas:
        u = m.get("url")
        if u and u not in seen:         # if there is a URL and I have not seen it yet
            seen.add(u)                 # .add() on a set
            uniq.append(m)              # .append() on a list
    print(f"\nUnique URLs: {len(uniq)} (from {len(metas)} raw)")

    # 2) full text concurrently, with INCREMENTAL WRITING: every downloaded page
    #    goes to disk RIGHT AWAY (not yet enriched). This way a crash
    #    mid-run does not lose the download work (the slow part).
    #    'enumerate(..., 1)' numbers the futures as they finish -> progress.
    recs = []
    with open(out, "w", encoding="utf-8") as f, \
         ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(scrape_one, m) for m in uniq]
        for done, fut in enumerate(as_completed(futures), 1):
            rec = fut.result()          # .result() = the value returned by scrape_one
            if rec and rec["chars"] > min_chars:
                recs.append(rec)
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            if done % 250 == 0:         # every 250: print progress and flush
                f.flush()
                print(f"  ...{done}/{len(uniq)} downloaded, {len(recs)} with text")
    print(f"Articles with text: {len(recs)}")

    # 3) ENRICHMENT (outside the threads): language from text with langdetect.
    #    seed=0 -> reproducible; single-thread because langdetect is NOT thread-safe.
    #    detect() may raise on ambiguous texts.
    try:
        from langdetect import detect, DetectorFactory
        DetectorFactory.seed = 0
        for rec in recs:
            try:
                rec["language"] = detect(rec["text"][:1000])
            except Exception:
                rec["language"] = "unknown"   # empty/ambiguous text
        print("Language detected for every article.")
    except Exception as e:
        print(f"language skipped ({e}) -> pip install langdetect")

    # 4) final JSONL rewrite with the enriched field (language).
    #    Always executed; ensure_ascii=False keeps the accents.
    with open(out, "w", encoding="utf-8") as f:
        for rec in recs:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"Saved {len(recs)} articles to {out}")
    return recs
