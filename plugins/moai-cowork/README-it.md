# 🗿 MoAI-Cowork

**100 strumenti di auto-evoluzione — Il tuo esperto IA personalizzato**

[![Version](https://img.shields.io/badge/version-0.1.0-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

🌐 [한국어](README.md) | [English](README-en.md) | [日本語](README-ja.md) | [Español](README-es.md) | [Français](README-fr.md) | [Deutsch](README-de.md) | [Português](README-pt-BR.md) | [中文](README-zh-CN.md) | [Bahasa](README-id.md) | [हिन्दी](README-hi.md) | [Tiếng Việt](README-vi.md) | [ภาษาไทย](README-th.md) | [Italiano](README-it.md) | [Nederlands](README-nl.md) | [Polski](README-pl.md) | [العربية](README-ar.md) | [עברית](README-he.md)

---

## 🎯 Cos'è MoAI?

**MoAI-Cowork** è un sistema di apprendimento automatico che trasforma l'IA in esperti specializzati per ogni dominio della tua organizzazione.

- **100 strumenti**: 10 categorie × 10 domini (contabilità, legale, HR, tecnologia, marketing, ecc.)
- **Auto-evoluzione**: Ciclo Self-Refine basato sul feedback dell'utente e sull'analisi dei risultati
- **Profilo globale**: Risposte personalizzate attraverso profili individuali, di team e organizzativi
- **Basato su plugin**: Integrazione perfetta con Claude Code e l'ecosistema Cowork

### Caratteristiche principali

| Funzione | Descrizione |
|----------|-------------|
| **Apprendimento automatico** | Registrazione e analisi delle prestazioni ad ogni interazione |
| **Specializzazione per dominio** | Conoscenze pratiche all'avanguardia in ogni campo |
| **Adattamento culturale** | Supporto per pratiche commerciali globali e lingue |
| **Aggiornamenti in tempo reale** | Include leggi fiscali, normative e informazioni di mercato più recenti |
| **Supporto multi-utente** | Gestione dei profili a livello di team e collaborazione |

---

## 📦 Installazione

### Requisiti
- Claude Code (versione più recente)
- Supporto plugin Cowork

### Passaggio 1: Aggiungere il plugin a Cowork
```bash
# Installa tramite Cowork CLI (a breve)
cowork install moai-cowork
```

### Passaggio 2: Inizializzare il profilo
```bash
moai init
```

### Passaggio 3: Configurare il profilo personale
```bash
moai profile --set-personal
```

---

## 🚀 Avvio rapido

### Eseguire la tua prima query

```
@moai Qual è il calendario di dichiarazione IVA italiana per il 2026?
```

**Risposta**: MoAI automaticamente:
1. Carica le informazioni di localizzazione italiana
2. Consulta i dati normativo fiscali 2026
3. Fornisce un calendario IVA personalizzato

### Attivare l'apprendimento automatico

```
moai learn --feedback "La risposta era molto accurata"
```

MoAI registra questo feedback per migliorare le query simili in futuro.

---

## 📚 Catalogo di 100 strumenti

### 10 Categorie

#### 1️⃣ Tasse e contabilità (Tax & Accounting)
- **IT_TAX_001**: IVA italiana
- **US_TAX_001**: Imposta federale sul reddito USA
- **JP_TAX_001**: Imposta sui consumi giapponese
- **UK_TAX_001**: IVA del Regno Unito
- **VN_TAX_001**: IVA vietnamita
- **TH_TAX_001**: IVA tailandese
- *(6 altri)*

#### 2️⃣ Diritto del lavoro e HR (Labor & HR)
- **IT_HR_001**: Diritto del lavoro italiano
- **US_HR_001**: FLSA e salario minimo
- **JP_HR_001**: Diritto del lavoro giapponese
- **UK_HR_001**: Diritto dell'occupazione britannico
- *(6 altri)*

#### 3️⃣ Dati e conformità (Data & Compliance)
- **IT_DATA_001**: Protezione dei dati (GDPR)
- **US_DATA_001**: CCPA/HIPAA
- **JP_DATA_001**: Legge sulla protezione dei dati personali
- **UK_DATA_001**: UK GDPR
- *(6 altri)*

#### 4️⃣ Operazioni commerciali (Business Operations)
- **IT_BIZ_001**: Pratiche commerciali italiane
- **US_BIZ_001**: Cultura delle riunioni americana
- **JP_BIZ_001**: Cultura della collaborazione giapponese
- *(7 altri)*

#### 5️⃣ Tecnologia e IT (Technology & IT)
- **TECH_001**: Best practice dello sviluppo software
- **TECH_002**: Architettura cloud
- *(8 altri)*

#### 6️⃣ Marketing e vendite (Marketing & Sales)
- **MKT_001**: Strategia di marketing digitale
- **MKT_002**: Tecniche di vendita B2B
- *(8 altri)*

#### 7️⃣ Finanze e investimenti (Finance & Investment)
- **FIN_001**: Analisi di bilancio
- **FIN_002**: Gestione del portafoglio di investimento
- *(8 altri)*

#### 8️⃣ Legge e contratti (Legal & Contracts)
- **LEG_001**: Revisione contrattuale
- **LEG_002**: Redazione NDA
- *(8 altri)*

#### 9️⃣ Strategia e pianificazione (Strategy & Planning)
- **STR_001**: Sviluppo della strategia aziendale
- **STR_002**: Impostazione OKR
- *(8 altri)*

#### 🔟 Cliente e servizio (Customer & Service)
- **CUS_001**: Analisi della soddisfazione dei clienti
- **CUS_002**: Piano di miglioramento dei servizi
- *(8 altri)*

---

## 👤 Sistema di profilo globale

### Profilo personale (Personal Profile)
```yaml
name: "Marco Rossi"
role: "CFO"
locale: "it_IT"
industry: "Finanza"
experience_years: 15
languages: ["Italiano", "Inglese"]
```

### Profilo del team (Team Profile)
```yaml
team_name: "Team Finanza"
region: "Milano"
size: 8
focus_areas: ["Tasse", "Contabilità"]
```

### Profilo organizzativo (Organization Profile)
```yaml
company_name: "ABC Corporation"
headquarters: "Milano"
founded: 2010
employees: 500
industries: ["Finanza", "Tecnologia"]
expansion_regions: ["Francia", "Germania"]
```

---

## 🔄 Ciclo di auto-apprendimento (Self-Refine)

### Flusso di apprendimento

```
1. Esegui la query
   ↓
2. Genera la risposta (usando gli strumenti)
   ↓
3. Raccogli il feedback dell'utente
   ↓
4. Analizza i risultati (accuratezza, pertinenza, utilità)
   ↓
5. Migliora lo strumento (regola i pesi)
   ↓
6. Applica alla prossima query
```

### Tipi di feedback

| Tipo | Descrizione | Impatto |
|------|-------------|---------|
| **Positivo** | "Molto accurato" | Peso dello strumento +10% |
| **Parziale** | "Parzialmente corretto" | Peso ±5% |
| **Negativo** | "Errato" | Peso dello strumento -15% |
| **Personalizzato** | "Hai bisogno di più contenuto su X" | Rafforzamento di area specifica |

---

## 📖 Esempi di utilizzo

### Esempio 1: Consulenza fiscale
```
D: "Qual è il processo di registrazione dei contributi per i nuovi dipendenti in Italia?"
→ Attiva lo strumento IT_HR_001
→ Fornisce scadenze, documenti richiesti e procedura
```

### Esempio 2: Affari internazionali
```
D: "Su cosa dovrei stare attento in una riunione di affari negli USA?"
→ Attiva lo strumento US_BIZ_001
→ Guida all'adattamento culturale, gestione del tempo, stile di comunicazione
```

### Esempio 3: Conformità normativa
```
D: "Quali procedure devo seguire per elaborare i dati dei clienti nell'UE?"
→ Attiva gli strumenti IT_DATA_001 e GDPR correlato
→ Conformità GDPR, gestione del consenso, procedure di trasferimento dati
```

---

## 🛠 Come contribuire (Contributing)

### 1. Proponi un nuovo strumento
```bash
# Proponi un nuovo dominio
moai contribute --domain "Diritto commerciale italiano" --category "legal"
```

### 2. Migliora uno strumento esistente
```bash
# Miglioramento basato sul feedback
moai improve DOMAIN_ID --feedback "Contenuto aggiuntivo necessario"
```

### 3. Aggiungi una nuova localizzazione
```bash
# Aggiungi una nuova localizzazione di paese
moai add-locale --country "Svizzera" --code "it_CH"
```

### 4. Migliora la documentazione
- Modifica i file di localizzazione in `/skills/moai/references/locale/`
- Invia una Pull Request su GitHub
- Aggiorna le guide di adattamento culturale

---

## 📋 Roadmap

### Fase 1 (Attuale)
- [x] Sistema di strumenti di base
- [x] Guide di localizzazione globale (7 paesi)
- [ ] Implementazione del ciclo Self-Refine

### Fase 2 (2026 Q2)
- [ ] 100 strumenti completati
- [ ] Interfaccia multilingue (12 lingue)
- [ ] Funzioni di collaborazione del team

### Fase 3 (2026 Q3)
- [ ] Aggiornamenti normativi in tempo reale
- [ ] Processo di revisione AI-to-Human
- [ ] Modelli specifici per il settore

---

## 📞 Supporto e contatti

- **Documentazione**: `/skills/moai/references/locale/`
- **GitHub**: (a breve)
- **Email**: support@moai-cowork.dev

---

## 📄 Licenza

Licenza MIT - Libera da usare, modificare e distribuire

---

## 🙏 Ringraziamenti

MoAI-Cowork continua a evolversi con il feedback della comunità Claude e Cowork.

---

**MoAI-Cowork: Incontra il tuo esperto IA personalizzato.**

*Ultimo aggiornamento: 2026-04-04*
