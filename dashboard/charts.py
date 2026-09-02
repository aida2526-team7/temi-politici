"""I grafici della dashboard.

Ogni funzione prende un DataFrame già pronto (`build_data.py`) e restituisce un
grafico Altair, o l'HTML di una tabella. Nessun numero si calcola qui che non sia
già nei dati: grafico e tabella devono leggere la stessa riga, altrimenti prima o
poi divergono.

Il colore si sceglie per ultimo e per il mestiere che fa — vedi `theme.py`.
"""

from __future__ import annotations

import altair as alt
import numpy as np
import pandas as pd

import theme as t

LARGHEZZA = 700


def _quota(campo: str, titolo: str, **kwargs) -> alt.X:
    return alt.X(campo, type="quantitative", title=titolo,
                 axis=alt.Axis(format=".0f", labelExpr="datum.value + '%'"), **kwargs)


def tabella_html(df: pd.DataFrame, nome_file: str) -> str:
    """La gemella tabellare di un grafico: stessi numeri, senza bisogno del mouse.

    Non è un ripiego per l'accessibilità, è l'unico modo di leggere un valore
    esatto senza passare da un tooltip — e di scaricarlo.
    """
    csv = df.to_csv(index=False)
    corpo = df.to_html(index=False, border=0, classes="tabella-dati",
                       float_format=lambda v: f"{v:.2f}".replace(".", ","))
    import base64
    b64 = base64.b64encode(csv.encode("utf-8")).decode("ascii")
    return (f'{corpo}<p class="scarica">'
            f'<a download="{nome_file}" href="data:text/csv;base64,{b64}">'
            f'Scarica {nome_file}</a></p>')


# --------------------------------------------------------------------------- #

def quadrante(df: pd.DataFrame, larghezza: int = LARGHEZZA):
    """Attenzione della stampa contro attività legislativa, un punto per macrotema.

    Le mediane tagliano il piano in quattro. I due riquadri fuori diagonale sono
    la domanda del progetto: di cosa si parla senza legiferare, e su cosa si
    legifera senza che se ne parli.

    Colore a *emphasis*: in accento solo i temi che stanno fuori diagonale, che
    sono il contenuto. Gli altri in grigio, come contesto.
    """
    # L'enfasi va sulla DISTANZA dalla diagonale, non sull'appartenenza al
    # quadrante: un punto che cade esattamente sulla mediana finisce in un
    # riquadro per arrotondamento, e non e' quello il contenuto. La distanza
    # invece dice davvero quanto stampa e Parlamento divergono su quel tema.
    df = df.assign(distanza=(df["stampa"] - df["leggi"]).abs())
    df = df.assign(rilievo=df["distanza"] >= 4.0)
    mx = float(df["mediana_stampa"].iloc[0])
    my = float(df["mediana_leggi"].iloc[0])

    base = alt.Chart(df)
    punti = base.mark_circle(size=150, opacity=0.95).encode(
        x=_quota("stampa", "Quota della stampa",
                 scale=alt.Scale(domain=[0, 14.5], nice=False)),
        y=alt.Y("leggi:Q", title="Quota dei progetti di legge",
                axis=alt.Axis(format=".0f", labelExpr="datum.value + '%'"),
                scale=alt.Scale(domain=[0, 10.5], nice=False)),
        color=alt.condition(alt.datum.rilievo, alt.value(t.ACCENTO), alt.value(t.GRIGIO_BARRA)),
        tooltip=[alt.Tooltip("macrotema:N", title="Macrotema"),
                 alt.Tooltip("programmi:Q", title="Programmi %", format=".2f"),
                 alt.Tooltip("leggi:Q", title="Progetti di legge %", format=".2f"),
                 alt.Tooltip("stampa:Q", title="Stampa %", format=".2f"),
                 alt.Tooltip("quadrante:N", title="Quadrante")])

    # Etichette selettive: i due temi in rilievo e i grandi del riquadro in alto a
    # destra. Etichettarli tutti e quindici li fa sovrapporre, e il resto si legge
    # dal tooltip e dalla tabella.
    nominati = df[df["rilievo"] | ((df["stampa"] >= mx) & (df["leggi"] >= my))].copy()

    # Declutter: due etichette vicine si scavalcano. Si scorre da sinistra e chi
    # cade addosso a chi lo precede va sotto invece che sopra. Vega-Lite non
    # sposta le etichette da solo.
    nominati = nominati.sort_values("stampa").reset_index(drop=True)
    scostamenti, precedenti = [], []
    for _, punto in nominati.iterrows():
        collide = any(abs(punto["stampa"] - px) < 2.5 and abs(punto["leggi"] - py) < 0.8
                      for px, py in precedenti)
        scostamenti.append(16 if collide else -10)
        precedenti.append((punto["stampa"], punto["leggi"]))
    nominati["dy"] = scostamenti
    # Vicino al bordo destro l'etichetta esce dal grafico: si ribalta a sinistra.
    nominati["a_destra"] = nominati["stampa"] > 10

    # `dx`/`dy` sono proprieta' del mark, non canali: un livello per combinazione.
    def testo(sotto, a_destra, dy):
        return alt.Chart(sotto).mark_text(
            align="right" if a_destra else "left", dx=-12 if a_destra else 10, dy=dy,
            fontSize=12, font=t.FONT, color=t.INCHIOSTRO).encode(
            x="stampa:Q", y="leggi:Q", text="macrotema:N",
            opacity=alt.condition(alt.datum.rilievo, alt.value(1.0), alt.value(0.7)))

    etichette = alt.layer(*[
        testo(gruppo, bool(destra), int(dy))
        for (destra, dy), gruppo in nominati.groupby(["a_destra", "dy"])])

    divisori = (alt.Chart(pd.DataFrame({"x": [mx]})).mark_rule(
        color=t.GRIGIO, strokeDash=[4, 4]).encode(x="x:Q")
        + alt.Chart(pd.DataFrame({"y": [my]})).mark_rule(
        color=t.GRIGIO, strokeDash=[4, 4]).encode(y="y:Q"))

    # `align` non accetta un campo: due livelli, uno per allineamento.
    def angolo(righe, allineamento):
        return alt.Chart(pd.DataFrame(righe)).mark_text(
            fontSize=11, font=t.FONT, color=t.MUTO, fontStyle="italic",
            align=allineamento).encode(x="x:Q", y="y:Q", text="testo:N")

    caselle = (
        angolo([{"x": 14.2, "y": 10.2, "testo": "se ne parla e si legifera"},
                {"x": 14.2, "y": 0.15, "testo": "se ne parla soltanto"}], "right")
        + angolo([{"x": 0.15, "y": 10.2, "testo": "si legifera in silenzio"},
                  {"x": 0.15, "y": 0.15, "testo": "ai margini"}], "left"))

    return t.tema((divisori + caselle + punti + etichette)
                  .properties(width=larghezza, height=430))


def scarto(df: pd.DataFrame, colonna: str, accenti: list[str], titolo_asse: str,
           larghezza: int = LARGHEZZA - 60):
    """Barre divergenti attorno allo zero, ordinate. Emphasis sui due estremi.

    La forma dice il segno: a destra ciò che si promette più di quanto si faccia,
    a sinistra il contrario. Niente griglia — c'è la linea dello zero e basta.
    """
    dati = df[df["id"].notna()].copy()
    dati["valore"] = dati[colonna]
    dati["rilievo"] = dati["macrotema"].isin(accenti)
    ordine = dati.sort_values("valore", ascending=False)["macrotema"].tolist()
    # Il colore si calcola qui e non con una condizione annidata: Altair non
    # accetta un `condition` dentro un `condition`, e tre casi (positivo in
    # rilievo, negativo in rilievo, contesto) sono tre.
    dati["colore"] = [
        (t.DIV_POSITIVO if valore > 0 else t.DIV_NEGATIVO) if rilievo else t.DIV_NEUTRO
        for valore, rilievo in zip(dati["valore"], dati["rilievo"])]
    # d3-format non conosce la virgola decimale italiana: l'etichetta si compone qui.
    dati["etichetta"] = [f"{v:+.1f} pp".replace(".", ",") for v in dati["valore"]]

    barre = alt.Chart(dati).mark_bar(height=15, cornerRadius=3).encode(
        x=alt.X("valore:Q", title=titolo_asse,
                axis=alt.Axis(grid=False, format="+.0f",
                              labelExpr="datum.value + ' pp'")),
        y=alt.Y("macrotema:N", title=None, sort=ordine,
                axis=alt.Axis(grid=False, domain=False, ticks=False)),
        color=alt.Color("colore:N", scale=None, legend=None),
        tooltip=[alt.Tooltip("macrotema:N", title="Macrotema"),
                 alt.Tooltip("valore:Q", title="Scarto (punti percentuali)", format="+.2f")])

    # `dx` non è un canale: due livelli, uno per verso, con lo scostamento fisso.
    def etichette(sotto, dx, align):
        return alt.Chart(sotto).mark_text(
            fontSize=12, font=t.FONT, color=t.INCHIOSTRO, fontWeight="bold",
            dx=dx, align=align).encode(
            x="valore:Q", y=alt.Y("macrotema:N", sort=ordine), text="etichetta:N")

    rilevanti = dati[dati["rilievo"]]
    valori = (etichette(rilevanti[rilevanti["valore"] > 0], 8, "left")
              + etichette(rilevanti[rilevanti["valore"] <= 0], -8, "right"))

    zero = alt.Chart(pd.DataFrame({"x": [0]})).mark_rule(color=t.INCHIOSTRO, size=1).encode(x="x:Q")
    return t.tema((barre + zero + valori).properties(width=larghezza, height=330))


def politica_su_se_stessa(meta: dict):
    """Tre barre: la quota di ciascun layer che è politica come processo.

    Barre e non griglia di unità: con 0,46% su cento puntini si accenderebbe
    mezzo puntino, e "quasi zero" si legge peggio di quanto si legga una barra
    lunga un pixel accanto a una lunga cento.
    """
    dati = pd.DataFrame([
        {"layer": "Programmi", "quota": meta["politica_non_tematica"]["layer1"]},
        {"layer": "Progetti di legge", "quota": meta["politica_non_tematica"]["layer2"]},
        {"layer": "Stampa", "quota": meta["politica_non_tematica"]["layer3"]},
    ])
    dati["rilievo"] = dati["layer"] == "Stampa"
    dati["etichetta"] = [f"{q:.2f}%".replace(".", ",") for q in dati["quota"]]

    barre = alt.Chart(dati).mark_bar(height=34, cornerRadius=3).encode(
        x=alt.X("quota:Q", title="Quota del corpus", scale=alt.Scale(domain=[0, 12]),
                axis=alt.Axis(grid=False, format=".0f", labelExpr="datum.value + '%'")),
        y=alt.Y("layer:N", title=None, sort=t.LAYER_DOMINIO,
                axis=alt.Axis(grid=False, domain=False, ticks=False)),
        color=alt.condition(alt.datum.rilievo, alt.value(t.ACCENTO), alt.value(t.GRIGIO_BARRA)),
        tooltip=[alt.Tooltip("layer:N", title="Layer"),
                 alt.Tooltip("quota:Q", title="Quota", format=".2f")])
    valori = alt.Chart(dati).mark_text(
        align="left", dx=8, fontSize=13, font=t.FONT, color=t.INCHIOSTRO).encode(
        x="quota:Q", y=alt.Y("layer:N", sort=t.LAYER_DOMINIO), text="etichetta:N")
    return t.tema((barre + valori).properties(width=LARGHEZZA - 120, height=150))


def occorrenze(df: pd.DataFrame, larghezza: int = LARGHEZZA - 180):
    """Accordo umano col lessico, per quante volte il tema vincitore compare.

    Emphasis, non ramp ordinata: il contenuto non e' la salita, e' che la fascia
    piu' numerosa — trenta righe su 78, etichettate da una parola sola — e' anche
    quella su cui gli umani danno ragione al lessico una volta su otto. Quella in
    accento, le altre come contesto.

    Le righe di ciascuna fascia stanno nell'etichetta e non in un secondo canale:
    sono il motivo per cui la prima barra conta, e vanno lette insieme al valore.
    """
    dati = df.copy()
    ordine = dati["fascia"].tolist()
    dati["rilievo"] = dati["fascia"] == ordine[0]
    dati["etichetta"] = [
        f"{q:.0f}%  ·  {int(n)} righe" for q, n in zip(dati["accordo_pct"], dati["righe"])]

    barre = alt.Chart(dati).mark_bar(height=26, cornerRadius=3).encode(
        x=alt.X("accordo_pct:Q", title="Accordo con almeno un revisore",
                scale=alt.Scale(domain=[0, 100]),
                axis=alt.Axis(grid=False, format=".0f", labelExpr="datum.value + '%'")),
        y=alt.Y("fascia:N", title=None, sort=ordine,
                axis=alt.Axis(grid=False, domain=False, ticks=False)),
        color=alt.condition(alt.datum.rilievo, alt.value(t.ACCENTO), alt.value(t.GRIGIO_BARRA)),
        tooltip=[alt.Tooltip("fascia:N", title="Occorrenze del tema vincitore"),
                 alt.Tooltip("righe:Q", title="Righe"),
                 alt.Tooltip("accordo_pct:Q", title="Accordo %", format=".0f")])
    valori = alt.Chart(dati).mark_text(
        align="left", dx=8, fontSize=12, font=t.FONT, color=t.INCHIOSTRO).encode(
        x="accordo_pct:Q", y=alt.Y("fascia:N", sort=ordine), text="etichetta:N")
    return t.tema((barre + valori).properties(width=larghezza, height=190))


def curva_woke(df: pd.DataFrame, larghezza: int = LARGHEZZA):
    """Il volume del frame nel tempo, normalizzato: il corpus cresce ogni mese.

    Contarlo grezzo direbbe una crescita che è in parte solo più articoli.
    """
    dati = df[df["marcatore"] == "woke"].copy()
    linea = alt.Chart(dati).mark_line(
        color=t.GRIGIO, strokeWidth=2, point=alt.OverlayMarkDef(
            color=t.GRIGIO, size=60, filled=True)).encode(
        x=alt.X("mese:N", title=None, axis=alt.Axis(labelAngle=0, grid=False)),
        y=alt.Y("su_mille_articoli:Q", title="Articoli col frame, su mille",
                axis=alt.Axis(grid=True)),
        tooltip=[alt.Tooltip("mese:N", title="Mese"),
                 alt.Tooltip("articoli:Q", title="Articoli"),
                 alt.Tooltip("su_mille_articoli:Q", title="Su mille", format=".2f")])
    picco = dati.nlargest(1, "su_mille_articoli").copy()
    picco["etichetta"] = [f"{int(a)} articoli" for a in picco["articoli"]]
    rilievo = alt.Chart(picco).mark_point(
        color=t.ACCENTO, size=140, filled=True).encode(x="mese:N", y="su_mille_articoli:Q")
    etichetta = alt.Chart(picco).mark_text(
        align="right", dx=-12, dy=-4, fontSize=13, font=t.FONT,
        color=t.ACCENTO, fontWeight="bold").encode(
        x="mese:N", y="su_mille_articoli:Q", text="etichetta:N")
    return t.tema((linea + rilievo + etichetta).properties(width=larghezza, height=260))


def tre_distribuzioni(df: pd.DataFrame, larghezza: int = LARGHEZZA - 40):
    """I 15 macrotemi visti dai tre layer. L'unico grafico davvero categorico."""
    dati = df[df["e_macrotema"]].copy()
    ordine = (dati[dati["layer"] == "Progetti di legge"]
              .sort_values("quota", ascending=False)["macrotema"].tolist())
    grafico = alt.Chart(dati).mark_bar(cornerRadius=2).encode(
        x=_quota("quota", "Quota entro il layer"),
        y=alt.Y("macrotema:N", title=None, sort=ordine,
                axis=alt.Axis(grid=False, domain=False, ticks=False)),
        yOffset=alt.YOffset("layer:N", sort=t.LAYER_DOMINIO,
                            scale=alt.Scale(paddingInner=0.25)),
        color=alt.Color("layer:N", sort=t.LAYER_DOMINIO,
                        scale=alt.Scale(domain=t.LAYER_DOMINIO, range=t.LAYER_RANGE)),
        tooltip=[alt.Tooltip("macrotema:N", title="Macrotema"),
                 alt.Tooltip("layer:N", title="Layer"),
                 alt.Tooltip("quota:Q", title="Quota", format=".2f")])
    return t.tema(grafico.properties(width=larghezza, height=520))


# --------------------------------------------------------------------------- #
# Radar: il profilo tematico di un partito
# --------------------------------------------------------------------------- #

# L'ordine dei temi lungo la circonferenza è arbitrario ma non innocuo: cambia
# la forma della figura, e quindi la lettura. Va scelto una volta e dichiarato.
# Qui i temi sono raggruppati per famiglia — estero e istituzioni, poi sicurezza
# e diritti, poi la persona, poi l'economia — così due partiti vicini per
# famiglia hanno forme vicine.
ORDINE_RADAR = [1, 2, 3, 11, 10, 12, 14, 15, 8, 7, 6, 5, 4, 13, 9]

# Ordine fisso, mai ciclato: il colore segue il partito, non la sua posizione
# in un filtro. Se un partito sparisce dalla selezione, gli altri non cambiano.
# Validata con lo stesso script: ALL CHECKS PASS su quattro slot,
# CVD ΔE 9,1 · normale 22,9.
PARTITI_RANGE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]


def _polari(df: pd.DataFrame, raggio_max: float) -> pd.DataFrame:
    """Dalle quote alle coordinate cartesiane sul cerchio.

    Vega-Lite non ha un mark radar: si calcolano qui x e y e si disegna una
    spezzata. Angolo zero in alto, senso orario.
    """
    import math

    posizione = {tema: i for i, tema in enumerate(ORDINE_RADAR)}
    n = len(ORDINE_RADAR)
    righe = []
    for _, r in df.iterrows():
        i = posizione[int(r["id"])]
        angolo = 2 * math.pi * i / n
        raggio = min(float(r["quota"]), raggio_max) / raggio_max
        righe.append({**r.to_dict(), "ordine": i,
                      "x": raggio * math.sin(angolo), "y": raggio * math.cos(angolo)})
    # Il primo punto va ripetuto in fondo, altrimenti la spezzata resta aperta.
    if righe:
        primo = dict(righe[0])
        primo["ordine"] = n
        righe.append(primo)
    return pd.DataFrame(righe)


def _griglia_radar(raggio_max: float, anelli=(0.25, 0.5, 0.75, 1.0)):
    """Anelli di riferimento, raggi e nomi dei temi attorno al cerchio."""
    import math

    n = len(ORDINE_RADAR)
    cerchi = []
    for anello in anelli:
        for k in range(n + 1):
            a = 2 * math.pi * k / n
            cerchi.append({"anello": anello, "k": k,
                           "x": anello * math.sin(a), "y": anello * math.cos(a)})
    raggi, nomi = [], []
    for i, tema in enumerate(ORDINE_RADAR):
        a = 2 * math.pi * i / n
        raggi += [{"i": i, "x": 0.0, "y": 0.0},
                  {"i": i, "x": math.sin(a), "y": math.cos(a)}]
        nomi.append({"x": 1.16 * math.sin(a), "y": 1.16 * math.cos(a),
                     "nome": MACRO_BREVI.get(tema, str(tema))})
    scala = [{"x": 0.0, "y": a, "testo": f"{a * raggio_max:.0f}%".replace(".", ",")}
             for a in anelli]
    return pd.DataFrame(cerchi), pd.DataFrame(raggi), pd.DataFrame(nomi), pd.DataFrame(scala)


# Nomi corti: quelli per esteso non stanno attorno a un cerchio.
MACRO_BREVI = {
    1: "Estera", 2: "UE", 3: "Istituzioni", 4: "Economia", 5: "Lavoro",
    6: "Welfare", 7: "Sanità", 8: "Istruzione", 9: "Ambiente", 10: "Immigrazione",
    11: "Sicurezza", 12: "Diritti", 13: "Infrastrutture", 14: "Cultura", 15: "Sport",
}


# La scala di questo grafico non si adatta alla selezione: e' la decisione che
# rende onesto un filtro. Se l'asse si ridisegnasse a ogni partito, due profili
# identici direbbero numeri diversi e nessuno se ne accorgerebbe. Il massimo
# copre il valore piu' alto di qualunque partito, cosi' non si taglia niente.
QUOTA_MASSIMA_PARTITI = 45


def profilo_partito(df: pd.DataFrame, iniziale: str):
    """I quindici temi di un partito sui tre layer, col partito scelto a mano.

    Barre e non radar: con la scala fissa — obbligatoria, se la selezione cambia
    — un radar lascerebbe quasi tutti i partiti schiacciati al centro, perche' i
    profili concentrati sono l'eccezione. Le barre non hanno questo problema, e
    si leggono anche di sfuggita.

    Il filtro e' lato client: i dati di tutti i partiti sono gia' nella pagina e
    la tendina ne accende uno. Nessun server, e il file resta uno solo.
    """
    partiti = sorted(df["partito"].dropna().unique().tolist())
    scelta = alt.param(
        name="partito_scelto", value=iniziale,
        bind=alt.binding_select(options=partiti, name="Partito  "))

    # L'ordine dei temi e' fisso, non ordinato per valore: se si riordinasse a
    # ogni partito, il confronto fra due selezioni diventerebbe impossibile.
    ordine = [MACRO_BREVI[i] for i in sorted(MACRO_BREVI)]
    dati = df.assign(tema=df["id"].map(MACRO_BREVI))

    grafico = alt.Chart(dati).transform_filter(
        alt.datum.partito == scelta).mark_bar(cornerRadius=2).encode(
        x=_quota("quota", "Quota dentro l'attività del partito",
                 scale=alt.Scale(domain=[0, QUOTA_MASSIMA_PARTITI], nice=False)),
        y=alt.Y("tema:N", title=None, sort=ordine,
                axis=alt.Axis(grid=False, domain=False, ticks=False)),
        yOffset=alt.YOffset("layer:N", sort=t.LAYER_DOMINIO,
                            scale=alt.Scale(paddingInner=0.25)),
        color=alt.Color("layer:N", sort=t.LAYER_DOMINIO,
                        scale=alt.Scale(domain=t.LAYER_DOMINIO, range=t.LAYER_RANGE)),
        tooltip=[alt.Tooltip("partito:N", title="Partito"),
                 alt.Tooltip("macrotema:N", title="Macrotema"),
                 alt.Tooltip("layer:N", title="Layer"),
                 alt.Tooltip("quota:Q", title="Quota nel partito", format=".2f")])

    return t.tema(grafico.add_params(scelta).properties(width=560, height=470))


def radar(df: pd.DataFrame, partiti: list[str], layer: str,
          raggio_max: float | None = None):
    """Profilo tematico di uno o più partiti, su un layer.

    Il raggio è la quota del tema dentro quel partito. Punti e spezzata, **area
    non riempita**: l'area di un radar cresce col quadrato del raggio, e riempirla
    fa sembrare quattro volte più forte chi è due volte più distante.

    Il colore è codificato, non assegnato a mano, così la legenda esiste: con due
    o più serie l'identità non può stare nel solo colore di una linea muta.
    """
    dati = df[(df["layer"] == layer) & (df["partito"].isin(partiti))]
    if dati.empty:
        raise ValueError(f"nessun dato per {partiti} sul layer {layer}")
    # La scala si adatta ai dati: fissarla a un valore tondo lascia mezzo grafico
    # vuoto e schiaccia le differenze che dovrebbe mostrare.
    if raggio_max is None:
        raggio_max = float(np.ceil(dati["quota"].max() / 2.5) * 2.5)

    cerchi, raggi, nomi, scala = _griglia_radar(raggio_max)
    lim = alt.Scale(domain=[-1.45, 1.45], nice=False)
    vuoto = alt.Axis(labels=False, ticks=False, domain=False, grid=False, title=None)
    scala_colore = alt.Scale(domain=partiti, range=PARTITI_RANGE[:len(partiti)])

    sfondo = alt.Chart(cerchi).mark_line(color=t.GRIGLIA, strokeWidth=1).encode(
        x=alt.X("x:Q", scale=lim, axis=vuoto), y=alt.Y("y:Q", scale=lim, axis=vuoto),
        order="k:Q", detail="anello:N")
    assi = alt.Chart(raggi).mark_line(color=t.GRIGLIA, strokeWidth=1).encode(
        x="x:Q", y="y:Q", detail="i:N")
    etichette = alt.Chart(nomi).mark_text(
        fontSize=11, font=t.FONT, color=t.INCHIOSTRO).encode(
        x="x:Q", y="y:Q", text="nome:N")
    valori = alt.Chart(scala).mark_text(
        fontSize=9, font=t.FONT, color=t.MUTO, align="left", dx=6, dy=-4).encode(
        x="x:Q", y="y:Q", text="testo:N")

    punti = pd.concat([_polari(dati[dati["partito"] == p], raggio_max) for p in partiti
                       if not dati[dati["partito"] == p].empty])
    linee = alt.Chart(punti).mark_line(strokeWidth=2, opacity=0.9).encode(
        x="x:Q", y="y:Q", order="ordine:Q", detail="partito:N",
        color=alt.Color("partito:N", scale=scala_colore, title=None))
    vertici = alt.Chart(punti[punti["ordine"] < len(ORDINE_RADAR)]).mark_point(
        size=45, filled=True).encode(
        x="x:Q", y="y:Q", color=alt.Color("partito:N", scale=scala_colore, title=None),
        tooltip=[alt.Tooltip("partito:N", title="Partito"),
                 alt.Tooltip("macrotema:N", title="Macrotema"),
                 alt.Tooltip("quota:Q", title="Quota nel partito", format=".2f")])

    return t.tema(alt.layer(sfondo, assi, etichette, valori, linee, vertici)
                  .properties(width=520, height=520, title=alt.Title(
                      layer, subtitle="quota del tema dentro l'attivita' del partito",
                      anchor="start", fontSize=15, subtitleFontSize=12,
                      subtitleColor=t.MUTO)))


def radar_layer(df: pd.DataFrame, partito: str, raggio_max: float | None = None):
    """Lo stesso partito sui tre layer: promesso, depositato, raccontato.

    Stessa forma del radar per partito, ma la serie è il layer. È la tesi del
    progetto vista da dentro un partito solo.
    """
    dati = df[df["partito"] == partito].copy()
    layer = [x for x in t.LAYER_DOMINIO if x in set(dati["layer"])]
    if not layer:
        raise ValueError(f"nessun layer per {partito}")
    if raggio_max is None:
        raggio_max = float(np.ceil(dati["quota"].max() / 2.5) * 2.5)

    cerchi, raggi, nomi, scala = _griglia_radar(raggio_max)
    lim = alt.Scale(domain=[-1.45, 1.45], nice=False)
    vuoto = alt.Axis(labels=False, ticks=False, domain=False, grid=False, title=None)
    scala_colore = alt.Scale(domain=layer, range=t.LAYER_RANGE[:len(layer)])

    sfondo = alt.Chart(cerchi).mark_line(color=t.GRIGLIA, strokeWidth=1).encode(
        x=alt.X("x:Q", scale=lim, axis=vuoto), y=alt.Y("y:Q", scale=lim, axis=vuoto),
        order="k:Q", detail="anello:N")
    assi = alt.Chart(raggi).mark_line(color=t.GRIGLIA, strokeWidth=1).encode(
        x="x:Q", y="y:Q", detail="i:N")
    etichette = alt.Chart(nomi).mark_text(
        fontSize=11, font=t.FONT, color=t.INCHIOSTRO).encode(x="x:Q", y="y:Q", text="nome:N")
    valori = alt.Chart(scala).mark_text(
        fontSize=9, font=t.FONT, color=t.MUTO, align="left", dx=6, dy=-4).encode(
        x="x:Q", y="y:Q", text="testo:N")

    punti = pd.concat([_polari(dati[dati["layer"] == x], raggio_max) for x in layer])
    linee = alt.Chart(punti).mark_line(strokeWidth=2, opacity=0.9).encode(
        x="x:Q", y="y:Q", order="ordine:Q", detail="layer:N",
        color=alt.Color("layer:N", scale=scala_colore, sort=layer, title=None))
    vertici = alt.Chart(punti[punti["ordine"] < len(ORDINE_RADAR)]).mark_point(
        size=45, filled=True).encode(
        x="x:Q", y="y:Q", color=alt.Color("layer:N", scale=scala_colore, sort=layer, title=None),
        tooltip=[alt.Tooltip("layer:N", title="Layer"),
                 alt.Tooltip("macrotema:N", title="Macrotema"),
                 alt.Tooltip("quota:Q", title="Quota", format=".2f")])

    return t.tema(alt.layer(sfondo, assi, etichette, valori, linee, vertici)
                  .properties(width=520, height=520, title=alt.Title(
                      partito, subtitle="quota del tema dentro ciascun layer",
                      anchor="start", fontSize=15, subtitleFontSize=12,
                      subtitleColor=t.MUTO)))
