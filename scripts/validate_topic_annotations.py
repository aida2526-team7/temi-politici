#!/usr/bin/env python3
"""Valida in sola lettura i file compilati dai revisori."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_HINT = Path(__file__).resolve().parents[1]
if str(REPO_HINT) not in sys.path:
    sys.path.insert(0, str(REPO_HINT))

from src.topic_annotation import find_repo_root, load_config, resolve_repo_path, validate_annotation_files


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="config/topic_annotation.json")
    parser.add_argument(
        "--allow-incomplete",
        action="store_true",
        help="valida struttura e valori presenti senza richiedere la compilazione completa",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        root = find_repo_root(Path(__file__))
        config = load_config(resolve_repo_path(root, args.config), root)
        counts = validate_annotation_files(root, config, require_complete=not args.allow_incomplete)
    except (FileNotFoundError, ValueError, KeyError, OSError) as error:
        print(f"ERRORE VALIDAZIONE ANNOTAZIONI: {error}", file=sys.stderr)
        return 2
    mode = "strutturale" if args.allow_incomplete else "completa"
    print(f"Validazione {mode} superata:")
    for reviewer_id, values in sorted(counts.items()):
        print(
            f" - {reviewer_id}: righe={values['rows']}, calibrazione={values['calibration']}, "
            f"indipendente={values['independent']}, celle_umane_compilate={values['filled_human_cells']}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
