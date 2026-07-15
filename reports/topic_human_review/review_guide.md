# Guida allo human check dei topic

## Scopo

Il campione è selezionato automaticamente e in modo riproducibile. Il giudizio
semantico resta umano: non modificare le colonne di provenienza o selezione.

## Come è costruito il campione

- Topic utili `[1, 8, 9]`: 3 record ad alto peso e 3 casuali per topic.
- Topic di controllo artefatto `[0, 2, 3, 4, 5, 6, 7, 10, 11]`: 1 record ad alto peso per topic.
- Seed casuale: `42`.
- Massimo desiderato per dominio nei topic utili: `2`.
- Duplicati esatti titolo + estratto esclusi.

## Categorie per `classificazione_umana`

- tema politico coerente
- tema politico misto
- boilerplate o formato editoriale
- contenuto non politico
- dubbio

Per `boilerplate_si_no` e `duplicato_sospetto_si_no` usare: `sì`, `no`, `incerto`.
Per `decisione_inclusione` usare: `mantenere`, `escludere`, `riesaminare`.

Compilare anche `etichetta_tema_proposta` e `note_revisore` quando utili. La
`valutazione_preliminare` descrive soltanto il motivo automatico della selezione.

## Eccezioni documentate

- Nessuna eccezione alla diversificazione per dominio.

## Limiti

Il campione non stima la prevalenza dei temi e non misura stance, consenso o
comportamento politico. Serve esclusivamente a controllare interpretabilità,
boilerplate, contenuti non politici e casi dubbi.
