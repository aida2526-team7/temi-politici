# Riproducibilità dell'audit NMF

## Scopo

L'audit legge gli output già prodotti dal classificatore. Non scarica articoli,
non modifica gli input e non addestra nuovamente TF-IDF o NMF.

## Prerequisiti

- Python 3.11 o successivo;
- ambiente virtuale consigliato;
- dipendenze dichiarate in `requirements.txt`;
- `data/processed/news_topic_review.csv`;
- `data/processed/topic_model_metadata.json`.

Gli input grandi sono ignorati da Git e devono essere rigenerati o ottenuti
attraverso il flusso dati approvato dal gruppo.

## Ambiente

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Test

I test usano soltanto `tests/fixtures/topic_review_fixture.csv`:

```bash
python -m unittest tests/test_news_topic_audit.py -v
```

Questo comando costituisce anche la demo sintetica: verifica conteggi, duplicati,
campionamento deterministico, scrittura degli output e manifest.

## Audit reale

```bash
python scripts/run_topic_audit.py --config config/topic_audit.json
```

Output attesi in `reports/topic_audit/`:

- `audit_report.md`;
- `topic_distribution.csv`;
- `confidence_summary.csv`;
- `domain_summary.csv`;
- `duplicate_summary.json`;
- `run_manifest.json`.

## Manifest

Il manifest registra versione Python e librerie, parametri, seed, schema del CSV,
dimensioni e SHA-256 streaming degli input e degli output. I percorsi sono relativi
alla root. Il manifest non incorpora il proprio hash, perché un file non può
contenere stabilmente l'hash del proprio contenuto senza ricorsione.

## Limiti

- Il proxy dei quasi duplicati usa il prefisso normalizzato degli estratti da 500
  caratteri, non il full-text completo.
- La confidenza è una quota normalizzata dei pesi NMF, non una probabilità.
- L'audit produce evidenze quantitative; l'interpretazione semantica resta umana.
- Gli output dipendono dagli input locali identificati dagli hash nel manifest.
