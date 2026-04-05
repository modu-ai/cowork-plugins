# 🗿 MoAI-Cowork

**100 selbstentwickelnde Instrumente — Dein personalisierter KI-Experte**

[![Version](https://img.shields.io/badge/version-0.1.0-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

🌐 [한국어](README.md) | [English](README-en.md) | [日本語](README-ja.md) | [Español](README-es.md) | [Français](README-fr.md) | [Deutsch](README-de.md) | [Português](README-pt-BR.md) | [中文](README-zh-CN.md) | [Bahasa](README-id.md) | [हिन्दी](README-hi.md) | [Tiếng Việt](README-vi.md) | [ภาษาไทย](README-th.md) | [Italiano](README-it.md) | [Nederlands](README-nl.md) | [Polski](README-pl.md) | [العربية](README-ar.md) | [עברית](README-he.md)

---

## 🎯 Was ist MoAI?

**MoAI-Cowork** ist ein automatisches Lernsystem, das KI in spezialisierte Experten für jeden Bereich deiner Organisation verwandelt.

- **100 Instrumente**: 10 Kategorien × 10 Domänen (Buchhaltung, Recht, Personalwesen, Technologie, Marketing, etc.)
- **Selbstentwicklung**: Self-Refine-Zyklus basierend auf Nutzerfeedback und Ergebnisanalyse
- **Globales Profil**: Personalisierte Antworten durch individuelle, Team- und Organisationsprofile
- **Plugin-basiert**: Nahtlose Integration mit Claude Code und dem Cowork-Ökosystem

### Kernfunktionen

| Funktion | Beschreibung |
|----------|-------------|
| **Automatisches Lernen** | Leistungserfassung und -analyse bei jeder Interaktion |
| **Domänenspezialisierung** | State-of-the-Art praktisches Wissen in jedem Bereich |
| **Kulturelle Anpassung** | Unterstützung globaler Geschäftspraktiken und Sprachen |
| **Echtzeit-Updates** | Neueste Steuergesetze, Vorschriften und Marktinformationen |
| **Multi-User-Unterstützung** | Profilmanagement auf Team-Ebene und Zusammenarbeit |

---

## 📦 Installation

### Anforderungen
- Claude Code (neueste Version)
- Cowork Plugin-Unterstützung

### Schritt 1: Plugin zu Cowork hinzufügen
```bash
# Installation über Cowork CLI (in Kürze)
cowork install moai-cowork
```

### Schritt 2: Profil initialisieren
```bash
moai init
```

### Schritt 3: Persönliches Profil konfigurieren
```bash
moai profile --set-personal
```

---

## 🚀 Schnellstart

### Deine erste Abfrage ausführen

```
@moai Wie sind die Fristen für die Umsatzsteuererklärung in Deutschland 2026?
```

**Antwort**: MoAI automatisch:
1. Lädt Standortinformationen für Deutschland
2. Konsultiert Steuergesetzdaten 2026
3. Bietet einen personalisierten Umsatzsteuer-Kalender

### Automatisches Lernen aktivieren

```
moai learn --feedback "Die Antwort war sehr genau"
```

MoAI speichert dieses Feedback, um ähnliche zukünftige Abfragen zu verbessern.

---

## 📚 Katalog der 100 Instrumente

### 10 Kategorien

#### 1️⃣ Steuern und Buchhaltung (Tax & Accounting)
- **DE_TAX_001**: Deutsche Umsatzsteuer
- **US_TAX_001**: US-Einkommensteuer
- **JP_TAX_001**: Japanische Verbrauchsteuer
- **UK_TAX_001**: UK VAT
- **VN_TAX_001**: Vietnamesische Umsatzsteuer
- **TH_TAX_001**: Thailändische Umsatzsteuer
- *(6 weitere)*

#### 2️⃣ Arbeitsrecht und Personalwesen (Labor & HR)
- **DE_HR_001**: Deutsches Arbeitsrecht
- **US_HR_001**: FLSA und Mindestlohn
- **JP_HR_001**: Japanisches Arbeitsrecht
- **UK_HR_001**: Britisches Arbeitsrecht
- *(6 weitere)*

#### 3️⃣ Datenschutz und Compliance (Data & Compliance)
- **DE_DATA_001**: Datenschutz (DSGVO)
- **US_DATA_001**: CCPA/HIPAA
- **JP_DATA_001**: Gesetz zum Schutz persönlicher Daten
- **UK_DATA_001**: UK GDPR
- *(6 weitere)*

#### 4️⃣ Geschäftsabläufe (Business Operations)
- **DE_BIZ_001**: Deutsche Geschäftspraktiken
- **US_BIZ_001**: US-Besprechungskultur
- **JP_BIZ_001**: Japanische Kooperationskultur
- *(7 weitere)*

#### 5️⃣ Technologie und IT (Technology & IT)
- **TECH_001**: Best Practices in der Softwareentwicklung
- **TECH_002**: Cloud-Architektur
- *(8 weitere)*

#### 6️⃣ Marketing und Vertrieb (Marketing & Sales)
- **MKT_001**: Digitale Marketingstrategie
- **MKT_002**: B2B-Vertriebstechniken
- *(8 weitere)*

#### 7️⃣ Finanzen und Investitionen (Finance & Investment)
- **FIN_001**: Finanzanalyse
- **FIN_002**: Investitionsportfoliomanagement
- *(8 weitere)*

#### 8️⃣ Recht und Verträge (Legal & Contracts)
- **LEG_001**: Vertragsreview
- **LEG_002**: NDA-Erstellung
- *(8 weitere)*

#### 9️⃣ Strategie und Planung (Strategy & Planning)
- **STR_001**: Geschäftsstrategie entwickeln
- **STR_002**: OKR-Einstellung
- *(8 weitere)*

#### 🔟 Kundenbeziehungen und Service (Customer & Service)
- **CUS_001**: Kundenzufriedenheitsanalyse
- **CUS_002**: Serviceverbesserungsplan
- *(8 weitere)*

---

## 👤 Globales Profilsystem

### Persönliches Profil (Personal Profile)
```yaml
name: "Hans Müller"
role: "CFO"
locale: "de_DE"
industry: "Finanzen"
experience_years: 15
languages: ["Deutsch", "Englisch"]
```

### Teamprofil (Team Profile)
```yaml
team_name: "Finanzteam"
region: "Berlin"
size: 8
focus_areas: ["Steuern", "Buchhaltung"]
```

### Organisationsprofil (Organization Profile)
```yaml
company_name: "ABC Corporation"
headquarters: "Berlin"
founded: 2010
employees: 500
industries: ["Finanzen", "Technologie"]
expansion_regions: ["Schweiz", "Österreich"]
```

---

## 🔄 Selbstlern-Zyklus (Self-Refine)

### Lernfluss

```
1. Abfrage ausführen
   ↓
2. Antwort generieren (unter Verwendung von Instrumenten)
   ↓
3. Nutzerfeedback sammeln
   ↓
4. Ergebnisse analysieren (Genauigkeit, Relevanz, Nützlichkeit)
   ↓
5. Instrument verbessern (Gewichte anpassen)
   ↓
6. Auf nächste Abfrage anwenden
```

### Feedback-Typen

| Typ | Beschreibung | Auswirkung |
|-----|-------------|-----------|
| **Positiv** | "Sehr genau" | Instrument-Gewicht +10% |
| **Teilweise** | "Teilweise korrekt" | Gewicht ±5% |
| **Negativ** | "Falsch" | Instrument-Gewicht -15% |
| **Benutzerdefiniert** | "Benötigt mehr Inhalte zu X" | Spezifische Bereichsverstärkung |

---

## 📖 Verwendungsbeispiele

### Beispiel 1: Steuerberatung
```
Q: "Wie ist der Registrierungsprozess für neue Mitarbeiter in Deutschland?"
→ Aktiviert Instrument DE_HR_001
→ Liefert Fristen, erforderliche Unterlagen und Verfahren
```

### Beispiel 2: Internationales Geschäft
```
Q: "Worauf sollte ich in einem US-Geschäftstreffen achten?"
→ Aktiviert Instrument US_BIZ_001
→ Kulturelles Anpassungsleitfaden, Zeitmanagement, Kommunikationsstil
```

### Beispiel 3: Regelkonformität
```
Q: "Welche Verfahren muss ich für die Verarbeitung von Kundendaten in der EU befolgen?"
→ Aktiviert Instrumente DE_DATA_001 und zugehörige GDPR
→ DSGVO-Konformität, Einwiltigungsverwaltung, Übergabeverfahren
```

---

## 🛠 Wie man beiträgt (Contributing)

### 1. Ein neues Instrument vorschlagen
```bash
# Neuen Bereich vorschlagen
moai contribute --domain "Deutsches Handelsrecht" --category "legal"
```

### 2. Ein bestehendes Instrument verbessern
```bash
# Feedback-basierte Verbesserung
moai improve DOMAIN_ID --feedback "Zusätzliche Inhalte erforderlich"
```

### 3. Neue Lokalisierung hinzufügen
```bash
# Neue Länderlokal hinzufügen
moai add-locale --country "Schweiz" --code "de_CH"
```

### 4. Dokumentation verbessern
- Bearbeite Lokalisierungsdateien in `/skills/moai/references/locale/`
- Übermittle einen Pull Request auf GitHub
- Aktualisiere kulturelle Anpassungsleitfäden

---

## 📋 Roadmap

### Phase 1 (Aktuell)
- [x] Basis-Instrumentensystem
- [x] Globale Lokalisierungsleitfäden (7 Länder)
- [ ] Self-Refine-Zyklus-Implementierung

### Phase 2 (2026 Q2)
- [ ] 100 Instrumente abgeschlossen
- [ ] Mehrsprachige Benutzeroberfläche (12 Sprachen)
- [ ] Team-Kollaborationsfunktionen

### Phase 3 (2026 Q3)
- [ ] Echtzeit-Regulierungsaktualisierungen
- [ ] KI-zu-Mensch-Überprüfungsprozess
- [ ] Branchenspezifische Vorlagen

---

## 📞 Support und Kontakt

- **Dokumentation**: `/skills/moai/references/locale/`
- **GitHub**: (in Kürze)
- **Email**: support@moai-cowork.dev

---

## 📄 Lizenz

MIT-Lizenz - Frei zu verwenden, zu ändern und zu verteilen

---

## 🙏 Danksagungen

MoAI-Cowork entwickelt sich kontinuierlich weiter durch Feedback der Claude- und Cowork-Gemeinschaft.

---

**MoAI-Cowork: Triff deinen personalisierten KI-Experten.**

*Zuletzt aktualisiert: 2026-04-04*
