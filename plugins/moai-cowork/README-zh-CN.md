# 🗿 MoAI-Cowork

**100个自演进域名工具 — 您的个性化AI专家**

[![Version](https://img.shields.io/badge/version-0.1.0-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

🌐 [한국어](README.md) | [English](README-en.md) | [日本語](README-ja.md) | [Español](README-es.md) | [Français](README-fr.md) | [Deutsch](README-de.md) | [Português](README-pt-BR.md) | [中文](README-zh-CN.md) | [Bahasa](README-id.md) | [हिन्दी](README-hi.md) | [Tiếng Việt](README-vi.md) | [ภาษาไทย](README-th.md) | [Italiano](README-it.md) | [Nederlands](README-nl.md) | [Polski](README-pl.md) | [العربية](README-ar.md) | [עברית](README-he.md)

---

## 🎯 什么是MoAI？

**MoAI-Cowork** 是一个自动学习系统，将AI转变为组织各领域的专业专家。

- **100个工具**: 10个类别 × 10个领域 (会计、法律、人力资源、技术、营销等)
- **自我进化**: 基于用户反馈和结果分析的Self-Refine循环
- **全球化档案**: 通过个人、团队和组织档案提供个性化回应
- **插件式设计**: 与Claude Code和Cowork生态系统无缝集成

### 核心特性

| 功能 | 描述 |
|------|------|
| **自动学习** | 每次互动的性能记录和分析 |
| **域名专业化** | 每个领域最前沿的实用知识 |
| **文化适应** | 支持全球商业实践和语言 |
| **实时更新** | 包含最新的税法、法规和市场信息 |
| **多用户支持** | 团队级别的档案管理和协作 |

---

## 📦 安装

### 需求
- Claude Code（最新版本）
- Cowork插件支持

### 步骤1：将插件添加到Cowork
```bash
# 通过Cowork CLI安装（即将推出）
cowork install moai-cowork
```

### 步骤2：初始化档案
```bash
moai init
```

### 步骤3：配置个人档案
```bash
moai profile --set-personal
```

---

## 🚀 快速开始

### 运行您的第一个查询

```
@moai 2026年中国增值税申报日期是什么？
```

**回应**: MoAI自动：
1. 加载中国的位置信息
2. 查询2026年税法数据
3. 提供个性化增值税申报日期

### 激活自动学习

```
moai learn --feedback "答案非常准确"
```

MoAI记录此反馈，以改进未来的类似查询。

---

## 📚 100个工具目录

### 10个类别

#### 1️⃣ 税务和会计 (Tax & Accounting)
- **CN_TAX_001**: 中国增值税
- **US_TAX_001**: 美国联邦所得税
- **JP_TAX_001**: 日本消费税
- **UK_TAX_001**: 英国增值税
- **VN_TAX_001**: 越南增值税
- **TH_TAX_001**: 泰国增值税
- *(6个更多)*

#### 2️⃣ 劳动法和人力资源 (Labor & HR)
- **CN_HR_001**: 中国劳动法
- **US_HR_001**: FLSA和最低工资
- **JP_HR_001**: 日本劳动法
- **UK_HR_001**: 英国就业法
- *(6个更多)*

#### 3️⃣ 数据和合规性 (Data & Compliance)
- **CN_DATA_001**: 个人信息保护法
- **US_DATA_001**: CCPA/HIPAA
- **JP_DATA_001**: 个人信息保护法
- **UK_DATA_001**: UK GDPR
- *(6个更多)*

#### 4️⃣ 商业运营 (Business Operations)
- **CN_BIZ_001**: 中国商业实践
- **US_BIZ_001**: 美国会议文化
- **JP_BIZ_001**: 日本协作文化
- *(7个更多)*

#### 5️⃣ 技术和IT (Technology & IT)
- **TECH_001**: 软件开发最佳实践
- **TECH_002**: 云架构
- *(8个更多)*

#### 6️⃣ 市场营销和销售 (Marketing & Sales)
- **MKT_001**: 数字营销战略
- **MKT_002**: B2B销售技巧
- *(8个更多)*

#### 7️⃣ 财务和投资 (Finance & Investment)
- **FIN_001**: 财务报表分析
- **FIN_002**: 投资组合管理
- *(8个更多)*

#### 8️⃣ 法律和合同 (Legal & Contracts)
- **LEG_001**: 合同审查
- **LEG_002**: NDA起草
- *(8个更多)*

#### 9️⃣ 战略和规划 (Strategy & Planning)
- **STR_001**: 业务战略制定
- **STR_002**: OKR设定
- *(8个更多)*

#### 🔟 客户和服务 (Customer & Service)
- **CUS_001**: 客户满意度分析
- **CUS_002**: 服务改进计划
- *(8个更多)*

---

## 👤 全球档案系统

### 个人档案 (Personal Profile)
```yaml
name: "王小明"
role: "首席财务官"
locale: "zh_CN"
industry: "金融"
experience_years: 15
languages: ["中文", "英文"]
```

### 团队档案 (Team Profile)
```yaml
team_name: "财务团队"
region: "北京"
size: 8
focus_areas: ["税务", "会计"]
```

### 组织档案 (Organization Profile)
```yaml
company_name: "ABC Corporation"
headquarters: "北京"
founded: 2010
employees: 500
industries: ["金融", "技术"]
expansion_regions: ["日本", "新加坡"]
```

---

## 🔄 自学循环 (Self-Refine)

### 学习流程

```
1. 执行查询
   ↓
2. 生成回应（使用工具）
   ↓
3. 收集用户反馈
   ↓
4. 分析结果（准确性、相关性、实用性）
   ↓
5. 改进工具（调整权重）
   ↓
6. 应用到下一个查询
```

### 反馈类型

| 类型 | 描述 | 影响 |
|------|------|------|
| **正面** | "非常准确" | 工具权重 +10% |
| **部分** | "部分正确" | 权重 ±5% |
| **负面** | "不正确" | 工具权重 -15% |
| **自定义** | "需要更多关于X的内容" | 特定领域加强 |

---

## 📖 使用示例

### 示例1：税务咨询
```
问：在中国招聘新员工时的社保登记流程是什么？
→ 激活工具CN_HR_001
→ 提供截止日期、所需文件和流程
```

### 示例2：国际商务
```
问：在美国商务会议中应该注意什么？
→ 激活工具US_BIZ_001
→ 文化适应指南、时间管理、沟通风格
```

### 示例3：法规合规
```
问：在欧盟处理客户数据需要什么程序？
→ 激活工具CN_DATA_001和相关GDPR
→ GDPR合规、同意管理、数据转移流程
```

---

## 🛠 如何贡献 (Contributing)

### 1. 提议新工具
```bash
# 提议新领域
moai contribute --domain "中国商业法" --category "legal"
```

### 2. 改进现有工具
```bash
# 基于反馈的改进
moai improve DOMAIN_ID --feedback "需要更多内容"
```

### 3. 添加新的本地化
```bash
# 添加新国家本地化
moai add-locale --country "台湾" --code "zh_TW"
```

### 4. 改进文档
- 编辑 `/skills/moai/references/locale/` 中的本地化文件
- 在GitHub上提交Pull Request
- 更新文化适应指南

---

## 📋 路线图

### 阶段1（当前）
- [x] 基础工具系统
- [x] 全球本地化指南（7个国家）
- [ ] Self-Refine循环实现

### 阶段2（2026年Q2）
- [ ] 100个工具完成
- [ ] 多语言UI（12种语言）
- [ ] 团队协作功能

### 阶段3（2026年Q3）
- [ ] 实时法规更新
- [ ] AI转人工审查流程
- [ ] 行业特定模板

---

## 📞 支持和联系

- **文档**: `/skills/moai/references/locale/`
- **GitHub**: （即将推出）
- **邮箱**: support@moai-cowork.dev

---

## 📄 许可证

MIT许可 - 自由使用、修改和分发

---

## 🙏 致谢

MoAI-Cowork通过Claude和Cowork社区的反馈不断发展。

---

**MoAI-Cowork: 认识您的个性化AI专家。**

*上次更新：2026-04-04*
