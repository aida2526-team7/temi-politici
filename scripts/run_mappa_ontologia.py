"""Mappa i tre layer sui 15 macrotemi dell'ontologia v2.0 e ne misura la divergenza.

L'ontologia è congelata (`docs/ontologia_tematica.md`) ma nessun layer era ancora
stato mappato su di essa: le categorie esistevano sulla carta e i tre dataset
continuavano ognuno con la propria nomenclatura. Questo script chiude il buco.

Tre operazioni diverse, come impone il contratto:

- layer 1, programmi elettorali: unità = **paragrafo**; ogni programma esce come
  distribuzione sui 15 temi, non come etichetta;
- layer 2, progetti di legge: unità = **atto**, cioè il titolo; etichetta singola;
- layer 3, stampa: unità = **articolo**. Col corpus completo in locale si
  classificano tutti gli articoli; senza, resta il campione stratificato, che va
  ripesato sulle prevalenze reali. La modalità usata finisce nel manifest.

Il confronto fra layer si fa su quote, mai su conteggi (ontologia, sezione
*Conseguenza*).

Uso:
    python scripts/run_mappa_ontologia.py

Output in `reports/ontologia_mapping/`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import mappa_ontologia as mo  # noqa: E402

CAMERA_IN = ROOT / "data/raw/camera_ddl.jsonl"
PROGRAMMI_IN = ROOT / "data/raw/programmi_fulltext.jsonl"
REVIEW_IN = ROOT / "data/processed/news_topic_review.csv"
CAMPIONE_IN = ROOT / "data/processed/news_topic_review_campione.csv"
DISTRIBUZIONE_IN = ROOT / "reports/topic_audit/topic_distribution.csv"
OUT_DIR = ROOT / "reports/ontologia_mapping"

# Sotto questa soglia un paragrafo di programma è uno slogan ("serve un cambio di
# passo"), non una posizione su un tema. L'ontologia chiede che la soglia sia
# dichiarata insieme al risultato: eccola.
MIN_CHARS_PARAGRAFO = 200


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def leggi_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(riga) for riga in handle if riga.strip()]


def quote(conteggi: Counter | dict) -> dict:
    """Da conteggi a quote percentuali. Il denominatore include `non assegnato`.

    Nasconderlo gonfierebbe ogni tema della stessa quantità e farebbe sparire
    l'unica misura di qualità che questo metodo ha.
    """
    totale = sum(conteggi.values())
    if not totale:
        return {}
    return {k: 100.0 * v / totale for k, v in conteggi.items()}


def divergenza_l1(a: dict, b: dict) -> float:
    """Distanza in variazione totale fra due distribuzioni, in punti percentuali.

    Metà della somma degli scarti assoluti: 0 = identiche, 100 = disgiunte. È la
    quota di massa che andrebbe spostata per rendere uguale una all'altra.
    """
    chiavi = set(a) | set(b)
    return 0.5 * sum(abs(a.get(k, 0.0) - b.get(k, 0.0)) for k in chiavi)


# --------------------------------------------------------------------------- #
# Layer 2 — progetti di legge: un atto, un tema
# --------------------------------------------------------------------------- #

def mappa_layer2() -> tuple[Counter, list[dict], Counter]:
    atti = leggi_jsonl(CAMERA_IN)
    conteggi: Counter = Counter()
    sotto: Counter = Counter()
    per_gruppo: defaultdict[str, Counter] = defaultdict(Counter)
    for atto in atti:
        tema, _ = mo.classifica(atto["title"])
        conteggi[tema] += 1
        figlio = mo.sottotema(atto["title"], tema)
        if figlio:
            sotto[figlio] += 1
        gruppo = (atto.get("gruppo") or "").strip()
        if gruppo:
            per_gruppo[gruppo][tema] += 1
    righe = [
        {"gruppo": g, "atti": sum(c.values()), **{str(k): v for k, v in c.items()}}
        for g, c in sorted(per_gruppo.items(), key=lambda kv: -sum(kv[1].values()))
    ]
    print(f"Layer 2: {len(atti)} atti, {len(per_gruppo)} gruppi con attribuzione")
    return conteggi, righe, sotto


# --------------------------------------------------------------------------- #
# Layer 1 — programmi elettorali: un paragrafo, un tema
# --------------------------------------------------------------------------- #

def paragrafi(testo: str) -> list[str]:
    """Spezza sugli a capo. L'OCR sbaglia la punteggiatura, molto meno gli a capo."""
    grezzi = re.split(r"\n\s*\n|\n(?=[A-ZÀ-Ù0-9])", testo)
    return [p.strip() for p in grezzi if len(p.strip()) >= MIN_CHARS_PARAGRAFO]


def mappa_layer1() -> tuple[Counter, list[dict], Counter]:
    programmi = leggi_jsonl(PROGRAMMI_IN)
    conteggi: Counter = Counter()
    sotto: Counter = Counter()
    righe = []
    for prog in programmi:
        blocchi = paragrafi(prog.get("text", ""))
        locale: Counter = Counter()
        for blocco in blocchi:
            tema, _ = mo.classifica(blocco)
            locale[tema] += 1
            conteggi[tema] += 1
            figlio = mo.sottotema(blocco, tema)
            if figlio:
                sotto[figlio] += 1
        if blocchi:
            righe.append({
                "partito_lista": prog.get("partito_lista", ""),
                "consultazione": prog.get("consultazione", ""),
                "estrazione": prog.get("estrazione", ""),
                "paragrafi": len(blocchi),
                **{str(k): round(v, 2) for k, v in quote(locale).items()},
            })
    totale_par = sum(conteggi.values())
    print(f"Layer 1: {len(programmi)} programmi, {totale_par} paragrafi "
          f"(soglia {MIN_CHARS_PARAGRAFO} caratteri)")
    return conteggi, righe, sotto


# --------------------------------------------------------------------------- #
# Layer 3 — stampa: corpus completo se c'è, campione ripesato altrimenti
# --------------------------------------------------------------------------- #

def prevalenze_topic() -> dict[int, float]:
    import csv
    with DISTRIBUZIONE_IN.open(encoding="utf-8-sig") as handle:
        return {int(r["topic_id"]): float(r["percentage"]) for r in csv.DictReader(handle)}


def _scorri_layer3() -> tuple[str, object]:
    """Il corpus stampa migliore che c'è su questa macchina.

    Col file completo si classificano tutti gli articoli e non serve nessun
    ripeso. Senza — cioè per chiunque cloni il repository, visto che i 92 MB
    stanno in `.gitignore` — resta il campione stratificato, che va ripesato
    perché ha ~400 articoli per topic a prescindere da quanto quel topic pesi.
    """
    if REVIEW_IN.exists():
        return "completo", REVIEW_IN
    return "campione", CAMPIONE_IN


def mappa_layer3() -> tuple[Counter, Counter, list[dict], str]:
    """Restituisce (quote, conteggi grezzi, tabella per topic, modalità)."""
    import csv
    modalita, sorgente = _scorri_layer3()
    per_topic: defaultdict[int, Counter] = defaultdict(Counter)
    boiler_per_topic: defaultdict[int, int] = defaultdict(int)
    grezzi: Counter = Counter()

    with sorgente.open(encoding="utf-8-sig") as handle:
        for riga in csv.DictReader(handle):
            topic = int(riga["topic_id"])
            testo = f"{riga.get('title', '')} {riga.get('estratto', '')}"
            if mo.quota_boilerplate(testo) > 0:
                tema: int | str = mo.BOILERPLATE
                boiler_per_topic[topic] += 1
            else:
                tema, _ = mo.classifica(testo)
            per_topic[topic][tema] += 1
            grezzi[tema] += 1

    totale = sum(grezzi.values())
    prevalenze = prevalenze_topic()
    quote_finali: Counter = Counter()
    tabella = []
    for topic, conteggi in sorted(per_topic.items()):
        n = sum(conteggi.values())
        if modalita == "completo":
            # Ogni articolo vale uno: la distribuzione dei topic è già quella vera.
            for tema, quanti in conteggi.items():
                quote_finali[tema] += quanti
            prevalenza = 100.0 * n / totale
        else:
            peso = prevalenze[topic] / n
            for tema, quanti in conteggi.items():
                quote_finali[tema] += quanti * peso
            prevalenza = prevalenze[topic]
        dominante, quanti_dom = conteggi.most_common(1)[0]
        tabella.append({
            "topic_id": topic,
            "prevalenza_corpus_pct": round(prevalenza, 2),
            "articoli": n,
            "macrotema_dominante": mo.etichetta(dominante),
            "quota_dominante_pct": round(100.0 * quanti_dom / n, 1),
            "boilerplate_pct": round(100.0 * boiler_per_topic[topic] / n, 1),
            "non_assegnato_pct": round(100.0 * conteggi[mo.NON_ASSEGNATO] / n, 1),
        })
    dettaglio = "tutti gli articoli" if modalita == "completo" else "campione ripesato"
    print(f"Layer 3: {totale} articoli, {dettaglio}, {len(per_topic)} topic")
    return quote_finali, grezzi, tabella, modalita


# --------------------------------------------------------------------------- #

def scrivi_csv(path: Path, righe: list[dict], colonne: list[str] | None = None) -> None:
    import csv
    if not righe:
        return
    colonne = colonne or sorted({k for r in righe for k in r})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=colonne, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(righe)


def tabella_confronto(l1: dict, l2: dict, l3: dict) -> list[dict]:
    righe = []
    servizio = [mo.POLITICA_NON_TEMATICA, mo.NON_ASSEGNATO, mo.BOILERPLATE]
    for tema in list(mo.MACROTEMI) + servizio:
        a, b, c = l1.get(tema, 0.0), l2.get(tema, 0.0), l3.get(tema, 0.0)
        if a == b == c == 0.0:
            continue
        righe.append({
            "id": tema if isinstance(tema, int) else "",
            "macrotema": mo.etichetta(tema),
            "layer1_programmi_pct": round(a, 2),
            "layer2_ddl_pct": round(b, 2),
            "layer3_stampa_pct": round(c, 2),
            "scarto_l1_l2": round(a - b, 2),
            "scarto_l2_l3": round(b - c, 2),
        })
    return righe


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    c1, per_programma, sotto1 = mappa_layer1()
    c2, per_gruppo, sotto2 = mappa_layer2()
    r3, grezzi3, per_topic, modalita3 = mappa_layer3()

    q1, q2, q3 = quote(c1), quote(c2), quote(r3)
    confronto = tabella_confronto(q1, q2, q3)

    scrivi_csv(OUT_DIR / "distribuzione_layer.csv", confronto,
               ["id", "macrotema", "layer1_programmi_pct", "layer2_ddl_pct",
                "layer3_stampa_pct", "scarto_l1_l2", "scarto_l2_l3"])
    scrivi_csv(OUT_DIR / "layer3_topic_nmf.csv", per_topic,
               ["topic_id", "prevalenza_corpus_pct", "articoli", "macrotema_dominante",
                "quota_dominante_pct", "boilerplate_pct", "non_assegnato_pct"])
    scrivi_csv(OUT_DIR / "layer1_per_programma.csv", per_programma)
    scrivi_csv(OUT_DIR / "layer2_per_gruppo.csv", per_gruppo)

    # Le distribuzioni su cui si misura la divergenza escludono le categorie di
    # servizio: confrontare il boilerplate di un layer col welfare di un altro non
    # vuol dire niente. La quota di servizio si riporta a parte, come qualità.
    def solo_temi(q: dict) -> dict:
        temi = {k: v for k, v in q.items() if isinstance(k, int)}
        tot = sum(temi.values())
        return {k: 100.0 * v / tot for k, v in temi.items()} if tot else {}

    t1, t2, t3 = solo_temi(q1), solo_temi(q2), solo_temi(q3)
    divergenze = {
        "layer1_vs_layer2": round(divergenza_l1(t1, t2), 2),
        "layer2_vs_layer3": round(divergenza_l1(t2, t3), 2),
        "layer1_vs_layer3": round(divergenza_l1(t1, t3), 2),
    }

    # I sottotemi si riportano come quota del proprio padre, non del corpus: è ciò
    # che dice se valeva la pena aprirlo.
    sottotemi = {
        figlio: {
            "layer1_su_padre_pct": round(100.0 * sotto1[figlio] / c1[padre], 2)
            if c1.get(padre) else 0.0,
            "layer2_su_padre_pct": round(100.0 * sotto2[figlio] / c2[padre], 2)
            if c2.get(padre) else 0.0,
        }
        for figlio in mo.SOTTOTEMI
        for padre in [int(figlio.split(".")[0])]
    }

    manifest = {
        "generato_utc": datetime.now(timezone.utc).isoformat(),
        "ontologia": "docs/ontologia_tematica.md v2.0 (congelata 2026-08-27)",
        "metodo": "lessicale deterministico, src/mappa_ontologia.py",
        "min_chars_paragrafo": MIN_CHARS_PARAGRAFO,
        "layer3_sorgente": modalita3,
        "input": [
            {"path": str(p.relative_to(ROOT)).replace("\\", "/"),
             "sha256": sha256(p), "byte": p.stat().st_size}
            for p in (PROGRAMMI_IN, CAMERA_IN, _scorri_layer3()[1], DISTRIBUZIONE_IN)
        ],
        "copertura_pct_assegnati": {
            layer: round(sum(v for k, v in q.items() if isinstance(k, int)), 2)
            for layer, q in (("layer1", q1), ("layer2", q2), ("layer3", q3))
        },
        # Quanto ogni layer parla di politica come processo invece che di policy.
        # Sul layer 3 è l'indice di game frame; sui layer 1 e 2 è la linea di base
        # dal lato dei politici, che quando fanno hanno sempre un oggetto.
        "politica_non_tematica_pct": {
            "layer1": round(q1.get(mo.POLITICA_NON_TEMATICA, 0.0), 2),
            "layer2": round(q2.get(mo.POLITICA_NON_TEMATICA, 0.0), 2),
            "layer3": round(q3.get(mo.POLITICA_NON_TEMATICA, 0.0), 2),
        },
        "divergenza_variazione_totale_pp": divergenze,
        "sottotemi": sottotemi,
        "avvertenza": (
            "Le quote sono confrontabili fra layer solo come quote: le tre unità di "
            "misura (paragrafo, atto, articolo) hanno dimensioni di ordini di "
            "grandezza diversi. Il lessico non è validato contro codifica umana."
        ),
    }
    (OUT_DIR / "mapping_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\nCopertura (quota di unità assegnate a un macrotema):")
    for layer, valore in manifest["copertura_pct_assegnati"].items():
        print(f"  {layer}: {valore:5.1f}%")
    print("\nDivergenza fra layer (variazione totale, punti percentuali):")
    for coppia, valore in divergenze.items():
        print(f"  {coppia}: {valore:5.1f}")
    print("\nPolitica come processo invece che come policy:")
    for layer, valore in manifest["politica_non_tematica_pct"].items():
        print(f"  {layer}: {valore:5.1f}%")
    print("\nSottotemi (quota del proprio macrotema padre):")
    for figlio, valori in sottotemi.items():
        print(f"  {figlio} {mo.etichetta(figlio)}: L1 "
              f"{valori['layer1_su_padre_pct']:.1f}%  L2 {valori['layer2_su_padre_pct']:.1f}%")
    print(f"\nOutput: {OUT_DIR.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
