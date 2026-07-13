# Istruzioni per Codex — progetto AIDA temi-politici

## 1. Contesto del progetto

Questo repository contiene un progetto universitario del Master AIDA dedicato
all’analisi data-driven dei temi politici italiani.

La pipeline attualmente sviluppata riguarda principalmente la copertura mediatica
della politica attraverso articoli raccolti con Media Cloud.

I principali componenti del repository sono:

- `src/mediacloud_spike.py`: discovery degli URL;
- `src/mediacloud_fulltext.py`: acquisizione e pulizia del testo completo;
- `src/harvester.py`: download ed estrazione delle pagine;
- `src/news_topic_model.py`: baseline TF-IDF + NMF;
- `src/drive_mirror.py`: copia atomica degli output nel mirror locale di Google Drive;
- `notebooks/00_esegui_pipeline.ipynb`: orchestrazione didattica della pipeline;
- `notebooks/classificatore.ipynb`: documentazione metodologica;
- `scripts/run_overnight_pipeline.sh`: esecuzione sequenziale della pipeline.

Questa descrizione deriva dal brief utente e deve essere verificata sui file
effettivamente presenti nel repository.

## 2. Visione del progetto

La visione futura può essere descritta attraverso tre layer:

1. **Cosa dicono**
   - programmi elettorali;
   - siti ufficiali;
   - comunicati;
   - contenuti diretti dei partiti.

2. **Cosa fanno**
   - proposte e disegni di legge;
   - votazioni;
   - interrogazioni;
   - mozioni;
   - risoluzioni;
   - emendamenti;
   - interventi parlamentari;
   - attività istituzionale e di governo.

3. **Come vengono raccontati**
   - copertura mediatica;
   - temi associati ai partiti;
   - variazioni temporali dell’attenzione della stampa.

Attualmente il corpus Media Cloud rappresenta soltanto il terzo layer:
**come vengono raccontati**.

Non deve essere interpretato automaticamente come misura di:

- comunicazione diretta dei partiti;
- attività legislativa;
- consenso elettorale;
- posizionamento politico;
- stance verso una policy;
- opinione pubblica complessiva.

## 3. Obiettivo della fase attuale

L’obiettivo della fase corrente è costruire dal corpus stampa una:

> tassonomia candidata dei macrotemi politici emergenti.

La tassonomia deve essere scoperta in modo data-driven e successivamente
validata dal gruppo.

Il percorso previsto è:

1. verificare qualità e struttura degli output esistenti;
2. controllare i topic NMF già prodotti;
3. identificare boilerplate, agenzie, nomi di testate, menu, navigazione e altri
   artefatti editoriali;
4. migliorare la qualità dei topic;
5. interpretare circa 15–20 microtemi emergenti;
6. aggregare i microtemi in macrotemi candidati;
7. confrontare soluzioni di sintesi da 3, 4 e 5 macrotemi;
8. sottoporre i risultati a validazione umana;
9. produrre una tassonomia candidata;
10. scegliere successivamente quali macrotemi mantenere nel prosieguo.

La tassonomia prodotta in questa fase non è ancora l’ontologia definitiva
applicabile automaticamente a tutti i futuri layer.

## 4. Distinzioni metodologiche obbligatorie

Mantenere sempre distinti:

- **microtema emergente**:
  argomento granulare scoperto dal modello;

- **macrotema candidato**:
  aggregazione interpretabile di più microtemi;

- **macrotema selezionato**:
  tema scelto dal gruppo per le fasi successive;

- **ontologia multi-layer**:
  futura struttura comune da validare anche su programmi, siti e attività
  istituzionale;

- **salienza**:
  quantità di attenzione ricevuta da un tema;

- **sentiment o tono**:
  polarità generale del testo;

- **stance o posizionamento**:
  orientamento verso una policy, un soggetto o una proposta;

- **comportamento osservato**:
  attività legislativa o istituzionale documentabile.

Il sentiment generale di un articolo non deve essere interpretato come:

- giudizio verso un partito;
- posizione su una policy;
- consenso;
- coerenza programmatica.

## 5. Interpretazione del corpus Media Cloud

Il corpus Media Cloud è stato costruito tramite query su partiti e leader.

Di conseguenza:

- non rappresenta l’intero ecosistema informativo italiano;
- non misura la presenza dei partiti su tutta la stampa;
- un articolo può menzionare più partiti;
- le percentuali associate ai partiti non devono necessariamente sommare a 100%;
- la tabella di copertura per partito è un controllo della raccolta;
- i conteggi grezzi non sono il risultato principale del progetto.

La copertura per partito può essere usata per verificare:

- qualità delle query;
- bilanciamento del campione;
- presenza di omonimie;
- problemi come la parola “Lega” usata in ambito sportivo;
- fonti dominate da aggregatori o agenzie.

## 6. Regola di verificabilità

Per ogni affermazione usare una delle seguenti etichette:

- `CONFERMATO DAL REPOSITORY`
- `CONFERMATO DAL BRIEF UTENTE`
- `PROPOSTA DA VALIDARE`
- `NON VERIFICABILE`

Quando un’affermazione deriva dal repository, indicare:

- file;
- funzione, variabile o sezione rilevante;
- eventuale output osservato.

Non inventare:

- nomi di progetto;
- ipotesi di ricerca;
- risultati;
- decisioni;
- file;
- percorsi;
- metriche;
- requisiti.

Se un’informazione non è disponibile, dichiararla come `NON VERIFICABILE`.

## 7. Nome del progetto

Non usare nomi di progetto non confermati.

In assenza di un nome ufficialmente approvato, usare:

- `progetto temi-politici`;
- oppure `progetto AIDA sui temi politici`.

Il nome “Politica 3D” può essere utilizzato soltanto se:

- compare realmente nel repository;
- oppure viene esplicitamente approvato dall’utente.

## 8. Modalità di lavoro per milestone

Procedere con una sola milestone alla volta.

Non eseguire più milestone nella stessa risposta.

Per ogni milestone:

1. dichiarare l’obiettivo;
2. indicare file e dati interessati;
3. descrivere le attività previste;
4. eseguire soltanto le attività della milestone;
5. fermarsi;
6. spiegare in termini semplici cosa è stato fatto;
7. mostrare risultati verificabili;
8. proporre un human check limitato e concreto;
9. indicare criteri di accettazione;
10. segnalare problemi e limiti;
11. descrivere brevemente la milestone successiva;
12. chiedere esplicitamente autorizzazione prima di proseguire.

Non iniziare automaticamente la milestone successiva.

Una risposta come:

- “ok”;
- “approvo”;
- “procedi”;
- “passa alla fase successiva”;

costituisce autorizzazione.

In assenza di approvazione esplicita, fermarsi.

## 9. Formato obbligatorio di chiusura delle milestone

Al termine di ogni milestone usare sempre queste sezioni:

## Milestone completata

Numero e nome della milestone.

## Obiettivo

Spiegazione semplice, massimo 3–4 righe.

## Cosa è stato fatto

Elenco delle operazioni realmente eseguite.

Per ogni modifica indicare:

- file interessato;
- tipo di modifica;
- motivo;
- output prodotto.

## Risultati raggiunti

Mostrare:

- numeri;
- tabelle sintetiche;
- percorsi;
- file;
- output;
- anomalie osservate.

Distinguere sempre:

- risultato verificato;
- interpretazione;
- ipotesi;
- elemento ancora da validare.

## Come leggere i risultati

Spiegare:

- cosa significano;
- cosa non significano;
- quali conclusioni sono ammesse;
- quali conclusioni non sono supportate.

## Human check richiesto

Indicare controlli concreti e limitati, per esempio:

- file da aprire;
- colonne da osservare;
- numero di righe da campionare;
- articoli rappresentativi da leggere;
- termini da controllare;
- topic sospetti;
- grafici o tabelle da confrontare.

Non chiedere di controllare manualmente migliaia di record.

Quando serve una revisione dei topic, preparare un campione gestibile con:

- parole principali;
- 5–10 articoli rappresentativi;
- fonti prevalenti;
- distribuzione temporale;
- casi a bassa chiarezza;
- possibili artefatti.

## Criteri di accettazione

Elencare le condizioni necessarie per considerare approvata la milestone.

## Problemi e limiti

Indicare:

- anomalie;
- bias;
- dati mancanti;
- decisioni aperte;
- rischi di interpretazione.

## Prossima milestone proposta

Spiegare brevemente:

- cosa farà;
- perché è necessaria;
- quali file leggerà o modificherà;
- quali output dovrebbe produrre.

## Richiesta di autorizzazione

Concludere sempre con:

> Approvi questa milestone e posso procedere con la milestone successiva?

## 10. Sequenza iniziale delle milestone

### Milestone 0 — Verifica dello stato reale

- controllare root del repository;
- controllare branch;
- controllare `git status`;
- distinguere file tracciati, ignorati, locali ed esterni;
- verificare esistenza e leggibilità degli output;
- non modificare nulla.

### Milestone 1 — Audit degli output NMF esistenti

- leggere `news_topic_review.csv`;
- leggere `news_topic_terms.csv`;
- leggere `topic_model_metadata.json`;
- verificare parametri, topic, pesi e dimensioni;
- non modificare ancora il modello.

### Milestone 2 — Human check dei topic

- preparare parole principali;
- preparare articoli rappresentativi;
- distinguere temi politici da boilerplate;
- creare una tabella di revisione gestibile.

### Milestone 3 — Regole di pulizia

- individuare stopword aggiuntive;
- identificare nomi di testate e agenzie;
- riconoscere menu, navigazione e boilerplate;
- proporre modifiche senza applicarle automaticamente.

### Milestone 4 — Nuova esecuzione controllata

- applicare solo le regole approvate;
- rieseguire TF-IDF + NMF;
- confrontare prima e dopo;
- verificare se interpretabilità e qualità migliorano.

### Milestone 5 — Validazione dei microtemi

- interpretare circa 15–20 microtemi;
- controllare volume, distintività e persistenza;
- assegnare etichette provvisorie;
- sottoporre i risultati al gruppo.

### Milestone 6 — Aggregazione in macrotemi candidati

- raggruppare gerarchicamente i microtemi;
- confrontare soluzioni da 3, 4 e 5 macrotemi;
- non scegliere automaticamente una soluzione sulla base di una sola metrica.

### Milestone 7 — Tassonomia candidata

- produrre un insieme motivato di macrotemi candidati;
- descrivere sottotemi, evidenze, copertura e limiti;
- non definirli ancora ontologia definitiva multi-layer.

### Milestone 8 — Selezione per il prosieguo

- aiutare il gruppo a scegliere i macrotemi da mantenere;
- valutare rilevanza, persistenza, interpretabilità e utilità decisionale;
- documentare inclusioni, esclusioni e motivazioni.

## 11. Regole sulle modifiche

Prima di modificare un file, indicare:

- file da modificare;
- contenuto da cambiare;
- motivo;
- output atteso;
- possibilità di rollback.

Durante una milestone modificare soltanto i file strettamente necessari.

Non modificare file estranei alla milestone.

Non:

- cambiare branch;
- aggiungere file allo staging;
- creare commit;
- eseguire push;
- fare merge;
- aprire pull request;
- riscrivere l’architettura;
- introdurre BERTopic;
- aggiungere nuovi layer;
- rilanciare tutta la pipeline;

senza approvazione esplicita.

## 12. Stato Git

Prima di iniziare una milestone che prevede modifiche, controllare:

- branch corrente;
- `git status`;
- file modificati;
- file non tracciati;
- file ignorati.

Non alterare lo stato Git senza autorizzazione.

Le modifiche locali già presenti non devono essere sovrascritte.

## 13. Limiti di accesso al filesystem

Lavorare esclusivamente dentro la root del repository aperto.

Non:

- esplorare ricorsivamente la home directory;
- accedere a `~/Library`;
- accedere a Music;
- accedere a Photos;
- accedere a Mail;
- accedere a Messages;
- accedere ai dati di altre applicazioni;
- usare `find`, `rg` o `mdfind` sopra la root del repository;
- cercare file nell’intero disco;
- richiedere Accesso completo al disco;
- richiedere accesso ad Apple Music;
- richiedere accesso ai dati di altre app.

Il file `.drive-export-dir` può essere letto soltanto per verificare che contenga
un percorso.

Prima di accedere al mirror Google Drive:

1. mostrare all’utente il percorso esatto;
2. indicare i file specifici da leggere;
3. spiegare perché sono necessari;
4. chiedere autorizzazione esplicita.

Non esplorare ricorsivamente l’intero Google Drive.

## 14. Gestione dei file di grandi dimensioni

Non caricare integralmente in memoria file JSONL di grandi dimensioni senza
necessità e senza autorizzazione.

Per una verifica preliminare usare soltanto:

- dimensione del file;
- numero di righe con lettura streaming;
- prima riga valida;
- schema dei campi;
- piccolo campione;
- conteggi aggregati strettamente necessari.

Non stampare grandi quantità di testo o interi articoli nel terminale o nella chat.

## 15. Dipendenze e strumenti

Non aggiungere dipendenze Python senza:

1. spiegare perché servono;
2. verificare se esiste già una dipendenza equivalente;
3. indicare l’impatto su `requirements.txt`;
4. chiedere approvazione.

Per la baseline attuale privilegiare:

- Python;
- pandas;
- scikit-learn;
- TF-IDF;
- NMF;
- clustering gerarchico;
- metriche semplici e spiegabili.

BERTopic e modelli più complessi possono essere considerati soltanto in una fase
successiva e dopo approvazione.

## 16. Linguaggio e spiegazioni

Scrivere in italiano semplice.

Il gruppo ha background diversi:

- data analysis;
- statistica;
- project management;
- SEO;
- giornalismo.

Quando si usano concetti tecnici come:

- TF-IDF;
- NMF;
- peso del topic;
- clustering;
- silhouette;
- stabilità;
- distanza coseno;
- distribuzione normalizzata;

spiegare sempre:

1. cosa sono;
2. a quale domanda rispondono;
3. quale output producono;
4. quali limiti hanno;
5. come possono essere controllati da una persona.

Il risultato di ogni milestone deve essere comprensibile anche senza leggere
tutto il codice.

## 17. Priorità attuale

La priorità attuale non è creare nuovo codice.

La priorità è:

1. verificare gli output già prodotti;
2. capire la qualità dei topic;
3. identificare il boilerplate;
4. preparare un human check;
5. migliorare gradualmente la tassonomia emergente.

Non anticipare la selezione definitiva dei macrotemi.

## 18. Riproducibilità e auditabilità obbligatorie

Questo repository è un progetto software e data science destinato alla
valutazione accademica e alla pubblicazione su GitHub.

Ogni risultato deve essere riproducibile e auditabile da:

- membri del team;
- docenti;
- revisori esterni;
- futuri lettori del repository.

### Regola fondamentale

Nessun risultato analitico può essere prodotto o presentato prima che il codice
che lo genera sia stato salvato nel repository.

La sequenza obbligatoria è:

1. definire l’obiettivo;
2. indicare i file da creare o modificare;
3. scrivere il codice nel repository;
4. aggiungere o aggiornare i test;
5. mostrare il comando di esecuzione;
6. eseguire il codice salvato;
7. generare output persistenti;
8. verificare gli output;
9. riassumere i risultati nella risposta.

### Attività vietate

È vietato produrre risultati di progetto tramite:

- codice Python temporaneo non salvato;
- `python -c`;
- heredoc Python eseguiti nel terminale;
- REPL o console interattive;
- script scratch esterni al repository;
- celle temporanee non salvate;
- calcoli manuali non documentati;
- analisi eseguite soltanto nella sessione interna di Codex;
- comandi ad hoc non trasformati in codice permanente.

I comandi del terminale possono essere usati direttamente soltanto per:

- `git status`;
- `git diff`;
- controllo del branch;
- elenco dei file;
- esecuzione di script già salvati;
- esecuzione dei test;
- controllo degli output generati.

### Tracciabilità dei risultati

Ogni risultato deve indicare:

- input utilizzato;
- codice che lo produce;
- configurazione utilizzata;
- comando di esecuzione;
- output generato;
- test o controllo effettuato;
- eventuale seed casuale;
- limiti del risultato.

Un risultato privo di questa catena deve essere classificato come:

`PROVVISORIO — NON RIPRODUCIBILE`

e non può chiudere una milestone.

### Separazione delle responsabilità

- `src/` contiene la logica riutilizzabile;
- `scripts/` contiene i punti di esecuzione;
- `notebooks/` contiene spiegazioni, visualizzazioni e chiamate alle funzioni;
- `config/` contiene i parametri espliciti;
- `tests/` contiene test automatici e fixture sintetiche;
- `reports/` contiene output piccoli e verificabili;
- `docs/` contiene provenienza dei dati e istruzioni di riproduzione.

Il notebook non deve duplicare la logica presente in `src/`.

### Notebook

Ogni notebook deve:

- partire da kernel pulito;
- essere eseguibile dall’inizio alla fine;
- evitare dipendenze da variabili create manualmente;
- usare percorsi relativi;
- importare la logica da `src/`;
- mostrare soltanto output sintetici;
- spiegare cosa significano e cosa non significano i risultati.

### Dati grandi e dati non pubblicabili

La riproducibilità non richiede di pubblicare su GitHub l’intero corpus.

Per dati grandi, protetti o soggetti a limiti di redistribuzione devono essere
forniti:

- script di acquisizione;
- parametri delle query;
- intervallo temporale;
- schema dei dati;
- conteggi;
- hash degli input;
- manifest del run;
- piccolo campione pubblicabile;
- fixture sintetiche per i test.

### Codice generato da Codex

Ogni modifica proposta da Codex deve essere visibile nel repository.

Codex deve sempre indicare:

- file creati;
- file modificati;
- funzioni aggiunte;
- comandi eseguiti;
- test eseguiti;
- output prodotti.

Non deve presentare come risultato ufficiale alcun calcolo effettuato soltanto
nella propria sessione interna.