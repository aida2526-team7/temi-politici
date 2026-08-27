#!/usr/bin/env python3
"""Allunga il corpus stampa invece di rifarlo, su una finestra esplicita.

Perche' esiste. `src/mediacloud_spike.py` usa una finestra **mobile**: START e'
sempre oggi meno 182 giorni. Rilanciarlo per «aggiornare» il corpus non lo
aggiorna, lo **sposta** - guadagna le settimane nuove e perde le vecchie di pari
numero - e per giunta riscrive `mediacloud_fulltext.jsonl` da zero, buttando via
un download da 339 MB.

Questo stage fa la cosa opposta: interroga l'intervallo che gli si dice, scarta
gli URL che il corpus ha gia' e **accoda** il resto. Girarlo ogni mese e' quasi
gratis, e il corpus cresce invece di scorrere.

Il conteggio per partito viene ricalcolato sull'intero corpus, non solo sui nuovi
articoli: `mediacloud_coverage.csv` e' una fotografia del totale.

Uso:
    python scripts/run_mediacloud_estensione.py --da 2026-07-01 --a 2026-08-27
    python scripts/run_mediacloud_estensione.py --da 2026-07-01           # a = oggi
    python scripts/run_mediacloud_estensione.py --da 2026-07-01 --solo-discovery
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import mediacloud.api  # noqa: E402
from harvester import scrape_metas  # noqa: E402
from mediacloud_fulltext import PARTY_PATTERNS, is_lega_sport_noise  # noqa: E402
from mediacloud_spike import (  # noqa: E402
    BLOCK_DOMAINS,
    COLLECTION_ID,
    COMBINED_QUERY,
    MC_API_KEY,
    domain_of,
)

URLS = ROOT / "data/raw/mediacloud_urls.jsonl"
CORPUS = ROOT / "data/raw/mediacloud_fulltext.jsonl"
COVERAGE = ROOT / "data/processed/mediacloud_coverage.csv"


def url_gia_presenti(path: Path) -> set[str]:
    """Gli URL gia' nel corpus. E' la difesa contro il doppio conteggio."""
    if not path.exists():
        return set()
    visti = set()
    with path.open(encoding="utf-8") as handle:
        for riga in handle:
            if riga.strip():
                visti.add(json.loads(riga).get("url", ""))
    return visti


def cerca(da: str, a: str, noti: set[str], max_storie: int | None) -> list[dict]:
    """Gli URL nella finestra che il corpus non ha ancora."""
    search = mediacloud.api.SearchApi(MC_API_KEY)
    nuovi: list[dict] = []
    token = None
    visti = 0
    print(f"Finestra: {da} -> {a} | collection {COLLECTION_ID}")
    while max_storie is None or len(nuovi) < max_storie:
        try:
            pagina, token = search.story_list(
                COMBINED_QUERY, start_date=date.fromisoformat(da),
                end_date=date.fromisoformat(a),
                collection_ids=[COLLECTION_ID], pagination_token=token)
        except Exception as errore:
            print(f"  story_list interrotta: {errore}", file=sys.stderr)
            break
        for storia in pagina:
            if max_storie is not None and len(nuovi) >= max_storie:
                break
            visti += 1
            url = storia.get("url")
            if not url or url in noti:
                continue
            host = url.split("/")[2].lower() if "://" in url else ""
            host = host[4:] if host.startswith("www.") else host
            if any(host == d or host.endswith("." + d) for d in BLOCK_DOMAINS):
                continue
            pubblicato = storia.get("publish_date")
            nuovi.append({
                "url": url,
                "domain": domain_of(storia),
                "seendate": (pubblicato.isoformat()
                             if hasattr(pubblicato, "isoformat") else pubblicato),
                "title": storia.get("title", ""),
            })
        if visti % 2000 < len(pagina):
            print(f"  ...{visti} storie viste, {len(nuovi)} nuove")
        if not token:
            break
    print(f"{visti} storie nella finestra, {len(nuovi)} non ancora nel corpus")
    return nuovi


def accoda(record: list[dict], path: Path) -> int:
    with path.open("a", encoding="utf-8") as handle:
        for riga in record:
            handle.write(json.dumps(riga, ensure_ascii=False) + "\n")
    return len(record)


def ricalcola_copertura(path: Path, out: Path) -> list[tuple[str, int]]:
    """Copertura per partito sull'intero corpus, non solo sui nuovi arrivi."""
    conteggi = Counter()
    totale = 0
    with path.open(encoding="utf-8") as handle:
        for riga in handle:
            if not riga.strip():
                continue
            record = json.loads(riga)
            totale += 1
            testo = (record.get("title", "") + " " + record.get("text", "")).lower()
            for etichetta, regex in PARTY_PATTERNS.items():
                if regex.search(testo):
                    conteggi[etichetta] += 1
    righe = sorted(conteggi.items(), key=lambda kv: -kv[1])
    with out.open("w", encoding="utf-8") as handle:
        handle.write("party,articles,pct\n")
        for etichetta, quanti in righe:
            handle.write(f"{etichetta},{quanti},{round(100 * quanti / (totale or 1), 2)}\n")
    print(f"\nCopertura ricalcolata su {totale:,} articoli -> {out.relative_to(ROOT)}")
    return righe


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--da", required=True, help="inizio finestra, AAAA-MM-GG")
    parser.add_argument("--a", default=date.today().isoformat(), help="fine finestra")
    parser.add_argument("--max-storie", type=int, help="tetto sugli URL nuovi")
    parser.add_argument("--solo-discovery", action="store_true",
                        help="trova gli URL nuovi senza scaricarne il testo")
    args = parser.parse_args()

    if not MC_API_KEY:
        print("MC_API_KEY assente: mettila in .env (ignorato da Git).", file=sys.stderr)
        return 2

    noti = url_gia_presenti(CORPUS)
    print(f"Corpus attuale: {len(noti):,} articoli")
    nuovi = cerca(args.da, args.a, noti, args.max_storie)
    if not nuovi:
        print("Niente da aggiungere.")
        return 0

    accoda(nuovi, URLS)
    if args.solo_discovery:
        print(f"--solo-discovery: {len(nuovi)} URL accodati a {URLS.relative_to(ROOT)}")
        return 0

    print(f"\nFull text di {len(nuovi)} articoli nuovi...")
    # scrape_metas apre sempre `out` in scrittura: gli si da' un file di appoggio,
    # mai il corpus, che va solo accodato. Passargli CORPUS lo azzererebbe.
    appoggio = CORPUS.with_suffix(".parziale.jsonl")
    record = scrape_metas(nuovi, out=str(appoggio))
    tenuti = [r for r in record if not is_lega_sport_noise(r)]
    print(f"{len(record)} scaricati, {len(record) - len(tenuti)} scartati dal filtro sport")

    accoda(tenuti, CORPUS)
    appoggio.unlink(missing_ok=True)
    print(f"Corpus: {len(noti):,} -> {len(noti) + len(tenuti):,} articoli")
    ricalcola_copertura(CORPUS, COVERAGE)
    print("\nProssimo passo: python src/news_topic_model.py --n-topics 12")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
