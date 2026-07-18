#!/usr/bin/env python3
"""Ingest della salienza dei temi Italia da Ipsos (stage sondaggi, prospettico).

Cattura il mese corrente dalla pagina Ipsos Italia e lo accumula nel dataset. Da
eseguire periodicamente (mensile): il dataset si costruisce nel tempo.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_HINT = Path(__file__).resolve().parents[1]
if str(REPO_HINT) not in sys.path:
    sys.path.insert(0, str(REPO_HINT))

# I temi possono contenere caratteri che la console Windows (cp1252) non codifica.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from src.programmi_discovery import build_session, load_config
from src.sondaggi_ipsos import aggiorna_dataset, raccogli_corrente, raccogli_storico


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="config/sondaggi_ipsos.json")
    parser.add_argument(
        "--storico",
        action="store_true",
        help="tenta anche il recupero da Wayback (best-effort, recupera poco)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="stampa la lettura corrente senza scrivere il dataset",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = load_config(REPO_HINT / args.config)
    session = build_session(config["user_agent"])

    print("Ingest Ipsos — salienza dei temi Italia (What Worries the World)")
    records = raccogli_corrente(session, config)
    if records:
        print(f"  mese corrente: {records[0]['data']} — {len(records)} temi")
    else:
        print("  pagina live: nessuna lettura estratta (struttura cambiata?)", file=sys.stderr)

    if args.storico:
        storici = raccogli_storico(session, config)
        mesi = sorted({r["data"] for r in storici})
        print(f"  Wayback (best-effort): {len(storici)} record da {len(mesi)} mesi {mesi}")
        records = storici + records

    if not records:
        return 1

    for r in sorted(records, key=lambda r: (r["data"], -int(r["valore"]))):
        print(f"    {r['data']}  {r['valore']:>3}%  {r['tema_norm']:<16} ({r['tema']})")

    if args.dry_run:
        print("\n--dry-run: dataset non scritto.")
        return 0

    out = REPO_HINT / config["output_csv"]
    aggiunti, totale = aggiorna_dataset(records, out)
    print(f"\nDataset aggiornato: +{aggiunti} record, {totale} totali")
    print(f"  -> {out.relative_to(REPO_HINT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
