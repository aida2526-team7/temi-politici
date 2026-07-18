"""Test della discovery dei programmi dal portale Elezioni trasparenti.

Fixture sintetiche che riproducono i due schemi reali del Viminale. Nessuna rete.
"""

from __future__ import annotations

import json
import unittest

from src.viminale_trasparenza import parse_html_index, parse_json_index


CONFIG = {"timeout": 30, "pause": 0.0}

# Mappatura di prova: una lista singola, una coalizione, una non seguita.
MAPPATURA = {
    "politiche2022": {
        "AZIONE - ITALIA VIVA - CALENDA": ["azione", "italia_viva"],
        "LISTA CON FASCICOLO": ["fdi"],
    },
    "politiche2018": {
        "MOVIMENTO ESEMPIO": ["m5s"],
        "LISTA RIPETUTA": ["europa_verde", "sinistra_italiana"],
    },
}

# Schema 2022: e_file con tp_doc. Riproduce il tranello del campo f_progr, che
# nell'originale e' null per tutte le liste.
JSON_INDEX = {
    "metadata": {"elez": "POLITICHE", "dt_elez": "25 09 2022", "dir": "POLITICHE_20220925"},
    "contrass": [
        {
            "n_ord": 7,
            "l_fasc": None,
            "partito": "AZIONE - ITALIA VIVA - CALENDA",
            "f_progr": None,
            "e_file": [
                {"tp_doc": 2, "desc_tp": "Programma elettorale", "f_doc": "(7_progr_2_)-programma.pdf"},
                {"tp_doc": 3, "desc_tp": "Statuto", "f_doc": "(7_stat)-statuto.pdf"},
            ],
        },
        {
            "n_ord": 12,
            "l_fasc": "A",
            "partito": "LISTA CON FASCICOLO",
            "f_progr": None,
            "e_file": [{"tp_doc": 2, "desc_tp": "Programma elettorale", "f_doc": "prog.pdf"}],
        },
        {
            "n_ord": 12,
            "l_fasc": "B",
            "partito": "LISTA CON FASCICOLO",
            "f_progr": None,
            "e_file": [{"tp_doc": 2, "desc_tp": "Programma elettorale", "f_doc": "prog.pdf"}],
        },
        {
            "n_ord": 20,
            "l_fasc": None,
            "partito": "LISTA SENZA PROGRAMMA",
            "f_progr": None,
            "e_file": [{"tp_doc": 6, "desc_tp": "Trasparenza", "f_doc": "(20_tra)-trasp.pdf"}],
        },
    ],
}

# Schema 2018: pagina statica. I nomi file sono inconsistenti (Progr_/Prog_/
# Programma, piu' un refuso "Eelettorale"): l'etichetta del link e' l'unico
# criterio affidabile.
HTML_INDEX = """
<html><body><table>
  <tr>
    <td>MOVIMENTO ESEMPIO</td>
    <td><a href="/documenti/trasparenza/politiche2018/Doc/7/7_Progr_Elettorale.pdf">Programma</a></td>
    <td><a href="/documenti/trasparenza/politiche2018/Doc/7/7_Dich_Trasparenza.pdf">Statuto/Dichiarazione di trasparenza</a></td>
  </tr>
  <tr>
    <td>PARTITO CON REFUSO</td>
    <td><a href="/documenti/trasparenza/politiche2018/Doc/8/8_Progr_Eelettorale.pdf">Programma</a></td>
  </tr>
  <tr>
    <td>PARTITO NOME DIVERSO</td>
    <td><a href="/documenti/trasparenza/politiche2018/Doc/28/28_Programma.pdf">Programma</a></td>
  </tr>
  <tr>
    <td>SOLO STATUTO</td>
    <td><a href="/documenti/trasparenza/politiche2018/Doc/30/30_Dich_Trasparenza.pdf">Statuto/Dichiarazione di trasparenza</a></td>
  </tr>
  <tr>
    <td>LISTA RIPETUTA</td>
    <td><a href="/documenti/trasparenza/politiche2018/Doc/14/14_Progr_Politico.pdf">Programma</a></td>
  </tr>
  <tr>
    <td>LISTA RIPETUTA</td>
    <td><a href="/documenti/trasparenza/politiche2018/Doc/14A/14_Progr_Politico.pdf">Programma</a></td>
  </tr>
  <tr>
    <td>LISTA RIPETUTA</td>
    <td><a href="/documenti/trasparenza/politiche2018/Doc/14B/14_Progr_Politico.pdf">Programma</a></td>
  </tr>
</table></body></html>
"""


class JsonIndexTest(unittest.TestCase):
    def setUp(self) -> None:
        self.records = parse_json_index(JSON_INDEX, "politiche2022", MAPPATURA)

    def test_prende_solo_i_programmi(self) -> None:
        self.assertEqual(len(self.records), 2)
        self.assertTrue(all(r["tipo_documento"] == "programma" for r in self.records))

    def test_url_costruito_senza_fascicolo(self) -> None:
        self.assertEqual(
            self.records[0]["url"],
            "https://dait.interno.gov.it/documenti/trasparenza/POLITICHE_20220925"
            "/Documenti/7/(7_progr_2_)-programma.pdf",
        )

    def test_il_fascicolo_non_entra_nel_path(self) -> None:
        """Verificato sul server: con il fascicolo nel path si prende un 404.
        Il JavaScript del portale sbaglia proprio qui, ed è per questo che la
        riga in originale è commentata."""
        self.assertEqual(
            self.records[1]["url"],
            "https://dait.interno.gov.it/documenti/trasparenza/POLITICHE_20220925"
            "/Documenti/12/prog.pdf",
        )

    def test_fascicoli_multipli_non_duplicano_il_programma(self) -> None:
        """AVS e PD compaiono con più fascicoli (A/B) e lo stesso programma."""
        urls = [r["url"] for r in self.records]
        self.assertEqual(len(urls), len(set(urls)))

    def test_statuti_e_trasparenza_esclusi(self) -> None:
        # Sui nomi file: "trasparenza" compare nel percorso base di ogni URL.
        nomi = [r["url"].split("/")[-1] for r in self.records]
        self.assertFalse([n for n in nomi if "statuto" in n or "trasp" in n])

    def test_seendate_e_la_data_dell_elezione(self) -> None:
        self.assertEqual(self.records[0]["seendate"], "2022-09-25T00:00:00")

    def test_titolo_e_il_nome_della_lista(self) -> None:
        self.assertEqual(self.records[0]["title"], "AZIONE - ITALIA VIVA - CALENDA")

    def test_coalizione_attribuita_a_entrambi_i_partiti(self) -> None:
        """Un programma, due partiti: Azione e Italia Viva si presentarono
        insieme. Emettere due record con lo stesso URL non funzionerebbe, perché
        harvester.scrape_metas deduplica per URL e ne perderebbe uno."""
        self.assertEqual(self.records[0]["partiti"], ["azione", "italia_viva"])
        self.assertTrue(self.records[0]["coalizione"])

    def test_lista_singola_un_solo_partito(self) -> None:
        self.assertEqual(self.records[1]["partiti"], ["fdi"])
        self.assertFalse(self.records[1]["coalizione"])

    def test_lista_non_seguita_resta_senza_attribuzione(self) -> None:
        """Le liste fuori dai partiti seguiti restano nel corpus, ma non entrano
        nei conteggi per partito."""
        record = parse_json_index(
            {"contrass": [{
                "n_ord": 99, "l_fasc": None, "partito": "LISTA SCONOSCIUTA",
                "e_file": [{"tp_doc": 2, "desc_tp": "Programma", "f_doc": "x.pdf"}],
            }]},
            "politiche2022",
            MAPPATURA,
        )[0]
        self.assertEqual(record["partiti"], [])
        self.assertEqual(record["partito_lista"], "LISTA SCONOSCIUTA")

    def test_formati_diversi_da_pdf_scartati(self) -> None:
        """Nel 2022 una lista ha depositato un .doc, che per giunta dà 404."""
        records = parse_json_index(
            {"contrass": [{
                "n_ord": 32, "l_fasc": None, "partito": "PARTITO COMUNISTA DEI LAVORATORI",
                "e_file": [{"tp_doc": 2, "desc_tp": "Programma", "f_doc": "programma.doc"}],
            }]},
            "politiche2022",
            MAPPATURA,
        )
        self.assertEqual(records, [])


class HtmlIndexTest(unittest.TestCase):
    def setUp(self) -> None:
        self.records = parse_html_index(HTML_INDEX, "politiche2018", MAPPATURA)

    def test_prende_i_programmi_per_etichetta_non_per_nome_file(self) -> None:
        """Il criterio è il testo del link. Filtrando per nome file si
        perderebbero le varianti: nell'originale 8 su 37."""
        self.assertEqual(len(self.records), 4)
        nomi = sorted(r["url"].split("/")[-1] for r in self.records)
        self.assertEqual(
            nomi,
            [
                "14_Progr_Politico.pdf",
                "28_Programma.pdf",
                "7_Progr_Elettorale.pdf",
                "8_Progr_Eelettorale.pdf",
            ],
        )

    def test_stesso_programma_in_cartelle_fascicolo_diverse(self) -> None:
        """Nel 2018 il fascicolo è una cartella: Doc/14, Doc/14A, Doc/14B
        contengono lo stesso 14_Progr_Politico.pdf. Gli URL sono distinti, quindi
        deduplicare per URL non basta: ITALIA EUROPA INSIEME entrerebbe 3 volte.
        """
        ripetute = [r for r in self.records if r["partito_lista"] == "LISTA RIPETUTA"]
        self.assertEqual(len(ripetute), 1)

    def test_statuto_escluso(self) -> None:
        urls = " ".join(r["url"] for r in self.records)
        self.assertNotIn("Trasparenza", urls)

    def test_url_assoluto(self) -> None:
        self.assertTrue(all(r["url"].startswith("https://dait.interno.gov.it/") for r in self.records))

    def test_partito_dalla_riga(self) -> None:
        self.assertEqual(self.records[0]["partito_lista"], "MOVIMENTO ESEMPIO")
        self.assertEqual(self.records[1]["partito_lista"], "PARTITO CON REFUSO")

    def test_seendate_2018(self) -> None:
        self.assertEqual(self.records[0]["seendate"], "2018-03-04T00:00:00")


class SchemaComuneTest(unittest.TestCase):
    def test_i_due_schemi_producono_gli_stessi_campi(self) -> None:
        """Il layer 1 deve uscire omogeneo a prescindere dalla consultazione."""
        json_record = parse_json_index(JSON_INDEX, "politiche2022", MAPPATURA)[0]
        html_record = parse_html_index(HTML_INDEX, "politiche2018", MAPPATURA)[0]
        self.assertEqual(sorted(json_record), sorted(html_record))

    def test_campi_attesi_da_harvester(self) -> None:
        record = parse_json_index(JSON_INDEX, "politiche2022", MAPPATURA)[0]
        for campo in ("url", "domain", "seendate", "title"):
            self.assertIn(campo, record)

    def test_coalizione_riconosciuta_anche_nello_schema_2018(self) -> None:
        record = [
            r for r in parse_html_index(HTML_INDEX, "politiche2018", MAPPATURA)
            if r["partito_lista"] == "LISTA RIPETUTA"
        ][0]
        self.assertEqual(record["partiti"], ["europa_verde", "sinistra_italiana"])
        self.assertTrue(record["coalizione"])


if __name__ == "__main__":
    unittest.main()
