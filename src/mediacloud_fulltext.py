"""
Media Cloud full-text driver: closes the spike -> scraping -> cleaning pipeline.

  mediacloud_spike.py   -> mediacloud_urls.jsonl   (URLs + metadata, one article per line)
  THIS script           -> mediacloud_fulltext.jsonl (full text + language)

Reads the spike's URLs, passes them to harvester.scrape_metas (the shared scraping
engine) and then applies the ANTI-SPORT PASS on the Lega branch only.

Why the pass: in the spike query the Lega branch includes bare "lega", because
nobody writes "Lega Nord" anymore and without that word Lega-on-its-own would never
be caught. But "lega" is also football (Serie A, Lega Pro, Lega Serie A): over the
whole Italy collection some sport pieces slip in purely on "lega". We remove them
HERE, downstream, where the full text lets us decide for sure.

The drop is SURGICAL (see is_lega_sport_noise): an article falls only if
  (1) it enters via bare "lega", NOT via Salvini/Carroccio;
  (2) it contains no other party term;
  (3) it has sport vocabulary.
So a political piece using football as a metaphor stays; a match report that
mentions "la lega di Serie A" is dropped.

Usage:  python mediacloud_fulltext.py
Prerequisite: having run mediacloud_spike.py (produces mediacloud_urls.jsonl).
"""

import os
import re
import json
from harvester import scrape_metas   # reuse the full-text engine (download + language)
from drive_mirror import mirror_file

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")   # repo/data (this script lives in repo/src)
URLS_IN = os.path.join(DATA, "raw", "mediacloud_urls.jsonl")
FULLTEXT_OUT = os.path.join(DATA, "raw", "mediacloud_fulltext.jsonl")
COVERAGE_OUT = os.path.join(DATA, "processed", "mediacloud_coverage.csv")   # per-party coverage

# Per-party coverage computed ON THE CLEAN CORPUS (not via the API's story_count,
# which on the Lega branch is inflated by football). Mirrors PARTIES in
# mediacloud_spike.py, but here as REGEX with word boundaries: bare-substring "lega"
# would match collega/legale/allegato. One article can count for several parties
# (the percentages do not add up to 100: they are the share of the sample that
# mentions each one).
PARTY_PATTERNS = {
    "FdI / Meloni":                re.compile(r"\bmeloni\b|fratelli d'italia|\bfdi\b", re.I),
    "PD / Schlein":                re.compile(r"\bschlein\b|partito democratico|\bpd\b", re.I),
    "Lega / Salvini":              re.compile(r"\bsalvini\b|carroccio|\blega\b", re.I),
    "M5S / Conte":                 re.compile(r"movimento 5 stelle|giuseppe conte|\bm5s\b", re.I),
    "Forza Italia / Tajani":       re.compile(r"forza italia|\btajani\b", re.I),
    "Azione / Calenda":            re.compile(r"\bcalenda\b", re.I),
    "Italia Viva / Renzi":         re.compile(r"italia viva|\brenzi\b", re.I),
    "AVS / Fratoianni-Bonelli":    re.compile(r"\bfratoianni\b|\bbonelli\b|alleanza verdi|verdi e sinistra|\bavs\b", re.I),
    "+Europa":                     re.compile(r"pi[uù] europa", re.I),
    "Futuro Nazionale / Vannacci": re.compile(r"\bvannacci\b|futuro nazionale", re.I),
}

# --- terms for the "lega only" scoping (aligned with PARTIES in mediacloud_spike.py) ---
LEGA_BARE = re.compile(r"\blega\b", re.I)             # the leak: common word
LEGA_STRONG = re.compile(r"\bsalvini\b|carroccio", re.I)   # the real Lega, unambiguous
OTHER_PARTIES = re.compile("|".join([                  # the other 9 branches of the query
    r"\bmeloni\b", r"fratelli d'italia", r"\bfdi\b",
    r"\bschlein\b", r"partito democratico", r"\bpd\b",
    r"movimento 5 stelle", r"giuseppe conte", r"\bm5s\b",
    r"forza italia", r"\btajani\b", r"\bcalenda\b",
    r"italia viva", r"\brenzi\b",
    r"\bfratoianni\b", r"\bbonelli\b", r"alleanza verdi", r"verdi e sinistra", r"\bavs\b",
    r"pi[uù] europa", r"\bvannacci\b", r"futuro nazionale",
]), re.I)

# Sport vocabulary: if present (and the only political hook is "lega") -> noise.
SPORT = re.compile(r"\b(serie a|serie b|serie c|lega pro|lega serie|lega calcio|lega basket|"
                   r"lega volley|campionato|scudetto|calciomercato|calciator|allenator|"
                   r"attaccant|centrocampist|difensor|portier|gol|goal|arbitr|pallone|"
                   r"coppa italia|champions|europa league|retrocess|playoff|pallavol|"
                   r"pallacanestr|volley|basket|tennis|atp|wta)\b", re.I)


def is_lega_sport_noise(rec):
    """True = drop. True ONLY for sport that entered via bare 'lega' and nothing else.
    Tested: 0 false positives over the ~900 political articles of the colleagues' sample."""
    blob = (rec.get("title", "") + " " + rec.get("text", "")).lower()
    if not LEGA_BARE.search(blob):     return False   # not a lega article
    if LEGA_STRONG.search(blob):       return False   # real Lega (Salvini/Carroccio)
    if OTHER_PARTIES.search(blob):     return False   # political via another term
    return bool(SPORT.search(blob))                    # only 'lega' + sport -> noise


def main():
    # 1) spike URLs -> list of metadata (the format scrape_metas already expects).
    if not os.path.exists(URLS_IN):
        print(f"Missing {URLS_IN}: run mediacloud_spike.py first."); return
    metas = []
    with open(URLS_IN, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                metas.append(json.loads(line))
    print(f"Input URLs: {len(metas)}")

    # 2) full text: scrape_metas downloads, enriches (language) and already
    #    writes FULLTEXT_OUT. It returns the records: we filter and rewrite them clean.
    recs = scrape_metas(metas, out=FULLTEXT_OUT)

    # 3) anti-sport pass on the Lega branch.
    kept = [r for r in recs if not is_lega_sport_noise(r)]
    dropped = len(recs) - len(kept)

    # 4) rewrite the file without the noise.
    with open(FULLTEXT_OUT, "w", encoding="utf-8") as f:
        for r in kept:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"\nAnti-sport pass ('lega' branch only): dropped {dropped} articles.")
    print(f"Final full text: {len(kept)} articles -> {FULLTEXT_OUT}")
    mirror_file(FULLTEXT_OUT, "raw")

    # 5) PER-PARTY COVERAGE on the CLEAN corpus (authoritative source, not the API's
    #    story_count). One article can count for several parties.
    blobs = [(r.get("title", "") + " " + r.get("text", "")).lower() for r in kept]
    cov = {label: sum(1 for b in blobs if rx.search(b))
           for label, rx in PARTY_PATTERNS.items()}
    n = len(kept) or 1
    rows = sorted(cov.items(), key=lambda kv: kv[1], reverse=True)
    print("\nPER-PARTY COVERAGE (articles, % of the clean corpus):")
    with open(COVERAGE_OUT, "w", encoding="utf-8") as f:
        f.write("party,articles,pct\n")
        for label, c in rows:
            print(f"  {c:5}  {100*c/n:5.1f}%  {label}")
            f.write(f"{label},{c},{round(100*c/n, 2)}\n")
    print(f"-> {COVERAGE_OUT}")
    mirror_file(COVERAGE_OUT, "processed")


if __name__ == "__main__":
    main()
