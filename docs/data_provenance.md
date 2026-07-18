# Provenienza dei dati

Il progetto raccoglie due layer distinti, che non vanno confusi (vedi `AGENTS.md`
sezione 2):

- **layer 3, "come vengono raccontati"**: articoli di stampa via Media Cloud. È la
  comunicazione partitica *indiretta*, filtrata dalle testate.
- **layer 1, "cosa dicono"**: programmi elettorali depositati dai partiti. È la
  comunicazione *diretta*.

I due corpus condividono lo schema (`url`, `domain`, `seendate`, `title`, `text`,
`chars`, `language`) e il motore di acquisizione (`src/harvester.py`), così che
gli stessi strumenti di misura possano girare su entrambi.

---

# Layer 1 — Programmi elettorali (Elezioni trasparenti)

## Origine

La legge 165/2017 obbliga il Ministero dell'Interno a pubblicare il programma
elettorale depositato da ogni lista che si presenta alle elezioni politiche
(art. 14-bis del DPR 361/1957). Il portale è
`dait.interno.gov.it/elezioni/trasparenza`.

È una fonte migliore dei siti dei partiti: autorevole, completa per definizione,
con data certa, e senza euristiche per capire quale PDF sia il programma.

## Catena dei dati

1. `scripts/run_viminale_discovery.py` legge gli indici delle consultazioni e
   produce `data/raw/programmi_viminale_urls.jsonl` (metadata).
2. `src/programmi_fulltext.py` passa i metadata a `src/harvester.py`, che scarica
   i PDF, ne estrae il testo (`pypdf`) e rileva la lingua; poi riattacca i campi
   del layer 1 e produce `data/raw/programmi_fulltext.jsonl`.
3. I PDF senza testo nativo (scansioni) passano per l'OCR di `src/ocr_pdf.py`
   (PyMuPDF rasterizza, RapidOCR riconosce). Ogni record dichiara nel campo
   `estrazione` se il testo e' `nativa` o `ocr`.

## Scansioni e OCR

Circa tre programmi depositati su quattro sono **scansioni**: fogli fotocopiati e
salvati in PDF (il programma del PD 2022 riporta `/Producer: RICOH Aficio MP
C4502`). Dentro non ci sono caratteri, ci sono immagini di caratteri — verificato
con tre estrattori indipendenti (pypdf, pdftotext, PyMuPDF), tutti a zero.

L'OCR e' un **fallback**: si tenta sempre prima l'estrazione nativa, e solo se
questa da' zero caratteri si rasterizza e si riconosce. I programmi depositati
come PDF veri restano intatti e sono piu' fedeli. La distinzione resta nel campo
`estrazione`: un testo riconosciuto da un'immagine non e' il testo depositato.

L'OCR perde gli accenti (`fragilita` invece di `fragilita'`), ma il topic model
usa `TfidfVectorizer(strip_accents="unicode")`, che li toglie comunque: l'input
che arriva al modello e' identico a quello del testo nativo.

## Schemi delle consultazioni

Le due consultazioni usano formati diversi, ed è la ragione per cui il codice le
tratta separatamente:

| | politiche 2018 | politiche 2022 |
|---|---|---|
| indice | pagina HTML statica | JSON |
| come si riconosce un programma | etichetta del link ("Programma") | campo `tp_doc = 2` |
| fascicolo | **è una cartella** (`Doc/14`, `Doc/14A`) | **non entra nel path** |

Trappole verificate, che non si deducono dalla documentazione:

- nel JSON esiste un campo `f_progr` dal nome invitante: è `null` per tutte le
  liste. I programmi stanno in `e_file`;
- il JavaScript del portale costruisce l'URL col fascicolo nel path e prende 404:
  quella riga nell'originale è infatti commentata;
- i nomi dei file del 2018 sono inconsistenti (`Progr_`, `Prog_`, `Programma`,
  più un refuso `Eelettorale`): filtrare per nome ne trova 8 su 37;
- la stessa lista può depositare lo stesso programma per più circoscrizioni: la
  deduplica è per (lista, nome file), non per URL.

## Attribuzione ai partiti

`config/viminale_liste.json` mappa la lista depositata sui partiti seguiti. **Non
è 1:1** e va validata a mano:

- una coalizione deposita un solo programma per più partiti (AZIONE - ITALIA VIVA
  vale per `azione` e `italia_viva`; ALLEANZA VERDI E SINISTRA per `europa_verde`
  e `sinistra_italiana`). Il documento resta uno, con più attribuzioni: **i
  conteggi per partito non sommano al numero di documenti**, come già nel layer 3
  (`AGENTS.md` sezione 5);
- i nomi cambiano nel tempo: `LEGA NORD` (2018) → `LEGA PER SALVINI PREMIER` (2022);
- le liste fuori dai partiti seguiti restano nel corpus con `partiti: []`.

## Limiti

- Copre le **politiche** (2018 e 2022). Le europee 2019/2024 hanno la sezione
  trasparenza ma **non pubblicano i programmi**: l'obbligo riguarda le politiche.
- Sono fotografie al momento del voto: non catturano come un programma viene
  riformulato fra un'elezione e l'altra.
- Azione e Italia Viva hanno un solo programma (2022): nel 2018 non esistevano.
- I PDF scansiti (~3 su 4) sono recuperati via OCR, marcati `estrazione: ocr`.
  Il testo OCR ha piccoli errori di riconoscimento; per l'analisi tematica sono
  ininfluenti (vedi sopra), ma per una citazione letterale va usato il PDF.
- Solo PDF: nel 2022 una lista ha depositato un `.doc`, che per giunta dà 404.

---

# Layer 3 — Copertura di stampa (Media Cloud)

## Origine

Il corpus deriva da Media Cloud, usato come servizio di discovery degli URL della
stampa. Media Cloud non fornisce il full-text utilizzato dal classificatore.

## Catena dei dati

1. `src/mediacloud_spike.py` interroga la collezione configurata e produce
   `data/raw/mediacloud_urls.jsonl`.
2. `src/mediacloud_fulltext.py` passa gli URL a `src/harvester.py`, che scarica le
   pagine, estrae il testo e rileva la lingua sul corpo dell'articolo.
3. Il driver full-text applica il filtro anti-sport relativo alla query "Lega" e
   produce `data/raw/mediacloud_fulltext.jsonl`.
4. `src/news_topic_model.py` deduplica per URL, mantiene i record con lingua
   italiana, combina `title` e `text`, normalizza il testo e richiede almeno 300
   caratteri prima di applicare TF-IDF + NMF.
5. Il classificatore produce `news_topic_review.csv` e
   `topic_model_metadata.json`, che sono gli input dell'audit.

## Campi principali

Il full-text contiene, quando disponibili:

- `url`, `domain`, `seendate`;
- `title`, `text`, `chars`;
- `language`.

Il CSV di review aggiunge:

- `estratto`;
- un peso `topic_N_peso` per ogni topic;
- `topic_id` dominante;
- `confidenza_topic`;
- `termini_caratteristici`.

## Conteggi

I conteggi del run corrente non sono fissati manualmente in questo documento.
Sono rigenerati da `scripts/run_topic_audit.py` e registrati in:

- `reports/topic_audit/topic_distribution.csv`;
- `reports/topic_audit/run_manifest.json`.

I checkpoint precedenti, come numero di URL e full-text, devono essere verificati
direttamente sui rispettivi JSONL o nei log della pipeline quando necessario.

## File non pubblicati

I JSONL raw, il CSV di review e i metadati generati sono ignorati da Git perché:

- sono rigenerabili;
- possono essere grandi;
- contengono testi acquisiti da fonti editoriali esterne;
- la loro distribuzione richiede valutazioni su copyright e condizioni delle fonti.

Il repository pubblica codice, configurazione relativa, fixture sintetica, test,
documentazione e report di audit previsti dal gruppo.

## Rigenerazione prevista

Layer 3 (stampa):

```bash
python src/mediacloud_spike.py
python src/mediacloud_fulltext.py
python src/news_topic_model.py --n-topics 12
python scripts/run_topic_audit.py --config config/topic_audit.json
```

Layer 1 (programmi):

```bash
python scripts/run_viminale_discovery.py
python src/programmi_fulltext.py
```

Ricognizione delle sitemap dei siti di partito (diagnostica, non produce corpus):

```bash
python scripts/run_layer1_recon.py
```

Le credenziali, i percorsi locali e il mirror Google Drive non devono essere
inseriti nei file versionati.
