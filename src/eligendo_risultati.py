"""Layer 3 del piano — risultati elettorali dal catalogo Eligendo del Viminale.

E' il "chi li sostiene" di docs/politica-3d.md, e finora non esisteva. Serve
all'ipotesi H2 (lo scostamento di coerenza correla con la variazione di
consenso): senza risultati elettorali non c'e' il termine di consenso.

Fonte: i CSV del catalogo AgID pubblicati dal Dipartimento per gli Affari
Interni e Territoriali, sotto
<https://dait.interno.gov.it/daithome/documenti/opendata/catalogoagid/>.
Download diretto, nessuno scraping e nessuna API.

Granularita'
------------
I file sono a livello COMUNALE. Il piano ha deciso la granularita'
**temporale/nazionale** (la comunale serviva al sentiment, declassato), quindi
qui si aggrega a livello nazionale per lista. L'aggregazione avviene su una copia
in memoria: il CSV comunale resta disponibile se la decisione cambia.

Due schemi, non uno
-------------------
Politiche ed europee usano nomi di colonna diversi per gli stessi concetti:

    politiche 2022   DATAELEZIONE   DESCRLISTA   VOTILISTA    COMUNE
    europee 2024     DATA_ELEZIONE  DESCLISTA    NUMVOTI      DESCCOMUNE

Non e' una svista da correggere a mano ogni volta: `SCHEMI` lo dichiara una volta
e `normalizza_righe` lo applica. Un file con uno schema ignoto solleva, invece di
produrre zeri silenziosi.
"""

from __future__ import annotations

import csv
import io
from collections import defaultdict

import requests


BASE = "https://dait.interno.gov.it/daithome/documenti/opendata/catalogoagid/"

HEADERS = {"User-Agent": "temi-politici/1.0 (progetto universitario AIDA, Unimib)"}

# Il campo che porta lo stesso significato, per famiglia di consultazione.
SCHEMI = {
    "politiche": {"data": "DATAELEZIONE", "lista": "DESCRLISTA",
                  "voti": "VOTILISTA", "comune": "COMUNE"},
    "europee": {"data": "DATA_ELEZIONE", "lista": "DESCLISTA",
                "voti": "NUMVOTI", "comune": "DESCCOMUNE"},
}

# Consultazioni della finestra 2018-2026 presenti nel catalogo.
# NOTA: le politiche 2018 NON ci sono (verificato: Camera_Italia_LivComune.csv
# contiene il 2022, non il 2018). Vedi i limiti nel report dello spike.
CONSULTAZIONI = {
    "camera2022": {"file": "camera-2022-Italia-livcomune.csv", "schema": "politiche"},
    "senato2022": {"file": "senato-2022-italia-livcomune.csv", "schema": "politiche"},
    "europee2024": {"file": "europee-2024-italia-livcomune.csv", "schema": "europee"},
}


def scarica(nome_file, base=BASE, timeout=180):
    """Il CSV come testo. utf-8-sig: i file del Viminale hanno il BOM."""
    risposta = requests.get(base + nome_file, headers=HEADERS, timeout=timeout)
    risposta.raise_for_status()
    return risposta.content.decode("utf-8-sig", errors="replace")


def leggi_csv(testo):
    """Righe del CSV. Separatore ';', come pubblicato."""
    return list(csv.DictReader(io.StringIO(testo), delimiter=";"))


def rileva_schema(colonne):
    """Nome dello schema che combacia con queste colonne.

    Solleva se nessuno combacia: un file con uno schema ignoto, letto con le
    chiavi sbagliate, produrrebbe zero voti per ogni lista senza un errore.
    """
    colonne = set(colonne or ())
    for nome, campi in SCHEMI.items():
        if set(campi.values()) <= colonne:
            return nome
    raise ValueError(
        f"Schema non riconosciuto. Colonne trovate: {sorted(colonne)}. "
        f"Schemi noti: { {k: sorted(v.values()) for k, v in SCHEMI.items()} }")


def normalizza_data(valore):
    """'25/9/2022 00:00:00' -> '2022-09-25'."""
    valore = (valore or "").split(" ")[0].strip()
    parti = valore.split("/")
    if len(parti) != 3:
        return valore
    giorno, mese, anno = parti
    return f"{anno}-{int(mese):02d}-{int(giorno):02d}"


def aggrega_nazionale(righe, schema=None, consultazione=""):
    """Righe comunali -> totali nazionali per lista.

    Ritorna (record, diagnostica). Le righe con voti non numerici sono contate a
    parte e non buttate in silenzio: se sono tante, il file non e' quello che si
    crede.
    """
    if not righe:
        return [], {"righe": 0, "comuni": 0, "voti_non_numerici": 0, "liste": 0}

    campi = SCHEMI[schema or rileva_schema(righe[0].keys())]
    voti_per_lista: dict[str, int] = defaultdict(int)
    comuni, date, scarti = set(), set(), 0

    for riga in righe:
        lista = (riga.get(campi["lista"]) or "").strip()
        if not lista:
            continue
        try:
            voti = int((riga.get(campi["voti"]) or "0").strip() or 0)
        except ValueError:
            scarti += 1
            continue
        voti_per_lista[lista] += voti
        comuni.add((riga.get(campi["comune"]) or "").strip())
        date.add(normalizza_data(riga.get(campi["data"])))

    totale = sum(voti_per_lista.values())
    data = sorted(d for d in date if d)
    record = [
        {
            "consultazione": consultazione,
            "data": data[0] if data else "",
            "lista": lista,
            "voti": voti,
            # La percentuale sui voti di lista validi, non sui votanti: le schede
            # bianche e nulle non sono attribuite a nessuna lista.
            "pct": round(100 * voti / totale, 4) if totale else 0.0,
        }
        for lista, voti in sorted(voti_per_lista.items(), key=lambda x: -x[1])
    ]
    diagnostica = {
        "righe": len(righe),
        "comuni": len(comuni),
        "voti_non_numerici": scarti,
        "liste": len(record),
        "voti_totali": totale,
        "date_distinte": data,
    }
    return record, diagnostica


def scarica_consultazione(chiave, base=BASE, scaricatore=scarica):
    """Una consultazione -> (record nazionali, diagnostica).

    `scaricatore` e' iniettabile: i test girano senza rete.
    """
    if chiave not in CONSULTAZIONI:
        raise ValueError(f"Consultazione non prevista: {chiave}. "
                         f"Disponibili: {sorted(CONSULTAZIONI)}")
    voce = CONSULTAZIONI[chiave]
    righe = leggi_csv(scaricatore(voce["file"], base))
    return aggrega_nazionale(righe, schema=voce["schema"], consultazione=chiave)
