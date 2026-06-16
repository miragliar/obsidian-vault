---
type: workshop-prep
client: "[[Ennio_Ferrari]]"
status: active
date: 2026-06-08
location: "Ennio Ferrari Holding SA — Via Perdaglie 1, 6527 Lodrino (TI)"
lingua: it
tags: [workshop, ennio-ferrari, ticino, powerbi, powerapps, domus, preparazione]
---
# 🇮🇹 Workshop on-site Ennio Ferrari — Lodrino, lun 08.06.2026

> [!abstract] In sintesi
> Workshop vis-à-vis presso **[[Ennio_Ferrari|Ennio Ferrari Holding SA]]** a Lodrino. Tema dominante atteso: **PowerApp "Rapporto giornaliero / Cantieri"** e la sua **alimentazione dati da DOMUS**, oltre allo stato dei cockpit Power BI del gruppo. Lingua di lavoro: **italiano**.

---

## 👥 Partecipanti (da confermare sul posto)
| Persona | Ruolo | Note |
|---|---|---|
| [[Mirko Lanzi]] | **CFO** — interlocutore principale | Coordina tutto, corrispondenza in italiano. Tel. 076 201 54 62 |
| [[Matteo Ferrari]] | Famiglia / proprietà | — |
| [[Omar Rodoni]] | Controllo costi (controllo costi / pivot) | Temi: tabella controllo costi, Nr. fattura / quantità |
| [[Petar Jovic]] | Team | — |
| [[Juliana Araujo]] | Team | — |
| Gorgi Malinov | Team (presente a workshop precedenti) | — |
| HR + "Devis" | Processi ore / inventario in DOMUS | Citati da Mirko per i prossimi step dell'app |

**In remoto / esterni (eventuali):**
- **Antonio Marini** — ReqTech AG (mail `antonio.marini@celerisconsulting.com`) → **sviluppo PowerApp** Ennio Ferrari
- **Simone Bernardi** — Celeris Consulting → app / rapporto giornaliero
- [[Maurizio Tonizzo]] — Optiwork/BRZ → **fornitore ERP DOMUS** (di norma non in workshop, ma referente per le domande dati)

---

## 🎯 Obiettivo proposto del workshop
1. **Allineare** lo stato dei cockpit Power BI del gruppo (cosa è chiuso, cosa è aperto).
2. **Definire l'architettura dati per la PowerApp** "Rapporto giornaliero": come l'app riceve da DOMUS i dati anagrafici (collaboratori, cantieri, inventario) ed eventualmente **riscrive le ore** verso DOMUS.
3. **Decidere** i prossimi passi tecnici + responsabilità (io = lato dati/flussi; Marini/Celeris = app; Tonizzo = DOMUS).

---

## 🗓️ Agenda proposta (mezza/intera giornata)
> [!tip] Timeboxing indicativo — adattare sul posto
> 1. **Recap & stato** (20') — cockpit EFSA, Compul, Martello; contratto manutenzione.
> 2. **Dashboard Compul "Debitori poste aperte"** (10') — ✅ risolto, conferma chiusura + nota sul workaround.
> 3. **Domanda DOMUS aperta** (15') — link `OffenePostenDebi ↔ Dokument` (commessa/COM): stato risposta Tonizzo.
> 4. **PowerApp Cantieri ↔ DOMUS** (60') — **blocco centrale** (vedi sotto).
> 5. **Delimitazioni cantieri / errori caricamento** (20') — robustezza del processo Excel/SharePoint.
> 6. **Sicurezza & permessi** (15') — RLS per cantiere/ruolo.
> 7. **Decisioni, owner, prossimi passi** (15').

---

## 📊 Stato dei lavori (cockpit & dossier)

> [!success] Chiuso / in produzione
> - **Cockpit Compul — "Debitori poste aperte"**: bug *off-by-one* su Descrizione/COM **RISOLTO e confermato da Mirko (05.06.2026)**. Verifica su **216 poste, 0 mismatch**, 1 sola posta senza commessa (fattura **1940116/2019**, corretto = null). Vedi [[Compul]].
> - **Contratto di manutenzione Power Platform**: **firmato** (mag. 2026) → aggiornamento + formazione continua.
> - **Cockpit EFSA** (Conto Economico / Cantieri): in uso; aggiornato via dataflow + file Excel su SharePoint (`sites/Businessintelligence`).
> - **Cockpit EFSA — nuova vista "Liquidità per cantiere"** (08.06): scatter "margine × cassa" + matrix operativa → mostra su quali cantieri anticipiamo cassa (crediti aperti + lavoro non fatturato/WIP). **Da presentare al workshop.** Dettagli → [[EFSA]].
> - **Lavoro del mattino (08.06):** fix calc-item *Singolo* su `Costo totale` (saldo Delimitazione di apertura) + riconciliazione Excel ↔ DOMUS (con O. Rodoni) + consolidamento misure cumulative (`Risultato`/`Costi cantiere cumulativo`). Dettagli → [[EFSA]].
> - **Cockpit Martello Manutenzione** (Reddito progetto): attivo.

> [!warning] Aperto / in lavorazione
> - **Domanda dati DOMUS a [[Maurizio Tonizzo]]** (inviata 04.06): esiste un campo/relazione *ufficiale* che colleghi `OffenePostenDebi` al suo documento-commessa in `Dokument`, senza usare `busDokumentID` (inaffidabile)? **In attesa di risposta** — nel frattempo workaround stabile.
> - **PowerApp "Rapporto giornaliero / Cantieri"**: in sviluppo (Marini/ReqTech + Celeris). **Pilota** in partenza (vedi sotto).
> - **Delimitazioni cantieri**: errori ricorrenti di caricamento dati (vedi sezione dedicata).

---

## 🛠️ BLOCCO CENTRALE — PowerApp "Rapporto giornaliero" ↔ DOMUS

> [!info] Pilota
> **Cantiere edilizia 299-25 — "Residenza Nina", Bellinzona** · inizio ≈ metà giugno · Tecnici: **Giada Marzoli**, **Nicola Sirianni** · Capo cantiere: **Massimo Didonna**.

**Situazione (da mail Mirko 13.05 + Marini 22.05):** Marini sviluppa l'app; oggi **molti dati sono inseriti a mano** ma esistono già in DOMUS, dove **ho costruito i flussi dati**. Mirko chiede di **alimentare l'app da DOMUS** per non rifare la mappatura manuale.

### Dati anagrafici DOMUS → App (lettura)
- **Collaboratori** (ID + Nome/Cognome **univoci e allineati a DOMUS**) → serve per firma/validazione e per il futuro invio ore.
- **Numero / nome cantieri**.
- **Inventario** (mezzi/attrezzature).

### Punti da decidere (architettura)
1. **Meccanismo di sincronizzazione DOMUS → app.** L'app gira su Dataverse/Power Platform; io oggi porto DOMUS → datalake → Power BI. Opzioni da discutere:
   - riuso degli **stessi flussi** verso **tabelle Dataverse** (Power Platform dataflow), oppure
   - dataset/condivisione, oppure
   - sorgente curata dedicata per l'app.
   → **Chiarire chi possiede cosa**: io = estrazione/flussi DOMUS; Marini = consumo lato app.
2. **Gestione utenti per cantiere** ("evitare confusione tra due cantieri"): capocantiere/tecnico devono firmare **solo** il rapporto del proprio cantiere. Soluzione = **filtrare gli utenti per cantiere** → richiede anagrafica collaboratori **con assegnazione cantiere**. (Logica app = Marini; dati = io.)
3. **Invio ore App → DOMUS (write-back) — futuro.** ⚠️ Da gestire le **aspettative**: i miei flussi DOMUS sono **in sola lettura** (ODBC). La **scrittura verso DOMUS** è un'integrazione diversa → coinvolgere **Tonizzo/Optiwork** (API/interfaccia DOMUS). Non è "gratis" dentro l'app.
4. **Inventario — incrocio interessante:** in DOMUS l'assegnazione è *pianificata* via **bollettini** (es. escavatore = 5 giorni al cantiere); l'app rileva l'**utilizzo reale** (rapporto giornaliero). → **Cross-analysis in Power BI: carico pianificato vs utilizzo reale.** Buona opportunità di valore.
5. **Dati HR:** Mirko incontra HR per capire come inseriscono i dati in DOMUS e quali **controlli automatici** servono → ribadire la necessità dell'**anagrafica collaboratori da DOMUS** come master.

> [!question] Domande da porre a Marini/Mirko
> - Su quale piattaforma vive l'app e dove vuole leggere i dati (Dataverse? SharePoint? dataset?)
> - Frequenza di aggiornamento richiesta per collaboratori/cantieri/inventario?
> - Chiave univoca collaboratore concordata (ID DOMUS) — chi la espone?
> - Write-back ore: tempistiche reali e disponibilità Optiwork → serve riunione a 3 con Tonizzo?

---

## ⚠️ Delimitazioni cantieri — errori ricorrenti di caricamento
Tema ripetuto (apr. 2026, "Errore caricamento dati / Delimitazioni cantieri"). Cause emerse:
- in una delimitazione c'è solo un **"–"** invece di un **numero o 0**;
- cartelle che iniziano con **"X.2026"** → mese non identificabile.

→ **Proposta al workshop:** introdurre **validazione/regola** nel processo Excel/SharePoint (o nel Power Query) per intercettare valori non numerici e nomi cartella non conformi, così il refresh non si rompe. Mostrare a Mirko **come accedere** all'errore (già promesso: "ti faccio vedere la prossima volta come accedere").

---

## 🔐 Sicurezza & permessi
- Temi ricorrenti di **caricamento dati & autorizzazioni sui cantieri**. Valutare **Row-Level Security** in Power BI per **cantiere/ruolo** (capocantiere vede il suo cantiere), coerente con il filtro utenti dell'app.

---

## 🧷 Cheat-sheet tecnico DOMUS (per riferimento rapido)
> Dettagli completi: [[DOMUS]] · [[Compul]]

- **Connessione:** ODBC `dsn=0_DOMBWA_64` → DB **DOMBWA**, schema **PUB**. Catena: DOMUS → datalake dataflow (workspace `d9c16c71…`) → dataflow **"Domus Compul e Forestale"** (`workspaceId 61f51a96…`, `dataflowId 712a7c03…`) → modello PBI.
- **Mandanti:** **Compul = `mandantID 2`** · Forestale = `mndNr 5`. In "Compul e Forestale": `Dokument` filtrato **`mandantID = 2`**.
- **Tabelle chiave:** `OffenePostenDebi` (poste aperte deb., `opDebiReferenzReGS` = n. fattura), `Dokument` (`dokKurzBez` = "COM <nr>/<anno>"), `BuchungsJournalDetail` (ore + link DocuWare), `KontoDebitor`, `MA_` (collaboratori), `Stelle` (commessa).
- **Workaround COM (in produzione, query `Debitori poste aperte`):** ricavare il COM dal n. fattura e fare merge su `Dokument[dokKurzBez]`:
  ```
  "COM " & Text.Range([Fattura nr.],2) & "/20" & Text.Start([Fattura nr.],2)
  ```
  (es. "2640035" → "COM 40035/2026"). `busDokumentID` punta al documento sbagliato → **non usare**.
- ⚠️ Modifica applicata via **Editor avanzato**, **non** via MCP (un refresh da Desktop sovrascriverebbe la scrittura MCP).

---

## ✅ Decisioni da prendere / prossimi passi (bozza da compilare nel meeting)
- [ ] Confermare **chiusura** dashboard Compul debitori (Mirko OK 05.06).
- [ ] **Architettura dati App↔DOMUS**: scegliere meccanismo (Dataverse dataflow vs alternativa) + **owner**.
- [ ] **Anagrafica collaboratori da DOMUS** come master (ID univoco) → sblocca firma per cantiere + write-back futuro.
- [ ] **Write-back ore**: decidere se aprire tavolo con **Tonizzo/Optiwork** (interfaccia DOMUS in scrittura).
- [ ] **Inventario**: definire report PBI *pianificato (bollettini) vs reale (app)*.
- [ ] **Delimitazioni cantieri**: concordare regola di validazione + mostrare a Mirko l'accesso all'errore.
- [ ] **RLS per cantiere/ruolo** in Power BI.
- [ ] Sollecitare/registrare la **risposta DOMUS di Tonizzo** sul link OPD↔Dokument.

---

## 📞 Contatti
- **Mirko Lanzi** (CFO) — `mirko.lanzi@ennio-ferrari.ch` — 076 201 54 62 / 091 863 33 55
- **Omar Rodoni** — `omar.rodoni@ennio-ferrari.ch`
- **Matteo Ferrari** — `matteo.ferrari@ennio-ferrari.ch`
- **Antonio Marini** (app, ReqTech) — `antonio.marini@celerisconsulting.com`
- **Simone Bernardi** (app, Celeris) — `simone.bernardi@celerisconsulting.com`
- **Maurizio Tonizzo** (DOMUS/Optiwork) — `maurizio.tonizzo@optiwork.ch`
- **Sede:** Via Perdaglie 1, 6527 Lodrino (TI)

---

## 🔗 Fonti nel vault
- Hub cliente: [[Ennio_Ferrari]] · Gruppo: [[Compul]] · [[Martello_Manutenzione]]
- Persone: [[Mirko Lanzi]] · [[Omar Rodoni]] · [[Matteo Ferrari]] · [[Petar Jovic]] · [[Juliana Araujo]] · [[Maurizio Tonizzo]]
- Tecnico: [[DOMUS]]
- *Email di riferimento (Outlook):* "Errore dashboard compul" (22.05→05.06), "Estrazione dati Domus" (Marini, 22.05), "Prossimi app / Rapporto giornaliero" (13.05), "Errore caricamento dati / Delimitazioni cantieri" (apr.), "DOMUS — collegamento OffenePostenDebi ↔ Dokument" (a Tonizzo, 04.06).

> [!note] Log
> - 2026-06-08 — Nota di preparazione creata da Claudian (ricerca vault + email M365).
