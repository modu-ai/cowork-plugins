# 🗿 MoAI-Cowork

**100 arneses de auto-evolução — Seu especialista em IA personalizado**

[![Version](https://img.shields.io/badge/version-0.1.0-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

🌐 [한국어](README.md) | [English](README-en.md) | [日本語](README-ja.md) | [Español](README-es.md) | [Français](README-fr.md) | [Deutsch](README-de.md) | [Português](README-pt-BR.md) | [中文](README-zh-CN.md) | [Bahasa](README-id.md) | [हिन्दी](README-hi.md) | [Tiếng Việt](README-vi.md) | [ภาษาไทย](README-th.md) | [Italiano](README-it.md) | [Nederlands](README-nl.md) | [Polski](README-pl.md) | [العربية](README-ar.md) | [עברית](README-he.md)

---

## 🎯 O que é MoAI?

**MoAI-Cowork** é um sistema de aprendizado automático que transforma IA em especialistas dedicados para cada domínio da sua organização.

- **100 arneses**: 10 categorias × 10 domínios (contabilidade, direito, RH, tecnologia, marketing, etc.)
- **Auto-evolução**: Ciclo Self-Refine baseado em feedback do usuário e análise de resultados
- **Perfil global**: Respostas personalizadas através de perfis individual, de equipe e organizacional
- **Baseado em plugins**: Integração perfeita com Claude Code e o ecossistema Cowork

### Características principais

| Função | Descrição |
|--------|-----------|
| **Aprendizado automático** | Registro e análise de desempenho em cada interação |
| **Especialização em domínio** | Conhecimento prático de ponta em cada campo |
| **Adaptação cultural** | Suporte a práticas comerciais globais e idiomas |
| **Atualizações em tempo real** | Inclui leis fiscais, regulamentações e informações de mercado mais recentes |
| **Suporte multi-usuário** | Gerenciamento de perfis em nível de equipe e colaboração |

---

## 📦 Instalação

### Requisitos
- Claude Code (versão mais recente)
- Suporte a plugins Cowork

### Passo 1: Adicionar plugin ao Cowork
```bash
# Instalar via Cowork CLI (em breve)
cowork install moai-cowork
```

### Passo 2: Inicializar perfil
```bash
moai init
```

### Passo 3: Configurar perfil pessoal
```bash
moai profile --set-personal
```

---

## 🚀 Guia de início rápido

### Executar sua primeira consulta

```
@moai Qual é o calendário de declaração de ICMS no Brasil para 2026?
```

**Resposta**: MoAI automaticamente:
1. Carrega informações de localização do Brasil
2. Consulta dados de leis fiscais 2026
3. Fornece um calendário de ICMS personalizado

### Ativar aprendizado automático

```
moai learn --feedback "A resposta foi muito precisa"
```

MoAI registra este feedback para melhorar consultas similares no futuro.

---

## 📚 Catálogo de 100 arneses

### 10 Categorias

#### 1️⃣ Impostos e Contabilidade (Tax & Accounting)
- **BR_TAX_001**: ICMS e impostos federais brasileiros
- **US_TAX_001**: Imposto de renda federal dos EUA
- **JP_TAX_001**: Imposto sobre consumo japonês
- **UK_TAX_001**: VAT do Reino Unido
- **VN_TAX_001**: Imposto sobre valor agregado vietnamita
- **TH_TAX_001**: VAT tailandês
- *(6 mais)*

#### 2️⃣ Direito do trabalho e RH (Labor & HR)
- **BR_HR_001**: Direito do trabalho brasileiro
- **US_HR_001**: FLSA e salário mínimo
- **JP_HR_001**: Direito do trabalho japonês
- **UK_HR_001**: Direito de emprego britânico
- *(6 mais)*

#### 3️⃣ Dados e Conformidade (Data & Compliance)
- **BR_DATA_001**: Proteção de dados (LGPD)
- **US_DATA_001**: CCPA/HIPAA
- **JP_DATA_001**: Lei de Proteção de Informações Pessoais
- **UK_DATA_001**: UK GDPR
- *(6 mais)*

#### 4️⃣ Operações comerciais (Business Operations)
- **BR_BIZ_001**: Práticas comerciais brasileiras
- **US_BIZ_001**: Cultura de reuniões americanas
- **JP_BIZ_001**: Cultura colaborativa japonesa
- *(7 mais)*

#### 5️⃣ Tecnologia e TI (Technology & IT)
- **TECH_001**: Melhores práticas de desenvolvimento de software
- **TECH_002**: Arquitetura em nuvem
- *(8 mais)*

#### 6️⃣ Marketing e Vendas (Marketing & Sales)
- **MKT_001**: Estratégia de marketing digital
- **MKT_002**: Técnicas de vendas B2B
- *(8 mais)*

#### 7️⃣ Finanças e Investimento (Finance & Investment)
- **FIN_001**: Análise de demonstrações financeiras
- **FIN_002**: Gestão de portfólio de investimentos
- *(8 mais)*

#### 8️⃣ Direito e Contratos (Legal & Contracts)
- **LEG_001**: Revisão de contratos
- **LEG_002**: Redação de NDA
- *(8 mais)*

#### 9️⃣ Estratégia e Planejamento (Strategy & Planning)
- **STR_001**: Estabelecimento de estratégia empresarial
- **STR_002**: Configuração de OKR
- *(8 mais)*

#### 🔟 Cliente e Serviço (Customer & Service)
- **CUS_001**: Análise de satisfação do cliente
- **CUS_002**: Plano de melhoria de serviço
- *(8 mais)*

---

## 👤 Sistema de Perfil Global

### Perfil Pessoal (Personal Profile)
```yaml
name: "João Silva"
role: "CFO"
locale: "pt_BR"
industry: "Finanças"
experience_years: 15
languages: ["Português", "Inglês"]
```

### Perfil de Equipe (Team Profile)
```yaml
team_name: "Equipe Financeira"
region: "São Paulo"
size: 8
focus_areas: ["Impostos", "Contabilidade"]
```

### Perfil Organizacional (Organization Profile)
```yaml
company_name: "ABC Corporation"
headquarters: "São Paulo"
founded: 2010
employees: 500
industries: ["Finanças", "Tecnologia"]
expansion_regions: ["Argentina", "México"]
```

---

## 🔄 Ciclo de Auto-aprendizado (Self-Refine)

### Fluxo de aprendizado

```
1. Executar consulta
   ↓
2. Gerar resposta (usando arneses)
   ↓
3. Coletar feedback do usuário
   ↓
4. Analisar resultados (precisão, relevância, utilidade)
   ↓
5. Melhorar arnês (ajustar pesos)
   ↓
6. Aplicar à próxima consulta
```

### Tipos de feedback

| Tipo | Descrição | Impacto |
|------|-----------|---------|
| **Positivo** | "Muito preciso" | Peso do arnês +10% |
| **Parcial** | "Parcialmente correto" | Peso ±5% |
| **Negativo** | "Incorreto" | Peso do arnês -15% |
| **Personalizado** | "Precisa de mais conteúdo sobre X" | Reforço de área específica |

---

## 📖 Exemplos de uso

### Exemplo 1: Consulta fiscal
```
P: "Qual é o processo de registro de contribuições para novos funcionários no Brasil?"
→ Ativa arnês BR_HR_001
→ Fornece prazos, documentação necessária e procedimento
```

### Exemplo 2: Negócios internacionais
```
P: "O que devo observar em uma reunião de negócios nos EUA?"
→ Ativa arnês US_BIZ_001
→ Guia de adaptação cultural, gestão de tempo, estilo de comunicação
```

### Exemplo 3: Conformidade regulatória
```
P: "Que procedimentos preciso seguir para processar dados de clientes na UE?"
→ Ativa arneses BR_DATA_001 e GDPR relacionado
→ Conformidade GDPR, gerenciamento de consentimento, procedimentos de transferência
```

---

## 🛠 Como contribuir (Contributing)

### 1. Propor um novo arnês
```bash
# Propor novo domínio
moai contribute --domain "Direito comercial brasileiro" --category "legal"
```

### 2. Melhorar um arnês existente
```bash
# Melhoria baseada em feedback
moai improve DOMAIN_ID --feedback "Conteúdo adicional necessário"
```

### 3. Adicionar nova localização
```bash
# Adicionar nova localização de país
moai add-locale --country "Portugal" --code "pt_PT"
```

### 4. Melhorar documentação
- Editar arquivos de localização em `/skills/moai/references/locale/`
- Enviar Pull Request no GitHub
- Atualizar guias de adaptação cultural

---

## 📋 Roteiro

### Fase 1 (Atual)
- [x] Sistema base de arneses
- [x] Guias de localização global (7 países)
- [ ] Implementação do ciclo Self-Refine

### Fase 2 (2026 Q2)
- [ ] 100 arneses completos
- [ ] Interface multilíngue (12 idiomas)
- [ ] Funcionalidades de colaboração em equipe

### Fase 3 (2026 Q3)
- [ ] Atualizações regulatórias em tempo real
- [ ] Processo de revisão IA-para-Humano
- [ ] Modelos específicos da indústria

---

## 📞 Suporte e contato

- **Documentação**: `/skills/moai/references/locale/`
- **GitHub**: (em breve)
- **Email**: support@moai-cowork.dev

---

## 📄 Licença

Licença MIT - Livre para usar, modificar e distribuir

---

## 🙏 Agradecimentos

MoAI-Cowork evolui continuamente com feedback da comunidade Claude e Cowork.

---

**MoAI-Cowork: Conheça seu especialista em IA personalizado.**

*Última atualização: 2026-04-04*
