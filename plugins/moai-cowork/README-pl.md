# 🗿 MoAI-Cowork

**100 narzędzi samowzrostu — Twój spersonalizowany ekspert AI**

[![Version](https://img.shields.io/badge/version-0.1.0-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

🌐 [한국어](README.md) | [English](README-en.md) | [日本語](README-ja.md) | [Español](README-es.md) | [Français](README-fr.md) | [Deutsch](README-de.md) | [Português](README-pt-BR.md) | [中文](README-zh-CN.md) | [Bahasa](README-id.md) | [हिन्दी](README-hi.md) | [Tiếng Việt](README-vi.md) | [ภาษาไทย](README-th.md) | [Italiano](README-it.md) | [Nederlands](README-nl.md) | [Polski](README-pl.md) | [العربية](README-ar.md) | [עברית](README-he.md)

---

## 🎯 Czym jest MoAI?

**MoAI-Cowork** to system automatycznego uczenia się, który przekształca AI w wyspecjalizowanych ekspertów dla każdej dziedziny Twojej organizacji.

- **100 narzędzi**: 10 kategorii × 10 dziedzin (księgowość, prawo, HR, technologia, marketing, itp.)
- **Samowzrost**: Cykl Self-Refine oparty na opinii użytkownika i analizie wyników
- **Profil globalny**: Spersonalizowane odpowiedzi poprzez profile indywidualne, zespołowe i organizacyjne
- **Oparte na pluginach**: Bezproblemowa integracja z Claude Code i ekosystemem Cowork

### Główne cechy

| Funkcja | Opis |
|---------|------|
| **Automatyczne uczenie się** | Rejestracja i analiza wydajności przy każdej interakcji |
| **Specjalizacja w dziedzinie** | Najnowocześniejsza praktyczna wiedza w każdej dziedzinie |
| **Adaptacja kulturowa** | Wsparcie dla globalnych praktyk biznesowych i języków |
| **Aktualizacje w czasie rzeczywistym** | Zawiera najnowsze prawa podatkowe, przepisy i informacje rynkowe |
| **Obsługa wielu użytkowników** | Zarządzanie profilami na poziomie zespołu i współpraca |

---

## 📦 Instalacja

### Wymagania
- Claude Code (najnowsza wersja)
- Obsługa wtyczek Cowork

### Krok 1: Dodaj wtyczkę do Cowork
```bash
# Instalacja przez Cowork CLI (już niedługo)
cowork install moai-cowork
```

### Krok 2: Zainicjuj profil
```bash
moai init
```

### Krok 3: Skonfiguruj profil osobisty
```bash
moai profile --set-personal
```

---

## 🚀 Szybki start

### Uruchom swoje pierwsze zapytanie

```
@moai Jaki jest polski harmonogram deklaracji VAT na 2026 rok?
```

**Odpowiedź**: MoAI automatycznie:
1. Ładuje informacje o polskiej lokalizacji
2. Konsultuje dane ustawodawstwa podatkowego 2026
3. Udostępnia spersonalizowany harmonogram VAT

### Włącz automatyczne uczenie się

```
moai learn --feedback "Odpowiedź była bardzo dokładna"
```

MoAI rejestruje tę opinię, aby ulepszyć podobne przyszłe zapytania.

---

## 📚 Katalog 100 narzędzi

### 10 Kategorii

#### 1️⃣ Podatki i księgowość (Tax & Accounting)
- **PL_TAX_001**: Polski VAT
- **US_TAX_001**: Amerykański podatek dochodowy od osób prawnych
- **JP_TAX_001**: Japoński podatek konsumpcyjny
- **UK_TAX_001**: Brytyjski VAT
- **VN_TAX_001**: Wietnamski VAT
- **TH_TAX_001**: Tajski VAT
- *(6 więcej)*

#### 2️⃣ Prawo pracy i HR (Labor & HR)
- **PL_HR_001**: Polskie prawo pracy
- **US_HR_001**: FLSA i płaca minimalna
- **JP_HR_001**: Japońskie prawo pracy
- **UK_HR_001**: Brytyjskie prawo zatrudnienia
- *(6 więcej)*

#### 3️⃣ Dane i zgodność (Data & Compliance)
- **PL_DATA_001**: Ochrona danych osobowych (RODO)
- **US_DATA_001**: CCPA/HIPAA
- **JP_DATA_001**: Ustawa o ochronie danych osobowych
- **UK_DATA_001**: UK GDPR
- *(6 więcej)*

#### 4️⃣ Operacje biznesowe (Business Operations)
- **PL_BIZ_001**: Polskie praktyki biznesowe
- **US_BIZ_001**: Amerykańska kultura spotkań
- **JP_BIZ_001**: Japońska kultura współpracy
- *(7 więcej)*

#### 5️⃣ Technologia i IT (Technology & IT)
- **TECH_001**: Najlepsze praktyki tworzenia oprogramowania
- **TECH_002**: Architektura chmury
- *(8 więcej)*

#### 6️⃣ Marketing i sprzedaż (Marketing & Sales)
- **MKT_001**: Strategia marketingu cyfrowego
- **MKT_002**: Techniki sprzedaży B2B
- *(8 więcej)*

#### 7️⃣ Finanse i inwestycje (Finance & Investment)
- **FIN_001**: Analiza sprawozdań finansowych
- **FIN_002**: Zarządzanie portfelem inwestycyjnym
- *(8 więcej)*

#### 8️⃣ Prawo i umowy (Legal & Contracts)
- **LEG_001**: Przegląd umów
- **LEG_002**: Redakcja NDA
- *(8 więcej)*

#### 9️⃣ Strategia i planowanie (Strategy & Planning)
- **STR_001**: Opracowanie strategii biznesowej
- **STR_002**: Ustawienie OKR
- *(8 więcej)*

#### 🔟 Klient i obsługa (Customer & Service)
- **CUS_001**: Analiza zadowolenia klienta
- **CUS_002**: Plan doskonalenia obsługi
- *(8 więcej)*

---

## 👤 Globalny system profilów

### Profil osobisty (Personal Profile)
```yaml
name: "Jan Kowalski"
role: "CFO"
locale: "pl_PL"
industry: "Finanse"
experience_years: 15
languages: ["Polski", "Angielski"]
```

### Profil zespołu (Team Profile)
```yaml
team_name: "Zespół Finansów"
region: "Warszawa"
size: 8
focus_areas: ["Podatki", "Księgowość"]
```

### Profil organizacji (Organization Profile)
```yaml
company_name: "ABC Corporation"
headquarters: "Warszawa"
founded: 2010
employees: 500
industries: ["Finanse", "Technologia"]
expansion_regions: ["Niemcy", "Czechy"]
```

---

## 🔄 Cykl samouczenia się (Self-Refine)

### Przepływ uczenia

```
1. Wykonaj zapytanie
   ↓
2. Wygeneruj odpowiedź (używając narzędzi)
   ↓
3. Zbierz opinię użytkownika
   ↓
4. Przeanalizuj wyniki (dokładność, trafność, przydatność)
   ↓
5. Ulepszaj narzędzie (dostosuj wagi)
   ↓
6. Zastosuj do następnego zapytania
```

### Rodzaje opinii

| Typ | Opis | Wpływ |
|-----|------|-------|
| **Pozytywna** | "Bardzo dokładne" | Waga narzędzia +10% |
| **Częściowa** | "Częściowo poprawne" | Waga ±5% |
| **Negatywna** | "Błędne" | Waga narzędzia -15% |
| **Niestandardowa** | "Potrzeba więcej zawartości na temat X" | Wzmocnienie konkretnego obszaru |

---

## 📖 Przykłady użycia

### Przykład 1: Konsultacja podatkowa
```
P: "Jaki jest proces rejestracji ubezpieczenia społecznego dla nowych pracowników w Polsce?"
→ Aktywuj narzędzie PL_HR_001
→ Podaj terminy, wymagane dokumenty i procedurę
```

### Przykład 2: Biznes międzynarodowy
```
P: "Na co powinienem zwrócić uwagę na spotkaniu biznesowym w Stanach Zjednoczonych?"
→ Aktywuj narzędzie US_BIZ_001
→ Przewodnik adaptacji kulturowej, zarządzanie czasem, styl komunikacji
```

### Przykład 3: Zgodność z przepisami
```
P: "Jakie procedury muszę postępować, aby przetwarzać dane klientów w UE?"
→ Aktywuj narzędzia PL_DATA_001 i powiązane RODO
→ Zgodność RODO, zarządzanie zgodą, procedury transferu danych
```

---

## 🛠 Jak wnieść wkład (Contributing)

### 1. Zaproponuj nowe narzędzie
```bash
# Zaproponuj nową dziedzinę
moai contribute --domain "Polskie prawo handlowe" --category "legal"
```

### 2. Ulepszaj istniejące narzędzie
```bash
# Ulepszenie na podstawie opinii
moai improve DOMAIN_ID --feedback "Potrzebna dodatkowa zawartość"
```

### 3. Dodaj nową lokalizację
```bash
# Dodaj nową lokalizację kraju
moai add-locale --country "Ukraina" --code "uk_UA"
```

### 4. Ulepszaj dokumentację
- Edytuj pliki lokalizacji w `/skills/moai/references/locale/`
- Przesyłaj Pull Request na GitHub
- Aktualizuj przewodniki adaptacji kulturowej

---

## 📋 Mapa drogowa

### Faza 1 (Bieżąca)
- [x] Podstawowy system narzędzi
- [x] Globalne przewodniki lokalizacji (7 krajów)
- [ ] Implementacja cyklu Self-Refine

### Faza 2 (2026 Q2)
- [ ] 100 narzędzi ukończonych
- [ ] Interfejs wielojęzyczny (12 języków)
- [ ] Funkcje współpracy zespołowej

### Faza 3 (2026 Q3)
- [ ] Aktualizacje przepisów w czasie rzeczywistym
- [ ] Proces przeglądu AI-to-Human
- [ ] Szablony branżowe

---

## 📞 Wsparcie i kontakt

- **Dokumentacja**: `/skills/moai/references/locale/`
- **GitHub**: (już niedługo)
- **Email**: support@moai-cowork.dev

---

## 📄 Licencja

Licencja MIT - Wolna do użytku, modyfikacji i dystrybucji

---

## 🙏 Podziękowania

MoAI-Cowork stale się rozwija dzięki informacji zwrotnej od społeczności Claude i Cowork.

---

**MoAI-Cowork: Poznaj swojego spersonalizowanego eksperta AI.**

*Ostatnia aktualizacja: 2026-04-04*
