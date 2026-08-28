# Ontologia tematica — v2.1, congelata

**Stato: congelata il 2026-08-28.** È il contratto fra i tre layer. Da qui in
avanti le trasformazioni si scrivono contro questa versione; cambiarla richiede
una nuova versione e la rilettura di ciò che ne dipende.

La v2.0 ha portato i macrotemi da 13 a **15** e aggiunto il primo sottotema; la
v2.1 aggiunge i **marcatori trasversali**, che non toccano i 15. Le versioni
precedenti restano nella storia Git; il diario è in fondo.

Le cinque decisioni aperte sono state prese e sono registrate nella sezione
*Decisioni*, con la conseguenza che ognuna comporta. Sono state prese da un
membro del gruppo per sbloccare il lavoro a valle: restano aperte alla revisione
del gruppo, non allo stallo.

## Perché esiste

`docs/politica-3d.md`, sezione 4, dice due cose:

> Artefatto critico del progetto. […] È il contratto fra i tre layer.
> **Va congelata prima di scrivere qualsiasi trasformazione.**

Non era stata congelata, e le trasformazioni erano state scritte lo stesso. Da lì
veniva il blocco: il topic modeling stava venendo usato per *derivare* la
tassonomia su cui doveva essere mappato. Un NMF non restituisce categorie
politiche — restituisce i gruppi di parole più regolari del corpus, che al primo
giro erano i template delle testate. Aspettare che ne uscisse un'ontologia
significava aspettare una cosa che non può succedere.

Le categorie si decidono dall'alto, da uno standard. I topic ci si mappano sopra.

## Da dove vengono le categorie

Dal **Comparative Manifesto Project / MARPOR**, lo schema con cui i programmi
elettorali sono codificati a mano nella letteratura comparata. Aggancio voluto:
dà un riferimento accademico citabile e rende confrontabile il lavoro con dati
esterni.

MARPOR ha 7 domini e 56 categorie. 56 sono troppe per un corpus di stampa
italiano su sette mesi: molte non compaiono mai e altre si distinguono per una
sfumatura di posizione (*pro* vs *contro* la stessa policy) che un topic model non
vede — l'NMF riconosce di *cosa* si parla, non *come*.

Questa versione tiene i 7 domini MARPOR e li apre in 15 macrotemi, accorpando le
coppie pro/contro. 15 è il limite superiore dell'intervallo 10-15 fissato dal
piano: non c'è spazio per un sedicesimo senza rivedere il piano.

## I 15 macrotemi

Il numero è l'identificativo stabile: è ciò che finisce nei config e nelle
tabelle, e non cambia quando cambia l'etichetta.

| # | Macrotema | Dominio MARPOR | Categorie MARPOR accorpate | Cosa ci sta dentro |
|---|---|---|---|---|
| 1 | Politica estera e difesa | 1 | 101-107 | Alleanze, NATO, guerra, missioni, spesa militare, rapporti bilaterali |
| 2 | Unione europea | 1 | 108/110 | Integrazione, fondi UE, vincoli europei, posizione dell'Italia in UE |
| 3 | Istituzioni e assetto dello Stato | 2 | 201-204, 301-302 | Riforme costituzionali, premierato, autonomia differenziata, rapporti Stato-Regioni, giustizia come ordinamento |
| 4 | Economia e finanza pubblica | 4 | 401-402, 409, 414 | Manovra, debito, tasse, incentivi, mercato, concorrenza |
| 5 | Lavoro e imprese | 4 | 403, 405, 412, 701-702 | Occupazione, salari, contratti, industria, PMI, sindacati |
| 6 | Welfare e pensioni | 5 | 503, 504 (quota) | Assistenza, povertà, previdenza, sostegni al reddito |
| 7 | Sanità | 5 | 504 (quota) | SSN, liste d'attesa, personale sanitario, farmaci |
| 8 | Istruzione e ricerca | 5 | 506/507 | Scuola, università, ricerca, formazione |
| 9 | Ambiente ed energia | 4/5 | 410, 416, 501 | Transizione, rinnovabili, prezzi dell'energia, clima, territorio |
| 10 | Immigrazione e cittadinanza | 6/7 | 601/602, 607/608, 705 | Flussi, accoglienza, rimpatri, cittadinanza, integrazione |
| 11 | Sicurezza e criminalità | 6 | 605 | Ordine pubblico, criminalità organizzata, reati, forze dell'ordine |
| 12 | Diritti civili e società | 6/7 | 603/604, 705-706 | Famiglia, diritti LGBT+, fine vita, parità, libertà individuali |
| 13 | Infrastrutture e territorio | 4/5 | 411, 703 | Trasporti, opere pubbliche, PNRR, aree interne, agricoltura |
| 14 | Cultura e patrimonio | 5 | 502 | Beni culturali, musei, biblioteche, teatro, cinema, editoria, spettacolo |
| 15 | Sport | 5 | 502 (quota) | Impianti, federazioni, pratica sportiva, grandi eventi |

### Sottotemi

Un livello sotto i macrotemi. Non hanno identificativo proprio nella tassonomia
piatta: si scrivono `macrotema.sottotema` e si possono sempre riaccorpare al
padre. Aggiungerne uno non tocca i numeri di sopra.

| # | Sottotema | Padre | Cosa ci sta dentro |
|---|---|---|---|
| 9.1 | Animali e fauna | 9 — Ambiente ed energia | Benessere e tutela degli animali, fauna selvatica, randagismo, attività venatoria |

### Marcatori trasversali

Non sono macrotemi e non competono con loro: **convivono**. Un macrotema dice di
*che cosa* parla un documento, un marcatore dice *come* lo inquadra. Lo stesso
articolo può essere «Immigrazione e cittadinanza» e portare il marcatore `woke`.

Restano fuori dai conteggi per macrotema: aggiungerne uno aggiunge una domanda —
«dove si posa questo modo di parlare?» — non una categoria.

| Marcatore | Cosa segna |
|---|---|
| `woke` | Il frame «woke sì / woke no»: politicamente corretto, cancel culture, ideologia gender. Non una policy, un modo di inquadrare diritti, immigrazione, scuola e linguaggio |

**Perché non è un macrotema, misurato.** Sui 202 articoli del corpus che portano il
frame woke il tema vincente ha **margine mediano 0,40** — il testo pesca da quattro
o cinque lessici e nessuno domina, mentre un macrotema vero sta sopra 0,8. E si
sparpagliano su otto temi: Cultura 52, politica non tematica 31, Immigrazione 29,
Diritti civili 20. Incastrarli in una casella sola butterebbe via l'informazione
interessante, cioè a quali temi il frame si attacca.

**Perché non è `politica non tematica`.** Quella categoria è assenza di policy —
nomine, sondaggi, retroscena. Il woke è il contrario: è policy inquadrata in un
certo modo. Solo 31 articoli su 202 cadono in `politica non tematica` per contenuto
proprio, e quel 15% è un risultato da misurare, non una decisione da prendere prima.

**Limite.** Il marcatore rileva la presenza del frame, non la posizione di chi lo
usa: chi accusa e chi difende finiscono insieme. Coerente con il resto della
tassonomia, che non misura posizione, e da dichiarare ogni volta che il numero
viene citato.

### Categorie di servizio, fuori tassonomia

Non sono temi politici e restano separate, altrimenti inquinano ogni conteggio:

- **`boilerplate`** — testo di struttura editoriale: menu, rilanci, formule
  d'agenzia, paywall. Al primo giro erano 7 topic su 12. Ora li toglie
  `src/pulizia_corpus.py` prima del modello; la categoria resta per i residui.
- **`politica non tematica`** — cronaca politica senza policy: nomine,
  dichiarazioni di posizionamento, sondaggi, retroscena. È politica, non è un tema.
  Misurata: vale il **10,35% della stampa** contro lo 0,55% dei programmi e lo
  0,52% dei progetti di legge. Lo scarto fra i layer è il dato, non la quota da
  sola — vedi `reports/ontologia_mapping/mappatura.md`.
- **`non politico`** — cronaca nera, risultati sportivi, gossip finiti nel corpus
  per omonimia. La riga di confine con i temi 14 e 15 è la policy: il finanziamento
  di un teatro è 14, la recensione dello spettacolo no; la legge sugli impianti
  sportivi è 15, la cronaca della partita no.
- **`dubbio`** — le evidenze non bastano.

## Come si applica ai tre layer

Il senso di un'ontologia condivisa è che la stessa misura giri su corpus diversi.
Le tre superfici non sono uguali e la mappatura non è la stessa operazione.

| Layer | Cosa contiene | Unità di misura | Come si assegna il tema |
|---|---|---|---|
| 1 — cosa dicono | Programmi elettorali (60 documenti, 2018 e 2022) | **Paragrafo** (decisione 3) | Un tema per paragrafo; il programma esce come distribuzione sui 15 temi, non come etichetta |
| 2 — cosa fanno | Progetti di legge Camera (6.865, leg. 18-19) | Atto (titolo, mediana 161 caratteri) | Un DDL ha un oggetto: etichetta singola |
| 3 — come se ne parla | Articoli di stampa (96.345 record) | Articolo (mediana ~2.800 caratteri) | Etichetta dominante più distribuzione |

**Questa tabella è il contenuto vero del contratto.** Le 15 categorie sono la
parte facile; la parte che rompe le pipeline è che "assegnare un tema" vuol dire
tre cose diverse nei tre layer, e finché non è scritto ognuno assume la propria.

### Conseguenza: si confrontano quote, mai conteggi

Le tre unità hanno dimensioni diverse di ordini di grandezza — un paragrafo, un
titolo di legge, un articolo. Un conteggio grezzo fra layer non significa niente.

Ogni confronto fra layer si fa su **quote entro il corpus di quel partito in quel
layer**: la percentuale di paragrafi del programma sul tema *X* contro la
percentuale dei suoi DDL sul tema *X*. L'indice di coerenza programmatica (H1) è
la distanza fra due distribuzioni, non fra due numeri.

## Decisioni

Le prime quattro sono del 2026-08-20, la quinta del 2026-08-27. Ognuna porta una
conseguenza che va dichiarata nei limiti del lavoro, ed è scritta qui perché non
venga persa.

### 1. La sanità è un macrotema separato dal welfare

**Decisione: separata.** Tema 7, distinto dal tema 6.

Motivo: nel discorso pubblico italiano la sanità ha volume e autonomia propri, e
accorparla al welfare renderebbe illeggibile uno dei temi più presenti.

**Conseguenza da dichiarare.** MARPOR tiene la sanità dentro la categoria 504,
insieme al welfare. Il confronto con MARPOR su questo punto **non è diretto**: per
qualsiasi validazione esterna che tocchi il welfare, i temi 6 e 7 vanno
ri-accorpati prima del confronto.

### 2. L'immigrazione è un macrotema unico

**Decisione: un tema solo.** Tema 10.

Motivo: tenere unita la materia mantiene i volumi leggibili e non richiede
annotazione umana per assegnare il framing.

**Conseguenza da dichiarare.** MARPOR distingue 601 e 602, cioè chi tratta
l'immigrazione come questione di sicurezza e chi come questione di diritti.
Accorpando, quella distinzione **non è misurata**. Resta recuperabile in seguito
come sottotema del 10 senza rompere la tassonomia: gli identificativi non cambiano.

### 3. Il layer 1 si segmenta per paragrafo

**Decisione: paragrafo.** Non capitolo, non frase.

Motivo: i capitoli sono scelti dal partito, quindi un capitolo del PD e uno della
Lega non sono la stessa unità e i numeri non sono confrontabili fra partiti — ed è
il confronto fra partiti l'obiettivo del progetto. Il paragrafo è l'unità
confrontabile più grande, quindi il miglior compromesso fra rumore e significato,
e sopravvive all'OCR meglio della frase: il riconoscimento sbaglia spesso la
punteggiatura, molto più raramente gli a capo.

**Conseguenze da dichiarare.**

- Si misura **quanto testo** un partito spende su un tema, non che cosa mette in
  vetrina. La struttura dei capitoli, che è una scelta comunicativa e
  un'informazione vera, non entra nella misura.
- I paragrafi corti e privi di contenuto ("serve un cambio di passo") vanno
  scartati con una soglia minima di caratteri, dichiarata insieme al risultato.
- 45 dei 60 programmi vengono dall'OCR e portano `estrazione: "ocr"`: la
  segmentazione lavora su un testo riconosciuto, non depositato. La distinzione è
  già nei dati e va riportata nei risultati.

### 4. La validazione esterna si fa contro MARPOR, dove esiste

**Decisione: verificata la copertura.** Esiste per il 2018, non per il 2022.

Verifica sulle release notes ufficiali del Manifesto Project, versioni
2011a→2025a (ultima aprile 2025). Le elezioni italiane codificate sono **2001,
2008, 2013, 2018**. L'aggiunta del 2018 è esplicita — *«MARPOR Full Dataset
2019a: July 2019 — Elections added: … Italy 2018»*. Il 2022 non compare né fra le
elezioni aggiunte nelle versioni 2022a, 2023a, 2024a, 2025a, né come codice
partito (`32xxx_2022xx`: nessuna occorrenza).

**Conseguenze da dichiarare.**

- I **34 programmi del 2018** sono validabili contro una codifica manuale
  accademica; i **26 del 2022** no.
- MARPOR codifica i partiti che hanno ottenuto seggi, non tutte le liste
  depositate: la validazione copre realisticamente 8-10 documenti del 2018, non
  tutti e 34.
- Dove la validazione non è possibile resta il solo controllo interno, e va detto
  che su quella parte la tassonomia non è verificata contro uno standard.

Fonti: <https://manifesto-project.wzb.eu/datasets> ·
<https://manifesto-project.wzb.eu/down/data/2025a/codebooks/release_notes_MPDS2025a.pdf>

### 5. Cultura e sport diventano macrotemi, gli animali un sottotema

Presa il 2026-08-27. È la decisione che porta la v2.0.

**Decisione: cultura → 14, sport → 15, animali → sottotema 9.1.**

Motivo: la prima mappatura dei tre layer (`reports/ontologia_mapping/`) non aveva
una casella per nessuna delle tre materie, e le aveva parcheggiate nel 12 e nel
13. Misurate sul testo, non sono residuali — quota di unità che nominano la
materia:

| Materia | DDL Camera | Paragrafi di programma |
|---|---|---|
| Cultura | 3,58% | 7,55% |
| Animali | 2,78% | 2,83% |
| Sport | 1,86% | 1,53% |

Il termine di paragone sono i macrotemi già in tassonomia: *Unione europea* vale
l'1,59% dei DDL, *Immigrazione e cittadinanza* l'1,68%, *Welfare e pensioni* il
2,46%. Tutte e tre le materie stanno sopra il più piccolo dei 13, e gli animali
sopra l'immigrazione. Tenerle spalmate su 12 e 13 gonfiava quei due e nascondeva
tre temi veri.

Cultura e sport salgono a macrotema perché in MARPOR hanno un codice proprio, la
502, e reggono da soli. Gli animali restano sottotema perché MARPOR li tiene
sotto la 501 ambientale: promuoverli romperebbe l'aggancio allo standard, che è
la ragione per cui le categorie vengono da MARPOR e non da noi.

**Conseguenze da dichiarare.**

- La v1.0 è stata in vigore sette giorni e l'unica cosa scritta contro di essa era
  `src/mappa_ontologia.py`. Il costo della rilettura è quello, e la finestra per
  farlo a costo quasi nullo è questa.
- MARPOR mette cultura e sport nella stessa categoria 502. Separandoli, il
  confronto con MARPOR su questo punto **non è diretto**: per una validazione
  esterna i temi 14 e 15 vanno ri-accorpati prima del confronto, come già vale per
  6 e 7 sul welfare.
- 15 è il tetto dell'intervallo fissato dal piano. Un sedicesimo macrotema
  richiede prima di rivedere il piano.

## Cosa questa tassonomia non fa

- Non misura **posizione**: dice di cosa si parla, non se a favore o contro.
  Accorpare le coppie MARPOR pro/contro è la scelta che lo rende esplicito.
- Non misura **consenso**. Il volume di copertura di un tema non è sostegno.
- Non misura **sentiment**, che il piano ha già declassato a modulo accessorio.
- Non è un'ontologia formale (nessun OWL, nessuna gerarchia inferenziale): è una
  tassonomia a 15 voci, più un livello di sottotemi e 4 categorie di servizio.

## Come si cambia

Gli identificativi già assegnati sono stabili: 1-13 non si sono mossi passando
alla v2.0, e non si muoveranno più.

Aggiungere un **sottotema** — per esempio spaccare il 10 nelle due letture MARPOR
— non rompe niente e non richiede un cambio di versione maggiore: si aggiunge un
livello sotto, i numeri restano.

Aggiungere un **macrotema** in coda, come hanno fatto il 14 e il 15, non
rinumera niente ma cambia il denominatore di ogni quota già calcolata: chiede una
versione maggiore e la riesecuzione delle mappature, non la loro riscrittura.

Accorpare, togliere o rinumerare è la cosa cara, e obbliga a rileggere tutto ciò
che è stato mappato con la versione precedente.

## Diario delle versioni

| Versione | Data | Cosa cambia |
|---|---|---|
| v1.0 | 2026-08-20 | Prima versione congelata: 13 macrotemi da MARPOR, decisioni 1-4 |
| v2.0 | 2026-08-27 | Aggiunti i macrotemi 14 (Cultura e patrimonio) e 15 (Sport); aggiunto il sottotema 9.1 (Animali e fauna); decisione 5 |
| v2.1 | 2026-08-28 | Aggiunto il livello dei **marcatori trasversali**, e il primo marcatore (`woke`). I 15 macrotemi non si toccano: un marcatore convive con il tema invece di sostituirlo |
