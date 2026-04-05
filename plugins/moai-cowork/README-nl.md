# 🗿 MoAI-Cowork

**100 zelfevoluerende instrumenten — Je persoonlijke AI-expert**

[![Version](https://img.shields.io/badge/version-0.1.0-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

🌐 [한국어](README.md) | [English](README-en.md) | [日本語](README-ja.md) | [Español](README-es.md) | [Français](README-fr.md) | [Deutsch](README-de.md) | [Português](README-pt-BR.md) | [中文](README-zh-CN.md) | [Bahasa](README-id.md) | [हिन्दी](README-hi.md) | [Tiếng Việt](README-vi.md) | [ภาษาไทย](README-th.md) | [Italiano](README-it.md) | [Nederlands](README-nl.md) | [Polski](README-pl.md) | [العربية](README-ar.md) | [עברית](README-he.md)

---

## 🎯 Wat is MoAI?

**MoAI-Cowork** is een automatisch leersysteem dat AI omzet in gespecialiseerde experts voor elk domein van je organisatie.

- **100 instrumenten**: 10 categorieën × 10 domeinen (boekhouden, recht, HR, technologie, marketing, enz.)
- **Zelfevolutie**: Self-Refine-cyclus gebaseerd op gebruikersfeedback en resultaatanalyse
- **Globaal profiel**: Gepersonaliseerde reacties via persoonlijke, team- en organisatieprofielen
- **Op plugins gebaseerd**: Naadloze integratie met Claude Code en het Cowork-ecosysteem

### Kernfuncties

| Functie | Beschrijving |
|---------|-------------|
| **Automatisch leren** | Registratie en analyse van prestaties bij elke interactie |
| **Domeinspecialisatie** | State-of-the-art praktische kennis in elk veld |
| **Culturele aanpassing** | Ondersteuning voor wereldwijde bedrijfspraktijken en talen |
| **Real-time updates** | Bevat de meest recente belastingwetten, regelgeving en marktinformatie |
| **Multi-user ondersteuning** | Profielbeheer op teamniveau en samenwerking |

---

## 📦 Installatie

### Vereisten
- Claude Code (nieuwste versie)
- Cowork plugin-ondersteuning

### Stap 1: Plugin toevoegen aan Cowork
```bash
# Installeren via Cowork CLI (binnenkort)
cowork install moai-cowork
```

### Stap 2: Profiel initialiseren
```bash
moai init
```

### Stap 3: Persoonlijk profiel configureren
```bash
moai profile --set-personal
```

---

## 🚀 Snel starten

### Voer je eerste zoekopdracht uit

```
@moai Wat is het Nederlandse btw-aangiftekalender voor 2026?
```

**Antwoord**: MoAI automatisch:
1. Laadt Nederlandse lokalisatie-informatie
2. Raadpleegt belastingwetgeving gegevens 2026
3. Geeft een gepersonaliseerde btw-kalender

### Automatisch leren inschakelen

```
moai learn --feedback "Het antwoord was zeer nauwkeurig"
```

MoAI registreert deze feedback om vergelijkbare toekomstige zoekopdrachten te verbeteren.

---

## 📚 Catalogus van 100 instrumenten

### 10 Categorieën

#### 1️⃣ Belastingen en boekhouden (Tax & Accounting)
- **NL_TAX_001**: Nederlandse btw
- **US_TAX_001**: Amerikaanse federale inkomstenbelasting
- **JP_TAX_001**: Japanse verbruiksbelasting
- **UK_TAX_001**: Britse VAT
- **VN_TAX_001**: Vietnamese VAT
- **TH_TAX_001**: Thaise VAT
- *(6 meer)*

#### 2️⃣ Arbeidsrecht en HR (Labor & HR)
- **NL_HR_001**: Nederlands arbeidsrecht
- **US_HR_001**: FLSA en minimumloon
- **JP_HR_001**: Japans arbeidsrecht
- **UK_HR_001**: Brits arbeidswetgeving
- *(6 meer)*

#### 3️⃣ Gegevens en naleving (Data & Compliance)
- **NL_DATA_001**: Gegevensbescherming (AVG)
- **US_DATA_001**: CCPA/HIPAA
- **JP_DATA_001**: Wet op de bescherming van persoonsgegevens
- **UK_DATA_001**: UK GDPR
- *(6 meer)*

#### 4️⃣ Bedrijfsvoering (Business Operations)
- **NL_BIZ_001**: Nederlandse bedrijfspraktijken
- **US_BIZ_001**: Amerikaanse vergadercultuur
- **JP_BIZ_001**: Japanse samenwerkingscultuur
- *(7 meer)*

#### 5️⃣ Technologie en IT (Technology & IT)
- **TECH_001**: Best practices voor softwareontwikkeling
- **TECH_002**: Cloud-architectuur
- *(8 meer)*

#### 6️⃣ Marketing en verkoop (Marketing & Sales)
- **MKT_001**: Digitale marketingstrategie
- **MKT_002**: B2B-verkooptechnieken
- *(8 meer)*

#### 7️⃣ Financiën en beleggingen (Finance & Investment)
- **FIN_001**: Financiële analyse
- **FIN_002**: Beleggingsportfoliobeheer
- *(8 meer)*

#### 8️⃣ Recht en contracten (Legal & Contracts)
- **LEG_001**: Contractbeoordeling
- **LEG_002**: NDA-opstelling
- *(8 meer)*

#### 9️⃣ Strategie en planning (Strategy & Planning)
- **STR_001**: Bedrijfsstrategieformulering
- **STR_002**: OKR-instellingen
- *(8 meer)*

#### 🔟 Klant en service (Customer & Service)
- **CUS_001**: Klanttevredenheidsanalyse
- **CUS_002**: Serviceverbetersingsplan
- *(8 meer)*

---

## 👤 Globaal profileersysteem

### Persoonlijk profiel (Personal Profile)
```yaml
name: "Jan Jansen"
role: "CFO"
locale: "nl_NL"
industry: "Financiën"
experience_years: 15
languages: ["Nederlands", "Engels"]
```

### Teamprofiel (Team Profile)
```yaml
team_name: "Financieel Team"
region: "Amsterdam"
size: 8
focus_areas: ["Belastingen", "Boekhouden"]
```

### Organisatieprofiel (Organization Profile)
```yaml
company_name: "ABC Corporation"
headquarters: "Amsterdam"
founded: 2010
employees: 500
industries: ["Financiën", "Technologie"]
expansion_regions: ["België", "Duitsland"]
```

---

## 🔄 Zelf-leercyclus (Self-Refine)

### Leerstroomdoorgave

```
1. Voer zoekopdracht uit
   ↓
2. Genereer antwoord (met behulp van instrumenten)
   ↓
3. Verzamel gebruikersfeedback
   ↓
4. Analyseer resultaten (nauwkeurigheid, relevantie, bruikbaarheid)
   ↓
5. Verbeter instrument (gewichten aanpassen)
   ↓
6. Toepassen op volgende zoekopdracht
```

### Soorten feedback

| Type | Beschrijving | Impact |
|------|-------------|--------|
| **Positief** | "Zeer nauwkeurig" | Instrumentgewicht +10% |
| **Gedeeltelijk** | "Gedeeltelijk correct" | Gewicht ±5% |
| **Negatief** | "Onjuist" | Instrumentgewicht -15% |
| **Aangepast** | "Meer inhoud nodig over X" | Versterking van specifiek gebied |

---

## 📖 Gebruiksvoorbeelden

### Voorbeeld 1: Belastingconsultatie
```
V: "Wat is het registratieproces voor werknemersbijdragen in Nederland?"
→ Activeer instrument NL_HR_001
→ Geef termijnen, vereiste documenten en procedure
```

### Voorbeeld 2: Internationaal bedrijf
```
V: "Waarop moet ik letten in een zakenmeeting in de VS?"
→ Activeer instrument US_BIZ_001
→ Cultuuradaptatiegids, tijdbeheer, communicatiestijl
```

### Voorbeeld 3: Regelgevingsconformiteit
```
V: "Welke procedures moet ik volgen om klantgegevens in de EU te verwerken?"
→ Activeer instrumenten NL_DATA_001 en gerelateerde GDPR
→ GDPR-conformiteit, toestemmingsbeheer, gegevensoverdrachtsprocedures
```

---

## 🛠 Hoe bij te dragen (Contributing)

### 1. Stel een nieuw instrument voor
```bash
# Stel een nieuw domein voor
moai contribute --domain "Nederlands handelsrecht" --category "legal"
```

### 2. Verbeter een bestaand instrument
```bash
# Verbetering op basis van feedback
moai improve DOMAIN_ID --feedback "Aanvullende inhoud nodig"
```

### 3. Voeg nieuwe lokalisatie toe
```bash
# Voeg nieuwe landlokalisatie toe
moai add-locale --country "België" --code "nl_BE"
```

### 4. Verbeter documentatie
- Bewerk lokalisatiebestanden in `/skills/moai/references/locale/`
- Dien Pull Request in op GitHub
- Update cultuuradaptatierichtlijnen

---

## 📋 Routekaart

### Fase 1 (Actueel)
- [x] Basissysteem van instrumenten
- [x] Globale lokalisatierichtlijnen (7 landen)
- [ ] Self-Refine cyclus implementatie

### Fase 2 (2026 Q2)
- [ ] 100 instrumenten voltooid
- [ ] Meertalige interface (12 talen)
- [ ] Samenwerkingsfuncties van het team

### Fase 3 (2026 Q3)
- [ ] Updates van regelgeving in real-time
- [ ] AI-to-Human beoordelingsproces
- [ ] Branchespecifieke sjablonen

---

## 📞 Ondersteuning en contact

- **Documentatie**: `/skills/moai/references/locale/`
- **GitHub**: (binnenkort)
- **Email**: support@moai-cowork.dev

---

## 📄 Licentie

MIT-licentie - Vrij te gebruiken, aan te passen en te distribueren

---

## 🙏 Dankbetuigingen

MoAI-Cowork evolueert voortdurend met feedback van de Claude- en Cowork-gemeenschap.

---

**MoAI-Cowork: Ontmoet je persoonlijke AI-expert.**

*Laatst bijgewerkt: 2026-04-04*
