"""
FULL-TEXT engine: from a list of URLs (metadata) to the clean article text.
Hand-made scraper (no Scrapy), reusable and decoupled from the URL source.

- Input: METADATA (dict with at least 'url'), passed by whoever does the discovery.
  In this project that is mediacloud_fulltext.py (Media Cloud). The engine does NOT
  know where the URLs come from: the same methods serve any source.
- Full text: requests + BeautifulSoup + trafilatura (boilerplate removal),
  concurrently via ThreadPoolExecutor (what Scrapy would do in its middlewares).
- Enrichment: language (langdetect) per article.
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


def fetch(url, retries=1):
    """Download an article's HTML, with retry + backoff. Uses the Session.

    Short timeout and a single retry: for full text a page that does not answer in
    ~12s is not worth the wait (there are thousands of URLs, many dead or very slow).
    """
    for i in range(retries + 1):
        try:
            r = session.get(url, timeout=12)
            if r.status_code == 200:
                return r.text           # r.text = the page body as a string
        except requests.RequestException:
            pass
        time.sleep(1 + i)
    return None                         # None = "I failed" (see scrape_one)


def _extract_body(html, soup):
    """Extract ONLY the article body, dropping the boilerplate (menu, cookie banner,
    'related articles', footer, newsletter, captions).

    Why: the old method grabbed ALL the page's <p> -> any text analysis read a mush
    (title + 'Accept cookies' + links to other pieces). Boilerplate pollutes topic
    modeling and every downstream NLP step. trafilatura is the standard for
    boilerplate removal, multilingual.

    If trafilatura is not installed or finds no body, fall back to the old join of
    all <p>: the code still runs, just less clean.
    """
    try:
        import trafilatura
        body = trafilatura.extract(
            html,
            include_comments=False,   # drop reader comments
            include_tables=False,     # drop tables (often side data)
            favor_recall=True,        # prefer keeping real text over losing it
        )
        if body:
            return body
    except Exception:
        pass   # not installed or tricky page -> fallback below
    # FALLBACK: old method (all the <p>). Dirty text beats nothing.
    return "\n".join(p.get_text(" ", strip=True) for p in soup.find_all("p"))


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
    # CLEAN body via trafilatura (with <p> fallback): see _extract_body.
    text = _extract_body(html, soup)
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
    }


def scrape_one(meta):
    """Download + extract ONE article. Returns the dict, or None if anything fails."""
    html = fetch(meta["url"])
    if not html:                        # 'if not html' = if html is None/empty
        return None
    try:
        return parse(html, meta)
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
