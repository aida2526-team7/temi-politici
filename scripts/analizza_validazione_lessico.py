#!/usr/bin/env python3
"""Confronta i due revisori fra loro e col lessico, e ne ricava le cifre.

Il campione cieco di 100 articoli serve a rispondere a due domande, in
quest'ordine: **i due revisori sono d'accordo fra loro?** e solo dopo **il
lessico ha ragione?**. L'ordine non e' negoziabile: se il metro non e' stabile,
qualunque misura fatta con quel metro eredita la sua incertezza, e va detto
invece che nascosto dietro una percentuale.

Legge i file cosi' come i revisori li hanno restituiti — R1 in xlsx, R2 in
Numbers — perche' riconvertirli a mano e' un passaggio non tracciabile, e ogni
passaggio non tracciabile e' un punto in cui l'analisi si puo' contestare.

Scrive `reports/validazione_lessico/confronto_revisori.csv` (riga per riga) e
`dashboard/data/validazione.json` (le cifre che la dashboard mostra).

    py scripts/analizza_validazione_lessico.py
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from src.mappa_ontologia import (  # noqa: E402
    LESSICO,
    MACROTEMI,
    NON_ASSEGNATO,
    POLITICA_NON_TEMATICA,
    classifica,
)

# Le quattro categorie di servizio offerte ai revisori in ISTRUZIONI.md. Solo
# `politica non tematica` esiste anche nel classificatore: `non politico` no, ed
# e' esattamente il buco che questa analisi misura.
SERVIZIO = ("politica non tematica", "non politico", "boilerplate", "dubbio")
SENZA_POLICY = ("non politico", "boilerplate")

CANONICHE = tuple(MACROTEMI.values()) + SERVIZIO


def _piatto(testo: str) -> str:
    """Minuscolo, senza accenti, senza doppi spazi: la forma su cui confrontare.

    I file tornano con accenti mangiati (`criminalit`), lettere perse in testa
    (`olitica non tematica`) e maiuscole a caso. Sono danni di compilazione, non
    disaccordi: normalizzarli prima e' l'unico modo perche' il numero misuri
    quello che dice di misurare.
    """
    piatto = unicodedata.normalize("NFKD", str(testo or ""))
    piatto = "".join(c for c in piatto if not unicodedata.combining(c))
    piatto = piatto.replace("�", "").lower()
    return re.sub(r"\s+", " ", piatto).strip()


_INDICE = {_piatto(x): x for x in CANONICHE}


def normalizza(valore: str, note: str = "") -> str:
    """Riporta un'etichetta alla sua forma canonica, o la lascia vuota.

    Un macrotema vuoto con «dubbio» finito nelle note e' un `dubbio`: e'
    chiaramente cio' che il revisore intendeva, e trattarlo come mancante
    gonfierebbe il disaccordo con un artefatto del foglio di calcolo.
    """
    piatto = _piatto(valore)
    if not piatto:
        return "dubbio" if "dubbio" in _piatto(note) else ""
    if piatto in _INDICE:
        return _INDICE[piatto]
    # Troncature in testa o in coda: `olitica non tematica`, `criminalit`.
    contenute = [c for p, c in _INDICE.items() if p.startswith(piatto) or piatto in p]
    if len(contenute) == 1:
        return contenute[0]
    vicine = difflib.get_close_matches(piatto, list(_INDICE), n=1, cutoff=0.82)
    return _INDICE[vicine[0]] if vicine else str(valore).strip()


def leggi_revisore(percorso: Path) -> pd.DataFrame:
    """Un file di revisore, in qualunque formato sia tornato indietro."""
    suffisso = percorso.suffix.lower()
    if suffisso == ".numbers":
        from numbers_parser import Document

        righe = Document(str(percorso)).sheets[0].tables[0].rows(values_only=True)
        df = pd.DataFrame(righe[1:], columns=list(righe[0]))
    elif suffisso in (".xlsx", ".xlsm"):
        df = pd.read_excel(percorso, sheet_name=0, dtype=str)
    else:
        df = pd.read_csv(percorso, dtype=str, sep=None, engine="python")

    # R2 ha rinominato `dominio` in `Ansa`, probabilmente un completamento
    # automatico del foglio. La posizione della colonna e' rimasta la stessa.
    df.columns = [str(c).strip().lstrip("﻿") for c in df.columns]
    if "dominio" not in df.columns and len(df.columns) > 3:
        df = df.rename(columns={df.columns[3]: "dominio"})

    df["id_riga"] = df["id_riga"].astype(str).str.strip()
    note = df["note"] if "note" in df.columns else ""
    for colonna in ("macrotema", "macrotema_secondario"):
        grezzo = df[colonna] if colonna in df.columns else ""
        df[colonna] = [normalizza(v, n) for v, n in zip(grezzo, note if len(note) else [""] * len(df))]
    return df[["id_riga", "macrotema", "macrotema_secondario"]]


def occorrenze_del_vincitore(testo: str, esito: str) -> int:
    """Quante volte il lessico del tema assegnato compare nel testo.

    E' la misura di evidenza che il campo `confidenza` non da': il margine e' la
    quota di punteggio che va al vincitore, quindi vale 1,0 anche quando un solo
    lessico e' stato toccato una volta sola.
    """
    identificativo = next((i for i, nome in MACROTEMI.items() if nome == esito), None)
    if identificativo is None:
        return 0
    return sum(len(re.findall(p, testo, flags=re.IGNORECASE))
               for p in LESSICO.get(identificativo, ()))


def kappa(a: pd.Series, b: pd.Series) -> float:
    """Kappa di Cohen non pesato, sulle categorie osservate nelle due serie."""
    from sklearn.metrics import cohen_kappa_score

    return float(cohen_kappa_score(a.tolist(), b.tolist()))


def ic95(successi: int, prove: int) -> tuple[float, float]:
    """Intervallo normale al 95%. Con n = 20 e' larghissimo, ed e' il punto."""
    if not prove:
        return (0.0, 0.0)
    p = successi / prove
    mezzo = 1.96 * (p * (1 - p) / prove) ** 0.5
    return (round(max(0.0, p - mezzo) * 100, 1), round(min(1.0, p + mezzo) * 100, 1))


def costruisci(root: Path, r1: Path, r2: Path) -> tuple[pd.DataFrame, dict]:
    chiave = pd.read_csv(root / "reports/validazione_lessico/chiave_lessico.csv", dtype=str)
    chiave.columns = [c.lstrip("﻿") for c in chiave.columns]
    chiave["id_riga"] = chiave["id_riga"].str.strip()

    uno = leggi_revisore(r1).add_suffix("_r1").rename(columns={"id_riga_r1": "id_riga"})
    due = leggi_revisore(r2).add_suffix("_r2").rename(columns={"id_riga_r2": "id_riga"})
    df = chiave.merge(uno, on="id_riga").merge(due, on="id_riga")
    if len(df) != len(chiave):
        raise ValueError(f"riallineamento fallito: {len(df)} righe su {len(chiave)}")

    # Il testo che il revisore ha letto: titolo piu' estratto. Che sia lo stesso
    # su cui gira il classificatore si verifica sotto, ricalcolando l'esito.
    sorgente = pd.read_excel(r1, sheet_name=0, dtype=str) if r1.suffix.lower() == ".xlsx" \
        else pd.read_csv(r1, dtype=str, sep=None, engine="python")
    sorgente.columns = [str(c).strip().lstrip("﻿") for c in sorgente.columns]
    sorgente["id_riga"] = sorgente["id_riga"].astype(str).str.strip()
    testi = sorgente.set_index("id_riga").apply(
        lambda r: f"{r.get('titolo', '')} {r.get('estratto', '')}", axis=1)
    df["testo"] = df["id_riga"].map(testi).fillna("")

    ricalcolato = [classifica(t)[0] for t in df["testo"]]
    df["esito_ricalcolato"] = [MACROTEMI.get(x, x) if isinstance(x, int) else x
                               for x in ricalcolato]
    df["combacia"] = df["esito_ricalcolato"] == df["esito_lessico"]
    df["occorrenze"] = [occorrenze_del_vincitore(t, e)
                        for t, e in zip(df["testo"], df["esito_lessico"])]

    # --- accordo fra i due revisori --------------------------------------- #
    df["accordo_esatto"] = df["macrotema_r1"] == df["macrotema_r2"]
    df["accordo_largo"] = df["accordo_esatto"] | (
        (df["macrotema_r1"] == df["macrotema_secondario_r2"])
        | (df["macrotema_r2"] == df["macrotema_secondario_r1"]))

    # La decisione grossolana: l'articolo ha un tema di policy oppure no.
    # `dubbio` non e' una risposta a questa domanda e resta fuori dal conteggio.
    def policy(valore: str) -> str | None:
        if valore == "dubbio" or not valore:
            return None
        return "no" if valore in SENZA_POLICY or valore == POLITICA_NON_TEMATICA else "si"

    df["policy_r1"] = df["macrotema_r1"].map(policy)
    df["policy_r2"] = df["macrotema_r2"].map(policy)

    # --- il lessico contro gli umani --------------------------------------- #
    def confermato(riga, revisori=("r1", "r2"), generoso=True) -> bool:
        risposte = set()
        for r in revisori:
            risposte.add(riga[f"macrotema_{r}"])
            if generoso:
                risposte.add(riga[f"macrotema_secondario_{r}"])
        return riga["esito_lessico"] in (risposte - {""})

    df["lessico_ok_generoso"] = df.apply(confermato, axis=1)
    df["lessico_ok_r1"] = df.apply(lambda r: confermato(r, ("r1",)), axis=1)
    df["etichettato"] = ~df["esito_lessico"].isin([NON_ASSEGNATO, ""])
    df["falso_positivo_lessico"] = (
        df["etichettato"]
        & (df["policy_r1"] == "no") & (df["policy_r2"] == "no"))

    indipendenti = df[df["fase"] != "calibrazione"]
    calibrazione = df[df["fase"] == "calibrazione"]
    casuali = df[df["strato"].str.startswith("casuale", na=False)]
    etichettate = df[df["etichettato"]]
    policy_note = df[df["policy_r1"].notna() & df["policy_r2"].notna()]

    def pct(serie) -> float:
        return round(100 * float(serie.mean()), 1) if len(serie) else 0.0

    # Sullo strato casuale — l'unico non distorto — si misurano due cose: il
    # criterio stretto (l'etichetta del lessico e' il primario di un revisore) e
    # quello generoso (compare da qualche parte fra le risposte). Il primo e' la
    # stima, il secondo e' il tetto ottimistico. Darne uno solo sarebbe una scelta
    # travestita da misura.
    casuali_stretto = casuali.apply(
        lambda r: r["esito_lessico"] in {r["macrotema_r1"], r["macrotema_r2"]} - {""},
        axis=1)
    casuali_ok = int(casuali_stretto.sum())
    cifre = {
        "generato_utc": datetime.now(timezone.utc).isoformat(),
        "fonte": ("Ricalcolato da scripts/analizza_validazione_lessico.py sui file "
                  f"{r1.name} e {r2.name}, riallineati su chiave_lessico.csv. "
                  f"Esito del lessico riprodotto su {int(df['combacia'].sum())}/{len(df)} righe."),
        "ricalcolato_qui": True,
        "campione": {
            "righe": len(df),
            "calibrazione": len(calibrazione),
            "indipendenti": len(indipendenti),
            "strato_casuale": len(casuali),
        },
        "accordo_revisori": {
            "kappa_cohen": round(kappa(indipendenti["macrotema_r1"],
                                       indipendenti["macrotema_r2"]), 2),
            "esatto_pct": pct(indipendenti["accordo_esatto"]),
            "largo_pct": pct(indipendenti["accordo_largo"]),
            "calibrazione_pct": pct(calibrazione["accordo_esatto"]),
            "policy_si_no_pct": pct(policy_note["policy_r1"] == policy_note["policy_r2"]),
            "policy_si_no_kappa": round(kappa(policy_note["policy_r1"],
                                              policy_note["policy_r2"]), 2),
        },
        "lessico": {
            "precisione_generosa_pct": pct(etichettate["lessico_ok_generoso"]),
            "righe_etichettate": len(etichettate),
            "precisione_casuale_pct": pct(casuali_stretto),
            "precisione_casuale_generosa_pct": pct(casuali["lessico_ok_generoso"]),
            "casuale_ic95": list(ic95(casuali_ok, len(casuali))),
            "casuale_n": len(casuali),
            "falsi_positivi": int(df["falso_positivo_lessico"].sum()),
            "non_policy_stimato_pct": pct(
                pd.concat([df["policy_r1"], df["policy_r2"]]).dropna() == "no"),
        },
        "occorrenze": [],
        "temi_mai_confermati": [],
    }

    fasce = [("1 occorrenza", 1, 1), ("2 occorrenze", 2, 2),
             ("3-4 occorrenze", 3, 4), ("5+ occorrenze", 5, 10**6)]
    for nome, minimo, massimo in fasce:
        sotto = etichettate[etichettate["occorrenze"].between(minimo, massimo)]
        cifre["occorrenze"].append({"fascia": nome, "righe": len(sotto),
                                    "accordo_pct": pct(sotto["lessico_ok_generoso"])})

    soglie = []
    for minimo in (1, 2, 3, 4):
        sotto = df[df["occorrenze"] >= minimo]
        soglie.append({"min_punteggio": minimo, "righe": len(sotto),
                       "precisione_pct": pct(sotto["lessico_ok_generoso"])})
    cifre["soglia"] = soglie

    per_tema = (etichettate.groupby("esito_lessico")["lessico_ok_generoso"]
                .agg(["sum", "count"]))
    cifre["temi_mai_confermati"] = sorted(per_tema[per_tema["sum"] == 0].index.tolist())

    colonne = ["id_riga", "fase", "strato", "esito_lessico", "esito_ricalcolato",
               "combacia", "occorrenze", "macrotema_r1", "macrotema_secondario_r1",
               "macrotema_r2", "macrotema_secondario_r2", "accordo_esatto",
               "accordo_largo", "policy_r1", "policy_r2", "lessico_ok_generoso",
               "falso_positivo_lessico", "titolo"]
    return df[[c for c in colonne if c in df.columns]], cifre


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    # I file compilati stanno accanto alle istruzioni che i revisori hanno letto:
    # separarli renderebbe piu' difficile capire a quale giro appartengono.
    consegne = "annotations/validazione_lessico"
    parser.add_argument("--r1", default=f"{consegne}/revisore_R1_compilato.xlsx")
    parser.add_argument("--r2", default=f"{consegne}/revisore_R2_compilato.numbers")
    args = parser.parse_args()

    confronto, cifre = costruisci(REPO, REPO / args.r1, REPO / args.r2)

    uscita = REPO / "reports/validazione_lessico/confronto_revisori.csv"
    confronto.to_csv(uscita, index=False, encoding="utf-8")
    (REPO / "dashboard/data/validazione.json").write_text(
        json.dumps(cifre, ensure_ascii=False, indent=2), encoding="utf-8")

    acc = cifre["accordo_revisori"]
    les = cifre["lessico"]
    print(f"righe: {cifre['campione']['righe']} · "
          f"esito riprodotto: {int(confronto['combacia'].sum())}/{len(confronto)}")
    print(f"accordo R1/R2 indipendenti: {acc['esatto_pct']}% · kappa {acc['kappa_cohen']}")
    print(f"policy si/no: {acc['policy_si_no_pct']}% · kappa {acc['policy_si_no_kappa']}")
    print(f"lessico (generoso): {les['precisione_generosa_pct']}% su "
          f"{les['righe_etichettate']} righe · casuali {les['precisione_casuale_pct']}% "
          f"IC {les['casuale_ic95']}")
    print(f"falsi positivi: {les['falsi_positivi']} · "
          f"senza policy: {les['non_policy_stimato_pct']}%")
    print(f"mai confermati: {', '.join(cifre['temi_mai_confermati']) or 'nessuno'}")
    print(f"scritto: {uscita.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
