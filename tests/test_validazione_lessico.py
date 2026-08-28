"""Test della preparazione del campione di validazione.

La proprieta' che questi test proteggono e' una sola, e se salta il lavoro dei
revisori non vale niente: **il file che ricevono non deve contenere la risposta**.

Non basta togliere la colonna con l'esito del lessico. Lo strato di campionamento
la rivela ugualmente - una riga presa dallo strato "Sanita'" e' una riga che il
lessico ha messo in Sanita' - e cosi' fa l'ordine, se le righe restano raggruppate
per strato.
"""

from __future__ import annotations

import csv
import importlib.util
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

import mappa_ontologia as mo

_spec = importlib.util.spec_from_file_location(
    "prepara_validazione_lessico", REPO_ROOT / "scripts" / "prepara_validazione_lessico.py")
pvl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pvl)


def finto_corpus(n: int = 400) -> tuple[list[dict], dict]:
    """Articoli sintetici che il lessico sa classificare, piu' alcuni che non sa."""
    temi = ["liste di attesa negli ospedali", "riforma delle pensioni",
            "transizione ecologica e rinnovabili", "contratti collettivi e salari",
            "permesso di soggiorno e rimpatri"]
    righe, per_esito = [], {}
    for i in range(n):
        testo = temi[i % len(temi)] if i % 3 else "buongiorno a tutti quanti"
        esito, _ = mo.classifica(testo)
        etichetta = mo.etichetta(esito)
        righe.append({
            "indice": i, "data": "2026-05-01", "dominio": "esempio.it",
            "titolo": testo, "estratto": testo, "url": f"https://esempio.it/{i}",
            "esito_lessico": etichetta, "marcatori_lessico": "",
        })
        per_esito.setdefault(etichetta, []).append(i)
    return righe, per_esito


class TestCecita(unittest.TestCase):
    def test_il_revisore_non_vede_l_esito_del_lessico(self):
        self.assertNotIn("esito_lessico", pvl.COLONNE_VISIBILI)
        self.assertNotIn("marcatori_lessico", pvl.COLONNE_VISIBILI)

    def test_il_revisore_non_vede_lo_strato(self):
        """Lo strato E' la risposta: "stratificato:Sanita'" dice il tema."""
        self.assertNotIn("strato", pvl.COLONNE_VISIBILI)

    def test_il_file_scritto_contiene_solo_le_colonne_previste(self):
        """Scrive in una cartella temporanea: `scrivi_revisori` punta ai file veri,
        e un test che li sovrascrive cancellerebbe il lavoro dei revisori."""
        import tempfile

        righe, per_esito = finto_corpus()
        campione = pvl.campiona(righe, per_esito, per_tema=2, non_assegnati=5, casuali=5)
        originale = pvl.OUT_REVISORI
        with tempfile.TemporaryDirectory() as cartella:
            pvl.OUT_REVISORI = Path(cartella)
            try:
                for percorso in pvl.scrivi_revisori(campione):
                    with percorso.open(encoding="utf-8-sig") as handle:
                        intestazione = next(csv.reader(handle))
                    self.assertEqual(intestazione,
                                     pvl.COLONNE_VISIBILI + pvl.COLONNE_DA_COMPILARE)
            finally:
                pvl.OUT_REVISORI = originale

    def test_le_righe_non_restano_raggruppate_per_strato(self):
        """Anche senza la colonna, l'ordine rivelerebbe lo strato."""
        righe, per_esito = finto_corpus()
        campione = pvl.campiona(righe, per_esito, per_tema=3, non_assegnati=10, casuali=10)
        strati = [r["strato"] for r in campione]
        blocchi = sum(1 for a, b in zip(strati, strati[1:]) if a != b)
        self.assertGreater(blocchi, len(set(strati)))


class TestComposizione(unittest.TestCase):
    def test_le_tre_parti_ci_sono_tutte(self):
        righe, per_esito = finto_corpus()
        campione = pvl.campiona(righe, per_esito, per_tema=2, non_assegnati=5, casuali=5)
        strati = {r["strato"].split(":")[0] for r in campione}
        self.assertIn("stratificato", strati)
        self.assertIn("non_assegnato", strati)
        self.assertIn("casuale", strati)

    def test_nessun_articolo_compare_due_volte(self):
        righe, per_esito = finto_corpus()
        campione = pvl.campiona(righe, per_esito, per_tema=2, non_assegnati=5, casuali=5)
        indici = [r["indice"] for r in campione]
        self.assertEqual(len(indici), len(set(indici)))

    def test_le_prime_righe_sono_di_calibrazione(self):
        righe, per_esito = finto_corpus()
        campione = pvl.campiona(righe, per_esito, per_tema=2, non_assegnati=5, casuali=5)
        fasi = [r["fase"] for r in campione[:pvl.RIGHE_CALIBRAZIONE]]
        self.assertTrue(all(f == "calibrazione" for f in fasi))
        self.assertEqual(campione[pvl.RIGHE_CALIBRAZIONE]["fase"], "indipendente")

    def test_lo_stesso_seed_da_lo_stesso_campione(self):
        righe, per_esito = finto_corpus()
        a = pvl.campiona(righe, per_esito, 2, 5, 5)
        b = pvl.campiona(righe, per_esito, 2, 5, 5)
        self.assertEqual([r["indice"] for r in a], [r["indice"] for r in b])


class TestIstruzioni(unittest.TestCase):
    def test_le_definizioni_vengono_dall_ontologia(self):
        """Riscriverle nel modulo vorrebbe dire tenerne due copie divergenti."""
        definizioni = pvl.definizioni_dall_ontologia()
        self.assertEqual(sorted(definizioni), sorted(mo.MACROTEMI))
        for numero, testo in definizioni.items():
            self.assertTrue(testo.strip(), f"macrotema {numero} senza definizione")


if __name__ == "__main__":
    unittest.main()
