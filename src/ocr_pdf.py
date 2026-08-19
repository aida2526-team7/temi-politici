"""OCR dei PDF scansionati (layer 1).

Il 77% dei programmi depositati al Viminale sono scansioni: fogli fotocopiati e
salvati in PDF (il programma del PD 2022 riporta `/Producer: RICOH Aficio MP
C4502`). Dentro non ci sono lettere, ci sono fotografie di lettere: nessun
estrattore di testo puo' leggerli — verificato con pypdf, pdftotext e PyMuPDF,
tutti e tre a zero caratteri.

Questo modulo li rende leggibili: PyMuPDF rasterizza le pagine, RapidOCR
riconosce i caratteri.

NON e' in harvester.py di proposito: harvester serve anche il layer 3 (stampa) e
li' l'OCR non serve mai. Un articolo di giornale non deve pagare secondi di OCR
per pagina.

Qualita': l'OCR perde gli accenti ("fragilita" invece di "fragilita'"). Non e' un
problema per l'analisi tematica, perche' `news_topic_model.py` usa
`TfidfVectorizer(strip_accents="unicode")`, che li toglie comunque: l'input che
arriva al modello e' identico a quello del testo nativo.
"""

from __future__ import annotations

import io

# Il motore va creato una volta sola: caricare i modelli ONNX costa alcuni
# secondi, e rifarlo per ogni pagina renderebbe l'OCR inutilizzabile.
_MOTORE = None

DPI_DEFAULT = 200          # compromesso qualita'/velocita' verificato sui programmi
MIN_CARATTERI_PAGINA = 20  # sotto: pagina vuota o solo logo, non un fallimento

# Tetto di pixel per pagina rasterizzata.
#
# Il DPI da solo non basta: descrive la densita', non la dimensione. Una pagina
# A4 a 200 DPI fa 3.9 Mpx, ma fra i programmi depositati ce n'e' una da 107 Mpx
# (`1_Prog_Elettorale.pdf`: formato manifesto, o MediaBox sbagliata). Stessa
# richiesta di DPI, ventotto volte il lavoro. Quel documento da solo vale 450
# Mpx e il totale sui 46 scansionati e' 2.260 Mpx: piu' di due ore di OCR, che
# infatti non e' mai arrivato in fondo.
#
# 6 Mpx sta sopra l'A4 a 200 DPI, quindi le pagine normali non vengono toccate.
# Scende solo cio' che e' fuori scala, e una pagina fisicamente enorme ha testo
# grande, che resta leggibile a densita' minore.
MAX_PIXEL_PAGINA = 6_000_000


def crea_motore():
    """Motore OCR, creato una volta e riusato."""
    global _MOTORE
    if _MOTORE is None:
        from rapidocr_onnxruntime import RapidOCR
        _MOTORE = RapidOCR()
    return _MOTORE


def dpi_effettivo(larghezza_pt: float, altezza_pt: float, dpi: int,
                  max_pixel: int = MAX_PIXEL_PAGINA) -> int:
    """DPI da usare per questa pagina, abbassato se sforerebbe il tetto di pixel.

    Le misure di un PDF sono in punti tipografici (1/72 di pollice), quindi i
    pixel a un dato DPI sono `punti * dpi / 72` per lato. Si scala di
    `sqrt(max/effettivi)` perche' il vincolo e' sull'area.
    """
    if larghezza_pt <= 0 or altezza_pt <= 0:
        return dpi
    pixel = (larghezza_pt * dpi / 72) * (altezza_pt * dpi / 72)
    if pixel <= max_pixel:
        return dpi
    return max(36, int(dpi * (max_pixel / pixel) ** 0.5))


def pdf_a_immagini(content: bytes, dpi: int = DPI_DEFAULT, max_pagine: int | None = None,
                   max_pixel: int = MAX_PIXEL_PAGINA):
    """Pagine del PDF come array numpy, pronte per l'OCR.

    Il DPI e' per pagina, non per documento: una pagina fuori scala viene
    rasterizzata piu' bassa invece di far esplodere il lavoro (vedi
    MAX_PIXEL_PAGINA).
    """
    import fitz
    import numpy as np
    from PIL import Image

    documento = fitz.open(stream=content, filetype="pdf")
    immagini = []
    for numero, pagina in enumerate(documento):
        if max_pagine is not None and numero >= max_pagine:
            break
        effettivo = dpi_effettivo(pagina.rect.width, pagina.rect.height, dpi, max_pixel)
        pixmap = pagina.get_pixmap(dpi=effettivo)
        immagini.append(np.array(Image.open(io.BytesIO(pixmap.tobytes("png")))))
    documento.close()
    return immagini


def ocr_immagine(immagine, motore=None) -> str:
    """Testo di una singola pagina rasterizzata."""
    motore = motore or crea_motore()
    risultato, _ = motore(immagine)
    if not risultato:
        return ""
    return "\n".join(riga[1] for riga in risultato)


def ocr_pdf(content: bytes, dpi: int = DPI_DEFAULT, max_pagine: int | None = None,
            motore=None, max_pixel: int = MAX_PIXEL_PAGINA) -> str:
    """Testo di un PDF scansionato, pagina per pagina.

    `motore` e' iniettabile per i test: cosi' la logica si verifica senza caricare
    gli 80 MB di modelli ONNX.

    Una pagina che fallisce non ferma il documento: meglio un programma con un
    buco che nessun programma.
    """
    motore = motore or crea_motore()
    pagine = []
    for immagine in pdf_a_immagini(content, dpi=dpi, max_pagine=max_pagine,
                                   max_pixel=max_pixel):
        try:
            testo = ocr_immagine(immagine, motore)
        except Exception:
            testo = ""
        if len(testo) >= MIN_CARATTERI_PAGINA:
            pagine.append(testo)
    return "\n\n".join(pagine).strip()


def serve_ocr(testo_nativo: str, soglia: int = 1) -> bool:
    """True se l'estrazione normale non ha prodotto nulla.

    L'OCR e' un fallback, non il metodo principale: i PDF con testo vero si
    leggono come sempre, e sono piu' fedeli di qualsiasi riconoscimento.
    """
    return len(testo_nativo.strip()) < soglia
