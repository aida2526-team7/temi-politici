# Temi politici

Progetto universitario di team del Master AIDA @ Unimib.it (A.A. 2025-2026) dedicato alla raccolta, elaborazione e analisi di dati politici.
https://aidamasterbicocca.it/

## Obiettivo

Realizzare una pipeline dati che consenta di:

- raccogliere dati da fonti pubbliche e contenuti online;
- organizzare e classificare i principali temi politici;
- analizzare candidati, partiti e copertura mediatica;
- produrre indicatori, visualizzazioni e dashboard;
- supportare attività di analisi per spin doctor, ricercatori e data journalist.

## Componenti del progetto

- scraping e acquisizione dati;
- archiviazione e gestione dei dataset;
- pulizia e trasformazione dei dati;
- analisi testuale e individuazione dei macrotemi;
- visualizzazione e dashboard;
- documentazione metodologica.

## Tecnologie

Il progetto potrà utilizzare Python, pandas, database SQL o NoSQL, KNIME, strumenti cloud e software di data visualization.

## Deposito automatico su Google Drive

Con Google Drive Desktop installato, impostare il percorso locale della cartella
di progetto prima di avviare la pipeline:

```bash
export GOOGLE_DRIVE_EXPORT_DIR="/percorso/reale/Politica Felice"
```

In alternativa, per conservarlo solo sul proprio computer, creare nel root del
repository il file `.drive-export-dir` contenente il percorso. Il file e' ignorato
da Git e prevale solo quando la variabile d'ambiente non e' presente.

`src/mediacloud_spike.py` copierà `mediacloud_urls.jsonl` in `raw/`;
`src/mediacloud_fulltext.py` copierà il full-text in `raw/` e la copertura per
partito in `processed/`. Le copie sono prima scritte in un file temporaneo, per
evitare che Drive sincronizzi output parziali. Senza la variabile, la pipeline
continua a scrivere solo nel repository locale.

## Stato

Progetto in fase iniziale di definizione.

********************************************************************
English vers.

# "Temi Politici" ("Political Issues")

A team project within the AIDA Master's program @ Unimib.it (Academic Year 2025-2026) dedicated to the collection, processing, and analysis of political data.
https://aidamasterbicocca.it/

## Objective

Create a data pipeline that allows:

- collect data from public sources and online content;
- organize and classify key political issues;
- analyze candidates, parties, and media coverage;
- produce indicators, visualizations, and dashboards;
- support analysis activities for spin doctors, researchers, and data journalists.

## Project Components

- scraping and data acquisition;
- dataset archiving and management;
- data cleaning and transformation;
- text analysis and identification of macro-themes;
- visualization and dashboards;
- methodological documentation.

## Technologies

The project may use Python, pandas, SQL or NoSQL databases, KNIME, cloud tools, and data visualization software.

## Status

Project in the early stages of definition.
