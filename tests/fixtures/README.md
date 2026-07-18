# Fixture sintetiche

Dati finti che riproducono la forma di quelli veri. Nessuna rete nei test.

| file | riproduce |
|---|---|
| `topic_review_fixture.csv` | output del classificatore NMF |
| `topic_annotation_fixture.csv`, `topic_human_review_fixture.csv` | campioni di annotazione |
| `programmi_sitemap_fixture.xml` | sitemap di un sito di partito, con `lastmod` |
| `programmi_cdx_fixture.json` | risposta dell'indice CDX di Wayback |
| `programma_fixture.pdf` | programma elettorale in PDF, con testo estraibile |
| `programma_scansione_fixture.pdf` | programma scansionato (immagini, zero testo): il caso OCR |

## Rigenerare `programma_fixture.pdf`

PDF minimo valido con testo selezionabile, costruito a mano: nessuna dipendenza
del progetto genera PDF (`pypdf` li legge, non li scrive con testo dentro).
Serve a `tests/test_harvester_pdf.py`.

```python
from pathlib import Path

testo = "Programma elettorale di prova. Sanita pubblica e liste di attesa."
stream = f"BT /F1 12 Tf 72 720 Td ({testo}) Tj ET".encode("latin-1")

objs = [
    b"<</Type/Catalog/Pages 2 0 R>>",
    b"<</Type/Pages/Kids[3 0 R]/Count 1>>",
    b"<</Type/Page/Parent 2 0 R/Resources<</Font<</F1 4 0 R>>>>"
    b"/MediaBox[0 0 612 792]/Contents 5 0 R>>",
    b"<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>",
    b"<</Length %d>>\nstream\n" % len(stream) + stream + b"\nendstream",
]

out = bytearray(b"%PDF-1.4\n")
offsets = []
for i, body in enumerate(objs, 1):
    offsets.append(len(out))
    out += b"%d 0 obj\n" % i + body + b"\nendobj\n"

xref_at = len(out)
out += b"xref\n0 %d\n" % (len(objs) + 1)
out += b"0000000000 65535 f \n"
for off in offsets:
    out += b"%010d 00000 n \n" % off
out += b"trailer\n<</Size %d/Root 1 0 R>>\nstartxref\n%d\n%%%%EOF\n" % (
    len(objs) + 1, xref_at
)

Path("tests/fixtures/programma_fixture.pdf").write_bytes(bytes(out))
```

Verifica: `pypdf` deve leggere 1 pagina e 65 caratteri.

## Rigenerare `programma_scansione_fixture.pdf`

Un programma scansionato sintetico: si rasterizza `programma_fixture.pdf` in
un'immagine JPEG per pagina, come farebbe una fotocopiatrice. Zero testo
estraibile, una immagine incorporata — la forma dei programmi veri del Viminale.
Serve a `tests/test_ocr_pdf.py`. JPEG grigio q60 per stare in ~11 KB.

```python
import fitz, io
from pathlib import Path
from PIL import Image

src = fitz.open("tests/fixtures/programma_fixture.pdf")
out = fitz.open()
for pagina in src:
    pix = pagina.get_pixmap(dpi=100)
    img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("L")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=60, optimize=True)
    nuova = out.new_page(width=pagina.rect.width, height=pagina.rect.height)
    nuova.insert_image(nuova.rect, stream=buf.getvalue())
Path("tests/fixtures/programma_scansione_fixture.pdf").write_bytes(b"")
out.save("tests/fixtures/programma_scansione_fixture.pdf", deflate=True, garbage=4)
```

Verifica: 0 caratteri estraibili, 1 immagine.

