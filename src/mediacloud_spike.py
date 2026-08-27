"""
Media Cloud SPIKE: validating it as a historical DISCOVERY source. Media Cloud is
queryable: you search by keywords + collection + date range over ~50,000 sources
(Italian included) and get story METADATA (url, title, date, source, language) —
NOT the full text (copyright). It gives you the URLs; you fetch the text yourself
with harvester.scrape_metas.

What this spike measures:
  - how many articles per party/leader over the last 6 months in the Italy collection;
  - the SOURCE MIX of the sample (to check how much it is dominated by aggregators);
  - saves the URLs, ready for the harvester.

No domain WHITELIST (the whole Italy collection), but PURE-sport domains are
excluded (BLOCK_DOMAINS): they leaked noise through the full-text query.

--- SETUP (free, two minutes, no identity verification) --------------------
  1) create an account and grab the API key: https://search.mediacloud.org/  (user profile);
  2) pip install mediacloud
  3) export the key (no secrets in the code):
        Windows (PowerShell):  $env:MC_API_KEY="your-key"
  4) python mediacloud_spike.py
     On first run, if COLLECTION_ID is None, the script LOOKS UP the "Italy"
     collections and prints them (id + name): copy the right id into COLLECTION_ID
     and re-run.

Output:
  mediacloud_urls.jsonl  -> one article per line (url/domain/seendate/title):
                            input for the full-text step (mediacloud_fulltext.py).
  on screen: per-party counts + top sources of the sample.

Next step: python mediacloud_fulltext.py  (fetches the text + anti-sport pass).
Client docs: https://github.com/mediacloud/api-client
"""

# --- imports --------------------------------------------------------------
import os
import json
import argparse
import sys
from datetime import date, timedelta
from collections import Counter
from drive_mirror import mirror_file
from dotenv import load_dotenv

try:
    import mediacloud.api
except ImportError:
    mediacloud = None

# --- configuration --------------------------------------------------------
# .env FIRST, then the key. The other way round (which is how this file used to
# read) the key is looked up before the file is loaded, so it is always None and
# the .env support documented in the README never actually works: it only works
# when the variable is exported in the shell.
HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(os.path.dirname(HERE), ".env"))  # local key only; .env is ignored by Git
MC_API_KEY = os.environ.get("MC_API_KEY")     # see SETUP in the docstring

# Id of the "Italy - National" collection. None -> the script looks it up and prints it.
# Fill it in with the real id after the first run, then re-run.
COLLECTION_ID = 34412372   # Italy - National

# 6-month window (project decision).
END = date.today()
START = END - timedelta(days=182)

# PARTIES -> boolean query (Elasticsearch/Solr syntax, Italian full text).
# Surnames = strong signal; party forms only the unambiguous ones. One count per
# party = the "per-party coverage".
# Quotes ONLY force a phrase (adjacent words): "Forza Italia". A single token goes
# bare (M5S, FdI); quoting it does not narrow it. That is why the party's bare
# "Azione" was removed -> it matches the common word, not Calenda.
# Acronyms added only when unambiguous (FdI, PD, AVS); NO FI (Florence), NO IV (Roman numeral).
PARTIES = {
    "FdI / Meloni":                'Meloni OR "Fratelli d\'Italia" OR FdI',
    "PD / Schlein":                'Schlein OR "Partito Democratico" OR PD',  # PD ~unambiguous (rarely: Padua province code)
    "Lega / Salvini":              'Salvini OR Carroccio OR Lega',   # bare "lega" is needed (nobody says "Lega Nord" anymore); the football that slips in is removed downstream (see is_lega_sport_noise in the full-text step)
    "M5S / Conte":                 '"Movimento 5 Stelle" OR "Giuseppe Conte" OR M5S',
    "Forza Italia / Tajani":       '"Forza Italia" OR Tajani',
    "Azione / Calenda":            'Calenda',   # surname only: Calenda is the face of the party
    "Italia Viva / Renzi":         '"Italia Viva" OR Renzi',
    "AVS / Fratoianni-Bonelli":    'Fratoianni OR Bonelli OR "Alleanza Verdi Sinistra" OR "Verdi e Sinistra" OR AVS',  # bare "Bonelli": almost always Angelo B. (the comics publisher is 1 case in 72)
    "+Europa":                     '"Più Europa" OR "Piu Europa"',
    "Futuro Nazionale / Vannacci": 'Vannacci OR "Futuro Nazionale"',
}
# Combined query to extract the URL sample (OR of all of them).
COMBINED_QUERY = "(" + " OR ".join(f"({q})" for q in PARTIES.values()) + ")"

# URL sample cap. None = the WHOLE period (the real 6-month run): story_list sorts
# newest-first, so a low cap would grab only the last few days; to actually cover
# the 6 months we page until the window is exhausted.
# Set a number (e.g. 500) only for a quick test.
MAX_STORIES = None

# PURE-sport domains to exclude (do not confuse with gazzettadelsud/diparma, generalist).
BLOCK_DOMAINS = {"gazzetta.it", "corrieredellosport.it", "tuttosport.com"}

DATA = os.path.join(os.path.dirname(HERE), "data")   # repo/data (this script lives in repo/src)
URLS_OUT = os.path.join(DATA, "raw", "mediacloud_urls.jsonl")
# -------------------------------------------------------------------------


def find_italy_collections(api_key):
    """Print the collections whose name contains 'Italy' (id + name), to find the
    right id for COLLECTION_ID. Defensive: if the client method changes, explain
    how to find it by hand in the web app."""
    try:
        directory = mediacloud.api.DirectoryApi(api_key)
        res = directory.collection_list(name="Italy", limit=50)
        rows = res.get("results", res) if isinstance(res, dict) else res
        print("\nCollections containing 'Italy' (copy the right id into COLLECTION_ID):")
        for c in rows:
            print(f"  id={c.get('id')}  {c.get('name')}  (sources: {c.get('source_count','?')})")
    except Exception as ex:
        print(f"\nAutomatic lookup failed ({ex}).")
        print("Find the id by hand: https://search.mediacloud.org/ -> search for the "
              "'Italy - National' collection, the id is in the collection URL.")


def read_count(res):
    """story_count may return a dict {'relevant':..,'total':..} or an int: normalize."""
    if isinstance(res, dict):
        return res.get("relevant", res.get("count", res.get("total", 0)))
    return res or 0


def domain_of(story):
    """Source domain, from whichever field is available (media_name/media_url/url)."""
    for k in ("media_name", "media_url"):
        v = story.get(k)
        if v:
            return v
    u = story.get("url", "")
    return u.split("/")[2] if "://" in u else u


def parse_args():
    parser = argparse.ArgumentParser(description="Raccoglie URL Media Cloud per la pipeline temi politici.")
    parser.add_argument(
        "--max-stories",
        type=int,
        default=MAX_STORIES,
        help="limite di URL per smoke test; omettere per l'intero periodo",
    )
    return parser.parse_args()


def main(max_stories=MAX_STORIES):
    if mediacloud is None:
        print("Missing client -> pip install mediacloud")
        return 2
    if not MC_API_KEY:
        print("Missing MC_API_KEY (see SETUP in the docstring).")
        return 2
    if COLLECTION_ID is None:
        find_italy_collections(MC_API_KEY)
        print("\nSet COLLECTION_ID to the id you found and re-run.")
        return 2

    search = mediacloud.api.SearchApi(MC_API_KEY)
    print(f"Window: {START} -> {END} | collection: {COLLECTION_ID}")

    # 1) per-party count (cheap: no pagination). ROUGH PREVIEW: it runs on the
    #    query, so Lega is inflated by football ("lega"). The authoritative numbers
    #    come from the cleaned corpus in mediacloud_fulltext.py.
    print("\nPER-PARTY COVERAGE (rough preview, last 6 months):")
    counts = {}
    for label, q in PARTIES.items():
        try:
            n = read_count(search.story_count(q, START, END, collection_ids=[COLLECTION_ID]))
        except Exception as ex:
            n = f"error ({ex})"
        counts[label] = n
        print(f"  {str(n):>8}  {label}")

    # 2) URL sample with the combined query, paging up to max_stories
    #    (or until the 6 months are exhausted if max_stories is None).
    cap = "whole period" if max_stories is None else f"max {max_stories}"
    print(f"\nExtracting URL sample ({cap}) for the harvester...")
    sources = Counter()
    langs = Counter()
    kept = 0
    token = None
    with open(URLS_OUT, "w", encoding="utf-8") as fout:
        while max_stories is None or kept < max_stories:
            try:
                page, token = search.story_list(
                    COMBINED_QUERY, start_date=START, end_date=END,
                    collection_ids=[COLLECTION_ID], pagination_token=token)
            except Exception as ex:
                print(f"  story_list error: {ex}"); break
            for s in page:
                if max_stories is not None and kept >= max_stories:
                    break
                url = s.get("url")
                if not url:
                    continue
                # drop pure-sport domains (match on the URL host)
                host = url.split("/")[2].lower() if "://" in url else ""
                host = host[4:] if host.startswith("www.") else host
                if any(host == d or host.endswith("." + d) for d in BLOCK_DOMAINS):
                    continue
                dom = domain_of(s)
                sources[dom] += 1
                langs[s.get("language", "?")] += 1
                # format expected by harvester.scrape_metas (url/domain/seendate/title)
                pub = s.get("publish_date")   # the client returns a date object: serialize to ISO
                fout.write(json.dumps({
                    "url": url,
                    "domain": dom,
                    "seendate": pub.isoformat() if hasattr(pub, "isoformat") else pub,
                    "title": s.get("title", ""),
                }, ensure_ascii=False) + "\n")
                kept += 1
            if kept and kept % 1000 == 0:     # progress (the 6-month run is long)
                print(f"  ...{kept} URLs collected")
            if not token:      # no more pages
                break

    print(f"\nSample: {kept} URLs -> {URLS_OUT}")
    mirror_file(URLS_OUT, "raw")
    print(f"Languages in the sample: {dict(langs)}")
    print("\nTop 20 SOURCES of the sample (to see the aggregator mix):")
    for dom, n in sources.most_common(20):
        print(f"  {n:5}  {dom}")
    return 0


if __name__ == "__main__":
    sys.exit(main(parse_args().max_stories))
