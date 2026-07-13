# Progetto AIDA sui temi politici

Progetto universitario del Master AIDA @ Unimib.it (A.A. 2025–2026) dedicato
all'analisi data-driven dei temi politici italiani.

## Obiettivo della fase corrente

La fase attuale analizza articoli raccolti tramite query Media Cloud su partiti e
leader. Il corpus rappresenta **come la politica viene raccontata dalla stampa**:
non misura automaticamente comunicazione diretta, attività legislativa,
consenso, sentiment verso un partito o stance su una policy.

L'obiettivo è scoprire microtemi con TF-IDF + NMF, controllarne qualità e
boilerplate e prepararne la validazione umana. I macrotemi risultanti saranno
ancora una tassonomia candidata, non un'ontologia definitiva multi-layer.

## Pipeline

1. `src/mediacloud_spike.py` interroga Media Cloud e salva gli URL.
2. `src/mediacloud_fulltext.py` e `src/harvester.py` scaricano e puliscono il
   full-text, rilevano la lingua e producono la copertura aggregata.
3. `src/news_topic_model.py` applica TF-IDF + NMF e genera 12 topic esplorativi.
4. `scripts/run_topic_audit.py` verifica distribuzioni, confidenza, domini,
   duplicati e anomalie degli output NMF.
5. `scripts/run_topic_human_review.py` costruisce un campione deterministico di
   27 record per lo human check.
6. `scripts/prepare_topic_annotation_files.py` prepara due copie indipendenti
   per R1 e R2; `scripts/validate_topic_annotations.py` le valida senza
   modificarle.

I notebook richiamano o leggono la logica e gli output salvati nel repository:

- `notebooks/00_esegui_pipeline.ipynb`: orchestrazione didattica della pipeline;
- `notebooks/classificatore.ipynb`: audit, campione e istruzioni di review.

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

- `data/raw/*.jsonl` con URL e full-text;
- `data/processed/news_topic_review.csv`;
- `data/processed/news_topic_terms.csv`;
- `data/processed/topic_model_metadata.json`;
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
