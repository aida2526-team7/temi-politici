# Mappatura dei tre layer sull'ontologia v2.0

Generato da `scripts/run_mappa_ontologia.py`. Hash degli input in
`mapping_manifest.json`.

Il layer 3 è mappato sul **corpus completo**, 88.279 articoli, dal run NMF del
2026-08-27 — il primo eseguito dopo `src/pulizia_corpus.py`. Nessun ripeso: ogni
articolo vale uno.

## Quanto la politica parla di sé

**Layer 1: 0,55%. Layer 2: 0,52%. Layer 3: 10,35%.**

È la quota di ciascun corpus che finisce in `politica non tematica`: nomine,
rimpasti, sondaggi, candidature, retroscena, chi sale e chi scende. Politica come
processo invece che come policy.

Il rapporto è di circa **venti a uno** fra la stampa e i due layer politici. Quando
i partiti promettono e quando la Camera legifera, hanno quasi sempre un oggetto —
un programma che parla di sé e basta non serve a niente, e un progetto di legge
senza materia non esiste. Il gioco puro compare quasi solo nel racconto.

Questo rende lo scarto interpretabile. Con il solo layer 3 non si potrebbe
distinguere «i politici parlano di sé» da «la stampa sceglie di raccontare il
gioco»: sono la stessa misura. La linea di base vicina allo zero sui layer 1 e 2
dice che il 10,35% è una **scelta di inquadramento della stampa**, non un riflesso
del comportamento di chi fa politica.

Resta una misura del corpus stampa, con i suoi limiti: il corpus viene da query
Media Cloud su partiti e leader, quindi è già selezionato attorno alle persone.
Un corpus costruito attorno alle policy darebbe una quota diversa.

In letteratura la distinzione fra *game frame* e *issue frame* è standard. La
citazione precisa va verificata prima di usarla in un documento accademico: qui
non è stata controllata.

## Le tre distribuzioni

Quote entro il corpus di ciascun layer, come impone l'ontologia.

| # | Macrotema | L1 programmi | L2 DDL | L3 stampa |
|---|---|---|---|---|
| 1 | Politica estera e difesa | 6,18% | 3,12% | **14,50%** |
| 2 | Unione europea | 2,60% | 1,59% | 4,05% |
| 3 | Istituzioni e assetto dello Stato | 7,22% | 9,57% | 11,01% |
| 4 | Economia e finanza pubblica | 9,53% | 7,84% | 2,96% |
| 5 | Lavoro e imprese | **18,32%** | 9,15% | 8,19% |
| 6 | Welfare e pensioni | 3,06% | 2,48% | 0,75% |
| 7 | Sanità | 4,59% | 7,43% | 4,25% |
| 8 | Istruzione e ricerca | 7,26% | 4,97% | 3,30% |
| 9 | Ambiente ed energia | 9,60% | 5,64% | 2,98% |
| 10 | Immigrazione e cittadinanza | 2,28% | 1,65% | 1,87% |
| 11 | Sicurezza e criminalità | 2,77% | **7,91%** | 4,40% |
| 12 | Diritti civili e società | 2,77% | 2,77% | 2,15% |
| 13 | Infrastrutture e territorio | 4,46% | 4,38% | 4,83% |
| 14 | Cultura e patrimonio | 2,60% | 3,18% | 3,87% |
| 15 | Sport | 0,42% | 0,96% | 2,38% |
| — | politica non tematica | 0,55% | 0,52% | 10,35% |
| — | non assegnato | 15,78% | 26,86% | 14,87% |
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
| L1 programmi ↔ L2 DDL | 20,2 pp |
| L2 DDL ↔ L3 stampa | 25,8 pp |
| L1 programmi ↔ L3 stampa | 32,1 pp |

**Il lavoro si promette il doppio di quanto si legiferi.** *Lavoro e imprese* è il
18,3% dei paragrafi di programma e il 9,2% dei progetti di legge: +9,2 pp. È il
tema più grande del layer 1 e il secondo del layer 2. Nella stampa vale l'8,2%,
quasi come nei DDL: lo scarto è fra ciò che i partiti promettono e tutto il resto.

**La sicurezza si legifera il triplo di quanto si prometta.** *Sicurezza e
criminalità* è il 2,8% dei programmi e il 7,9% dei DDL: −5,1 pp, lo scarto
invertito più largo. Il segno opposto rispetto al lavoro rende improbabile un
artefatto del lessico, che sui due temi ha grana simile.

**La stampa e la Camera guardano due paesi diversi in politica estera.** 14,5%
degli articoli contro il 3,1% dei DDL: **−11,4 pp**, lo scarto singolo più largo
del confronto. È anche il più solido: il topic 10 è il topic NMF meglio definito
del corpus pulito, con il 68,0% dei suoi articoli su questo macrotema.

**L'economia va nella direzione opposta.** 7,8% dei DDL contro il 3,0% degli
articoli: +4,9 pp. La Camera legifera su bilancio, tributi e concorrenza molto più
di quanto la stampa ne scriva.

Dati per gruppo parlamentare in [`layer2_per_gruppo.csv`](layer2_per_gruppo.csv),
per programma in [`layer1_per_programma.csv`](layer1_per_programma.csv).

## Cosa ha cambiato la pulizia del corpus

Il layer 3 era stato mappato una prima volta sul campione del run NMF del
2026-07-12, precedente a `src/pulizia_corpus.py`. Il confronto misura cosa vale
la pulizia, a lessico costante — le due colonne usano il lessico com'era **prima**
che esistesse `politica non tematica`:

| | Run sporco (12 lug) | Run pulito (27 ago) |
|---|---|---|
| Articoli modellati | 96.345 | 88.279 |
| Copertura del lessico | 63,2% | **75,0%** |
| Residuo boilerplate | 6,26% | 3,27% |
| Topic con etichetta *non assegnato* | 6 su 12 | 3 su 12 |

I due topic di parole funzione che nel run sporco valevano il 62% del corpus —
`si, ma, da, al, le` e `dei, le, dell, da, al` — sono spariti: la lista di 348
stopword italiane li ha sciolti. La pulizia ha tolto 93.329 righe di template da
31 domini su 80, e scartato 4.644 documenti senza testo e 3.555 duplicati.

I topic di boilerplate restano 5, ma sono diventati piccoli: insieme valgono il
4,95% del corpus contro il 7,15% di prima, e sono residui di testate singole
(`corriere viterbo`, `agenzia vista`, cookie policy ANSA), non più formule che
attraversano il corpus.

Aggiungere `politica non tematica` ha poi spostato **6,9 pp** del layer 3 fuori da
`non assegnato`, che scende dal 21,7% al 14,9%, e 3,5 pp da macrotemi assegnati
per un soffio. La copertura per macrotema cala di conseguenza dal 75,0% al 71,5%:
non è un peggioramento, è la stessa massa contata meglio.

## I 12 topic NMF sul corpus pulito

| Topic | Prevalenza | Etichetta dominante | Quota | Boilerplate |
|---|---|---|---|---|
| 0 | 19,70% | non assegnato | 22,0% | 0,4% |
| 1 | 1,01% | boilerplate | 45,0% | 45,0% |
| 2 | 0,33% | boilerplate | 87,5% | 87,5% |
| 3 | 12,37% | Politica estera e difesa | 21,9% | 0,5% |
| 4 | 16,46% | **politica non tematica** | 39,5% | 0,2% |
| 5 | 0,31% | Istituzioni e assetto dello Stato | 23,3% | 1,1% |
| 6 | 2,53% | boilerplate | 74,8% | 74,8% |
| 7 | 0,18% | boilerplate | 65,0% | 65,0% |
| 8 | 11,26% | **Istituzioni e assetto dello Stato** | 49,5% | 0,3% |
| 9 | 23,68% | Lavoro e imprese | 16,9% | 0,3% |
| 10 | 11,28% | **Politica estera e difesa** | 68,0% | 0,7% |
| 11 | 0,90% | boilerplate | 16,8% | 16,8% |

Tre topic corrispondono a una categoria con margine largo. Il **10** è la politica
estera (`iran, tajani, trump, esteri, guerra, israele`), l'**8** è l'assetto
istituzionale (`referendum, riforma, giustizia, magistratura, nordio,
costituzione`), il **4** è la politica come processo (`sindaco, centrodestra,
candidato, coalizione, elezioni, lista`) — il topic elettorale, riconosciuto per
quello che è.

Restano fuori il topic 0 (19,7%), cronaca generalista finita nel corpus (`vita,
storia, milano, persone, mondo, famiglia, piazza`), e il topic 9 (23,68%), il più
grande di tutti e il più diffuso: `euro, regionale, regione, risorse, territorio,
imprese, lavoro` non è un tema, è il lessico dell'amministrazione che attraversa
tutti i temi.

## Metodo

Mappatura **lessicale deterministica**, `src/mappa_ontologia.py`: 350 pattern sui
15 macrotemi, 45 per `politica non tematica`, 10 per il sottotema 9.1. Testo
normalizzato senza diacritici, punteggio per occorrenze, vince il più alto.

`politica non tematica` concorre come i macrotemi, non filtra prima di loro: un
pezzo sulla manovra che cita anche il vertice di maggioranza parla di manovra. A
parità di punteggio vince il macrotema, perché la parità dice che il testo una
policy ce l'ha. Il suo lessico è deliberatamente specifico del processo —
`governo`, `ministro`, `partito` e `opposizione` ne restano fuori, perché
compaiono in ogni articolo politico e includerli farebbe vincere questa categoria
su tutto il resto.

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

La quota di unità che il lessico assegna a un **macrotema**. Le categorie di
servizio non contano come copertura, e il denominatore le include.

| Layer | Copertura |
|---|---|
| L1 programmi | 83,7% |
| L2 DDL | 72,6% |
| L3 stampa | 71,5% |

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

- Il lessico **non è validato** contro una codifica umana, e vale anche per
  `politica non tematica`: il 10,35% del layer 3 è una misura di lessico, non di
  codifica. La validazione è il passo successivo, e per i 34 programmi del 2018
  può appoggiarsi a MARPOR (ontologia, decisione 4).
- Misura di *cosa* si parla, mai la posizione. Coerente con la tassonomia, che
  accorpa le coppie pro/contro di MARPOR.
- Il 41,3% del tema 9 che finisce nel sottotema 9.1 nel layer 2 poggia su un
  lessico ampio (`\banimal\w*`). Va controllato a mano su un campione prima di
  farci sopra un'affermazione.
- Il 14,9% del layer 3 ancora non assegnato è concentrato nei topic 0 e 9, che
  non sono temi: cronaca generalista e lessico amministrativo diffuso.
- 45 dei 60 programmi vengono dall'OCR. La segmentazione in paragrafi lavora su
  testo riconosciuto, e la soglia di 200 caratteri scarta i frammenti che l'OCR
  spezza.
