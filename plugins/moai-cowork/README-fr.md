# 🗿 MoAI-Cowork

**100 harnais d'auto-évolution — Votre expert IA personnalisé**

[![Version](https://img.shields.io/badge/version-0.1.0-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

🌐 [한국어](README.md) | [English](README-en.md) | [日本語](README-ja.md) | [Español](README-es.md) | [Français](README-fr.md) | [Deutsch](README-de.md) | [Português](README-pt-BR.md) | [中文](README-zh-CN.md) | [Bahasa](README-id.md) | [हिन्दी](README-hi.md) | [Tiếng Việt](README-vi.md) | [ภาษาไทย](README-th.md) | [Italiano](README-it.md) | [Nederlands](README-nl.md) | [Polski](README-pl.md) | [العربية](README-ar.md) | [עברית](README-he.md)

---

## 🎯 Qu'est-ce que MoAI ?

**MoAI-Cowork** est un système d'apprentissage automatique qui transforme l'IA en experts spécialisés pour chaque domaine de votre organisation.

- **100 harnais**: 10 catégories × 10 domaines (comptabilité, droit, RH, technologie, marketing, etc.)
- **Auto-évolution**: Cycle Self-Refine basé sur les retours utilisateur et l'analyse des résultats
- **Profil global**: Réponses personnalisées via des profils individuels, d'équipe et organisationnels
- **Basé sur plugins**: Intégration transparente avec Claude Code et l'écosystème Cowork

### Caractéristiques principales

| Fonction | Description |
|----------|-------------|
| **Apprentissage automatique** | Enregistrement et analyse des performances à chaque interaction |
| **Spécialisation par domaine** | Connaissances pratiques de pointe dans chaque domaine |
| **Adaptation culturelle** | Support des pratiques commerciales mondiales et des langues |
| **Mises à jour en temps réel** | Inclut les dernières lois fiscales, réglementations et informations de marché |
| **Support multi-utilisateur** | Gestion des profils au niveau équipe et collaboration |

---

## 📦 Installation

### Prérequis
- Claude Code (dernière version)
- Support des plugins Cowork

### Étape 1: Ajouter le plugin à Cowork
```bash
# Installer via Cowork CLI (à venir)
cowork install moai-cowork
```

### Étape 2: Initialiser le profil
```bash
moai init
```

### Étape 3: Configurer votre profil personnel
```bash
moai profile --set-personal
```

---

## 🚀 Démarrage rapide

### Exécuter votre première requête

```
@moai Quel est le calendrier de déclaration de TVA en France pour 2026 ?
```

**Réponse**: MoAI automatiquement:
1. Charge les informations de localisation pour la France
2. Consulte les données de droit fiscal 2026
3. Fournit un calendrier de TVA personnalisé

### Activer l'apprentissage automatique

```
moai learn --feedback "La réponse était très précise"
```

MoAI enregistre ce retour pour améliorer les requêtes similaires à l'avenir.

---

## 📚 Catalogue de 100 harnais

### 10 Catégories

#### 1️⃣ Fiscalité et Comptabilité (Tax & Accounting)
- **FR_TAX_001**: TVA française et impôts
- **US_TAX_001**: Impôt fédéral sur le revenu américain
- **JP_TAX_001**: Taxe de consommation japonaise
- **UK_TAX_001**: TVA du Royaume-Uni
- **VN_TAX_001**: TVA vietnamienne
- **TH_TAX_001**: TVA thaïlandaise
- *(6 supplémentaires)*

#### 2️⃣ Droit du travail et RH (Labor & HR)
- **FR_HR_001**: Droit du travail français
- **US_HR_001**: FLSA et salaire minimum
- **JP_HR_001**: Droit du travail japonais
- **UK_HR_001**: Droit de l'emploi britannique
- *(6 supplémentaires)*

#### 3️⃣ Données et Conformité (Data & Compliance)
- **FR_DATA_001**: Protection des données (RGPD)
- **US_DATA_001**: CCPA/HIPAA
- **JP_DATA_001**: Loi sur la protection des informations personnelles
- **UK_DATA_001**: UK GDPR
- *(6 supplémentaires)*

#### 4️⃣ Opérations commerciales (Business Operations)
- **FR_BIZ_001**: Pratiques commerciales françaises
- **US_BIZ_001**: Culture des réunions américaines
- **JP_BIZ_001**: Culture collaborative japonaise
- *(7 supplémentaires)*

#### 5️⃣ Technologie et IT (Technology & IT)
- **TECH_001**: Meilleures pratiques de développement logiciel
- **TECH_002**: Architecture cloud
- *(8 supplémentaires)*

#### 6️⃣ Marketing et Ventes (Marketing & Sales)
- **MKT_001**: Stratégie de marketing numérique
- **MKT_002**: Techniques de vente B2B
- *(8 supplémentaires)*

#### 7️⃣ Finance et Investissement (Finance & Investment)
- **FIN_001**: Analyse des états financiers
- **FIN_002**: Gestion de portefeuille d'investissement
- *(8 supplémentaires)*

#### 8️⃣ Droit et Contrats (Legal & Contracts)
- **LEG_001**: Révision de contrats
- **LEG_002**: Rédaction de NDA
- *(8 supplémentaires)*

#### 9️⃣ Stratégie et Planification (Strategy & Planning)
- **STR_001**: Élaboration de stratégie commerciale
- **STR_002**: Configuration des OKR
- *(8 supplémentaires)*

#### 🔟 Client et Service (Customer & Service)
- **CUS_001**: Analyse de la satisfaction client
- **CUS_002**: Plan d'amélioration des services
- *(8 supplémentaires)*

---

## 👤 Système de profil global

### Profil personnel (Personal Profile)
```yaml
name: "Marie Dupont"
role: "CFO"
locale: "fr_FR"
industry: "Finance"
experience_years: 15
languages: ["Français", "Anglais"]
```

### Profil d'équipe (Team Profile)
```yaml
team_name: "Équipe Finance"
region: "Paris"
size: 8
focus_areas: ["Fiscalité", "Comptabilité"]
```

### Profil organisationnel (Organization Profile)
```yaml
company_name: "ABC Corporation"
headquarters: "Paris"
founded: 2010
employees: 500
industries: ["Finance", "Technologie"]
expansion_regions: ["Allemagne", "Italie"]
```

---

## 🔄 Cycle d'auto-apprentissage (Self-Refine)

### Flux d'apprentissage

```
1. Exécuter la requête
   ↓
2. Générer la réponse (utilisant les harnais)
   ↓
3. Collecter les retours utilisateur
   ↓
4. Analyser les résultats (précision, pertinence, utilité)
   ↓
5. Améliorer le harnais (ajuster les poids)
   ↓
6. Appliquer à la requête suivante
```

### Types de retours

| Type | Description | Impact |
|------|-------------|--------|
| **Positif** | "Très précis" | Poids du harnais +10% |
| **Partiel** | "Partiellement correct" | Poids ±5% |
| **Négatif** | "Incorrect" | Poids du harnais -15% |
| **Personnalisé** | "Nécessite plus de contenu sur X" | Renforcement de domaine spécifique |

---

## 📖 Exemples d'utilisation

### Exemple 1: Consultation fiscale
```
Q: "Quel est le processus d'enregistrement des retenues sociales pour les nouveaux salariés en France ?"
→ Active le harnais FR_HR_001
→ Fournit les délais, documents requis et procédure
```

### Exemple 2: Commerce international
```
Q: "À quoi dois-je faire attention lors d'une réunion d'affaires aux États-Unis ?"
→ Active le harnais US_BIZ_001
→ Guide d'adaptation culturelle, gestion du temps, style de communication
```

### Exemple 3: Conformité réglementaire
```
Q: "Quelles procédures dois-je suivre pour traiter les données clients en UE ?"
→ Active les harnais FR_DATA_001 et RGPD pertinents
→ Conformité RGPD, gestion du consentement, procédures de transfert
```

---

## 🛠 Comment contribuer (Contributing)

### 1. Proposer un nouveau harnais
```bash
# Proposer un nouveau domaine
moai contribute --domain "Droit commercial français" --category "legal"
```

### 2. Améliorer un harnais existant
```bash
# Amélioration basée sur les retours
moai improve DOMAIN_ID --feedback "Contenu supplémentaire nécessaire"
```

### 3. Ajouter une nouvelle localisation
```bash
# Ajouter une nouvelle localisation de pays
moai add-locale --country "Belgique" --code "fr_BE"
```

### 4. Améliorer la documentation
- Modifier les fichiers de localisation dans `/skills/moai/references/locale/`
- Soumettre une Pull Request sur GitHub
- Mettre à jour les guides d'adaptation culturelle

---

## 📋 Roadmap

### Phase 1 (Actuelle)
- [x] Système de harnais de base
- [x] Guides de localisation globale (7 pays)
- [ ] Implémentation du cycle Self-Refine

### Phase 2 (2026 Q2)
- [ ] 100 harnais complétés
- [ ] Interface multilingue (12 langues)
- [ ] Fonctionnalités de collaboration d'équipe

### Phase 3 (2026 Q3)
- [ ] Mises à jour réglementaires en temps réel
- [ ] Processus d'examen IA-vers-Humain
- [ ] Modèles spécifiques à l'industrie

---

## 📞 Support et contact

- **Documentation**: `/skills/moai/references/locale/`
- **GitHub**: (à venir)
- **Email**: support@moai-cowork.dev

---

## 📄 Licence

Licence MIT - Libre d'utiliser, modifier et distribuer

---

## 🙏 Remerciements

MoAI-Cowork évolue continuellement grâce aux retours de la communauté Claude et Cowork.

---

**MoAI-Cowork: Rencontrez votre expert IA personnalisé.**

*Dernière mise à jour: 2026-04-04*
