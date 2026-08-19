# Progetto AIDA sui temi politici

Progetto universitario del Master AIDA @ Unimib.it (A.A. 2025–2026) dedicato
all'analisi data-driven dei temi politici italiani.

## Obiettivo della fase corrente

La fase attuale analizza articoli raccolti tramite query Media Cloud (https://www.mediacloud.org/about-us)
su partiti e leader. Il corpus rappresenta **come la politica viene raccontata dalla stampa**:
non misura automaticamente comunicazione diretta, attività legislativa,
consenso, sentiment verso un partito o stance su una policy.

L'obiettivo è scoprire microtemi con TF-IDF + NMF, controllarne qualità e
boilerplate e prepararne la validazione umana. I macrotemi risultanti saranno
ancora una tassonomia candidata, non un'ontologia definitiva multi-layer.

In parallelo il repository predispone la **raccolta del layer 1** ("cosa dicono"
— la comunicazione diretta dei partiti): i programmi elettorali depositati.
È solo acquisizione: l'analisi tematica resta per ora sul corpus stampa. Lo scopo
è avere i due corpus nello stesso schema, così che gli stessi strumenti di misura
possano girare su entrambi (vedi la sezione *Layer 1* più sotto e
`docs/data_provenance.md`).
Cos'è TF-IF: https://it.wikipedia.org/wiki/Tf-idf
Cos'è NMF: https://share.google/aimode/WrVVpSDpQwY4P6i7H

## Pipeline

1. `src/mediacloud_spike.py` interroga Media Cloud e salva gli URL.
2. `src/mediacloud_fulltext.py` e `src/harvester.py` scaricano il full-text,
   rilevano la lingua e producono la copertura aggregata. Ogni record dichiara
   in `estrazione` con che metodo è stato letto.
3. `src/pulizia_corpus.py` toglie il boilerplate e i duplicati (vedi
   *Pulizia del corpus* più sotto). Lo chiama il classificatore, prima di
   modellare.
4. `src/news_topic_model.py` applica TF-IDF + NMF e genera 12 topic esplorativi.
5. `scripts/run_topic_audit.py` verifica distribuzioni, confidenza, domini,
   duplicati e anomalie degli output NMF.
6. `scripts/run_topic_human_review.py` costruisce un campione deterministico di
   27 record per lo human check.
7. `scripts/prepare_topic_annotation_files.py` prepara due copie indipendenti
   per R1 e R2; `scripts/validate_topic_annotations.py` le valida senza
   modificarle.

### Pulizia del corpus

Il primo giro di TF-IDF + NMF ha prodotto 12 topic di cui 7 erano template di
testate (`in evidenza`, `riproduzione riservata copyright ansa`, `vai all
articolo su raiplay`) e 2 erano parole funzione italiane. Non è un difetto
dell'NMF: quelle stringhe sono il testo più regolare del corpus, quindi anche la
struttura più forte che una fattorizzazione può trovare.

Il boilerplate non si riconosce guardando una pagina alla volta — su
`adnkronos.com/internazionale/japanese/*` il corpo dell'articolo è renderizzato
in JS e trafilatura restituisce la spalla come contenuto legittimo. Si riconosce
guardando il corpus: `src/pulizia_corpus.py` marca come template le righe che
ricorrono in almeno il 30% dei documenti di un dominio, più quelle che superano
il 2% del corpus e stanno su almeno 3 testate diverse. Poi deduplica sull'hash
del testo (non sull'URL: 3.095 URL diversi servivano lo stesso identico testo) e
rilegge la lingua sul testo pulito.

Verificato su 912 articoli reali: la perdita mediana di testo sugli articoli
tenuti è **0%**. Il report di cosa è stato tolto finisce in
`topic_model_metadata.json`.

I notebook richiamano o leggono la logica e gli output salvati nel repository:

- `notebooks/00_esegui_pipeline.ipynb`: orchestrazione didattica della pipeline;
- `notebooks/classificatore.ipynb`: audit, campione e istruzioni di review.

### Layer 1 — Programmi elettorali (acquisizione)

Raccolta della comunicazione diretta dei partiti dal portale *Elezioni
trasparenti* del Viminale (fonte ufficiale ex legge 165/2017), con discovery dai
siti dei partiti come fallback. Discovery separata dall'acquisizione, come nel
layer 3:

1. `scripts/run_viminale_discovery.py` legge gli indici delle consultazioni
   (politiche 2018 e 2022) e salva i metadata dei programmi.
2. `src/programmi_fulltext.py` scarica i PDF via `src/harvester.py`, ne estrae il
   testo e applica l'**OCR** ai documenti scansionati (circa tre su quattro);
   ogni record dichiara in `estrazione` se il testo è `nativa` o `ocr`.
3. `src/programmi_discovery.py` e `scripts/run_programmi_discovery.py` raccolgono
   dai siti dei partiti (sitemap e Wayback) ciò che il portale non copre.

Il corpus esce con lo stesso schema del layer 3 (`url, domain, seendate, title,
text, chars, language`) più i campi propri (`partiti`, `tipo_documento`,
`consultazione`, `estrazione`). Dettagli, trappole e limiti in
`docs/data_provenance.md`.

### Layer 2 — Progetti di legge della Camera

Il layer "cosa fanno". Fonte: l'endpoint SPARQL pubblico
<https://dati.camera.it/sparql>, nessuno scraping.

```bash
python scripts/run_camera_spike.py
```

6.865 progetti di legge delle legislature 18 e 19, in circa 22 secondi. Il testo
tematizzabile è il **titolo** dell'atto, che alla Camera è una frase descrittiva
completa (mediana 161 caratteri) — molto più corto di un articolo di stampa: un
topic model tarato sul layer 3 non si applica tale e quale.

Paginazione **per chiave**, non per OFFSET: con `OFFSET 10000` Virtuoso risponde
500, perché per servire un offset profondo deve riordinare tutto il risultato a
ogni richiesta. Resa, costo e limiti misurati in `reports/layer2_recon/camera.md`.

### Risultati elettorali (catalogo Eligendo)

Il layer "chi li sostiene". Fonte: i CSV del catalogo AgID del Viminale,
download diretto.

```bash
python scripts/run_eligendo_spike.py
```

Camera e Senato 2022 ed europee 2024, aggregati a livello nazionale per lista
(i file sono comunali; la granularità nazionale è quella decisa dal piano).
Sette secondi in tutto.

Politiche ed europee usano **due schemi diversi** per gli stessi concetti
(`DESCRLISTA`/`VOTILISTA` contro `DESCLISTA`/`NUMVOTI`): il modulo lo dichiara
una volta e solleva su un file con schema ignoto, invece di sommare zeri in
silenzio.

Due limiti che cambiano il piano, dettagliati in
`reports/layer3_recon/eligendo.md`: **le politiche 2018 non sono nel catalogo**
(quindi la finestra 2018→2026 copre una sola politica), e la Valle d'Aosta è
assente dai file "Italia".

### Sondaggi — Salienza dei temi (Ipsos)

Stage separato dai corpus testuali (numeri, non testo): la salienza dei temi
nell'opinione pubblica, da correlare a valle con i temi della stampa.

`scripts/run_sondaggi_ipsos.py` estrae dal testo della pagina Ipsos Italia
(*What Worries the World*) i temi principali con le relative percentuali e li
accumula in un CSV tidy (`data, istituto, tema, valore, …`), deduplicando per
mese e tema.

L'approccio è **prospettico**: la pagina espone solo il mese corrente e lo storico
non è recuperabile, quindi il dataset si costruisce nel tempo eseguendo l'ingest
ogni mese. È un dataset che cresce in avanti, non una serie retrospettiva.
Dettagli e limiti in `docs/data_provenance.md`.

## Ambiente e dipendenze

Da una shell aperta nella root del repository:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

La discovery richiede `MC_API_KEY` come variabile d'ambiente oppure in un file
locale `.env`, ignorato da Git.

## Esecuzione della pipeline

Discovery degli URL, full-text e classificatore:

```bash
python src/mediacloud_spike.py
python src/mediacloud_fulltext.py
python src/news_topic_model.py --n-topics 12
```

Per uno smoke test della discovery:

```bash
python src/mediacloud_spike.py --max-stories 500
```

Audit riproducibile:

```bash
python scripts/run_topic_audit.py --config config/topic_audit.json
```

Layer 1 — programmi elettorali (discovery, poi full-text con OCR):

```bash
python scripts/run_viminale_discovery.py
python src/programmi_fulltext.py
```

Sondaggi — salienza dei temi Ipsos (da eseguire ogni mese, il dataset si accumula):

```bash
python scripts/run_sondaggi_ipsos.py
```

Campione riproducibile per lo human check:

```bash
python scripts/run_topic_human_review.py --config config/topic_human_review.json
```

Preparazione iniziale dei file R1/R2:

```bash
python scripts/prepare_topic_annotation_files.py --config config/topic_annotation.json
```

Controllo strutturale prima della compilazione:

```bash
python scripts/validate_topic_annotations.py \
  --config config/topic_annotation.json \
  --allow-incomplete
```

Validazione dopo la compilazione umana completa:

```bash
python scripts/validate_topic_annotations.py --config config/topic_annotation.json
```

## Test e verifica del notebook

Suite automatica completa:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Esecuzione del notebook da kernel pulito:

```bash
python -m jupyter nbconvert \
  --to notebook \
  --execute notebooks/classificatore.ipynb \
  --stdout \
  --ExecutePreprocessor.timeout=120 \
  > /dev/null
```

## Output versionati

Il checkpoint include soltanto output piccoli e verificabili:

- `data/processed/mediacloud_coverage.csv`: copertura aggregata per partito;
- `reports/topic_audit/`: audit, tabelle e manifest con hash;
- `reports/topic_human_review/`: campione di 27 record, riepilogo, guida e
  manifest;
- `annotations/topic_human_review/`: template separati per R1 e R2;
- `tests/fixtures/`: dati sintetici per i test.

I conteggi di copertura per partito controllano la raccolta. Poiché un articolo
può menzionare più partiti, le percentuali non devono necessariamente sommare a
100% e non misurano il consenso.

## Dati non versionati

Restano fuori da Git:

- `data/raw/*.jsonl` con URL e full-text (stampa e programmi del layer 1);
- `data/processed/news_topic_review.csv`;
- `data/processed/news_topic_terms.csv`;
- `data/processed/topic_model_metadata.json`;
- `data/processed/sondaggi_salienza_temi.csv` (dati Ipsos proprietari: versionarli
  richiede la revisione di compliance);
- `.env`, `.drive-export-dir`, credenziali e chiavi;
- ambienti virtuali, cache, log e file temporanei.

Gli input locali sono identificati dagli hash nei manifest. Il corpus completo
non viene pubblicato perché è grande e contiene testi acquisiti da fonti
editoriali esterne.

## Provenienza e riproducibilità

- `docs/data_provenance.md`: origine, trasformazioni e limiti dei dati;
- `docs/reproducibility.md`: ambiente, test, audit e manifest;
- `docs/topic_annotation_protocol.md`: categorie, calibrazione e revisione
  indipendente R1/R2;
- `AGENTS.md`: regole metodologiche e operative del progetto.

## Mirror locale Google Drive

Il mirror è facoltativo. Configurarlo soltanto sul proprio computer:

```bash
export GOOGLE_DRIVE_EXPORT_DIR="/percorso/al/mirror-locale"
```

In alternativa, inserire il percorso nel file locale `.drive-export-dir`. Il
file è ignorato da Git. Senza configurazione la pipeline continua a scrivere
soltanto nel repository locale.

## Esecuzione notturna

Per proseguire automaticamente dopo una discovery già avviata, su macOS:

```bash
mkdir -p logs
nohup /usr/bin/caffeinate -dims zsh scripts/run_overnight_pipeline.sh \
  > logs/overnight.log 2>&1 &
```

Lo script attende la fine della discovery e avvia full-text e classificatore.
I log restano locali e sono ignorati da Git.

## Condividere l'input del classificatore

`data/processed/news_topic_review.csv` pesa 98 MB, è in `.gitignore` e sta su una
macchina sola: chi clona il repository non può rieseguire né l'audit né il
campionamento. Sulla macchina che ha il file completo:

```bash
python scripts/prepara_review_condivisibile.py
```

Produce un campione stratificato per topic — 81 MB diventano 2.0 MB, il 2.5% —
pensato per essere versionato, più un manifest con gli hash. Non stima le
prevalenze: per quelle resta `reports/topic_audit/topic_distribution.csv`.

## Stato delle milestone

- Milestone 1R: audit NMF riproducibile approvato;
- Milestone 2: campione deterministico per human review approvato;
- Milestone 2A: protocollo tecnico R1/R2 approvato;
- calibrazione umana: sospesa fino al checkpoint Git condivisibile;
- Milestone 3: non iniziata.

## Compliance

Il repository è attualmente privato e destinato al lavoro accademico del team.
Campioni, estratti e annotazioni saranno sottoposti a una revisione di compliance
prima di un'eventuale pubblicazione.
