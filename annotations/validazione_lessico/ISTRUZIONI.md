# Validazione dei macrotemi — istruzioni per R1 e R2

**100 articoli, 30-40 minuti.** Per ognuno decidi di quale tema parla.

Serve a controllare se il classificatore automatico ci azzecca. Finora nessuno
gliel'ha mai verificato: tutti i numeri del progetto poggiano su regole scritte
a mano e mai controllate contro qualcuno che abbia letto gli articoli.

## Cosa devi fare

Apri il tuo file — `revisore_R1.csv` o `revisore_R2.csv` — con Excel o Fogli
Google. Per ogni riga compili quattro colonne, le ultime quattro:

| Colonna | Cosa scrivere |
|---|---|
| `macrotema` | **Uno** dei 15 temi qui sotto, oppure una categoria di servizio |
| `macrotema_secondario` | Solo se l'articolo tratta davvero due temi. Altrimenti vuoto |
| `frame_woke` | `sì` se compare il discorso woke / politicamente corretto / cancel culture, `no` altrimenti |
| `note` | Facoltativo. Utile soprattutto quando scrivi `dubbio` |

Scrivi il **nome del tema**, non il numero.

## Le tre regole che rendono valido il lavoro

**Non cercare la risposta del programma.** Il tuo file non la contiene, ed è
voluto: se sapessi cosa ha deciso la macchina non staresti validando, staresti
confermando.

**Le prime 10 righe insieme, il resto da solo.** Le righe marcate
`calibrazione` si fanno insieme all'altro revisore per allinearsi sui criteri.
Dalla riga 11 in poi — marcate `indipendente` — ognuno lavora per conto suo,
senza consultarsi e senza guardare il file dell'altro. Il disaccordo fra voi due
è un dato che serve: se non andate d'accordo voi, non è colpa del programma, sono
le categorie a non funzionare, ed è meglio saperlo adesso.

**Giudica di cosa parla, non se è scritto bene o se sei d'accordo.** E non
andare oltre quello che leggi: se titolo ed estratto non bastano, la risposta
giusta è `dubbio`. Un `dubbio` è informazione, una risposta tirata a indovinare
è rumore.

## I 15 macrotemi

| Tema | Ci sta dentro |
|---|---|
| **Politica estera e difesa** | Alleanze, NATO, guerra, missioni, spesa militare, rapporti bilaterali |
| **Unione europea** | Integrazione, fondi UE, vincoli europei, posizione dell'Italia in UE |
| **Istituzioni e assetto dello Stato** | Riforme costituzionali, premierato, autonomia differenziata, rapporti Stato-Regioni, giustizia come ordinamento |
| **Economia e finanza pubblica** | Manovra, debito, tasse, incentivi, mercato, concorrenza |
| **Lavoro e imprese** | Occupazione, salari, contratti, industria, PMI, sindacati |
| **Welfare e pensioni** | Assistenza, povertà, previdenza, sostegni al reddito |
| **Sanità** | SSN, liste d'attesa, personale sanitario, farmaci |
| **Istruzione e ricerca** | Scuola, università, ricerca, formazione |
| **Ambiente ed energia** | Transizione, rinnovabili, prezzi dell'energia, clima, territorio |
| **Immigrazione e cittadinanza** | Flussi, accoglienza, rimpatri, cittadinanza, integrazione |
| **Sicurezza e criminalità** | Ordine pubblico, criminalità organizzata, reati, forze dell'ordine |
| **Diritti civili e società** | Famiglia, diritti LGBT+, fine vita, parità, libertà individuali |
| **Infrastrutture e territorio** | Trasporti, opere pubbliche, PNRR, aree interne, agricoltura |
| **Cultura e patrimonio** | Beni culturali, musei, biblioteche, teatro, cinema, editoria, spettacolo |
| **Sport** | Impianti, federazioni, pratica sportiva, grandi eventi |

## Le categorie di servizio

Da usare quando nessuno dei 15 va bene:

- **politica non tematica** — è politica ma non c'è una policy: nomine, rimpasti,
  sondaggi, candidature, retroscena, chi sale e chi scende;
- **non politico** — cronaca nera, risultati sportivi, gossip, necrologi. Finito
  nel corpus per omonimia;
- **boilerplate** — non è un articolo: menu, rilanci, formule d'agenzia, testo di
  struttura del sito;
- **dubbio** — titolo ed estratto non bastano per decidere.

Il confine fra *Cultura* e *non politico*: il finanziamento di un teatro è
cultura, la recensione dello spettacolo no. Fra *Sport* e *non politico*: la
legge sugli impianti è sport, la cronaca della partita no.

## Quando finisci

Rimanda il file senza rinominarlo e senza toccare le colonne che non sono le tue
quattro. Il confronto fra i due file è automatico.

---

## I 100 articoli

Sono qui per poterli leggere anche fuori dal foglio di calcolo. Le risposte però
vanno scritte **nel CSV**, non qui.

### V001 · calibrazione

**Per il Comala si mobilitano anche i social: Grimaldi (Avs) attacca il Comune - La Stampa**

*lastampa.it · 2026-02-21*

Â«I locali di corso Ferrucci devono mantenere la loro principale vocazione di centro giovanile e non diventare sede di start up e dâimpresa. Questa vicenda ci insegna ancora una volta che gli spazi della cittÃ non si possono governare solo con bandi e regolamenti. Questa storia non Ã¨ ancora finitaÂ». A difendere il Comala cosÃ¬ come Torino lo conosce Ã¨ Marco Grimaldi, deputato di Avs. BenchÃ© la sua stessa forza politica sieda nella giunta e nella maggioranza di Lo Russo, sindaco con il quale

### V002 · calibrazione

**Voto di scambio, consigliere regionale e sindaco indagati nel Casertano**

*ilmattino.it · 2026-01-23*

Nuovi guai giudiziari per il consigliere regionale di Forza Italia Giovanni Zannini, cui la Procura della Repubblica di Santa Maria Capua Vetere (Caserta) ha notificato tramite i carabinieri un avviso di conclusione indagini per voto di scambio in relazione alle elezioni comunali tenutesi a Castel Volturno (Caserta) nel giugno 2024, quando fu eletto l'attuale sindaco Pasquale Marrandino. L'avviso è stato notificato anche a quest'ultimo, così come al primo cittadino di San Cipriano d'Aversa Vince

### V003 · calibrazione

**Ravenna, la guerra in Iran mette a rischio i cantieri stradali: âPrezzi del bitume alle stelleâ**

*corriereromagna.it · 2026-04-09*

Non solo i carburanti. La guerra in Iran mette a rischio anche i cantieri stradali. Come sottolinea questo pomeriggio in Consiglio comunale lâassessore ai Lavori pubblici del Comune di Ravenna Massimo Cameliani, rispondendo a un question time del Partito democratico sulle tempistiche di asfaltatura di alcune strade del centro, le tensioni internazionali hanno un âeffetto a catenaâ sui prezzi che incide anche sulla pianificazione dei cantieri stradali. Il bitume infatti deriva dal petrolio e âneg

### V004 · calibrazione

**Leva civica senior, Astuti (Pd): "Troppe criticità, serve un confronto urgente"**

*varesenews.it · 2026-04-24*

Leva civica senior, Astuti (Pd): “Troppe criticità, serve un confronto urgente” Il consigliere del Pd critica il mancato coinvolgimento del Terzo Settore nella nuova misura per gli over 65 e chiede un’audizione immediata per chiarire i contenuti della delibera La sperimentazione della “Leva civica lombarda senior”, avviata dalla Giunta regionale lo scorso 13 aprile, finisce al centro del dibattito in Consiglio Regionale. Le opposizioni, guidate dal consigliere varesino del Partito Democratico Sa

### V005 · calibrazione

**Europa e Stati Uniti in rotta di collisione – Avanti**

*avantionline.it · 2026-01-21*

La reale consistenza dei rapporti fra Europa e Stati Uniti sta venendo allo scoperto e solo per questo bisognerebbe dire grazie a Trump rispetto al cinismo delle precedenti amministrazioni che hanno sempre complottato per tenere l’Europa divisa e al guinzaglio nel loro solo ed esclusivo interesse. Con Trump sono maturati i tempi per una generale revisione della piattaforma geostrategica fra Stati Uniti ed Europa che costringerà questa ad una revisione generale dei rapporti e dei trattati all’int

### V006 · calibrazione

**Meloni a Palermo per l’omaggio a Falcone e Borsellino: "Colpiremo chi vuole terrorizzare la città. Forse in campo l’Esercito" - Gazzetta del Sud**

*gazzettadelsud.it · 2026-07-13*

La prima tappa è stata alla Stele di Capaci, il monumento che ricorda la strage in cui persero la vita Giovanni Falcone, la moglie Francesca Morvillo e gli agenti della scorta Rocco Dicillo, Vito Schifani e Antonio Montinari. Giorgia Meloni inizia col tributo alle vittime dell’attentato mafioso la sua giornata a Palermo. Poi, a poche ore dal blitz della dda contro la banda di estortori (22 sono finiti in cella) che per mesi ha terrorizzato commercianti e imprenditori a colpi di kalashnikov, va i

### V007 · calibrazione

**Report, Rai sospende le repliche estive della trasmissione**

*laverita.info · 2026-07-11*

Alla presentazione dei palinsesti Rai, qualche giorno fa ad Ancona, l’amministratore delegato Giampaolo Rossi ha annunciato una prima serata dedicata a San Francesco con Roberto Benigni. C’è chi sussurra che dopo gli sviluppi dell’inchiesta sull’attentato che aveva come bersaglio il vicedirettore ad personam dell’emittente di Stato (dunque stipendiato dal contribuente italiano) ispirandosi al suo film da Oscar, lui abbia proposto un secondo appuntamento: «Lavitola è bella» interprete principale

### V008 · calibrazione

**il manifesto**

*ilmanifesto.it · 2026-02-09*

Takaichi vola alle urne: maggioranza devastante, adesso il Giappone è suo Asia La leader nazionalista governava per 3 voti, ora ne ha 83. La Borsa celebra (+4%), torna anche l’atomo: riaperta megacentrale a 15 anni da Fukushima Asia La leader nazionalista governava per 3 voti, ora ne ha 83. La Borsa celebra (+4%), torna anche l’atomo: riaperta megacentrale a 15 anni da Fukushima «Affronterò questioni irrisolte di enorme portata e renderò il Giappone più forte». Sanae Takaichi ha ora il potere pe

### V009 · calibrazione

**Meloni chiede aiuto a Merz | il manifesto**

*ilmanifesto.it · 2026-04-30*

Meloni chiede aiuto a Merz Bilancio Serve la mediazione tedesca per convincere i “frugali” ad allentare i vincoli di spesa sull’energia. Ma la Germania ha altre priorità Bilancio Serve la mediazione tedesca per convincere i “frugali” ad allentare i vincoli di spesa sull’energia. Ma la Germania ha altre priorità La sfida nella maggioranza sull’ipotesi di uno scostamento di bilancio, che implicherebbe la rottura unilaterale del patto di Stabilità, si conclude solo al fotofinish, con la modifica de

### V010 · calibrazione

**Quanto conta il centro in vista delle Politiche? Il "campo largo" ora si interroga**

*avvenire.it · 2026-06-20*

Quanto conta il centro in vista delle Politiche? Il "campo largo" ora si interroga Venerdì alla festa della Fiom di Bologna nuovo incontro tra i leader di Pd, M5s e Avs. Sullo sfondo restano le grandi manovre per allargare l'offerta politica del centrosinistra, tra ambizioni e veti. Ecco chi c'è nell'area più affollata della politica in questo momento Le nozze di Bologna. Dopo il selfie insieme, Elly Schlein, Giuseppe Conte e Nicola Fratoianni si ritrovano assieme sul palco alla festa della Fiom

### V011 · indipendente

**Il consiglio comunale festeggia 80 anni di democrazia: "Occasione per riflettere"**

*ilrestodelcarlino.it · 2026-03-26*

La storia della democrazia a Modena nasce il 31 marzo 1946, quando per la prima volta in città si vota a suffragio universale per eleggere il Consiglio comunale. È proprio ‘Democrazia’ il filo rosso che lega tutte le iniziative che, dal 31 marzo al 2 giugno, ripercorreranno questi 80 anni di storia e partecipazione democratica. "Rievocando 80 anni di storia democratica a Modena – commenta il sindaco Massimo Mezzetti – emerge il percorso di una città che, uscita distrutta dalla guerra, ha saputo

### V012 · indipendente

**Turista 89enne muore sulla spiaggia di Otranto dopo un malore - Gazzetta del Mezzogiorno**

*lagazzettadelmezzogiorno.it · 2026-08-14*

Un turista bresciano di 89 anni, in vacanza in Salento con la famiglia, ha perso la vita stroncato da un malore mentre era nello specchio d’acqua antistante un lido nella baia di Otranto. Ad accorgersi dell’anziano riverso in mare è stato il bagnino che ha subito lanciato l’allarme. Soccorso e trasportato a riva, ogni tentativo di rianimarlo è risultato vano. Inutili i soccorsi. L'anziano era residente nel Bresciano Venerdì 14 Agosto 2026, 19:15

### V013 · indipendente

**Mozione di FdI per le scuole delle isole veneziane**

*ladige.it · 2026-04-09*

(ANSA) - VENEZIA, 09 APR - La consigliera di FdI in Regione Veneto Laura Besio ha presentato oggi una mozione per impegnare la giunta a promuovere presso il ministero dell'Istruzione il riconoscimento delle isole della laguna di Venezia come aree assimilabili alle piccole isole ai fini dell'applicazione della normativa scolastica. L'obiettivo è ottenere l'estensione alle scuole delle isole veneziane delle misure previste per salvaguardare i servizi scolastici nei territori insulari. Inoltre la m

### V014 · indipendente

**Basi Usa in Italia, da Sigonella a Camp Darby: dove sono e come potrebbero essere usate per la guerra in Iran. La mappa**

*ilgazzettino.it · 2026-03-05*

Mentre i droni di sorveglianza MQ-4C Triton volano da e verso la base di Sigonella, in Sicilia, la premier Giorgia Meloni ribadisce che «sulle basi militari americane «mi pare che tutti si stiano attenendo agli accordi bilaterali». La questione delle basi Usa sul territorio italiano è tornata rilevante dopo l'attacco degli Stati Uniti all'Iran. Le basi Usa sul territorio italiano Sigonella (Sicilia). Da qualche giorno dalla Naval Air Station di Sigonella, principale hub della Us Navy nel Mediter

### V015 · indipendente

**San Siro, il conto che pesa sui milanesi**

*laverita.info · 2026-08-23*

Per capire quanto i milanesi hanno perso nell’operazione stadio, bisogna tornare alle chat di qualche anno fa, contenute nei faldoni delle inchieste sull’urbanistica milanese. Il 5 dicembre 2022 l’ex assessore Giancarlo Tancredi scrive al direttore generale Christian Malangone: «Oggi ho visto Barberis (Pd) che vorrebbe proporre un odg di indirizzo sullo Stadio. […] Che ne dici se ci vediamo lunedì con Bonomi (Giuseppe, presidente di Sport Life City), Mark (Van Huuksloot, all’epoca manager dell’I

### V016 · indipendente

**Ok definitivo al decreto maltempo: dallo stop a tasse e contributi al sostegno al reddito per i lavoratori, ecco le misure - Il Sole 24 ORE**

*ilsole24ore.com · 2026-04-22*

Ok definitivo al decreto maltempo: dallo stop a tasse e contributi al sostegno al reddito per i lavoratori, ecco le misure Il provvedimento riconosce, al ricorrere di determinati presupposti, la sospensione, dal 18 gennaio 2026 al 30 aprile 2026, di taluni termini in materia di adempimenti e versamenti tributari e contributivi ai soggetti che, alla data del 18 gennaio 2026, erano residenti, oppure avevano sede legale od operativa, in immobili danneggiati situati nei comuni interessati dagli even

### V017 · indipendente

**Per Meloni l’ultimo tratto di legislatura è decisivo | Giornale di Brescia**

*giornaledibrescia.it · 2026-07-05*

Giunta all’ultimo miglio della legislatura, Giorgia Meloni si trova di fronte a un bivio cruciale, costretta ancora una volta a reinventare se stessa e la postura del suo governo. Non è una novità assoluta per la leader di Fratelli d’Italia. Già all’indomani del voto del 2022, si vide costretta ad operare una metamorfosi rapida e per certi versi sorprendente: archiviate le tonalità più accese del populismo di destra e dell’euroscetticismo della prima ora, traghettò la sua azione verso un conserv

### V018 · indipendente

**Migranti, Finlandia verso ripresa trasferimenti in Italia**

*mediaset.it · 2026-08-20*

Migranti, anche Finlandia e Svezia pronti ai trasferimenti verso l'Italia | Francia e Spagna: no alle espulsioni | Le opposizioni: clamoroso boomerang per governo Il ministero dell'Interno finlandese non ha fatto sapere quanti richiedenti asilo sarebbero interessati dalla misura, mentre la Svezia spera nella collaborazione di Roma © Afp Anche i richiedenti asilo che si trovano sul territorio finlandese e svedese stanno per essere trasferiti in Italia. Per la Finlandia, il ministero dell'Interno

### V019 · indipendente

**Morte del piccolo Domenico, accolta l'istanza di ricusazione: domani autopsia - Il Roma**

*ilroma.net · 2026-03-02*

Cuore bruciato 02 Marzo 2026 - 11:46 Il gip del tribunale di Napoli Mariano Sorrentino ha accolto la richiesta avanzata dall'avvocato Francesco Petruzzi, legale della famiglia del piccolo Domenico Caliendo, morto sabato 21 febbraio in seguito a un trapianto di cuore fallito lo scorso 23 dicembre all'ospedale Monaldi di Napoli. «È stata accolta l'istanza di ricusazione - ha confermato l'avvocato Petruzzi - ed è stato nominato il professor Ugolino Livi di Udine in sostituzione di Mauro Rinaldi». D

### V020 · indipendente

**Crans-Montana, famiglie vittime Corinaldo a Meloni: "Drammi simili, non lasciateci soli"**

*adnkronos.com · 2026-01-12*

Lettera aperta: "Chiediamo sostegno da parte dello Stato anche per le nostre famiglie, mai più queste tragedie" "Noi aspetteremo fiduciosi che la giustizia faccia il suo corso, ma chiediamo di non essere lasciati soli". Lo scrivono le famiglie delle vittime della tragedia avvenuta, la notte dell’8 dicembre 2018, nella discoteca di Corinaldo (Ancona) dove persero la vita cinque ragazze e ragazzi tra i 14 e i 16 anni e una mamma di 39 anni, in un passaggio della lettera aperta indirizzata alla pre

### V021 · indipendente

**Meloni-Trump, la missione della premier italiana: l'analisi tra Ue e Usa**

*adnkronos.com · 2026-02-17*

"La leader italiana sostiene che l'Europa non ha altra scelta che perseverare con l'alleanza con gli Stati Uniti" Gli Stati Uniti sotto la presidenza di Donald Trump hanno perso la fiducia in tutta Europa, ma il presidente del Consiglio italiano Giorgia Meloni resta fedele all'America. Meloni sta facendo tutto il possibile per mantenere vive le travagliate relazioni transatlantiche. Lo scrive il Wall Street Journal che sottolinea come la premier abbia "resistito alle proposte europee di ritorsio

### V022 · indipendente

**Il Festival Star e novità per “Moon in June“**

*lanazione.it · 2026-06-05*

Incrocia i grandi interpreti che hanno fatto la storia della musica italiana e le sperimentazioni contemporanee, con la promessa di tornare presto là dove tutto è iniziato, Isola Maggiore. Il festival ’Moon in June’ ha svelato ieri a Perugia il ricchissimo cartellone della 12esima edizione, priva della storica location dell’Isola Maggiore ma forte di un suggestivo connubio di voci e suoni che animerà l’estate del Lago Trasimeno con tappe a Perugia e Todi e star come Capossela, i Negrita, Daniele

### V023 · indipendente

**Anarchici, nuove minacce: "Sabotaggi e fuoco alle Olimpiadi" – Il Tempo**

*iltempo.it · 2026-02-10*

Anarchici, nuove minacce: "Sabotaggi e fuoco alle Olimpiadi" «Fuoco alle Olimpiadi e a chi le produce». A distanza di tre giorni dagli scontri di Milano, gli anarchici rilanciano la lotta contro le Olimpiadi e contro il governo. In un lungo post dal titolo «Chi sabota è nemico dell’Italia», pubblicato ieri su un sito d’area, partono dal sabotaggio delle linee ferroviarie, avvenuto proprio la mattina di sabato. Raccontano l’episodio e lo mettono in relazione a quanto accaduto in Francia nel 2024

### V024 · indipendente

**L’opposizione controbatte : "Maggioranza arrogante. Proposte bocciate a priori"**

*lanazione.it · 2026-08-15*

Commercio, trasporto pubblico, lavoro, sanità, università, porto, Pontremolese, ex aree Enel, waterfront e quartieri. L’opposizione sciorina tutti i temi principali su cui ha battuto ferro nelle ultime due legislature, come ribasce in una nota condivisa e sottoscritta da Pd, Avs-Leali a Spezia, Italia Viva e Rifondanzione Comunista - Spezia Bene Comune, che rinfocola il botta e risposta tra maggioranza e minoranza di questi ultimi giorni. Una vera e propria prova muscolare su chi ha fatto e ha f

### V025 · indipendente

**Salvini: «Lega sdoppiata? Fantasie. Sistemeremo ciò che va sistemato» — La Verità**

*laverita.info · 2026-06-10*

Oggi alle 11, «in presenza» nella sala Bruno Salvadori del gruppo Camera, si terrà il Consiglio federale della Lega, ovvero la riunione dei big del Carroccio per decidere il rilancio. Rilancio che passa dal coinvolgimento di Luca Zaia, presidente del Consiglio regionale veneto, e Massimiliano Fedriga, presidente della Regione Friuli Venezia Giulia e della Conferenza Stato-Regioni (carica paragonabile a quella di un ministro). I due rappresentati del Nordest dovrebbero essere, nei pensieri di Mat

### V026 · indipendente

**Gozi (Renew), 'su Europa più forte a quale Meloni dobbiamo credere?' - La voce degli Eurodeputati - Ansa.it**

*ansa.it · 2026-06-27*

"Nel videomessaggio inviato al FII Priority Europe Summit, Giorgia Meloni sostiene che serva un'Europa più forte e più coesa. Da europeisti non possiamo che prenderne atto con favore. Il problema è che fino a ieri la presidente del Consiglio italiana diceva e faceva l'esatto contrario". Lo afferma Sandro Gozi, eurodeputato di Renew Europe e segretario generale del Partito Democratico europeo. "La domanda - aggiunge Gozi - è inevitabile: a quale Giorgia Meloni dobbiamo credere? A quella che pochi

### V027 · indipendente

**Gasparri: “Maggiore severità per immigrazione clandestina” - L'Opinione**

*opinione.it · 2026-02-12*

Il Consiglio dei ministri ieri ha approvato, “con la previsione della richiesta alle Camere di sollecita calendarizzazione nel rispetto dei regolamenti dei due rami del Parlamento”, un disegno di legge che introduce disposizioni in materia di immigrazione e protezione internazionale, nonché disposizioni per l’attuazione del Patto dell’Unione europea sulla migrazione e l’asilo del 14 maggio 2024. Per queste ragioni, Maurizio Gasparri non ha dubbi: il Governo promuove una “maggiore severità per l’

### V028 · indipendente

**Gastroenterologia trasferita a Pesaro, compensazioni per Fano. L'assessore alla sanità Calcinaro: «Rafforzate senologia e ortopedia»**

*corriereadriatico.it · 2026-03-06*

FANO Il reparto di gastroenterologia, con i suoi 20 posti letto, è stato trasferito a Pesaro per ragioni cliniche (la sinergia con la chirurgia generale), ma l’ospedale Santa Croce di Fano, in attesa di un prossimo potenziamento dei servizi, riceve le compensazioni richieste dal sindaco Luca Serfilippi: 8 posti letto, che erano già disponibili a otorinolaringoiatria, assegnati a senologia (eccellenza ospedaliera che finora non disponeva di degenze autonome) e 12 posti letto istituiti ex novo per

### V029 · indipendente

**Il sacco dimenticato del Nord - Tempi**

*tempi.it · 2026-05-22*

Oltre alla questione meridionale, esiste in Italia una questione settentrionale, di cui non discute più nessuno, Lega compresa. E la gallina dalle uova d’oro del Nord continua a pagare e a tacere Fino a una manciata di giorni dal referendum sulla giustizia, il centrodestra ha provato a negare che avrebbe avuto conseguenze politiche. Ovviamente le ha avute. La vittoria del no è stata significativa, e il centrodestra ha pagato l’inferiore capacità di mobilitazione dei suoi. Ma è interessante guard

### V030 · indipendente

**Meloni: "L'uccisione di Quentin Deranque una ferita per l'intera Europa" - il Giornale**

*ilgiornale.it · 2026-02-18*

La morte del giovane militante di destra, a Lione, ha suscitato una profonda commozione, in Francia ma non solo. È un delitto orribile, maturato nell'odio politico. Gli arrestati, finora nove, sono ex membri del movimento di estrema sinistra Jeune Garde, sciolto dal governo francese nel 2025. Profonda la commozione della presidente del Consiglio italiana, Giorgia Meloni. "L’uccisione del giovane Quentin Deranque in Francia - scrive Meloni sui propri canali social - è un fatto che sconvolge e add

### V031 · indipendente

**Rifugiati, si apre il fronte svizzero. Via libera ai trasferimenti in Italia - la Repubblica**

*repubblica.it · 2026-08-19*

BERLINO – Il Patto per l’Asilo europeo propagandato da Giorgia Meloni come supremo argine contro le crisi migratorie sta cominciando a svelare il suo vero volto. Dopo la Germania anche la Svizzera ha annunciato che riprenderà i trasferimenti in Italia dei “dublinanti”, i richiedenti asilo approdati nel nostro Paese ma che hanno proseguito la loro odissea verso il Nordeuropa. Lo ha dichiarato alla…

### V032 · indipendente

**Delegazione deputati FnV lascia Aula e va al flashmob sulla Rai | Giornale di Brescia**

*giornaledibrescia.it · 2026-06-25*

ROMA, 25 GIU - Una delegazione dei deputati di Futuro Nazionale - come ha riferito Edoardo Ziello - ha lasciato la Camera dove e' in corso la cerimonia per gli 80 anni dell'Assemblea costituente, per partecipare al flashmob organizzato dal partito per denunciare la presunta censura della Rai nei loro confronti. Il sit-in era previsto alle 10.45 in via Cristoforo Colombo a Roma. Oltre a Ziello, hanno confermato di non essere in aula anche i deputati Rossano Sasso e Domenico Furgiuele, Emanuele Po

### V033 · indipendente

**Morte di Umberto Bossi, l’ultimo saluto al Senatùr domenica a Pontida tra la sua gente | Varese7Press**

*varese7press.it · 2026-03-20*

VARESE, 20 marzo 2026-di GIANNI BERALDO Sarà il pratone di Pontida, luogo simbolo delle battaglie autonomiste e delle “giurate” della Lega Nord, a fare da cornice all’ultimo addio a Umberto Bossi. I funerali verranno celebrati domenica 22 marzo alle ore 12, nell’abbazia del monastero di San Giacomo. Una scelta, quella della famiglia, che trasforma l’esequie in un evento corale, un ultimo passaggio condiviso con quel “popolo della Padania” che Bossi ha contribuito a plasmare e guidare per oltre t

### V034 · indipendente

**La âgiornata perfettaâ del Lago Maggiore con lâarrivo del Giro dâItalia - La Stampa**

*lastampa.it · 2026-05-24*

Un Â«pubblico fantasticamente in rosaÂ» Ã¨ stato descritto quello di Verbania, venerdÃ¬ dallo speaker. La cittÃ Ã¨ stata piÃ¹ volte elogiata e ringraziata per il calore con cui ha accolto la 13Âª tappa partita da Alessandria. Il traguardo era sotto il municipio a Pallanza, e proprio nello specchio dâacqua di fronte galleggiavano le otto lettere che compongono il nome Â«VerbaniaÂ», scritto in caratteri cubitali a favore di riprese aeree. Suggestive tutte le immagini televisive che hanno immortala

### V035 · indipendente

**Ponte sullo Stretto: PresaDiretta Open esamina costi e impatto a Rai 3**

*ilfattoquotidiano.it · 2026-02-28*

Il Ponte sullo Stretto, tra questione ambientale, mancata gara, aumento dei costi, è al centro di “PresaDiretta Open“, in onda domenica 1° marzo, alle 20.30 su Rai 3. Nel reportage un’intervista all’ad della Società Stretto di Messina, Pietro Ciucci, e un viaggio a Messina, la città col più alto tasso di spopolamento in Europa e dove solo un cittadino su tre riceve l’acqua 24 ore al giorno. Dopo la delibera della Corte dei Conti e il nuovo decreto del governo Meloni, si dà voce agli abitanti di

### V036 · indipendente

**L’ego da Guinness che copre pure il talento — La Verità**

*laverita.info · 2026-02-08*

Cognome e nome: Barbareschi Luca Giorgio. Montevideo, 1956. Artista colto e dal multiforme ingegno: attore, regista e produttore cinematografico e teatrale, conduttore televisivo. Un dissipatore di talento (il suo). In onda su Rai 3 con l’ennesima, noiosa, «spompa» rimasticatura del late show americano. Titolo: Allegro ma non troppo. Nelle prime cinque puntate del 2026, media di 345.000 telespettatori, share del 3,18. Ascolti non proprio allegrissimi, migliori comunque del precedente Se mi lasci

### V037 · indipendente

**Tajani: «Con il “sì” è garantito più equilibrio. Molti magistrati voteranno così»**

*avvenire.it · 2026-03-19*

Tajani: «Con il “sì” è garantito più equilibrio. Molti magistrati voteranno così» Il vicepremier e capo di Forza Italia ad Avvenire: «I toni aspri non mi sono piaciuti. I pm sottoposti alla politica? No, anzi: la loro autonomia sarà rafforzata» Ministro Antonio Tajani, si chiude domani una campagna referendaria che ha visto toni molto accesi, da ambo le parti. In questo, restiamo un Paese non riformabile? I toni aspri non sono piaciuti affatto neppure a me. Ma deve consentirmi di osservare che l

### V038 · indipendente

**L’impronta francese nel cortile africano: il Franco Cfa - L'Opinione**

*opinione.it · 2026-04-02*

Come commenterebbe un cittadino nigerino la riconferma di Parigi a roccaforte dei diritti dopo le ultime elezioni comunali? Beh, forse avrebbe qualcosa da ridire. Come lui, tanti altri di ben 14 Nazioni africane la cui valuta ufficiale è niente di meno se non la più grande eredità coloniale francese: il Franco Cfa (Colonie francesi d’Africa). In uso dal secondo dopoguerra, si presenta oggi in due varianti, il Franco Cfa dell’Africa occidentale e quello dell’Africa centrale, dettando gli scambi d

### V039 · indipendente

**Conte, venerdì a Roma evento M5S per il no al referendum - Ultima ora - Ansa.it**

*ansa.it · 2026-03-15*

"Ci siamo quasi, la prossima sarà l'ultima della campagna referendaria e allora abbiamo organizzato per venerdì prossimo 20 un incontro: ci ritroviamo tutti a Roma al Palazzo dei Congressi alle 17 per ribadire tutti insieme le ragioni del No": ad annunciarlo il leader del M5s Giuseppe Conte con un video su Fb. "Vi aspettiamo per confrontarci sui veri contributi di questa riforma, dobbiamo fermarli, dobbiamo votare tutti insieme No", aggiunge. "Avremo tantissimi ospiti, ci saranno: Gustavo Zagreb

### V040 · indipendente

**Angelo con il volto di Meloni, il cardinale Reina: âNon si puÃ² strumentalizzare lâarte sacraâ - la Repubblica**

*repubblica.it · 2026-01-31*

Il Vicariato di Roma ha avviato unâindagine interna sul restauro effettuato nella basilica di San Lorenzo in Lucina, nel centro storico della Capitale, dove il volto di un angelo Ã¨ stato restaurato assumendo tratti somatici riconducibili alla presidente del Consiglio Giorgia Meloni. E il cardinale Baldo Reina, vicario di Papa Leone XIV, esprime tutto il suo disappunto attraverso una nota in cui â¦

### V041 · indipendente

**Rassegna stampa 20-02-2026 edizioni Calabria - Gazzetta del Sud**

*gazzettadelsud.it · 2026-02-20*

In questo video alcuni dei titoli principali del nostro giornale, edizioni calabresi, a cura di Salvatore De Maria. Di seguito gli altri che potete leggere nel giornale in edicola oggi CALABRIA - Integrazioni al reddito e indennità, ecco le misure del decreto maltempo dopo le devastazioni in Calabria - Il conto salato dei cicloni in Calabria: terreni sott’acqua e filiere produttive in crisi - Ciclone Harry, Elly Schlein a Siderno: “I sindaci aspettano risposte e ristori” - Maltempo a Cosenza, nu

### V042 · indipendente

**Moretti scarcerato, protesta il governo: un oltraggio - la Repubblica**

*repubblica.it · 2026-01-24*

Il governo vuole chiedere spiegazioni alla Svizzera. Giorgia Meloni sbotta: «Sono indignata». La scarcerazione dietro cauzione di Jacques Moretti, proprietario del Constellation indagato per la strage di capodanno a Crans-Montana, dove sono morte 40 persone e 116 sono rimaste ferite, è «un oltraggio alla memoria delle vittime e un insulto alle loro famiglie», dice la premier annunciando che l’ese…

### V043 · indipendente

**Emergenza abitativa. Oltre duemila richieste ancora in stand-by. E 515 nuclei in povertà**

*lanazione.it · 2026-05-09*

Su 2420 domande per gli alloggi di edilizia popolare presentate nel 2023 alla Spezia, 2082 sono ancora in attesa. Di queste, a oggi, solo 40 sono state archiviate con l’assegnazione dell’alloggio alle famiglie chiavi in mano. Di questi 2082 nuclei familiari in stand by, 515 vivono sotto la soglia di povertà assoluta. "Secondo i dati aggiornati alla fine del 2024 dal Ministero degli Interni, La Spezia è la provincia con il tasso più basso di sfratti per morosità in Italia in base al numero di res

### V044 · indipendente

**Terrorismo, La Russa: "Pericolo sempre in agguato. Aldo Moro? La sua morte una delle pagine più buie della democrazia"**

*affaritaliani.it · 2026-05-09*

Giorno della memoria delle vittime del terrorismo, al via le celebrazioni in Senato. La Russa: “Pericolo sempre in agguato. Aldo Moro? La sua morte una delle pagine più buie della democrazia” “In occasione del 48simo anniversario dell’uccisione di Aldo Moro ricordiamo uno statista che ha servito la nazione con equilibrio, senso delle istituzioni e profondo spirito di dialogo. La sua tragica morte segnò una delle pagine più buie e dolorose della nostra democrazia. Custodire la sua memoria signifi

### V045 · indipendente

**Avanti ma non tutta con Macron - La Stampa**

*lastampa.it · 2026-04-18*

Lâabbraccio con Macron, i saluti con gli altri partner chiamandosi per nome, che dovevano consacrare lâingresso senza riserve, per la prima volta, dopo la lite con Trump, di Meloni nel gruppo dei âVolenterosiâ, non hanno impedito che tra Italia e alleati restasse qualche dissenso di fondo. Meloni con Macron: âSÃ¬ alla missione per Hormuzâ Il primo riguarda la posizione dellâEuropa e del gruppo di Paesi che da tempo stanno cercando di dare un senso alla loro iniziativa comune, mentre Trump li acc

### V046 · indipendente

**prof e neomamma chiede di rinviare il corso di abilitazione: il caso lo risolve il ministero**

*mediaset.it · 2026-03-10*

Alessandria, prof e neomamma chiede di rinviare il corso di abilitazione: il caso lo risolve il ministero Dopo la nascita del figlio Caterina Giacalone ha chiesto di rimandare il percorso abilitante. L'intervento del ministro Valditara ha sbloccato la situazione © Dal Web Ha vinto il concorso per insegnare ma, in quanto priva dell'abilitazione, rischiava di dover seguire le lezioni del corso abilitante con il figlio neonato in braccio visto che le era stata negata la richiesta di rinvio. Il caso

### V047 · indipendente

**To-Mi, i binari dello scontento: oltre 7 mila firme contro i disservizi - La Stampa**

*lastampa.it · 2026-02-15*

Sono quasi 7.200 le firme raccolte con la petizione Â«Migliorate le nostre ferrovie regionaliÂ» promossa dal Comis, Coordinamento mobilitÃ integrata e sostenibile del Piemonte, a cui aderisce anche il Comitato pendolari vercellesi. La petizione era stata lanciata su change. org per esprimere il malcontento dei viaggiatori sui disservizi sulle linee ferroviarie, in primo luogo la Torino-Milano, che hanno ripercussioni su lavoro, scuola e vita privata. Ancora in questa settimana sono stati segnala

### V048 · indipendente

**Inselvini (FdI), 'Ue affronti inverno demografico, a maggio conferenza a Roma' - Altre news - Ansa.it**

*ansa.it · 2026-03-31*

"I dati diffusi oggi dall'Istat certificano ancora una volta una tendenza allarmante: nel 2025 le nascite continuano a diminuire, segnando un ulteriore calo del 3,9% rispetto all'anno precedente e raggiungendo un nuovo minimo storico. Dopo anni di incuranza da parte della sinistra, l'attenzione del governo Meloni, sin dal suo insediamento, è stata massima, con oltre 3 miliardi investiti e numerose riforme a favore della natalità. Serve rendersi conto che non parliamo di una flessione congiuntura

### V049 · indipendente

**Vandali e furti, nasce il gruppo per avvisare. "Un’escalation"**

*lanazione.it · 2026-06-27*

Specchietti rotti, finestrini spaccati o forzati e piccoli furti nelle auto in sosta. È quanto sta accadendo da qualche giorno nel quartiere San Giusto-San Marco, con episodi che si sono concentrati in particolare in via Morrona, ma non solo. Una situazione definita un’escalation, o una "prassi", come ha denunciato anche il consigliere comunale di Sinistra Unita, Luigi Sofia, in una comunicazione fatta durante il consiglio comunale di giovedì. Tanto da portare i residenti di via Morrona a formar

### V050 · indipendente

**Meloni in Giappone, la premier posta foto con Takaichi stile manga e riceve in dono mascotte dell'Expo. «Amicizia e sintonia»**

*ilmattino.it · 2026-01-16*

Dalla foto in “stile manga” alla mascotte in dono. A margine della visita della presidente del Consiglio a Tokyo, c’è spazio per un siparietto tra Giorgia Meloni e la premier giapponese Sanae Takaichi. «Due Nazioni lontane, ma sempre più vicine. Amicizia e sintonia», scrive Meloni sui social, a corredo di uno scatto che ritrae le due leader sorridenti accanto alla versione manga della stessa immagine. In occasione dell’incontro, Takaichi ha omaggiato la premier italiana con la mascotte ufficiale

### V051 · indipendente

**Vannacci su Salvini: "È lui il traditore, è in posizione prona"**

*mediaset.it · 2026-02-04*

Vannacci contro Salvini: "Il traditore è lui, si è messo in posizione prona" Roberto Vannacci ha assicurato che Futuro nazionale sarà un progetto "di destra vera, non nera". E ha criticato Salvini sull'Ucraina sulla legge Fornero Non è questione di slealtà, quanto di lealtà la scelta di Roberto Vannacci di troncare di punto in bianco il nodo che lo legava a Matteo Salvini e alla Lega per mettersi in proprio. E non è nemmeno una questione di parola data e non rispettata, perché - contrattacca l'e

### V052 · indipendente

**Meloni stoppa Crosetto sulle spese per le armi: «La priorità ora sono i fondi per il caro energia»**

*ilgazzettino.it · 2026-05-28*

ROMA Una lite furibonda. Chi ieri mattina era a Palazzo Chigi racconta che nei corridoi, anche a voler esser discreti, non si poteva fare a meno di captare toni su di giri di diversi decibel. Guido Crosetto versus Giorgia Meloni: un testa a testa di fuoco tra o due cofondatori di Fdi che, quando hanno qualcosa che non va, certo non se le mandano a dire. Sarà che è una vita che camminano l'uno di fianco all'altra. Resta alla storia la foto in cui lui, gigante di due metri, la solleva di peso per

### V053 · indipendente

**A14, disagi infiniti: la galleria Vinci chiude per lavori dopo l'incendio. Saranno 212 giorni di passione in autostrada**

*corriereadriatico.it · 2026-01-28*

CUPRA MARITTIMA - «Nella galleria Vinci, subito dopo l’evento dell’aprile 2024, fu fatto un intervento di messa in sicurezza temporaneo in tempi record, data anche la volontà di rimuovere il cantiere in tempo per i ponti del 25 aprile e del 1° maggio. Da metà febbraio partirà l’intervento definitivo di messa in sicurezza e di ammodernamento che prevede la realizzazione di una calotta e di un rivestimento complessivo ex novo». Le parole di Christian Tucciarone, direttore di Tronco di Pescara di A

### V054 · indipendente

**Grillo torna e attacca: “Persa identità M5s”. Conte: ‘Per lui Draghi era grillino…’**

*askanews.it · 2026-07-29*

Roma, 29 lug. (askanews) – “Il MoVimento 5 Stelle ha perso la sua identità, soprattutto ha perso la sua ‘diversità'”. Beppe Grillo torna a parlare dal suo blog e ad attaccare la sua ‘creatura’. Grillo torna e attacca: “Persa identità M5s”. Conte: ‘Per lui Draghi era grillino…’ A gennaio udienza su nome e simbolo rivendicati dal comico

### V055 · indipendente

**IGE 2026, a Roma il confronto sul futuro del gaming tra sfide del mercato, ricerca e nuove regole - il Giornale**

*ilgiornale.it · 2026-04-14*

Si è aperta oggi a Roma l’edizione 2026 dell’Italian Gaming Expo & Conference (IGE), appuntamento di riferimento per il settore del gaming regolamentato e per l’ecosistema tecnologico, normativo e accademico che ne accompagna l’evoluzione. L’evento riunisce istituzioni, regolatori, operatori, aziende tecnologiche e mondo della ricerca in un momento chiave per il comparto, impegnato tra riordino del gioco pubblico e ridefinizione degli equilibri tra innovazione, compliance e sostenibilità. L’ediz

### V056 · indipendente

**Dal Sant’Elia al Gigi Riva: confronto tra istituzioni e società rossoblù alla ex Manifattura Tabacchi**

*unionesarda.it · 2026-06-06*

Dal Sant’Elia al Gigi Riva: confronto tra istituzioni e società rossoblù alla ex Manifattura Tabacchi Il convegno promosso dal Centro Studi Aldo Moro ha riunito amministratori regionali e comunali, il Cagliari Calcio e il figlio di Rombo di Tuono. Il sindaco Zedda: Iter in dirittura d'arrivo, conclusione attesa entro luglioPer restare aggiornato entra nel nostro canale Whatsapp Sala gremita negli spazi della ex Manifattura Tabacchi di Cagliari per il convegno "Dal Sant'Elia al Gigi Riva. Le ragi

### V057 · indipendente

**Leal denuncia per i cani morti al World Dog Show | Giornale di Brescia**

*giornaledibrescia.it · 2026-06-10*

ROMA, 10 GIU - Leal Lega Antivivisezionista ha sporto denuncia-querela alla Procura della Repubblica di Bologna per la morte di tre cani avvenuta il 5 giugno 2026 nei parcheggi di Bologna Fiere, durante il World Dog Show organizzato da Enci. Secondo quanto ricostruito, sei cani di razza Drahthaar, cane da ferma tedesco, erano stati lasciati per ore in due furgoni metallici parcheggiati sotto il sole, senza acqua né adeguata areazione. Il personale di sorveglianza ha rinvenuto un cane già morto a

### V058 · indipendente

**La destra feudale sorveglia e punisce i giornali | il manifesto**

*ilmanifesto.it · 2026-02-24*

La destra feudale sorveglia e punisce i giornali Ri-mediamo La rubrica settimanale su media e società. A cura di Vincenzo Vita Ri-mediamo La rubrica settimanale su media e società. A cura di Vincenzo Vita Mentre in diversi luoghi specializzati si stanno elaborando strategie atte a frenare la crisi della carta stampata, sempre più dirompente, la destra italiana va controcorrente. Sembra che davvero i contropoteri infastidiscano la corte della Regina. Così come è in corso l’offensiva contro la mag

### V059 · indipendente

**Conte: “Meloni ha fallito. Risorse da banche e armi. Primarie a tempo debito” - la Repubblica**

*repubblica.it · 2026-06-14*

Attacca Giorgia Meloni, chiude alla patrimoniale, promette di non volersi assicurare un posto da leader della coalizione di centrosinistra («sono un costruttore, non un rottamatore») ma difende le primarie. Anche se, chiarisce: «Non adesso». Il leader dei 5 Stelle Giuseppe Conte, intervistato dal vicedirettore Stefano Cappellini assicura: «Il Movimento ha scelto di stare nel campo progressista: è…

### V060 · indipendente

**Clochard dorme all’asilo: una dada lo trova in aula. Paura e rabbia tra i genitori**

*ilrestodelcarlino.it · 2026-02-17*

Bologna, 17 febbraio 2026 – Quando la dada, la mattina presto, ha aperto la porta della materna Girotondo se lo è trovato di fronte. Tranquillo. Lui è un ragazzo tunisino, classe 2005, senza fissa dimora che, per ripararsi dal freddo, ha forzato la porta della materna di via Pettazzoni e ha trascorso la notte tra i lettini dei bimbi. La materna fa parte dell’Istituto comprensivo 4 a Corticella. La denuncia Superato lo choc iniziale, la dada ha avvisato la preside Simona Lipparini che sporgerà de

### V061 · indipendente

**Mastella scuote il Campo Largo - Il Roma**

*ilroma.net · 2026-02-11*

il monito 11 Febbraio 2026 - 08:43 NAPOLI. Nel Campo Largo non mancano mai le scosse. «La Campania può essere il principale e primo serbatoio di voti del Paese per il campo largo alle Politiche del 2027, a patto che avverte il leader nazionale di Noi di Centro e sindaco di Benevento Clemente Mastella si rompano ora gli indugi e si riproduca l'alleanza che ha vinto alle Regionali ovunque, in tutte le province, senza eccezioni e senza veti. A questo proposito chiedo che il segretario regionale del

### V062 · indipendente

**Meloni a Reggio Calabria per il 212^ Annuale della Fondazione dei Carabinieri**

*italpress.com · 2026-06-05*

CALABRIA (ITALPRESS) – Alla presenza del Comandante Generale, generale di Corpo d’armata Salvatore Luongo, si è svolta per la prima volta a Reggio Calabria, sul Lungomare Falcomatà, la festa dell’Arma dei Carabinieri, giunta al 212^ Annuale della sua Fondazione. L’evento è stato suggellato dalla presenza del Presidente del Consiglio dei Ministri Giorgia Meloni, del Ministro della Difesa Guido Crosetto, del Ministro dell’Interno Matteo Piantedosi, del Ministro della Salute Orazio Schillaci, del M

### V063 · indipendente

**Stretto di Hormuz, con il blocco a rischio 30 mila marittimi. Gli armatori: «Intervenga la Marina»**

*ilmattino.it · 2026-03-11*

Trentamila marittimi a rischio, molti dei quali italiani. Un quadro allarmante che rischia di diventare sempre più preoccupante con il passare dei giorni. Le famiglie si affidano ai telefoni e seguono con preoccupazioni le notizie che arrivano dal fronte. Ieri sera, ad esempio, un sussulto quando è cominciata a circolare la voce che molte navi hanno spento l’Ais, l’apparato che mostra la rotta, per evitare di essere localizzate. Anche il piccolo profilo della nave su Marin Traffic aiuta le famig

### V064 · indipendente

**Morte di Umberto Bossi, ricordi e divisioni nella Lega in Piemonte - La Stampa**

*lastampa.it · 2026-03-21*

Attorno al feretro del Â«CapoÂ» niente Ã¨ dimenticato, quasi nulla Ã¨ perdonato. Per una certa parte d'Italia che per lui aveva i confini del Nord, la morte di Umberto Bossi Ã¨ lutto collettivo di ricordi personali e analisi politiche. Con un prima e un dopo: la vigorÃ¬a della proletaria canottiera ostentata nei giardini di Arcore e l'invaliditÃ ; il passaggio, nel 2013 e formalmente nel 2017, dalla Â«suaÂ» Lega Nord per l'indipendenza della Padania alla Lega per Salvini premier. Il ricordo di C

### V065 · indipendente

**Il Quirinale chiede modifiche su scudo e fermo preventivo, Palazzo Chigi al lavoro - Notizie - Ansa.it**

*ansa.it · 2026-02-04*

Il "segnale" che Giorgia Meloni voleva dare da settimane, e su cui ha accelerato dopo le violenze di Torino, è atteso nelle prossime ore. Un decreto legge e un disegno di legge "a garanzia della sicurezza dei cittadini e dell'ordine pubblico" dovrebbero approdare, confermano qualificate fonti di governo, sul tavolo del Consiglio dei ministri, non ancora convocato ma previsto nel tardo pomeriggio. Qualche minimo di incertezza ancora c'è, ma per tutta la giornata - in cui c'è stato anche un confro

### V066 · indipendente

**Modello 730, novità e scadenze da rispettare: dalla nuova dichiarazione alla stretta sui bonus**

*ilmessaggero.it · 2026-02-10*

È arrivata, diffusa dall'Agenzia delle Entrate, la pubblicazione delle versioni preliminari dei modelli per la dichiarazione dei redditi relativi al 2025. In questo modo i contribuenti potranno orientarsi sulle regole da seguire per l’adempimento fiscale. Le nuove istruzioni tengono conto sia delle modifiche introdotte dall’ultima manovra economica sia del percorso di revisione del sistema tributario. I redditi che i contribuenti hanno ottenuto nel corso del 2025 dovranno essere dichiarati attra

### V067 · indipendente

**Ue, l'Europa si allarga a Est e sfida Putin: il piano per blindare i Balcani, porte aperte al Montenegro – Il Tempo**

*iltempo.it · 2026-06-05*

Ue, l'Europa si allarga a Est e sfida Putin: il piano per blindare i Balcani, porte aperte al Montenegro Accelerare sull'allargamento, senza snaturarne la natura di processo basato sul merito. È questo il messaggio che emerge dal vertice Ue-Balcani occidentali che si è tenuto a Tivat, Montenegro. All'appuntamento era attesa anche Giorgia Meloni, che però ha disertato all'ultimo. La ragione, secondo fonti di governo, è da ricercare in un ritardo alla cerimonia del 212° Annuale di Fondazione dell'

### V068 · indipendente

**Tajani "Abusi a Minneapolis, c'è differenza tra arrestare una persona armata e ucciderla"**

*italpress.com · 2026-01-26*

ROMA (ITALPRESS) – “Il presidente del Consiglio Giorgia Meloni ha chiarito che per il momento l’Italia non entra a far parte del Board of Peace”. Lo ha detto il vicepremier e ministro degli Esteri Antonio Tajani, ospite di Ping Pong su Rai Radio1. “Ci sono limiti costituzionali invalicabili: l’articolo 11 della Costituzione e l’articolo 9 dello statuto del Board non rispettano il principio di parità tra i componenti. Se lo statuto del Board venisse modificato e venissero meno i vincoli costituzi

### V069 · indipendente

**Da Kedrion agli studi con Sanofi, il conflitto d’interessi della Pd Zambito - il Giornale**

*ilgiornale.it · 2026-05-30*

Perché al Pd in commissione Covid quando si parla dei monoclonali Eli Lilly in pandemia rifiutati dall’Italia alla sinistra parte la testa? Forse perché la deputata Ylenia Zambito è in conflitto d’interessi, avendo lavorato come docente presso il dipartimento di Farmacia dell’Università di Pisa ad alcune ricerche scientifiche con Toscana Life Science, la società che avrebbe dovuto produrre monoclonali in Italia ricevendo milioni di finanziamento pubblico. Lo dicono diversi documenti trovati in r

### V070 · indipendente

**Buttafuoco: Biennale libera e audace come dice Mattarella**

*askanews.it · 2026-05-06*

Buttafuoco: Biennale libera e audace come dice Mattarella Meloni ha ribadito che, anche dissentendo, la Biennale è autonoma Salta al contenuto Videonews Buttafuoco: Biennale libera e audace come dice Mattarella Venezia, 6 mag. (askanews) – “Andare avanti avere audacia, ha accomandato Mattarella ai David di Donatello. Siate liberi e audaci, dice. Eccoci. Se le autorità politiche fossero fureria dove le ingerenze arrivano a piegare la solidità delle istituzioni, avremmo altro esito” Lo ha detto il

### V071 · indipendente

**Pro Vita, sen. Malan: "Garantire a tutti libertà di espressione, come insegna Costituzione" – Il Tempo**

*iltempo.it · 2026-03-02*

Pro Vita, sen. Malan: "Garantire a tutti libertà di espressione, come insegna Costituzione" Roma, 2 mar. (Adnkronos) - “In questa conferenza stampa mostriamo alcuni manifesti che esprimono un'opinione - che ciascuno è libero di non condividere - in modo garbato e, a volte, anche quasi poetico. Eppure, ne è stata vietata l'affissione. La Costituzione tutela la libertà d'espressione e credo che debba essere garantita per tutti”. Lo afferma Lucio Malan, capogruppo al Senato di FdI, intervenuto a ‘.

### V072 · indipendente

**E' morta Valeria Fedeli, ex ministra dell'Istruzione - Notizie - Ansa.it**

*ansa.it · 2026-01-14*

E' morta Valeria Fedeli. Sindacalista ed ex ministra dell'Istruzione con il governo Gentiloni, aveva 76 anni. Prima della sua nomina al governo aveva ricoperto anche la carica di vicepresidente del Senato. Nata a Treviglio nel 1949, Valeria Fedeli ha speso la propria vita tra scuola, impegno sindacale e successivamente nella politica attiva. Dopo aver insegnato nelle scuole primarie ed aver qui iniziato la propria attività sindacale con la Cgil, nel 1979 abbraccia questo impegno al 100% tanto da

### V073 · indipendente

**Il parere dei geologi: a Niscemi fragilitÃ  'nota'**

*agi.it · 2026-01-28*

AGI - L'Ordine regionale dei geologi di Sicilia esprime "profonda e sincera solidarietà" alla popolazione di Niscemi, duramente colpita dal grave movimento franoso che ha interessato il territorio comunale, provocando l'evacuazione di centinaia di famiglie, danni ingenti al patrimonio edilizio e una comprensibile condizione di paura e incertezza. La frana di Niscemi, spiega il presidente Paolo Mozzicato, "non può essere letta come un evento improvviso o eccezionale, ma va inquadrata all'interno

### V074 · indipendente

**Tarquinio (Pd), 'Patto migrazione Ue produce mostruosità, non sicurezza' - La voce degli Eurodeputati - Ansa.it**

*ansa.it · 2026-06-11*

"La cosa più sconcertante" in relazione al Patto sulla migrazione e l'asilo "è dover constatare di nuovo che anche forze che si definisco popolari e liberali condividano oramai posizioni che fino a pochi anni fa appartenevano quasi solo alle estreme destre nazionaliste. Ma la riduzione dei diritti e la cancellazione e dei doveri produce mostruosità non ordine e sicurezza. E ciò che viene negato o sottratto ad alcuni erode la libertà e la dignità di tutti". Così in una nota l'eurodeputato del Pd

### V075 · indipendente

**25 aprile, Mattarella: «Pace diritto di ogni popolo. Questo il senso della Resistenza» - Il Roma**

*ilroma.net · 2026-04-25*

Festa della Liberazione 25 Aprile 2026 - 10:12 L’Italia celebra oggi, 25 aprile 2026, l’81° anniversario della Liberazione. Le celebrazioni si sono aperte a Roma con la deposizione di una corona d’alloro all’Altare della Patria da parte del presidente della Repubblica, Sergio Mattarella, accompagnato dalle più alte cariche dello Stato: il presidente del Senato Ignazio La Russa, il presidente della Camera Lorenzo Fontana, la presidente del Consiglio Giorgia Meloni, il presidente della Corte costi

### V076 · indipendente

**Primo Piano Calabria, il cinema incontra il territorio: Fabrizio Maria Cortese e Vincent Riotta protagonisti della prima rassegna di cineturismo**

*ilmessaggero.it · 2026-03-16*

Al termine della prima giornata della rassegna Primo Piano Calabria – Rassegna di Cineturismo, abbiamo incontrato il regista Fabrizio Maria Cortese e l’attore Vincent Riotta per parlare di cinema, dei loro progetti più recenti e del rapporto speciale che li lega alla Calabria. L’evento, promosso e sostenuto dalla Calabria Film Commission, presieduta da Anton Giulio Grande con il direttore generale Giampaolo Calabrese, si è svolto presso l’Auditorium Franco Battiato. La rassegna rappresenta il pr

### V077 · indipendente

**Fontana commemora Umberto Bossi in Consiglio: «È stato un visionario che ha dato voce al Nord»**

*varesenews.it · 2026-03-31*

Fontana commemora Umberto Bossi in Consiglio: «È stato un visionario che ha dato voce al Nord» Il ricordo del governatore nell'aula del Pirellone dopo la scomparsa del fondatore della Lega: «Ha imposto temi come autonomia e federalismo quando nessuno ne parlava» L’aula del Consiglio regionale della Lombardia si è fermata oggi, 31 marzo, per rendere omaggio a Umberto Bossi, il fondatore della Lega scomparso lo scorso 19 marzo. A tracciarne il profilo politico e umano è stato il presidente Attilio

### V078 · indipendente

**Le opposizioni presentano la mozione sfiducia su Santanchè, 'si discuta subito' - Ultima ora - Ansa.it**

*ansa.it · 2026-03-25*

Le opposizioni hanno presentato al Senato e alla Camera una mozione di sfiducia nei confronti della ministra del Turismo, Daniela Santanché. A inizio seduta a Palazzo Madama le opposizioni hanno chiesto di poter discutere al più presto la mozione di sfiducia. In aula è intervenuto per primo il capogruppo del M5s, Luca Pirondini, chiedendo che la premier si assuma la responsabilità per "mettere fine a questo balletto indecente". Sulla ministra, Pirondini ha ricordato che è "uno scempio che va ava

### V079 · indipendente

**L'Ice minaccia due giornalisti Rai a Minneapolis. Il video: "Spaccheremo il finestrino e vi tireremo fuori dall'auto"**

*ilfattoquotidiano.it · 2026-01-25*

L’Ice minaccia due giornalisti Rai a Minneapolis. Il video: “Spaccheremo il finestrino e vi tireremo fuori dall’auto” Due inviati della trasmissione Rai ‘In Mezz’ora’, condotta da Monica Maggioni, sono stati minacciati da uomini dell’Ice a Minneapolis. In un video postato sul profilo Instagram della trasmissione, si vedono gli agenti dell’Ice che si avvicinano ad un auto con a bordo i giornalisti Laura Cappon e Daniele Babbo intimando loro di abbassare il finestrino. “’Spaccheremo il finestrino

### V080 · indipendente

**Comune di Matera: Pd, Matera non si governa senza progetto e maggioranza politica - Notizie - Ansa.it**

*ansa.it · 2026-02-20*

"La crisi politica che si è aperta nel centrodestra a Matera impone una riflessione seria e responsabile sul futuro della città. Non si può governare una comunità complessa e strategica come Matera senza un progetto chiaro, senza un programma di mandato condiviso e, soprattutto, senza una maggioranza politica coesa". Così il commissario regionale del Pd, Daniele Manca, "interviene sulla situazione amministrativa del capoluogo dei Sassi sottolineando come la città stia vivendo una fase di evident

### V081 · indipendente

**Morto Luigi Nicolais, ex ministro ed ex presidente del Cnr - Il Sole 24 ORE**

*ilsole24ore.com · 2026-01-12*

Morto Luigi Nicolais, ex ministro ed ex presidente del Cnr Aveva 83 anni. Era stato ministro per le Riforme nel secondo governo Prodi II e guidato il Consiglio nazionale delle ricerche dal 2012 al 2016 2' di lettura 2' di lettura È morto a 83 anni Luigi Nicolais, era stato ministro per le Riforme e le innovazioni nella pubblica amministrazione nel governo Prodi II e presidente del Consiglio Nazionale delle Ricerche dal 2012 al 2016. È stato inoltre assessore della giunta regionale della Campania

### V082 · indipendente

**Francesco Boccia: «Il governo è allo sbando, a pagare sono le famiglie e le imprese» - Gazzetta del Mezzogiorno**

*lagazzettadelmezzogiorno.it · 2026-04-24*

Conti in rosso, economia in crisi e finanza pubblica in affanno che non riesce a scendere il patto di stabilità sotto la fatidica soglia del 3%. Senatore Boccia, quanto è alto il livello di preoccupazione? «Altissimo. La legislatura è entrata nella fase finale e, dopo 4 leggi di bilancio su 5 già fatte con risultati fallimentari, il Governo Meloni appare allo sbando. Siamo molto preoccupati sia per le scelte di politica economica che per quelle di politica estera. Gli errori li stanno pagando nu

### V083 · indipendente

**Addio a Gianni Mattioli, fondatore delle Liste Verdi. Bonelli: âCondusse la battaglia antinucleareâ - La Stampa**

*lastampa.it · 2026-06-01*

ROMA. Â«Con profondo dolore apprendo della scomparsa di Gianni Mattioli, fondatore delle Liste Verdi, giÃ deputato e ministro della Repubblica. Se ne va uno dei protagonisti piÃ¹ autorevoli dell'ambientalismo italiano, un uomo che ha saputo coniugare rigore scientifico, impegno civile e passione politicaÂ». CosÃ¬ Angelo Bonelli, deputato AVS e co-portavoce di Europa Verde. Â«Insieme a Massimo Scalia Ã¨ stato uno dei principali artefici della storica battaglia antinucleare che ha cambiato il nost

### V084 · indipendente

**Tajani a Washington per riunione Board of Peace: Lavoriamo per la pace – Il Tempo**

*iltempo.it · 2026-02-19*

Tajani a Washington per riunione Board of Peace: Lavoriamo per la pace Washington, 19 feb. (askanews) - "Assolutamente no": l'Italia non può restare ai margini di questo processo di pace. Lo ha affermato il ministro degli Esteri Antonio Tajani al suo arrivo a Washington, dove oggi parteciperà alla prima riunione del Board of Peace. "Abbiamo visto - ha spiegato Tajani - che Paesi come la Germania, il Regno Unito, la Norvegia e tanti altri Paesi europei partecipano da osservatori a questa riunione

### V085 · indipendente

**Chiara Pellacani: "Cinque ori agli Europei, poi la telefonata di Giorgia Meloni". L'intervista alla regina azzurra dei tuffi**

*adnkronos.com · 2026-08-12*

La campionessa azzurra si racconta all'Adnkronos dopo le 5 medaglie vinte nella rassegna continentale di tuffi a Parigi: "Penso alle Olimpiadi di Los Angeles, ma ci arriverò al meglio solo attraverso obiettivi intermedi e più vicini" Immaginate di vincere cinque ori agli Europei, in una settimana. E poi, tornati a casa, di ricevere pure - tra centinaia di messaggi - una telefonata del presidente del Consiglio. A Chiara Pellacani, regina azzurra dei tuffi, è successo dopo il pokerissimo nella ras

### V086 · indipendente

**Domani presentazione del medico**

*lanazione.it · 2026-01-23*

Una settimana ricca di appuntamenti tra sanità, politica e cultura. Domani, sabato 24 gennaio alle ore 15.30, la Pro Loco di Prunetta organizza un importante incontro, aperto a tutta la popolazione, dedicato all’assistenza sanitaria territoriale. Durante la riunione verrà presentato il nuovo medico, il dottor Matteo Zagati, e si discuteranno le strategie per garantire il mantenimento dei servizi sanitari sul territorio. Sempre domani, alle ore 16.30, a San Marcello Pistoiese, nella Sala Baccarin

### V087 · indipendente

**Meloni, da Rutte entusiastica ricostruzione confusionaria, serve prudenza - Ultima ora - Ansa.it**

*ansa.it · 2026-06-25*

"Il Segretario Generale nella sua, diciamo così, entusiastica ricostruzione ha messo insieme cose che in realtà sono diverse tra loro, confondendo la tipologia dei voli autorizzati, e lui stesso poi ha corretto e puntualizzato". Così la presidente del Consiglio Giorgia Meloni nella conferenza stampa con il presidente francese Emmanuel Macron dopo l'incontro bilaterale a Cap d'Antibes, nell'ambito del vertice intergovernativo Italia-Francia. "Non so dire, diciamo, questa semplicistica ricostruzio

### V088 · indipendente

**Valnerina tra erba alta e marciapiedi “inagibili“. Il circolo del Pd bacchetta Comune e Anas**

*lanazione.it · 2026-04-05*

TERNI "È arrivata Pasqua, arrivano i turisti, ma Anas e Comune di Terni non si fanno trovare pronti, in una zona turistica come quella della Cascata delle Marmore", lo denuncia Massimo Leopoldi, segretario del circolo Pd di Collestatte e Torre Orsina. "Il tratto di Collestatte e Torre Orsina della strada statale 209 Valnerina anche quest’anno presenta erba alta sui bordi, marciapiedi impraticabili e cunette ostruite da detriti – attacca Leopoldi – Negli anni in cui governava il Pd le manutenzion

### V089 · indipendente

**Conte: Nome del fronte progressista dovrebbe essere 'Alleanza per la Costituzione' – Il Tempo**

*iltempo.it · 2026-07-01*

Conte: Nome del fronte progressista dovrebbe essere 'Alleanza per la Costituzione' Il presidente Rocca a Il Tempo: mascherine, se il pasticcio di Zingaretti l'avesse fatto il centrodestra... PubblicitÃ UNESCO, per la prima volta le Consulte studentesche ai lavori del Comitato di alto livello. Valditara: “Italia protagonista anche per il modello di partecipazione studentesca ai processi decisionali” Alessandro Bertoldi a Come States? — Trump, Nato, Milei e il futuro dell'Occidente (Agenzia Vista)

### V090 · indipendente

**La bufala di Sigfrido. Quando Ranucci evocava camorra, politica e deep state. E ieri il bis – Il Tempo**

*iltempo.it · 2026-08-24*

La bufala di Sigfrido. Quando Ranucci evocava camorra, politica e deep state. E ieri il bis Da Fedez sostenne che l'attentato serviva a fermare le inchieste di Report. Parlava a vanvera? Abboccava alle storie di Lavitola? O cos'altro? Poi il minestrone citando l'ex Usigrai Giulietti dagli 007 deviati alla mafia Fa una certa impressione riascoltare la puntata di Pulp Podcast del 7 aprile scorso. Quella in cui Fedez ospitò l’uomo del momento, Sigfrido Ranucci. Fresco della vittoria del No al refer

### V091 · indipendente

**Conte "Commissione Antimafia evita approfondimenti su stragi '92-'93" Agenzia di stampa Italpress - Italpress**

*italpress.com · 2026-05-23*

Conte “Commissione Antimafia evita approfondimenti su stragi ’92-’93” PALERMO (ITALPRESS) - "Questo è un altro capitolo che francamente mi addolora e mi indigna. Sono quasi ormai più di tre anni di una Commissione antimafia che si è insediata sotto una presidenza in mano a Fratelli d'Italia, che ha assolutamente e sistematicamente cercato di evitare gli approfondimenti, addirittura da noi suggeriti, sulla scorta di prove documentali, sentenze ormai passate in giudicato, per accertare la verità d

### V092 · indipendente

**Calcio, Trofeo D’Alterio: decima edizione per il Mundialito Under 12**

*askanews.it · 2026-05-19*

Roma, 19 mag. (askanews) – Lo stadio Alberto Vallifuoco di Mugnano si prepara a diventare, dal 30 maggio al 3 giugno, uno dei punti di riferimento del calcio giovanile internazionale ospitando la decima edizione del Trofeo Internazionale D’Alterio Group dedicato alla categoria Under 12. Saranno 26 le squadre partecipanti, con oltre 520 giovani calciatori provenienti dall’Italia e dall’estero.

### V093 · indipendente

**Controcorrente, anche De Leo aderisce al movimento - Notizie - Ansa.it**

*ansa.it · 2026-07-01*

Anche il deputato regionale Alessandro De Leo, ex Forza Italia che era poi andato al gruppo misto, è passato al movimento Controcorrente insieme ai deputati regionali, ex M5s, Carlo Gilistro e Jose Marano. Il leader del movimento Ismaele La Vardera li ha presentati in conferenza stampa annunciando anche la creazione del gruppo Controcorrente all'Ars. Marano sarà la capogruppo. "Da oggi - ha detto La Vardera - non sono più solo. Ho trovato Carlo e Jose e ritrovato Alessandro, sono felice. Vorrei

### V094 · indipendente

**Crans Montana, il padre di Trystan: «Le vittime risarcite con 10mila franchi, per le cure chiesto 10 volte tanto»**

*ilmessaggero.it · 2026-04-26*

«Queste fatture sono uno scandalo. Una follia. Il nostro dolore, e quello delle altre famiglie, non può essere contabilizzato. Ma quello che sta facendo il mio Paese è una vergogna». Michel Pidoux fatica a riconoscersi nelle scelte della Svizzera da quando ha saputo che verranno chiesti all'Italia 108 mila euro per le cure prestate a tre ragazzi italiani la notte del 31 dicembre all'ospedale di Sion. Giovani che si trovavano all'interno del bar "Le Constellation", a Crans-Montana, e che sono rim

### V095 · indipendente

**A Taranto rinnovo del consiglio provinciale, oggi al voto i 27 Comuni: urne aperte fino alle 20 - Gazzetta del Mezzogiorno**

*lagazzettadelmezzogiorno.it · 2026-06-14*

Cinque liste, 47 candidati per 12 seggi disponibili. Sono i numeri della corsa per il rinnovo del Consiglio provinciale di Taranto previsto per oggi, dalle 8 alle 20. Si tratta, è opportuno ribadirlo, di consultazioni di secondo livello (non votano i cittadini ma i consiglieri e i sindaci dei 27 comuni ionici) e non riguardano il presidente della Provincia: Gianfranco Palmisano, infatti, rimarrà in carica indipendentemente dall’esito della votazione. Il centrosinistra si presenta al voto con il

### V096 · indipendente

**Sul diesel sconto da 17 cent fino al 6 agosto - Norme e Istituzioni - Ansa.it**

*ansa.it · 2026-07-27*

Da mezzanotte fino al 6 agosto il gasolio alla pompa costerà 17 centesimi in meno. Il taglio, tra accise mobili e Iva, è il risultato del combinato tra il decreto legge approvato dal Consiglio dei ministri (anche con altri 100 milioni per l'ex Ilva per completare il percorso di cessione) e un decreto interministeriale di Mef e Mase, secondo l'accelerazione dettata venerdì da Giorgia Meloni nell'incontro con Giancarlo Giorgetti. La premier ha rivendicato sui social la misura (solo sul diesel ques

### V097 · indipendente

**Confedilizia si riunisce: tra Piano Casa e novità - L'Opinione**

*opinione.it · 2026-05-13*

La proprietà immobiliare torna al centro del dibattito. È tempo di Assemblea annuale per Confedilizia, che martedì 19 maggio riunirà a Roma il mondo della proprietà edilizia italiana per fare il punto sulle principali sfide del settore. L’appuntamento è fissato a partire dalle ore 11 nella cornice del Teatro Adriano, dove convergeranno rappresentanti del Governo, del Parlamento, delle istituzioni e delle principali associazioni di categoria. Alla riunione prenderanno parte anche i dirigenti dell

### V098 · indipendente

**Sicurezza, Piantedosi: no rischio terrorismo ma massima allerta**

*askanews.it · 2026-03-07*

Sicurezza, Piantedosi: no rischio terrorismo ma massima allerta “Rafforzati migliaia di obiettivi sensibili sul territorio” Salta al contenuto Videonews Sicurezza, Piantedosi: no rischio terrorismo ma massima allerta Bologna, 7 mar. (askanews) – “Al momento no”, non c’è rischio terrorismo legato ai conflitti in Iran, ma “ogni qualvolta viviamo situazioni internazionali di questo tipo dobbiamo sempre porci il problema”. Lo ha detto il ministro dell’Interno Matteo Piantedosi a margine dell’incontr

### V099 · indipendente

**Ue, i Pasdaran sono terroristi. Tajani: " Raggiunto consenso politico" – Il Tempo**

*iltempo.it · 2026-01-29*

Ue, i Pasdaran sono terroristi. Tajani: " Raggiunto consenso politico" A margine del Consiglio Affari esteri di Bruxelles, il ministro degli Esteri Antonio Tajani ha annunciato il raggiungimento dell'intesa per l'iscrizione dei Pasdaran, i Guardiani della Rivoluzione iraniana, nella lista delle organizzazioni terroristiche. Il video di TotalEU.

### V100 · indipendente

**Scontri a Torino, Piantedosi: Falso che Governo Meloni stretta libertà manifestare, cortei aumentati – Il Tempo**

*iltempo.it · 2026-02-04*

Scontri a Torino, Piantedosi: Falso che Governo Meloni stretta libertà manifestare, cortei aumentati Il presidente Rocca a Il Tempo: mascherine, se il pasticcio di Zingaretti l'avesse fatto il centrodestra... PubblicitÃ UNESCO, per la prima volta le Consulte studentesche ai lavori del Comitato di alto livello. Valditara: “Italia protagonista anche per il modello di partecipazione studentesca ai processi decisionali” Alessandro Bertoldi a Come States? — Trump, Nato, Milei e il futuro dell'Occiden

