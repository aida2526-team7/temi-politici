#!/usr/bin/env python3
"""Incrocia la salienza dei temi nell'opinione pubblica con i tre layer.

La domanda: i temi che preoccupano gli italiani sono gli stessi su cui i partiti
promettono, legiferano e la stampa scrive?

**Si confrontano ranghi, non livelli.** I valori Ipsos sono la percentuale di
intervistati che cita un tema fra le proprie preoccupazioni principali: ognuno è
indipendente dagli altri e la somma supera il 100% (162% nel giugno 2026). Non
sono una distribuzione, quindi non stanno sulla stessa scala delle quote dei tre
layer, che invece sommano a 100. Il rango sopravvive a questa differenza: dice
quale tema viene prima, e quello si confronta.

Restano due limiti che nessuna elaborazione toglie:

- Ipsos espone solo i temi in testa, non tutti. Dei 15 macrotemi ne copre 4.
- La serie è sparsa: 7 mesi, e solo `tasse` ha più di tre rilevazioni. Il
  confronto si fa sul mese più completo, non su una serie storica.

Uso:
    python scripts/run_intersezione_sondaggi.py
    python scripts/run_intersezione_sondaggi.py --mese 2024-12
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import mappa_ontologia as mo  # noqa: E402

SONDAGGI_IN = ROOT / "data/processed/sondaggi_salienza_temi.csv"
DISTRIBUZIONE_IN = ROOT / "reports/ontologia_mapping/distribuzione_layer.csv"
OUT_DIR = ROOT / "reports/ontologia_mapping"

# Dai temi Ipsos ai macrotemi dell'ontologia v2.0. Il ponte è corto perché Ipsos
# espone poche voci, ma va scritto: `disoccupazione` non è un macrotema, è il
# nome che l'indagine dà a ciò che noi chiamiamo *Lavoro e imprese*.
#
# `inflazione` e `tasse` cadono entrambi nel 4. Non si sommano — sono due
# domande diverse allo stesso intervistato, e sommarle conterebbe due volte chi
# ha citato entrambe. Si tiene la più alta: quanto pesa, al massimo, la
# preoccupazione economica.
TEMI_IPSOS: dict[str, int] = {
    "criminalita": 11,
    "sanita": 7,
    "disoccupazione": 5,
    "inflazione": 4,
    "tasse": 4,
}


def leggi_sondaggi(path: Path) -> dict[str, dict[int, float]]:
    """Per ogni mese, il valore massimo di salienza per macrotema."""
    per_mese: defaultdict[str, dict[int, float]] = defaultdict(dict)
    with path.open(encoding="utf-8-sig") as handle:
        for riga in csv.DictReader(handle):
            tema = TEMI_IPSOS.get(riga["tema_norm"])
            if tema is None:
                continue
            valore = float(riga["valore"])
            mese = riga["data"]
            per_mese[mese][tema] = max(per_mese[mese].get(tema, 0.0), valore)
    return dict(per_mese)


def leggi_layer(path: Path) -> dict[str, dict[int, float]]:
    quote: dict[str, dict[int, float]] = {"l1": {}, "l2": {}, "l3": {}}
    with path.open(encoding="utf-8-sig") as handle:
        for riga in csv.DictReader(handle):
            if not riga["id"]:
                continue
            tema = int(riga["id"])
            quote["l1"][tema] = float(riga["layer1_programmi_pct"])
            quote["l2"][tema] = float(riga["layer2_ddl_pct"])
            quote["l3"][tema] = float(riga["layer3_stampa_pct"])
    return quote


def ranghi(valori: dict[int, float], temi: list[int]) -> dict[int, int]:
    """Rango 1 al valore più alto, fra i soli temi confrontabili."""
    ordinati = sorted(temi, key=lambda t: -valori.get(t, 0.0))
    return {tema: posizione for posizione, tema in enumerate(ordinati, start=1)}


def scarto_ranghi(a: dict[int, int], b: dict[int, int]) -> int:
    """Somma degli scostamenti assoluti di rango. 0 = stesso ordine."""
    return sum(abs(a[t] - b[t]) for t in a)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mese", help="mese da confrontare; default: il più completo")
    args = parser.parse_args()

    sondaggi = leggi_sondaggi(SONDAGGI_IN)
    if not sondaggi:
        print("Nessun dato Ipsos mappabile sui macrotemi.", file=sys.stderr)
        return 1

    mese = args.mese or max(sondaggi, key=lambda m: (len(sondaggi[m]), m))
    if mese not in sondaggi:
        print(f"Mese {mese} assente. Disponibili: {sorted(sondaggi)}", file=sys.stderr)
        return 2

    salienza = sondaggi[mese]
    temi = sorted(salienza)
    layer = leggi_layer(DISTRIBUZIONE_IN)

    r_ipsos = ranghi(salienza, temi)
    r_layer = {nome: ranghi(quote, temi) for nome, quote in layer.items()}

    print(f"Mese confrontato: {mese} ({len(temi)} macrotemi coperti su 15)")
    print(f"Mesi disponibili: {', '.join(sorted(sondaggi))}\n")

    righe = []
    for tema in sorted(temi, key=lambda t: r_ipsos[t]):
        righe.append({
            "id": tema,
            "macrotema": mo.etichetta(tema),
            "salienza_ipsos_pct": salienza[tema],
            "rango_opinione": r_ipsos[tema],
            "rango_programmi": r_layer["l1"][tema],
            "rango_ddl": r_layer["l2"][tema],
            "rango_stampa": r_layer["l3"][tema],
            "quota_programmi_pct": layer["l1"].get(tema),
            "quota_ddl_pct": layer["l2"].get(tema),
            "quota_stampa_pct": layer["l3"].get(tema),
            "scarto_opinione_programmi": r_layer["l1"][tema] - r_ipsos[tema],
        })

    intestazione = f"{'macrotema':34s} {'Ipsos':>7s} {'op.':>4s} {'prog':>5s} {'ddl':>4s} {'st.':>4s}"
    print(intestazione)
    for riga in righe:
        print(f"{riga['macrotema'][:34]:34s} {riga['salienza_ipsos_pct']:6.0f}% "
              f"{riga['rango_opinione']:4d} {riga['rango_programmi']:5d} "
              f"{riga['rango_ddl']:4d} {riga['rango_stampa']:4d}")

    print("\nScarto di rango rispetto all'opinione pubblica (0 = stesso ordine):")
    for nome, etichetta in (("l1", "programmi"), ("l2", "progetti di legge"), ("l3", "stampa")):
        print(f"  {etichetta:20s} {scarto_ranghi(r_ipsos, r_layer[nome]):2d}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / "intersezione_sondaggi.csv"
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(righe[0]))
        writer.writeheader()
        writer.writerows(righe)
    print(f"\nOutput: {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
