#!/usr/bin/env python3
"""Ingest delle intenzioni di voto dal registro ufficiale dei sondaggi.

Serve a rispondere a una domanda che i temi da soli non chiudono: quando un
partito viene nominato piu' spesso in relazione a un tema, le sue intenzioni di
voto si muovono?

Questo script porta a casa **meta' della risposta** - la serie delle intenzioni di
voto. L'altra meta', partito x tema x settimana, si ricostruisce dal corpus stampa
applicando il lessico di src/mediacloud_spike.py.

Prima di costruire qualsiasi correlazione va guardata la varianza della serie: il
margine d'errore dichiarato dagli istituti sta attorno a +/- 2,6 punti su campioni
da 1.400, e fuori campagna elettorale i movimenti mensili sono spesso piu' piccoli
di cosi'. Se la serie e' piatta dentro l'errore, non c'e' niente da correlare, e
saperlo costa un grafico invece di una settimana.

Il registro e' un sito della pubblica amministrazione: una richiesta alla volta,
con pausa. Non c'e' nessuna fretta.

Uso:
    python scripts/run_sondaggi_intenzioni.py
    python scripts/run_sondaggi_intenzioni.py --max-sondaggi 5 --dry-run
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import sondaggi_intenzioni as si  # noqa: E402

DEFAULT_CONFIG = ROOT / "config/sondaggi_intenzioni.json"


def leggi_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def raccogli(config: dict, max_sondaggi: int | None,
             verbose: bool) -> tuple[list[dict], list[tuple]]:
    """Percorre il registro e restituisce una riga per partito per rilevazione."""
    pausa = config.get("pause", 1.0)
    timeout = config.get("timeout", 90)
    sessione = si.apri_sessione(config["user_agent"])
    risposta = sessione.get(si.LISTA, timeout=timeout)
    filtri = si.campi_ricerca(config)
    risposta = si.postback(sessione, si.LISTA, risposta.text,
                           {**filtri, "ctl00$Contenuto$FiltriListaSondaggi": "Cerca"},
                           timeout, pausa)

    totale_pagine = si.pagine_totali(risposta.text)
    print(f"Ricerca: titolo «{config['titolo']}», "
          f"{config['data_da']}-{config['data_a']}, {totale_pagine} pagine")

    record: list[dict] = []
    saltati: list[tuple] = []
    visti = 0
    for pagina in range(1, totale_pagine + 1):
        if pagina > 1:
            risposta = si.postback(
                sessione, si.LISTA, risposta.text,
                {**filtri, "ctl00$Contenuto$dgSondaggi_VaiAPaginaTextBox": str(pagina),
                 "ctl00$Contenuto$dgSondaggi_VaiAPaginaBottone": "Vai"},
                timeout, pausa)
        righe = si._valori_input(risposta.text, r"dgSondaggi_Row\d+_DataInserimento$")
        print(f"  pagina {pagina}/{totale_pagine}: {len(righe)} sondaggi")
        lista_html = risposta.text

        for nome, data_inserimento in righe:
            if max_sondaggi is not None and visti >= max_sondaggi:
                return record, saltati
            visti += 1
            scheda = si.postback(sessione, si.LISTA, lista_html,
                                 {**filtri, nome: data_inserimento}, timeout, pausa)
            meta = si.metadati(scheda.text)
            domande_html = si.postback(
                sessione, si.SCHEDA, scheda.text,
                {"__EVENTTARGET": "ctl00$Titolo$TabSondaggio$DomandeRisposte"},
                timeout, pausa).text

            trovate = si._valori_input(domande_html, r"dgDomande_Row\d+_Domanda$")
            candidate = [(n, t) for n, t in trovate if si.DOMANDA_VOTO.search(t)]
            if verbose:
                print(f"    {meta['realizzatore'][:28]:30s} {meta['data_da']}-{meta['data_a']}"
                      f"  {len(trovate)} domande, {len(candidate)} candidate")

            # La scheda rende gia' il dettaglio di una domanda. Se e' quella che
            # serve, il lavoro e' finito senza un'altra richiesta al sito.
            mostrata = si.domanda_mostrata(domande_html)
            for nome_domanda, testo_domanda in candidate:
                if si.normalizza(mostrata)[:60] == si.normalizza(testo_domanda)[:60]:
                    testo_risposta = domande_html
                else:
                    aperta = si.postback(
                        sessione, si.SCHEDA, domande_html,
                        {nome_domanda: testo_domanda,
                         "ctl00$Titolo$TabSondaggio$DomandeRisposte": "Domande"},
                        timeout, pausa)
                    if si.normalizza(si.domanda_mostrata(aperta.text))[:60] != \
                            si.normalizza(testo_domanda)[:60]:
                        saltati.append((meta["realizzatore"], meta["data_a"], testo_domanda))
                        continue
                    testo_risposta = aperta.text
                righe_risposta = si.risposte(testo_risposta)
                if not si.e_intenzione_di_voto(testo_domanda, righe_risposta):
                    continue
                quote, base = si.normalizza_quote(righe_risposta)
                colonne = max((len(v) for _, v in righe_risposta), default=1)
                for partito, valori in quote.items():
                    record.append({
                        "data_da": meta["data_da"],
                        "data_a": meta["data_a"],
                        "realizzatore": si.normalizza_istituto(meta["realizzatore"]),
                        "realizzatore_grezzo": meta["realizzatore"],
                        "committente": meta["committente"],
                        "partito": partito,
                        "valore_grezzo": round(valori["grezzo"], 2),
                        "valore_normalizzato": round(valori["normalizzato"], 2),
                        "base_grezza": round(base, 2),
                        "colonne_risposta": colonne,
                        "domanda": testo_domanda[:200],
                        "fonte": "sondaggipoliticoelettorali.it",
                    })
                print(f"    + {meta['realizzatore'][:26]:28s} {meta['data_a']}  "
                      f"{len(quote)} partiti, base grezza {base:.1f}%")
                break  # una domanda di intenzione di voto per sondaggio basta

    return record, saltati


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--max-sondaggi", type=int, help="fermati dopo N sondaggi")
    parser.add_argument("--dry-run", action="store_true", help="non scrive il CSV")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    config = leggi_config(args.config)
    record, saltati = raccogli(config, args.max_sondaggi, args.verbose)
    if saltati:
        print(f"\n{len(saltati)} domande candidate non estratte: il registro non "
              f"serve il dettaglio di una domanda fuori dalla prima posizione.")
        for realizzatore, data, testo in saltati[:8]:
            print(f"    {realizzatore[:26]:28s} {data}  {testo[:56]}")
    if not record:
        print("Nessuna intenzione di voto estratta.", file=sys.stderr)
        return 1

    rilevazioni = {(r["realizzatore"], r["data_a"]) for r in record}
    istituti = sorted({r["realizzatore"] for r in record})
    print(f"Istituti: {', '.join(istituti)}")
    print(f"\n{len(record)} righe da {len(rilevazioni)} rilevazioni")
    basi = sorted(r["base_grezza"] for r in record)
    print(f"Base grezza dei soli partiti: min {basi[0]:.1f}%  "
          f"mediana {basi[len(basi) // 2]:.1f}%  max {basi[-1]:.1f}%")
    print("Quanto la normalizzazione sposta: la distanza di ogni base da 100.")

    if args.dry_run:
        print("\n--dry-run: niente file scritto.")
        return 0

    out = ROOT / config["output_csv"]
    out.parent.mkdir(parents=True, exist_ok=True)
    colonne = list(record[0])
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=colonne)
        writer.writeheader()
        writer.writerows(record)

    manifest = {
        "generato_utc": datetime.now(timezone.utc).isoformat(),
        "fonte": "https://www.sondaggipoliticoelettorali.it",
        "filtro_titolo": config["titolo"],
        "periodo": [config["data_da"], config["data_a"]],
        "righe": len(record),
        "rilevazioni": len(rilevazioni),
        "normalizzazione": (
            "Quote rinormalizzate a 100 sui soli partiti riconosciuti. Il valore "
            "grezzo e la base restano nel CSV: senza la base la quota normalizzata "
            "non e' giudicabile."
        ),
    }
    (out.parent / "sondaggi_intenzioni_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nOutput: {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
