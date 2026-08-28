# Audit riproducibile degli output NMF

> Report generato automaticamente da `scripts/run_topic_audit.py`.

## Fatti quantitativi

### Distribuzione dei topic

| Topic | Articoli | Percentuale |
|---|---|---|
| 0 | 22016 | 20.572% |
| 1 | 892 | 0.833% |
| 2 | 335 | 0.313% |
| 3 | 19646 | 18.357% |
| 4 | 17803 | 16.635% |
| 5 | 2920 | 2.728% |
| 6 | 334 | 0.312% |
| 7 | 28247 | 26.394% |
| 8 | 172 | 0.161% |
| 9 | 12928 | 12.080% |
| 10 | 754 | 0.705% |
| 11 | 974 | 0.910% |

Output tabellare: [`topic_distribution.csv`](topic_distribution.csv).

### Confidenza normalizzata

| Metrica | Valore |
|---|---|
| min | 0.16743736 |
| mean | 0.57460246 |
| median | 0.55011243 |
| p25 | 0.43306429 |
| p75 | 0.70459152 |
| p90 | 0.83675362 |
| p99 | 0.98274268 |
| exactly_1_percentage | 0.29433476 |
| below_0.40_percentage | 18.08617000 |
| below_0.50_percentage | 39.81368143 |
| below_0.60_percentage | 59.06878089 |

La confidenza è `max(pesi NMF) / somma(pesi NMF)`: non è una probabilità calibrata.
Output completo: [`confidence_summary.csv`](confidence_summary.csv).

### Duplicazioni

| Sezione | Metrica | Valore |
|---|---|---|
| exact_excerpt | records_in_duplicate_groups | 4210 |
| exact_excerpt | duplicate_groups | 1757 |
| exact_excerpt | largest_group | 253 |
| exact_title_excerpt | records_in_duplicate_groups | 1570 |
| exact_title_excerpt | duplicate_groups | 749 |
| exact_title_excerpt | largest_group | 4 |
| near_duplicate_proxy | prefix_length | 300 |
| near_duplicate_proxy | records_in_duplicate_groups | 7127 |
| near_duplicate_proxy | duplicate_groups | 2941 |
| near_duplicate_proxy | largest_group | 253 |
| near_duplicate_proxy | definition | same normalized prefix of the review excerpt |

Output strutturato: [`duplicate_summary.json`](duplicate_summary.json).

### Parametri registrati dal classificatore

```json
{
  "created_at_utc": "2026-08-27T23:51:39.200979+00:00",
  "input": "mediacloud_fulltext.jsonl",
  "articles": 107021,
  "tfidf_shape": [
    107021,
    1721860
  ],
  "n_topics": 12,
  "requested_n_topics": 12,
  "min_df": 3,
  "max_df": 0.85,
  "random_state": 42,
  "pulizia": {
    "documenti": 118756,
    "domini": 80,
    "domini_con_template": 32,
    "domini_sotto_soglia": 8,
    "righe_template_globali": 1,
    "righe_template_rimosse": 105884,
    "scartati_senza_testo": 4993,
    "scartati_duplicati": 4811,
    "lingua_corretta": 0,
    "documenti_finali": 108952,
    "lingue_finali": {
      "it": 107023,
      "en": 1455,
      "de": 397,
      "fr": 65,
      "pt": 10,
      "ar": 1,
      "es": 1
    },
    "template_per_dominio": {
      "varesenews.it": [
        [
          "la community di varesenews",
          0.9809187279151943
        ],
        [
          "ultimi commenti",
          0.9809187279151943
        ],
        [
          "loro ne fanno gia parte",
          0.9809187279151943
        ],
        [
          "l'email e richiesta ma non verra mostrata ai visitatori. il contenuto di questo commento esprime il pensiero dell'autore e non rappresenta la linea editoriale di varesenews.it, che rimane autonoma e indipendente. i messaggi inclusi nei commenti non sono testi giornalistici, ma post inviati dai singoli lettori che possono essere automaticamente pubblicati senza filtro preventivo. i commenti che includano uno o piu link a siti esterni verranno rimossi in automatico dal sistema.",
          0.9809187279151943
        ],
        [
          "accedi o registrati per commentare questo articolo.",
          0.9802120141342756
        ],
        [
          "tag articolo",
          0.8742049469964664
        ],
        [
          "- bustocco-71 su guasto tra le stazioni di varese e gallarate: ritardi e modifiche al servizio sulle tratte di porto ceresio e mendrisio",
          0.8088339222614841
        ],
        [
          "- principe.rosso su e pronta la prima scuola realizzata con il pnrr in provincia di varese. e le altre? ecco a che punto siamo",
          0.8088339222614841
        ],
        [
          "- felice su anche a varese la maturita si festeggia a colpi di uova, spumante e farina. e i rifiuti restano li",
          0.8088339222614841
        ],
        [
          "- felice su e pronta la prima scuola realizzata con il pnrr in provincia di varese. e le altre? ecco a che punto siamo",
          0.8088339222614841
        ]
      ],
      "tempi.it": [
        [
          "i commenti sono aperti solo per gli utenti registrati. abbonati subito per commentare!",
          0.5113636363636364
        ],
        [
          "articoli correlati",
          0.5113636363636364
        ],
        [
          "il quotidiano online + il mensile digitale e cartaceo",
          0.4602272727272727
        ],
        [
          "digitale",
          0.4602272727272727
        ],
        [
          "full",
          0.4602272727272727
        ],
        [
          "il quotidiano online + il mensile digitale",
          0.4602272727272727
        ],
        [
          "0 commenti",
          0.4431818181818182
        ],
        [
          "non ci sono ancora commenti.",
          0.4431818181818182
        ]
      ],
      "italiachecambia.org": [
        [
          "valuteremo il suo inserimento all'interno di un prossimo episodio.",
          0.5961538461538461
        ],
        [
          "segnala una notizia",
          0.5961538461538461
        ],
        [
          "segnalaci una notizia interessante per io non mi rassegno.",
          0.5961538461538461
        ],
        [
          "trascrizione episodio",
          0.5576923076923077
        ],
        [
          "fonti",
          0.5384615384615384
        ],
        [
          "questo episodio e disponibile anche su youtube",
          0.4423076923076923
        ]
      ],
      "rai.it": [
        [
          "pagina 556 - documentariarchivio dei documentari, clicca qui",
          0.8549422336328626
        ],
        [
          "cultura e spettacolofilm - \"l’hangar rosso\", vai all'articolo, al trailer e alle clip 1 e 2 teatro - \"il barbiere di siviglia - opera buffa in due atti\", vai all'articolo e al video festival - \"60° festival teatrale di borgio verezzi\", vai all'articolo museo - \"museo del disco d’epoca\", vai all'articolo film in sala e quelli in arrivo, guarda i trailer clicca qui la nottola, programmazione roma e lazio clicca qui tutti i concerti di musica leggera",
          0.8549422336328626
        ],
        [
          "pagina 690 - lottoestrazioni del lotto",
          0.8549422336328626
        ],
        [
          "pagina 752 - la nuova tv digitale",
          0.8549422336328626
        ],
        [
          "pagina 546 - magazine tvi mestieri di mirko – speciale alto adige estate, dal 24 luglio su raiplay con un nuovo episodio, vai all'articolo under 25 – giovani talenti, dal 26 maggio su raiplay, vai all'articolo e al video promo il club - canzoni sotto la pelle, dall’ 8 maggio su raiplay, vai all'articolo e al video promo",
          0.8549422336328626
        ]
      ],
      "adnkronos.com": [
        [
          "scoop su air force one donato dal qatar, nyt nel mirino di trump: mandati di comparizione per i reporter",
          0.4385716310046762
        ],
        [
          "in evidenza universita, a leonardo maria del vecchio la laurea honoris causa in diritto innovazione tecnologica e sostenibilita",
          0.4385716310046762
        ],
        [
          "in evidenza 'sindrome di rett: bisogni, prospettive e priorita emergenti dall’europa all’italia', digital talk adnkronos - acadia",
          0.4385716310046762
        ],
        [
          "in evidenza presentato lo studio 'sinergie tra agricoltura e trasporto aereo per la produzione di saf'",
          0.4385716310046762
        ],
        [
          "in evidenza presentato a roma il 'forum delle citta della notte', aurigemma: \"il tema della sicurezza non ha colore politico\"",
          0.4385716310046762
        ]
      ],
      "gazzettadiparma.it": [
        [
          "© riproduzione riservata",
          0.9875091844232182
        ],
        [
          "gazzetta di parma srl - p.i. 02361510346 - codice sdi: m5uxcr1",
          0.9875091844232182
        ],
        [
          "© gazzetta di parma - riproduzione riservata",
          0.9875091844232182
        ],
        [
          "roma",
          0.4739162380602498
        ]
      ],
      "laverita.info": [
        [
          "prosegui con la lettura >",
          0.8961038961038961
        ],
        [
          "rinnova il tuo abbonamento per proseguire con la lettura >",
          0.8961038961038961
        ],
        [
          "contenuto riservato agli abbonati",
          0.8961038961038961
        ]
      ],
      "tageszeitung.it": [
        [
          "ahnliche artikel",
          1.0
        ],
        [
          "lesen sie die netiquette und die nutzerbedingungen",
          0.7555555555555555
        ],
        [
          "du musst dich einloggen um die kommentare zu lesen.",
          0.7555555555555555
        ]
      ],
      "avvenire.it": [
        [
          "© riproduzione riservata",
          1.0
        ],
        [
          "seguici anche su google discover di avvenire",
          0.7085478887744593
        ]
      ],
      "ilsole24ore.com": [
        [
          "i punti chiave",
          0.4262485481997677
        ],
        [
          "3' di lettura",
          0.3362369337979094
        ]
      ],
      "ilroma.net": [
        [
          "copyright @ - nuovo giornale roma societa cooperativa - corso garibaldi, 32 - napoli - 80142 - partita iva 07406411210 - la societa percepisce i contributi di cui al decreto legislativo 15 maggio 2017, n. 70. indicazione resa ai sensi della lettera f) del comma 2 dell’articolo 5 del medesimo decreto legislativo - il giornale aderisce alla file (federazione italiana liberi editori) e all'iap (istituto di autodisciplina pubblicitaria) tutti i diritti sono riservati. nessuna parte di questo giornale puo essere riprodotta con alcun mezzo e/o diffusa in alcun modo e a qualsiasi titolo",
          0.9952718676122931
        ],
        [
          "tutte le novita",
          0.9869976359338062
        ]
      ],
      "ilmanifesto.it": [
        [
          "la storia sulle ferite del g8. il 17 luglio in edicola con il manifesto un inserto straordinario su quelle giornate del 2001.",
          0.8938888888888888
        ],
        [
          "genova, 25 anni dopo.",
          0.8938888888888888
        ]
      ],
      "ilgiornaledivicenza.it": [
        [
          "il giornale di vicenza e su whatsapp. clicca qui per iscriverti al nostro canale e rimanere aggiornato in tempo reale.",
          0.9784615384615385
        ]
      ],
      "ansa.it": [
        [
          "riproduzione riservata © copyright ansa",
          0.9302450641468848
        ]
      ],
      "larena.it": [
        [
          "l’arena e su whatsapp. clicca qui per iscriverti al nostro canale e rimanere aggiornato in tempo reale.",
          0.9815384615384616
        ]
      ],
      "ligurianotizie.it": [
        [
          "non perdere gli ultimi aggiornamenti su cronaca, eventi e politica in liguria! iscriviti sui canali di liguria notizie di telegram, facebook, twitter e youtube",
          0.4247619047619048
        ]
      ],
      "laprovinciadicomo.it": [
        [
          "© riproduzione riservata",
          1.0
        ]
      ],
      "leggo.it": [
        [
          "© riproduzione riservata",
          0.9075
        ]
      ],
      "italpress.com": [
        [
          "(italpress).",
          0.6800368833563855
        ]
      ],
      "nove.firenze.it": [
        [
          "approfondimenti",
          0.43238095238095237
        ]
      ]
    },
    "template_globali": [
      [
        "© riproduzione riservata",
        0.048039677995217085
      ]
    ]
  },
  "stopwords": 348
}
```

## Evidenze per topic

### Topic 0

- Articoli: 22016 (20.572%).
- Termini registrati: euro, regionale, regione, territorio, risorse, imprese, piano, interventi, lavoro, cittadini, sistema, commissione
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | ansa.it | 3588 | 16.297% |
| 2 | lanazione.it | 2385 | 10.833% |
| 3 | ilrestodelcarlino.it | 1425 | 6.473% |
| 4 | iltempo.it | 817 | 3.711% |
| 5 | varesenews.it | 747 | 3.393% |
| 6 | lastampa.it | 737 | 3.348% |
| 7 | ilgiorno.it | 724 | 3.289% |
| 8 | ilgiornale.it | 655 | 2.975% |
| 9 | lagazzettadelmezzogiorno.it | 585 | 2.657% |
| 10 | adnkronos.com | 572 | 2.598% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 1947 |
| 2026-02 | 2363 |
| 2026-03 | 2416 |
| 2026-04 | 2928 |
| 2026-05 | 3236 |
| 2026-06 | 3341 |
| 2026-07 | 3717 |
| 2026-08 | 2068 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.06081743 | lasicilia.it | 2026-07-21 | La Sicilia di Schifani risanata e competitiva: «Il mio operato rigoroso e trasparente». Ma per opposizioni è un'altra storia  - La Sicilia |
| 2 | 0.04454339 | adnkronos.com | 2026-05-12 | Cni: "Rischio idrogeologico? Non solo fondi, da liberi professionisti 'serbatoio competenze' a cui gli enti locali dovrebbero maggiormente attingere" |
| 3 | 0.04419258 | affaritaliani.it | 2026-07-24 | Lombardia, via libera a rendiconto e assestamento: più fondi a sanità e infrastrutture, scontro sui tagli al welfare |
| 4 | 0.04411603 | ilfattoquotidiano.it | 2026-06-16 | PNRR: asili, studentati e Case della comunità, le grandi incompiute a 15 giorni dalla scadenza \| Il Fatto Quotidiano.it |
| 5 | 0.04384033 | nove.firenze.it | 2026-03-31 | Variazione in bilancio per chiudere i conti 2025 della sanità toscana • Nove da Firenze |
| 6 | 0.04307591 | nove.firenze.it | 2026-03-16 | Europa: in Regione il punto sulla gestione dei fondi Ue • Nove da Firenze |
| 7 | 0.04171815 | ansa.it | 2026-02-19 | Nuovo confronto in Assemblea legislativa sulla liste d'attesa - Notizie - Ansa.it |
| 8 | 0.04154462 | lagazzettadelmezzogiorno.it | 2026-07-08 | Crisafi (Remind) “Costruiamo insieme l’Italia che abiteremo” - Gazzetta del Mezzogiorno |
| 9 | 0.04150883 | vocedimantova.it | 2026-07-08 | Crisafi (Remind) “Costruiamo insieme l’Italia che abiteremo” \| la Voce Di Mantova |
| 10 | 0.04145107 | iltempo.it | 2026-07-08 | Crisafi (Remind) “Costruiamo insieme l'Italia che abiteremo” – Il Tempo |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.01457230 | 0.50248776 | lanazione.it | 2026-01-22 | Sassaiola contro il treno, le polemiche: “Contesto preoccupante per degrado e insicurezza” |
| 2 | 0.02330242 | 0.62939871 | lanazione.it | 2026-06-18 | L’emergenza nella sanità: "All’ospedale di Branca servono subito rinforzi" |
| 3 | 0.04307591 | 0.90120222 | nove.firenze.it | 2026-03-16 | Europa: in Regione il punto sulla gestione dei fondi Ue • Nove da Firenze |
| 4 | 0.01316662 | 0.42546852 | varesenews.it | 2026-05-21 | Elly Schlein a Solaro per incontrare i lavoratori Electrolux |
| 5 | 0.01626500 | 0.61998645 | varesenews.it | 2026-05-01 | Sicurezza nei locali pubblici, convegno a Ville Ponti il 29 giugno |

### Topic 1

- Articoli: 892 (0.833%).
- Termini registrati: agenzia vista, agenzia, bertoldi states, milei futuro, nato milei, states trump, studentesche lavori, partecipazione studentesca, studentesca processi, pubblicit unesco, decisionali alessandro, rocca tempo
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | iltempo.it | 888 | 99.552% |
| 2 | ansa.it | 1 | 0.112% |
| 3 | gazzettadiparma.it | 1 | 0.112% |
| 4 | giornaledibrescia.it | 1 | 0.112% |
| 5 | lagazzettadelmezzogiorno.it | 1 | 0.112% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 127 |
| 2026-02 | 96 |
| 2026-03 | 166 |
| 2026-04 | 165 |
| 2026-05 | 128 |
| 2026-06 | 170 |
| 2026-07 | 40 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.18263180 | iltempo.it | 2026-03-23 | Il Ministro Tajani vota per il referendum sulla giustizia a Fiuggi – Il Tempo |
| 2 | 0.18027580 | iltempo.it | 2026-01-16 | Takaichi fa gli auguri di compleanno a Meloni, l'applauso della delegazione giapponese – Il Tempo |
| 3 | 0.17996633 | iltempo.it | 2026-04-10 | Meloni in Senato: Non faremo misure demagogiche che devastano conti Stato come hanno fatto altri – Il Tempo |
| 4 | 0.17839227 | iltempo.it | 2026-02-10 | Calenda: Vannacci da sempre sostiene le ragioni di Putin – Il Tempo |
| 5 | 0.17473529 | iltempo.it | 2026-02-10 | Giorno del Ricordo, l'applauso dell'Aula di Montecitorio – Il Tempo |
| 6 | 0.17441768 | iltempo.it | 2026-06-18 | Meloni arriva al Consiglio Ue di Bruxelles – Il Tempo |
| 7 | 0.17428161 | iltempo.it | 2026-07-10 | Rampelli: Non si possono fare banchetti sull'Altare della Patria – Il Tempo |
| 8 | 0.17150497 | iltempo.it | 2026-04-30 | Salvini: Sono sempre d'accordo con la Presidente del Consiglio – Il Tempo |
| 9 | 0.17066835 | iltempo.it | 2026-03-22 | Elly Schlein vota per il Referendum sulla giustizia – Il Tempo |
| 10 | 0.17026578 | iltempo.it | 2026-04-09 | Meloni entra in Senato per informativa in Aula – Il Tempo |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.12002266 | 0.92145347 | iltempo.it | 2026-01-16 | Meloni invita Takaichi a Roma: Può nascere una bella amicizia – Il Tempo |
| 2 | 0.14572195 | 0.93908767 | iltempo.it | 2026-01-28 | Calenda: "Salvini non ha idee, segue solo la convenienza" – Il Tempo |
| 3 | 0.08816660 | 0.83179050 | iltempo.it | 2026-02-16 | Emergenza maltempo, Meloni: "Stiamo cercando di dare una risposta complessiva alle aree colpite" – Il Tempo |
| 4 | 0.09682455 | 0.79644977 | iltempo.it | 2026-05-22 | Meloni: Non si può chiedere a imprese di correre sui mercati se in Ue le freniamo con burocrazia – Il Tempo |
| 5 | 0.12972328 | 0.93852392 | iltempo.it | 2026-06-05 | Meloni non riesce a prendere aereo e salta vertice Ue, Conte: Lo guidava Salvini? – Il Tempo |

### Topic 2

- Articoli: 335 (0.313%).
- Termini registrati: carlo antini, antini, controtempo, rieti corriere, corriere rieti, attualita esteri, tempo tv, personaggi opinioni, corriere viterbo, edicola digitale, rieti, viterbo
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | iltempo.it | 299 | 89.254% |
| 2 | laverita.info | 26 | 7.761% |
| 3 | italpress.com | 3 | 0.896% |
| 4 | askanews.it | 2 | 0.597% |
| 5 | lagazzettadelmezzogiorno.it | 2 | 0.597% |
| 6 | adnkronos.com | 1 | 0.299% |
| 7 | repubblica.it | 1 | 0.299% |
| 8 | unionesarda.it | 1 | 0.299% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 42 |
| 2026-02 | 56 |
| 2026-03 | 43 |
| 2026-04 | 51 |
| 2026-05 | 39 |
| 2026-06 | 42 |
| 2026-07 | 45 |
| 2026-08 | 17 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.24819039 | iltempo.it | 2026-06-24 | Meloni "Nel 2025 dal Governo 160 milioni di euro contro le dipendenze" – Il Tempo |
| 2 | 0.24563381 | iltempo.it | 2026-06-10 | Meloni "L'Italia non è la repubblica delle banane" – Il Tempo |
| 3 | 0.24486258 | iltempo.it | 2026-02-27 | Salvini "Lavorerò per le Olimpiadi di Roma 2040" – Il Tempo |
| 4 | 0.24420230 | iltempo.it | 2026-04-23 | Energia, Meloni "L'Europa sia più coraggiosa" – Il Tempo |
| 5 | 0.24370281 | iltempo.it | 2026-04-29 | Tajani "Sull'energia l'Unione Europea deve essere più elastica" – Il Tempo |
| 6 | 0.24321738 | iltempo.it | 2026-06-15 | Lega, Guidesi "Discussione sia strutturale, non contingente o elettorale" – Il Tempo |
| 7 | 0.24313117 | iltempo.it | 2026-03-07 | Iran, Lupi "Le iniziative della Meloni vanno verso la via diplomatica" – Il Tempo |
| 8 | 0.24221985 | iltempo.it | 2026-05-11 | Tajani "L'Iran non può avere l'arma nucleare" – Il Tempo |
| 9 | 0.24146787 | iltempo.it | 2026-04-15 | Calenda "Clamoroso che solo ora si riconosca che Trump sia un pericolo" – Il Tempo |
| 10 | 0.24068345 | iltempo.it | 2026-04-28 | Renzi "A Bologna fatti vergognosi, il 25 aprile è la festa della libertà" – Il Tempo |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.21889298 | 0.97981129 | iltempo.it | 2026-03-05 | Iran, Tajani "Abbiamo aiutato 10 mila italiani a lasciare le zone a rischio" – Il Tempo |
| 2 | 0.21260330 | 0.98814794 | iltempo.it | 2026-05-28 | Vannacci "In Sicilia grandissimi problemi, valutazione governo non lusinghiera" – Il Tempo |
| 3 | 0.18339785 | 0.95784921 | iltempo.it | 2026-07-29 | Tajani "Aperti alle preferenze ma serve accordo nel centrodestra" – Il Tempo |
| 4 | 0.17964127 | 0.97832786 | iltempo.it | 2026-07-29 | Tajani "No a riconoscimento demagogico o fittizio dello Stato Palestinese" – Il Tempo |
| 5 | 0.16823711 | 0.96320584 | iltempo.it | 2026-08-26 | Tajani a San Patrignano "Sostegno a comunità, recupero ragazzi opera meritoria" – Il Tempo |

### Topic 3

- Articoli: 19646 (18.357%).
- Termini registrati: trump, meloni, iran, tajani, usa, uniti, esteri, ministro, ue, europa, guerra, italia
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | ansa.it | 2495 | 12.700% |
| 2 | iltempo.it | 1477 | 7.518% |
| 3 | ilgiornale.it | 1095 | 5.574% |
| 4 | askanews.it | 1044 | 5.314% |
| 5 | adnkronos.com | 918 | 4.673% |
| 6 | ilmessaggero.it | 834 | 4.245% |
| 7 | italpress.com | 826 | 4.204% |
| 8 | repubblica.it | 801 | 4.077% |
| 9 | lastampa.it | 772 | 3.930% |
| 10 | laverita.info | 591 | 3.008% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 1992 |
| 2026-02 | 1853 |
| 2026-03 | 2882 |
| 2026-04 | 3576 |
| 2026-05 | 2773 |
| 2026-06 | 3127 |
| 2026-07 | 2091 |
| 2026-08 | 1352 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.08041879 | repubblica.it | 2026-03-19 | Guerra in Iran, le news del 19 marzo - la Repubblica |
| 2 | 0.08024557 | mediaset.it | 2026-04-17 | Guerra Iran, oggi in diretta: Trump: "Non ci saremo per l'Italia" |
| 3 | 0.08005112 | repubblica.it | 2026-06-24 | Le news del 24 giugno. Guerra in Iran. Rutte: “500 aerei Usa sono decollati da basi in Italia" - la Repubblica |
| 4 | 0.07984504 | repubblica.it | 2026-06-17 | Guerra in Iran, le news del 17 giugno \| Venerdì la firma dell'accordo Usa - Iran - la Repubblica |
| 5 | 0.07966427 | ilsole24ore.com | 2026-04-08 | Guerra in Iran, ultime notizie - Iran blocca Hormuz dopo raid Israele in Libano. Macron: tregua deve includerlo - Il Sole 24 ORE |
| 6 | 0.07905145 | repubblica.it | 2026-04-09 | Guerra in Iran, le news del 9 aprile. Idf: “Evacuare Beirut sud”. Hormuz ancora chiuso - la Repubblica |
| 7 | 0.07871747 | ilgiornale.it | 2026-03-10 | Allarme degli 007 Usa: "Teheran vuole minare Hormuz". Trump: "Le rimuova o conseguenze mai viste". Italia, Germania e Inghilterra al lavoro per proteggere le navi - il Giornale |
| 8 | 0.07830863 | lastampa.it | 2026-04-08 | Guerra Iran, le news dopo lâattacco di Usa Israele. La diretta - La Stampa |
| 9 | 0.07812462 | repubblica.it | 2026-04-17 | Guerra in Iran, le news del 17 aprile in diretta \| Tregua tra Israele e Libano - la Repubblica |
| 10 | 0.07776830 | mediaset.it | 2026-03-10 | Guerra Iran, oggi in diretta: Trump minaccia Teheran sul petrolio |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.00723078 | 0.19597831 | ansa.it | 2026-06-22 | Zan (Pd), 'diritti civili bersaglio delle destre in Europa, noi guardiamo al futuro' - La voce degli Eurodeputati - Ansa.it |
| 2 | 0.04238528 | 0.85724203 | ilgiornale.it | 2026-07-03 | Trump sferza Nato (e Italia). "Noi spendiamo più di tutti" - il Giornale |
| 3 | 0.02116497 | 0.36294747 | italpress.com | 2026-07-24 | Confronto tra Meloni e Giorgetti sul caro carburanti, allo studio ipotesi accise mobili Agenzia di stampa Italpress - Italpress |
| 4 | 0.05021079 | 0.97692370 | italpress.com | 2026-06-15 | Accordo Iran-Stati Uniti, le reazioni: notizie e dichiarazioni 15 giugno |
| 5 | 0.02614432 | 0.69145290 | ladige.it | 2026-03-14 | Tajani, le sanzioni a Mosca vanno assolutamente mantenute |

### Topic 4

- Articoli: 17803 (16.635%).
- Termini registrati: sindaco, centrodestra, partito, candidato, centrosinistra, coalizione, forza italia, forza, pd, elezioni, vannacci, lega
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | lanazione.it | 2037 | 11.442% |
| 2 | ansa.it | 1642 | 9.223% |
| 3 | ilrestodelcarlino.it | 1186 | 6.662% |
| 4 | gazzettadelsud.it | 1002 | 5.628% |
| 5 | ilgiornale.it | 726 | 4.078% |
| 6 | ilmattino.it | 702 | 3.943% |
| 7 | lastampa.it | 685 | 3.848% |
| 8 | repubblica.it | 621 | 3.488% |
| 9 | ilgiorno.it | 610 | 3.426% |
| 10 | ilgazzettino.it | 505 | 2.837% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 1214 |
| 2026-02 | 2024 |
| 2026-03 | 1911 |
| 2026-04 | 2481 |
| 2026-05 | 3385 |
| 2026-06 | 3245 |
| 2026-07 | 2134 |
| 2026-08 | 1409 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.08332668 | ilfoglio.it | 2026-05-25 | De Luca a valanga a Salerno. A Venezia il centrodestra verso la vittoria al primo turno. I risultati delle comunali |
| 2 | 0.07974484 | ilgiornale.it | 2026-05-25 | Amministrative, da Arezzo a Reggio Calabria: tutte le sfide-chiave nelle città  - il Giornale |
| 3 | 0.07889365 | ilfattoquotidiano.it | 2026-05-23 | Elezioni amministrative 2026: Venezia, Salerno, Messina e Reggio Calabria le sfide chiave \| Il Fatto Quotidiano.it |
| 4 | 0.07568849 | adnkronos.com | 2026-05-06 | Elezioni amministrative 2026, dove si vota il 24 e 25 maggio: comuni, schieramenti e candidati |
| 5 | 0.07456429 | ilmattino.it | 2026-05-25 | Elezioni Comunali 24 e 25 maggio 2026, i risultati in diretta, le preferenze e gli exit poll in provincia di Avellino, Benevento, Caserta Napoli e Salerno |
| 6 | 0.07349737 | repubblica.it | 2026-05-22 | Elezioni comunali 2026: dove e come si vota il 24 e 25 maggio - la Repubblica |
| 7 | 0.07330536 | avvenire.it | 2026-05-22 | Le “bizze” della Lega, la sfida per Venezia, il caso De Luca: tutto quello che c'è da sapere sulle Comunali |
| 8 | 0.07327384 | agi.it | 2026-05-24 | Da Venezia a Reggio Calabria, oggi 6 milioni e mezzo di italiani |
| 9 | 0.07311449 | repubblica.it | 2026-05-24 | Comunali 2026, dove e come si vota - la Repubblica |
| 10 | 0.07207942 | agi.it | 2026-05-23 | Urne aperte per 6 milioni di italiani per le elezioni comunali |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.01060901 | 0.38013459 | askanews.it | 2026-08-03 | Centrosinistra,Renzi: pronti a primarie, ma poi nessuno si tiri indietro |
| 2 | 0.01705890 | 0.46471431 | ansa.it | 2026-07-09 | Donzelli, su preferenze obiettivo emendamento unitario del centrodestra - Ultima ora - Ansa.it |
| 3 | 0.01790378 | 0.69506848 | giornaledibrescia.it | 2026-07-14 | ++ Tensioni al comizio di Vannacci a Pescara, interviene la polizia ++ \| Giornale di Brescia |
| 4 | 0.01709952 | 0.50643967 | ilgiornaledivicenza.it | 2026-04-22 | Mara Bizzotto succede a Bitonci: è sottosegretaria di Stato al MIMIT \| G. di Vicenza |
| 5 | 0.01826546 | 0.34596070 | iltempo.it | 2026-06-15 | Attenzione, "compri" Vannacci e ti arrivano a casa Conte e Schlein. L'analisi di Capezzone – Il Tempo |

### Topic 5

- Articoli: 2920 (2.728%).
- Termini registrati: agenzia vista, agenzia, vista, jakhnagiev, alexander jakhnagiev, vista alexander, alexander, fonte agenzia, fonte, vista roma, immobile asta, tuo immobile
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | agi.it | 844 | 28.904% |
| 2 | ilmessaggero.it | 821 | 28.116% |
| 3 | affaritaliani.it | 488 | 16.712% |
| 4 | ilmattino.it | 411 | 14.075% |
| 5 | iltempo.it | 140 | 4.795% |
| 6 | ilgazzettino.it | 81 | 2.774% |
| 7 | italpress.com | 71 | 2.432% |
| 8 | askanews.it | 12 | 0.411% |
| 9 | repubblica.it | 10 | 0.342% |
| 10 | leggo.it | 7 | 0.240% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 125 |
| 2026-02 | 198 |
| 2026-03 | 413 |
| 2026-04 | 550 |
| 2026-05 | 440 |
| 2026-06 | 511 |
| 2026-07 | 461 |
| 2026-08 | 222 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.17679867 | ilmessaggero.it | 2026-03-14 | Il dietro la tenda dell'intervista con Conte del direttore di Agenzia Vista Alexander Jakhnagiev |
| 2 | 0.17458065 | ilmessaggero.it | 2026-06-11 | Meloni esce dal Senato e saluta il direttore di Agenzia Vista Alexander Jakhnagiev a fine seduta |
| 3 | 0.16135288 | ilmessaggero.it | 2026-04-30 | Salvini: Sono sempre d’accordo con la Presidente del Consiglio |
| 4 | 0.15989826 | ilmessaggero.it | 2026-04-15 | L'abbraccio tra Meloni e Zelensky all'arrivo del Presidente ucraino a Palazzo Chigi |
| 5 | 0.15434167 | ilmessaggero.it | 2026-04-28 | Meloni: Su Patto di Stabilità non va esclusa deroga generale |
| 6 | 0.15091351 | ilmessaggero.it | 2026-06-13 | Vannacci: La Costituzione è antifascista? Non mi risulta |
| 7 | 0.15027019 | ilmessaggero.it | 2026-02-17 | Il Presidente Mattarella allAmbasciata della Santa Sede a Roma per i 97 anni dei Patti Lateranensi |
| 8 | 0.14990488 | ilmessaggero.it | 2026-04-15 | Zelensky arriva a Palazzo Chigi per incontro con Meloni. La pioggia e l’ingresso in macchina |
| 9 | 0.14853834 | ilmessaggero.it | 2026-03-23 | Meloni, il selfie con le sostenitrici dopo aver votato |
| 10 | 0.14754062 | ilmessaggero.it | 2026-05-08 | Meloni incontra il Segretario Usa Marco Rubio a Palazzo Chigi |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.08916875 | 0.87428561 | affaritaliani.it | 2026-07-02 | 250esimo Usa, Arianna Meloni alla festa per l'Indipendenza americana a Villa Taverna |
| 2 | 0.04768090 | 0.74728190 | affaritaliani.it | 2026-08-06 | Boccia (Pd) su conti pubblici a Giorgetti: Non possiamo affidarci al Governo a occhi chiusi |
| 3 | 0.04702148 | 0.66862469 | agi.it | 2026-05-04 | Meloni: Per evitare crisi migratoria bisogna combattere trafficanti e cooperare con Paesi origine |
| 4 | 0.06134303 | 0.75874510 | agi.it | 2026-05-27 | Meloni sul Pnrr: Non ci rimane che fare l'ultimo miglio, il piÃ¹ impegnativo |
| 5 | 0.09445854 | 0.86812926 | ilmessaggero.it | 2026-03-26 | Stefania Craxi nuovo capogruppo FI al Senato: Marina Berlusconi non è adusa a mettere becco |

### Topic 6

- Articoli: 334 (0.312%).
- Termini registrati: avellino, irpinia, pratola, reg, serra, ariano, grottaminarda, corriere, magia, irpini, momenti, campania
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | corriereirpinia.it | 324 | 97.006% |
| 2 | lagazzettadelmezzogiorno.it | 4 | 1.198% |
| 3 | ansa.it | 2 | 0.599% |
| 4 | askanews.it | 1 | 0.299% |
| 5 | giornaledibrescia.it | 1 | 0.299% |
| 6 | ilmattino.it | 1 | 0.299% |
| 7 | lanazione.it | 1 | 0.299% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 20 |
| 2026-02 | 27 |
| 2026-03 | 44 |
| 2026-04 | 62 |
| 2026-05 | 76 |
| 2026-06 | 41 |
| 2026-07 | 34 |
| 2026-08 | 30 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.28624462 | corriereirpinia.it | 2026-04-03 | Il Sud che vuole cambiare – Corriere dell'Irpinia |
| 2 | 0.28407828 | corriereirpinia.it | 2026-04-30 | Primo maggio, spazio alla dignità del lavoro – Corriere dell'Irpinia |
| 3 | 0.28014902 | corriereirpinia.it | 2026-05-17 | I 18 anni di Maia – Corriere dell'Irpinia |
| 4 | 0.27762747 | corriereirpinia.it | 2026-05-20 | Noi di Centro, Negrone: “L’entusiasmo dei giovani, una marcia in più per Nello Pizza” – Corriere dell'Irpinia |
| 5 | 0.27731680 | corriereirpinia.it | 2026-04-12 | Il battesimo di Carlo – Corriere dell'Irpinia |
| 6 | 0.27617897 | corriereirpinia.it | 2026-07-09 | Laurea Preziosi, auguri alla neodottoressa – Corriere dell'Irpinia |
| 7 | 0.27403642 | corriereirpinia.it | 2026-04-24 | Buon compleanno Roberta – Corriere dell'Irpinia |
| 8 | 0.27351769 | corriereirpinia.it | 2026-04-14 | Lutto Vitale, l’abbraccio della redazione ai colleghi Giancarlo e Norberto – Corriere dell'Irpinia |
| 9 | 0.27052767 | corriereirpinia.it | 2026-05-01 | Auguroni di buon compleanno alla splendida Sara Tozza – Corriere dell'Irpinia |
| 10 | 0.26801071 | corriereirpinia.it | 2026-05-27 | Buon compleanno Renato – Corriere dell'Irpinia |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.12684986 | 0.84569692 | corriereirpinia.it | 2026-05-22 | Amministrative Ariano Irpino, Grasso chiude la campagna elettorale: comizio finale alle 23 in piazza Franza – Corriere dell'Irpinia |
| 2 | 0.01519161 | 0.52556111 | corriereirpinia.it | 2026-08-05 | Auguri al piccolo supereroe Francesco Carrino – Corriere dell'Irpinia |
| 3 | 0.09900643 | 0.84498961 | corriereirpinia.it | 2026-08-08 | Grottaminarda, acqua rossastra e sabbia da alcuni rubinetti. Il Comune pronto ad intervenire,  Spera: “Un fatto grave e spiacevole, se dovesse continuare chiamerò Alto Calore” – Co |
| 4 | 0.20988316 | 0.93747719 | corriereirpinia.it | 2026-05-04 | I protagonisti della politica, così i notabili affermarono il loro potere in Campania – Corriere dell'Irpinia |
| 5 | 0.02024447 | 0.45755126 | ilmattino.it | 2026-04-24 | Svolta “Agenda Sud», in Irpinia 2,7 milioni |

### Topic 7

- Articoli: 28247 (26.394%).
- Termini registrati: vita, persone, storia, milano, mondo, famiglia, uomo, piazza, lega, polizia, citta, casa
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | ilgiornale.it | 2259 | 7.997% |
| 2 | ansa.it | 1974 | 6.988% |
| 3 | lanazione.it | 1645 | 5.824% |
| 4 | ilrestodelcarlino.it | 1479 | 5.236% |
| 5 | iltempo.it | 1344 | 4.758% |
| 6 | varesenews.it | 1175 | 4.160% |
| 7 | lastampa.it | 1134 | 4.015% |
| 8 | ilfattoquotidiano.it | 1118 | 3.958% |
| 9 | ilmattino.it | 1027 | 3.636% |
| 10 | ilmessaggero.it | 1015 | 3.593% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 2262 |
| 2026-02 | 3802 |
| 2026-03 | 3300 |
| 2026-04 | 3587 |
| 2026-05 | 3927 |
| 2026-06 | 4187 |
| 2026-07 | 4272 |
| 2026-08 | 2910 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.06293628 | leggo.it | 2026-05-08 | Live la visita del Papa, in 20mila a Pompei. Il Pontefice a Piazza del Plebiscito: «Napoli non perdere la speranza» |
| 2 | 0.05954024 | ilrestodelcarlino.it | 2026-08-06 | È morto Francesco Guccini: aveva 86 anni. Addio a uno dei più grandi cantautori della musica italiana. Il cordoglio: la diretta |
| 3 | 0.05818985 | repubblica.it | 2026-06-13 | Repubblica delle idee 2026, la diretta. Renzi: “Basta litigare”. Saviano e l’inganno di Garlasco. Massini racconta Trump. Conte: “No alla patrimoniale” - la Repubblica |
| 4 | 0.05815257 | ilmessaggero.it | 2026-05-09 | Festa della Mamma, i libri da regalare tra romanzi-coccola e storie di grandi donne |
| 5 | 0.05798018 | repubblica.it | 2026-08-06 | Morto Francesco Guccini, le reazioni da Lepore a Gabbani a Pupi Avati - la Repubblica |
| 6 | 0.05742508 | repubblica.it | 2026-08-08 | Francesco Guccini: qualcosa che non sapete su di lui. L’intervista per ricordarlo oggi - la Repubblica |
| 7 | 0.05422373 | ilmessaggero.it | 2026-08-02 | Dori Ghezzi, la custode dell’eredità di Fabrizio De André. Anteprima a “La Voce delle Emozioni”: il Premio alla carriera 2026 andrà a Renato Zero |
| 8 | 0.05334657 | repubblica.it | 2026-05-08 | Papa Leone oggi a Pompei e a Napoli: "Affido alla Madonna l'intera umanitÃ " - la Repubblica |
| 9 | 0.05294986 | affaritaliani.it | 2026-08-10 | Cinque romanzi da portare in vacanza ad agosto 2026 |
| 10 | 0.05195607 | ilgiorno.it | 2026-02-05 | Olimpiadi, la diretta a Milano: folla per la torcia in piazza Duomo. L’ultima tedofora Nicoletta Manni accende il braciere olimpico |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.01319896 | 0.45881059 | corriereadriatico.it | 2026-08-09 | Olivetti e la risposta ironica all’Anpi. «Sentite la mia mancanza, ma torno» |
| 2 | 0.01455985 | 0.42866646 | ilgiorno.it | 2026-05-01 | “Area storica sottratta alla città per farci un hotel con 199 stanze”: Cinque Vie, “spianata” sequestrata |
| 3 | 0.01964067 | 0.82692471 | lasicilia.it | 2026-05-05 | Il talento di Agrigento alla conquista del Teatro Massimo: Leonardo Scicolone firma l’apertura della stagione sinfonica - La Sicilia |
| 4 | 0.01496826 | 0.32846857 | lasicilia.it | 2026-07-26 | Pirlo ct  e il confine mobile tra calcio, politica e affari.  Vannacci: «Con lui come con Buttafuoco» - La Sicilia |
| 5 | 0.02497568 | 0.78898769 | mediaset.it | 2026-01-24 | Taranto,"cane-eroe Bruno non fu avvelenato":indagato addestratore |

### Topic 8

- Articoli: 172 (0.161%).
- Termini registrati: wimbledon, ciclismo tour, calcio mondiali, de france, tour de, ciclismo, tennis wimbledon, france, km tennis, tennis, mondiali, km
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | repubblica.it | 106 | 61.628% |
| 2 | lagazzettadelmezzogiorno.it | 17 | 9.884% |
| 3 | ilfattoquotidiano.it | 13 | 7.558% |
| 4 | askanews.it | 7 | 4.070% |
| 5 | ansa.it | 5 | 2.907% |
| 6 | iltempo.it | 4 | 2.326% |
| 7 | adnkronos.com | 3 | 1.744% |
| 8 | italpress.com | 3 | 1.744% |
| 9 | leggo.it | 3 | 1.744% |
| 10 | corriereromagna.it | 2 | 1.163% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 2 |
| 2026-02 | 4 |
| 2026-03 | 3 |
| 2026-04 | 70 |
| 2026-05 | 52 |
| 2026-06 | 21 |
| 2026-07 | 11 |
| 2026-08 | 9 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.28874859 | repubblica.it | 2026-04-19 | Pesaro - Forlì (85-73) Serie A2 - la Repubblica |
| 2 | 0.28864987 | repubblica.it | 2026-04-19 | Torino - Baltur Cento (80-69) Serie A2 - la Repubblica |
| 3 | 0.28860535 | repubblica.it | 2026-04-10 | Monaco - Barcelona (93-86) Euroleague - la Repubblica |
| 4 | 0.28852694 | repubblica.it | 2026-04-19 | Pistoia - Brindisi (79-71) Serie A2 - la Repubblica |
| 5 | 0.28851104 | repubblica.it | 2026-04-07 | Valencia - Milano (102-96) Euroleague - la Repubblica |
| 6 | 0.28849949 | repubblica.it | 2026-04-17 | Dubai - Valencia (85-95) Euroleague - la Repubblica |
| 7 | 0.28840495 | repubblica.it | 2026-04-07 | Žalgiris - Dubai (65-77) Euroleague - la Repubblica |
| 8 | 0.28837556 | repubblica.it | 2026-04-16 | Olympiacos - Milano (85-76) Euroleague - la Repubblica |
| 9 | 0.28835634 | repubblica.it | 2026-04-26 | Baltur Cento - Pistoia (99-86) Serie A2 - la Repubblica |
| 10 | 0.28832660 | repubblica.it | 2026-04-12 | Baltur Cento - Scafati (83-88) Serie A2 - la Repubblica |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.00677310 | 0.41615269 | corriereromagna.it | 2026-05-31 | Tennis, Renzi vince a Riccione |
| 2 | 0.01980564 | 0.53571677 | ilfattoquotidiano.it | 2026-05-04 | Internazionali Roma 2026: il tabellone, l'esordio di Sinner |
| 3 | 0.01053801 | 0.27385604 | iltempo.it | 2026-06-11 | Flavio Cobolli il più citato su radio e tv nell'ultima settimana – Il Tempo |
| 4 | 0.28789802 | 1.00000000 | repubblica.it | 2026-04-28 | Fenerbahçe - Žalgiris (89-78) Euroleague - la Repubblica |
| 5 | 0.28789561 | 1.00000000 | repubblica.it | 2026-05-08 | Pistoia - Ruvo di Puglia (79-78) Serie A2 - la Repubblica |

### Topic 9

- Articoli: 12928 (12.080%).
- Termini registrati: referendum, riforma, giustizia, meloni, no, governo, schlein, legge, conte, voto, magistratura, camera
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | iltempo.it | 1255 | 9.708% |
| 2 | ansa.it | 1064 | 8.230% |
| 3 | ilgiornale.it | 1058 | 8.184% |
| 4 | repubblica.it | 944 | 7.302% |
| 5 | askanews.it | 845 | 6.536% |
| 6 | ilfoglio.it | 512 | 3.960% |
| 7 | ilfattoquotidiano.it | 502 | 3.883% |
| 8 | lastampa.it | 500 | 3.868% |
| 9 | ilmessaggero.it | 435 | 3.365% |
| 10 | ilmanifesto.it | 434 | 3.357% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 1033 |
| 2026-02 | 2102 |
| 2026-03 | 3599 |
| 2026-04 | 1490 |
| 2026-05 | 945 |
| 2026-06 | 1190 |
| 2026-07 | 1882 |
| 2026-08 | 687 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.05614350 | tpi.it | 2026-03-06 | Referendum di mid-term: perché il 22-23 marzo la posta in gioco è doppia |
| 2 | 0.05365173 | lastampa.it | 2026-03-24 | Referendum 2026, dopo il voto si dimettono Delmastro e Bartolozzi - La Stampa |
| 3 | 0.05209722 | laverita.info | 2026-03-19 | Referendum sulla giustizia: storia, quesiti e scontro politico — La Verità |
| 4 | 0.05204532 | repubblica.it | 2026-03-24 | Referendum Giustizia 2026, le reazioni dopo i risultati \| Diretta   - la Repubblica |
| 5 | 0.05202200 | unionesarda.it | 2026-03-23 | Referendum giustizia, i risultati in diretta: tutti gli aggiornamenti |
| 6 | 0.05197315 | ansa.it | 2026-03-20 | L'ultima spinta del campo largo, 'un No contro i pieni poteri' - Notizie - Ansa.it |
| 7 | 0.05170458 | lastampa.it | 2026-03-21 | Referendum, scontro finale Meloni-Schlein - La Stampa |
| 8 | 0.05153956 | ilfattoquotidiano.it | 2026-02-22 | Referendum giustizia: al via la campagna elettorale tra Nordio e Conte \| Il Fatto Quotidiano |
| 9 | 0.05132790 | ansa.it | 2026-03-23 | Referendum, netta vittoria del No, bloccata la riforma della giustizia - Notizie - Ansa.it |
| 10 | 0.05097183 | gazzettadelsud.it | 2026-03-24 | Referendum Giustizia, gli italiani bocciano la riforma. I dati definitivi: il SI' al 46,26%, il NO al 53,74%. Meloni: "Occasione persa, ma la sovranità popolare si rispetta" - Gazz |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.01604341 | 0.38583075 | askanews.it | 2026-04-01 | M5S, Covid e inviato di Trump, Conte nel mirino del centrodestra |
| 2 | 0.01396389 | 0.46403433 | ansa.it | 2026-05-23 | Conte, 'torneremo al governo e cancelleremo norme a favore colletti bianchi collusi' - Notizie - Ansa.it |
| 3 | 0.01255273 | 0.53436581 | avvenire.it | 2026-02-11 | Vigilanza, tredicesima fumata nera sul voto del presidente Rai |
| 4 | 0.02051156 | 0.42932081 | ilfoglio.it | 2026-05-19 | Mulè (FI): "La Lega? No a rotture unilaterali sul Patto di stabilità. L’Ue ci ascolti” |
| 5 | 0.02615570 | 0.42006382 | ilgiornale.it | 2026-05-04 | Antonio Padellaro: "La sinistra non è pronta per governare. E sull'immigrazione cosa vogliono fare?" - il Giornale |

### Topic 10

- Articoli: 754 (0.705%).
- Termini registrati: risorse sconto, carburanti finiscono, proroga gasolio, sconto proroga, finiscono risorse, gasolio fino, fino mercoledi, gasolio, sconto, carburanti, proroga, varese
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | varesenews.it | 539 | 71.485% |
| 2 | ansa.it | 20 | 2.653% |
| 3 | askanews.it | 16 | 2.122% |
| 4 | gazzettadiparma.it | 11 | 1.459% |
| 5 | ilsole24ore.com | 11 | 1.459% |
| 6 | lagazzettadelmezzogiorno.it | 11 | 1.459% |
| 7 | repubblica.it | 11 | 1.459% |
| 8 | giornaledibrescia.it | 10 | 1.326% |
| 9 | unionesarda.it | 10 | 1.326% |
| 10 | gazzettadelsud.it | 9 | 1.194% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 2 |
| 2026-03 | 15 |
| 2026-04 | 53 |
| 2026-05 | 39 |
| 2026-06 | 31 |
| 2026-07 | 158 |
| 2026-08 | 456 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.24290645 | varesenews.it | 2026-08-22 | A4 e tangenziale A52, le chiusure dei prossimi giorni |
| 2 | 0.22905058 | varesenews.it | 2026-08-24 | Le carte Pokemon non dichiarate a Malpensa e la nuova ondata di maltempo |
| 3 | 0.21171835 | varesenews.it | 2026-07-24 | Fine vita e diritto alla salute, il M5S raccoglie firme a Varese per due proposte di legge regionali |
| 4 | 0.20274736 | varesenews.it | 2026-08-23 | Pro Patria - Varesina in diretta |
| 5 | 0.20060377 | varesenews.it | 2026-08-20 | La storia d'amore che fa il giro d'Italia e i maxi store cinesi che eludono il fisco |
| 6 | 0.19452118 | varesenews.it | 2026-08-17 | A Velate l'ultimo saluto a Fabio Molinari, il varesino morto a Formentera |
| 7 | 0.18811879 | varesenews.it | 2026-08-23 | Albero crolla su un'auto in Valganna: due feriti lievi |
| 8 | 0.18644491 | varesenews.it | 2026-08-20 | Incidente a Cantello lungo la Provinciale: due i feriti |
| 9 | 0.18488551 | varesenews.it | 2026-08-25 | Grandine e vento su Malpensa: voli cancellati, ritardi e allagamenti nei terminal |
| 10 | 0.18391467 | varesenews.it | 2026-08-19 | Dieci donne in manette a Malpensa e la fine del grande caldo |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.02076562 | 0.40896168 | panorama.it | 2026-07-03 | Benzina e Diesel: finisce lo sconto sulle accise, il pieno costerà fino a 3 euro in più |
| 2 | 0.00945448 | 0.46606753 | varesenews.it | 2026-06-21 | Chiusure serali della diramazione autostradale tra Sesto Calende e Castelletto Ticino per verifiche nelle gallerie |
| 3 | 0.01146795 | 0.56432208 | varesenews.it | 2026-07-06 | D08 Diramazione Gallarate-Gattico: chiuso per una notte il tratto tra Besnate e il ramo di immissione sulla A8 |
| 4 | 0.08008559 | 0.66919642 | varesenews.it | 2026-07-27 | Il centrosinistra di Somma Lombardo preoccupato per l'ospedale: "Si sta sottovalutando il trasferimento del primo intervento" |
| 5 | 0.14115302 | 0.91115320 | varesenews.it | 2026-08-18 | Maltempo alla Festa di Ranco, la Pro Loco: "Rimborsi per chi non ha ricevuto il cibo" |

### Topic 11

- Articoli: 974 (0.910%).
- Termini registrati: ansa, ansa it, it, notizie ansa, cookie, it abbonati, abbonamento, notizie, abbonati, evidenza, leggere, informazione
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | ansa.it | 864 | 88.706% |
| 2 | lagazzettadelmezzogiorno.it | 63 | 6.468% |
| 3 | ladige.it | 13 | 1.335% |
| 4 | gazzettadiparma.it | 10 | 1.027% |
| 5 | ilfattoquotidiano.it | 10 | 1.027% |
| 6 | ilsecoloxix.it | 3 | 0.308% |
| 7 | ilgiorno.it | 2 | 0.205% |
| 8 | lasicilia.it | 2 | 0.205% |
| 9 | repubblica.it | 2 | 0.205% |
| 10 | askanews.it | 1 | 0.103% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 103 |
| 2026-02 | 131 |
| 2026-03 | 124 |
| 2026-04 | 123 |
| 2026-05 | 128 |
| 2026-06 | 144 |
| 2026-07 | 131 |
| 2026-08 | 90 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.27540009 | ansa.it | 2026-03-31 | Futuro Nazionale, Vannacci incontra la stampa - Primopiano - Ansa.it |
| 2 | 0.26718459 | ansa.it | 2026-03-31 | Camera, in aula il decreto bollette, le dichiarazioni di voto - Primopiano - Ansa.it |
| 3 | 0.26707168 | ansa.it | 2026-04-13 | Tajani è atterrato a Beirut - Primopiano - Ansa.it |
| 4 | 0.26549324 | ansa.it | 2026-04-23 | Roma, cerimonia alla Farnesina per le targhe dei Giusti - Primopiano - Ansa.it |
| 5 | 0.26348333 | ansa.it | 2026-02-15 | Ucciso migrante da un agente a Verona, il video-choc sui social di Ilaria Cucchi - Italia - Ansa.it |
| 6 | 0.26236580 | ansa.it | 2026-04-11 | Il vicepremier Matteo Salvini a un gazebo della Lega a Milano - Primopiano - Ansa.it |
| 7 | 0.26131608 | ansa.it | 2026-04-21 | La premier Meloni in visita al Salone del Mobile - People - Ansa.it |
| 8 | 0.25997021 | ansa.it | 2026-02-21 | Tajani a Forlì incontra Roberto Donadoni - Primopiano - Ansa.it |
| 9 | 0.25994071 | ansa.it | 2026-06-04 | Il ministro Matteo Salvini interviene agli Stati generali dell'abitare - People - Ansa.it |
| 10 | 0.25865610 | ansa.it | 2026-03-31 | Ucraina, i ministri degli Esteri Ue commemorano il massacro di Bucha - Primopiano - Ansa.it |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.01085560 | 0.30696659 | ansa.it | 2026-02-09 | Città del vino, un accordo di cooperazione tra Acerenza e società rumene - Notizie - Ansa.it |
| 2 | 0.01237414 | 0.38160015 | ansa.it | 2026-04-02 | Polese (Italia Viva), il Potenza è un sentimento che unisce i padri ai figli - Notizie - Ansa.it |
| 3 | 0.00809086 | 0.31360908 | ansa.it | 2026-01-20 | Mirabella Eclano tra le dieci finaliste per la Capitale italiana della cultura 2028 - Notizie - Ansa.it |
| 4 | 0.01159291 | 0.40798939 | ansa.it | 2026-02-14 | Schlein incontra delegazione lavoratori Trasnova - Notizie - Ansa.it |
| 5 | 0.01560361 | 0.40393183 | ansa.it | 2026-01-22 | Vannacci a Ventimiglia, antifascisti protestano - Notizie - Ansa.it |

## Interpretazioni e limiti

- I conteggi precedenti sono fatti quantitativi riproducibili.
- Il report non assegna nomi definitivi né giudizi semantici ai topic.
- I quasi duplicati sono un proxy basato sul prefisso normalizzato degli estratti, non sul full-text.
- Gli estratti hanno lunghezza massima di 500 caratteri.
- I record ad alto peso possono rappresentare boilerplate molto distintivo.

## Avvisi automatici

- Il metadata sorgente contiene un percorso input assoluto; il percorso è oscurato negli output.
- Topic con dominio dominante >= 50.0%: [1, 2, 6, 8, 10, 11]

## Output

- [`topic_distribution.csv`](topic_distribution.csv)
- [`confidence_summary.csv`](confidence_summary.csv)
- [`domain_summary.csv`](domain_summary.csv)
- [`duplicate_summary.json`](duplicate_summary.json)
- [`run_manifest.json`](run_manifest.json)
