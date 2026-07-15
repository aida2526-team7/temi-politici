#!/usr/bin/env python3
"""Punto di esecuzione ufficiale dell'audit NMF riproducibile."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_HINT = Path(__file__).resolve().parents[1]
if str(REPO_HINT) not in sys.path:
    sys.path.insert(0, str(REPO_HINT))

from src.news_topic_audit import find_repo_root, load_config, resolve_repo_path, run_audit


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        default="config/topic_audit.json",
        help="percorso relativo del file di configurazione",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        repo_root = find_repo_root(Path(__file__))
        config_path = resolve_repo_path(repo_root, args.config)
        config = load_config(config_path, repo_root)
        results, outputs = run_audit(repo_root, config)
    except (FileNotFoundError, ValueError, KeyError, OSError) as error:
        print(f"ERRORE AUDIT: {error}", file=sys.stderr)
        return 2

    total_articles = int(results.topic_distribution["articles"].sum())
    print(f"Audit NMF completato: {total_articles:,} articoli, {len(results.topic_distribution)} topic.")
    print("Output generati:")
    for name, path in sorted(outputs.items()):
        print(f" - {name}: {path.relative_to(repo_root)}")
    if results.warnings:
        print("Avvisi:")
        for warning in results.warnings:
            print(f" - {warning}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
