# Annotazioni human review

Questa directory contiene due copie indipendenti del campione immutabile:

- `reviewer_R1.csv` per il revisore R1;
- `reviewer_R2.csv` per il revisore R2.

Compilare soltanto le colonne elencate in
`docs/topic_annotation_protocol.md`. Non consultare il file dell'altro revisore
durante la fase indipendente. I file vengono validati in sola lettura con:

```bash
python scripts/validate_topic_annotations.py --config config/topic_annotation.json
```

La preparazione non produce classificazioni, accordo o aggiudicazione.

## Avvertenza sulla rigenerazione

Eseguire `scripts/prepare_topic_annotation_files.py` soltanto per creare i
template iniziali. **Dopo l'inizio delle annotazioni non rilanciare il
preparatore:** i file `reviewer_R1.csv` e `reviewer_R2.csv` vengono rigenerati e
le risposte umane già inserite potrebbero essere sovrascritte.

Il validatore `scripts/validate_topic_annotations.py` opera invece in sola
lettura e può essere eseguito in qualsiasi momento.
