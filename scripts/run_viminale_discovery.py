#!/usr/bin/env python3
"""Discovery dei programmi elettorali dal portale Elezioni trasparenti (layer 1)."""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path


REPO_HINT = Path(__file__).resolve().parents[1]
if str(REPO_HINT) not in sys.path:
    sys.path.insert(0, str(REPO_HINT))

# I nomi delle liste contengono caratteri che la console Windows (cp1252) non sa
# codificare: senza questo, stampare l'elenco solleva UnicodeEncodeError.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from src.programmi_discovery import build_session, fetch, load_config, write_metadata
from src.viminale_trasparenza import CONSULTAZIONI, carica_mappatura, discover_programmi


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="config/programmi_discovery.json")
    parser.add_argument("--liste", default="config/viminale_liste.json")
    parser.add_argument(
        "--consultazione",
        action="append",
        choices=sorted(CONSULTAZIONI),
        help="ripetibile; default: tutte",
    )
    parser.add_argument(
        "--verifica-url",
        action="store_true",
        help="controlla con una HEAD che ogni programma risponda 200 (lento)",
    )
    parser.add_argument("--dry-run", action="store_true", help="non scrive il file di output")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = load_config(REPO_HINT / args.config)
    mappatura = carica_mappatura(REPO_HINT / args.liste)
    session = build_session(config["user_agent"])

    print("Discovery programmi dal portale Elezioni trasparenti")
    records = discover_programmi(session, config, mappatura, args.consultazione)
    if not records:
        print("Nessun programma trovato.", file=sys.stderr)
        return 1

    per_consultazione = Counter(r["consultazione"] for r in records)
    print(f"\nTotale: {len(records)} programmi")
    for nome, quanti in sorted(per_consultazione.items()):
        print(f"  {nome:16s} {quanti:3d}")

    # Copertura per partito. Un programma di coalizione conta per entrambi i
    # partiti: la somma supera il numero di documenti, ed e' corretto cosi'.
    print("\nCopertura per partito (un programma di coalizione conta per entrambi):")
    per_partito: Counter = Counter()
    for record in records:
        for partito in record["partiti"]:
            per_partito[partito] += 1
    for partito in sorted(p["id"] for p in config["partiti"]):
        quante = per_partito.get(partito, 0)
        consultazioni = sorted(
            r["consultazione"].replace("politiche", "")
            for r in records
            if partito in r["partiti"]
        )
        segno = " " if quante else "!"
        print(f"  {segno} {partito:20s} {quante}  {', '.join(consultazioni) or 'nessun programma'}")
    non_attribuiti = sum(1 for r in records if not r["partiti"])
    print(f"\n  {non_attribuiti} programmi di liste non seguite (restano nel corpus, senza attribuzione)")

    if args.verifica_url:
        print("\nVerifica che gli URL rispondano:")
        rotti = []
        for record in records:
            # HEAD: interessa se la risorsa c'è, non il suo contenuto.
            response = fetch(session, record["url"], config["timeout"], 0.2, method="HEAD")
            if response is None:
                rotti.append(record["url"])
        print(f"  raggiungibili: {len(records) - len(rotti)}/{len(records)}")
        for url in rotti[:10]:
            print(f"  ROTTO: {url}")
        if rotti:
            return 1

    if args.dry_run:
        # Elenco completo, non un campione: serve a leggere i nomi delle liste
        # depositate, che è il passo su cui si costruisce la mappatura verso i
        # partiti di config/programmi_discovery.json.
        print("\n--dry-run: nessun file scritto. Liste depositate:")
        for nome in sorted(per_consultazione):
            print(f"\n  === {nome} ===")
            for i, record in enumerate(
                sorted((r for r in records if r["consultazione"] == nome),
                       key=lambda r: r["title"]), 1
            ):
                titolo = record["title"] or "(nome non estratto)"
                print(f"  {i:3d}. {titolo}")
        return 0

    out_path = REPO_HINT / "data" / "raw" / "programmi_viminale_urls.jsonl"
    write_metadata(records, out_path)
    print(f"\nOutput: {out_path.relative_to(REPO_HINT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
