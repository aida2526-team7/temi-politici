"""Test della mappatura sui macrotemi (src/mappa_ontologia.py).

Tre gruppi di casi:

- il lessico assegna il macrotema giusto a testi che lo dichiarano apertamente;
- chi non pesca in nessun lessico esce `non assegnato`, non forzato nel tema piu'
  vicino: la copertura e' la misura di qualita' del metodo, e un'etichetta
  inventata la falserebbe verso l'alto;
- le due esclusioni misurate sul campione stampa restano tolte. Sono i casi in cui
  una formula fissa, moltiplicata dai quasi-duplicati, spostava un topic intero:
  "dopo una lunga malattia" mandava in Sanita' un topic di necrologi, "lavori del"
  mandava in Lavoro e imprese la cronaca parlamentare.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

import mappa_ontologia as mo


class TestTassonomia(unittest.TestCase):
    def test_quindici_macrotemi_con_identificativi_da_uno_a_quindici(self):
        self.assertEqual(sorted(mo.MACROTEMI), list(range(1, 16)))

    def test_ogni_macrotema_ha_un_lessico(self):
        self.assertEqual(sorted(mo.LESSICO), sorted(mo.MACROTEMI))
        for tema, pattern in mo.LESSICO.items():
            self.assertTrue(pattern, f"macrotema {tema} senza pattern")

    def test_ogni_sottotema_ha_un_padre_in_tassonomia(self):
        """La v2.0 promette che un sottotema si riaccorpi sempre al padre."""
        for figlio in mo.SOTTOTEMI:
            padre = int(figlio.split(".")[0])
            self.assertIn(padre, mo.MACROTEMI)

    def test_ogni_sottotema_ha_un_lessico(self):
        self.assertEqual(sorted(mo.LESSICO_SOTTOTEMI), sorted(mo.SOTTOTEMI))


class TestClassificazione(unittest.TestCase):
    CASI = [
        ("Ratifica ed esecuzione del trattato internazionale sulla difesa comune", 1),
        ("Attuazione della direttiva europea in materia di fondi europei", 2),
        ("Modifiche alla legge elettorale e al referendum costituzionale", 3),
        ("Disposizioni sul debito pubblico e sull'evasione fiscale", 4),
        ("Norme sul contratto collettivo e sulle piccole e medie imprese", 5),
        ("Riforma della previdenza e dell'assegno unico", 6),
        ("Riduzione delle liste di attesa nel servizio sanitario", 7),
        ("Diritto allo studio nelle universita' e formazione professionale", 8),
        ("Transizione ecologica e incentivi alle fonti rinnovabili", 9),
        ("Permesso di soggiorno e protezione internazionale", 10),
        ("Modifiche al codice penale in materia di femminicidio", 11),
        ("Disciplina delle unioni civili e del testamento biologico", 12),
        ("Piano per le infrastrutture ferroviarie e la mobilita' urbana", 13),
        ("Finanziamento dei musei e tutela del patrimonio culturale", 14),
        ("Norme sugli impianti sportivi e le societa' dilettantistiche", 15),
    ]

    def test_ogni_macrotema_si_riconosce_dal_proprio_lessico(self):
        for testo, atteso in self.CASI:
            with self.subTest(tema=atteso):
                tema, margine = mo.classifica(testo)
                self.assertEqual(tema, atteso)
                self.assertGreater(margine, 0.0)

    def test_testo_senza_lessico_resta_non_assegnato(self):
        tema, margine = mo.classifica("Il cielo era grigio e la strada in salita.")
        self.assertEqual(tema, mo.NON_ASSEGNATO)
        self.assertEqual(margine, 0.0)

    def test_testo_vuoto_resta_non_assegnato(self):
        self.assertEqual(mo.classifica("")[0], mo.NON_ASSEGNATO)

    def test_margine_pieno_quando_pesca_da_un_lessico_solo(self):
        _, margine = mo.classifica("Riduzione delle liste di attesa negli ospedali")
        self.assertEqual(margine, 1.0)

    def test_margine_ridotto_quando_i_lessici_sono_piu_di_uno(self):
        _, margine = mo.classifica(
            "Cittadinanza agli stranieri e riforma costituzionale del premierato")
        self.assertLess(margine, 1.0)

    def test_gli_accenti_non_cambiano_il_risultato(self):
        self.assertEqual(mo.classifica("sanita' pubblica")[0],
                         mo.classifica("sanità pubblica")[0])


class TestEsclusioni(unittest.TestCase):
    def test_la_formula_del_coccodrillo_non_finisce_in_sanita(self):
        testo = "Il cantante e' morto oggi a 87 anni dopo una lunga malattia."
        self.assertEqual(mo.classifica(testo)[0], mo.NON_ASSEGNATO)

    def test_i_lavori_parlamentari_non_finiscono_in_lavoro_e_imprese(self):
        testo = "Il ministro ha partecipato ai lavori del Consiglio a Roma."
        self.assertNotEqual(mo.classifica(testo)[0], 5)

    def test_il_lavoro_vero_resta_riconosciuto(self):
        testo = "Tutela dei lavoratori e aumento dei salari nei contratti collettivi"
        self.assertEqual(mo.classifica(testo)[0], 5)

    def test_la_malattia_come_tema_resta_riconosciuta(self):
        testo = "Prevenzione e cura delle malattie croniche negli ospedali pubblici"
        self.assertEqual(mo.classifica(testo)[0], 7)


class TestSottotemi(unittest.TestCase):
    """Il sottotema qualifica il padre, non compete con lui (ontologia v2.0)."""

    def test_gli_animali_restano_dentro_ambiente_ed_energia(self):
        testo = "Contrasto al randagismo e tutela della fauna selvatica"
        tema, _ = mo.classifica(testo)
        self.assertEqual(tema, 9)
        self.assertEqual(mo.sottotema(testo, tema), "9.1")

    def test_un_tema_ambientale_senza_animali_non_prende_il_sottotema(self):
        testo = "Incentivi al fotovoltaico e alla decarbonizzazione"
        tema, _ = mo.classifica(testo)
        self.assertEqual(tema, 9)
        self.assertIsNone(mo.sottotema(testo, tema))

    def test_un_macrotema_senza_figli_non_restituisce_sottotemi(self):
        self.assertIsNone(mo.sottotema("Riforma delle pensioni", 6))

    def test_le_categorie_di_servizio_non_hanno_sottotemi(self):
        self.assertIsNone(mo.sottotema("buongiorno", mo.NON_ASSEGNATO))


class TestBoilerplate(unittest.TestCase):
    def test_riconosce_le_formule_editoriali(self):
        self.assertGreater(mo.quota_boilerplate("Riproduzione riservata © Copyright ANSA"), 0)

    def test_un_articolo_normale_non_e_boilerplate(self):
        self.assertEqual(mo.quota_boilerplate("Il ministro ha presentato la manovra."), 0)


class TestDistribuzione(unittest.TestCase):
    def test_conta_ogni_testo_una_volta_sola(self):
        testi = ["liste di attesa negli ospedali", "riforma delle pensioni", "buongiorno"]
        conteggi = mo.distribuzione(testi)
        self.assertEqual(sum(conteggi.values()), len(testi))
        self.assertEqual(conteggi[7], 1)
        self.assertEqual(conteggi[6], 1)
        self.assertEqual(conteggi[mo.NON_ASSEGNATO], 1)

    def test_etichetta_traduce_gli_identificativi_e_lascia_stare_il_resto(self):
        self.assertEqual(mo.etichetta(7), "Sanità")
        self.assertEqual(mo.etichetta(mo.NON_ASSEGNATO), mo.NON_ASSEGNATO)


if __name__ == "__main__":
    unittest.main()
