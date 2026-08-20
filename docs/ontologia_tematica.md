# Ontologia tematica — v1.0, congelata

**Stato: congelata il 2026-08-20.** È il contratto fra i tre layer. Da qui in
avanti le trasformazioni si scrivono contro questa versione; cambiarla richiede
una v1.1 e la rilettura di ciò che ne dipende.

Le quattro decisioni aperte nella bozza v0 sono state prese e sono registrate
nella sezione *Decisioni*, con la conseguenza che ognuna comporta. Sono state
prese da un membro del gruppo per sbloccare il lavoro a valle: restano aperte
alla revisione del gruppo, non allo stallo.

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

Questa versione tiene i 7 domini MARPOR e li apre in 13 macrotemi, accorpando le
coppie pro/contro. 13 sta nell'intervallo 10-15 fissato dal piano.

## I 13 macrotemi

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

### Categorie di servizio, fuori tassonomia

Non sono temi politici e restano separate, altrimenti inquinano ogni conteggio:

- **`boilerplate`** — testo di struttura editoriale: menu, rilanci, formule
  d'agenzia, paywall. Al primo giro erano 7 topic su 12. Ora li toglie
  `src/pulizia_corpus.py` prima del modello; la categoria resta per i residui.
- **`politica non tematica`** — cronaca politica senza policy: nomine,
  dichiarazioni di posizionamento, sondaggi, retroscena. È politica, non è un tema.
- **`non politico`** — cronaca, sport, spettacolo finiti nel corpus per omonimia.
- **`dubbio`** — le evidenze non bastano.

## Come si applica ai tre layer

Il senso di un'ontologia condivisa è che la stessa misura giri su corpus diversi.
Le tre superfici non sono uguali e la mappatura non è la stessa operazione.

| Layer | Cosa contiene | Unità di misura | Come si assegna il tema |
|---|---|---|---|
| 1 — cosa dicono | Programmi elettorali (60 documenti, 2018 e 2022) | **Paragrafo** (decisione 3) | Un tema per paragrafo; il programma esce come distribuzione sui 13 temi, non come etichetta |
| 2 — cosa fanno | Progetti di legge Camera (6.865, leg. 18-19) | Atto (titolo, mediana 161 caratteri) | Un DDL ha un oggetto: etichetta singola |
| 3 — come se ne parla | Articoli di stampa (96.345 record) | Articolo (mediana ~2.800 caratteri) | Etichetta dominante più distribuzione |

**Questa tabella è il contenuto vero del contratto.** Le 13 categorie sono la
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

Prese il 2026-08-20. Ognuna porta una conseguenza che va dichiarata nei limiti
del lavoro, ed è scritta qui perché non venga persa.

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

## Cosa questa tassonomia non fa

- Non misura **posizione**: dice di cosa si parla, non se a favore o contro.
  Accorpare le coppie MARPOR pro/contro è la scelta che lo rende esplicito.
- Non misura **consenso**. Il volume di copertura di un tema non è sostegno.
- Non misura **sentiment**, che il piano ha già declassato a modulo accessorio.
- Non è un'ontologia formale (nessun OWL, nessuna gerarchia inferenziale): è una
  tassonomia piatta a 13 voci più 4 categorie di servizio.

## Come si cambia

I 13 identificativi sono stabili. Aggiungere un sottotema — per esempio spaccare
il 10 nelle due letture MARPOR — non rompe niente e non richiede una v2: si
aggiunge un livello sotto, i numeri restano.

Cambiare l'insieme dei 13, cioè accorpare, togliere o rinumerare, è una v2, e
obbliga a rileggere tutto ciò che è stato mappato con la v1.
