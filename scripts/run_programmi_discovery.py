#!/usr/bin/env python3
"""Punto di esecuzione della discovery dei documenti di partito (layer 1)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_HINT = Path(__file__).resolve().parents[1]
if str(REPO_HINT) not in sys.path:
    sys.path.insert(0, str(REPO_HINT))

from src.programmi_discovery import discover, load_config, select_candidates, write_metadata


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        default="config/programmi_discovery.json",
        help="percorso relativo del file di configurazione",
    )
    parser.add_argument(
        "--partito",
        action="append",
        help="ID partito da includere; ripetibile (es. --partito fdi)",
    )
    parser.add_argument(
        "--no-wayback",
        action="store_true",
        help="salta le copie storiche: solo i siti attuali",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="stampa i candidati senza scrivere il file di output",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = REPO_HINT
    try:
        config = load_config(repo_root / args.config)
    except (FileNotFoundError, ValueError) as error:
        print(f"ERRORE CONFIGURAZIONE: {error}", file=sys.stderr)
        return 2

    parties = config["partiti"]
    if args.partito:
        selected = set(args.partito)
        parties = [party for party in parties if party["id"] in selected]
        if not parties:
            print(f"ERRORE: nessun partito corrisponde a {sorted(selected)}", file=sys.stderr)
            return 2
    if args.no_wayback:
        config["wayback"] = False

    print(f"Discovery layer 1 su {len(parties)} partiti (wayback: {config['wayback']})")
    try:
        records = discover(config, parties)
    except KeyboardInterrupt:
        print("Interrotto dall'utente.", file=sys.stderr)
        return 130

    programmi = sum(1 for record in records if record["tipo_documento"] == "programma")
    comunicati = sum(1 for record in records if record["tipo_documento"] == "comunicato")
    correnti = sum(1 for record in records if record["fonte"] == "corrente")
    print(
        f"\nTotale: {len(records)} documenti "
        f"({programmi} programmi, {comunicati} comunicati; "
        f"{correnti} correnti, {len(records) - correnti} storici)"
    )

    if args.dry_run:
        print("\n--dry-run: nessun file scritto. Primi 20 candidati per punteggio:")
        for record in sorted(records, key=lambda r: -r["score"])[:20]:
            print(f"  {record['score']:4d}  {record['tipo_documento']:11s}  {record['url_originale']}")
        return 0

    out_path = repo_root / config["output_urls_jsonl"]
    write_metadata(records, out_path)
    print(f"\nOutput: {out_path.relative_to(repo_root)}")
    print("Prossimo passo: python src/programmi_fulltext.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
