# Audit riproducibile degli output NMF

> Report generato automaticamente da `scripts/run_topic_audit.py`.

## Fatti quantitativi

### Distribuzione dei topic

| Topic | Articoli | Percentuale |
|---|---|---|
| 0 | 17390 | 19.699% |
| 1 | 891 | 1.009% |
| 2 | 289 | 0.327% |
| 3 | 10923 | 12.373% |
| 4 | 14530 | 16.459% |
| 5 | 270 | 0.306% |
| 6 | 2234 | 2.531% |
| 7 | 163 | 0.185% |
| 8 | 9938 | 11.257% |
| 9 | 20904 | 23.679% |
| 10 | 9955 | 11.277% |
| 11 | 792 | 0.897% |

Output tabellare: [`topic_distribution.csv`](topic_distribution.csv).

### Confidenza normalizzata

| Metrica | Valore |
|---|---|
| min | 0.16750271 |
| mean | 0.55973887 |
| median | 0.53483528 |
| p25 | 0.41851569 |
| p75 | 0.68646296 |
| p90 | 0.82197862 |
| p99 | 0.98101213 |
| exactly_1_percentage | 0.32737118 |
| below_0.40_percentage | 20.99026949 |
| below_0.50_percentage | 42.96831636 |
| below_0.60_percentage | 62.04420077 |

La confidenza è `max(pesi NMF) / somma(pesi NMF)`: non è una probabilità calibrata.
Output completo: [`confidence_summary.csv`](confidence_summary.csv).

### Duplicazioni

| Sezione | Metrica | Valore |
|---|---|---|
| exact_excerpt | records_in_duplicate_groups | 3328 |
| exact_excerpt | duplicate_groups | 1372 |
| exact_excerpt | largest_group | 253 |
| exact_title_excerpt | records_in_duplicate_groups | 1300 |
| exact_title_excerpt | duplicate_groups | 620 |
| exact_title_excerpt | largest_group | 4 |
| near_duplicate_proxy | prefix_length | 300 |
| near_duplicate_proxy | records_in_duplicate_groups | 5679 |
| near_duplicate_proxy | duplicate_groups | 2324 |
| near_duplicate_proxy | largest_group | 253 |
| near_duplicate_proxy | definition | same normalized prefix of the review excerpt |

Output strutturato: [`duplicate_summary.json`](duplicate_summary.json).

### Parametri registrati dal classificatore

```json
{
  "created_at_utc": "2026-08-27T08:16:46.737182+00:00",
  "input": "mediacloud_fulltext.jsonl",
  "articles": 88279,
  "tfidf_shape": [
    88279,
    1431448
  ],
  "n_topics": 12,
  "requested_n_topics": 12,
  "min_df": 3,
  "max_df": 0.85,
  "random_state": 42,
  "pulizia": {
    "documenti": 97999,
    "domini": 80,
    "domini_con_template": 31,
    "domini_sotto_soglia": 9,
    "righe_template_globali": 1,
    "righe_template_rimosse": 93329,
    "scartati_senza_testo": 4644,
    "scartati_duplicati": 3555,
    "lingua_corretta": 0,
    "documenti_finali": 89800,
    "lingue_finali": {
      "it": 88280,
      "en": 1119,
      "de": 329,
      "fr": 61,
      "pt": 10,
      "ar": 1
    },
    "template_per_dominio": {
      "varesenews.it": [
        [
          "- felice su da busto arsizio a milano per fare ricerca sul cancro: la storia di francesca peluso",
          0.9790419161676647
        ],
        [
          "loro ne fanno gia parte",
          0.9790419161676647
        ],
        [
          "- bustocco-71 su guasto tra le stazioni di varese e gallarate: ritardi e modifiche al servizio sulle tratte di porto ceresio e mendrisio",
          0.9790419161676647
        ],
        [
          "la community di varesenews",
          0.9790419161676647
        ],
        [
          "l'email e richiesta ma non verra mostrata ai visitatori. il contenuto di questo commento esprime il pensiero dell'autore e non rappresenta la linea editoriale di varesenews.it, che rimane autonoma e indipendente. i messaggi inclusi nei commenti non sono testi giornalistici, ma post inviati dai singoli lettori che possono essere automaticamente pubblicati senza filtro preventivo. i commenti che includano uno o piu link a siti esterni verranno rimossi in automatico dal sistema.",
          0.9790419161676647
        ],
        [
          "ultimi commenti",
          0.9790419161676647
        ],
        [
          "- felice su e pronta la prima scuola realizzata con il pnrr in provincia di varese. e le altre? ecco a che punto siamo",
          0.9790419161676647
        ],
        [
          "- principe.rosso su e pronta la prima scuola realizzata con il pnrr in provincia di varese. e le altre? ecco a che punto siamo",
          0.9790419161676647
        ],
        [
          "- felice su anche a varese la maturita si festeggia a colpi di uova, spumante e farina. e i rifiuti restano li",
          0.9790419161676647
        ],
        [
          "accedi o registrati per commentare questo articolo.",
          0.9781864841745082
        ]
      ],
      "tempi.it": [
        [
          "i commenti sono aperti solo per gli utenti registrati. abbonati subito per commentare!",
          0.5100671140939598
        ],
        [
          "articoli correlati",
          0.5100671140939598
        ],
        [
          "il quotidiano online + il mensile digitale",
          0.47651006711409394
        ],
        [
          "digitale",
          0.47651006711409394
        ],
        [
          "full",
          0.47651006711409394
        ],
        [
          "il quotidiano online + il mensile digitale e cartaceo",
          0.47651006711409394
        ],
        [
          "0 commenti",
          0.4429530201342282
        ],
        [
          "non ci sono ancora commenti.",
          0.4429530201342282
        ],
        [
          "contenuto riservato agli abbonati digitale e full",
          0.3288590604026846
        ]
      ],
      "italiachecambia.org": [
        [
          "segnala una notizia",
          0.625
        ],
        [
          "segnalaci una notizia interessante per io non mi rassegno.",
          0.625
        ],
        [
          "valuteremo il suo inserimento all'interno di un prossimo episodio.",
          0.625
        ],
        [
          "trascrizione episodio",
          0.575
        ],
        [
          "fonti",
          0.55
        ],
        [
          "questo episodio e disponibile anche su youtube",
          0.425
        ]
      ],
      "rai.it": [
        [
          "cultura e spettacolofilm - \"l’hangar rosso\", vai all'articolo, al trailer e alle clip 1 e 2 teatro - \"il barbiere di siviglia - opera buffa in due atti\", vai all'articolo e al video festival - \"60° festival teatrale di borgio verezzi\", vai all'articolo museo - \"museo del disco d’epoca\", vai all'articolo film in sala e quelli in arrivo, guarda i trailer clicca qui la nottola, programmazione roma e lazio clicca qui tutti i concerti di musica leggera",
          0.992548435171386
        ],
        [
          "pagina 690 - lottoestrazioni del lotto",
          0.992548435171386
        ],
        [
          "pagina 546 - magazine tvi mestieri di mirko – speciale alto adige estate, dal 24 luglio su raiplay con un nuovo episodio, vai all'articolo under 25 – giovani talenti, dal 26 maggio su raiplay, vai all'articolo e al video promo il club - canzoni sotto la pelle, dall’ 8 maggio su raiplay, vai all'articolo e al video promo",
          0.992548435171386
        ],
        [
          "pagina 556 - documentariarchivio dei documentari, clicca qui",
          0.992548435171386
        ],
        [
          "pagina 752 - la nuova tv digitale",
          0.992548435171386
        ]
      ],
      "adnkronos.com": [
        [
          "in evidenza presentato lo studio 'sinergie tra agricoltura e trasporto aereo per la produzione di saf'",
          0.5263605442176871
        ],
        [
          "in evidenza presentato a roma il 'forum delle citta della notte', aurigemma: \"il tema della sicurezza non ha colore politico\"",
          0.5263605442176871
        ],
        [
          "scoop su air force one donato dal qatar, nyt nel mirino di trump: mandati di comparizione per i reporter",
          0.5263605442176871
        ],
        [
          "in evidenza 'sindrome di rett: bisogni, prospettive e priorita emergenti dall’europa all’italia', digital talk adnkronos - acadia",
          0.5263605442176871
        ],
        [
          "in evidenza universita, a leonardo maria del vecchio la laurea honoris causa in diritto innovazione tecnologica e sostenibilita",
          0.5263605442176871
        ]
      ],
      "gazzettadiparma.it": [
        [
          "© riproduzione riservata",
          0.9865513928914506
        ],
        [
          "gazzetta di parma srl - p.i. 02361510346 - codice sdi: m5uxcr1",
          0.9865513928914506
        ],
        [
          "© gazzetta di parma - riproduzione riservata",
          0.9865513928914506
        ],
        [
          "roma",
          0.44188280499519694
        ]
      ],
      "laverita.info": [
        [
          "rinnova il tuo abbonamento per proseguire con la lettura >",
          0.8908507223113965
        ],
        [
          "contenuto riservato agli abbonati",
          0.8908507223113965
        ],
        [
          "prosegui con la lettura >",
          0.8908507223113965
        ]
      ],
      "tageszeitung.it": [
        [
          "ahnliche artikel",
          1.0
        ],
        [
          "du musst dich einloggen um die kommentare zu lesen.",
          0.7555555555555555
        ],
        [
          "lesen sie die netiquette und die nutzerbedingungen",
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
          0.6907894736842105
        ]
      ],
      "ilsole24ore.com": [
        [
          "i punti chiave",
          0.42798070296347346
        ],
        [
          "3' di lettura",
          0.3349414197105445
        ]
      ],
      "ilroma.net": [
        [
          "copyright @ - nuovo giornale roma societa cooperativa - corso garibaldi, 32 - napoli - 80142 - partita iva 07406411210 - la societa percepisce i contributi di cui al decreto legislativo 15 maggio 2017, n. 70. indicazione resa ai sensi della lettera f) del comma 2 dell’articolo 5 del medesimo decreto legislativo - il giornale aderisce alla file (federazione italiana liberi editori) e all'iap (istituto di autodisciplina pubblicitaria) tutti i diritti sono riservati. nessuna parte di questo giornale puo essere riprodotta con alcun mezzo e/o diffusa in alcun modo e a qualsiasi titolo",
          0.9942857142857143
        ],
        [
          "tutte le novita",
          0.9857142857142858
        ]
      ],
      "ilmanifesto.it": [
        [
          "genova, 25 anni dopo.",
          1.0
        ],
        [
          "la storia sulle ferite del g8. il 17 luglio in edicola con il manifesto un inserto straordinario su quelle giornate del 2001.",
          1.0
        ]
      ],
      "ilgiornaledivicenza.it": [
        [
          "il giornale di vicenza e su whatsapp. clicca qui per iscriverti al nostro canale e rimanere aggiornato in tempo reale.",
          0.9734848484848485
        ]
      ],
      "ansa.it": [
        [
          "riproduzione riservata © copyright ansa",
          0.9280182232346241
        ]
      ],
      "larena.it": [
        [
          "l’arena e su whatsapp. clicca qui per iscriverti al nostro canale e rimanere aggiornato in tempo reale.",
          0.9773584905660377
        ]
      ],
      "ligurianotizie.it": [
        [
          "non perdere gli ultimi aggiornamenti su cronaca, eventi e politica in liguria! iscriviti sui canali di liguria notizie di telegram, facebook, twitter e youtube",
          0.32038834951456313
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
          0.9170896785109983
        ]
      ],
      "italpress.com": [
        [
          "(italpress).",
          0.671000565291125
        ]
      ],
      "nove.firenze.it": [
        [
          "approfondimenti",
          0.4094292803970223
        ]
      ]
    },
    "template_globali": [
      [
        "© riproduzione riservata",
        0.04563311870529291
      ]
    ]
  },
  "stopwords": 348
}
```

## Evidenze per topic

### Topic 0

- Articoli: 17390 (19.699%).
- Termini registrati: vita, storia, milano, persone, mondo, lega, famiglia, piazza, uomo, citta, casa, quel
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | ilgiornale.it | 1474 | 8.476% |
| 2 | ansa.it | 1131 | 6.504% |
| 3 | lanazione.it | 1101 | 6.331% |
| 4 | varesenews.it | 1090 | 6.268% |
| 5 | ilrestodelcarlino.it | 910 | 5.233% |
| 6 | iltempo.it | 742 | 4.267% |
| 7 | lastampa.it | 711 | 4.089% |
| 8 | ilmattino.it | 665 | 3.824% |
| 9 | ilmessaggero.it | 629 | 3.617% |
| 10 | ilfattoquotidiano.it | 616 | 3.542% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 1703 |
| 2026-02 | 2895 |
| 2026-03 | 2584 |
| 2026-04 | 2740 |
| 2026-05 | 3040 |
| 2026-06 | 3262 |
| 2026-07 | 1166 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.05666593 | leggo.it | 2026-05-08 | Live la visita del Papa, in 20mila a Pompei. Il Pontefice a Piazza del Plebiscito: «Napoli non perdere la speranza» |
| 2 | 0.05175062 | repubblica.it | 2026-06-13 | Repubblica delle idee 2026, la diretta. Renzi: “Basta litigare”. Saviano e l’inganno di Garlasco. Massini racconta Trump. Conte: “No alla patrimoniale” - la Repubblica |
| 3 | 0.05159111 | ilmessaggero.it | 2026-05-09 | Festa della Mamma, i libri da regalare tra romanzi-coccola e storie di grandi donne |
| 4 | 0.04811087 | ilgiorno.it | 2026-02-05 | Olimpiadi, la diretta a Milano: folla per la torcia in piazza Duomo. L’ultima tedofora Nicoletta Manni accende il braciere olimpico |
| 5 | 0.04774722 | repubblica.it | 2026-05-08 | Papa Leone oggi a Pompei e a Napoli: "Affido alla Madonna l'intera umanitÃ " - la Repubblica |
| 6 | 0.04670023 | ilgiorno.it | 2026-02-06 | Milano-Cortina 2026 la diretta, oggi l’inaugurazione a San Siro. La sorpresa di Mattarella: arriva in tram con Valentino Rossi. L’accensione del braciere all’Arco della Pace |
| 7 | 0.04665976 | nove.firenze.it | 2026-06-23 | Lucca Comics and Games: presentata l'edizione dei 60 anni del festival • Nove da Firenze |
| 8 | 0.04655311 | lastampa.it | 2026-02-06 | Cerimonia di apertura Olimpiadi Miano-Cortina 2026: segui la diretta  - La Stampa |
| 9 | 0.04516180 | lastampa.it | 2026-05-16 | Salone del Libro, eventi ed ospiti di oggi 16 maggio. La diretta - La Stampa |
| 10 | 0.04513700 | repubblica.it | 2026-01-24 | C.S.I., il ritorno. Giovanni Lindo Ferretti: “Non contano i pensieri ma le cose che accadono” - la Repubblica |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.00931534 | 0.39808425 | gazzettadiparma.it | 2026-07-10 | Tempo di meloni: dissetanti, dolci, ma con pochi zuccheri Ricchi di potassio, vitamina C, beta-carotene e  acidi - Gazzetta di Parma |
| 2 | 0.01798310 | 0.56306770 | ilmattino.it | 2026-06-14 | Vannacci e il femminicidio, il papà di Ilaria Sula: «Rispetto per mia figlia e tutte le donne uccise» |
| 3 | 0.02029789 | 0.56059771 | ilrestodelcarlino.it | 2026-05-25 | Stava preparando un attentato in centro a Reggio Emilia, arrestato un terrorista |
| 4 | 0.01471520 | 0.39824288 | ilsole24ore.com | 2026-05-08 | Mamma di una bambina malata grave scrive a Meloni: “Non siamo invisibili” - Il Sole 24 ORE |
| 5 | 0.01442932 | 0.62031064 | larena.it | 2026-02-09 | Giorgia torna live a Verona, gran finale del tour estivo in Arena: la data \| L'Arena |

### Topic 1

- Articoli: 891 (1.009%).
- Termini registrati: agenzia vista, agenzia, nato milei, milei futuro, bertoldi states, states trump, livello valditara, avesse centrodestra, mascherine pasticcio, studentesca processi, studentesche lavori, partecipazione studentesca
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | iltempo.it | 889 | 99.776% |
| 2 | ansa.it | 1 | 0.112% |
| 3 | lagazzettadelmezzogiorno.it | 1 | 0.112% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 127 |
| 2026-02 | 96 |
| 2026-03 | 166 |
| 2026-04 | 165 |
| 2026-05 | 129 |
| 2026-06 | 170 |
| 2026-07 | 38 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.18448465 | iltempo.it | 2026-03-23 | Il Ministro Tajani vota per il referendum sulla giustizia a Fiuggi – Il Tempo |
| 2 | 0.18177773 | iltempo.it | 2026-01-16 | Takaichi fa gli auguri di compleanno a Meloni, l'applauso della delegazione giapponese – Il Tempo |
| 3 | 0.18072616 | iltempo.it | 2026-04-10 | Meloni in Senato: Non faremo misure demagogiche che devastano conti Stato come hanno fatto altri – Il Tempo |
| 4 | 0.18016550 | iltempo.it | 2026-02-10 | Calenda: Vannacci da sempre sostiene le ragioni di Putin – Il Tempo |
| 5 | 0.17799428 | iltempo.it | 2026-07-10 | Rampelli: Non si possono fare banchetti sull'Altare della Patria – Il Tempo |
| 6 | 0.17522606 | iltempo.it | 2026-06-18 | Meloni arriva al Consiglio Ue di Bruxelles – Il Tempo |
| 7 | 0.17431731 | iltempo.it | 2026-02-10 | Giorno del Ricordo, l'applauso dell'Aula di Montecitorio – Il Tempo |
| 8 | 0.17338685 | iltempo.it | 2026-03-11 | Bonelli contro Tajani: Fatto appelli imbarazzanti su droni e “oggi come sono stati i bombardamenti” – Il Tempo |
| 9 | 0.17304424 | iltempo.it | 2026-03-22 | Elly Schlein vota per il Referendum sulla giustizia – Il Tempo |
| 10 | 0.17223401 | iltempo.it | 2026-04-30 | Salvini: Sono sempre d'accordo con la Presidente del Consiglio – Il Tempo |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.14984109 | 0.90088289 | iltempo.it | 2026-01-16 | Selfie per Meloni e Sanae Takaichi di fronte al grande vaso di fiori nel Palazzo del Governo a Tokyo – Il Tempo |
| 2 | 0.12898490 | 0.89959520 | iltempo.it | 2026-02-12 | Meloni: Costi energia? "Occorre partire da una revisione degli Ets e contrastare la speculazione" – Il Tempo |
| 3 | 0.11465504 | 0.73124382 | iltempo.it | 2026-04-09 | Tregua Iran, Meloni: Condanniamo qualsiasi forma di violazione del cessate il fuoco – Il Tempo |
| 4 | 0.15495276 | 0.75787361 | iltempo.it | 2026-04-28 | Caso Minetti, Meloni: Escludo le dimissioni di Nordio – Il Tempo |
| 5 | 0.13153721 | 0.86978366 | iltempo.it | 2026-05-11 | Tajani su Hantavirus: Non sono per l'uscita dall'Oms – Il Tempo |

### Topic 2

- Articoli: 289 (0.327%).
- Termini registrati: corriere viterbo, corriere rieti, tempo tv, carlo antini, attualita esteri, rieti corriere, personaggi opinioni, antini, edicola digitale, controtempo, rieti, viterbo
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | iltempo.it | 253 | 87.543% |
| 2 | laverita.info | 27 | 9.343% |
| 3 | askanews.it | 2 | 0.692% |
| 4 | lagazzettadelmezzogiorno.it | 2 | 0.692% |
| 5 | adnkronos.com | 1 | 0.346% |
| 6 | ilnuovolevante.it | 1 | 0.346% |
| 7 | italpress.com | 1 | 0.346% |
| 8 | repubblica.it | 1 | 0.346% |
| 9 | unionesarda.it | 1 | 0.346% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 42 |
| 2026-02 | 56 |
| 2026-03 | 43 |
| 2026-04 | 51 |
| 2026-05 | 40 |
| 2026-06 | 44 |
| 2026-07 | 13 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.25743253 | iltempo.it | 2026-03-07 | Iran, Lupi "Le iniziative della Meloni vanno verso la via diplomatica" – Il Tempo |
| 2 | 0.25511847 | iltempo.it | 2026-06-24 | Meloni "Nel 2025 dal Governo 160 milioni di euro contro le dipendenze" – Il Tempo |
| 3 | 0.25318374 | iltempo.it | 2026-06-15 | Lega, Guidesi "Discussione sia strutturale, non contingente o elettorale" – Il Tempo |
| 4 | 0.25260099 | iltempo.it | 2026-06-10 | Meloni "L'Italia non è la repubblica delle banane" – Il Tempo |
| 5 | 0.25170500 | iltempo.it | 2026-02-27 | Salvini "Lavorerò per le Olimpiadi di Roma 2040" – Il Tempo |
| 6 | 0.25130414 | iltempo.it | 2026-04-23 | Energia, Meloni "L'Europa sia più coraggiosa" – Il Tempo |
| 7 | 0.25011982 | iltempo.it | 2026-04-29 | Tajani "Sull'energia l'Unione Europea deve essere più elastica" – Il Tempo |
| 8 | 0.24976886 | iltempo.it | 2026-02-27 | Legge elettorale Salvini "Se garantisce la stabilità va benissimo" – Il Tempo |
| 9 | 0.24932795 | iltempo.it | 2026-05-11 | Tajani "L'Iran non può avere l'arma nucleare" – Il Tempo |
| 10 | 0.24836283 | iltempo.it | 2026-05-04 | Nato, Meloni "L'Italia ha sempre mantenuto gli impegni" – Il Tempo |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.23789313 | 0.98713295 | iltempo.it | 2026-02-24 | Tajani "Vogliamo far sì che Matera sia un ponte verso tutta l'area mediterranea" – Il Tempo |
| 2 | 0.22737320 | 0.96813887 | iltempo.it | 2026-03-16 | Tajani "Rafforzare la missione Aspides ma no all'allargamento a Hormuz" – Il Tempo |
| 3 | 0.22313055 | 0.96411506 | iltempo.it | 2026-04-09 | Meloni "In Iran flebile prospettiva di pace, Israele fermi escalation in Libano" – Il Tempo |
| 4 | 0.23597023 | 0.97124209 | iltempo.it | 2026-05-07 | Ue, Meloni "Da Italia e Polonia stessa linea sul nuovo quadro finanziario" – Il Tempo |
| 5 | 0.24932795 | 0.97408873 | iltempo.it | 2026-05-11 | Tajani "L'Iran non può avere l'arma nucleare" – Il Tempo |

### Topic 3

- Articoli: 10923 (12.373%).
- Termini registrati: meloni, giorgia, giorgia meloni, premier, presidente consiglio, presidente, consiglio, consiglio giorgia, chigi, palazzo chigi, palazzo, roma
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | askanews.it | 1144 | 10.473% |
| 2 | ansa.it | 1069 | 9.787% |
| 3 | iltempo.it | 931 | 8.523% |
| 4 | repubblica.it | 863 | 7.901% |
| 5 | ilgiornale.it | 576 | 5.273% |
| 6 | italpress.com | 540 | 4.944% |
| 7 | adnkronos.com | 411 | 3.763% |
| 8 | gazzettadiparma.it | 397 | 3.635% |
| 9 | giornaledibrescia.it | 371 | 3.397% |
| 10 | lastampa.it | 356 | 3.259% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 951 |
| 2026-02 | 1224 |
| 2026-03 | 1393 |
| 2026-04 | 2661 |
| 2026-05 | 1730 |
| 2026-06 | 2276 |
| 2026-07 | 688 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.08617188 | askanews.it | 2026-03-18 | Governo, Meloni incontra Giorgetti a Palazzo Chigi |
| 2 | 0.08154691 | adnkronos.com | 2026-03-16 | L’agenda del Premier |
| 3 | 0.07932773 | askanews.it | 2026-04-28 | Meloni: entro la fine della settimana Piano casa |
| 4 | 0.07869262 | adnkronos.com | 2026-04-13 | L’agenda del Premier |
| 5 | 0.07800963 | adnkronos.com | 2026-06-22 | L’agenda del premier Giorgia Meloni |
| 6 | 0.07717425 | askanews.it | 2026-04-11 | Ucraina, Zelensky mercoledì a Roma incontra Meloni |
| 7 | 0.07565925 | gazzettadiparma.it | 2026-05-16 | Fonti Chigi, Meloni segue con massima attenzione quanto accaduto a Modena - Gazzetta di Parma |
| 8 | 0.07411972 | askanews.it | 2026-04-02 | Governo, vertice maggioranza con Meloni a palazzo Chigi su Dfp |
| 9 | 0.07391666 | adnkronos.com | 2026-06-08 | L’agenda del Premier Meloni |
| 10 | 0.07371504 | adnkronos.com | 2026-04-20 | L’agenda del premier Giorgia Meloni |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.01417993 | 0.69612631 | askanews.it | 2026-04-21 | Terna, Giuseppina Di Foggia rinuncia all’indennità di fine rapporto |
| 2 | 0.03178265 | 0.46220744 | adnkronos.com | 2026-06-25 | Meloni e il summit con Macron, oggi il vertice bilaterale ad Antibes: i temi |
| 3 | 0.02899148 | 0.59848212 | ansa.it | 2026-04-14 | Meloni, l'economia preoccupa molto se non riapre Hormuz - Ultima ora - Ansa.it |
| 4 | 0.02948189 | 0.39449113 | ilgiornaledivicenza.it | 2026-03-31 | Roma chiama Luca Zaia. E il Veneto si prepara al dopo \| G. di Vicenza |
| 5 | 0.00850500 | 0.41212501 | repubblica.it | 2026-06-05 | Salvini batte cassa alle banche: “Unicredit e Intesa diano un contributo”. E i titoli vanno giù - la Repubblica |

### Topic 4

- Articoli: 14530 (16.459%).
- Termini registrati: sindaco, centrodestra, partito, candidato, centrosinistra, coalizione, pd, forza italia, elezioni, forza, elettorale, lista
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | lanazione.it | 1605 | 11.046% |
| 2 | ansa.it | 1370 | 9.429% |
| 3 | ilrestodelcarlino.it | 952 | 6.552% |
| 4 | gazzettadelsud.it | 809 | 5.568% |
| 5 | ilgiornale.it | 651 | 4.480% |
| 6 | ilmattino.it | 570 | 3.923% |
| 7 | lastampa.it | 567 | 3.902% |
| 8 | repubblica.it | 508 | 3.496% |
| 9 | ilgiorno.it | 499 | 3.434% |
| 10 | ilgazzettino.it | 460 | 3.166% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 1162 |
| 2026-02 | 1946 |
| 2026-03 | 1746 |
| 2026-04 | 2371 |
| 2026-05 | 3300 |
| 2026-06 | 3153 |
| 2026-07 | 852 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.08735698 | ilfoglio.it | 2026-05-25 | De Luca a valanga a Salerno. A Venezia il centrodestra verso la vittoria al primo turno. I risultati delle comunali |
| 2 | 0.08375187 | ilgiornale.it | 2026-05-25 | Amministrative, da Arezzo a Reggio Calabria: tutte le sfide-chiave nelle città  - il Giornale |
| 3 | 0.08297321 | ilfattoquotidiano.it | 2026-05-23 | Elezioni amministrative 2026: Venezia, Salerno, Messina e Reggio Calabria le sfide chiave \| Il Fatto Quotidiano.it |
| 4 | 0.07981509 | adnkronos.com | 2026-05-06 | Elezioni amministrative 2026, dove si vota il 24 e 25 maggio: comuni, schieramenti e candidati |
| 5 | 0.07839232 | ilmattino.it | 2026-05-25 | Elezioni Comunali 24 e 25 maggio 2026, i risultati in diretta, le preferenze e gli exit poll in provincia di Avellino, Benevento, Caserta Napoli e Salerno |
| 6 | 0.07818664 | agi.it | 2026-05-24 | Da Venezia a Reggio Calabria, oggi 6 milioni e mezzo di italiani |
| 7 | 0.07750925 | repubblica.it | 2026-05-22 | Elezioni comunali 2026: dove e come si vota il 24 e 25 maggio - la Repubblica |
| 8 | 0.07710441 | repubblica.it | 2026-05-24 | Comunali 2026, dove e come si vota - la Repubblica |
| 9 | 0.07641016 | avvenire.it | 2026-05-22 | Le “bizze” della Lega, la sfida per Venezia, il caso De Luca: tutto quello che c'è da sapere sulle Comunali |
| 10 | 0.07636253 | lastampa.it | 2026-06-08 | Elezioni comunali 2026, i risultati dei ballottaggi in diretta - La Stampa |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.02871268 | 0.70515478 | gazzettadelsud.it | 2026-01-15 | Amministrazione al giro di boa a Vibo: Romeo sussurra, il Pd borbotta - Gazzetta del Sud |
| 2 | 0.01892174 | 0.38515922 | adnkronos.com | 2026-05-04 | Forza Italia, Marina Berlusconi resta fuori: tensioni in Campania e appello all’unità |
| 3 | 0.00849717 | 0.33341162 | iltempo.it | 2026-04-01 | Il Tempo di Osho, la vignetta di oggi: Grillo-Conte, altro round in tribunale (mercoledì 1 aprile) – Il Tempo |
| 4 | 0.02610932 | 0.59674156 | iltempo.it | 2026-02-12 | Vannacci: "Sostengo il Governo ma resto critico su invio armi a Kiev" – Il Tempo |
| 5 | 0.04094596 | 0.78635404 | lanazione.it | 2026-01-17 | Graverini mantiene il pallino. Prende tempo sulla risposta e mette a fuoco la squadra. Tanti e Comanducci in pista |

### Topic 5

- Articoli: 270 (0.306%).
- Termini registrati: avellino, irpinia, pratola, reg, ariano, serra, grottaminarda, magia, corriere, momenti, gianni festa, irpini
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | corriereirpinia.it | 263 | 97.407% |
| 2 | lagazzettadelmezzogiorno.it | 2 | 0.741% |
| 3 | ansa.it | 1 | 0.370% |
| 4 | askanews.it | 1 | 0.370% |
| 5 | giornaledibrescia.it | 1 | 0.370% |
| 6 | lanazione.it | 1 | 0.370% |
| 7 | ligurianotizie.it | 1 | 0.370% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 19 |
| 2026-02 | 27 |
| 2026-03 | 42 |
| 2026-04 | 59 |
| 2026-05 | 73 |
| 2026-06 | 40 |
| 2026-07 | 10 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.29007320 | corriereirpinia.it | 2026-04-03 | Il Sud che vuole cambiare – Corriere dell'Irpinia |
| 2 | 0.28789114 | corriereirpinia.it | 2026-04-30 | Primo maggio, spazio alla dignità del lavoro – Corriere dell'Irpinia |
| 3 | 0.28370598 | corriereirpinia.it | 2026-05-17 | I 18 anni di Maia – Corriere dell'Irpinia |
| 4 | 0.28217344 | corriereirpinia.it | 2026-05-20 | Noi di Centro, Negrone: “L’entusiasmo dei giovani, una marcia in più per Nello Pizza” – Corriere dell'Irpinia |
| 5 | 0.28170606 | corriereirpinia.it | 2026-04-12 | Il battesimo di Carlo – Corriere dell'Irpinia |
| 6 | 0.27966108 | corriereirpinia.it | 2026-07-09 | Laurea Preziosi, auguri alla neodottoressa – Corriere dell'Irpinia |
| 7 | 0.27911855 | corriereirpinia.it | 2026-04-24 | Buon compleanno Roberta – Corriere dell'Irpinia |
| 8 | 0.27662143 | corriereirpinia.it | 2026-04-14 | Lutto Vitale, l’abbraccio della redazione ai colleghi Giancarlo e Norberto – Corriere dell'Irpinia |
| 9 | 0.27475991 | corriereirpinia.it | 2026-05-01 | Auguroni di buon compleanno alla splendida Sara Tozza – Corriere dell'Irpinia |
| 10 | 0.27191569 | corriereirpinia.it | 2026-05-27 | Buon compleanno Renato – Corriere dell'Irpinia |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.21905458 | 0.91032602 | corriereirpinia.it | 2026-05-21 | Amministrative Ariano, domani gli appelli finali. Tre candidati sindaci,12 liste,187 aspiranti consiglieri comunali – Corriere dell'Irpinia |
| 2 | 0.01477084 | 0.42902382 | corriereirpinia.it | 2026-05-27 | Gargani, Sena: “Ha valorizzato la presenza dell’Irpinia nelle istituzioni” – Corriere dell'Irpinia |
| 3 | 0.22450788 | 0.92740600 | corriereirpinia.it | 2026-03-23 | Micillo (M5s): i cittadini hanno difeso con il No la garanzia di diritti e libertà – Corriere dell'Irpinia |
| 4 | 0.24021768 | 0.98629186 | corriereirpinia.it | 2026-05-17 | Montoro, è realtà il sogno Promozione – Corriere dell'Irpinia |
| 5 | 0.12556979 | 0.81836074 | corriereirpinia.it | 2026-03-28 | Piano di rientro, Sarracino: “Si apre una stagione nuova” – Corriere dell'Irpinia |

### Topic 6

- Articoli: 2234 (2.531%).
- Termini registrati: agenzia vista, agenzia, vista, jakhnagiev, alexander jakhnagiev, vista alexander, alexander, fonte agenzia, fonte, vista roma, immobile asta, tuo immobile
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | agi.it | 783 | 35.049% |
| 2 | ilmessaggero.it | 675 | 30.215% |
| 3 | affaritaliani.it | 380 | 17.010% |
| 4 | ilmattino.it | 318 | 14.235% |
| 5 | ilgazzettino.it | 65 | 2.910% |
| 6 | corriereadriatico.it | 3 | 0.134% |
| 7 | italpress.com | 3 | 0.134% |
| 8 | laverita.info | 2 | 0.090% |
| 9 | leggo.it | 2 | 0.090% |
| 10 | ilmanifesto.it | 1 | 0.045% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 115 |
| 2026-02 | 189 |
| 2026-03 | 388 |
| 2026-04 | 524 |
| 2026-05 | 417 |
| 2026-06 | 487 |
| 2026-07 | 114 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.19415288 | ilmessaggero.it | 2026-03-14 | Il dietro la tenda dell'intervista con Conte del direttore di Agenzia Vista Alexander Jakhnagiev |
| 2 | 0.18337201 | ilmessaggero.it | 2026-06-11 | Meloni esce dal Senato e saluta il direttore di Agenzia Vista Alexander Jakhnagiev a fine seduta |
| 3 | 0.16743704 | ilmessaggero.it | 2026-06-13 | Vannacci: La Costituzione è antifascista? Non mi risulta |
| 4 | 0.16387794 | ilmessaggero.it | 2026-04-30 | Salvini: Sono sempre d’accordo con la Presidente del Consiglio |
| 5 | 0.16200175 | ilmessaggero.it | 2026-04-15 | L'abbraccio tra Meloni e Zelensky all'arrivo del Presidente ucraino a Palazzo Chigi |
| 6 | 0.15900859 | ilmessaggero.it | 2026-05-25 | Dalla biennale a Gaza, dalla benzina a Taiwan, ecco gli ultimi elenchi di Salvini |
| 7 | 0.15820310 | ilmessaggero.it | 2026-04-28 | Meloni: Su Patto di Stabilità non va esclusa deroga generale |
| 8 | 0.15750568 | ilmessaggero.it | 2026-03-23 | Meloni, il selfie con le sostenitrici dopo aver votato |
| 9 | 0.15722288 | ilmessaggero.it | 2026-02-17 | Il Presidente Mattarella allAmbasciata della Santa Sede a Roma per i 97 anni dei Patti Lateranensi |
| 10 | 0.15667869 | ilmessaggero.it | 2026-05-30 | 'Siate coraggiosi e io farò lo stesso' su Camera con VIsta su La7 di Alexander Jakhnagiev |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.08675679 | 0.65948384 | affaritaliani.it | 2026-06-11 | Meloni risponde a Silvestri sulle 'ginocchiere', ovazione dal centrodestra alla Camera |
| 2 | 0.08467565 | 0.68520128 | affaritaliani.it | 2026-05-01 | Primo Maggio, Meloni visita PizzAut a Monza |
| 3 | 0.04597686 | 0.57480244 | agi.it | 2026-02-14 | Guerra Ucraina, Tajani: 'Per garantire sicurezza serve impegno Usa soprattutto su difesa aerea' |
| 4 | 0.05761460 | 0.57584447 | agi.it | 2026-05-07 | Meloni: Italia e Polonia condividono radici culturali profonde |
| 5 | 0.10191886 | 0.76646367 | ilmessaggero.it | 2026-05-14 | Meloni al Comint: Ok a documento strategico di politica spaziale nazionale |

### Topic 7

- Articoli: 163 (0.185%).
- Termini registrati: wimbledon, ciclismo tour, de france, calcio mondiali, tour de, ciclismo, tennis wimbledon, france, km tennis, tennis, mondiali, km
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | repubblica.it | 106 | 65.031% |
| 2 | lagazzettadelmezzogiorno.it | 11 | 6.748% |
| 3 | ilfattoquotidiano.it | 8 | 4.908% |
| 4 | askanews.it | 6 | 3.681% |
| 5 | ansa.it | 5 | 3.067% |
| 6 | italpress.com | 4 | 2.454% |
| 7 | adnkronos.com | 3 | 1.840% |
| 8 | iltempo.it | 3 | 1.840% |
| 9 | leggo.it | 3 | 1.840% |
| 10 | varesenews.it | 3 | 1.840% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 2 |
| 2026-02 | 7 |
| 2026-03 | 2 |
| 2026-04 | 70 |
| 2026-05 | 54 |
| 2026-06 | 20 |
| 2026-07 | 8 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.30831567 | repubblica.it | 2026-04-19 | Pesaro - Forlì (85-73) Serie A2 - la Repubblica |
| 2 | 0.30821779 | repubblica.it | 2026-04-19 | Torino - Baltur Cento (80-69) Serie A2 - la Repubblica |
| 3 | 0.30817045 | repubblica.it | 2026-04-10 | Monaco - Barcelona (93-86) Euroleague - la Repubblica |
| 4 | 0.30807913 | repubblica.it | 2026-04-19 | Pistoia - Brindisi (79-71) Serie A2 - la Repubblica |
| 5 | 0.30804706 | repubblica.it | 2026-04-07 | Valencia - Milano (102-96) Euroleague - la Repubblica |
| 6 | 0.30803751 | repubblica.it | 2026-04-17 | Dubai - Valencia (85-95) Euroleague - la Repubblica |
| 7 | 0.30799351 | repubblica.it | 2026-04-12 | Baltur Cento - Scafati (83-88) Serie A2 - la Repubblica |
| 8 | 0.30796419 | repubblica.it | 2026-04-16 | Partizan - Baskonia (91-79) Euroleague - la Repubblica |
| 9 | 0.30795907 | repubblica.it | 2026-04-07 | Žalgiris - Dubai (65-77) Euroleague - la Repubblica |
| 10 | 0.30792452 | repubblica.it | 2026-04-16 | Olympiacos - Milano (85-76) Euroleague - la Repubblica |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.30741370 | 1.00000000 | repubblica.it | 2026-04-09 | Fenerbahçe - Real Madrid (69-74) Euroleague - la Repubblica |
| 2 | 0.30678959 | 1.00000000 | repubblica.it | 2026-05-05 | Hapoel Tel Aviv - Real Madrid (76-69) Euroleague - la Repubblica |
| 3 | 0.30722945 | 1.00000000 | repubblica.it | 2026-04-09 | Valencia - Panathinaikos (102-84) Euroleague - la Repubblica |
| 4 | 0.30732362 | 1.00000000 | repubblica.it | 2026-04-10 | Virtus Bologna - Baskonia (72-82) Euroleague - la Repubblica |
| 5 | 0.30708042 | 0.99786140 | repubblica.it | 2026-04-26 | Real Sebastiani Rieti - Torino (80-66) Serie A2 - la Repubblica |

### Topic 8

- Articoli: 9938 (11.257%).
- Termini registrati: referendum, riforma, giustizia, no, magistratura, magistrati, governo, nordio, schlein, voto, costituzione, legge
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | ilgiornale.it | 1116 | 11.230% |
| 2 | iltempo.it | 1056 | 10.626% |
| 3 | ansa.it | 845 | 8.503% |
| 4 | ilfattoquotidiano.it | 503 | 5.061% |
| 5 | repubblica.it | 488 | 4.910% |
| 6 | ilfoglio.it | 465 | 4.679% |
| 7 | lastampa.it | 417 | 4.196% |
| 8 | ilmanifesto.it | 399 | 4.015% |
| 9 | ilriformista.it | 331 | 3.331% |
| 10 | laverita.info | 317 | 3.190% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 1100 |
| 2026-02 | 2093 |
| 2026-03 | 3487 |
| 2026-04 | 1138 |
| 2026-05 | 786 |
| 2026-06 | 956 |
| 2026-07 | 378 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.08938695 | tpi.it | 2026-03-06 | Referendum di mid-term: perché il 22-23 marzo la posta in gioco è doppia |
| 2 | 0.08645943 | laverita.info | 2026-03-19 | Referendum sulla giustizia: storia, quesiti e scontro politico — La Verità |
| 3 | 0.08300977 | internazionale.it | 2026-03-10 | I rischi della riforma della magistratura - Alessandro Calvi - Internazionale |
| 4 | 0.08254085 | panorama.it | 2026-01-12 | Giustizia, fissata la data del referendum il 22 e 23 marzo 2026: le novità punto per punto |
| 5 | 0.08231324 | ilfattoquotidiano.it | 2026-03-20 | Referendum giustizia 2026: le ragioni per votare "No" |
| 6 | 0.08230845 | tempi.it | 2026-02-15 | Battista: «Il mio sì al referendum sulla giustizia» - Tempi |
| 7 | 0.08224274 | italpress.com | 2026-03-22 | Seggi aperti per il referendum sulla riforma della giustizia: i dati dell'affluenza |
| 8 | 0.08152987 | ilfattoquotidiano.it | 2026-03-20 | Referendum 2026 sulla Giustizia: quando e per cosa si vota |
| 9 | 0.08099440 | ildispariquotidiano.it | 2026-03-07 | Cristiano Rossetti: “Il referendum sulla magistratura? Guardate i contenuti, non le bandiere” – Il Dispari Quotidiano |
| 10 | 0.08093508 | tpi.it | 2026-03-06 | Luciano Violante a TPI: "La riforma Nordio rafforza i pm" |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.02557909 | 0.54143730 | ilmanifesto.it | 2026-03-13 | il manifesto |
| 2 | 0.02356889 | 0.81428254 | repubblica.it | 2026-03-09 | Matone (Lega): âLa canzone di Da Vinci Ã¨ da matrimoni pacchiani ma aiuta il SÃ¬ al referendumâ - la Repubblica |
| 3 | 0.01162852 | 0.24976980 | adnkronos.com | 2026-06-09 | Senato, Silvestro e l'accusa di violenza sessuale: come procede l'inchiesta oggi |
| 4 | 0.03232828 | 0.62130098 | ansa.it | 2026-03-24 | Pedullà (M5s): "Le dimissioni di Dalmastro e Bartolozzi dovute, ora Santanché" - Video - Ansa.it |
| 5 | 0.03772632 | 0.46032571 | ilmessaggero.it | 2026-07-01 | Conte-Schlein: «Destra al Colle? La premier vuole solo il potere» |

### Topic 9

- Articoli: 20904 (23.679%).
- Termini registrati: euro, regionale, regione, risorse, territorio, imprese, lavoro, piano, commissione, sistema, interventi, cittadini
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | ansa.it | 3339 | 15.973% |
| 2 | lanazione.it | 2111 | 10.099% |
| 3 | ilrestodelcarlino.it | 1299 | 6.214% |
| 4 | varesenews.it | 902 | 4.315% |
| 5 | iltempo.it | 805 | 3.851% |
| 6 | ilgiornale.it | 725 | 3.468% |
| 7 | lastampa.it | 699 | 3.344% |
| 8 | ilgiorno.it | 656 | 3.138% |
| 9 | adnkronos.com | 577 | 2.760% |
| 10 | ilsole24ore.com | 548 | 2.622% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 2209 |
| 2026-02 | 2806 |
| 2026-03 | 2872 |
| 2026-04 | 3480 |
| 2026-05 | 3872 |
| 2026-06 | 3986 |
| 2026-07 | 1679 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.05776406 | adnkronos.com | 2026-05-12 | Cni: "Rischio idrogeologico? Non solo fondi, da liberi professionisti 'serbatoio competenze' a cui gli enti locali dovrebbero maggiormente attingere" |
| 2 | 0.05738551 | ilfattoquotidiano.it | 2026-06-16 | PNRR: asili, studentati e Case della comunità, le grandi incompiute a 15 giorni dalla scadenza \| Il Fatto Quotidiano.it |
| 3 | 0.05693535 | nove.firenze.it | 2026-03-16 | Europa: in Regione il punto sulla gestione dei fondi Ue • Nove da Firenze |
| 4 | 0.05684943 | nove.firenze.it | 2026-03-31 | Variazione in bilancio per chiudere i conti 2025 della sanità toscana • Nove da Firenze |
| 5 | 0.05345949 | lagazzettadelmezzogiorno.it | 2026-07-08 | Crisafi (Remind) “Costruiamo insieme l’Italia che abiteremo” - Gazzetta del Mezzogiorno |
| 6 | 0.05341134 | vocedimantova.it | 2026-07-08 | Crisafi (Remind) “Costruiamo insieme l’Italia che abiteremo” \| la Voce Di Mantova |
| 7 | 0.05334262 | iltempo.it | 2026-07-08 | Crisafi (Remind) “Costruiamo insieme l'Italia che abiteremo” – Il Tempo |
| 8 | 0.05322056 | ansa.it | 2026-02-19 | Nuovo confronto in Assemblea legislativa sulla liste d'attesa - Notizie - Ansa.it |
| 9 | 0.05251710 | lasicilia.it | 2026-05-13 | Caro carburante, lavoratori Asu, B&b, dipendenti regionali: tutte le ultime norme approvate dall'Ars - La Sicilia |
| 10 | 0.05173822 | varesenews.it | 2026-06-17 | "L'Ecosistema del Valore": l'impatto economico e sociale di Acinque per lo sviluppo del territorio |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.01442459 | 0.37708258 | gazzettadelsud.it | 2026-02-17 | Cardiochirurgia pediatrica di Taormina, l'affondo di De Luca: "In commissione approvato un pastrocchio" - Gazzetta del Sud |
| 2 | 0.03197236 | 0.80633284 | bresciaoggi.it | 2026-01-13 | A Brescia arriveranno 24 nuovi poliziotti, il sindacato: «Ma ancora non bastano» \| Bresciaoggi |
| 3 | 0.02379013 | 0.40375400 | giornaledibrescia.it | 2026-06-20 | Scontro sul futuro bilancio dell’Ue, l’Italia guida il fronte della coesione \| Giornale di Brescia |
| 4 | 0.01798411 | 0.36579619 | ilmattino.it | 2026-04-28 | Elezioni ad Avellino, la battaglia sui programmi dallo stadio al salario minimo |
| 5 | 0.02354256 | 0.54136290 | ilrestodelcarlino.it | 2026-01-16 | Rifiuti abbandonati: ecco come premiare chi è virtuoso |

### Topic 10

- Articoli: 9955 (11.277%).
- Termini registrati: iran, tajani, trump, esteri, guerra, uniti, usa, ministro, israele, ministro esteri, paesi, europa
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | ansa.it | 1317 | 13.230% |
| 2 | iltempo.it | 774 | 7.775% |
| 3 | ilgiornale.it | 683 | 6.861% |
| 4 | adnkronos.com | 476 | 4.782% |
| 5 | ilmessaggero.it | 453 | 4.550% |
| 6 | lastampa.it | 429 | 4.309% |
| 7 | laverita.info | 373 | 3.747% |
| 8 | italpress.com | 339 | 3.405% |
| 9 | ilfattoquotidiano.it | 335 | 3.365% |
| 10 | ilsole24ore.com | 319 | 3.204% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 1332 |
| 2026-02 | 1187 |
| 2026-03 | 2083 |
| 2026-04 | 1738 |
| 2026-05 | 1608 |
| 2026-06 | 1504 |
| 2026-07 | 503 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.08392033 | ilgiornale.it | 2026-03-10 | Allarme degli 007 Usa: "Teheran vuole minare Hormuz". Trump: "Le rimuova o conseguenze mai viste". Italia, Germania e Inghilterra al lavoro per proteggere le navi - il Giornale |
| 2 | 0.08294643 | lastampa.it | 2026-04-08 | Guerra Iran, le news dopo lâattacco di Usa Israele. La diretta - La Stampa |
| 3 | 0.08282926 | repubblica.it | 2026-04-09 | Guerra in Iran, le news del 9 aprile. Idf: “Evacuare Beirut sud”. Hormuz ancora chiuso - la Repubblica |
| 4 | 0.08254604 | ilsole24ore.com | 2026-03-15 | Iran, «Amministrazione Trump pronta ad annunciare coalizione per Hormuz». Berlino: «Non parteciperemo» - Il Sole 24 ORE |
| 5 | 0.08238322 | repubblica.it | 2026-03-19 | Guerra in Iran, le news del 19 marzo - la Repubblica |
| 6 | 0.08220454 | ilsole24ore.com | 2026-03-04 | Teheran spara contro Turchia, scudo della Nato. Media Usa: iniziata un’offensiva di terra di migliaia di curdi  - Il Sole 24 ORE |
| 7 | 0.08132371 | ilsole24ore.com | 2026-04-08 | Guerra in Iran, ultime notizie - Iran blocca Hormuz dopo raid Israele in Libano. Macron: tregua deve includerlo - Il Sole 24 ORE |
| 8 | 0.08129876 | ilsole24ore.com | 2026-03-02 | Colpita ambasciata Usa a Riyadh. Israele riprende ad attaccare Teheran. Usa: «Hormuz è aperto» - Il Sole 24 ORE |
| 9 | 0.08078433 | ilgiornale.it | 2026-04-02 | Razzo sulla base italiana Unifil in Libano. Sale a 40 il numero di Paesi nella coalizione per Hormuz. Hegseth caccia il capo di Stato maggiore dell'Esercito Usa - il Giornale |
| 10 | 0.08071469 | lastampa.it | 2026-03-03 | Guerra Iran, le news dopo lâattacco di Usa Israele. La diretta - La Stampa |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.00720419 | 0.40058646 | askanews.it | 2026-05-04 | Paesi Asia-Pacifico contro quasi monopolio Cina terre rare |
| 2 | 0.01524886 | 0.33596519 | ilmanifesto.it | 2026-05-16 | Nuovi colonialismi, i partiti comunisti contro l’allargamento a est di Macron \| il manifesto |
| 3 | 0.04550529 | 0.61849803 | ansa.it | 2026-03-06 | Meloni e gli europei, 'diplomazia e coordinamento militare' - Notizie - Ansa.it |
| 4 | 0.02866451 | 0.69974883 | gazzettadiparma.it | 2026-04-21 | Tajani, 'meglio sanzioni a coloni violenti che stop a intesa Ue-Israele' - Gazzetta di Parma |
| 5 | 0.01451043 | 0.49329630 | repubblica.it | 2026-02-23 | Dazi, Foti: “Stop allarmismi, Parigi vuole il bazooka ma è stupido usarlo” - la Repubblica |

### Topic 11

- Articoli: 792 (0.897%).
- Termini registrati: ansa, ansa it, it, cookie, notizie ansa, it abbonati, abbonamento, notizie, abbonati, evidenza, leggere, informazione
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | ansa.it | 730 | 92.172% |
| 2 | lagazzettadelmezzogiorno.it | 32 | 4.040% |
| 3 | ladige.it | 9 | 1.136% |
| 4 | lanazione.it | 5 | 0.631% |
| 5 | ilrestodelcarlino.it | 4 | 0.505% |
| 6 | ilgiorno.it | 3 | 0.379% |
| 7 | gazzettadiparma.it | 2 | 0.253% |
| 8 | ilsecoloxix.it | 2 | 0.253% |
| 9 | lasicilia.it | 2 | 0.253% |
| 10 | ilfattoquotidiano.it | 1 | 0.126% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 107 |
| 2026-02 | 130 |
| 2026-03 | 110 |
| 2026-04 | 139 |
| 2026-05 | 119 |
| 2026-06 | 152 |
| 2026-07 | 35 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.31830337 | ansa.it | 2026-03-31 | Futuro Nazionale, Vannacci incontra la stampa - Primopiano - Ansa.it |
| 2 | 0.30915006 | ansa.it | 2026-04-13 | Tajani è atterrato a Beirut - Primopiano - Ansa.it |
| 3 | 0.30858170 | ansa.it | 2026-03-31 | Camera, in aula il decreto bollette, le dichiarazioni di voto - Primopiano - Ansa.it |
| 4 | 0.30688812 | ansa.it | 2026-02-15 | Ucciso migrante da un agente a Verona, il video-choc sui social di Ilaria Cucchi - Italia - Ansa.it |
| 5 | 0.30628844 | ansa.it | 2026-04-23 | Roma, cerimonia alla Farnesina per le targhe dei Giusti - Primopiano - Ansa.it |
| 6 | 0.30604790 | ansa.it | 2026-02-21 | Tajani a Forlì incontra Roberto Donadoni - Primopiano - Ansa.it |
| 7 | 0.30317295 | ansa.it | 2026-04-11 | Il vicepremier Matteo Salvini a un gazebo della Lega a Milano - Primopiano - Ansa.it |
| 8 | 0.30184081 | ansa.it | 2026-04-21 | La premier Meloni in visita al Salone del Mobile - People - Ansa.it |
| 9 | 0.30019467 | ansa.it | 2026-06-04 | Il ministro Matteo Salvini interviene agli Stati generali dell'abitare - People - Ansa.it |
| 10 | 0.29988685 | ansa.it | 2026-03-23 | Referendum, conferenza stampa del M5s dopo la vittoria del No - Primopiano - Ansa.it |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.01052589 | 0.22013991 | ansa.it | 2026-05-08 | A Roma l'evento “Luci d’Europa”. Attesa la Presidente Metsola - Altre news - Ansa.it |
| 2 | 0.01031866 | 0.40237778 | ansa.it | 2026-06-26 | Inselvini (FdI), 'la droga è schiavitù e morte, tolleranza zero' - La voce degli Eurodeputati - Ansa.it |
| 3 | 0.00736803 | 0.32746655 | ansa.it | 2026-05-14 | In Fvg riconfermate anche nel 2026 le Bandiere blu a Grado e Lignano - Notizie - Ansa.it |
| 4 | 0.01322335 | 0.30921038 | ansa.it | 2026-05-21 | Salvini, 'il ponte sullo Stretto unirà il Paese nel nome della velocità' - Notizie - Ansa.it |
| 5 | 0.01544587 | 0.40415879 | ansa.it | 2026-05-20 | Dl lavoro: 189 emendamenti inammissibili, resta proposta Lega-Fi salva-imprenditori - Notizie - Ansa.it |

## Interpretazioni e limiti

- I conteggi precedenti sono fatti quantitativi riproducibili.
- Il report non assegna nomi definitivi né giudizi semantici ai topic.
- I quasi duplicati sono un proxy basato sul prefisso normalizzato degli estratti, non sul full-text.
- Gli estratti hanno lunghezza massima di 500 caratteri.
- I record ad alto peso possono rappresentare boilerplate molto distintivo.

## Avvisi automatici

- Il metadata sorgente contiene un percorso input assoluto; il percorso è oscurato negli output.
- Topic con dominio dominante >= 50.0%: [1, 2, 5, 7, 11]

## Output

- [`topic_distribution.csv`](topic_distribution.csv)
- [`confidence_summary.csv`](confidence_summary.csv)
- [`domain_summary.csv`](domain_summary.csv)
- [`duplicate_summary.json`](duplicate_summary.json)
- [`run_manifest.json`](run_manifest.json)
