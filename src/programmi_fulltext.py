"""Driver full-text del layer 1: dai metadata dei programmi al testo.

  scripts/run_viminale_discovery.py -> data/raw/programmi_viminale_urls.jsonl
  QUESTO modulo                     -> data/raw/programmi_fulltext.jsonl

Stessa struttura di src/mediacloud_fulltext.py, che fa lo stesso lavoro per il
layer 3: legge i metadata, li passa a `harvester.scrape_metas` (il motore
condiviso) e post-processa i record restituiti.

Perche' il join: `harvester.parse_pdf` costruisce un dizionario con i campi che
conosce (url/domain/seendate/title/text/chars) e ignora gli altri. I campi propri
del layer 1 — `partiti`, `tipo_documento`, `consultazione` — vanno riattaccati
qui, appaiando per URL.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

# I nomi delle liste contengono caratteri che la console Windows (cp1252) non sa
# codificare (es. SŰDTIROLER): senza questo, stamparli solleva UnicodeEncodeError.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from harvester import fetch_response, scrape_metas

sys.path.insert(0, str(ROOT))
from src.ocr_pdf import ocr_pdf, serve_ocr

URLS_IN = ROOT / "data" / "raw" / "programmi_viminale_urls.jsonl"
FULLTEXT_OUT = ROOT / "data" / "raw" / "programmi_fulltext.jsonl"
# Cache dell'OCR: e' la parte cara del lavoro, e va conservata fra le
# esecuzioni. Non versionata (data/raw/*.jsonl e' in .gitignore).
CACHE_OCR = ROOT / "data" / "raw" / "programmi_ocr_cache.jsonl"

# I programmi sono documenti lunghi: sotto questa soglia c'e' un file rotto o una
# scansione che nemmeno l'OCR ha saputo leggere. La soglia del layer 3 (200) e'
# tarata sugli articoli di stampa, non su un programma di 50 pagine.
MIN_CHARS_PROGRAMMA = 2000

# scrape_metas scarta i record con chars <= min_chars. Qui serve tenerli tutti,
# perche' un PDF scansionato esce con chars = 0 ed e' proprio quello da mandare
# in OCR: il filtro vero si applica dopo.
TIENI_TUTTO = -1


def leggi_metadata(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(
            f"Metadata assenti: {path}. Esegui prima scripts/run_viminale_discovery.py"
        )
    with path.open(encoding="utf-8") as handle:
        return [json.loads(riga) for riga in handle if riga.strip()]


def rifai_join(records: list[dict], metas: list[dict]) -> list[dict]:
    """Riattacca ai record i campi del layer 1, appaiando per URL."""
    per_url = {meta["url"]: meta for meta in metas}
    uniti = []
    for record in records:
        meta = per_url.get(record["url"], {})
        record.update({
            "partiti": meta.get("partiti", []),
            "partito_lista": meta.get("partito_lista", ""),
            "coalizione": meta.get("coalizione", False),
            "tipo_documento": meta.get("tipo_documento", ""),
            "fonte": meta.get("fonte", ""),
            "consultazione": meta.get("consultazione", ""),
        })
        uniti.append(record)
    return uniti


def leggi_cache(path: Path) -> dict[str, str]:
    """Testi gia' riconosciuti nelle esecuzioni precedenti, per URL."""
    if not path.exists():
        return {}
    cache = {}
    with path.open(encoding="utf-8") as handle:
        for riga in handle:
            if not riga.strip():
                continue
            voce = json.loads(riga)
            cache[voce["url"]] = voce["text"]
    return cache


def applica_ocr(records: list[dict], cache_path: Path | None = None) -> list[dict]:
    """OCR dei record senza testo nativo.

    E' un fallback: i programmi depositati come PDF veri restano come sono, e sono
    piu' fedeli di qualsiasi riconoscimento. Solo le scansioni passano di qui.

    Ogni record dichiara come e' stato letto nel campo `estrazione`: un testo
    riconosciuto da un'immagine non e' il testo depositato, e chi legge i
    risultati deve poterlo distinguere.

    RIPARTIBILE. Ogni documento riconosciuto va subito in `cache_path`, e un
    rilancio lo salta. Sono 46 documenti, alcuni da minuti l'uno: senza cache
    un'interruzione al quarantesimo butta via tutto il lavoro — ed e' successo.
    """
    da_ocr = [r for r in records if serve_ocr(r.get("text", ""))]
    if not da_ocr:
        return records

    cache_path = cache_path or CACHE_OCR
    cache = leggi_cache(cache_path)
    cache_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"\nOCR di {len(da_ocr)} documenti scansionati (nessun testo nativo)."
          f" Gia' in cache: {sum(1 for r in da_ocr if r['url'] in cache)}", flush=True)
    for numero, record in enumerate(da_ocr, 1):
        etichetta = (record.get("title") or record["url"].split("/")[-1])[:40]

        if record["url"] in cache:
            testo = cache[record["url"]]
            record["text"] = testo
            record["chars"] = len(testo)
            record["estrazione"] = "ocr" if testo else "fallita"
            print(f"  {numero:2d}/{len(da_ocr)}  {etichetta:42s} {len(testo):7,} "
                  f"caratteri  [cache]", flush=True)
            continue

        response = fetch_response(record["url"], timeout=90)
        if response is None:
            record["estrazione"] = "fallita"
            print(f"  {numero:2d}/{len(da_ocr)}  {etichetta:42s} non scaricabile",
                  flush=True)
            continue
        testo = ocr_pdf(response.content)
        record["text"] = testo
        record["chars"] = len(testo)
        record["estrazione"] = "ocr" if testo else "fallita"
        # Si scrive PRIMA di passare al prossimo: il costo e' gia' stato pagato.
        with cache_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({"url": record["url"], "text": testo},
                                    ensure_ascii=False) + "\n")
        print(f"  {numero:2d}/{len(da_ocr)}  {etichetta:42s} {len(testo):7,} caratteri",
              flush=True)

    # harvester.parse_pdf marca gia' "nativa" i PDF con uno strato di testo e
    # lascia il campo vuoto sulle scansioni. Resta vuoto solo cio' che non e'
    # passato di qui: nessun testo leggibile, in nessun modo.
    for record in records:
        if not record.get("estrazione"):
            record["estrazione"] = "fallita"
    return records


def scrivi(records: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def riepiloga(records: list[dict]) -> None:
    print(f"\nProgrammi con testo: {len(records)}")
    if not records:
        return
    caratteri = sorted(r["chars"] for r in records)
    print(f"  caratteri: min {caratteri[0]:,} | mediana {caratteri[len(caratteri) // 2]:,} "
          f"| max {caratteri[-1]:,}")
    estrazione = Counter(r.get("estrazione", "?") for r in records)
    print(f"  estrazione: {dict(estrazione)}")
    lingue = Counter(r.get("language", "?") for r in records)
    print(f"  lingue: {dict(lingue)}")
    per_consultazione = Counter(r["consultazione"] for r in records)
    for nome, quanti in sorted(per_consultazione.items()):
        print(f"  {nome:16s} {quanti:3d}")
    per_partito: Counter = Counter()
    for record in records:
        for partito in record["partiti"]:
            per_partito[partito] += 1
    if per_partito:
        print("  per partito (le coalizioni contano per entrambi):")
        for partito, quanti in sorted(per_partito.items()):
            print(f"    {partito:20s} {quanti}")


def main() -> int:
    metas = leggi_metadata(URLS_IN)
    print(f"Metadata in ingresso: {len(metas)}")

    # workers bassi: e' un sito della pubblica amministrazione, non una CDN, e i
    # documenti sono pochi. Non c'e' motivo di aprirgli 24 connessioni.
    records = scrape_metas(metas, out=str(FULLTEXT_OUT), workers=4,
                           min_chars=TIENI_TUTTO)
    records = rifai_join(records, metas)
    records = applica_ocr(records)

    # Il filtro si applica DOPO l'OCR: prima un programma scansionato avrebbe
    # zero caratteri e verrebbe buttato senza che nessuno provi a leggerlo.
    buoni = [r for r in records if r["chars"] >= MIN_CHARS_PROGRAMMA]
    scartati = [r for r in records if r["chars"] < MIN_CHARS_PROGRAMMA]
    scrivi(buoni, FULLTEXT_OUT)

    if scartati:
        print(f"\n{len(scartati)} documenti senza testo utilizzabile nemmeno con l'OCR:")
        for record in scartati:
            print(f"  - {(record.get('partito_lista') or '?')[:44]:46s} "
                  f"{record['chars']:6,} caratteri  [{record.get('estrazione')}]")

    riepiloga(buoni)
    print(f"\nOutput: {FULLTEXT_OUT.relative_to(ROOT)}")
    return 0


def diagnostica(persi: list[dict]) -> None:
    """Perché un programma non ha testo: scansione, file rotto, o soglia.

    Senza questa distinzione "49 documenti scartati" non dice se il problema è dei
    PDF (scansioni, servirebbe OCR) o della soglia che ho scelto io.
    """
    print(f"\n{len(persi)} documenti senza testo utilizzabile. Diagnosi:")
    categorie: Counter = Counter()
    dettaglio = []
    for meta in persi:
        response = fetch_response(meta["url"])
        if response is None:
            categorie["non scaricabile"] += 1
            dettaglio.append((meta["partito_lista"], "non scaricabile", 0))
            continue
        caratteri = len(extract_pdf_text(response.content))
        if caratteri == 0:
            categoria = "scansione senza testo (servirebbe OCR)"
        elif caratteri < MIN_CHARS_PROGRAMMA:
            categoria = f"testo sotto la soglia di {MIN_CHARS_PROGRAMMA}"
        else:
            categoria = "testo presente: scartato da harvester"
        categorie[categoria] += 1
        dettaglio.append((meta["partito_lista"], categoria, caratteri))

    for categoria, quanti in categorie.most_common():
        print(f"  {quanti:3d}  {categoria}")
    print("\n  dettaglio (lista, causa, caratteri estratti):")
    for lista, categoria, caratteri in sorted(dettaglio, key=lambda x: -x[2]):
        print(f"    {lista[:40]:42s} {categoria[:38]:40s} {caratteri:7,}")


if __name__ == "__main__":
    sys.exit(main())
