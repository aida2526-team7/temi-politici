"""Test unitari della discovery dei documenti di partito (layer 1).

Tutti i test girano su fixture sintetiche, senza rete.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from src.programmi_discovery import (
    canonical_key,
    cdx_params,
    document_type,
    extract_links,
    host_in_domains,
    is_supported_document,
    normalize_url,
    parse_cdx_rows,
    parse_sitemap,
    sample_monthly,
    score_candidate,
    select_candidates,
    wayback_seendate,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = REPO_ROOT / "tests" / "fixtures"
SITEMAP = FIXTURES / "programmi_sitemap_fixture.xml"
CDX = FIXTURES / "programmi_cdx_fixture.json"

DOMAINS = frozenset({"partito-esempio.it"})


class NormalizzazioneTest(unittest.TestCase):
    def test_normalize_url_rimuove_fragment_e_slash_doppi(self) -> None:
        self.assertEqual(
            normalize_url("https://ESEMPIO.it//programma/#sezione"),
            "https://esempio.it/programma/",
        )

    def test_canonical_key_ignora_schema_e_www(self) -> None:
        """Le copie Wayback sono http://, le pagine correnti https://.

        Se la chiave non le unifica, la stessa pagina risulta due documenti diversi.
        """
        storico = canonical_key("http://www.partito-esempio.it/programma/")
        corrente = canonical_key("https://partito-esempio.it/programma")
        self.assertEqual(storico, corrente)


class DominiTest(unittest.TestCase):
    def test_dominio_esatto_ammesso(self) -> None:
        self.assertTrue(host_in_domains("www.partito-esempio.it", DOMAINS))

    def test_sottodominio_ammesso(self) -> None:
        self.assertTrue(host_in_domains("programma.partito-esempio.it", DOMAINS))

    def test_host_di_test_escluso(self) -> None:
        self.assertFalse(host_in_domains("test.partito-esempio.it", DOMAINS))

    def test_dominio_esterno_escluso(self) -> None:
        self.assertFalse(host_in_domains("altro-sito.it", DOMAINS))

    def test_dominio_che_termina_per_caso_escluso(self) -> None:
        self.assertFalse(host_in_domains("finto-partito-esempio.it", DOMAINS))


class TipoDocumentoTest(unittest.TestCase):
    def test_pagina_programma(self) -> None:
        self.assertEqual(
            document_type("https://www.partito-esempio.it/programma/"), "programma"
        )

    def test_pdf_programma_anche_con_maiuscole(self) -> None:
        self.assertEqual(
            document_type(
                "https://www.partito-esempio.it/wp-content/uploads/2022/08/Programma_Elettorale.pdf"
            ),
            "programma",
        )

    def test_pdf_cronoprogramma_non_e_un_programma(self) -> None:
        """Regressione, e il caso che DISCRIMINA il match con confini di parola.

        Con il match per sottostringa 'Cronoprogramma_Lavori.pdf' diventa un
        programma elettorale. Sostituendo has_word con 'term in normalized'
        questo test deve diventare rosso: e' la prova che serve a qualcosa.
        """
        self.assertEqual(
            document_type(
                "https://www.partito-esempio.it/wp-content/uploads/2024/05/Cronoprogramma_Lavori.pdf"
            ),
            "comunicato",
        )

    def test_cronoprogramma_in_un_comunicato(self) -> None:
        self.assertEqual(
            document_type(
                "https://www.partito-esempio.it/a14-autostrade-definisca-cronoprogramma-e-sospenda-pedaggio/"
            ),
            "comunicato",
        )

    def test_comunicato_senza_termini_programmatici(self) -> None:
        """Il default e' comunicato: il sito di un partito e' comunicazione
        diretta, e un comunicato non dice mai 'programma'."""
        self.assertEqual(
            document_type("https://www.partito-esempio.it/inaugurata-la-nuova-sede-di-ancona/"),
            "comunicato",
        )

    def test_privacy_e_altro(self) -> None:
        self.assertEqual(
            document_type("https://www.partito-esempio.it/privacy-policy/"), "altro"
        )

    def test_tesseramento_e_altro(self) -> None:
        self.assertEqual(
            document_type("https://www.partito-esempio.it/tesseramento/"), "altro"
        )

    def test_homepage_e_altro(self) -> None:
        self.assertEqual(document_type("https://www.partito-esempio.it/"), "altro")

    def test_anchor_text_contribuisce(self) -> None:
        self.assertEqual(
            document_type("https://www.partito-esempio.it/documenti/2022/", "Il nostro programma"),
            "programma",
        )


class EstensioniTest(unittest.TestCase):
    def test_html_ammesso(self) -> None:
        self.assertTrue(is_supported_document("https://x.it/programma/"))

    def test_pdf_ammesso(self) -> None:
        self.assertTrue(is_supported_document("https://x.it/programma.pdf"))

    def test_immagine_esclusa(self) -> None:
        """Regressione: programma-turismo.jpeg veniva scaricato e finiva in
        errori.csv come falso errore."""
        self.assertFalse(
            is_supported_document("https://x.it/wp-content/uploads/programma-turismo.jpeg")
        )


class SelezioneTest(unittest.TestCase):
    def test_selezione_garantisce_i_programmi(self) -> None:
        """Regressione: sorted(candidati)[:40] ordinava alfabeticamente, quindi
        centinaia di comunicati riempivano i posti e /programma/ restava fuori.
        """
        candidati = [
            {
                "url": f"https://www.partito-esempio.it/aaa-comunicato-{i}-elezioni/",
                "tipo_documento": "comunicato",
            }
            for i in range(300)
        ]
        candidati.append(
            {"url": "https://www.partito-esempio.it/programma/", "tipo_documento": "programma"}
        )

        selezionati = select_candidates(candidati, max_programmi=10, max_comunicati=40)
        urls = [c["url"] for c in selezionati]

        self.assertIn("https://www.partito-esempio.it/programma/", urls)
        self.assertEqual(len(urls), 41)

    def test_altro_non_viene_selezionato(self) -> None:
        candidati = [
            {"url": "https://www.partito-esempio.it/privacy-policy/", "tipo_documento": "altro"}
        ]
        self.assertEqual(select_candidates(candidati, max_programmi=10, max_comunicati=40), [])

    def test_budget_rispettati(self) -> None:
        candidati = [
            {"url": f"https://www.partito-esempio.it/programma-{i}/", "tipo_documento": "programma"}
            for i in range(20)
        ]
        selezionati = select_candidates(candidati, max_programmi=5, max_comunicati=0)
        self.assertEqual(len(selezionati), 5)

    def test_programma_batte_comunicato_nel_punteggio(self) -> None:
        programma = score_candidate("https://www.partito-esempio.it/programma/", "")
        comunicato = score_candidate(
            "https://www.partito-esempio.it/oggi-a-san-benedetto-per-chiedere-elezioni-subito/", ""
        )
        self.assertGreater(programma, comunicato)

    def test_comunicati_ordinati_per_lastmod(self) -> None:
        """I più recenti entrano nel budget. Con l'ordine alfabetico entrerebbe
        'aaa-vecchio', che è del 2020."""
        candidati = [
            {
                "url": "https://www.partito-esempio.it/aaa-vecchio/",
                "tipo_documento": "comunicato",
                "lastmod": "2020-01-01",
            },
            {
                "url": "https://www.partito-esempio.it/zzz-recente/",
                "tipo_documento": "comunicato",
                "lastmod": "2026-07-02",
            },
        ]
        selezionati = select_candidates(candidati, max_programmi=0, max_comunicati=1)
        self.assertEqual(
            [c["url"] for c in selezionati], ["https://www.partito-esempio.it/zzz-recente/"]
        )

    def test_comunicati_senza_lastmod_vanno_in_fondo(self) -> None:
        candidati = [
            {"url": "https://www.partito-esempio.it/senza-data/", "tipo_documento": "comunicato"},
            {
                "url": "https://www.partito-esempio.it/con-data/",
                "tipo_documento": "comunicato",
                "lastmod": "2026-07-02",
            },
        ]
        selezionati = select_candidates(candidati, max_programmi=0, max_comunicati=1)
        self.assertEqual(
            [c["url"] for c in selezionati], ["https://www.partito-esempio.it/con-data/"]
        )

    def test_lastmod_non_scavalca_il_budget_dei_programmi(self) -> None:
        """Un programma vecchio entra comunque: ha un budget suo."""
        candidati = [
            {
                "url": "https://www.partito-esempio.it/programma/",
                "tipo_documento": "programma",
                "lastmod": "2022-09-01",
            },
        ] + [
            {
                "url": f"https://www.partito-esempio.it/comunicato-{i}/",
                "tipo_documento": "comunicato",
                "lastmod": "2026-07-01",
            }
            for i in range(100)
        ]
        selezionati = select_candidates(candidati, max_programmi=5, max_comunicati=10)
        urls = [c["url"] for c in selezionati]
        self.assertIn("https://www.partito-esempio.it/programma/", urls)
        self.assertEqual(len(urls), 11)


class SitemapTest(unittest.TestCase):
    def test_parse_sitemap_senza_lxml(self) -> None:
        """La sitemap si legge con la stdlib: lxml non è tra le dipendenze."""
        sitemaps, pagine = parse_sitemap(SITEMAP.read_bytes())
        self.assertEqual(sitemaps, [])
        self.assertIn("https://www.partito-esempio.it/programma/", [p["loc"] for p in pagine])
        self.assertEqual(len(pagine), 14)

    def test_lastmod_letto_dalla_sitemap(self) -> None:
        """Senza lastmod la selezione dei comunicati ricadrebbe sull'ordine
        alfabetico, che è il difetto che stiamo eliminando."""
        _, pagine = parse_sitemap(SITEMAP.read_bytes())
        per_loc = {p["loc"]: p["lastmod"] for p in pagine}
        self.assertEqual(per_loc["https://www.partito-esempio.it/programma/"], "2022-09-01")
        self.assertEqual(
            per_loc["https://www.partito-esempio.it/inaugurata-la-nuova-sede-di-ancona/"],
            "2026-07-02",
        )

    def test_lastmod_assente_non_solleva(self) -> None:
        contenuto = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            b"<url><loc>https://x.it/pagina/</loc></url>"
            b"</urlset>"
        )
        _, pagine = parse_sitemap(contenuto)
        self.assertEqual(pagine, [{"loc": "https://x.it/pagina/", "lastmod": ""}])

    def test_parse_sitemap_index(self) -> None:
        contenuto = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            b"<sitemap><loc>https://x.it/sitemap-1.xml</loc></sitemap>"
            b"</sitemapindex>"
        )
        sitemaps, pagine = parse_sitemap(contenuto)
        self.assertEqual(sitemaps, ["https://x.it/sitemap-1.xml"])
        self.assertEqual(pagine, [])

    def test_sitemap_malformata_non_solleva(self) -> None:
        sitemaps, pagine = parse_sitemap(b"non xml")
        self.assertEqual((sitemaps, pagine), ([], []))


class LinkTest(unittest.TestCase):
    def test_extract_links_restituisce_url_e_anchor(self) -> None:
        html = (
            "<html><body>"
            '<a href="/programma/">Il nostro programma</a>'
            '<a href="https://esterno.it/x">Esterno</a>'
            '<iframe src="/documenti/piano.pdf"></iframe>'
            "</body></html>"
        )
        link = extract_links(html, "https://www.partito-esempio.it/")
        urls = {u for u, _ in link}
        self.assertIn("https://www.partito-esempio.it/programma/", urls)
        self.assertIn("https://www.partito-esempio.it/documenti/piano.pdf", urls)
        self.assertIn("https://esterno.it/x", urls)
        anchor = dict(link)["https://www.partito-esempio.it/programma/"]
        self.assertEqual(anchor, "Il nostro programma")


class WaybackTest(unittest.TestCase):
    def test_seendate_in_iso_come_il_corpus_news(self) -> None:
        self.assertEqual(wayback_seendate("20220128180000"), "2022-01-28T18:00:00")

    def test_una_copia_per_url_e_per_mese(self) -> None:
        catture = parse_cdx_rows(json.loads(CDX.read_text(encoding="utf-8")))
        campione = sample_monthly(catture)
        programma = [
            c for c in campione if canonical_key(c["original"]) == "partito-esempio.it/programma"
        ]
        self.assertEqual(
            [c["timestamp"] for c in programma], ["20220128180000", "20220214090000"]
        )

    def test_parse_cdx_rows_salta_intestazione(self) -> None:
        catture = parse_cdx_rows(json.loads(CDX.read_text(encoding="utf-8")))
        self.assertEqual(len(catture), 6)
        self.assertEqual(catture[0]["timestamp"], "20220105100000")

    def test_parse_cdx_rows_su_risposta_vuota(self) -> None:
        self.assertEqual(parse_cdx_rows([]), [])

    def test_filtro_cdx_e_case_insensitive(self) -> None:
        """Senza (?i) il filtro server perde i PDF chiamati Programma_*.pdf."""
        params = cdx_params("partito-esempio.it", 2020, 2026, 500)
        regex = [f for f in params["filter"] if f.startswith("original:")]
        self.assertEqual(len(regex), 1)
        self.assertIn("(?i)", regex[0])

    def test_cdx_non_usa_wildcard_con_matchtype_domain(self) -> None:
        params = cdx_params("partito-esempio.it", 2020, 2026, 500)
        self.assertEqual(params["matchType"], "domain")
        self.assertEqual(params["url"], "partito-esempio.it")


if __name__ == "__main__":
    unittest.main()
