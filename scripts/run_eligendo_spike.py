"""Spike layer "chi li sostiene": risultati elettorali dal catalogo Eligendo.

Lo spike previsto dal piano (docs/politica-3d.md, fase 0, punto 4) e mai
eseguito. Risponde a: che formato hanno i dati, che granularita' effettiva, e
che copertura sulla finestra 2018-2026.

Uso:
    python scripts/run_eligendo_spike.py
    python scripts/run_eligendo_spike.py --consultazione camera2022

Output:
    data/raw/eligendo_nazionale.csv        totali nazionali per lista
    reports/layer3_recon/eligendo.md       la ricognizione, versionata
"""

from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import eligendo_risultati as er

OUT_CSV = ROOT / "data" / "raw" / "eligendo_nazionale.csv"
OUT_REPORT = ROOT / "reports" / "layer3_recon" / "eligendo.md"

CAMPI = ["consultazione", "data", "lista", "voti", "pct"]


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--consultazione", action="append",
                        choices=sorted(er.CONSULTAZIONI),
                        help="ripetibile; default: tutte")
    return parser.parse_args()


def riga_tabella(valori):
    return "| " + " | ".join(str(v) for v in valori) + " |"


def scrivi_report(esiti, path):
    righe = [
        "# Ricognizione layer \"chi li sostiene\" — risultati elettorali",
        "",
        f"Eseguito: {time.strftime('%Y-%m-%dT%H:%M:%S%z')}",
        "Comando: `python scripts/run_eligendo_spike.py`",
        f"Fonte: <{er.BASE}> (catalogo AgID del Viminale, download diretto)",
        "",
        "## Cosa c'è, e a che costo",
        "",
        riga_tabella(["consultazione", "data", "righe", "comuni", "liste",
                      "voti di lista", "secondi"]),
        riga_tabella(["---"] * 7),
    ]
    for esito in esiti:
        d = esito["diagnostica"]
        righe.append(riga_tabella([
            esito["chiave"], (d["date_distinte"] or [""])[0], f"{d['righe']:,}",
            f"{d['comuni']:,}", d["liste"], f"{d['voti_totali']:,}",
            f"{esito['secondi']:.1f}"]))

    for esito in esiti:
        righe += ["", f"### {esito['chiave']} — prime 10 liste", "",
                  riga_tabella(["lista", "voti", "%"]), riga_tabella(["---"] * 3)]
        for record in esito["record"][:10]:
            righe.append(riga_tabella([record["lista"], f"{record['voti']:,}",
                                       f"{record['pct']:.2f}%"]))

    righe += [
        "",
        "## Limiti",
        "",
        "- **Le politiche 2018 non sono in questo catalogo.** Verificato:",
        "  `Camera_Italia_LivComune.csv` contiene il 2022, non il 2018, ed è lo",
        "  stesso file di `camera-2022-Italia-livcomune.csv`. Senza il 2018 la",
        "  finestra del piano (2018→2026) copre una sola politica: H2 può",
        "  confrontare al massimo 2022 con le europee 2024. Il 2018 va cercato",
        "  nell'archivio storico Eligendo, che non espone CSV diretti.",
        "- **Valle d'Aosta assente** dai file `Italia`: ha un file separato, come",
        "  il Trentino per il Senato. I totali qui sotto sono quindi leggermente",
        "  sotto quelli ufficiali e **vanno riconciliati** con la pubblicazione",
        "  del Viminale prima di essere usati in un indice.",
        "- La **percentuale è sui voti di lista validi**, non sui votanti: schede",
        "  bianche, nulle e contestate non sono attribuite a nessuna lista.",
        "- I file sono a **livello comunale**; qui si aggrega a nazionale perché è",
        "  la granularità decisa dal piano. Il dettaglio comunale resta",
        "  disponibile se la decisione cambia.",
        "- Le **liste non sono i partiti**: \"AZIONE - ITALIA VIVA - CALENDA\" nel",
        "  2022 e \"AZIONE - SIAMO EUROPEI\" nel 2024 sono cartelli diversi. Serve",
        "  la stessa mappatura verso chiavi canoniche già richiesta dal layer 2.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(righe), encoding="utf-8")


def main():
    args = parse_args()
    chiavi = args.consultazione or sorted(er.CONSULTAZIONI)

    esiti, tutti = [], []
    for chiave in chiavi:
        print(f"{chiave}...", flush=True)
        avvio = time.perf_counter()
        record, diagnostica = er.scarica_consultazione(chiave)
        durata = time.perf_counter() - avvio
        esiti.append({"chiave": chiave, "record": record,
                      "diagnostica": diagnostica, "secondi": durata})
        tutti.extend(record)
        print(f"  {diagnostica['righe']:,} righe da {diagnostica['comuni']:,} comuni "
              f"-> {diagnostica['liste']} liste, {diagnostica['voti_totali']:,} voti "
              f"({durata:.1f}s)")
        if diagnostica["voti_non_numerici"]:
            print(f"  ATTENZIONE: {diagnostica['voti_non_numerici']} righe con voti "
                  f"non numerici, scartate")

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        scrittore = csv.DictWriter(handle, fieldnames=CAMPI)
        scrittore.writeheader()
        scrittore.writerows(tutti)

    scrivi_report(esiti, OUT_REPORT)
    print(f"\nOutput: {OUT_CSV.relative_to(ROOT)}")
    print(f"        {OUT_REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
