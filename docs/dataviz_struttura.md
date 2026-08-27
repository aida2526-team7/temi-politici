# Struttura del dataviz

Sei grafici e tre schede. Destinazione `dashboard/`, oggi vuota.

Regola che vale per tutti, prima delle singole schede: **ogni numero che compare
sulla pagina si ricalcola dai file a build time**. Un numero scritto a mano è
giusto una volta sola e poi sbaglia in silenzio al primo aggiornamento. Le fonti
sono `reports/ontologia_mapping/*.csv` e `reports/topic_audit/*.csv`, già scritte
dalla pipeline con gli hash nei manifest.

Ogni grafico esce con una tabella affiancata (tab *Grafico* | *Tabella*) e
tooltip che portano i **conteggi** dietro le percentuali, non solo la percentuale.

---

## Le tre schede in cima

Non grafici: tre numeri grandi, uno per parte della storia, ciascuno con il link
alla sezione che lo dimostra.

| Scheda | Numero | Rimanda a |
|---|---|---|
| Quanto divergono promesse e leggi | **20,2 pp** | Grafico 2 |
| Quanto la politica parla di sé | **10,35%** contro 0,5% | Grafico 5 |
| Quanto il corpus era sporco | **7 topic su 12** | Grafico 4 |

Sopra la piega ci vanno queste e il paragrafo che dice cosa si sta guardando.
Nessun grafico: il primo grafico apre la sezione che lo prova.

---

## Grafico 1 — Le tre distribuzioni sui 15 macrotemi

**Cosa dimostra.** Che i tre layer hanno forme diverse. È la slide di lettura, non
di conclusione: qui il lettore si orienta.

**Forma.** Barre **orizzontali raggruppate**, 15 categorie × 3 layer. Orizzontali
perché i nomi dei macrotemi sono lunghi e in verticale diventano illeggibili.
Ordinate per il layer 2, che è il più affidabile dei tre.

**Colore.** Categorico a 3 valori, uno per layer — è l'unico grafico dove i tre
layer sono davvero paritari, quindi l'unico che merita un vero categorico.

**Dati.** `reports/ontologia_mapping/distribuzione_layer.csv`.

**Attenzione.** Le righe `non assegnato`, `politica non tematica` e `boilerplate`
**non** vanno mescolate ai 15 temi nella stessa scala: o si escludono con una nota
sul denominatore, o si mettono in un blocco separato sotto, staccato.

---

## Grafico 2 — Lo scarto fra ciò che si promette e ciò che si legifera

**Il grafico che porta la tesi.** Se ne resta uno solo, è questo.

**Cosa dimostra.** Che lo scarto ha due direzioni: lavoro e ambiente promessi più
di quanto si legiferi, sicurezza e sanità il contrario.

**Forma.** Barre **divergenti orizzontali** attorno allo zero, ordinate dallo
scarto più positivo al più negativo. Una barra per macrotema, lunghezza = punti
percentuali di differenza (L1 − L2).

**Colore.** *Emphasis, non categorico*: `Lavoro e imprese` e `Sicurezza e
criminalità` nell'accento, gli altri tredici in grigio. Sono i due estremi e sono
il punto; il resto è contesto che serve a far vedere che gli estremi sono estremi.

**Etichette.** Il valore direttamente sulle due barre in accento. Sulle altre no.
Nessuna griglia: c'è la linea dello zero e basta.

**Dati.** Colonna `scarto_l1_l2` dello stesso CSV.

---

## Grafico 3 — Lo scarto fra le leggi e la stampa

Stessa forma del 2, colonna `scarto_l2_l3`, accento su `Politica estera e difesa`.

Vale la pena **affiancarlo al 2**, stessa scala sull'asse: si vede a colpo d'occhio
che lo scarto stampa-leggi è più largo di quello promesse-leggi, e che il tema che
lo domina è un altro.

---

## Grafico 4 — Cosa ha cambiato la pulizia del corpus

**Cosa dimostra.** Che senza la pulizia il corpus non era analizzabile, e di
quanto.

**Forma.** Due barre impilate al 100%, affiancate: *prima* e *dopo*. Tre segmenti
— `boilerplate`, `non assegnato`, `assegnato a un macrotema`. La barra impilata
qui funziona perché i segmenti sono tre e la domanda è una composizione, non un
confronto di livelli.

**Colore.** Rampa a una tinta ordinata: il boilerplate è il segmento «peggiore»,
l'assegnato il «migliore». Non tre colori scorrelati.

**Alternativa da valutare insieme.** Uno slope chart sulla sola copertura
(63,2% → 75,0%): più semplice, dice meno.

**Dati.** La tabella in `reports/ontologia_mapping/mappatura.md`, sezione *Cosa ha
cambiato la pulizia*. **Da sistemare:** quei valori oggi stanno solo in prosa. Se
questo grafico entra, la pipeline deve scriverli in un CSV — vedi la regola in
cima.

---

## Grafico 5 — Quanto la politica parla di sé

**Cosa dimostra.** Lo scarto di venti a uno fra la stampa e i due layer politici.

**Forma.** **Griglia di unità**, non barre. La frase è «circa 10 articoli su 100
contro 1 su 200»: è un *N su M*, e la griglia di puntini lo fa vedere invece di
farlo leggere. Tre pannelli da 100 puntini, uno per layer, con i puntini pieni a
rappresentare la quota.

Il rischio della griglia: con 0,55% su 100 puntini si accende mezzo puntino.
Verificare guardando il PNG — se il pannello L1 sembra vuoto, il messaggio passa
lo stesso («praticamente zero») oppure no. Se non passa, ripiegare su tre barre
orizzontali con i valori etichettati.

**Colore.** Accento solo sul pannello stampa. Gli altri due in grigio: sono la
linea di base, e il fatto che siano quasi vuoti è tutto il contenuto.

**Dati.** `politica_non_tematica_pct` in `mapping_manifest.json`.

---

## Grafico 6 — Il layer 1 è pesato al contrario

**Cosa dimostra.** Che i partiti con più attività legislativa avevano i programmi
più corti, e cosa ha recuperato il Wayback.

**Forma.** **Scatter**, un punto per partito: paragrafi di programma sull'asse x,
progetti di legge sull'asse y, entrambi logaritmici. Con l'integrazione, una
freccia da dove stava il punto a dove sta ora — il movimento *è* il risultato.

**Colore.** Grigio per tutti; accento sui partiti recuperati. Etichette direttamente
sui punti, sono sette.

**Dati.** `layer1_per_programma.csv` e `layer2_per_gruppo.csv`.

**Attenzione all'asse log:** con valori da 13 a 938 serve, ma va detto in didascalia,
perché su scala log una distanza visiva non è una distanza numerica.

---

## Scelte tecniche da fare insieme

**Lo stack.** Quarto + Altair è quello naturale qui: il repo è Python, gli output
sono CSV, e Quarto dà i tabset *Grafico | Tabella* senza scrivere JavaScript. È la
mia raccomandazione. L'alternativa è una pagina HTML statica costruita a mano, che
dà più controllo sulla tipografia e costa parecchio di più.

**Una pagina o due.** Tutto in `dashboard/index.qmd`, oppure una pagina di
racconto più una di appendice metodologica. Dipende da chi legge: se è la
commissione, una sola pagina che si scorre.

**Il rapporto con le slide.** I grafici 2, 3 e 5 servono a entrambe. Vanno esportati
in PNG per le slide dallo stesso codice che genera la pagina, mai rifatti a parte —
altrimenti fra un mese le due versioni non dicono più la stessa cosa.

---

## Da sistemare nella pipeline prima di costruire

1. I numeri del confronto prima/dopo la pulizia stanno solo in prosa dentro
   `mappatura.md`. Servono in CSV (grafico 4).
2. `layer1_per_programma.csv` non porta il gruppo parlamentare corrispondente: il
   raccordo con il layer 2 oggi è scritto in
   `config/programmi_integrazione.json` solo per i partiti integrati. Per il
   grafico 6 serve per tutti quelli che si vogliono mostrare.
3. Le quote per gruppo del layer 2 sono conteggi grezzi, non quote: il grafico
   deve normalizzarle, oppure lo fa la pipeline. Meglio la pipeline, così tabella
   e grafico leggono lo stesso numero.
