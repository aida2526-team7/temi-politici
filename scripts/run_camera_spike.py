"""Spike layer 2: scarica i progetti di legge della Camera e ne misura la resa.

Lo spike previsto dal piano (docs/politica-3d.md, fase 0, punto 3) e mai
eseguito. Risponde a tre domande, in questo ordine:

1. l'endpoint SPARQL regge una legislatura intera, e in quanto tempo?
2. quanti atti escono, con quale copertura di gruppo parlamentare?
3. il titolo basta come testo tematizzabile, o serve altro?

Uso:
    python scripts/run_camera_spike.py                 # legislature 18 e 19
    python scripts/run_camera_spike.py --legislatura 19
    python scripts/run_camera_spike.py --pagina 500    # se l'endpoint è lento

Output:
    data/raw/camera_ddl.jsonl        i record (non versionato, rigenerabile)
    reports/layer2_recon/camera.md   la ricognizione, versionata
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import camera_ddl

OUT_JSONL = ROOT / "data" / "raw" / "camera_ddl.jsonl"
OUT_REPORT = ROOT / "reports" / "layer2_recon" / "camera.md"


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--legislatura", type=int, action="append",
                        choices=sorted(camera_ddl.LEGISLATURE),
                        help="ripetibile; default: tutte")
    parser.add_argument("--pagina", type=int, default=camera_ddl.PAGINA,
                        help="righe per richiesta SPARQL")
    return parser.parse_args()


def scrivi_jsonl(records, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def riga_tabella(valori):
    return "| " + " | ".join(str(v) for v in valori) + " |"


def scrivi_report(misure, records, path):
    """Il report e' l'output vero dello spike: i record si rigenerano, la
    misura di quanto costa e cosa esce va scritta una volta."""
    path.parent.mkdir(parents=True, exist_ok=True)
    righe = [
        "# Ricognizione layer 2 — progetti di legge della Camera",
        "",
        f"Eseguito: {time.strftime('%Y-%m-%dT%H:%M:%S%z')}",
        "Comando: `python scripts/run_camera_spike.py`",
        f"Endpoint: <{camera_ddl.ENDPOINT}> (SPARQL pubblico, nessuno scraping)",
        "",
        "## Resa e costo",
        "",
        riga_tabella(["legislatura", "atti", "righe SPARQL", "richieste", "secondi"]),
        riga_tabella(["---"] * 5),
    ]
    for m in misure:
        righe.append(riga_tabella([m["legislatura"], f"{m['atti']:,}", f"{m['righe']:,}",
                                   m["richieste"], f"{m['secondi']:.1f}"]))

    iniziativa = Counter(r["iniziativa"] or "(assente)" for r in records)
    gruppi = Counter(r["gruppo"] or "(assente)" for r in records)
    senza_gruppo = gruppi.get("(assente)", 0)
    lunghezze = sorted(r["chars"] for r in records)

    righe += [
        "",
        "## Cosa esce",
        "",
        f"- atti totali: **{len(records):,}**",
        f"- con gruppo parlamentare del primo firmatario: "
        f"**{len(records) - senza_gruppo:,}** ({(len(records) - senza_gruppo) / max(len(records), 1):.1%})",
        f"- titolo: mediana **{lunghezze[len(lunghezze) // 2]:,} caratteri**, "
        f"min {lunghezze[0]}, max {lunghezze[-1]:,}",
        "",
        "### Per iniziativa",
        "",
        riga_tabella(["iniziativa", "atti", "%"]),
        riga_tabella(["---"] * 3),
    ]
    for nome, quanti in iniziativa.most_common():
        righe.append(riga_tabella([nome, f"{quanti:,}", f"{quanti / len(records):.1%}"]))

    righe += ["", "### Primi 15 gruppi", "", riga_tabella(["gruppo", "atti"]),
              riga_tabella(["---"] * 2)]
    for nome, quanti in gruppi.most_common(15):
        righe.append(riga_tabella([nome, f"{quanti:,}"]))

    righe += [
        "",
        "## Limiti",
        "",
        "- Il **gruppo** è quello del primo firmatario, non del provvedimento: un",
        "  atto firmato da più gruppi risulta attribuito a uno solo.",
        "- I nomi dei gruppi **cambiano fra legislature**: \"PARTITO DEMOCRATICO\"",
        "  e \"PARTITO DEMOCRATICO - ITALIA DEMOCRATICA E PROGRESSISTA\" sono lo",
        "  stesso partito e contano separatamente, come Forza Italia con e senza",
        "  \"- PPE\". Aggregare per partito richiede una mappatura verso chiavi",
        "  canoniche: quella del layer 1 sta in `config/viminale_liste.json` e va",
        "  estesa qui, non duplicata.",
        "- Gli atti di iniziativa governativa non hanno primo firmatario",
        "  parlamentare, quindi non hanno gruppo: vanno letti come governo, non",
        "  come partito.",
        "- Il testo tematizzabile è il **titolo**. Alla Camera è una frase",
        "  descrittiva completa, ma resta molto più corto di un articolo di",
        "  stampa: un topic model tarato sul layer 3 non si applica tale e quale.",
        "- Presentare un DDL non è approvarlo. Questo dataset misura ciò che un",
        "  gruppo *propone*, non ciò che il Parlamento *decide*.",
        "",
    ]
    path.write_text("\n".join(righe), encoding="utf-8")


def main():
    args = parse_args()
    legislature = args.legislatura or sorted(camera_ddl.LEGISLATURE)

    tutti, misure = [], []
    for legislatura in legislature:
        print(f"Legislatura {legislatura}...")
        richieste = {"n": 0}

        def conta(query, endpoint):
            richieste["n"] += 1
            return camera_ddl.interroga(query, endpoint)

        avvio = time.perf_counter()
        righe = camera_ddl.scarica_legislatura(legislatura, pagina=args.pagina,
                                               interrogatore=conta)
        records = camera_ddl.normalizza(righe, legislatura)
        durata = time.perf_counter() - avvio
        tutti.extend(records)
        misure.append({"legislatura": legislatura, "atti": len(records),
                       "righe": len(righe), "richieste": richieste["n"],
                       "secondi": durata})
        print(f"  {len(records):,} atti da {len(righe):,} righe "
              f"in {richieste['n']} richieste ({durata:.1f}s)")

    scrivi_jsonl(tutti, OUT_JSONL)
    scrivi_report(misure, tutti, OUT_REPORT)
    print(f"\nOutput: {OUT_JSONL.relative_to(ROOT)}")
    print(f"        {OUT_REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
