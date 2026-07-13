# Provenienza dei dati dell'audit NMF

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

La sequenza tecnica è:

```bash
python src/mediacloud_spike.py
python src/mediacloud_fulltext.py
python src/news_topic_model.py --n-topics 12
python scripts/run_topic_audit.py --config config/topic_audit.json
```

Le credenziali, i percorsi locali e il mirror Google Drive non devono essere
inseriti nei file versionati.
