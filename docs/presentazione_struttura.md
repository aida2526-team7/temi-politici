# Struttura della presentazione

Scheletro da riempire insieme. Ogni slide porta **una** affermazione, il titolo
la dice per esteso, e sotto c'è la prova. Nessuna slide con un titolo-etichetta
tipo «Metodologia»: se la slide non ha un'affermazione, non è una slide.

Durata stimata: 18-20 minuti, 17 slide. I grafici citati sono in
[`dataviz_struttura.md`](dataviz_struttura.md).

---

## Apertura — 2 slide

### 1. La domanda

> Sui temi politici italiani, ciò che i partiti **promettono**, ciò che **fanno**
> in Parlamento e ciò di cui la stampa **parla** sono tre cose diverse. Quanto?

Il progetto e le tre superfici. Niente numeri qui.

### 2. La risposta in una riga

La tesi, prima di tutto il resto. Candidata:

> Le tre superfici divergono di 20-32 punti percentuali su 15 temi, e la
> divergenza più grande non è fra i partiti e la stampa: è **dentro** i partiti,
> fra ciò che promettono e ciò che legiferano.

→ **Grafico 2** (scarto programmi ↔ leggi), solo i due estremi.

---

## Parte 1 — Il problema che abbiamo trovato — 3 slide

La parte più forte della presentazione, e la meno ovvia. È un errore di metodo
scoperto in corsa, non un risultato: raccontarlo come tale.

### 3. Stavamo usando il topic model per derivare le categorie su cui doveva essere mappato

Il circolo: l'NMF doveva mappare i temi su una tassonomia, e la tassonomia si
aspettava che uscisse dall'NMF. Un NMF non restituisce categorie politiche —
restituisce i gruppi di parole più regolari del corpus.

### 4. Al primo giro, 7 topic su 12 erano i template delle testate

`in evidenza`, `riproduzione riservata copyright ansa`, `vai all articolo su
raiplay`. E altri 2 erano parole funzione italiane: `si, ma, da, al, le`.

→ **Grafico 4a** (composizione dei topic, prima).

Il punto da far passare: non è un difetto dell'NMF. Quelle stringhe *sono* il
testo più regolare del corpus, quindi la struttura più forte che una
fattorizzazione può trovare.

### 5. Il boilerplate non si vede su una pagina, si vede sul corpus

Come `pulizia_corpus.py` lo riconosce: righe che ricorrono nel 30% dei documenti
di un dominio, o nel 2% del corpus su almeno 3 testate. 93.329 righe tolte da 31
domini su 80. Perdita mediana di testo sugli articoli tenuti: **0%**.

→ **Grafico 4b** (composizione dei topic, dopo).

---

## Parte 2 — L'ontologia come contratto — 3 slide

### 6. Le categorie si decidono dall'alto, da uno standard

MARPOR / Comparative Manifesto Project: 7 domini, 56 categorie, lo schema con cui
i programmi elettorali sono codificati a mano nella letteratura comparata.
56 sono troppe per un corpus italiano su sette mesi → 15 macrotemi.

Da dire: l'aggancio a MARPOR è voluto, dà un riferimento citabile e rende il
lavoro confrontabile con dati esterni.

### 7. La parte difficile non sono le 15 categorie, sono le tre unità di misura

**La slide chiave della metodologia.** La tabella del contratto:

| Layer | Unità | Come si assegna il tema |
|---|---|---|
| 1 — cosa dicono | paragrafo | distribuzione sui 15 temi |
| 2 — cosa fanno | atto (titolo) | etichetta singola |
| 3 — come se ne parla | articolo | dominante + distribuzione |

Conseguenza: si confrontano **quote**, mai conteggi.

### 8. Come mappiamo: lessico, non un secondo modello

350 pattern, regole leggibili una per una. Perché non un altro modello non
supervisionato: riporterebbe il problema della slide 3 un livello più su.

Chi non pesca in nessun lessico esce `non assegnato`. La **copertura** è la misura
di qualità, e va detta: L1 83,7% · L2 72,6% · L3 71,5%.

---

## Parte 3 — I tre layer — 4 slide

### 9. Le tre distribuzioni

→ **Grafico 1** (le tre distribuzioni sui 15 temi).

Slide di lettura, non di conclusione. Lasciare al pubblico il tempo di guardarla.

### 10. Il lavoro si promette il doppio di quanto si legiferi

18,3% dei paragrafi di programma contro 9,2% dei progetti di legge.

### 11. La sicurezza si legifera il triplo di quanto si prometta

2,8% contro 7,9%. Segno opposto rispetto al lavoro — ed è questo che rende
improbabile un artefatto del lessico, che sui due temi ha grana simile.

→ **Grafico 2**, ora per intero.

### 12. Stampa e Camera guardano due paesi diversi in politica estera

14,5% degli articoli contro 3,1% dei progetti di legge. Lo scarto singolo più
largo, e il più solido: poggia sul topic NMF meglio definito del corpus.

→ **Grafico 3** (scarto leggi ↔ stampa).

---

## Parte 4 — Quanto la politica parla di sé — 2 slide

La parte più citabile. Tenerla vicino alla fine.

### 13. Un articolo su dieci parla di politica, non di politiche

Nomine, sondaggi, candidature, retroscena: **10,35%** della stampa.

→ **Grafico 5** (la politica che parla di sé).

### 14. Ma il numero da solo non direbbe di chi è la scelta

0,55% nei programmi, 0,52% nei progetti di legge. Quando i partiti promettono e
la Camera legifera hanno quasi sempre un oggetto.

La linea di base vicina a zero è ciò che rende il 10,35% attribuibile a una
**scelta di inquadramento della stampa**. Con il solo layer 3 le due letture —
«i politici parlano di sé» e «la stampa racconta il gioco» — erano
indistinguibili.

Da dichiarare: il corpus viene da query su partiti e leader, quindi è già
selezionato attorno alle persone.

---

## Parte 5 — Limiti e prossimi passi — 3 slide

### 15. Cosa questo lavoro non misura

- Non misura **posizione**: di cosa si parla, non se a favore o contro.
- Non misura **consenso**. Il volume di copertura non è sostegno.
- Il lessico **non è validato** contro codifica umana.

Dirlo prima che lo chiedano.

### 16. Il layer 1 è pesato al contrario, e l'abbiamo scoperto provando a misurare la coerenza

I partiti con più attività legislativa hanno depositato i programmi più corti:
Lega 938 atti contro 14 paragrafi, M5S 936 contro 13. Il recupero via Wayback e
di quanto cambia.

→ **Grafico 6** (numerosità invertita, prima/dopo).

Slide onesta e interessante: un problema di dati trovato perché si è provato a
calcolare qualcosa, non perché si è guardato il dataset.

### 17. Dove va

- Validazione umana R1/R2 sui 15 macrotemi — sbloccata, il campione condiviso ora esiste;
- H1, l'indice di coerenza programmatica, sui partiti recuperati;
- il layer «chi li finanzia», fuori ontologia, tutto da fare.

---

## Cose da decidere insieme

1. **Il titolo.** «Politica 3D» è il nome interno del piano, non un titolo.
2. **Chi presenta cosa.** La parte 1 richiede di raccontare un errore: serve
   qualcuno a suo agio nel farlo.
3. **Quanto entrare nel metodo.** Le slide 7 e 8 sono le più tecniche. Se il tempo
   stringe, la 8 si comprime nella 7 e si rimanda al README.
4. **Se mostrare H1.** Adesso regge su due partiti. O si recupera il layer 1 e si
   mostra, o si tiene come lavoro futuro nella slide 17. Non una via di mezzo.
