# Mappatura dei tre layer sull'ontologia v2.0

Generato da `scripts/run_mappa_ontologia.py`. Hash degli input in
`mapping_manifest.json`.

Il layer 3 è mappato sul **corpus completo**, <!--n:articoli_l3-->107.021<!--/n--> articoli, dal run NMF del
2026-08-28 sul corpus esteso a tutto agosto. Nessun ripeso: ogni articolo vale uno.

## Quanto la politica parla di sé

**Layer 1: <!--n:pnt_l1-->0,46%<!--/n-->. Layer 2: <!--n:pnt_l2-->0,52%<!--/n-->. Layer 3: <!--n:pnt_l3-->10,03%<!--/n-->.**

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

## Il marcatore woke: agosto 2026

Un **marcatore trasversale** (ontologia v2.1) convive col macrotema invece di
sostituirlo: dice come un testo inquadra il tema, non di che tema parla.

Volume nel corpus, normalizzato su mille articoli perché il corpus cresce:

| Mese | Articoli | Su mille |
|---|---|---|
| gennaio | 13 | 0,12 |
| febbraio | 22 | 0,21 |
| marzo | 7 | 0,07 |
| aprile | 3 | 0,03 |
| maggio | 8 | 0,07 |
| giugno | 6 | 0,06 |
| luglio | 11 | 0,10 |
| **agosto** | **121** | **1,13** |

Undici volte la linea di base dei sette mesi precedenti, e agosto è troncato al
27. Nel corpus di ieri, che si fermava all'11 luglio, questa storia non esisteva:
è interamente dentro le sei settimane aggiunte.

**Dove si posa il frame**, come quota dei <!--n:marcatore_woke-->191<!--/n--> articoli che lo portano:

| Macrotema | Articoli | Quota |
|---|---|---|
| Cultura e patrimonio | 36 | 18,9% |
| non assegnato | 35 | 18,3% |
| Immigrazione e cittadinanza | 23 | 12,0% |
| Politica estera e difesa | 18 | 9,4% |
| Diritti civili e società | 16 | 8,4% |
| politica non tematica | 14 | 7,3% |
| Istruzione e ricerca | 13 | 6,8% |

**Questa tabella è la giustificazione della scelta di disegno.** Solo il 7,3%
cade in `politica non tematica`: archiviare lì l'intero frame avrebbe buttato via
il fatto che si attacca soprattutto a cultura, immigrazione, diritti e scuola. E
il 18,9% su *Cultura* non lo renderebbe un tema culturale: il margine mediano di
questi articoli resta basso, perché ognuno tocca quattro o cinque lessici.

**Limite, da ripetere ogni volta che il numero viene citato.** Il marcatore rileva
la presenza del frame, non la posizione di chi lo usa. Chi accusa il woke e chi lo
difende finiscono nello stesso conteggio, e i titoli del corpus mostrano entrambi.

Dati in [`marcatori_per_mese.csv`](marcatori_per_mese.csv) e
[`marcatori_per_tema.csv`](marcatori_per_tema.csv).

## Le tre distribuzioni

Quote entro il corpus di ciascun layer, come impone l'ontologia.

| # | Macrotema | L1 programmi | L2 DDL | L3 stampa |
|---|---|---|---|---|
| 1 | Politica estera e difesa | 5,47% | 3,12% | **13,34%** |
| 2 | Unione europea | 3,11% | 1,59% | 3,70% |
| 3 | Istituzioni e assetto dello Stato | 5,76% | 9,57% | 10,64% |
| 4 | Economia e finanza pubblica | 9,52% | 7,84% | 2,94% |
| 5 | Lavoro e imprese | **18,54%** | 9,15% | 7,99% |
| 6 | Welfare e pensioni | 3,22% | 2,48% | 0,78% |
| 7 | Sanità | 5,17% | 7,43% | 4,24% |
| 8 | Istruzione e ricerca | 6,75% | 4,97% | 3,09% |
| 9 | Ambiente ed energia | 11,18% | 5,72% | 4,16% |
| 10 | Immigrazione e cittadinanza | 1,87% | 1,65% | 2,29% |
| 11 | Sicurezza e criminalità | 2,94% | **7,91%** | 5,13% |
| 12 | Diritti civili e società | 2,67% | 2,77% | 2,12% |
| 13 | Infrastrutture e territorio | 5,66% | 4,37% | 4,95% |
| 14 | Cultura e patrimonio | 2,61% | 3,18% | 3,84% |
| 15 | Sport | 0,57% | 0,96% | 2,35% |
| — | politica non tematica | 0,46% | 0,52% | 10,03% |
| — | non assegnato | 14,50% | 26,79% | 15,14% |
| — | boilerplate | 0,00% | 0,00% | 3,28% |

Sottotema 9.1 *Animali e fauna*, come quota del proprio padre: **<!--n:sotto_9_1_l2-->40,7%<!--/n--> del tema 9
nel layer 2**, <!--n:sotto_9_1_l1-->17,2%<!--/n--> nel layer 1. Quasi metà dei progetti di legge che finiscono
in *Ambiente ed energia* alla Camera parla di randagismo, maltrattamento o fauna
selvatica, non di energia o clima. Se il numero regge alla validazione umana,
vuol dire che il tema 9 nel layer 2 sta misurando due cose.

## Dove i layer divergono

Distanza in variazione totale, sui soli 15 macrotemi:

| Coppia | Divergenza |
|---|---|
| L1 programmi ↔ L2 DDL | <!--n:div_l1_l2-->20,7 pp<!--/n--> |
| L2 DDL ↔ L3 stampa | <!--n:div_l2_l3-->23,8 pp<!--/n--> |
| L1 programmi ↔ L3 stampa | <!--n:div_l1_l3-->31,7 pp<!--/n--> |

**Il lavoro si promette il doppio di quanto si legiferi.** *Lavoro e imprese* è il
18,5% dei paragrafi di programma e il 9,2% dei progetti di legge: +9,4 pp. È il
tema più grande del layer 1 e il secondo del layer 2. Nella stampa vale l'8,0%,
quasi come nei DDL: lo scarto è fra ciò che i partiti promettono e tutto il resto.

**La sicurezza si legifera il triplo di quanto si prometta.** *Sicurezza e
criminalità* è il 2,9% dei programmi e il 7,9% dei DDL: −5,0 pp, lo scarto
invertito più largo. Il segno opposto rispetto al lavoro rende improbabile un
artefatto del lessico, che sui due temi ha grana simile.

**La stampa e la Camera guardano due paesi diversi in politica estera.** 13,3%
degli articoli contro il 3,1% dei DDL: **−10,2 pp**, lo scarto singolo più largo
del confronto. È anche il più solido: il topic 3, il 18,4% del corpus, è il topic
NMF meglio definito e ha il 49,8% dei suoi articoli su questo macrotema.

**L'economia va nella direzione opposta.** 7,8% dei DDL contro il 2,9% degli
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
| 0 | 20,57% | Lavoro e imprese | 17,1% | 0,4% |
| 1 | 0,83% | boilerplate | 45,0% | 45,0% |
| 2 | 0,31% | boilerplate | 89,3% | 89,3% |
| 3 | 18,36% | **Politica estera e difesa** | 49,8% | 0,6% |
| 4 | 16,64% | **politica non tematica** | 37,4% | 0,3% |
| 5 | 2,73% | boilerplate | 73,3% | 73,3% |
| 6 | 0,31% | Istituzioni e assetto dello Stato | 21,6% | 0,9% |
| 7 | 26,39% | non assegnato | 21,3% | 0,4% |
| 8 | 0,16% | boilerplate | 61,6% | 61,6% |
| 9 | 12,08% | **Istituzioni e assetto dello Stato** | 43,0% | 0,3% |
| 10 | 0,70% | Ambiente ed energia | 21,0% | 0,0% |
| 11 | 0,91% | non assegnato | 16,9% | 15,3% |

Tre topic corrispondono a una categoria con margine largo. Il **10** è la politica
estera (`iran, tajani, trump, esteri, guerra, israele`), l'**8** è l'assetto
istituzionale (`referendum, riforma, giustizia, magistratura, nordio,
costituzione`), il **4** è la politica come processo (`sindaco, centrodestra,
candidato, coalizione, elezioni, lista`) — il topic elettorale, riconosciuto per
quello che è.

Restano fuori il topic 7 (26,4%), cronaca generalista (`vita, persone, storia,
milano, famiglia`), e il topic 0 (20,6%), il lessico dell'amministrazione — `euro,
regionale, territorio, risorse, imprese` — che attraversa tutti i temi senza
esserne uno.

### Perché non si etichetta un topic dai suoi termini

Il topic 10 (754 articoli) ha come termini caratteristici `risorse sconto,
carburanti finiscono, proroga gasolio`: sembra un topic sul caro carburanti. Non
lo è. **539 dei suoi 754 articoli vengono da `varesenews.it`**, e il primo che si
apre parla di atti vandalici a Mustonate. È un artefatto di dominio — l'audit lo
segnala fra i topic con dominio dominante sopra il 50% — che tiene insieme cronaca
locale con dentro anche i pezzi sulle accise.

Non è boilerplate: i titoli distinti sono 748 su 754. È peggio, perché sembra
interpretabile. I termini caratteristici dell'NMF descrivevano una minoranza della
massa del topic, e chi avesse assegnato un macrotema leggendoli avrebbe etichettato
«energia» 754 articoli di cronaca varesina.

È il caso più chiaro del perché la mappatura si fa col lessico sul testo di ogni
articolo e non passando dai topic.

## H1 — coerenza fra ciò che si promette e ciò che si legifera

L'indice che il piano chiede: la distanza fra la distribuzione dei paragrafi di
programma di un partito e quella dei suoi progetti di legge. Variazione totale sui
15 macrotemi, in punti percentuali. Zero = identiche.

| Partito | Paragrafi | Atti | H1 |
|---|---|---|---|
| Partito Democratico | 221 | 354 | **23,6** |
| Lega | 988 | 683 | **24,8** |
| Movimento 5 Stelle | 976 | 711 | **24,8** |
| Forza Italia | 82 | 358 | 25,1 |
| Fratelli d'Italia | 145 | 599 | **30,3** |

Quattro valori su cinque reggono la soglia di 100 unità su entrambi i lati. Forza
Italia resta sotto, con 82 paragrafi: il valore c'è ma è marcato inaffidabile in
[`indice_h1.csv`](indice_h1.csv).

I quattro affidabili stanno in una forcella stretta, 23,6-30,3. **Fratelli
d'Italia è il meno coerente dei quattro**, con quasi 7 punti di distacco dal PD. Va
letto con prudenza: FdI ha anche il programma più corto fra i recuperati (145
paragrafi contro i 988 della Lega), e la coda della distribuzione è quella che
soffre di più con pochi paragrafi.

H1 misura **distanza di agenda**, non incoerenza politica: dice che i temi su cui
un partito deposita proposte di legge non sono, nelle stesse proporzioni, quelli
su cui ha costruito il programma. Non dice che abbia tradito il programma.

### Il controllo: le due fonti del layer 1 sono la stessa unità?

H1 poggia su programmi presi dai siti di partito, non sui depositi al Viminale.
Sono due unità diverse — l'atto formale previsto dalla legge 165/2017 contro il
materiale di campagna — e la sostituzione va giustificata, non assunta.

Cinque liste hanno entrambe le fonti, quindi la distanza fra le loro due
distribuzioni si misura:

| Partito | Paragrafi Viminale | Paragrafi sito | Divergenza |
|---|---|---|---|
| **Partito Democratico** | **172** | **221** | **6,4 pp** |
| Fratelli d'Italia | 24 | 145 | 19,8 pp |
| Forza Italia | 19 | 82 | 27,3 pp |
| Movimento 5 Stelle | 13 | 976 | 36,3 pp |
| Lega | 14 | 988 | 37,3 pp |

Solo il PD ha numeri sufficienti da entrambe le parti, ed è l'unica riga che
misura davvero la differenza fra le due unità: **6,4 pp**, contro valori di H1 fra
23 e 31. Le altre quattro righe misurano soprattutto il rumore del lato corto —
13 paragrafi contro 976 — non una divergenza di sostanza.

Con un solo controllo la conclusione resta provvisoria, ma va nella direzione
giusta: dove entrambe le fonti hanno testo a sufficienza raccontano quasi la stessa
distribuzione, e il margine che l'integrazione introduce è dell'ordine di 6 punti,
circa un quarto del valore di H1 che si vuole misurare.

## L'intersezione con i sondaggi

I temi che preoccupano gli italiani sono gli stessi su cui i partiti promettono,
legiferano e la stampa scrive?

**Si confrontano ranghi, non livelli.** I valori Ipsos sono la percentuale di
intervistati che cita un tema fra le proprie preoccupazioni principali: ognuno è
indipendente dagli altri e la somma supera il 100% — 162% nel giugno 2026. Non
sono una distribuzione e non stanno sulla stessa scala delle quote dei tre layer.
Il rango sopravvive alla differenza.

Giugno 2026, il mese con più rilevazioni:

| Macrotema | Ipsos | Opinione | Programmi | DDL | Stampa |
|---|---|---|---|---|---|
| Sicurezza e criminalità | 37% | **1** | **4** | 2 | 2 |
| Sanità | 35% | 2 | 3 | 4 | 3 |
| Lavoro e imprese | 34% | 3 | **1** | 1 | 1 |
| Economia e finanza pubblica | 30% | 4 | 2 | 3 | 4 |

**La preoccupazione numero uno degli italiani è il tema su cui i partiti
promettono meno.** Sicurezza e criminalità è prima per l'opinione pubblica e
ultima delle quattro nei programmi elettorali — un'inversione completa.

Nei progetti di legge però risale al secondo posto. Combinato con lo scarto già
misurato — la sicurezza si legifera il triplo di quanto si prometta — il quadro è
coerente: sulla criminalità i partiti **non promettono ma legiferano**, ed è ciò
che gli italiani dicono di temere di più.

Specularmente, *Lavoro e imprese* è primo in tutti e tre i nostri layer ma solo
terzo fra le preoccupazioni.

Scarto di rango rispetto all'opinione pubblica, somma degli scostamenti assoluti:

| Layer | Scarto |
|---|---|
| Stampa | **4** |
| Progetti di legge | 6 |
| Programmi | **8** |

Su queste quattro voci la stampa è più vicina alle preoccupazioni degli italiani
di quanto lo siano i programmi dei partiti.

### Quanto vale questo confronto

Poco, e va detto prima che lo si citi.

- Ipsos espone solo i temi in testa: dei 15 macrotemi ne copre **4**.
- Il confronto è su **un mese**. La serie ha 7 mesi ma è sparsa, e solo `tasse`
  ha più di tre rilevazioni.
- Con quattro voci lo scarto di rango è una statistica grossolana: l'ordine
  fra 4 e 6 non è distinguibile dal caso.
- `inflazione` e `tasse` cadono entrambe nel macrotema 4 e non si sommano — sono
  due domande allo stesso intervistato. Si tiene la più alta.

Il numero solido è l'inversione della sicurezza, perché è di quattro posizioni su
quattro possibili e regge indipendentemente da come si trattano le altre voci.

Dati in [`intersezione_sondaggi.csv`](intersezione_sondaggi.csv), rigenerabili con
`python scripts/run_intersezione_sondaggi.py`.

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
caratteri, 5.243 paragrafi da 60 programmi, di cui 5 presi dai siti di partito), atto per il layer 2 (6.865 titoli),
articolo per il layer 3 (<!--n:articoli_l3-->107.021<!--/n-->).

Con il corpus completo in locale lo script classifica tutti gli articoli. Senza —
cioè per chiunque cloni il repository, visto che i 92 MB stanno in `.gitignore` —
ricade sul campione stratificato e lo ripesa sulle prevalenze reali. La modalità
usata è scritta nel manifest, campo `layer3_sorgente`.

### Copertura

La quota di unità che il lessico assegna a un **macrotema**. Le categorie di
servizio non contano come copertura, e il denominatore le include.

| Layer | Copertura |
|---|---|
| L1 programmi | <!--n:copertura_l1-->85,1%<!--/n--> |
| L2 DDL | <!--n:copertura_l2-->72,7%<!--/n--> |
| L3 stampa | <!--n:copertura_l3-->71,6%<!--/n--> |

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
