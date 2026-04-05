# 🗿 MoAI-Cowork

**100 Self-Evolving Domain Harnesses — Your Personal AI Experts**

[![Version](https://img.shields.io/badge/version-0.1.0-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

🌐 [한국어](README.md) | [日本語](README-ja.md) | [Español](README-es.md) | [Français](README-fr.md) | [Deutsch](README-de.md) | [Português](README-pt-BR.md) | [中文](README-zh-CN.md) | [Bahasa](README-id.md) | [हिन्दी](README-hi.md) | [Tiếng Việt](README-vi.md) | [ภาษาไทย](README-th.md)

---

## 🎯 What is MoAI?

**MoAI-Cowork** is an auto-learning system that transforms AI into domain experts across your organization.

- **100 Harnesses**: 10 categories × 10 domains (Accounting, Legal, HR, Tech, Marketing, etc.)
- **Self-Evolving**: Continuous improvement through user feedback and Self-Refine cycles
- **Global Profiles**: Personalized responses based on individual, team, and organizational profiles
- **Plugin-Based**: Seamless integration with Claude Code and Cowork ecosystem

### Core Features

| Feature | Description |
|---------|-------------|
| **Auto-Learning** | Performance tracking and analysis with each interaction |
| **Domain Expertise** | Best practices from each field |
| **Cultural Adaptation** | Global business practices and multilingual support |
| **Real-Time Updates** | Latest tax laws, regulations, and market info |
| **Multi-User Support** | Team-level profile management and collaboration |

---

## 📦 Installation

### Requirements
- Claude Code (latest version)
- Cowork plugin support

### Step 1: Add Plugin to Cowork
```bash
# Via Cowork CLI (coming soon)
cowork install moai-cowork
```

### Step 2: Initialize Profile
```bash
moai init
```

### Step 3: Set Personal Profile
```bash
moai profile --set-personal
```

---

## 🚀 Quick Start

### Run Your First Query

```
@moai What are the VAT reporting deadlines in the UK for 2026?
```

**Response**: MoAI automatically:
1. Loads UK locale information
2. References 2026 tax data
3. Provides customized VAT reporting timeline

### Enable Auto-Learning

```
moai learn --feedback "The answer was very accurate"
```

MoAI records this feedback to improve similar future queries.

---

## 📚 100 Harnesses Catalog

### 10 Categories

#### 1️⃣ Tax & Accounting
- **US_TAX_001**: Federal Income Tax
- **UK_TAX_001**: VAT & Corporation Tax
- **JP_TAX_001**: Consumption Tax
- **DE_TAX_001**: German Income Tax
- **FR_TAX_001**: French Corporate Tax
- *(5 more)*

#### 2️⃣ Labor & HR
- **US_HR_001**: FLSA & Minimum Wage
- **UK_HR_001**: Employment Rights
- **JP_HR_001**: Japanese Labor Law
- **DE_HR_001**: German Works Council
- *(6 more)*

#### 3️⃣ Data & Compliance
- **US_DATA_001**: CCPA/HIPAA/SOX
- **UK_DATA_001**: UK GDPR & DPA 2018
- **JP_DATA_001**: APPI Compliance
- **DE_DATA_001**: GDPR Implementation
- *(6 more)*

#### 4️⃣ Business Operations
- **US_BIZ_001**: American Business Practices
- **UK_BIZ_001**: British Business Culture
- **JP_BIZ_001**: Japanese Harmony Culture
- *(7 more)*

#### 5️⃣ Technology & IT
- **TECH_001**: Software Development Best Practices
- **TECH_002**: Cloud Architecture
- *(8 more)*

#### 6️⃣ Marketing & Sales
- **MKT_001**: Digital Marketing Strategy
- **MKT_002**: B2B Sales Techniques
- *(8 more)*

#### 7️⃣ Finance & Investment
- **FIN_001**: Financial Statement Analysis
- **FIN_002**: Investment Portfolio Management
- *(8 more)*

#### 8️⃣ Legal & Contracts
- **LEG_001**: Contract Review
- **LEG_002**: NDA Drafting
- *(8 more)*

#### 9️⃣ Strategy & Planning
- **STR_001**: Business Strategy Development
- **STR_002**: OKR Setting
- *(8 more)*

#### 🔟 Customer & Service
- **CUS_001**: Customer Satisfaction Analysis
- **CUS_002**: Service Improvement Planning
- *(8 more)*

---

## 👤 Global Profile System

### Personal Profile
```yaml
name: "John Smith"
role: "CFO"
locale: "en_US"
industry: "Finance"
experience_years: 15
languages: ["English", "French"]
```

### Team Profile
```yaml
team_name: "Finance Team"
region: "London"
size: 8
focus_areas: ["Taxation", "Accounting"]
```

### Organization Profile
```yaml
company_name: "Global Tech Corp"
headquarters: "San Francisco"
founded: 2010
employees: 2000
industries: ["Technology", "Finance"]
expansion_regions: ["EU", "APAC"]
```

---

## 🔄 Self-Refine Learning Cycle

### Learning Flow

```
1. Execute Query
   ↓
2. Generate Response (harness-based)
   ↓
3. Collect User Feedback
   ↓
4. Analyze Results (accuracy, relevance, utility)
   ↓
5. Improve Harness (weight adjustment)
   ↓
6. Apply to Next Query
```

### Feedback Types

| Type | Description | Impact |
|------|-------------|--------|
| **Positive** | "Very accurate" | Harness weight +10% |
| **Partial** | "Partially correct" | Weight ±5% |
| **Negative** | "Incorrect" | Harness weight -15% |
| **Custom** | "Add XX content" | Specific field enhancement |

---

## 📖 Usage Examples

### Example 1: Tax Consultation
```
Q: "What are the FLSA overtime rules for a US-based startup?"
→ US_HR_001 harness activated
→ Provides FLSA regulations, overtime rates, exemptions
```

### Example 2: International Business
```
Q: "What should I know about Japanese business meeting etiquette?"
→ JP_BIZ_001 harness activated
→ Provides business card etiquette, meeting format, communication style
```

### Example 3: Regulatory Compliance
```
Q: "What GDPR requirements apply to our EU customer data?"
→ UK_DATA_001 + relevant EU locale harnesses activated
→ Provides GDPR compliance checklist, consent management, data transfer procedures
```

---

## 🛠 Contributing

### 1. Propose a New Harness
```bash
# Suggest a new domain
moai contribute --domain "German Employment Law" --category "labor"
```

### 2. Improve Existing Harness
```bash
# Feedback-based improvement
moai improve DOMAIN_ID --feedback "Add missing content"
```

### 3. Add a New Locale
```bash
# Add a new country locale
moai add-locale --country "Brazil" --code "pt_BR"
```

### 4. Improve Documentation
- Edit locale files in `/skills/moai/references/locale/`
- Submit Pull Request on GitHub
- Update cultural adaptation guides

---

## 📋 Roadmap

### Phase 1 (Current)
- [x] Core harness system
- [x] Global locale guides (7 countries)
- [ ] Self-Refine cycle implementation

### Phase 2 (2026 Q2)
- [ ] Complete 100 harnesses
- [ ] Multilingual UI (12 languages)
- [ ] Team collaboration features

### Phase 3 (2026 Q3)
- [ ] Real-time regulatory updates
- [ ] AI-to-Human review process
- [ ] Industry-specific templates

---

## 📞 Support & Feedback

- **Documentation**: `/skills/moai/references/locale/`
- **GitHub**: (coming soon)
- **Email**: support@moai-cowork.dev

---

## 📄 License

MIT License - Free to use, modify, and distribute

---

## 🙏 Acknowledgments

MoAI-Cowork continues to evolve through feedback from the Claude and Cowork communities.

---

**MoAI-Cowork: Meet Your AI Experts.**

*Last Updated: 2026-04-04*
