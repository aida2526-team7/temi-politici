#!/usr/bin/env python3
"""Porta nella dashboard i dati che la pagina deve leggere.

Perché una copia e non una lettura diretta di `reports/`: la pagina deve poter
essere renderizzata e pubblicata da sola, senza dipendere da percorsi che
risalgono fuori dalla sua cartella. La copia è piccola — pochi KB — e viene
rigenerata da qui, mai modificata a mano.

Nessun numero viene calcolato in questo file che non sia già stato calcolato
dalla pipeline: qui si aggrega solo ciò che serve alla forma di un grafico, e
tabella e grafico leggono sempre la stessa riga.

Uso:
    python dashboard/build_data.py
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pandas as pd

DASH = Path(__file__).resolve().parent
ROOT = DASH.parent
SORGENTE = ROOT / "reports/ontologia_mapping"
DATI = DASH / "data"

# Copiati tali e quali: la pipeline li scrive già nella forma giusta.
DA_COPIARE = [
    "distribuzione_layer.csv",
    "marcatori_per_mese.csv",
    "marcatori_per_tema.csv",
    "indice_h1.csv",
    "layer3_topic_nmf.csv",
    "layer1_controllo_fonti.csv",
    "partiti_per_tema.csv",
]


def distribuzione_lunga() -> pd.DataFrame:
    """La tabella delle tre distribuzioni in forma lunga, che è ciò che Altair vuole.

    Le categorie di servizio restano dentro con un flag invece di essere buttate:
    servono al grafico che le mostra a parte, e il denominatore delle quote le
    include comunque.
    """
    larga = pd.read_csv(SORGENTE / "distribuzione_layer.csv")
    lunga = larga.melt(
        id_vars=["id", "macrotema"],
        value_vars=["layer1_programmi_pct", "layer2_ddl_pct", "layer3_stampa_pct"],
        var_name="layer", value_name="quota")
    lunga["layer"] = lunga["layer"].map({
        "layer1_programmi_pct": "Programmi",
        "layer2_ddl_pct": "Progetti di legge",
        "layer3_stampa_pct": "Stampa"})
    lunga["macrotema_id"] = pd.to_numeric(lunga["id"], errors="coerce")
    lunga["e_macrotema"] = lunga["macrotema_id"].notna()
    return lunga


def quadrante() -> pd.DataFrame:
    """Un punto per macrotema: attenzione della stampa contro attività legislativa.

    Le mediane dei due assi tagliano il piano in quattro. Non è una decorazione:
    i due riquadri fuori diagonale sono la domanda del progetto — di cosa si
    parla senza legiferare, e su cosa si legifera senza che se ne parli.
    """
    larga = pd.read_csv(SORGENTE / "distribuzione_layer.csv")
    temi = larga[larga["id"].notna()].copy()
    temi["id"] = temi["id"].astype(int)
    temi = temi.rename(columns={
        "layer3_stampa_pct": "stampa",
        "layer2_ddl_pct": "leggi",
        "layer1_programmi_pct": "programmi"})
    mediana_x, mediana_y = temi["stampa"].median(), temi["leggi"].median()
    temi["quadrante"] = [
        ("Se ne parla e si legifera" if leggi >= mediana_y else "Se ne parla soltanto")
        if stampa >= mediana_x else
        ("Si legifera in silenzio" if leggi >= mediana_y else "Ai margini")
        for stampa, leggi in zip(temi["stampa"], temi["leggi"])]
    temi["mediana_stampa"] = mediana_x
    temi["mediana_leggi"] = mediana_y
    return temi[["id", "macrotema", "stampa", "leggi", "programmi",
                 "quadrante", "mediana_stampa", "mediana_leggi"]]


def main() -> int:
    DATI.mkdir(parents=True, exist_ok=True)
    for nome in DA_COPIARE:
        origine = SORGENTE / nome
        if origine.exists():
            shutil.copy2(origine, DATI / nome)
            print(f"  copiato   {nome}")
        else:
            print(f"  MANCANTE  {nome}")

    distribuzione_lunga().to_csv(DATI / "distribuzione_lunga.csv", index=False)
    print("  costruito distribuzione_lunga.csv")
    quadrante().to_csv(DATI / "quadrante.csv", index=False)
    print("  costruito quadrante.csv")

    manifest = json.loads((SORGENTE / "mapping_manifest.json").read_text(encoding="utf-8"))
    (DATI / "meta.json").write_text(json.dumps({
        "generato_utc": manifest["generato_utc"],
        "ontologia": manifest["ontologia"],
        "copertura": manifest["copertura_pct_assegnati"],
        "politica_non_tematica": manifest["politica_non_tematica_pct"],
        "divergenze": manifest["divergenza_variazione_totale_pp"],
        "marcatori": manifest["marcatori_trasversali"],
        "sottotemi": manifest["sottotemi"],
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print("  costruito meta.json")
    print(f"\nDati in {DATI.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
