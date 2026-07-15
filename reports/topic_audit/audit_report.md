# Audit riproducibile degli output NMF

> Report generato automaticamente da `scripts/run_topic_audit.py`.

## Fatti quantitativi

### Distribuzione dei topic

| Topic | Articoli | Percentuale |
|---|---|---|
| 0 | 3099 | 3.217% |
| 1 | 30908 | 32.081% |
| 2 | 669 | 0.694% |
| 3 | 635 | 0.659% |
| 4 | 2303 | 2.390% |
| 5 | 898 | 0.932% |
| 6 | 394 | 0.409% |
| 7 | 392 | 0.407% |
| 8 | 16934 | 17.576% |
| 9 | 29165 | 30.271% |
| 10 | 2726 | 2.829% |
| 11 | 8222 | 8.534% |

Output tabellare: [`topic_distribution.csv`](topic_distribution.csv).

### Confidenza normalizzata

| Metrica | Valore |
|---|---|
| min | 0.16285565 |
| mean | 0.63621972 |
| median | 0.61227740 |
| p25 | 0.48605502 |
| p75 | 0.78128437 |
| p90 | 0.92276714 |
| p99 | 1.00000000 |
| exactly_1_percentage | 1.18843739 |
| below_0.40_percentage | 9.94135658 |
| below_0.50_percentage | 28.02324978 |
| below_0.60_percentage | 47.81877627 |

La confidenza è `max(pesi NMF) / somma(pesi NMF)`: non è una probabilità calibrata.
Output completo: [`confidence_summary.csv`](confidence_summary.csv).

### Duplicazioni

| Sezione | Metrica | Valore |
|---|---|---|
| exact_excerpt | records_in_duplicate_groups | 11459 |
| exact_excerpt | duplicate_groups | 2772 |
| exact_excerpt | largest_group | 3095 |
| exact_title_excerpt | records_in_duplicate_groups | 4565 |
| exact_title_excerpt | duplicate_groups | 1823 |
| exact_title_excerpt | largest_group | 535 |
| near_duplicate_proxy | prefix_length | 300 |
| near_duplicate_proxy | records_in_duplicate_groups | 13642 |
| near_duplicate_proxy | duplicate_groups | 3573 |
| near_duplicate_proxy | largest_group | 3095 |
| near_duplicate_proxy | definition | same normalized prefix of the review excerpt |

Output strutturato: [`duplicate_summary.json`](duplicate_summary.json).

### Parametri registrati dal classificatore

```json
{
  "created_at_utc": "2026-07-12T08:27:10.550961+00:00",
  "input": "mediacloud_fulltext.jsonl",
  "articles": 96345,
  "tfidf_shape": [
    96345,
    1531569
  ],
  "n_topics": 12,
  "requested_n_topics": 12,
  "min_df": 3,
  "max_df": 0.85,
  "random_state": 42
}
```

## Evidenze per topic

### Topic 0

- Articoli: 3099 (3.217%).
- Termini registrati: in evidenza, evidenza, evidenza presentato, presentato, di rett, rett, bisogni prospettive, su air, rett bisogni, acadia, trump mandati, adnkronos acadia
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | adnkronos.com | 3096 | 99.903% |
| 2 | lagazzettadelmezzogiorno.it | 1 | 0.032% |
| 3 | lanazione.it | 1 | 0.032% |
| 4 | laverita.info | 1 | 0.032% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 414 |
| 2026-02 | 495 |
| 2026-03 | 444 |
| 2026-04 | 443 |
| 2026-05 | 511 |
| 2026-06 | 570 |
| 2026-07 | 222 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.13436381 | adnkronos.com | 2026-03-24 | イラン：ベイルート、「レバノンでのイスラエル攻撃開始以来1,070人以上が死亡」 |
| 2 | 0.13436381 | adnkronos.com | 2026-04-08 | レバノン保健省、死者数は112人に増加、負傷者は837人 |
| 3 | 0.13436381 | adnkronos.com | 2026-02-03 | ウクライナ、ハルキウへのロシアの空爆で1人死亡、5人負傷 |
| 4 | 0.13436381 | adnkronos.com | 2026-02-03 | ブラジル北東部でバス事故、少なくとも15人死亡 |
| 5 | 0.13436381 | adnkronos.com | 2026-03-17 | ナイジェリア北東部で自爆テロ：死者23人、負傷者108人 |
| 6 | 0.13436381 | adnkronos.com | 2026-05-20 | テヘラン、「過去24時間で26隻の船がホルムズ海峡を通過」 |
| 7 | 0.13436381 | adnkronos.com | 2026-01-16 | ウクライナ、ドニプロペトロウシクへのロシアの空爆で女性2人死亡 |
| 8 | 0.13436381 | adnkronos.com | 2026-03-30 | ベネズエラ、7年間の停止を経てカラカスで米国大使館が再開 |
| 9 | 0.13436381 | adnkronos.com | 2026-07-02 | シリア、ダマスカスのカフェで爆発、死者7人に増加 |
| 10 | 0.13436381 | adnkronos.com | 2026-01-21 | シリア、「クルド部隊のドローン攻撃で兵士7人死亡」 |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.13317397 | 0.99697404 | adnkronos.com | 2026-04-17 | GrAudio edizione delle 16:30 del 17 aprile |
| 2 | 0.13298923 | 0.99894252 | adnkronos.com | 2026-01-15 | GrAudio edizione delle 18:30 del 15 gennaio |
| 3 | 0.13339568 | 0.99597412 | adnkronos.com | 2026-06-23 | GrAudio edizione delle 18:30 del 23 giugno |
| 4 | 0.13292013 | 0.99804670 | adnkronos.com | 2026-04-22 | GrAudio Flash delle 18:50 del 22 aprile |
| 5 | 0.12737217 | 0.98102268 | adnkronos.com | 2026-05-20 | Rubrica delle buone notizie del 20 maggio |

### Topic 1

- Articoli: 30908 (32.081%).
- Termini registrati: si, ma, da, al, le, partito, se, ci, chi, alla, centrodestra, pd
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | ilgiornale.it | 2978 | 9.635% |
| 2 | iltempo.it | 2014 | 6.516% |
| 3 | lanazione.it | 1758 | 5.688% |
| 4 | repubblica.it | 1710 | 5.533% |
| 5 | lastampa.it | 1465 | 4.740% |
| 6 | ilrestodelcarlino.it | 1336 | 4.323% |
| 7 | ilmessaggero.it | 1212 | 3.921% |
| 8 | ilmattino.it | 1151 | 3.724% |
| 9 | ilfoglio.it | 1114 | 3.604% |
| 10 | ilfattoquotidiano.it | 1081 | 3.497% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 2885 |
| 2026-02 | 5226 |
| 2026-03 | 6212 |
| 2026-04 | 4721 |
| 2026-05 | 5031 |
| 2026-06 | 5312 |
| 2026-07 | 1521 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.05402650 | repubblica.it | 2026-03-23 | I risultati del Referendum Giustizia 2026: vince il no - la Repubblica |
| 2 | 0.05264575 | lastampa.it | 2026-03-23 | Risultati Referendum 2026, vince il NO Segui la diretta - La Stampa |
| 3 | 0.05043786 | lastampa.it | 2026-03-24 | Referendum 2026, dopo il voto si dimettono Delmastro e Bartolozzi - La Stampa |
| 4 | 0.04989536 | lastampa.it | 2026-05-26 | Risultati amministrative 2026. Meloni "Il nostro crollo rimandato a domani". La diretta - La Stampa |
| 5 | 0.04931020 | laverita.info | 2026-03-19 | Barbera: «La sinistra che voterà No solo per dar contro a Meloni tradisce la Costituzione» — La Verità |
| 6 | 0.04836242 | repubblica.it | 2026-03-25 | Santanchè ha dato le dimissioni \| Le news di oggi in diretta - la Repubblica |
| 7 | 0.04806471 | repubblica.it | 2026-03-24 | Referendum Giustizia 2026, le reazioni dopo i risultati \| Diretta   - la Repubblica |
| 8 | 0.04670681 | lastampa.it | 2026-03-25 | SantanchÃ© si Ã¨ dimessa, lettera a Meloni: âCara Giorgia, il mio certificato penale Ã¨ immacolatoâ - Segui la diretta - La Stampa |
| 9 | 0.04642410 | tpi.it | 2026-03-06 | Referendum di mid-term: perché il 22-23 marzo la posta in gioco è doppia |
| 10 | 0.04594883 | ilfoglio.it | 2026-05-25 | De Luca a valanga a Salerno. A Venezia il centrodestra verso la vittoria al primo turno. I risultati delle comunali |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.02394013 | 0.49401362 | ansa.it | 2026-03-09 | Conte: 'Meloni scatenata, sulla giustizia il disegno della P2' - Dirette e live - Ansa.it |
| 2 | 0.01028268 | 0.38751147 | bresciaoggi.it | 2026-01-23 | Manerba, si è spento Tonino Simoni: una vita di impegno per la sua comunità \| Bresciaoggi |
| 3 | 0.01535350 | 0.34569953 | italpress.com | 2026-03-23 | Referendum, Meloni "Occasione persa per modernizzare l'Italia, ma andiamo avanti" Agenzia di stampa Italpress - Italpress |
| 4 | 0.01830411 | 0.64505906 | lasicilia.it | 2026-07-09 | Futuro nazionale, exploit di comitati in Sicilia dopo il tour di Vannacci: quasi raddoppiati a 153 - La Sicilia |
| 5 | 0.00907176 | 0.56499385 | mediaset.it | 2026-03-22 | Pontida, l'ultimo saluto a Umberto Bossi |

### Topic 2

- Articoli: 669 (0.694%).
- Termini registrati: vai all, all articolo, vai, articolo al, su raiplay, al video, raiplay, pagina, clicca qui, clicca, video promo, raiplay vai
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | rai.it | 666 | 99.552% |
| 2 | askanews.it | 2 | 0.299% |
| 3 | ilrestodelcarlino.it | 1 | 0.149% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 75 |
| 2026-02 | 106 |
| 2026-03 | 137 |
| 2026-04 | 85 |
| 2026-05 | 104 |
| 2026-06 | 122 |
| 2026-07 | 40 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.18868751 | rai.it | 2026-01-11 | Televideo - Homepage |
| 2 | 0.18868751 | rai.it | 2026-01-11 | Televideo - Homepage |
| 3 | 0.18868751 | rai.it | 2026-01-12 | Televideo - Homepage |
| 4 | 0.18868751 | rai.it | 2026-01-12 | Televideo - Homepage |
| 5 | 0.18868751 | rai.it | 2026-01-12 | Televideo - Homepage |
| 6 | 0.18868751 | rai.it | 2026-01-12 | Televideo - Homepage |
| 7 | 0.18868751 | rai.it | 2026-01-13 | Televideo - Homepage |
| 8 | 0.18868751 | rai.it | 2026-01-13 | Televideo - Homepage |
| 9 | 0.18868751 | rai.it | 2026-01-13 | Televideo - Homepage |
| 10 | 0.18868751 | rai.it | 2026-01-13 | Televideo - Homepage |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.18868751 | 1.00000000 | rai.it | 2026-01-30 | Televideo - Homepage |
| 2 | 0.18868751 | 1.00000000 | rai.it | 2026-02-19 | Televideo - Homepage |
| 3 | 0.18868751 | 1.00000000 | rai.it | 2026-03-03 | Televideo - Homepage |
| 4 | 0.18868751 | 1.00000000 | rai.it | 2026-04-17 | Televideo - Homepage |
| 5 | 0.18868751 | 1.00000000 | rai.it | 2026-05-03 | Televideo - Homepage |

### Topic 3

- Articoli: 635 (0.659%).
- Termini registrati: peppino, capri, di capri, peppino di, sanremo, rockers, nel partecipa, nel vince, champagne, incide, giuliana, album
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | ilfattoquotidiano.it | 622 | 97.953% |
| 2 | askanews.it | 5 | 0.787% |
| 3 | repubblica.it | 3 | 0.472% |
| 4 | adnkronos.com | 1 | 0.157% |
| 5 | affaritaliani.it | 1 | 0.157% |
| 6 | ilgiorno.it | 1 | 0.157% |
| 7 | lastampa.it | 1 | 0.157% |
| 8 | mediaset.it | 1 | 0.157% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 89 |
| 2026-02 | 157 |
| 2026-03 | 67 |
| 2026-04 | 31 |
| 2026-05 | 115 |
| 2026-06 | 99 |
| 2026-07 | 77 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.21525363 | ilfattoquotidiano.it | 2026-07-04 | Attentato |
| 2 | 0.21523437 | ilfattoquotidiano.it | 2026-05-30 | Panico? |
| 3 | 0.21520540 | ilfattoquotidiano.it | 2026-06-06 | Montenegro |
| 4 | 0.21516288 | ilfattoquotidiano.it | 2026-02-08 | Montanari sul Nove: " |
| 5 | 0.21513054 | ilfattoquotidiano.it | 2026-05-26 | Il Papa contro l'IA |
| 6 | 0.21512679 | ilfattoquotidiano.it | 2026-06-27 | Clima: situazione attuale |
| 7 | 0.21508689 | ilfattoquotidiano.it | 2026-01-17 | La Riforma Addams |
| 8 | 0.21500726 | ilfattoquotidiano.it | 2026-06-10 | Al via i lavori |
| 9 | 0.21492296 | ilfattoquotidiano.it | 2026-07-03 | La sostituta |
| 10 | 0.21488609 | ilfattoquotidiano.it | 2026-06-09 | Manica larga |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.21414076 | 1.00000000 | ilfattoquotidiano.it | 2026-01-31 | Corteo Askatasuna a Torino: 50mila persone secondo gli organizzatori |
| 2 | 0.21301854 | 0.99706465 | ilfattoquotidiano.it | 2026-02-02 | Olimpiadi Milano-Cortina, lo stupore dell'atleta canadese davanti al bidet in camera: "Ooh" - Video |
| 3 | 0.21403112 | 0.99795813 | ilfattoquotidiano.it | 2026-02-06 | Referendum giustizia, Nordio: "Vinceremo e modificheremo codice procedura penale" \| Il Fatto |
| 4 | 0.21376367 | 1.00000000 | ilfattoquotidiano.it | 2026-02-10 | Milano Cortina: lame dei pattini danneggiate dal podio, protesta del Giappone |
| 5 | 0.21474171 | 1.00000000 | ilfattoquotidiano.it | 2026-05-17 | Giornata contro l'omofobia, Mattarella: "In Italia persistono discriminazioni" |

### Topic 4

- Articoli: 2303 (2.390%).
- Termini registrati: varese, di varese, varese le, scuola realizzata, altre ecco, felice su, su pronta, prima scuola, realizzata il, pnrr in, punto siamo, pronta la
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | varesenews.it | 2289 | 99.392% |
| 2 | laverita.info | 6 | 0.261% |
| 3 | mediaset.it | 2 | 0.087% |
| 4 | ilsecoloxix.it | 1 | 0.043% |
| 5 | ladige.it | 1 | 0.043% |
| 6 | lagazzettadelmezzogiorno.it | 1 | 0.043% |
| 7 | lanazione.it | 1 | 0.043% |
| 8 | lastampa.it | 1 | 0.043% |
| 9 | vocedimantova.it | 1 | 0.043% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 118 |
| 2026-02 | 160 |
| 2026-03 | 194 |
| 2026-04 | 222 |
| 2026-05 | 512 |
| 2026-06 | 630 |
| 2026-07 | 467 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.18039043 | varesenews.it | 2026-03-26 | A Varese il generale Vannacci riempie la sala: “Futuro Nazionale nel 2027 ci sarà” |
| 2 | 0.17645947 | varesenews.it | 2026-03-23 | Referendum, Alfieri (Pd) “Il governo esce sconfitto, ora serve un’alternativa” |
| 3 | 0.17046471 | varesenews.it | 2026-06-24 | Sinistra Italiana: "La Lombardia non è immune dalle mafie, negarne il radicamento è un errore" |
| 4 | 0.17028307 | varesenews.it | 2026-07-01 | Serate di evangelizzazione sotto la tenda con la Chiesa Evangelica ADI Castellanza |
| 5 | 0.16716683 | varesenews.it | 2026-07-01 | Ferita una turista di 45 anni caduta in bici nelle valli sopra a Maccagno con Pino e Veddasca |
| 6 | 0.16698147 | varesenews.it | 2026-07-06 | Ai domiciliari per tentato omicidio, 92enne trovato a passeggio: arrestato a Stresa per evasione |
| 7 | 0.16662858 | varesenews.it | 2026-02-27 | Dal Lago Maggiore a Sanremo, l’arte femminile celebra il “Golden Sound of Nature” |
| 8 | 0.16583108 | varesenews.it | 2026-07-05 | Al Sacro Monte arriva Ippolita Baldini: Santa Chiara raccontata tra ironia, cabaret e teatro |
| 9 | 0.16481314 | varesenews.it | 2026-06-22 | Sequestrati a Malpensa due teschi di coccodrillo provenienti dalla Cambogia |
| 10 | 0.16407302 | varesenews.it | 2026-04-30 | L'isola più antica delle Alpi riapre dopo 3 anni e anche l'ippodromo è pronto |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.11297515 | 0.92160827 | varesenews.it | 2026-01-14 | Pellicini: “Solidarietà al cittadino aggredito nella sua casa a Lonate Pozzolo” |
| 2 | 0.10434514 | 0.94284637 | varesenews.it | 2026-04-30 | Summer camp a Malnate: alla Tenuta La Novella settimane tra fattoria, natura e inglese |
| 3 | 0.12372785 | 0.96346792 | varesenews.it | 2026-05-02 | A Lugano il Primo Maggio finisce in rissa, spray urticante per riportare la calma |
| 4 | 0.10549177 | 0.89094182 | varesenews.it | 2026-06-20 | Festa e diritti arcobaleno nella Città Giardino per il decimo Varese Pride |
| 5 | 0.08802111 | 0.83002926 | varesenews.it | 2026-07-01 | Cedri di viale Aguggiari, Europa Verde chiede lo stop al taglio: “Serve perizia super partes” |

### Topic 5

- Articoli: 898 (0.932%).
- Termini registrati: agenzia vista, agenzia, il tempo, bertoldi states, nato milei, states trump, livello valditara, centrodestra pubblicit, decisionali alessandro, studentesca ai, studentesche ai, partecipazione studentesca
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | iltempo.it | 891 | 99.220% |
| 2 | askanews.it | 3 | 0.334% |
| 3 | lagazzettadelmezzogiorno.it | 3 | 0.334% |
| 4 | laverita.info | 1 | 0.111% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 127 |
| 2026-02 | 96 |
| 2026-03 | 167 |
| 2026-04 | 166 |
| 2026-05 | 130 |
| 2026-06 | 175 |
| 2026-07 | 37 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.18715812 | iltempo.it | 2026-03-23 | Il Ministro Tajani vota per il referendum sulla giustizia a Fiuggi – Il Tempo |
| 2 | 0.18282626 | iltempo.it | 2026-06-18 | Meloni arriva al Consiglio Ue di Bruxelles – Il Tempo |
| 3 | 0.18226974 | iltempo.it | 2026-04-09 | Meloni entra in Senato per informativa in Aula – Il Tempo |
| 4 | 0.17751123 | iltempo.it | 2026-01-16 | Takaichi fa gli auguri di compleanno a Meloni, l'applauso della delegazione giapponese – Il Tempo |
| 5 | 0.17644590 | iltempo.it | 2026-04-30 | Salvini: Sono sempre d'accordo con la Presidente del Consiglio – Il Tempo |
| 6 | 0.17591734 | iltempo.it | 2026-03-24 | Barelli (Fi): Ha vinto il No al Referendum, ma non è una sconfitta politica – Il Tempo |
| 7 | 0.17584432 | iltempo.it | 2026-03-22 | Elly Schlein vota per il Referendum sulla giustizia – Il Tempo |
| 8 | 0.17455130 | iltempo.it | 2026-02-10 | Calenda: Vannacci da sempre sostiene le ragioni di Putin – Il Tempo |
| 9 | 0.17185903 | iltempo.it | 2026-05-08 | Rubio arriva a Palazzo Chigi per incontrare Meloni – Il Tempo |
| 10 | 0.17069406 | iltempo.it | 2026-07-10 | Rampelli: Non si possono fare banchetti sull'Altare della Patria – Il Tempo |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.11227095 | 0.91330338 | iltempo.it | 2026-01-28 | Referendum Giustizia, Boccia: Grave che Governo blocchi voto ai fuori sede – Il Tempo |
| 2 | 0.13493667 | 0.91955402 | iltempo.it | 2026-03-03 | Meloni: Record storico occupazione femminile, risultato di cui vado fiera – Il Tempo |
| 3 | 0.13634740 | 0.88959641 | iltempo.it | 2026-04-09 | Referendum giustizia, Meloni: Abbiamo coscienza a posto, onorata parola responsabilità – Il Tempo |
| 4 | 0.10472057 | 0.87527692 | iltempo.it | 2026-04-09 | Richetti (Azione) a Meloni: No a un anno e mezzo di campagna elettorale in momento di crisi – Il Tempo |
| 5 | 0.10687488 | 0.82438940 | iltempo.it | 2026-05-21 | Meloni a Niscemi: 150 milioni per messa in sicurezza e indennizzi, domani in Consiglio dei Ministri – Il Tempo |

### Topic 6

- Articoli: 394 (0.409%).
- Termini registrati: websalvasalvata, redazione websalvasalvata, redazione, di redazione, antipasti, traghetti bus, luglio treni, treni traghetti, bus rischio, coinvoltesalvasalvata, regioni coinvoltesalvasalvata, traghetti
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | ilmessaggero.it | 341 | 86.548% |
| 2 | ilmattino.it | 50 | 12.690% |
| 3 | lagazzettadelmezzogiorno.it | 2 | 0.508% |
| 4 | leggo.it | 1 | 0.254% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-02 | 65 |
| 2026-03 | 53 |
| 2026-04 | 82 |
| 2026-05 | 71 |
| 2026-06 | 85 |
| 2026-07 | 38 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.24610014 | ilmessaggero.it | 2026-05-18 | Mondiali 2026 |
| 2 | 0.24570788 | ilmessaggero.it | 2026-05-17 | Roma-Lazio |
| 3 | 0.24564158 | ilmessaggero.it | 2026-05-20 | Palermo-Catanzaro |
| 4 | 0.24532426 | ilmessaggero.it | 2026-06-16 | Francia-Senegal 3-1 |
| 5 | 0.24522785 | ilmessaggero.it | 2026-05-04 | Cremonese-Lazio 1-2 |
| 6 | 0.24497332 | ilmessaggero.it | 2026-02-28 | Inter-Genoa |
| 7 | 0.24494306 | ilmessaggero.it | 2026-02-16 | Sinner debutta a Doha |
| 8 | 0.24492739 | ilmessaggero.it | 2026-03-01 | Cremonese-Milan 0-2 |
| 9 | 0.24488031 | ilmessaggero.it | 2026-05-11 | Napoli-Bologna 2-3 |
| 10 | 0.24486773 | ilmessaggero.it | 2026-05-18 | Napoli-Conte |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.09391997 | 0.91773411 | ilmattino.it | 2026-03-14 | ​La delegazione della LILT di Capri ha festeggiato il suo ventesimo compleanno |
| 2 | 0.07696797 | 0.87604605 | ilmattino.it | 2026-04-27 | Rosi la gattina salvata a Roma: dopo cure e ricovero trova finalmente una nuova casa |
| 3 | 0.22821793 | 0.99480464 | ilmessaggero.it | 2026-02-24 | L'artista a Castel di Tora |
| 4 | 0.19576532 | 0.96818311 | ilmessaggero.it | 2026-02-18 | Caffé a rischio estinzione, la «cintura dei chicchi» non riesce più a produrre l'Arabica |
| 5 | 0.20572358 | 0.97415459 | ilmessaggero.it | 2026-03-17 | Processo Becciu, riparte il dibattimento |

### Topic 7

- Articoli: 392 (0.407%).
- Termini registrati: corriere di, personaggi opinioni, attualita esteri, carlo antini, tempo tv, rieti corriere, antini, edicola digitale, controtempo, di rieti, chi siamo, di viterbo
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | iltempo.it | 255 | 65.051% |
| 2 | repubblica.it | 108 | 27.551% |
| 3 | laverita.info | 14 | 3.571% |
| 4 | rai.it | 5 | 1.276% |
| 5 | lanazione.it | 3 | 0.765% |
| 6 | ilgiorno.it | 2 | 0.510% |
| 7 | italpress.com | 2 | 0.510% |
| 8 | ilmessaggero.it | 1 | 0.255% |
| 9 | ilrestodelcarlino.it | 1 | 0.255% |
| 10 | ilsecoloxix.it | 1 | 0.255% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 42 |
| 2026-02 | 58 |
| 2026-03 | 42 |
| 2026-04 | 117 |
| 2026-05 | 78 |
| 2026-06 | 41 |
| 2026-07 | 14 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.25405094 | iltempo.it | 2026-06-10 | Meloni "L'Italia non è la repubblica delle banane" – Il Tempo |
| 2 | 0.25349122 | iltempo.it | 2026-02-27 | Salvini "Lavorerò per le Olimpiadi di Roma 2040" – Il Tempo |
| 3 | 0.24934196 | iltempo.it | 2026-05-04 | Nato, Meloni "L'Italia ha sempre mantenuto gli impegni" – Il Tempo |
| 4 | 0.24833567 | iltempo.it | 2026-04-23 | Energia, Meloni "L'Europa sia più coraggiosa" – Il Tempo |
| 5 | 0.24764154 | iltempo.it | 2026-03-02 | Iran, Salvini "L'Italia non è in guerra, non manderemo soldati" – Il Tempo |
| 6 | 0.24718475 | iltempo.it | 2026-01-28 | Meloni a Niscemi, le immagini dell'arrivo – Il Tempo |
| 7 | 0.24708251 | iltempo.it | 2026-06-15 | Lega, Guidesi "Discussione sia strutturale, non contingente o elettorale" – Il Tempo |
| 8 | 0.24617437 | iltempo.it | 2026-05-11 | Tajani "L'Iran non può avere l'arma nucleare" – Il Tempo |
| 9 | 0.24599425 | iltempo.it | 2026-01-28 | Niscemi, Meloni "Non ripetere il '97, lavorare insieme per risposte rapide" – Il Tempo |
| 10 | 0.24596034 | iltempo.it | 2026-04-23 | Migranti, Meloni "Servono soluzioni innovative" – Il Tempo |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.22840275 | 0.99768832 | iltempo.it | 2026-01-12 | Meloni "Gioia per liberazione di Trentini e Burlò, al lavoro col Venezuela" – Il Tempo |
| 2 | 0.23370536 | 0.99693086 | iltempo.it | 2026-05-04 | Ue, Salvini "Superare il Patto di Stabilità è questione di sopravvivenza" – Il Tempo |
| 3 | 0.23336868 | 0.98453579 | iltempo.it | 2026-05-07 | Ue, Meloni "Da Italia e Polonia stessa linea sul nuovo quadro finanziario" – Il Tempo |
| 4 | 0.01012668 | 0.38257320 | repubblica.it | 2026-04-09 | Fenerbahçe - Real Madrid (69-74) Euroleague - la Repubblica |
| 5 | 0.01014371 | 0.38180715 | repubblica.it | 2026-04-19 | Torino - Baltur Cento (80-69) Serie A2 - la Repubblica |

### Topic 8

- Articoli: 16934 (17.576%).
- Termini registrati: trump, meloni, iran, tajani, ministro, uniti, stati uniti, usa, stati, esteri, guerra, premier
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | iltempo.it | 1523 | 8.994% |
| 2 | askanews.it | 1081 | 6.384% |
| 3 | ilgiornale.it | 1060 | 6.260% |
| 4 | ansa.it | 906 | 5.350% |
| 5 | ilmessaggero.it | 894 | 5.279% |
| 6 | repubblica.it | 893 | 5.273% |
| 7 | adnkronos.com | 849 | 5.014% |
| 8 | italpress.com | 768 | 4.535% |
| 9 | lastampa.it | 690 | 4.075% |
| 10 | laverita.info | 588 | 3.472% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 1932 |
| 2026-02 | 1833 |
| 2026-03 | 3015 |
| 2026-04 | 3568 |
| 2026-05 | 2771 |
| 2026-06 | 2897 |
| 2026-07 | 918 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.09292682 | repubblica.it | 2026-04-09 | Guerra in Iran, le news del 9 aprile. Idf: “Evacuare Beirut sud”. Hormuz ancora chiuso - la Repubblica |
| 2 | 0.09203011 | ilsole24ore.com | 2026-04-08 | Guerra in Iran, ultime notizie - Iran blocca Hormuz dopo raid Israele in Libano. Macron: tregua deve includerlo - Il Sole 24 ORE |
| 3 | 0.09181207 | lastampa.it | 2026-04-08 | Guerra Iran, le news dopo lâattacco di Usa Israele. La diretta - La Stampa |
| 4 | 0.09155194 | repubblica.it | 2026-03-19 | Guerra in Iran, le news del 19 marzo - la Repubblica |
| 5 | 0.09039727 | mediaset.it | 2026-04-17 | Guerra Iran, oggi in diretta: Trump: "Non ci saremo per l'Italia" |
| 6 | 0.09011648 | repubblica.it | 2026-04-17 | Guerra in Iran, le news del 17 aprile in diretta \| Tregua tra Israele e Libano - la Repubblica |
| 7 | 0.09008055 | ilgiornale.it | 2026-03-10 | Allarme degli 007 Usa: "Teheran vuole minare Hormuz". Trump: "Le rimuova o conseguenze mai viste". Italia, Germania e Inghilterra al lavoro per proteggere le navi - il Giornale |
| 8 | 0.08973047 | repubblica.it | 2026-06-15 | Guerra in Iran, le news del 15 giugno \| Accordo Usa - Iran raggiunto: riapre Hormuz - la Repubblica |
| 9 | 0.08949902 | repubblica.it | 2026-06-24 | Le news del 24 giugno. Guerra in Iran. Rutte: “500 aerei Usa sono decollati da basi in Italia" - la Repubblica |
| 10 | 0.08940057 | repubblica.it | 2026-06-17 | Guerra in Iran, le news del 17 giugno \| Venerdì la firma dell'accordo Usa - Iran - la Repubblica |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.02038912 | 0.50421278 | ilgazzettino.it | 2026-04-07 | Emergenza energetica, si studia il piano: smart working, targhe alterne. Ecco cosa può succedere |
| 2 | 0.02171661 | 0.70621753 | ilsole24ore.com | 2026-05-18 | Israele intercetta la Global Sumud Flotilla al largo di Cipro |
| 3 | 0.01988873 | 0.42880850 | ladige.it | 2026-04-13 | Meloni al Papa, possa il suo viaggio in Africa portare la pace |
| 4 | 0.02413225 | 0.51308598 | lagazzettadelmezzogiorno.it | 2026-06-25 | Meloni, presto conferenza internazionale sul Libano post Unifil - Gazzetta del Mezzogiorno |
| 5 | 0.02517444 | 0.71015852 | mediaset.it | 2026-05-17 | Meloni a von der Leyen: "La deroga al Patto di stabilità sia estesa all'energia" |

### Topic 9

- Articoli: 29165 (30.271%).
- Termini registrati: dei, le, dell, da, al, si, euro, regionale, alla, nel, regione, territorio
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | lanazione.it | 3299 | 11.312% |
| 2 | ansa.it | 2376 | 8.147% |
| 3 | ilrestodelcarlino.it | 2070 | 7.098% |
| 4 | ilgiornale.it | 1190 | 4.080% |
| 5 | iltempo.it | 1189 | 4.077% |
| 6 | ilgiorno.it | 1047 | 3.590% |
| 7 | lastampa.it | 1022 | 3.504% |
| 8 | gazzettadelsud.it | 934 | 3.202% |
| 9 | ilmattino.it | 865 | 2.966% |
| 10 | lagazzettadelmezzogiorno.it | 854 | 2.928% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 3001 |
| 2026-02 | 4238 |
| 2026-03 | 4119 |
| 2026-04 | 5031 |
| 2026-05 | 5373 |
| 2026-06 | 5395 |
| 2026-07 | 2008 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.06233348 | adnkronos.com | 2026-05-12 | Cni: "Rischio idrogeologico? Non solo fondi, da liberi professionisti 'serbatoio competenze' a cui gli enti locali dovrebbero maggiormente attingere" |
| 2 | 0.05986092 | lagazzettadelmezzogiorno.it | 2026-07-08 | Crisafi (Remind) “Costruiamo insieme l’Italia che abiteremo” - Gazzetta del Mezzogiorno |
| 3 | 0.05980193 | vocedimantova.it | 2026-07-08 | Crisafi (Remind) “Costruiamo insieme l’Italia che abiteremo” \| la Voce Di Mantova |
| 4 | 0.05974579 | italpress.com | 2026-07-08 | Crisafi (Remind) "Costruiamo insieme l'Italia che abiteremo" Agenzia di stampa Italpress - Italpress |
| 5 | 0.05971034 | iltempo.it | 2026-07-08 | Crisafi (Remind) “Costruiamo insieme l'Italia che abiteremo” – Il Tempo |
| 6 | 0.05647560 | corriereirpinia.it | 2026-05-27 | Fico incontra gli architetti campani, a confronto su housing sociale, paesaggio e qualità urbana – Corriere dell'Irpinia |
| 7 | 0.05586311 | corriereirpinia.it | 2026-05-08 | Campania, Zinzi (Lega): oltre 300 milioni ai Comuni campani per sicurezza territori e infrastrutture – Corriere dell'Irpinia |
| 8 | 0.05477586 | nove.firenze.it | 2026-05-06 | Rigenerazione del patrimonio immobiliare pubblico: patto a Firenze • Nove da Firenze |
| 9 | 0.05469533 | lasicilia.it | 2026-05-13 | Caro carburante, lavoratori Asu, B&b, dipendenti regionali: tutte le ultime norme approvate dall'Ars - La Sicilia |
| 10 | 0.05438843 | corriereirpinia.it | 2026-06-30 | Movimento 5 Stelle Avellino: Antonio Aquino eletto capogruppo per il Consiglio comunale – Corriere dell'Irpinia |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.01627895 | 0.38499979 | ansa.it | 2026-03-15 | Bimbo di 2 anni disperso in un naufragio al largo di Lampedusa - Notizie - Ansa.it |
| 2 | 0.01450434 | 0.31733820 | ansa.it | 2026-03-09 | Mattarella: 'Per le donne tanta strada da fare, manca ancora l'equilibrio' - Notizie - Ansa.it |
| 3 | 0.01766572 | 0.60723457 | giornaledibrescia.it | 2026-05-06 | Terre di storia e pietre parlanti: tesori da scoprire tra Gardone e Sarezzo \| Giornale di Brescia |
| 4 | 0.01435957 | 0.51717224 | lagazzettadelmezzogiorno.it | 2026-06-18 | Tg Lavoro & Welfare - 18/6/2026 - Gazzetta del Mezzogiorno |
| 5 | 0.02192203 | 0.49886722 | nove.firenze.it | 2026-03-02 | Ramadan a scuola: la crociata del leghista Mossuto • Nove da Firenze |

### Topic 10

- Articoli: 2726 (2.829%).
- Termini registrati: agenzia vista, agenzia, vista, jakhnagiev, alexander jakhnagiev, vista alexander, alexander, fonte agenzia, fonte, adv, meloni, vista roma
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | agi.it | 906 | 33.236% |
| 2 | ilmessaggero.it | 775 | 28.430% |
| 3 | affaritaliani.it | 410 | 15.040% |
| 4 | ilmattino.it | 379 | 13.903% |
| 5 | ilgazzettino.it | 71 | 2.605% |
| 6 | italpress.com | 58 | 2.128% |
| 7 | askanews.it | 50 | 1.834% |
| 8 | repubblica.it | 19 | 0.697% |
| 9 | laverita.info | 13 | 0.477% |
| 10 | lastampa.it | 9 | 0.330% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 145 |
| 2026-02 | 234 |
| 2026-03 | 487 |
| 2026-04 | 665 |
| 2026-05 | 472 |
| 2026-06 | 586 |
| 2026-07 | 137 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.14886824 | ilmessaggero.it | 2026-04-30 | Salvini: Sono sempre d’accordo con la Presidente del Consiglio |
| 2 | 0.14750515 | ilmessaggero.it | 2026-06-11 | Meloni esce dal Senato e saluta il direttore di Agenzia Vista Alexander Jakhnagiev a fine seduta |
| 3 | 0.14597846 | ilmessaggero.it | 2026-05-08 | Rubio arriva a Palazzo Chigi per incontrare Meloni |
| 4 | 0.13989345 | ilmessaggero.it | 2026-04-10 | Meloni in Senato: Non faremo misure demagogiche che devastano conti Stato come hanno fatto altri |
| 5 | 0.13687071 | ilmessaggero.it | 2026-03-23 | Il Ministro Tajani vota per il referendum sulla giustizia a Fiuggi |
| 6 | 0.13262252 | ilmessaggero.it | 2026-04-15 | L'abbraccio tra Meloni e Zelensky all'arrivo del Presidente ucraino a Palazzo Chigi |
| 7 | 0.13258107 | ilmessaggero.it | 2026-03-23 | Meloni, il selfie con le sostenitrici dopo aver votato |
| 8 | 0.13130043 | ilmessaggero.it | 2026-03-14 | Il dietro la tenda dell'intervista con Conte del direttore di Agenzia Vista Alexander Jakhnagiev |
| 9 | 0.13085146 | ilmessaggero.it | 2026-04-28 | Meloni: Su Patto di Stabilità non va esclusa deroga generale |
| 10 | 0.13058020 | ilmessaggero.it | 2026-05-08 | Meloni incontra il Segretario Usa Marco Rubio a Palazzo Chigi |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.06854742 | 0.77706438 | agi.it | 2026-06-03 | Via libera Ue su flessibilitÃ , Meloni: Risultato importante, pronti 14 miliardi contro caro energia |
| 2 | 0.02405523 | 0.53361452 | ilmattino.it | 2026-02-21 | Trapianto fallito al Monaldi, morto il piccolo Domenico. Meloni: «L'Italia si stringe nel dolore». Manfredi: «Grande tragedia» |
| 3 | 0.01113674 | 0.32445227 | ilmattino.it | 2026-04-09 | Meloni al Senato: Conto su di voi colleghi senatori, alla Camera solo insulti |
| 4 | 0.07873342 | 0.79759432 | ilmessaggero.it | 2026-03-11 | Crisi Iran, Meloni: Rimpatriati 25 mila italiani, completare messa in sicurezza connazionali |
| 5 | 0.08457209 | 0.93239309 | ilmessaggero.it | 2026-06-15 | Premier giapponese Takaichi: Spero che Ponte di Messina diventi simbolo cooperazione Italia-Giappone |

### Topic 11

- Articoli: 8222 (8.534%).
- Termini registrati: ansa, riproduzione riservata, riproduzione, riservata, gazzetta di, di parma, parma, ansa it, copyright ansa, riservata copyright, gazzetta, copyright
- Interpretazione semantica: **da validare da una persona**.

Domini prevalenti:

| Rank | Dominio | Articoli | % topic |
|---|---|---|---|
| 1 | ansa.it | 6134 | 74.605% |
| 2 | gazzettadiparma.it | 1011 | 12.296% |
| 3 | ladige.it | 549 | 6.677% |
| 4 | lagazzettadelmezzogiorno.it | 252 | 3.065% |
| 5 | giornaledibrescia.it | 54 | 0.657% |
| 6 | askanews.it | 35 | 0.426% |
| 7 | ilmessaggero.it | 35 | 0.426% |
| 8 | leggo.it | 31 | 0.377% |
| 9 | unionesarda.it | 21 | 0.255% |
| 10 | avvenire.it | 12 | 0.146% |

Distribuzione mensile:

| Mese | Articoli |
|---|---|
| 2026-01 | 888 |
| 2026-02 | 1161 |
| 2026-03 | 1236 |
| 2026-04 | 1525 |
| 2026-05 | 1329 |
| 2026-06 | 1626 |
| 2026-07 | 457 |

Record con peso più alto:

| Rank | Peso | Dominio | Data | Titolo |
|---|---|---|---|---|
| 1 | 0.13792581 | gazzettadiparma.it | 2026-06-17 | Tajani, 'venerdì riapre la nostra ambasciata a Teheran' - Gazzetta di Parma |
| 2 | 0.13439188 | gazzettadiparma.it | 2026-04-11 | Meloni mercoledì 15 aprile riceve Zelensky a Roma - Gazzetta di Parma |
| 3 | 0.13240159 | gazzettadiparma.it | 2026-04-28 | Meloni, entro la settimana sarà varato il Piano casa - Gazzetta di Parma |
| 4 | 0.12559356 | gazzettadiparma.it | 2026-06-30 | Conte, progetto governo progressista, chiamiamola alleanza per la Costituzione - Gazzetta di Parma |
| 5 | 0.12530832 | gazzettadiparma.it | 2026-04-08 | Tajani, 'ho dato indicazione di convocare l'ambasciatore d'Israele' - Gazzetta di Parma |
| 6 | 0.12528718 | gazzettadiparma.it | 2026-04-21 | Messaggio di Mattarella a Meloni, indignato per parole Solovyov - Gazzetta di Parma |
| 7 | 0.12516010 | gazzettadiparma.it | 2026-07-07 | Incontro tra Tajani e Rubio ad Ankara - Gazzetta di Parma |
| 8 | 0.12342814 | gazzettadiparma.it | 2026-04-28 | Meloni, mi fido del ministro Nordio - Gazzetta di Parma |
| 9 | 0.12328244 | gazzettadiparma.it | 2026-04-02 | Vertice a Palazzo Chigi sul Documento di finanza pubblica - Gazzetta di Parma |
| 10 | 0.12253568 | gazzettadiparma.it | 2026-07-09 | Meloni al lavoro a Chigi, riunione con vice e ministri sulla sicurezza - Gazzetta di Parma |

Campione deterministico, seed base 42:

| Rank | Peso | Confidenza | Dominio | Data | Titolo |
|---|---|---|---|---|---|
| 1 | 0.04745465 | 0.67247299 | ansa.it | 2026-04-24 | Meloni, '800 milioni per ristrutturare sede Consiglio Ue spesa insostenibile' - Altre news - Ansa.it |
| 2 | 0.03230410 | 0.64182759 | ansa.it | 2026-01-28 | Salini (Fi), 'difesa comune europea pilastro dell'agenda politica dell'Unione' - La voce degli Eurodeputati - Ansa.it |
| 3 | 0.02347923 | 0.49469723 | ansa.it | 2026-01-27 | Garibaldi nuovo consigliere regionale per la Lega, subentra a Piana - Notizie - Ansa.it |
| 4 | 0.02642653 | 0.62700158 | ansa.it | 2026-05-21 | In Umbria non ci sono persone in quarantena o casi sospetti per l'Hantavirus - Notizie - Ansa.it |
| 5 | 0.03168328 | 0.65883831 | ansa.it | 2026-03-28 | 'Conservatoire de la Vallée d'Aoste', approvata la norma di attuazione - Notizie - Ansa.it |

## Interpretazioni e limiti

- I conteggi precedenti sono fatti quantitativi riproducibili.
- Il report non assegna nomi definitivi né giudizi semantici ai topic.
- I quasi duplicati sono un proxy basato sul prefisso normalizzato degli estratti, non sul full-text.
- Gli estratti hanno lunghezza massima di 500 caratteri.
- I record ad alto peso possono rappresentare boilerplate molto distintivo.

## Avvisi automatici

- Il metadata sorgente contiene un percorso input assoluto; il percorso è oscurato negli output.
- Topic con dominio dominante >= 50.0%: [0, 2, 3, 4, 5, 6, 7, 11]

## Output

- [`topic_distribution.csv`](topic_distribution.csv)
- [`confidence_summary.csv`](confidence_summary.csv)
- [`domain_summary.csv`](domain_summary.csv)
- [`duplicate_summary.json`](duplicate_summary.json)
- [`run_manifest.json`](run_manifest.json)
