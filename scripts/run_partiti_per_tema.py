#!/usr/bin/env python3
"""Partito × macrotema sui tre layer, sulla stessa scala.

Il pezzo che mancava. La mappatura produceva già il dettaglio per partito su
programmi e progetti di legge, ma non sulla stampa: la discovery Media Cloud ha
usato una query unica in OR e il tag del partito si è perso per strada. Qui si
ricostruisce applicando agli articoli lo stesso lessico che produce i conteggi di
copertura (`PARTY_PATTERNS` in `src/mediacloud_fulltext.py`).

**Un articolo può nominare più partiti, e conta per ognuno.** Non è un difetto: è
come è definita la copertura fin dall'inizio del progetto, ed è il motivo per cui
le quote di un layer non sommano a 100 fra i partiti. Ogni riga qui è "quanto pesa
il tema T dentro la copertura del partito P", che è la domanda giusta per un
confronto fra partiti di dimensioni molto diverse.

## Il raccordo fra i nomi

Lo stesso partito si chiama in tre modi: `LEGA PER SALVINI PREMIER` nel deposito
al Viminale, `LEGA - SALVINI PREMIER` fra i gruppi della Camera, `Lega / Salvini`
nel lessico della stampa. Senza una tabella di raccordo esplicita i tre layer non
si sovrappongono, e un fuzzy match silenzioso sbaglierebbe senza dirlo.

Uso:
    python scripts/run_partiti_per_tema.py
"""

from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import mappa_ontologia as mo  # noqa: E402
from mediacloud_fulltext import PARTY_PATTERNS  # noqa: E402

REVIEW_IN = ROOT / "data/processed/news_topic_review.csv"
LAYER1_IN = ROOT / "reports/ontologia_mapping/layer1_per_programma.csv"
LAYER2_IN = ROOT / "reports/ontologia_mapping/layer2_per_gruppo.csv"
OUT_DIR = ROOT / "reports/ontologia_mapping"

# Il raccordo, scritto a mano perché è una decisione, non un calcolo. La chiave è
# l'etichetta del lessico stampa: è quella che fa da nome canonico.
#
# `lista` è la denominazione depositata al Viminale per le politiche 2022,
# `gruppo` quella del gruppo parlamentare alla Camera. Un `None` dice che quel
# layer non ha una controparte, e va lasciato vuoto invece che forzato.
RACCORDO = {
    "FdI / Meloni": {
        "lista": "FRATELLI D'ITALIA CON GIORGIA MELONI",
        "gruppo": "FRATELLI D'ITALIA"},
    "PD / Schlein": {
        "lista": "PARTITO DEMOCRATICO - ITALIA DEMOCRATICA E PROGRESSISTA",
        "gruppo": "PARTITO DEMOCRATICO - ITALIA DEMOCRATICA E PROGRESSISTA"},
    "Lega / Salvini": {
        "lista": "LEGA PER SALVINI PREMIER",
        "gruppo": "LEGA - SALVINI PREMIER"},
    "M5S / Conte": {
        "lista": "MOVIMENTO 5 STELLE",
        "gruppo": "MOVIMENTO 5 STELLE"},
    "Forza Italia / Tajani": {
        "lista": "FORZA ITALIA",
        "gruppo": "FORZA ITALIA - BERLUSCONI PRESIDENTE"},
    "AVS / Fratoianni-Bonelli": {
        "lista": "ALLEANZA VERDI E SINISTRA",
        "gruppo": "ALLEANZA VERDI E SINISTRA"},
    "Azione / Calenda": {
        "lista": "AZIONE - ITALIA VIVA - CALENDA",
        "gruppo": "AZIONE - ITALIA VIVA - RENEW EUROPE"},
    "Italia Viva / Renzi": {
        # La lista 2022 è la stessa di Azione: correvano insieme. Attribuirla a
        # entrambi conterebbe due volte lo stesso testo, quindi qui resta vuota.
        "lista": None,
        "gruppo": "ITALIA VIVA"},
    "+Europa": {"lista": "+EUROPA", "gruppo": None},
    "Futuro Nazionale / Vannacci": {"lista": None, "gruppo": None},
}

TEMI = list(mo.MACROTEMI)


def quote(conteggi: dict[int, float]) -> dict[int, float]:
    totale = sum(conteggi.values())
    return {t: 100.0 * conteggi.get(t, 0.0) / totale for t in TEMI} if totale else {}


def stampa_per_partito() -> dict[str, dict[int, float]]:
    """Quanto pesa ogni macrotema dentro la copertura di ciascun partito."""
    conteggi: defaultdict[str, defaultdict[int, int]] = defaultdict(
        lambda: defaultdict(int))
    letti = 0
    with REVIEW_IN.open(encoding="utf-8-sig") as handle:
        for riga in csv.DictReader(handle):
            letti += 1
            testo = f"{riga.get('title', '')} {riga.get('estratto', '')}"
            if mo.quota_boilerplate(testo) > 0:
                continue
            tema, _ = mo.classifica(testo)
            if not isinstance(tema, int):
                continue
            for partito, pattern in PARTY_PATTERNS.items():
                if pattern.search(testo):
                    conteggi[partito][tema] += 1
    print(f"Layer 3: {letti:,} articoli letti, {len(conteggi)} partiti riconosciuti")
    return {p: quote(dict(c)) for p, c in conteggi.items()}


def da_csv_per_tema(path: Path, chiave: str, filtro: dict | None = None
                    ) -> dict[str, dict[int, float]]:
    """Quote per macrotema da una tabella che ha una colonna per tema."""
    risultato = {}
    with path.open(encoding="utf-8") as handle:
        for riga in csv.DictReader(handle):
            nome = riga[chiave]
            if filtro and nome not in filtro:
                continue
            conteggi = {t: float(riga.get(str(t)) or 0) for t in TEMI}
            if sum(conteggi.values()):
                risultato[nome] = quote(conteggi)
    return risultato


def main() -> int:
    stampa = stampa_per_partito()

    liste = {v["lista"] for v in RACCORDO.values() if v["lista"]}
    gruppi = {v["gruppo"] for v in RACCORDO.values() if v["gruppo"]}
    programmi = da_csv_per_tema(LAYER1_IN, "partito_lista", liste)
    leggi = da_csv_per_tema(LAYER2_IN, "gruppo", gruppi)
    print(f"Layer 1: {len(programmi)} liste raccordate")
    print(f"Layer 2: {len(leggi)} gruppi raccordati")

    righe = []
    for partito, nomi in RACCORDO.items():
        fonti = {
            "Programmi": programmi.get(nomi["lista"]) if nomi["lista"] else None,
            "Progetti di legge": leggi.get(nomi["gruppo"]) if nomi["gruppo"] else None,
            "Stampa": stampa.get(partito),
        }
        for layer, distribuzione in fonti.items():
            if not distribuzione:
                continue
            for tema in TEMI:
                righe.append({
                    "partito": partito,
                    "layer": layer,
                    "id": tema,
                    "macrotema": mo.MACROTEMI[tema],
                    "quota": round(distribuzione.get(tema, 0.0), 2),
                })

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    percorso = OUT_DIR / "partiti_per_tema.csv"
    with percorso.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["partito", "layer", "id", "macrotema", "quota"])
        writer.writeheader()
        writer.writerows(righe)

    coperti = defaultdict(set)
    for riga in righe:
        coperti[riga["partito"]].add(riga["layer"])
    print(f"\n{len(righe)} righe, {len(coperti)} partiti")
    for partito, layer in sorted(coperti.items()):
        print(f"  {partito[:30]:32s} {', '.join(sorted(layer))}")

    (OUT_DIR / "raccordo_partiti.json").write_text(
        json.dumps(RACCORDO, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nOutput: {percorso.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
