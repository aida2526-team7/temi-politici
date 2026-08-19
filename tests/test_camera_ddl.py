"""Test del layer 2 (src/camera_ddl.py).

Nessun test tocca la rete: l'interrogatore SPARQL è iniettabile, così la
paginazione si verifica in millisecondi e la suite gira anche offline.

I casi di pulizia replicano stringhe vere lette dall'endpoint, non inventate:
- 'SCHULLIAN ed altri: "Introduzione dell&rsquo;articolo 413-&lt;em&gt;bis&lt;/em&gt;...'
- '..."Misure a sostegno dei disoccupati..." (1)'
- data '20221013', gruppo 'MISTO (18.10.2022)'.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

import camera_ddl as cd


class PuliziaTitoloTest(unittest.TestCase):
    def test_toglie_le_entita_html(self) -> None:
        titolo = cd.pulisci_titolo(
            'SCHULLIAN ed altri: "Introduzione dell&rsquo;articolo '
            '413-&lt;em&gt;bis&lt;/em&gt; del codice civile, concernente il decesso"')
        self.assertNotIn("&rsquo;", titolo)
        self.assertNotIn("<em>", titolo)
        self.assertIn("413-bis", titolo)

    def test_toglie_il_prefisso_del_proponente(self) -> None:
        """Chi propone sta già in `primo_firmatario`. Lasciato nel testo, i
        cognomi dei deputati più prolifici formerebbero un topic per conto loro."""
        titolo = cd.pulisci_titolo('SCHULLIAN ed altri: "Modifiche al codice della strada"')
        self.assertTrue(titolo.startswith("Modifiche al codice"), titolo)

    def test_toglie_il_numero_ripetuto_in_coda(self) -> None:
        titolo = cd.pulisci_titolo(
            'PROPOSTA DI LEGGE D\'INIZIATIVA POPOLARE: "Misure a sostegno dei '
            'disoccupati e dell\'uscita anticipata dal lavoro" (1)')
        self.assertTrue(titolo.endswith("dal lavoro"), titolo)

    def test_titolo_senza_prefisso_resta_intero(self) -> None:
        originale = "Norme in materia di prevenzione dei danni causati dalla fauna selvatica"
        self.assertEqual(cd.pulisci_titolo(originale), originale)

    def test_prefisso_che_mangerebbe_tutto_non_viene_tolto(self) -> None:
        """Meglio un titolo sporco che un record vuoto."""
        self.assertNotEqual(cd.pulisci_titolo('SCHULLIAN: "Norme"'), "")

    def test_titolo_assente_non_solleva(self) -> None:
        self.assertEqual(cd.pulisci_titolo(None), "")


class NormalizzazioneCampiTest(unittest.TestCase):
    def test_data_compatta_diventa_iso(self) -> None:
        self.assertEqual(cd.normalizza_data("20221013"), "2022-10-13")

    def test_data_gia_iso_resta(self) -> None:
        self.assertEqual(cd.normalizza_data("2022-10-13"), "2022-10-13")

    def test_data_assente_non_solleva(self) -> None:
        self.assertEqual(cd.normalizza_data(None), "")

    def test_gruppo_perde_la_data_di_adesione(self) -> None:
        self.assertEqual(cd.pulisci_gruppo("MISTO (18.10.2022)"), "MISTO")

    def test_gruppo_perde_l_intervallo_di_mandato(self) -> None:
        """Senza, lo stesso partito conta come due gruppi diversi fra la
        legislatura 18 e la 19, e l'aggregazione per partito salta."""
        self.assertEqual(
            cd.pulisci_gruppo("PARTITO DEMOCRATICO (27.03.2018-12.10.2022)"),
            "PARTITO DEMOCRATICO")

    def test_gruppo_senza_data_resta(self) -> None:
        self.assertEqual(cd.pulisci_gruppo("MOVIMENTO 5 STELLE"), "MOVIMENTO 5 STELLE")


class NormalizzaTest(unittest.TestCase):
    def righe(self):
        return [
            {"atto": "http://x/ac19_10", "numero": "10", "titolo": 'TIZIO: "Norme sul lavoro agile"',
             "data": "20221013", "iniziativa": "Parlamentare",
             "firmatario": "MANFRED SCHULLIAN, XIX Legislatura della Repubblica",
             "gruppo": "MISTO (18.10.2022)"},
            # stesso atto, seconda adesione a un gruppo: non è un atto in più
            {"atto": "http://x/ac19_10", "numero": "10", "titolo": 'TIZIO: "Norme sul lavoro agile"',
             "data": "20221013", "iniziativa": "Parlamentare",
             "firmatario": "MANFRED SCHULLIAN, XIX Legislatura della Repubblica",
             "gruppo": "LEGA (01.02.2024)"},
            {"atto": "http://x/ac19_11", "numero": "11", "titolo": "Ratifica di un accordo",
             "data": "20221014", "iniziativa": "Governo"},
        ]

    def test_un_atto_per_riga_ripetuta(self) -> None:
        records = cd.normalizza(self.righe(), 19)
        self.assertEqual(len(records), 2)

    def test_dice_quante_righe_ha_accorpato(self) -> None:
        """Un'aggregazione silenziosa è un dato inventato."""
        records = {r["numero"]: r for r in cd.normalizza(self.righe(), 19)}
        self.assertEqual(records["10"]["righe_accorpate"], 2)
        self.assertEqual(records["11"]["righe_accorpate"], 1)

    def test_schema_condiviso_con_gli_altri_layer(self) -> None:
        record = cd.normalizza(self.righe(), 19)[0]
        for campo in ("url", "domain", "seendate", "title", "text", "chars", "language"):
            self.assertIn(campo, record)

    def test_campi_mancanti_diventano_stringhe_vuote(self) -> None:
        record = [r for r in cd.normalizza(self.righe(), 19) if r["numero"] == "11"][0]
        self.assertEqual(record["gruppo"], "")
        self.assertEqual(record["primo_firmatario"], "")

    def test_il_nome_perde_la_legislatura_appesa(self) -> None:
        record = cd.normalizza(self.righe(), 19)[0]
        self.assertEqual(record["primo_firmatario"], "MANFRED SCHULLIAN")

    def test_chars_coerente_con_il_testo(self) -> None:
        for record in cd.normalizza(self.righe(), 19):
            self.assertEqual(record["chars"], len(record["text"]))


class PaginazioneTest(unittest.TestCase):
    """Virtuoso tronca le risposte lunghe senza segnalarlo, e con OFFSET 10000
    risponde 500 (misurato sull'endpoint vero, legislatura 18). La paginazione
    per chiave è l'unica che regge: va verificata."""

    def finto_endpoint(self, totale, pagina):
        """Endpoint finto che rispetta il FILTER (STR(?atto) > "...").

        Gli URI sono zero-padded perché il confronto è fra stringhe: "a10" < "a9"
        in ordine lessicografico, e una chiave non monotona spezzerebbe la
        paginazione.
        """
        chiamate = []

        def interrogatore(query, endpoint):
            chiamate.append(query)
            dopo = query.split('STR(?atto) > "')[1].split('"')[0]
            uri = [f"http://x/a{i:06d}" for i in range(totale)]
            restanti = [u for u in uri if u > dopo][:pagina]
            return [{"atto": u, "titolo": f"Titolo del progetto di legge {u[-6:]}"}
                    for u in restanti]

        return interrogatore, chiamate

    def test_scorre_tutte_le_pagine(self) -> None:
        interrogatore, chiamate = self.finto_endpoint(totale=2500, pagina=1000)
        righe = cd.scarica_legislatura(19, pagina=1000, verbose=False,
                                       interrogatore=interrogatore)
        self.assertEqual(len(righe), 2500)
        self.assertEqual(len(chiamate), 3)

    def test_nessuna_riga_ripetuta(self) -> None:
        interrogatore, _ = self.finto_endpoint(totale=2500, pagina=1000)
        righe = cd.scarica_legislatura(19, pagina=1000, verbose=False,
                                       interrogatore=interrogatore)
        self.assertEqual(len({r["atto"] for r in righe}), 2500)

    def test_si_ferma_sull_ultima_pagina_piena(self) -> None:
        """Con un totale multiplo esatto serve una richiesta in più per sapere
        che è finita: se ci si fermasse prima si perderebbero righe."""
        interrogatore, chiamate = self.finto_endpoint(totale=2000, pagina=1000)
        righe = cd.scarica_legislatura(19, pagina=1000, verbose=False,
                                       interrogatore=interrogatore)
        self.assertEqual(len(righe), 2000)
        self.assertEqual(len(chiamate), 3)

    def test_la_query_non_usa_offset(self) -> None:
        """OFFSET profondo = 500 dall'endpoint. Se rientra, la paginazione muore
        di nuovo alla decima pagina."""
        self.assertNotIn("OFFSET", cd.QUERY)
        self.assertIn("ORDER BY", cd.QUERY)
        self.assertIn("FILTER", cd.QUERY)

    def test_paginazione_che_non_avanza_solleva(self) -> None:
        """Se una pagina intera contiene un solo atto, il filtro non avanza e si
        girerebbe a vuoto per sempre: meglio un errore."""
        def fermo(query, endpoint):
            return [{"atto": "http://x/a1", "titolo": "t"}] * 10
        with self.assertRaises(RuntimeError):
            cd.scarica_legislatura(19, pagina=10, verbose=False, interrogatore=fermo)

    def test_legislatura_non_prevista_e_un_errore_chiaro(self) -> None:
        with self.assertRaises(ValueError):
            cd.scarica_legislatura(17, interrogatore=lambda q, e: [])


if __name__ == "__main__":
    unittest.main()
