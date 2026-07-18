"""Test dell'OCR dei PDF scansionati.

La logica di fallback e il rendering si verificano con un motore FINTO, cosi' i
test restano veloci: caricare i modelli ONNX di RapidOCR costa secondi e ~80 MB.
Il motore vero e' esercitato da un solo test, saltato se la libreria non c'e'.

Fixture: `programma_scansione_fixture.pdf`, ottenuta rasterizzando
`programma_fixture.pdf` — la stessa cosa che fa una fotocopiatrice. Vedi
tests/fixtures/README.md.
"""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

from src.ocr_pdf import MIN_CARATTERI_PAGINA, ocr_immagine, ocr_pdf, pdf_a_immagini, serve_ocr


REPO_ROOT = Path(__file__).resolve().parents[1]
SCANSIONE = REPO_ROOT / "tests" / "fixtures" / "programma_scansione_fixture.pdf"
NATIVO = REPO_ROOT / "tests" / "fixtures" / "programma_fixture.pdf"

RAPIDOCR_PRESENTE = importlib.util.find_spec("rapidocr_onnxruntime") is not None


class MotoreFinto:
    """Sostituto di RapidOCR: restituisce righe prestabilite senza caricare i modelli."""

    def __init__(self, righe=("Programma elettorale di prova",), esplode=False):
        self.righe = righe
        self.esplode = esplode
        self.chiamate = 0

    def __call__(self, immagine):
        self.chiamate += 1
        if self.esplode:
            raise RuntimeError("motore in errore")
        return [[None, riga, 0.99] for riga in self.righe], None


class ServeOcrTest(unittest.TestCase):
    def test_testo_vuoto_richiede_ocr(self) -> None:
        self.assertTrue(serve_ocr(""))

    def test_solo_spazi_richiede_ocr(self) -> None:
        """pdftotext su una scansione restituisce i fine-pagina: 24 byte di nulla."""
        self.assertTrue(serve_ocr("\n\f\n \f"))

    def test_testo_presente_non_richiede_ocr(self) -> None:
        """L'OCR è un fallback: dove c'è testo vero, quello vince."""
        self.assertFalse(serve_ocr("Programma elettorale di prova"))


class RenderingTest(unittest.TestCase):
    def test_una_immagine_per_pagina(self) -> None:
        immagini = pdf_a_immagini(SCANSIONE.read_bytes(), dpi=72)
        self.assertEqual(len(immagini), 1)

    def test_immagine_non_vuota(self) -> None:
        immagine = pdf_a_immagini(SCANSIONE.read_bytes(), dpi=72)[0]
        altezza, larghezza = immagine.shape[:2]
        self.assertGreater(altezza, 100)
        self.assertGreater(larghezza, 100)

    def test_dpi_piu_alto_immagine_piu_grande(self) -> None:
        bassa = pdf_a_immagini(SCANSIONE.read_bytes(), dpi=72)[0]
        alta = pdf_a_immagini(SCANSIONE.read_bytes(), dpi=150)[0]
        self.assertGreater(alta.shape[0], bassa.shape[0])

    def test_max_pagine_limita_il_lavoro(self) -> None:
        self.assertEqual(len(pdf_a_immagini(SCANSIONE.read_bytes(), dpi=72, max_pagine=0)), 0)


class OcrConMotoreFintoTest(unittest.TestCase):
    def test_usa_il_motore_su_ogni_pagina(self) -> None:
        motore = MotoreFinto()
        testo = ocr_pdf(SCANSIONE.read_bytes(), dpi=72, motore=motore)
        self.assertEqual(motore.chiamate, 1)
        self.assertIn("Programma elettorale di prova", testo)

    def test_una_pagina_in_errore_non_ferma_il_documento(self) -> None:
        """Meglio un programma con un buco che nessun programma."""
        motore = MotoreFinto(esplode=True)
        self.assertEqual(ocr_pdf(SCANSIONE.read_bytes(), dpi=72, motore=motore), "")

    def test_pagine_quasi_vuote_scartate(self) -> None:
        """Una pagina con solo un logo non è un fallimento: non è testo."""
        motore = MotoreFinto(righe=("x",))
        self.assertEqual(ocr_pdf(SCANSIONE.read_bytes(), dpi=72, motore=motore), "")

    def test_soglia_di_pagina_documentata(self) -> None:
        self.assertGreater(MIN_CARATTERI_PAGINA, 0)

    def test_ocr_immagine_unisce_le_righe(self) -> None:
        motore = MotoreFinto(righe=("prima riga", "seconda riga"))
        immagine = pdf_a_immagini(SCANSIONE.read_bytes(), dpi=72)[0]
        self.assertEqual(ocr_immagine(immagine, motore), "prima riga\nseconda riga")


@unittest.skipUnless(RAPIDOCR_PRESENTE, "rapidocr-onnxruntime non installato")
class MotoreRealeTest(unittest.TestCase):
    """Un solo test con il motore vero: lento, ma è l'unico che dimostra che
    l'OCR legge davvero una scansione."""

    def test_legge_la_scansione_sintetica(self) -> None:
        testo = ocr_pdf(SCANSIONE.read_bytes(), dpi=200)
        self.assertIn("rogramma", testo)   # l'OCR può sbagliare la maiuscola iniziale


if __name__ == "__main__":
    unittest.main()
