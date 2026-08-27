#!/usr/bin/env python3
"""Integra il layer 1 con i programmi 2022 presi dai siti di partito.

Perché serve. Il deposito al portale *Elezioni trasparenti* è pesato al contrario
rispetto a ciò che serve: i partiti con più attività legislativa hanno depositato i
programmi più corti. Lega 938 progetti di legge contro 14 paragrafi di programma,
M5S 936 contro 13, FdI 832 contro 24. Stimare una distribuzione su 15 macrotemi da
13 unità non è una misura, e l'indice di coerenza programmatica H1 è una distanza
fra distribuzioni: l'errore si somma su entrambi i lati.

Il testo depositato non è corrotto — Lega 18.750 caratteri, M5S 19.373, integri. È
corto perché è quello che i partiti hanno scelto di depositare. Il programma pieno
sta sul sito del partito, e dove non è più online sta su Wayback.

Cosa NON risolve. Un programma preso dal sito non è la stessa unità del deposito al
Viminale: il deposito è l'atto formale previsto dalla legge 165/2017, il file sul
sito è materiale di campagna, aggiornabile e senza data certa. Il record lo dichiara
in `fonte`, e il PD è incluso come **controllo**: ha entrambi, quindi la distanza fra
le sue due distribuzioni misura quanto le due unità divergono davvero.

Uso:
    python scripts/run_programmi_integrazione.py
    python scripts/run_programmi_integrazione.py --partito lega --partito m5s
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from harvester import extract_pdf_text, fetch_response  # noqa: E402
from ocr_pdf import ocr_pdf, serve_ocr  # noqa: E402

DEFAULT_CONFIG = ROOT / "config/programmi_integrazione.json"

# Stessa soglia di src/programmi_fulltext.py: sotto questa un PDF non e' un
# programma, e' una copertina o un errore di download.
MIN_CHARS_PROGRAMMA = 2000


def leggi_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def gia_scaricati(path: Path) -> dict[str, dict]:
    """I record gia' presi, per non ripetere download da decine di MB.

    Wayback limita le richieste e i PDF dei programmi pesano: senza ripartenza, un
    rifiuto sull'ultimo file butta via tutti quelli prima. Stessa logica della
    cache OCR in src/programmi_fulltext.py.
    """
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as handle:
        record = (json.loads(riga) for riga in handle if riga.strip())
        return {r["partito_id"]: r for r in record
                if r.get("partito_id") and r.get("chars", 0) >= MIN_CHARS_PROGRAMMA}


def scarica(voce: dict, timeout: int, tentativi: int, pausa: float) -> dict | None:
    """Un record nello schema del layer 1, o None se il documento non si legge."""
    print(f"  {voce['partito_id']:6s} {voce['fonte']:12s} ...", end="", flush=True)
    response = None
    for tentativo in range(1, tentativi + 1):
        response = fetch_response(voce["url"], timeout=timeout)
        if response is not None:
            break
        if tentativo < tentativi:
            attesa = pausa * 2 ** tentativo
            print(f" ritento fra {attesa:.0f}s...", end="", flush=True)
            time.sleep(attesa)
    if response is None:
        print(f" non scaricabile dopo {tentativi} tentativi")
        return None

    testo = extract_pdf_text(response.content)
    estrazione = "nativa"
    if serve_ocr(testo):
        print(" OCR...", end="", flush=True)
        testo = ocr_pdf(response.content)
        estrazione = "ocr"

    record = {
        "partito_id": voce["partito_id"],
        "url": voce["url_originale"],
        "domain": voce["url_originale"].split("/")[2],
        "seendate": voce["seendate"],
        "title": voce["partito_lista"],
        "text": testo,
        "chars": len(testo),
        "language": "it",
        "estrazione": estrazione,
        "partiti": [voce["partito_lista"]],
        "partito_lista": voce["partito_lista"],
        "gruppo_camera": voce["gruppo_camera"],
        "tipo_documento": "programma",
        "consultazione": voce.get("consultazione", "politiche2022"),
        # Distingue il deposito formale dal materiale di campagna. Serve a valle:
        # le due cose non sono la stessa unita' di misura.
        "fonte": voce["fonte"],
        "url_recupero": voce["url"],
        "nota": voce.get("nota", ""),
    }
    print(f" {record['chars']:8,} caratteri [{estrazione}]")
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--partito", action="append", help="ID partito; ripetibile")
    parser.add_argument("--riscarica", action="store_true",
                        help="ignora quanto gia' scaricato e riprende tutto da capo")
    args = parser.parse_args()

    config = leggi_config(args.config)
    voci = config["programmi"]
    if args.partito:
        voci = [v for v in voci if v["partito_id"] in set(args.partito)]
        if not voci:
            print(f"ERRORE: nessun partito fra {sorted(set(args.partito))}", file=sys.stderr)
            return 2

    for voce in voci:
        voce.setdefault("consultazione", config.get("consultazione", "politiche2022"))

    out = ROOT / config["output_jsonl"]
    cache = {} if args.riscarica else gia_scaricati(out)
    if cache:
        print(f"Gia' in cache: {', '.join(sorted(cache))}")

    print(f"Integrazione layer 1: {len(voci)} programmi")
    records = list(cache.values())
    pausa = config.get("pause", 1.0)
    for voce in voci:
        if voce["partito_id"] in cache:
            continue
        record = scarica(voce, config.get("timeout", 60),
                         config.get("tentativi", 4), pausa)
        if record is not None:
            records.append(record)
        time.sleep(pausa)

    buoni = [r for r in records if r["chars"] >= MIN_CHARS_PROGRAMMA]
    scartati = [r for r in records if r["chars"] < MIN_CHARS_PROGRAMMA]
    for record in scartati:
        print(f"  scartato sotto {MIN_CHARS_PROGRAMMA} caratteri: {record['partito_lista']}")

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as handle:
        for record in buoni:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"\n{len(buoni)} programmi scritti. Caratteri per partito:")
    for record in sorted(buoni, key=lambda r: -r["chars"]):
        print(f"  {record['partito_lista'][:44]:46s} {record['chars']:8,}  [{record['fonte']}]")
    print(f"\nOutput: {out.relative_to(ROOT)}")
    print("Prossimo passo: python scripts/run_mappa_ontologia.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
