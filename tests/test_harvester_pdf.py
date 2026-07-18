"""Test del ramo PDF di harvester.

harvester.py e' condiviso con la pipeline del layer 3 (stampa), gia' in
produzione: meta' di questi test servono a dimostrare che il ramo PDF e'
ADDITIVO, cioe' che sull'HTML non cambia nulla.

La fixture `programma_fixture.pdf` e' un PDF minimo valido costruito a mano
(nessuna dipendenza del progetto genera PDF con testo). Vedi
tests/fixtures/README.md per rigenerarla.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
# harvester.py usa import piatti (`from harvester import ...` in
# mediacloud_fulltext.py), quindi src/ deve stare nel path.
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

import harvester

FIXTURE_PDF = REPO_ROOT / "tests" / "fixtures" / "programma_fixture.pdf"

HTML = """
<html><head><title>Titolo di prova</title></head><body>
<nav>Menu che non deve finire nel testo</nav>
<p>Primo paragrafo dell'articolo, abbastanza lungo da essere estratto senza problemi.</p>
<p>Secondo paragrafo con altro contenuto testuale di lunghezza ragionevole.</p>
</body></html>
"""


class RilevamentoPdfTest(unittest.TestCase):
    def test_riconosce_il_pdf_dai_byte(self) -> None:
        """Il magic number, non l'estensione: un URL può servire un PDF senza
        dirlo nel path."""
        self.assertTrue(harvester.is_pdf(FIXTURE_PDF.read_bytes(), ""))

    def test_riconosce_il_pdf_dal_content_type(self) -> None:
        self.assertTrue(harvester.is_pdf(b"", "application/pdf"))

    def test_html_non_e_un_pdf(self) -> None:
        self.assertFalse(harvester.is_pdf(HTML.encode("utf-8"), "text/html"))

    def test_contenuto_vuoto_non_e_un_pdf(self) -> None:
        self.assertFalse(harvester.is_pdf(b"", "text/html"))


class EstrazionePdfTest(unittest.TestCase):
    def test_estrae_il_testo(self) -> None:
        testo = harvester.extract_pdf_text(FIXTURE_PDF.read_bytes())
        self.assertIn("Programma elettorale di prova", testo)
        self.assertIn("liste di attesa", testo)

    def test_pdf_corrotto_non_solleva(self) -> None:
        """Un PDF malformato deve dare stringa vuota, non far cadere il run:
        scrape_one scarta i record senza testo."""
        self.assertEqual(harvester.extract_pdf_text(b"%PDF-1.4 spazzatura"), "")


class ParsePdfTest(unittest.TestCase):
    def test_parse_pdf_produce_i_campi_di_sempre(self) -> None:
        """Lo schema deve restare quello del layer 3: url/domain/seendate/
        title/text/chars."""
        meta = {
            "url": "https://dait.interno.gov.it/x/programma.pdf",
            "domain": "dait.interno.gov.it",
            "seendate": "2022-09-25T00:00:00",
            "title": "LISTA DI PROVA",
        }
        record = harvester.parse_pdf(FIXTURE_PDF.read_bytes(), meta)
        self.assertEqual(record["url"], meta["url"])
        self.assertEqual(record["domain"], "dait.interno.gov.it")
        self.assertEqual(record["seendate"], "2022-09-25T00:00:00")
        self.assertIn("Programma elettorale", record["text"])
        self.assertEqual(record["chars"], len(record["text"]))

    def test_titolo_dai_metadata_quando_il_pdf_non_lo_ha(self) -> None:
        meta = {"url": "u", "domain": "d", "seendate": "s", "title": "LISTA DI PROVA"}
        record = harvester.parse_pdf(FIXTURE_PDF.read_bytes(), meta)
        self.assertEqual(record["title"], "LISTA DI PROVA")

    def test_meta_description_assente_nei_pdf(self) -> None:
        """Il campo resta nello schema, a None: un PDF non ha meta description."""
        meta = {"url": "u", "domain": "d", "seendate": "s", "title": "t"}
        record = harvester.parse_pdf(FIXTURE_PDF.read_bytes(), meta)
        self.assertIn("meta_description", record)
        self.assertIsNone(record["meta_description"])


class NonRegressioneHtmlTest(unittest.TestCase):
    """harvester serve la pipeline del layer 3 già in produzione: il ramo PDF
    non deve cambiarne il comportamento."""

    def test_parse_html_invariato(self) -> None:
        meta = {"url": "https://x.it/a", "domain": "x.it", "seendate": "2026-01-01", "title": "M"}
        record = harvester.parse(HTML, meta)
        self.assertEqual(record["title"], "Titolo di prova")
        self.assertIn("Primo paragrafo", record["text"])
        self.assertEqual(record["chars"], len(record["text"]))

    def test_parse_html_accetta_ancora_una_stringa(self) -> None:
        """La firma storica parse(html: str, meta) non cambia: mediacloud_fulltext
        la usa attraverso scrape_metas."""
        meta = {"url": "u", "domain": "d", "seendate": "s", "title": "t"}
        self.assertIsInstance(harvester.parse(HTML, meta), dict)

    def test_schema_identico_fra_html_e_pdf(self) -> None:
        meta = {"url": "u", "domain": "d", "seendate": "s", "title": "t"}
        html_record = harvester.parse(HTML, meta)
        pdf_record = harvester.parse_pdf(FIXTURE_PDF.read_bytes(), meta)
        self.assertEqual(sorted(html_record), sorted(pdf_record))


if __name__ == "__main__":
    unittest.main()
