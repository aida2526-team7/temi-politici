#!/usr/bin/env python3
"""Entry point ufficiale per preparare i file dei revisori."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_HINT = Path(__file__).resolve().parents[1]
if str(REPO_HINT) not in sys.path:
    sys.path.insert(0, str(REPO_HINT))

from src.topic_annotation import find_repo_root, load_config, prepare_annotation_files, resolve_repo_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="config/topic_annotation.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        root = find_repo_root(Path(__file__))
        config = load_config(resolve_repo_path(root, args.config), root)
        paths, source_hash = prepare_annotation_files(root, config)
    except (FileNotFoundError, ValueError, KeyError, OSError) as error:
        print(f"ERRORE PREPARAZIONE ANNOTAZIONI: {error}", file=sys.stderr)
        return 2
    print(f"File revisori creati: {len(paths)}; hash sorgente verificato: {source_hash}")
    for reviewer_id, path in sorted(paths.items()):
        print(f" - {reviewer_id}: {path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
