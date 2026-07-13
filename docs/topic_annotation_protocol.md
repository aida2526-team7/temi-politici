# Protocollo di annotazione umana dei topic — versione 1.0

## 1. Scopo

Lo human check valuta se i topic NMF mostrano un tema politico coerente, un
tema misto, boilerplate editoriale, contenuto non politico o un caso dubbio.
Non misura consenso, sentiment, stance o comportamento istituzionale.

## 2. Selezione automatica e giudizio umano

Il campione è stato selezionato automaticamente con regole, seed e provenienza
registrati. `tipo_selezione`, pesi e `valutazione_preliminare` spiegano perché
un record è nel campione; non costituiscono un giudizio semantico. Solo R1 e R2
compilano le colonne di annotazione.

## 3. Categorie di classificazione

- **tema politico coerente**: il record tratta un argomento politico riconoscibile
  e compatibile con gli altri casi del topic;
- **tema politico misto**: contiene più argomenti o il legame tematico è parziale;
- **boilerplate o formato editoriale**: menu, riquadri, liste, rilanci, formule di
  agenzia o altri elementi di pagina dominano il contenuto selezionato;
- **contenuto non politico**: il contenuto principale non riguarda politica o
  attività istituzionale nel senso rilevante per il progetto;
- **dubbio**: le evidenze disponibili non consentono una classificazione affidabile.

## 4. Altri campi decisionali

**Boilerplate** indica testo ripetitivo legato alla struttura editoriale più che
all'articolo. **Duplicato sospetto** indica un caso che sembra replicare o
riutilizzare sostanzialmente un altro contenuto, anche se non è un duplicato
esatto già escluso dal codice.

- `mantenere`: il record è utile per interpretare il topic;
- `escludere`: il record è fuorviante o dominato da artefatti;
- `riesaminare`: serve confronto o maggiore contesto.

Per i campi sì/no usare esclusivamente `sì`, `no` o `incerto`.

## 5. Colonne compilabili

Compilare soltanto:

- `classificazione_umana`;
- `etichetta_tema_proposta`;
- `boilerplate_si_no`;
- `duplicato_sospetto_si_no`;
- `decisione_inclusione`;
- `note_revisore`.

## 6. Colonne da non modificare

Non modificare colonne sorgente, `reviewer_id`, `protocol_version` o
`fase_revisione`. In particolare non cambiare URL, titolo, estratto, topic,
pesi, data, dominio, `review_id` o `source_row_index`.

## 7. Calibrazione sui primi cinque record

R1 e R2 annotano i cinque record marcati `calibrazione`. Dopo averli compilati,
possono discutere insieme soltanto definizioni e criteri, annotando eventuali
chiarimenti al protocollo. Non si produce ancora un file aggiudicato.

## 8. Revisione indipendente

I restanti 22 record, marcati `indipendente`, devono essere valutati
separatamente applicando la versione 1.0 del protocollo.

## 9. Indipendenza dei revisori

Durante la fase indipendente è vietato consultare, copiare o discutere le
risposte dell'altro revisore. Ogni revisore lavora esclusivamente sul proprio CSV.

## 10. Confronto e futura aggiudicazione

Dopo la validazione completa dei due file verrà calcolato l'accordo tra revisori.
Disaccordi e casi dubbi saranno discussi in una fase futura e separata. Il file
`adjudicated.csv` non viene creato durante questa milestone.

## 11. Gestione dei dubbi

Usare `dubbio`, `incerto` o `riesaminare` quando il solo titolo ed estratto non
sono sufficienti. Spiegare brevemente il motivo in `note_revisore`, senza
inventare informazioni non presenti.

## 12. Limiti del campione

Le 27 righe servono a un controllo qualitativo mirato e non sono un campione
statisticamente rappresentativo dell'informazione politica italiana. Il corpus
deriva da query su partiti e leader e descrive come vengono raccontati.

## Comandi

Preparazione iniziale:

```bash
python scripts/prepare_topic_annotation_files.py --config config/topic_annotation.json
```

Controllo strutturale prima della compilazione:

```bash
python scripts/validate_topic_annotations.py --config config/topic_annotation.json --allow-incomplete
```

Validazione dopo la compilazione completa:

```bash
python scripts/validate_topic_annotations.py --config config/topic_annotation.json
```
