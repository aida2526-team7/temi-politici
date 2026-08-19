"""Riduce news_topic_review.csv a una versione versionabile su Git.

Il problema che risolve
-----------------------
`data/processed/news_topic_review.csv` pesa 98 MB ed è in `.gitignore`. È
l'input di `run_topic_audit.py`, di `run_topic_human_review.py` e di qualunque
rilancio del modello. Sta su una macchina sola: chi clona il repository può
compilare i due CSV di annotazione da 27 righe e nient'altro.

Cosa toglie, e perché il peso crolla
------------------------------------
1. le 12 colonne `topic_N_peso`: 12 float per riga su 96.345 righe sono circa
   metà del file. Servono all'audit, non a chi deve leggere e giudicare;
2. l'`estratto` da 500 caratteri, la voce più pesante, ridotto a 300 —
   abbastanza per riconoscere di cosa parla un pezzo;
3. le righe, con un campionamento stratificato per topic.

Restano `peso_topic_dominante` e `confidenza_topic`, che sono i due numeri su cui
si ragiona davvero.

Uso:
    python scripts/prepara_review_condivisibile.py
    python scripts/prepara_review_condivisibile.py --per-topic 500

Output: `data/processed/news_topic_review_campione.csv` (da versionare) e un
manifest con gli hash, perché un campione senza provenienza non è verificabile.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IN = ROOT / "data" / "processed" / "news_topic_review.csv"
DEFAULT_OUT = ROOT / "data" / "processed" / "news_topic_review_campione.csv"
DEFAULT_MANIFEST = ROOT / "reports" / "topic_audit" / "campione_manifest.json"

ESTRATTO_MAX = 300
SEED = 42


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_IN)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--per-topic", type=int, default=400,
                        help="righe campionate per topic (i topic più piccoli "
                             "entrano interi)")
    parser.add_argument("--seed", type=int, default=SEED)
    return parser.parse_args()


def mostra(path):
    """Percorso relativo alla root se ci sta dentro, assoluto altrimenti.

    relative_to() solleva su un percorso fuori dal repository, e questo script
    accetta --input/--output arbitrari: un manifest non deve morire per come e'
    scritto un percorso.
    """
    try:
        return str(Path(path).relative_to(ROOT))
    except ValueError:
        return str(path)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for blocco in iter(lambda: handle.read(1 << 20), b""):
            digest.update(blocco)
    return digest.hexdigest()


def main():
    args = parse_args()
    if not args.input.is_file():
        print(f"ERRORE: input non trovato: {args.input}\n"
              "Questo script gira sulla macchina che ha il file completo.",
              file=sys.stderr)
        return 2

    review = pd.read_csv(args.input, encoding="utf-8-sig", low_memory=False)
    righe_prima, byte_prima = len(review), args.input.stat().st_size

    pesi = [c for c in review.columns if c.startswith("topic_") and c.endswith("_peso")]
    if pesi:
        # Il peso del topic dominante è l'unico che serve a chi legge: gli altri
        # 11 sono l'input dell'audit, che gira dove sta il file completo.
        review["peso_topic_dominante"] = review[pesi].max(axis=1)
        review = review.drop(columns=pesi)

    if "estratto" in review.columns:
        review["estratto"] = review["estratto"].astype(str).str.slice(0, ESTRATTO_MAX)

    # Campionamento stratificato: ogni topic resta rappresentato, anche i piccoli.
    # Senza stratificazione un campione casuale su una distribuzione dove tre
    # topic fanno l'80% farebbe sparire gli altri nove.
    #
    # Si campionano gli INDICI e poi si seleziona: groupby().apply() cambia
    # comportamento fra pandas 2 e 3 (in 3 la colonna di raggruppamento finisce
    # nell'indice e sparisce), e questo script deve girare su entrambe.
    indici = []
    for _, gruppo in review.groupby("topic_id", sort=True):
        quanti = min(len(gruppo), args.per_topic)
        indici.extend(gruppo.sample(n=quanti, random_state=args.seed).index)
    campione = review.loc[indici].sort_values(
        ["topic_id", "confidenza_topic"], ascending=[True, False])

    args.output.parent.mkdir(parents=True, exist_ok=True)
    campione.to_csv(args.output, index=False, encoding="utf-8-sig")

    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps({
        "generato_utc": datetime.now(timezone.utc).isoformat(),
        "sorgente": {
            "path": mostra(args.input),
            "righe": int(righe_prima),
            "byte": int(byte_prima),
            "sha256": sha256(args.input),
        },
        "campione": {
            "path": mostra(args.output),
            "righe": int(len(campione)),
            "byte": int(args.output.stat().st_size),
            "sha256": sha256(args.output),
            "per_topic": args.per_topic,
            "seed": args.seed,
            "estratto_max_caratteri": ESTRATTO_MAX,
            "colonne_peso_rimosse": len(pesi),
        },
        "avvertenza": (
            "Campione stratificato, non rappresentativo delle prevalenze: i topic "
            "piccoli sono sovrarappresentati di proposito. Per stimare la "
            "distribuzione usare reports/topic_audit/topic_distribution.csv, che "
            "è calcolato sul file completo."
        ),
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Sorgente: {righe_prima:,} righe, {byte_prima / 1e6:.1f} MB")
    print(f"Campione: {len(campione):,} righe, {args.output.stat().st_size / 1e6:.1f} MB "
          f"({args.output.stat().st_size / byte_prima:.1%} dell'originale)")
    print(f"  {mostra(args.output)}")
    print(f"  {mostra(args.manifest)}")
    print("\nQuesto file è pensato per essere versionato: toglierlo da .gitignore.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
