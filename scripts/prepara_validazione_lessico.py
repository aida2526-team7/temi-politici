#!/usr/bin/env python3
"""Prepara il campione per la validazione umana del lessico sui 15 macrotemi.

Domanda a cui serve rispondere: quando `src/mappa_ontologia.py` assegna un
macrotema, ci azzecca? Oggi ogni numero del progetto poggia su 350 pattern
scritti a mano e mai controllati contro qualcuno che abbia letto gli articoli.

Non sostituisce `docs/topic_annotation_protocol.md`, che fa un'altra cosa:
quello chiede se un topic NMF e' coerente, questo chiede di che tema parla un
articolo. Convivono.

## Come e' composto il campione

100 articoli, e la composizione non e' un dettaglio:

- **60 stratificati**, 4 per ciascuno dei 15 macrotemi -> misurano la *precisione*:
  quando il lessico dice "Sanita'", e' davvero sanita'?
- **20 fra i `non assegnato`** -> misurano il *recall*: quanti temi si perde.
- **20 casuali** -> stimano l'accuratezza sul corpus vero.

I 20 casuali sono la parte che si salta piu' spesso ed e' quella che conta di
piu': controllare solo cio' che il lessico ha gia' etichettato dice quanto e'
preciso, mai quanto gli sfugge. E' esattamente l'errore che stava per passare col
caro carburanti, che usciva `non assegnato` senza che nessuno lo notasse.

## Perche' i file dei revisori sono ciechi

Il file che ricevono NON contiene la risposta del lessico, e nemmeno lo strato di
campionamento - sapere che una riga viene dallo strato "Sanita'" e' sapere la
risposta. Le righe sono anche mescolate, altrimenti l'ordine la rivela lo stesso.

Se un revisore vede l'esito automatico non sta validando, sta confermando.

Uso:
    python scripts/prepara_validazione_lessico.py
    python scripts/prepara_validazione_lessico.py --per-tema 6 --casuali 30
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import mappa_ontologia as mo  # noqa: E402

REVIEW_IN = ROOT / "data/processed/news_topic_review.csv"
CAMPIONE_IN = ROOT / "data/processed/news_topic_review_campione.csv"
OUT_CHIAVE = ROOT / "reports/validazione_lessico"
OUT_REVISORI = ROOT / "annotations/validazione_lessico"

SEED = 42
REVISORI = ("R1", "R2")
RIGHE_CALIBRAZIONE = 10

# Quello che il revisore vede. Nient'altro: niente esito del lessico, niente
# strato, niente topic NMF.
COLONNE_VISIBILI = ["id_riga", "fase", "data", "dominio", "titolo", "estratto", "url"]
COLONNE_DA_COMPILARE = ["macrotema", "macrotema_secondario", "frame_woke", "note"]


def sorgente() -> Path:
    return REVIEW_IN if REVIEW_IN.exists() else CAMPIONE_IN


def leggi_e_classifica(path: Path) -> tuple[list[dict], defaultdict]:
    """Ogni articolo con l'esito del lessico, e gli indici raggruppati per esito."""
    righe = []
    per_esito: defaultdict[str, list[int]] = defaultdict(list)
    with path.open(encoding="utf-8-sig") as handle:
        for indice, riga in enumerate(csv.DictReader(handle)):
            testo = f"{riga.get('title', '')} {riga.get('estratto', '')}"
            if mo.quota_boilerplate(testo) > 0:
                esito: int | str = mo.BOILERPLATE
            else:
                esito, _ = mo.classifica(testo)
            righe.append({
                "indice": indice,
                "data": riga.get("seendate", ""),
                "dominio": riga.get("domain", ""),
                "titolo": riga.get("title", ""),
                "estratto": (riga.get("estratto", "") or "")[:600],
                "url": riga.get("url", ""),
                "esito_lessico": mo.etichetta(esito),
                "marcatori_lessico": ",".join(mo.marcatori(testo)),
            })
            per_esito[mo.etichetta(esito)].append(indice)
    return righe, per_esito


def campiona(righe: list[dict], per_esito: dict, per_tema: int,
             non_assegnati: int, casuali: int) -> list[dict]:
    rng = random.Random(SEED)
    scelti: dict[int, str] = {}

    for tema in mo.MACROTEMI.values():
        candidati = [i for i in per_esito.get(tema, []) if i not in scelti]
        for indice in rng.sample(candidati, min(per_tema, len(candidati))):
            scelti[indice] = f"stratificato:{tema}"

    candidati = [i for i in per_esito.get(mo.NON_ASSEGNATO, []) if i not in scelti]
    for indice in rng.sample(candidati, min(non_assegnati, len(candidati))):
        scelti[indice] = "non_assegnato"

    tutti = [r["indice"] for r in righe if r["indice"] not in scelti]
    for indice in rng.sample(tutti, min(casuali, len(tutti))):
        scelti[indice] = "casuale"

    per_indice = {r["indice"]: r for r in righe}
    campione = [{**per_indice[i], "strato": strato} for i, strato in scelti.items()]
    # Mescolare non e' cosmetico: righe ordinate per strato rivelano la risposta.
    rng.shuffle(campione)
    for posizione, riga in enumerate(campione, start=1):
        riga["id_riga"] = f"V{posizione:03d}"
        riga["fase"] = "calibrazione" if posizione <= RIGHE_CALIBRAZIONE else "indipendente"
    return campione


def scrivi_chiave(campione: list[dict]) -> Path:
    """Il file con le risposte del lessico. Non va dato ai revisori."""
    OUT_CHIAVE.mkdir(parents=True, exist_ok=True)
    percorso = OUT_CHIAVE / "chiave_lessico.csv"
    colonne = ["id_riga", "fase", "strato", "esito_lessico", "marcatori_lessico",
               "data", "dominio", "titolo", "url"]
    with percorso.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=colonne, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(campione)
    return percorso


def scrivi_revisori(campione: list[dict]) -> list[Path]:
    OUT_REVISORI.mkdir(parents=True, exist_ok=True)
    scritti = []
    for revisore in REVISORI:
        percorso = OUT_REVISORI / f"revisore_{revisore}.csv"
        with percorso.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=COLONNE_VISIBILI + COLONNE_DA_COMPILARE)
            writer.writeheader()
            for riga in campione:
                writer.writerow({**{c: riga.get(c, "") for c in COLONNE_VISIBILI},
                                 **{c: "" for c in COLONNE_DA_COMPILARE}})
        scritti.append(percorso)
    return scritti


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--per-tema", type=int, default=4)
    parser.add_argument("--non-assegnati", type=int, default=20)
    parser.add_argument("--casuali", type=int, default=20)
    args = parser.parse_args()

    percorso = sorgente()
    print(f"Sorgente: {percorso.relative_to(ROOT)}")
    righe, per_esito = leggi_e_classifica(percorso)
    print(f"{len(righe):,} articoli classificati dal lessico")

    campione = campiona(righe, per_esito, args.per_tema, args.non_assegnati, args.casuali)
    composizione = defaultdict(int)
    for riga in campione:
        composizione[riga["strato"].split(":")[0]] += 1
    print(f"\nCampione: {len(campione)} articoli")
    for strato, quanti in sorted(composizione.items()):
        print(f"  {strato:16s} {quanti:3d}")

    chiave = scrivi_chiave(campione)
    revisori = scrivi_revisori(campione)

    manifest = {
        "generato_utc": datetime.now(timezone.utc).isoformat(),
        "sorgente": str(percorso.relative_to(ROOT)).replace("\\", "/"),
        "articoli_nel_corpus": len(righe),
        "seed": SEED,
        "composizione": dict(composizione),
        "righe_calibrazione": RIGHE_CALIBRAZIONE,
        "colonne_viste_dal_revisore": COLONNE_VISIBILI,
        "cecita": ("I file dei revisori non contengono l'esito del lessico ne' lo strato "
                   "di campionamento, e le righe sono mescolate: lo strato da solo "
                   "rivelerebbe la risposta."),
    }
    (OUT_CHIAVE / "validazione_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nChiave (NON ai revisori): {chiave.relative_to(ROOT)}")
    for percorso_revisore in revisori:
        print(f"Da girare:                {percorso_revisore.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
