"""Test dei risultati elettorali (src/eligendo_risultati.py).

Nessun test tocca la rete: lo scaricatore è iniettabile.

Le fixture replicano i due schemi veri del catalogo AgID, che per gli stessi
concetti usano nomi diversi:

    politiche 2022   DATAELEZIONE   DESCRLISTA   VOTILISTA   COMUNE
    europee 2024     DATA_ELEZIONE  DESCLISTA    NUMVOTI     DESCCOMUNE
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

import eligendo_risultati as er


CSV_POLITICHE = (
    'DATAELEZIONE;CODTIPOELEZIONE;CIRC-REG;COMUNE;VOTILISTA;DESCRLISTA\n'
    '25/9/2022 00:00:00;C;PIEMONTE 1;TORINO;300;FRATELLI D\'ITALIA\n'
    '25/9/2022 00:00:00;C;PIEMONTE 1;TORINO;200;PARTITO DEMOCRATICO\n'
    '25/9/2022 00:00:00;C;LOMBARDIA 1;MILANO;500;FRATELLI D\'ITALIA\n'
)

CSV_EUROPEE = (
    'DATA_ELEZIONE;DESCREGIONE;DESCCOMUNE;NUMVOTI;DESCLISTA\n'
    '9/6/2024 00:00:00;PIEMONTE;TORINO;120;FRATELLI D\'ITALIA\n'
    '9/6/2024 00:00:00;PIEMONTE;TORINO;80;PARTITO DEMOCRATICO\n'
)


class SchemaTest(unittest.TestCase):
    def test_riconosce_lo_schema_politiche(self) -> None:
        righe = er.leggi_csv(CSV_POLITICHE)
        self.assertEqual(er.rileva_schema(righe[0].keys()), "politiche")

    def test_riconosce_lo_schema_europee(self) -> None:
        righe = er.leggi_csv(CSV_EUROPEE)
        self.assertEqual(er.rileva_schema(righe[0].keys()), "europee")

    def test_schema_ignoto_solleva(self) -> None:
        """Letto con le chiavi sbagliate un file produrrebbe zero voti per ogni
        lista, senza un errore. Meglio fermarsi."""
        with self.assertRaises(ValueError):
            er.rileva_schema(["ANNO", "PARTITO", "PREFERENZE"])


class DataTest(unittest.TestCase):
    def test_formato_viminale_diventa_iso(self) -> None:
        self.assertEqual(er.normalizza_data("25/9/2022 00:00:00"), "2022-09-25")

    def test_mese_e_giorno_a_una_cifra(self) -> None:
        self.assertEqual(er.normalizza_data("9/6/2024 00:00:00"), "2024-06-09")

    def test_valore_assente_non_solleva(self) -> None:
        self.assertEqual(er.normalizza_data(None), "")


class AggregazioneTest(unittest.TestCase):
    def test_somma_i_comuni(self) -> None:
        record, _ = er.aggrega_nazionale(er.leggi_csv(CSV_POLITICHE),
                                         consultazione="camera2022")
        per_lista = {r["lista"]: r["voti"] for r in record}
        self.assertEqual(per_lista["FRATELLI D'ITALIA"], 800)   # 300 Torino + 500 Milano
        self.assertEqual(per_lista["PARTITO DEMOCRATICO"], 200)

    def test_percentuali_sui_voti_di_lista(self) -> None:
        record, _ = er.aggrega_nazionale(er.leggi_csv(CSV_POLITICHE))
        per_lista = {r["lista"]: r["pct"] for r in record}
        self.assertAlmostEqual(per_lista["FRATELLI D'ITALIA"], 80.0)
        self.assertAlmostEqual(per_lista["PARTITO DEMOCRATICO"], 20.0)

    def test_ordina_per_voti_discendenti(self) -> None:
        record, _ = er.aggrega_nazionale(er.leggi_csv(CSV_POLITICHE))
        self.assertEqual([r["voti"] for r in record], sorted((r["voti"] for r in record),
                                                             reverse=True))

    def test_funziona_anche_sullo_schema_europee(self) -> None:
        record, diagnostica = er.aggrega_nazionale(er.leggi_csv(CSV_EUROPEE),
                                                   consultazione="europee2024")
        self.assertEqual(diagnostica["comuni"], 1)
        self.assertEqual(record[0]["data"], "2024-06-09")

    def test_conta_i_comuni_distinti(self) -> None:
        _, diagnostica = er.aggrega_nazionale(er.leggi_csv(CSV_POLITICHE))
        self.assertEqual(diagnostica["comuni"], 2)

    def test_voti_non_numerici_contati_non_nascosti(self) -> None:
        """Se sono tanti, il file non è quello che si crede."""
        sporco = CSV_POLITICHE + '25/9/2022 00:00:00;C;LAZIO 1;ROMA;n.d.;LEGA\n'
        _, diagnostica = er.aggrega_nazionale(er.leggi_csv(sporco))
        self.assertEqual(diagnostica["voti_non_numerici"], 1)

    def test_righe_senza_lista_ignorate(self) -> None:
        sporco = CSV_POLITICHE + '25/9/2022 00:00:00;C;LAZIO 1;ROMA;10;\n'
        record, _ = er.aggrega_nazionale(er.leggi_csv(sporco))
        self.assertNotIn("", [r["lista"] for r in record])

    def test_file_vuoto_non_solleva(self) -> None:
        record, diagnostica = er.aggrega_nazionale([])
        self.assertEqual(record, [])
        self.assertEqual(diagnostica["righe"], 0)


class ScaricaConsultazioneTest(unittest.TestCase):
    def test_usa_lo_schema_dichiarato(self) -> None:
        record, _ = er.scarica_consultazione(
            "camera2022", scaricatore=lambda nome, base: CSV_POLITICHE)
        self.assertEqual(record[0]["consultazione"], "camera2022")
        self.assertEqual(record[0]["lista"], "FRATELLI D'ITALIA")

    def test_consultazione_ignota_e_un_errore_chiaro(self) -> None:
        with self.assertRaises(ValueError):
            er.scarica_consultazione("politiche2018", scaricatore=lambda n, b: "")

    def test_le_politiche_2018_non_sono_previste(self) -> None:
        """Verificato sul catalogo: Camera_Italia_LivComune.csv contiene il 2022.
        Se un giorno il 2018 comparisse, questo test va aggiornato apposta."""
        self.assertNotIn("camera2018", er.CONSULTAZIONI)


if __name__ == "__main__":
    unittest.main()
