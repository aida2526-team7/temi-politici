"""Test dell'ingest delle intenzioni di voto (src/sondaggi_intenzioni.py).

I casi replicano su HTML sintetico le tre cose che sul registro vero fanno male:

- le **basi diverse** fra istituti. SWG deposita percentuali che sommano all'81%
  perche' tiene dentro gli indecisi, NOTO al 95%: sono i valori misurati sul
  registro, ed e' la ragione per cui la normalizzazione esiste;
- le **colonne multiple** sulla stessa riga - scenari alternativi, o il confronto
  con la rilevazione precedente - che senza un parser attento fanno leggere il
  numero sbagliato;
- gli **aggregati di coalizione** ("TOTALE CENTRODESTRA"), che se contati insieme
  ai partiti raddoppiano meta' del campo.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

import sondaggi_intenzioni as si


def blocco(righe: list[str]) -> str:
    """L'HTML che il registro serve per una risposta."""
    return ('<p id="ctl00_Contenuto_ucSchedaDomandaReadOnly_Risposta" class="LabelRO">'
            + "<br />".join(righe) + "</p>")


class TestRiconoscimentoPartito(unittest.TestCase):
    def test_riconosce_le_grafie_degli_istituti(self):
        casi = [
            ("FDI", "FdI / Meloni"),
            ("Fratelli d'Italia", "FdI / Meloni"),
            ("PARTITO DEMOCRATICO", "PD / Schlein"),
            ("M5S", "M5S / Conte"),
            ("Movimento 5 Stelle", "M5S / Conte"),
            ("FORZA ITALIA", "Forza Italia / Tajani"),
            ("VERDI-SINISTRA", "AVS / Fratoianni-Bonelli"),
            ("Alleanza Verdi Sinistra", "AVS / Fratoianni-Bonelli"),
            ("CASA RIFORMISTA-ITALIA VIVA", "Italia Viva / Renzi"),
            ("+EUROPA", "+Europa"),
            ("FUTURO NAZIONALE (VANNACCI)", "Futuro Nazionale / Vannacci"),
        ]
        for etichetta, atteso in casi:
            with self.subTest(etichetta=etichetta):
                self.assertEqual(si.riconosci_partito(etichetta), atteso)

    def test_scarta_chi_non_e_un_partito(self):
        for etichetta in ("Non si esprime", "Indecisi", "Astensione", "Scheda bianca",
                          "ALTRI", "TOTALE", "TOTALE CENTRODESTRA", "Non saprei"):
            with self.subTest(etichetta=etichetta):
                self.assertIsNone(si.riconosci_partito(etichetta))


class TestRisposte(unittest.TestCase):
    def test_legge_etichetta_e_valore(self):
        html = blocco(["Fratelli d'Italia 29,5", "Partito Democratico 21,8"])
        self.assertEqual(si.risposte(html),
                         [("Fratelli d'Italia", [29.5]), ("Partito Democratico", [21.8])])

    def test_tiene_tutte_le_colonne_di_una_riga(self):
        """Scenari alternativi: il primo numero e' il caso base, non l'ultimo."""
        html = blocco(["FDI 27,0 29,0", "PD 20,0 20,0"])
        righe = si.risposte(html)
        self.assertEqual(righe[0], ("FDI", [27.0, 29.0]))
        self.assertEqual(si.normalizza_quote(righe)[0]["FdI / Meloni"]["grezzo"], 27.0)
        self.assertEqual(si.normalizza_quote(righe, colonna=1)[0]["FdI / Meloni"]["grezzo"], 29.0)

    def test_il_numero_nel_nome_del_partito_non_diventa_il_valore(self):
        """Regressione: «Movimento 5 Stelle 12,5».

        Tagliando sul primo numero l'etichetta diventava «Movimento» e il valore
        5,0. Non e' un caso di scuola: il M5S spariva da tutte le rilevazioni degli
        istituti che scrivono il nome per esteso invece della sigla, cioe' quasi
        tutte. I valori si prendono da destra.
        """
        righe = si.risposte(blocco(["Movimento 5 Stelle 12,5"]))
        self.assertEqual(righe, [("Movimento 5 Stelle", [12.5])])
        self.assertEqual(si.riconosci_partito(righe[0][0]), "M5S / Conte")

    def test_il_trattino_tiene_il_posto_della_colonna(self):
        """«FUTURO NAZIONALE - 6,0»: assente nel primo scenario, 6,0 nel secondo."""
        righe = si.risposte(blocco(["FUTURO NAZIONALE (VANNACCI) - 6,0"]))
        self.assertEqual(righe[0][1], [None, 6.0])
        self.assertEqual(si.normalizza_quote(righe, colonna=0)[0], {})
        quote, _ = si.normalizza_quote(righe, colonna=1)
        self.assertEqual(quote["Futuro Nazionale / Vannacci"]["grezzo"], 6.0)

    def test_il_simbolo_di_percentuale_staccato_non_rompe_la_riga(self):
        self.assertEqual(si.risposte(blocco(["Forza Italia 9,0 %"])),
                         [("Forza Italia", [9.0])])

    def test_ignora_le_righe_senza_numeri(self):
        html = blocco(["INTENZIONI DI VOTO", "FDI 29,5"])
        self.assertEqual(si.risposte(html), [("FDI", [29.5])])

    def test_senza_blocco_risposta_non_inventa_niente(self):
        self.assertEqual(si.risposte("<p>nessuna risposta qui</p>"), [])


class TestNormalizzazione(unittest.TestCase):
    # Base 81,5%: SWG tiene dentro gli indecisi. Misurato sul registro.
    SWG = [("FDI", [29.0]), ("PD", [21.5]), ("M5S", [12.0]), ("AVS", [6.5]),
           ("LEGA", [8.0]), ("FORZA ITALIA", [9.0]), ("AZIONE", [3.0]),
           ("ITALIA VIVA", [2.5]), ("Non si esprime", [18.5])]

    def test_la_base_esclude_chi_non_e_un_partito(self):
        _, base = si.normalizza_quote(self.SWG)
        self.assertAlmostEqual(base, 91.5, places=1)

    def test_le_quote_normalizzate_sommano_a_cento(self):
        quote, _ = si.normalizza_quote(self.SWG)
        somma = sum(v["normalizzato"] for v in quote.values())
        self.assertAlmostEqual(somma, 100.0, places=6)

    def test_il_grezzo_resta_accanto_al_normalizzato(self):
        quote, _ = si.normalizza_quote(self.SWG)
        self.assertEqual(quote["FdI / Meloni"]["grezzo"], 29.0)
        self.assertGreater(quote["FdI / Meloni"]["normalizzato"], 29.0)

    def test_gli_aggregati_di_coalizione_non_raddoppiano_il_campo(self):
        con_totale = self.SWG + [("TOTALE CENTRODESTRA", [46.0])]
        senza, _ = si.normalizza_quote(self.SWG)
        con, _ = si.normalizza_quote(con_totale)
        self.assertEqual(senza, con)

    def test_una_risposta_senza_partiti_non_produce_quote(self):
        quote, base = si.normalizza_quote([("Non si esprime", [100.0])])
        self.assertEqual(quote, {})
        self.assertEqual(base, 0.0)


class TestSelezioneDomanda(unittest.TestCase):
    """Le tre formule degli istituti vanno riconosciute tutte."""

    RISPOSTE = [("FDI", [29.0]), ("PD", [21.5]), ("M5S", [12.0]), ("LEGA", [8.0])]

    def test_riconosce_le_formule_dei_tre_istituti(self):
        for domanda in (
            "Se domani si dovesse votare per le elezioni politiche, lei quale lista voterebbe?",
            "Se si votasse oggi, per quale lista voterebbe alla Camera dei Deputati?",
            "Se dovesse votare oggi alle elezioni nazionali, a quale dei seguenti "
            "partiti darebbe il suo voto piu' probabilmente?",
        ):
            with self.subTest(domanda=domanda[:40]):
                self.assertTrue(si.e_intenzione_di_voto(domanda, self.RISPOSTE))

    def test_una_domanda_di_gradimento_non_passa(self):
        domanda = "Qual e' il suo livello di gradimento nei confronti del governo?"
        self.assertFalse(si.e_intenzione_di_voto(domanda, self.RISPOSTE))

    def test_il_testo_giusto_con_poche_liste_non_basta(self):
        """Il testo da solo non decide: servono anche i partiti fra le risposte."""
        domanda = "Se si votasse oggi, per quale lista voterebbe?"
        self.assertFalse(si.e_intenzione_di_voto(domanda, [("FDI", [29.0])]))


class TestNormalizzazioneIstituto(unittest.TestCase):
    def test_lo_stesso_istituto_non_si_spacca_in_due_serie(self):
        """"SWG S.p.A." e "SWG s.p.A" sono la stessa SWG.

        Conta: l'effetto istituto e' il confondente principale della serie, e per
        toglierlo bisogna poter raggruppare per istituto.
        """
        self.assertEqual(si.normalizza_istituto("SWG S.p.A."),
                         si.normalizza_istituto("SWG s.p.A"))

    def test_non_accorpa_istituti_diversi(self):
        nomi = {si.normalizza_istituto(n) for n in
                ("NOTO SONDAGGI", "Istituto Piepoli", "Only Numbers", "Ipsos Doxa")}
        self.assertEqual(len(nomi), 4)


class TestStato(unittest.TestCase):
    def test_raccoglie_i_campi_che_il_registro_pretende(self):
        html = ('<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="AAA" />'
                '<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="BBB" />'
                '<input type="hidden" name="_generation" value="1" />')
        valori = si.stato(html)
        self.assertEqual(valori["__VIEWSTATE"], "AAA")
        self.assertEqual(valori["__EVENTVALIDATION"], "BBB")
        # `_generation` non ha id: senza di esso il postback della domanda rimbalza.
        self.assertEqual(valori["_generation"], "1")


if __name__ == "__main__":
    unittest.main()
