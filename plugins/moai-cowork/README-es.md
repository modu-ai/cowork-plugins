# 🗿 MoAI-Cowork

**100 arneses de autoevolución — Tu experto en IA personalizado**

[![Version](https://img.shields.io/badge/version-0.1.0-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

🌐 [한국어](README.md) | [English](README-en.md) | [日本語](README-ja.md) | [Español](README-es.md) | [Français](README-fr.md) | [Deutsch](README-de.md) | [Português](README-pt-BR.md) | [中文](README-zh-CN.md) | [Bahasa](README-id.md) | [हिन्दी](README-hi.md) | [Tiếng Việt](README-vi.md) | [ภาษาไทย](README-th.md) | [Italiano](README-it.md) | [Nederlands](README-nl.md) | [Polski](README-pl.md) | [العربية](README-ar.md) | [עברית](README-he.md)

---

## 🎯 ¿Qué es MoAI?

**MoAI-Cowork** es un sistema de aprendizaje automático que transforma la IA en expertos especializados para cada dominio de tu organización.

- **100 arneses**: 10 categorías × 10 dominios (contabilidad, derecho, RRHH, tecnología, marketing, etc.)
- **Autoevolución**: Ciclo de Self-Refine basado en retroalimentación del usuario y análisis de resultados
- **Perfil global**: Respuestas personalizadas mediante perfiles individual, de equipo y organizacional
- **Basado en plugins**: Integración perfecta con Claude Code y el ecosistema Cowork

### Características clave

| Función | Descripción |
|---------|-------------|
| **Aprendizaje automático** | Registro y análisis del rendimiento en cada interacción |
| **Especialización de dominio** | Conocimiento práctico de vanguardia en cada campo |
| **Adaptación cultural** | Soporte para prácticas empresariales globales e idiomas |
| **Actualizaciones en tiempo real** | Incluye leyes fiscales, regulaciones e información de mercado más recientes |
| **Soporte Multi-Usuario** | Gestión de perfiles a nivel de equipo y colaboración |

---

## 📦 Instalación

### Requisitos
- Claude Code (última versión)
- Soporte de plugins Cowork

### Paso 1: Añadir el plugin a Cowork
```bash
# Instalar a través de Cowork CLI (próximamente)
cowork install moai-cowork
```

### Paso 2: Inicializar perfil
```bash
moai init
```

### Paso 3: Configurar perfil personal
```bash
moai profile --set-personal
```

---

## 🚀 Inicio rápido

### Ejecutar tu primera consulta

```
@moai ¿Cuál es el calendario de declaración de IVA en España para 2026?
```

**Respuesta**: MoAI automáticamente:
1. Carga la información de localización de España
2. Consulta datos de leyes fiscales de 2026
3. Proporciona un calendario de IVA personalizado

### Activar aprendizaje automático

```
moai learn --feedback "La respuesta fue muy precisa"
```

MoAI registra este comentario para mejorar consultas similares en el futuro.

---

## 📚 Catálogo de 100 arneses

### 10 Categorías

#### 1️⃣ Impuestos y Contabilidad (Tax & Accounting)
- **ES_TAX_001**: IVA español y retenciones
- **US_TAX_001**: Impuesto federal sobre la renta estadounidense
- **JP_TAX_001**: Impuesto al consumo japonés
- **UK_TAX_001**: IVA del Reino Unido
- **VN_TAX_001**: IVA vietnamita
- **TH_TAX_001**: IVA tailandés
- *(6 más)*

#### 2️⃣ Derecho laboral y RRHH (Labor & HR)
- **ES_HR_001**: Derecho laboral español
- **US_HR_001**: FLSA y salario mínimo
- **JP_HR_001**: Derecho laboral japonés
- **UK_HR_001**: Derecho de empleo británico
- *(6 más)*

#### 3️⃣ Datos y Cumplimiento (Data & Compliance)
- **ES_DATA_001**: Protección de datos (RGPD)
- **US_DATA_001**: CCPA/HIPAA
- **JP_DATA_001**: Ley de Protección de Información Personal
- **UK_DATA_001**: UK GDPR
- *(6 más)*

#### 4️⃣ Operaciones Empresariales (Business Operations)
- **ES_BIZ_001**: Prácticas empresariales españolas
- **US_BIZ_001**: Cultura de reuniones estadounidenses
- **JP_BIZ_001**: Cultura de colaboración japonesa
- *(7 más)*

#### 5️⃣ Tecnología e IT (Technology & IT)
- **TECH_001**: Mejores prácticas de desarrollo de software
- **TECH_002**: Arquitectura en la nube
- *(8 más)*

#### 6️⃣ Marketing y Ventas (Marketing & Sales)
- **MKT_001**: Estrategia de marketing digital
- **MKT_002**: Técnicas de venta B2B
- *(8 más)*

#### 7️⃣ Finanzas e Inversión (Finance & Investment)
- **FIN_001**: Análisis de estados financieros
- **FIN_002**: Gestión de cartera de inversión
- *(8 más)*

#### 8️⃣ Derecho y Contratos (Legal & Contracts)
- **LEG_001**: Revisión de contratos
- **LEG_002**: Redacción de NDA
- *(8 más)*

#### 9️⃣ Estrategia y Planificación (Strategy & Planning)
- **STR_001**: Establecimiento de estrategia empresarial
- **STR_002**: Configuración de OKR
- *(8 más)*

#### 🔟 Cliente y Servicio (Customer & Service)
- **CUS_001**: Análisis de satisfacción del cliente
- **CUS_002**: Plan de mejora de servicios
- *(8 más)*

---

## 👤 Sistema de Perfil Global

### Perfil Personal (Personal Profile)
```yaml
name: "María González"
role: "CFO"
locale: "es_ES"
industry: "Finanzas"
experience_years: 15
languages: ["Español", "Inglés"]
```

### Perfil de Equipo (Team Profile)
```yaml
team_name: "Equipo de Finanzas"
region: "Madrid"
size: 8
focus_areas: ["Impuestos", "Contabilidad"]
```

### Perfil Organizacional (Organization Profile)
```yaml
company_name: "ABC Corporation"
headquarters: "Madrid"
founded: 2010
employees: 500
industries: ["Finanzas", "Tecnología"]
expansion_regions: ["Portugal", "Italia"]
```

---

## 🔄 Ciclo de Autoaprendizaje (Self-Refine)

### Flujo de aprendizaje

```
1. Ejecutar consulta
   ↓
2. Generar respuesta (usando arneses)
   ↓
3. Recopilar retroalimentación del usuario
   ↓
4. Analizar resultados (precisión, relevancia, utilidad)
   ↓
5. Mejorar arnés (ajustar pesos)
   ↓
6. Aplicar a siguiente consulta
```

### Tipos de retroalimentación

| Tipo | Descripción | Impacto |
|------|-------------|---------|
| **Positiva** | "Muy preciso" | Peso del arnés +10% |
| **Parcial** | "Parcialmente correcto" | Peso ±5% |
| **Negativa** | "Incorrecto" | Peso del arnés -15% |
| **Personalizada** | "Necesita más contenido sobre X" | Refuerzo de área específica |

---

## 📖 Ejemplos de uso

### Ejemplo 1: Consulta fiscal
```
P: "¿Cuál es el proceso de registro de retenciones para empleados nuevos en España?"
→ Activa arnés ES_HR_001
→ Proporciona plazos, documentación requerida y procedimiento
```

### Ejemplo 2: Negocios internacionales
```
P: "¿Qué debo tener en cuenta en una reunión de negocios en Estados Unidos?"
→ Activa arnés US_BIZ_001
→ Guía de adaptación cultural, gestión del tiempo, estilo de comunicación
```

### Ejemplo 3: Cumplimiento normativo
```
P: "¿Qué procedimientos necesito para procesar datos de clientes en la UE?"
→ Activa arneses ES_DATA_001 y GDPR relacionado
→ Cumplimiento RGPD, gestión de consentimiento, procedimientos de transferencia
```

---

## 🛠 Cómo contribuir (Contributing)

### 1. Proponer un nuevo arnés
```bash
# Proponer nuevo dominio
moai contribute --domain "Derecho mercantil español" --category "legal"
```

### 2. Mejorar un arnés existente
```bash
# Mejora basada en retroalimentación
moai improve DOMAIN_ID --feedback "Se necesita más contenido"
```

### 3. Añadir una nueva localización
```bash
# Añadir nueva localización de país
moai add-locale --country "Portugal" --code "pt_PT"
```

### 4. Mejorar documentación
- Editar archivos de localización en `/skills/moai/references/locale/`
- Enviar Pull Request en GitHub
- Actualizar guías de adaptación cultural

---

## 📋 Roadmap

### Fase 1 (Actual)
- [x] Sistema básico de arneses
- [x] Guías de localización global (7 países)
- [ ] Implementación del ciclo Self-Refine

### Fase 2 (2026 Q2)
- [ ] 100 arneses completados
- [ ] Interfaz multilingüe (12 idiomas)
- [ ] Funciones de colaboración en equipo

### Fase 3 (2026 Q3)
- [ ] Actualizaciones de regulaciones en tiempo real
- [ ] Proceso de revisión AI-to-Human
- [ ] Plantillas específicas por industria

---

## 📞 Soporte y contacto

- **Documentación**: `/skills/moai/references/locale/`
- **GitHub**: (próximamente)
- **Email**: support@moai-cowork.dev

---

## 📄 Licencia

Licencia MIT - Libre para usar, modificar y distribuir

---

## 🙏 Agradecimientos

MoAI-Cowork evoluciona continuamente con retroalimentación de la comunidad Claude y Cowork.

---

**MoAI-Cowork: Conoce tu experto en IA personalizado.**

*Última actualización: 2026-04-04*
