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


def crea_motore():
    """Motore OCR, creato una volta e riusato."""
    global _MOTORE
    if _MOTORE is None:
        from rapidocr_onnxruntime import RapidOCR
        _MOTORE = RapidOCR()
    return _MOTORE


def pdf_a_immagini(content: bytes, dpi: int = DPI_DEFAULT, max_pagine: int | None = None):
    """Pagine del PDF come array numpy, pronte per l'OCR."""
    import fitz
    import numpy as np
    from PIL import Image

    documento = fitz.open(stream=content, filetype="pdf")
    immagini = []
    for numero, pagina in enumerate(documento):
        if max_pagine is not None and numero >= max_pagine:
            break
        pixmap = pagina.get_pixmap(dpi=dpi)
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
            motore=None) -> str:
    """Testo di un PDF scansionato, pagina per pagina.

    `motore` e' iniettabile per i test: cosi' la logica si verifica senza caricare
    gli 80 MB di modelli ONNX.

    Una pagina che fallisce non ferma il documento: meglio un programma con un
    buco che nessun programma.
    """
    motore = motore or crea_motore()
    pagine = []
    for immagine in pdf_a_immagini(content, dpi=dpi, max_pagine=max_pagine):
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
