"""Test dell'ingest Ipsos (salienza dei temi Italia). Nessuna rete."""

from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from src.sondaggi_ipsos import (
    aggiorna_dataset,
    estrai_preoccupazioni,
    mese_rilevazione,
    record,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE = REPO_ROOT / "tests" / "fixtures" / "ipsos_preoccupazioni_fixture.html"


class EstrazioneTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lettura = estrai_preoccupazioni(FIXTURE.read_text(encoding="utf-8"))

    def test_mese_dalla_riga_fonte(self) -> None:
        self.assertEqual(self.lettura["mese"], "2026-06")

    def test_cinque_temi(self) -> None:
        self.assertEqual(len(self.lettura["temi"]), 5)

    def test_valori_corretti(self) -> None:
        per_norm = {t["tema_norm"]: t["valore"] for t in self.lettura["temi"]}
        self.assertEqual(per_norm["criminalita"], 37)
        self.assertEqual(per_norm["sanita"], 35)
        self.assertEqual(per_norm["disoccupazione"], 34)
        self.assertEqual(per_norm["inflazione"], 30)
        self.assertEqual(per_norm["tasse"], 26)

    def test_congiunzione_iniziale_ripulita(self) -> None:
        """'e tasse (26%)' deve dare il tema 'tasse', non 'e tasse'."""
        tasse = [t for t in self.lettura["temi"] if t["tema_norm"] == "tasse"][0]
        self.assertEqual(tasse["tema"], "tasse")

    def test_ignora_percentuali_di_altre_sezioni(self) -> None:
        """Il 62% (direzione del Paese) e il 22% (Iran) non sono temi di salienza:
        stanno fuori dal blocco 'In Italia ... Fonte: What Worries'."""
        valori = {t["valore"] for t in self.lettura["temi"]}
        self.assertNotIn(62, valori)
        self.assertNotIn(22, valori)

    def test_niente_sezione_ritorna_none(self) -> None:
        self.assertIsNone(estrai_preoccupazioni("<p>pagina senza preoccupazioni</p>"))


class MeseTest(unittest.TestCase):
    def test_mese_inglese(self) -> None:
        self.assertEqual(mese_rilevazione("Fonte: What Worries The World, June 2026"), "2026-06")

    def test_mese_italiano(self) -> None:
        self.assertEqual(mese_rilevazione("What Worries the World, dicembre 2025"), "2025-12")

    def test_mese_assente(self) -> None:
        self.assertIsNone(mese_rilevazione("nessuna fonte qui"))


class DatasetTest(unittest.TestCase):
    def _record(self, mese, tema_norm, valore):
        return record(mese, {"tema": tema_norm, "tema_norm": tema_norm, "valore": valore}, "u")

    def test_accumulo_e_dedup(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "sondaggi.csv"
            giugno = [self._record("2026-06", "sanita", 35), self._record("2026-06", "tasse", 26)]

            aggiunti, totale = aggiorna_dataset(giugno, path)
            self.assertEqual((aggiunti, totale), (2, 2))

            # ri-eseguire lo stesso mese non duplica
            aggiunti, totale = aggiorna_dataset(giugno, path)
            self.assertEqual((aggiunti, totale), (0, 2))

            # un mese nuovo si aggiunge
            luglio = [self._record("2026-07", "sanita", 36)]
            aggiunti, totale = aggiorna_dataset(luglio, path)
            self.assertEqual((aggiunti, totale), (1, 3))

    def test_csv_ha_intestazione_e_righe(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "sondaggi.csv"
            aggiorna_dataset([self._record("2026-06", "sanita", 35)], path)
            with path.open(encoding="utf-8-sig", newline="") as handle:
                righe = list(csv.DictReader(handle))
            self.assertEqual(len(righe), 1)
            self.assertEqual(righe[0]["tema_norm"], "sanita")
            self.assertEqual(righe[0]["istituto"], "Ipsos")
            self.assertEqual(righe[0]["paese"], "Italia")


if __name__ == "__main__":
    unittest.main()
