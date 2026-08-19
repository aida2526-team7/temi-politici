"""Test della pulizia del corpus (src/pulizia_corpus.py).

I casi replicano su dati sintetici i tre difetti misurati sul corpus reale:

- il template di dominio ("in evidenza ...", 45.8% dei documenti adnkronos.com);
- la formula d'agenzia che attraversa i domini ("riproduzione riservata ©
  copyright ansa", 8.2% del corpus);
- i duplicati che la dedup per URL non vede (3.095 URL diversi, stesso testo).

Il test piu' importante e' `test_articolo_normale_resta_intero`: una pulizia che
toglie anche il contenuto e' peggio di nessuna pulizia, e sul campione vero la
perdita mediana di testo e' 0%.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

import pulizia_corpus as pc


TEMPLATE = "in Evidenza Presentato a Roma il Forum delle Citta della Notte"
FORMULA = "Riproduzione riservata © Copyright ANSA"


def articolo(i: int) -> str:
    """Due righe di contenuto, entrambe diverse a ogni documento.

    Ogni riga deve variare: una riga identica in tutti i documenti di un dominio
    E' un template, per la definizione che usa il modulo, e verrebbe tolta a
    ragione.
    """
    return (f"Il presidente del Consiglio ha illustrato in aula la misura {i} "
            f"prevista dalla manovra, sul capitolo fiscale numero {i}.\n"
            f"L'opposizione ha annunciato {i} emendamenti sul cuneo contributivo "
            f"e sulla sanita territoriale, chiedendo tempi certi entro il {i}.")


def corpus(n_dominio=30, dominio="adnkronos.com"):
    """n documenti dello stesso dominio, ognuno articolo + template."""
    return [
        {"url": f"https://{dominio}/a{i}", "domain": dominio, "language": "it",
         "text": f"{articolo(i)}\n{TEMPLATE}", "chars": 0}
        for i in range(n_dominio)
    ]


class RigheTemplateTest(unittest.TestCase):
    def test_riconosce_la_riga_ripetuta_dal_dominio(self) -> None:
        per_dominio, _, _ = pc.righe_template(corpus())
        righe = per_dominio["adnkronos.com"]
        self.assertIn(pc.normalizza_riga(TEMPLATE), righe)

    def test_non_marca_il_contenuto_variabile(self) -> None:
        per_dominio, _, _ = pc.righe_template(corpus())
        righe = per_dominio["adnkronos.com"]
        self.assertNotIn(pc.normalizza_riga(articolo(3).splitlines()[0]), righe)

    def test_dominio_con_pochi_documenti_e_ignorato(self) -> None:
        """Sotto la soglia due articoli che iniziano uguale non sono un template.
        Su corriereirpinia.it (10 documenti) la regola al 30% toglieva titoli veri
        ripresi nella spalla 'piu' letti': per questo il minimo e' 20."""
        per_dominio, _, diag = pc.righe_template(corpus(n_dominio=5))
        self.assertEqual(per_dominio, {})
        self.assertEqual(diag["domini_sotto_soglia"], 1)

    def test_formula_di_agenzia_riconosciuta_fra_domini(self) -> None:
        """La formula sta su tanti domini, ognuno con pochi documenti: la regola
        per dominio non la vedrebbe, quella globale si'.

        Servono almeno MIN_DOC_CORPUS documenti: sotto, la regola globale e'
        spenta di proposito (una quota su poche decine di documenti non e' una
        frequenza)."""
        records = [
            {"url": f"https://t{i % 40}.it/a{i}", "domain": f"t{i % 40}.it",
             "language": "it", "text": f"{articolo(i)}\n{FORMULA}", "chars": 0}
            for i in range(250)
        ]
        _, globali, _ = pc.righe_template(records)
        self.assertIn(pc.normalizza_riga(FORMULA), globali)

    def test_regola_globale_spenta_su_corpus_piccolo(self) -> None:
        """Il guasto che questo previene: con 30 documenti il 2% e' meno di uno,
        quindi ogni riga risulterebbe template e la pulizia svuoterebbe tutto."""
        _, globali, _ = pc.righe_template(corpus(n_dominio=30))
        self.assertEqual(globali, {})

    def test_riga_di_un_solo_dominio_non_e_globale(self) -> None:
        """Cio' che una sola redazione ripete lo prende la regola per dominio,
        con una soglia molto piu' alta. Altrimenti basterebbe un dominio molto
        rappresentato per imporre le sue righe a tutto il corpus."""
        records = [
            {"url": f"https://solo.it/a{i}", "domain": "solo.it", "language": "it",
             "text": f"{articolo(i)}\nfrase ricorrente di una sola testata", "chars": 0}
            for i in range(250)
        ]
        _, globali, _ = pc.righe_template(records)
        self.assertNotIn("frase ricorrente di una sola testata", globali)

    def test_la_riga_conta_una_volta_per_documento(self) -> None:
        """Un menu ripetuto tre volte nella stessa pagina non vale tre documenti."""
        records = corpus(n_dominio=25)
        records[0]["text"] += f"\n{TEMPLATE}\n{TEMPLATE}"
        per_dominio, _, _ = pc.righe_template(records)
        self.assertLessEqual(per_dominio["adnkronos.com"][pc.normalizza_riga(TEMPLATE)], 1.0)


class TogliBoilerplateTest(unittest.TestCase):
    def test_toglie_il_template_e_tiene_l_articolo(self) -> None:
        records = corpus()
        per_dominio, globali, _ = pc.righe_template(records)
        testo, tolte = pc.togli_boilerplate(records[0], per_dominio, globali)
        self.assertNotIn("in Evidenza", testo)
        self.assertIn("manovra", testo)
        self.assertEqual(tolte, 1)

    def test_maiuscole_e_accenti_non_ingannano(self) -> None:
        """Il template di un sito cambia capitalizzazione fra le pagine."""
        records = corpus()
        records[0]["text"] = (articolo(0) + "\n"
                              "IN EVIDENZA PRESENTATO A ROMA IL FORUM DELLE CITTA DELLA NOTTE")
        per_dominio, globali, _ = pc.righe_template(records)
        testo, tolte = pc.togli_boilerplate(records[0], per_dominio, globali)
        self.assertEqual(tolte, 1)


class DedupTest(unittest.TestCase):
    def test_stesso_testo_url_diversi(self) -> None:
        """Il caso di Adnkronos: 3.095 URL, un solo testo."""
        records = [{"url": f"https://x.it/{i}", "domain": "x.it", "text": TEMPLATE}
                   for i in range(10)]
        tenuti, scartati = pc.dedup_testo(records)
        self.assertEqual(len(tenuti), 1)
        self.assertEqual(len(scartati), 9)

    def test_tiene_il_primo_in_ordine(self) -> None:
        records = [{"url": "primo", "text": TEMPLATE}, {"url": "secondo", "text": TEMPLATE}]
        tenuti, _ = pc.dedup_testo(records)
        self.assertEqual(tenuti[0]["url"], "primo")

    def test_testi_diversi_restano(self) -> None:
        records = [{"url": "a", "text": articolo(1)}, {"url": "b", "text": articolo(2)}]
        tenuti, scartati = pc.dedup_testo(records)
        self.assertEqual(len(tenuti), 2)
        self.assertEqual(scartati, [])


class PipelineTest(unittest.TestCase):
    def test_articolo_normale_resta_intero(self) -> None:
        """Il vincolo che conta: la pulizia non deve toccare il contenuto."""
        records = corpus()
        tenuti, _ = pc.pulisci(records, min_chars=50)
        self.assertTrue(tenuti)
        for record in tenuti:
            self.assertIn("manovra", record["text"])
            self.assertIn("cuneo contributivo", record["text"])

    def test_documento_di_solo_template_sparisce(self) -> None:
        records = corpus()
        records.append({"url": "https://adnkronos.com/chrome", "domain": "adnkronos.com",
                        "language": "it", "text": TEMPLATE, "chars": 0})
        tenuti, report = pc.pulisci(records, min_chars=50)
        self.assertNotIn("https://adnkronos.com/chrome", [r["url"] for r in tenuti])
        self.assertGreaterEqual(report["scartati_senza_testo"], 1)

    def test_il_report_dice_cosa_e_stato_tolto(self) -> None:
        """Una pulizia non verificabile e' una cancellazione."""
        _, report = pc.pulisci(corpus(), min_chars=50)
        self.assertIn("template_per_dominio", report)
        self.assertIn("adnkronos.com", report["template_per_dominio"])
        self.assertGreater(report["righe_template_rimosse"], 0)

    def test_chars_riallineato_al_testo_pulito(self) -> None:
        tenuti, _ = pc.pulisci(corpus(), min_chars=50)
        for record in tenuti:
            self.assertEqual(record["chars"], len(record["text"]))


if __name__ == "__main__":
    unittest.main()
