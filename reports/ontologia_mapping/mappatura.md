# Mappatura dei tre layer sull'ontologia v2.0

Generato da `scripts/run_mappa_ontologia.py`. Hash degli input in
`mapping_manifest.json`.

Il layer 3 è mappato sul **corpus completo**, 88.279 articoli, dal run NMF del
2026-08-27 — il primo eseguito dopo `src/pulizia_corpus.py`. Nessun ripeso: ogni
articolo vale uno.

## Le tre distribuzioni

Quote entro il corpus di ciascun layer, come impone l'ontologia.

| # | Macrotema | L1 programmi | L2 DDL | L3 stampa |
|---|---|---|---|---|
| 1 | Politica estera e difesa | 6,18% | 3,12% | **14,89%** |
| 2 | Unione europea | 2,60% | 1,59% | 4,14% |
| 3 | Istituzioni e assetto dello Stato | 7,26% | 9,58% | 12,04% |
| 4 | Economia e finanza pubblica | 9,53% | 7,85% | 3,13% |
| 5 | Lavoro e imprese | **18,35%** | 9,15% | 8,75% |
| 6 | Welfare e pensioni | 3,06% | 2,48% | 0,79% |
| 7 | Sanità | 4,65% | 7,43% | 4,37% |
| 8 | Istruzione e ricerca | 7,26% | 4,97% | 3,43% |
| 9 | Ambiente ed energia | 9,60% | 5,64% | 3,16% |
| 10 | Immigrazione e cittadinanza | 2,28% | 1,65% | 1,93% |
| 11 | Sicurezza e criminalità | 2,77% | **7,91%** | 4,52% |
| 12 | Diritti civili e società | 2,77% | 2,77% | 2,23% |
| 13 | Infrastrutture e territorio | 4,46% | 4,38% | 5,09% |
| 14 | Cultura e patrimonio | 2,60% | 3,18% | 4,08% |
| 15 | Sport | 0,42% | 0,96% | 2,46% |
| — | non assegnato | 16,21% | 27,36% | 21,72% |
| — | boilerplate | 0,00% | 0,00% | 3,27% |

Sottotema 9.1 *Animali e fauna*, come quota del proprio padre: **41,3% del tema 9
nel layer 2**, 19,0% nel layer 1. Quasi metà dei progetti di legge che finiscono
in *Ambiente ed energia* alla Camera parla di randagismo, maltrattamento o fauna
selvatica, non di energia o clima. Se il numero regge alla validazione umana,
vuol dire che il tema 9 nel layer 2 sta misurando due cose.

## Dove i layer divergono

Distanza in variazione totale, sui soli 15 macrotemi:

| Coppia | Divergenza |
|---|---|
| L1 programmi ↔ L2 DDL | 20,1 pp |
| L2 DDL ↔ L3 stampa | 25,8 pp |
| L1 programmi ↔ L3 stampa | 31,8 pp |

**Il lavoro si promette il doppio di quanto si legiferi.** *Lavoro e imprese* è il
18,4% dei paragrafi di programma e il 9,2% dei progetti di legge: +9,2 pp. È il
tema più grande del layer 1 e il secondo del layer 2. Nella stampa vale l'8,8%,
quasi come nei DDL: è lo scarto fra ciò che i partiti promettono e tutto il resto.

**La sicurezza si legifera il triplo di quanto si prometta.** *Sicurezza e
criminalità* è il 2,8% dei programmi e il 7,9% dei DDL: −5,1 pp, lo scarto
invertito più largo. Il segno opposto rispetto al lavoro rende improbabile un
artefatto del lessico, che sui due temi ha grana simile.

**La stampa e la Camera guardano due paesi diversi in politica estera.** 14,9%
degli articoli contro il 3,1% dei DDL: **−11,8 pp**, lo scarto singolo più largo
del confronto. È anche il più solido: il topic 10 è il topic NMF meglio definito
del corpus pulito, con il 68,6% dei suoi articoli su questo macrotema.

**L'economia va nella direzione opposta.** 7,9% dei DDL contro il 3,1% degli
articoli: +4,7 pp. La Camera legifera su bilancio, tributi e concorrenza molto più
di quanto la stampa ne scriva.

Dati per gruppo parlamentare in [`layer2_per_gruppo.csv`](layer2_per_gruppo.csv),
per programma in [`layer1_per_programma.csv`](layer1_per_programma.csv).

## Cosa ha cambiato la pulizia del corpus

Il layer 3 era stato mappato una prima volta sul campione del run NMF del
2026-07-12, precedente a `src/pulizia_corpus.py`. Il confronto misura cosa vale
la pulizia, a lessico costante:

| | Run sporco (12 lug) | Run pulito (27 ago) |
|---|---|---|
| Articoli modellati | 96.345 | 88.279 |
| Copertura del lessico | 63,2% | **75,0%** |
| Residuo boilerplate | 6,26% | 3,27% |
| Topic con etichetta *non assegnato* | 6 su 12 | 3 su 12 |
| Topic di solo boilerplate | 4 su 12 | 5 su 12, ma il 4,95% del corpus |
| Politica estera e difesa | 12,05% | 14,89% |

I due topic di parole funzione che nel run sporco valevano il 62% del corpus —
`si, ma, da, al, le` e `dei, le, dell, da, al` — sono spariti: la lista di 348
stopword italiane li ha sciolti. La pulizia ha tolto 93.329 righe di template da
31 domini su 80, e scartato 4.644 documenti senza testo e 3.555 duplicati.

I topic di boilerplate restano 5, ma sono diventati piccoli: insieme valgono il
4,95% del corpus contro il 7,15% di prima, e sono residui di testate singole
(`corriere viterbo`, `agenzia vista`, cookie policy ANSA), non più formule che
attraversano il corpus.

## I 12 topic NMF sul corpus pulito

| Topic | Prevalenza | Etichetta dominante | Quota | Boilerplate |
|---|---|---|---|---|
| 0 | 19,70% | non assegnato | 24,0% | 0,4% |
| 1 | 1,01% | boilerplate | 45,0% | 45,0% |
| 2 | 0,33% | boilerplate | 87,5% | 87,5% |
| 3 | 12,37% | non assegnato | 26,0% | 0,5% |
| 4 | 16,46% | non assegnato | 45,2% | 0,2% |
| 5 | 0,31% | Istituzioni e assetto dello Stato | 25,6% | 1,1% |
| 6 | 2,53% | boilerplate | 74,8% | 74,8% |
| 7 | 0,18% | boilerplate | 65,0% | 65,0% |
| 8 | 11,26% | **Istituzioni e assetto dello Stato** | 51,3% | 0,3% |
| 9 | 23,68% | Lavoro e imprese | 17,2% | 0,3% |
| 10 | 11,28% | **Politica estera e difesa** | 68,6% | 0,7% |
| 11 | 0,90% | boilerplate | 16,8% | 16,8% |

Due topic ora corrispondono a un macrotema con margine largo. Il **10** è la
politica estera (`iran, tajani, trump, esteri, guerra, israele`), il **8** è
l'assetto istituzionale (`referendum, riforma, giustizia, magistratura, nordio,
costituzione`).

I tre grandi topic che restano *non assegnato* non sono rumore: sono **politica
non tematica**, la categoria di servizio che l'ontologia prevede e che il lessico
non sa ancora riconoscere. Il topic 3 (12,4%) è `meloni, premier, presidente
consiglio, palazzo chigi`, il topic 4 (16,5%) è `sindaco, centrodestra, candidato,
coalizione, elezioni, lista`. Cronaca politica senza policy: chi dice cosa, chi si
candida dove. Il topic 0 (19,7%) è più sfuggente — `vita, storia, milano, persone,
mondo, famiglia, piazza` — e somiglia a cronaca generalista finita nel corpus.

Riconoscere `politica non tematica` è la prima cosa da aggiungere al lessico:
varrebbe da sola una fetta grossa del 21,7% ancora non assegnato.

## Metodo

Mappatura **lessicale deterministica**, `src/mappa_ontologia.py`: 350 pattern sui
15 macrotemi più 10 per il sottotema 9.1, testo normalizzato senza diacritici,
punteggio per occorrenze, vince il tema col punteggio più alto.

Un modello non supervisionato è stato scartato di proposito. L'ontologia è stata
congelata dall'alto, da MARPOR, proprio perché un topic model non restituisce
categorie politiche; mapparci sopra con un secondo modello non supervisionato
riporterebbe lo stesso problema un livello più su. Qui le regole si leggono e si
discutono una per una.

Le tre unità di misura seguono il contratto: paragrafo per il layer 1 (soglia 200
caratteri, 3.073 paragrafi da 60 programmi), atto per il layer 2 (6.865 titoli),
articolo per il layer 3 (88.279).

Con il corpus completo in locale lo script classifica tutti gli articoli. Senza —
cioè per chiunque cloni il repository, visto che i 92 MB stanno in `.gitignore` —
ricade sul campione stratificato e lo ripesa sulle prevalenze reali. La modalità
usata è scritta nel manifest, campo `layer3_sorgente`.

### Copertura

La quota di unità che il lessico assegna a un macrotema. È la misura di qualità
del metodo, e il denominatore delle tabelle sopra la include.

| Layer | Copertura |
|---|---|
| L1 programmi | 83,8% |
| L2 DDL | 72,6% |
| L3 stampa | 75,0% |

Il 27% di titoli non assegnati del layer 2 è in buona parte struttura legislativa
senza oggetto tematico nel titolo — «Modifica all'articolo 16 della legge 27
febbraio 1967, n. 48, concernente la composizione del Comitato interministeriale…».
Il testo dell'atto non è nel dataset: alla Camera il campo tematizzabile è il
titolo, e per questi il titolo non basta.

### Due esclusioni, trovate misurando

Il lessico toglie due formule dal testo prima di contare.

«dopo una lunga malattia» è la formula del coccodrillo. Nel campione del run
sporco faceva 176 occorrenze in un solo topic — necrologi tenuti insieme dalla
morte di Peppino di Capri — e lo mandava in *Sanità* al 77%.

«lavori del/della/dei» sono i lavori parlamentari: 394 occorrenze su 400 articoli
di un altro topic, che finiva in *Lavoro e imprese*.

Sono i due casi in cui una formula fissa, moltiplicata dai quasi-duplicati,
spostava un topic intero. La pulizia riduce questa classe di artefatto, non la
elimina.

## Limiti

- Il lessico **non è validato** contro una codifica umana. La validazione è il
  passo successivo, e per i 34 programmi del 2018 può appoggiarsi a MARPOR
  (ontologia, decisione 4).
- Misura di *cosa* si parla, mai la posizione. Coerente con la tassonomia, che
  accorpa le coppie pro/contro di MARPOR.
- Manca il riconoscimento di `politica non tematica`, e sono i tre topic più
  grandi del layer 3.
- Il 41,3% del tema 9 che finisce nel sottotema 9.1 nel layer 2 poggia su un
  lessico ampio (`\banimal\w*`). Va controllato a mano su un campione prima di
  farci sopra un'affermazione.
- 45 dei 60 programmi vengono dall'OCR. La segmentazione in paragrafi lavora su
  testo riconosciuto, e la soglia di 200 caratteri scarta i frammenti che l'OCR
  spezza.
