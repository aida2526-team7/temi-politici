#!/usr/bin/env python3
"""Ricognizione delle sitemap dei siti di partito (layer 1).

Risponde a tre domande prima di progettare la discovery, invece di ipotizzarle:

1. quali siti espongono un sitemap index, e dove;
2. quali sono WordPress, e se separano i post (comunicati) dalle pagine;
3. se `lastmod` e' popolato con date vere e in che intervallo.

Sola lettura: nessuna pagina di contenuto viene scaricata, solo le sitemap.
Output in reports/layer1_recon/.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse


REPO_HINT = Path(__file__).resolve().parents[1]
if str(REPO_HINT) not in sys.path:
    sys.path.insert(0, str(REPO_HINT))

from src.programmi_discovery import build_session, fetch, load_config, parse_sitemap

# Nomi di sitemap che identificano il generatore e il tipo di contenuto.
POST_HINTS = ("post-sitemap", "wp-sitemap-posts-post", "sitemap-posts", "news-sitemap")
PAGE_HINTS = ("page-sitemap", "wp-sitemap-posts-page", "sitemap-pages")
WORDPRESS_HINTS = ("wp-sitemap", "post-sitemap", "page-sitemap", "wp-content")

CANDIDATE_SITEMAPS = ("/sitemap_index.xml", "/sitemap.xml", "/wp-sitemap.xml", "/sitemap-index.xml")


def sitemaps_from_robots(session, base: str, config: dict) -> list[str]:
    """Sitemap dichiarate in robots.txt: il posto canonico dove cercarle."""
    response = fetch(session, urljoin(base, "/robots.txt"), config["timeout"], config["pause"])
    if response is None:
        return []
    return re.findall(r"(?im)^\s*sitemap:\s*(\S+)", response.text)


def classify_sitemap(url: str) -> str:
    lowered = url.lower()
    if any(hint in lowered for hint in POST_HINTS):
        return "post"
    if any(hint in lowered for hint in PAGE_HINTS):
        return "page"
    return "altro"


def probe_party(session, party: dict, config: dict) -> dict:
    base = f"{urlparse(party['url'][0]).scheme}://{urlparse(party['url'][0]).netloc}"
    result = {
        "id": party["id"],
        "base": base,
        "index_url": "",
        "children": [],
        "wordpress": False,
        "post_sitemap": "",
        "page_sitemap": "",
        "post_sitemap_pagine": 0,
        "post_urls": 0,
        "lastmod_presenti": 0,
        "lastmod_giorni_distinti": 0,
        "lastmod_campione": [],
        "lastmod_min": "",
        "lastmod_max": "",
        "note": "",
    }

    candidates = list(CANDIDATE_SITEMAPS) + sitemaps_from_robots(session, base, config)
    children: list[str] = []
    bloccato = False
    for candidate in candidates:
        url = candidate if candidate.startswith("http") else urljoin(base, candidate)
        response = fetch(session, url, config["timeout"], config["pause"], allow_403=True)
        if response is None:
            continue
        # Un 403 con la challenge di Cloudflare non significa "sitemap assente":
        # significa "il sito rifiuta i bot". Distinguere le due cose evita di
        # concludere che un sito non abbia una sitemap che invece ha.
        if response.status_code == 403 or "Just a moment" in response.text[:600]:
            bloccato = True
            continue
        nested, pages = parse_sitemap(response.content)
        if nested:
            result["index_url"] = url
            children = nested
            break
        if pages:
            result["index_url"] = url
            children = [url]  # sitemap piatta: e' essa stessa la lista di pagine
            break

    if not children:
        result["note"] = (
            "sitemap protetta da Cloudflare (403 'Just a moment'): esiste ma non è "
            "raschiabile. Da prendere via Wayback."
            if bloccato
            else "nessuna sitemap trovata agli indirizzi canonici né in robots.txt"
        )
        return result

    result["children"] = children
    blob = " ".join(children).lower() + " " + result["index_url"].lower()
    result["wordpress"] = any(hint in blob for hint in WORDPRESS_HINTS)

    # Le sitemap dei post sono PAGINATE: Yoast tronca a 1000 URL e continua con
    # post-sitemap2.xml, post-sitemap3.xml... Leggerne una sola dava un intervallo
    # di date falso (un blocco cronologico scambiato per l'intero archivio).
    post_sitemaps = [c for c in children if classify_sitemap(c) == "post"]
    page_sitemaps = [c for c in children if classify_sitemap(c) == "page"]
    result["post_sitemap"] = post_sitemaps[0] if post_sitemaps else ""
    result["page_sitemap"] = page_sitemaps[0] if page_sitemaps else ""
    result["post_sitemap_pagine"] = len(post_sitemaps)

    targets = post_sitemaps or children[: config["max_sitemaps"]]
    dates: list[str] = []
    total = 0
    for target in targets:
        response = fetch(session, target, config["timeout"], config["pause"])
        if response is None:
            continue
        _, pages = parse_sitemap(response.content)
        total += len(pages)
        dates.extend(page["lastmod"] for page in pages if page.get("lastmod"))
    if not total:
        result["note"] = "nessuna pagina leggibile dalle sitemap"
        return result

    dates.sort()
    result["post_urls"] = total
    result["lastmod_presenti"] = len(dates)
    if dates:
        result["lastmod_min"] = dates[0][:10]
        result["lastmod_max"] = dates[-1][:10]
        result["lastmod_campione"] = [d[:19] for d in dates[-3:]]
        # Quante date distinte: se sono pochissime su molti URL, il lastmod e' la
        # data di rigenerazione del sito, non di pubblicazione. Inutile per ordinare.
        result["lastmod_giorni_distinti"] = len({d[:10] for d in dates})
    return result


def write_report(results: list[dict], out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Ricognizione sitemap dei siti di partito (layer 1)",
        "",
        f"Eseguito: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"Comando: `python scripts/run_layer1_recon.py`",
        "",
        "| partito | WP | sitemap post | URL post | lastmod | giorni distinti | intervallo |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in results:
        post = f"{r['post_sitemap_pagine']} pagine" if r["post_sitemap_pagine"] else "—"
        copertura = (
            f"{r['lastmod_presenti']}/{r['post_urls']}" if r["post_urls"] else "—"
        )
        intervallo = f"{r['lastmod_min']} → {r['lastmod_max']}" if r["lastmod_min"] else "—"
        lines.append(
            f"| {r['id']} | {'sì' if r['wordpress'] else 'no'} | {post} | "
            f"{r['post_urls'] or '—'} | {copertura} | {r['lastmod_giorni_distinti'] or '—'} | "
            f"{intervallo} |"
        )
    lines += ["", "## Note", ""]
    for r in results:
        if r["note"]:
            lines.append(f"- {r['id']}: {r['note']}")
        if r["lastmod_campione"]:
            lines.append(f"- {r['id']}: lastmod più recenti {r['lastmod_campione']}")
    report = out_dir / "sitemap_recon.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out_dir / "sitemap_recon.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="config/programmi_discovery.json")
    parser.add_argument("--partito", action="append")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = load_config(REPO_HINT / args.config)
    parties = config["partiti"]
    if args.partito:
        parties = [p for p in parties if p["id"] in set(args.partito)]

    session = build_session(config["user_agent"])
    results = []
    for party in parties:
        print(f"  {party['id']:20s} ...", flush=True)
        results.append(probe_party(session, party, config))

    report = write_report(results, REPO_HINT / "reports" / "layer1_recon")
    wordpress = sum(1 for r in results if r["wordpress"])
    con_post = sum(1 for r in results if r["post_sitemap"])
    print(f"\nWordPress: {wordpress}/{len(results)} | sitemap post distinta: {con_post}/{len(results)}")
    print(f"Report: {report.relative_to(REPO_HINT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
