#!/usr/bin/env python3
"""Entry point ufficiale del campione riproducibile per lo human check."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_HINT = Path(__file__).resolve().parents[1]
if str(REPO_HINT) not in sys.path:
    sys.path.insert(0, str(REPO_HINT))

from src.topic_human_review import find_repo_root, load_config, resolve_repo_path, run_human_review


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="config/topic_human_review.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        repo_root = find_repo_root(Path(__file__))
        config_path = resolve_repo_path(repo_root, args.config)
        config = load_config(config_path, repo_root)
        result, paths = run_human_review(repo_root, config)
    except (FileNotFoundError, ValueError, KeyError, OSError) as error:
        print(f"ERRORE HUMAN REVIEW: {error}", file=sys.stderr)
        return 2
    print(f"Campione human check creato: {len(result.sample)} righe, {result.sample['topic_id'].nunique()} topic.")
    print(f"Output: {', '.join(sorted(path.relative_to(repo_root).as_posix() for path in paths.values()))}")
    print(f"Eccezioni dominio: {len(result.exceptions)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
