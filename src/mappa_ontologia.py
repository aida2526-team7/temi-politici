"""Mappa testo italiano sui 15 macrotemi di `docs/ontologia_tematica.md` (v2.0).

Perché a lessico e non a modello. L'ontologia è stata congelata *dall'alto*, da
MARPOR, proprio perché un topic model non restituisce categorie politiche. Usare
un secondo modello non supervisionato per mappare sul primo riporterebbe lo
stesso problema un livello più su. Qui le regole sono scritte, leggibili e
discutibili una per una: è un ponte verso l'annotazione umana, non il
classificatore finale.

Limiti dichiarati:

- misura *di cosa* si parla, mai la posizione — coerente con la tassonomia, che
  accorpa le coppie pro/contro di MARPOR;
- un testo che non contiene nessuno dei termini esce `non assegnato`, non forzato
  nella categoria più vicina. La copertura è il dato di qualità da riportare;
- il lessico è tarato sull'italiano amministrativo e giornalistico corrente. Non
  è validato contro una codifica umana: la validazione è il passo dopo.
"""

from __future__ import annotations

import re
import unicodedata
from collections import Counter

# I 13 identificativi sono stabili per contratto: sono le chiavi, non le etichette.
MACROTEMI: dict[int, str] = {
    1: "Politica estera e difesa",
    2: "Unione europea",
    3: "Istituzioni e assetto dello Stato",
    4: "Economia e finanza pubblica",
    5: "Lavoro e imprese",
    6: "Welfare e pensioni",
    7: "Sanità",
    8: "Istruzione e ricerca",
    9: "Ambiente ed energia",
    10: "Immigrazione e cittadinanza",
    11: "Sicurezza e criminalità",
    12: "Diritti civili e società",
    13: "Infrastrutture e territorio",
    14: "Cultura e patrimonio",
    15: "Sport",
}

# Un livello sotto i macrotemi (ontologia v2.0, sezione *Sottotemi*). La chiave è
# `padre.figlio` e il padre resta il tema che vince: chi vuole la grana fine legge
# `sottotema()`, chi vuole le quote per macrotema non cambia niente.
SOTTOTEMI: dict[str, str] = {
    "9.1": "Animali e fauna",
}

# Categorie di servizio, fuori tassonomia (ontologia, sezione omonima).
NON_ASSEGNATO = "non assegnato"
BOILERPLATE = "boilerplate"

# Ogni voce è un pattern già in forma "senza accenti e minuscolo": il testo viene
# normalizzato allo stesso modo prima del confronto, così "sanità" e "sanita"
# pescano entrambi. I confini di parola reggono perché la normalizzazione tocca
# i diacritici, non la punteggiatura.
LESSICO: dict[int, tuple[str, ...]] = {
    1: (
        r"politic\w* est\w+", r"\bnato\b", r"alleanza atlantica", r"\bdifesa\b",
        r"militar\w*", r"forze armate", r"\bguerra\b", r"\barmi\b", r"armament\w*",
        r"ucrain\w*", r"\brussi\w*", r"israel\w*", r"\bgaza\b", r"\biran\b",
        r"missione internazional\w*", r"missioni internazional\w*", r"\besteri\b",
        r"ambasciat\w*", r"trattato internazional\w*", r"disarmo",
        r"cooperazione allo sviluppo", r"corpo diplomatico", r"\bonu\b",
        r"peacekeeping", r"geopolitic\w*",
    ),
    2: (
        r"unione europea", r"\bue\b", r"bruxelles", r"comunitari\w*",
        r"direttiv\w* europe\w*", r"regolament\w* europe\w*", r"fondi europei",
        r"parlamento europeo", r"commissione europea", r"consiglio europeo",
        r"eurozona", r"recovery fund", r"next generation eu", r"semestre europeo",
        r"patto di stabilita",
    ),
    3: (
        r"costituzional\w*", r"costituzione", r"premierato", r"autonomia differenziata",
        r"legge elettoral\w*", r"referendum", r"regolamento parlamentar\w*",
        r"enti local\w*", r"\bprovinc\w*", r"citta metropolitan\w*",
        r"pubblica amministrazione", r"magistratur\w*", r"ordinamento giudiziar\w*",
        r"\bcsm\b", r"consiglio superiore della magistratura",
        r"separazione delle carriere", r"processo civil\w*",
        r"processo amministrativ\w*", r"codice di procedura civile",
        r"\bgiudic\w*", r"\btribunal\w*", r"prefett\w*", r"decentramento",
        r"conflitto di interessi", r"\blobby\b", r"trasparenza amministrativ\w*",
        r"commissione parlamentare", r"commissione d.inchiesta", r"inchiesta parlamentare",
    ),
    4: (
        r"legge di bilancio", r"finanza pubblica", r"debito pubblic\w*", r"\bmanovra\b",
        r"tribut\w*", r"fiscal\w*", r"\bimposta\b", r"\bimposte\b", r"\biva\b",
        r"\birpef\b", r"\birap\b", r"\bimu\b", r"tassazione", r"\btasse\b",
        r"credito d.imposta", r"agevolazion\w* fiscal\w*", r"spesa pubblica",
        r"contabilita pubblica", r"\baccise\b", r"\bdogan\w*", r"evasione fiscal\w*",
        r"\bbanc\w*", r"concorrenza", r"antitrust", r"mercati finanziari",
        r"\bborsa\b", r"inflazione", r"\bpil\b", r"bilancio di previsione",
        r"bilancio pluriennale", r"\brendiconto\b", r"assestamento del bilancio",
    ),
    5: (
        r"\blavor\w*", r"occupazion\w*", r"disoccupazion\w*", r"\bsalari\w*",
        r"retribuzion\w*", r"contratt\w* collettiv\w*", r"sindacal\w*", r"sindacat\w*",
        r"\bimpres\w*", r"artigian\w*", r"piccole e medie imprese", r"\bpmi\b",
        r"industri\w*", r"cooperativ\w*", r"apprendistato", r"tirocin\w*",
        r"licenziament\w*", r"cassa integrazione", r"partita iva",
        r"lavoro autonomo", r"smart working", r"\bcommerc\w*", r"\bexport\b",
        r"internazionalizzazione delle imprese",
    ),
    6: (
        r"\bpension\w*", r"previdenz\w*", r"assistenza social\w*", r"\bpoverta\b",
        r"reddito di cittadinanza", r"assegno unico", r"sostegno al reddito",
        r"\bdisabil\w*", r"non autosufficienz\w*", r"invalidit\w*",
        r"servizi social\w*", r"terzo settore", r"volontariato",
        r"\bindigen\w*", r"esclusione social\w*", r"\banzian\w*",
        r"assegno sociale", r"inclusione social\w*",
    ),
    7: (
        r"\bsanitari\w*", r"\bsanita\b", r"\bsalute\b", r"ospedal\w*", r"\bmedic\w*",
        r"infermier\w*", r"farmac\w*", r"servizio sanitario", r"liste di attesa",
        r"liste d.attesa", r"\bmalatt\w*", r"\bcur[ae]\b", r"vaccin\w*",
        r"psichiatr\w*", r"salute mentale", r"dipendenz\w* patologic\w*",
        r"\bscreening\b", r"trapiant\w*", r"pront\w* soccorso",
        r"\bdiagnos\w*", r"\bterapi\w*", r"\bpazient\w*", r"\bobesit\w*",
    ),
    8: (
        r"\bscuol\w*", r"scolastic\w*", r"istruzione", r"\bstudent\w*", r"\bdocent\w*",
        r"insegnant\w*", r"universit\w*", r"\bricerca\b", r"\bateneo\b", r"\batenei\b",
        r"dottorat\w*", r"formazione professional\w*", r"asili nido", r"educazione",
        r"\bmaturit\w*", r"diritto allo studio", r"\bcnr\b", r"\bafam\b",
    ),
    9: (
        r"\bambient\w*", r"\benerg\w*", r"rinnovabil\w*", r"\bclima\b", r"climatic\w*",
        r"emissioni", r"inquinan\w*", r"\brifiut\w*", r"transizione ecologic\w*",
        r"risorse idric\w*", r"\bidrogeno\b", r"fotovoltaic\w*", r"\beolic\w*",
        r"idrocarbur\w*", r"\bmetano\b", r"biodiversit\w*", r"aree? protett\w*",
        r"parchi nazionali", r"dissesto idrogeologic\w*", r"economia circolare",
        r"decarbonizzazione", r"\bbonifica\b", r"\blaguna\b",
        # sottotema 9.1 — vedi SOTTOTEMI: pescano nel 9 e nel figlio insieme
        r"\banimal\w*", r"\bfauna\b", r"randag\w*", r"\bcanil\w*", r"\bveterinar\w*",
        r"venatori\w*", r"attivita venatoria", r"esercizio della caccia",
        r"benessere animal\w*", r"maltrattament\w* di animal\w*",
    ),
    10: (
        r"immigrazion\w*", r"\bimmigrat\w*", r"\bmigrant\w*", r"\bmigratori\w*",
        r"\bstranier\w*", r"\basilo\b", r"rifugiat\w*", r"\baccoglienza\b",
        r"rimpatri\w*", r"cittadinanza", r"permesso di soggiorno",
        r"protezione internazional\w*", r"profugh\w*", r"ius soli",
        r"centri di permanenza", r"\bcpr\b",
    ),
    11: (
        r"sicurezza pubblica", r"ordine pubblico", r"criminalit\w*", r"\bmafi\w*",
        r"\bcamorra\b", r".ndrangheta", r"\breat\w*", r"\bpenal\w*", r"\bcarcer\w*",
        r"detenut\w*", r"\bpolizia\b", r"carabinier\w*", r"forze dell.ordine",
        r"guardia di finanza", r"corruzion\w*", r"riciclaggio", r"stupefacent\w*",
        r"\bdroga\b", r"terrorism\w*", r"\bfurt\w*", r"\brapina\w*", r"\bomicid\w*",
        r"violenza di genere", r"femminicid\w*", r"\bstalking\b",
        r"legittima difesa", r"sicurezza urbana", r"videosorveglianza",
    ),
    12: (
        r"diritti civili", r"unioni civili", r"\bfamigli\w*", r"\bminori\b",
        r"parita di genere", r"discriminazion\w*", r"omofobi\w*", r"\blgbt\w*",
        r"fine vita", r"eutanasia", r"testamento biologico", r"\baborto\b",
        r"interruzione di gravidanza", r"adozion\w*", r"procreazione",
        r"liberta religios\w*", r"\bculto\b", r"liberta di stampa", r"\bprivacy\b",
        r"dati personal\w*", r"\bnatalit\w*", r"pari opportunit\w*",
        r"\bcognome\b", r"\bfigli\b",
    ),
    13: (
        r"infrastruttur\w*", r"\btrasport\w*", r"ferroviari\w*", r"\bferrovi\w*",
        r"autostrad\w*", r"viabilit\w*", r"\bportual\w*", r"aeroportual\w*",
        r"\bmobilit\w*", r"\bpnrr\b", r"opere pubblich\w*", r"edilizi\w*",
        r"urbanistic\w*", r"\bagricol\w*", r"agricoltura", r"\bpesca\b",
        r"zootecn\w*", r"allevament\w*", r"aree interne", r"\bmontagna\b", r"banda larga",
        r"digitalizzazione", r"telecomunicazion\w*", r"\bturism\w*",
        r"\bricostruzione\b", r"\bterremot\w*", r"\bsisma\b", r"rigenerazione urbana",
    ),
    14: (
        r"\bcultur\w*", r"beni cultural\w*", r"patrimonio cultural\w*",
        r"\bmuse[oi]\b", r"\bmuseal\w*", r"bibliotec\w*", r"\barchivi\w*",
        r"\bteatr\w*", r"\bcinema\w*", r"\bcinematografic\w*", r"\beditoria\b",
        r"spettacol\w*", r"\bmonument\w*", r"archeologic\w*", r"soprintendenz\w*",
        r"\bfestival\b", r"\bmusical\w*", r"\bartistic\w*", r"\bfumett\w*",
        r"\bpaesaggistic\w*", r"lingue minoritari\w*", r"\bdialett\w*",
    ),
    15: (
        r"\bsport\w*", r"\bolimpi\w*", r"paralimpi\w*", r"\bcalcio\b",
        r"\batlet\w*", r"impianti sportiv\w*", r"impiantistica sportiva",
        r"federazion\w* sportiv\w*", r"\bconi\b", r"dilettantistic\w*",
        r"pratica sportiva", r"\bpalestr\w*", r"\bstadi[oi]\b",
        r"associazion\w* sportiv\w*", r"\bagonistic\w*",
    ),
}

# Il lessico del sottotema è un sottoinsieme di quello del padre: serve a dire
# *quale parte* del 9 sta parlando, non a competere col 9. Chi conta per macrotema
# non lo vede.
LESSICO_SOTTOTEMI: dict[str, tuple[str, ...]] = {
    "9.1": (
        r"\banimal\w*", r"\bfauna\b", r"randag\w*", r"\bcanil\w*", r"\bveterinar\w*",
        r"venatori\w*", r"attivita venatoria", r"esercizio della caccia",
        r"benessere animal\w*", r"maltrattament\w* di animal\w*",
    ),
}

# Residui di struttura editoriale: l'ontologia li tiene fuori tassonomia perché
# altrimenti inquinano ogni conteggio. Sono i pattern che l'audit NMF ha trovato
# come topic interi (`reports/topic_audit/audit_report.md`).
LESSICO_BOILERPLATE: tuple[str, ...] = (
    r"riproduzione riservata", r"copyright ansa", r"vai all.articolo",
    r"clicca qui", r"su raiplay", r"in evidenza", r"agenzia vista",
    r"edicola digitale", r"chi siamo", r"leggi anche", r"tutti i diritti riservati",
    r"iscriviti alla newsletter", r"condividi su", r"video promo",
    r"fonte agenzia", r"redazione web",
)

# Formule fisse che pescano nel lessico sbagliato. Si tolgono dal testo prima di
# contare, non dopo: mascherarle a valle richiederebbe di sapere quale tema hanno
# gonfiato, che è esattamente ciò che si sta misurando.
#
# Le due voci non sono ipotesi: sono state trovate misurando. "dopo una lunga
# malattia" è la formula del coccodrillo e da sola faceva 176 occorrenze nel topic
# 3 del campione stampa — un topic di necrologi, che finiva in *Sanità*. "lavori
# d'aula" sono i lavori parlamentari, e mandavano in *Lavoro e imprese* il topic
# della cronaca da Montecitorio.
ESCLUSIONI: tuple[str, ...] = (
    r"(dopo una )?lunga malattia",
    r"lavori d.aula", r"lavori dell.aula", r"lavori parlamentar\w*",
    r"lavori in corso", r"lavori d.emiciclo",
    r"\blavori (?:del|dello|della|dei|degli|delle)\b",
)

_COMPILATI: dict[int, list[re.Pattern[str]]] = {
    tema: [re.compile(p) for p in pattern] for tema, pattern in LESSICO.items()
}
_COMPILATI_BOILERPLATE = [re.compile(p) for p in LESSICO_BOILERPLATE]
_COMPILATI_ESCLUSIONI = [re.compile(p) for p in ESCLUSIONI]
_COMPILATI_SOTTOTEMI: dict[str, list[re.Pattern[str]]] = {
    figlio: [re.compile(p) for p in pattern]
    for figlio, pattern in LESSICO_SOTTOTEMI.items()
}


def normalizza(testo: str) -> str:
    """Minuscole e via i diacritici, così un solo pattern copre "sanità"/"sanita"."""
    testo = unicodedata.normalize("NFD", testo.lower())
    testo = "".join(c for c in testo if unicodedata.category(c) != "Mn")
    testo = re.sub(r"\s+", " ", testo)
    for rx in _COMPILATI_ESCLUSIONI:
        testo = rx.sub(" ", testo)
    return testo


def punteggi(testo: str) -> dict[int, int]:
    """Quante occorrenze del lessico di ogni tema compaiono nel testo.

    Conta le occorrenze, non i pattern distinti: su un titolo di legge la
    differenza è nulla, su un articolo lungo distingue il tema di cui il pezzo
    parla da quello che nomina una volta di sfuggita.
    """
    norm = normalizza(testo)
    return {
        tema: sum(len(rx.findall(norm)) for rx in regex)
        for tema, regex in _COMPILATI.items()
    }


def quota_boilerplate(testo: str) -> int:
    """Occorrenze di formule editoriali residue nel testo."""
    norm = normalizza(testo)
    return sum(len(rx.findall(norm)) for rx in _COMPILATI_BOILERPLATE)


def classifica(testo: str, min_punteggio: int = 1) -> tuple[int | str, float]:
    """Il macrotema dominante e quanto domina.

    Restituisce `(tema, margine)`. `margine` è la quota del punteggio totale che
    va al vincitore: 1.0 vuol dire che il testo pesca da un lessico solo, 0.3 che
    ne tocca parecchi e la scelta è debole. Non è una probabilità.

    Sotto `min_punteggio` esce `non assegnato`: preferisco un buco dichiarato a
    un'etichetta inventata.
    """
    score = punteggi(testo)
    totale = sum(score.values())
    if totale < min_punteggio:
        return NON_ASSEGNATO, 0.0
    tema, punti = max(score.items(), key=lambda kv: (kv[1], -kv[0]))
    return tema, punti / totale


def sottotema(testo: str, tema: int | str) -> str | None:
    """Il sottotema del macrotema già assegnato, se il testo lo dichiara.

    Si chiama dopo `classifica`, mai al posto suo: un sottotema non compete col
    padre, lo qualifica. Se il macrotema non ne ha, o il testo non pesca nel suo
    lessico, restituisce `None` e il record resta sul padre.
    """
    if not isinstance(tema, int):
        return None
    norm = normalizza(testo)
    candidati = {
        figlio: sum(len(rx.findall(norm)) for rx in regex)
        for figlio, regex in _COMPILATI_SOTTOTEMI.items()
        if figlio.startswith(f"{tema}.")
    }
    vincitore = max(candidati.items(), key=lambda kv: kv[1], default=(None, 0))
    return vincitore[0] if vincitore[1] else None


def distribuzione(testi, min_punteggio: int = 1) -> Counter:
    """Conteggi per macrotema su un iterabile di testi."""
    return Counter(classifica(t, min_punteggio)[0] for t in testi)


def etichetta(tema: int | str) -> str:
    """Nome leggibile di un macrotema o sottotema; le categorie di servizio no."""
    if isinstance(tema, int):
        return MACROTEMI.get(tema, str(tema))
    return SOTTOTEMI.get(tema, str(tema))
