"""Palette e tema condivisi per i grafici della dashboard.

La palette viene da `aicrawl-census`, dove era già passata dal validatore della
skill `dataviz` (separazione per daltonismo, contrasto, banda di luminosità).
Riusarla invece di inventarne una nuova evita di rifare quella validazione, e
tiene i due progetti riconoscibili come lavoro della stessa mano.

Regola che governa tutto il file: **il colore si sceglie per ultimo, e per il
mestiere che deve fare.** Qui i mestieri sono tre.

- *Emphasis*: una serie è il punto, le altre sono contesto. Quella in `ACCENTO`,
  le altre in `GRIGIO_BARRA`. È il caso più frequente in questa pagina.
- *Divergente*: uno scarto con un segno. Due poli e un grigio neutro in mezzo —
  mai una tinta al centro.
- *Categorico*: solo dove i tre layer sono davvero paritari. Ordine fisso, mai
  ciclato.

I testi non prendono mai il colore della serie: restano `INCHIOSTRO` o `MUTO`.
"""

from __future__ import annotations

ACCENTO = "#1a1a19"       # inchiostro di firma: raro, per l'enfasi
CARTA = "#f9f9f7"         # piano della pagina, mai bianco puro
GRIGIO_BARRA = "#cbc9c2"  # le barre di contesto in un grafico a enfasi
GRIGIO = "#b5b3ab"
INCHIOSTRO = "#52514e"    # testo secondario: etichette, valori
MUTO = "#898781"
GRIGLIA = "#e6e4dd"
FONT = "system-ui, -apple-system, 'Segoe UI', sans-serif"

# I tre layer: l'unico posto dove servono davvero tre tinte alla pari.
# Ordine fisso — programmi, leggi, stampa — e mai riassegnato quando un filtro
# cambia il numero di serie.
#
# Le tinte vengono dalla palette categorica di riferimento della skill `dataviz`,
# non dai grigi del census. Il primo tentativo — inchiostro, azzurro, grigio
# chiaro — e' stato **bocciato dal validatore**: fascia di luminosita' fuori,
# croma sotto la soglia (due slot su tre leggevano come grigio) e contrasto 1,61
# contro un minimo di 3. Funzionava come emphasis, non come categorico.
#
#   node scripts/validate_palette.js "#2a78d6,#eb6834,#1baf7a" --mode light
#   → ALL CHECKS PASS, CVD ΔE 9,2 · normale 27,6
#
# Resta un WARN di contrasto sull'acqua (2,74 contro 3): la skill lo dichiara
# sanabile con etichette visibili o una tabella, e ogni grafico qui ha il tabset
# con la sua gemella tabellare.
LAYER_DOMINIO = ["Programmi", "Progetti di legge", "Stampa"]
LAYER_RANGE = ["#2a78d6", "#eb6834", "#1baf7a"]

# Divergente per gli scarti: due poli e un grigio neutro al centro — mai una
# tinta in mezzo. Il verso conta: positivo = promesso piu' di quanto legiferato.
DIV_POSITIVO = "#2a78d6"
DIV_NEGATIVO = "#eb6834"
DIV_NEUTRO = "#cbc9c2"


def tema(chart):
    """Il look condiviso, applicato a un grafico Altair finito.

    Sfondo trasparente: la pagina Quarto ci passa sotto, così il grafico non
    porta un rettangolo bianco dentro una pagina color carta.
    """
    return (
        chart
        .configure(background="transparent")
        .configure_view(stroke=None)
        .configure_axis(
            labelColor=INCHIOSTRO, titleColor=INCHIOSTRO, gridColor=GRIGLIA,
            domainColor=GRIGLIA, tickColor=GRIGLIA, labelFont=FONT, titleFont=FONT,
            labelFontSize=13, titleFontSize=13)
        .configure_legend(
            labelColor=INCHIOSTRO, titleColor=INCHIOSTRO, labelFont=FONT,
            titleFont=FONT, labelFontSize=13, titleFontSize=13, orient="top",
            title=None, symbolSize=140)
        .configure_title(color=INCHIOSTRO, font=FONT, fontSize=15, anchor="start")
    )
