---
version: alpha
name: Saniti-design-analysis
description: An inspired interpretation of Saniti's design language — a dark-first, content-platform marketing system that pairs an oversized editorial display sans (waldenburgNormal) with IBM Plex Mono for technical eyebrows. The site reads like a software-engineering trade journal: near-black `{colors.canvas}` reading bands, white text, a single signature coral-red accent (`{colors.brand}`) reserved for the highest-priority action, and a deliberate light-theme inversion on commercial pages (pricing) where dense feature tables demand maximum legibility. Display sizes climb to 112px with tightly-cut negative tracking; rounded pills coexist with sharply-cut 3–6px application-grade radii from the Studio screenshots, signalling the dual identity of "marketing brand" and "developer tool."

colors:
  primary: "#0b0b0b"
  on-primary: "#ffffff"
  brand: "#f36458"
  brand-deep: "#dd0000"
  ink: "#0b0b0b"
  ink-soft: "#212121"
  graphite: "#353535"
  slate: "#3c4758"
  slate-soft: "#505b6c"
  mute: "#797979"
  ash: "#b9b9b9"
  hairline: "#ededed"
  hairline-soft: "#353535"
  canvas: "#0b0b0b"
  canvas-soft: "#212121"
  canvas-light: "#ffffff"
  canvas-paper: "#ededed"
  on-canvas-light: "#0b0b0b"
  link-blue: "#0052ef"
  link-blue-soft: "#55beff"
  surface-blue-bg: "#afe3ff"
  success: "#37cd84"
  error: "#dd0000"

typography:
  display-mega:
    fontFamily: waldenburgNormal
    fontSize: 112px
    fontWeight: 400
    lineHeight: 1.0
    letterSpacing: -4.48px
    fontFeature: cv01, cv11, cv12, cv13, ss07
  display-xl:
    fontFamily: waldenburgNormal
    fontSize: 72px
    fontWeight: 400
    lineHeight: 1.05
    letterSpacing: -2.88px
  display-lg:
    fontFamily: waldenburgNormal
    fontSize: 60px
    fontWeight: 400
    lineHeight: 0.8
  display-md:
    fontFamily: waldenburgNormal
    fontSize: 48px
    fontWeight: 400
    lineHeight: 1.08
    letterSpacing: -1.68px
  display-sm:
    fontFamily: waldenburgNormal
    fontSize: 38px
    fontWeight: 400
    lineHeight: 1.1
    letterSpacing: -1.14px
  heading-md:
    fontFamily: waldenburgNormal
    fontSize: 32px
    fontWeight: 425
    lineHeight: 1.13
    letterSpacing: -0.32px
  heading-sm:
    fontFamily: waldenburgNormal
    fontSize: 24px
    fontWeight: 400
    lineHeight: 1.1
    letterSpacing: -0.24px
  subtitle:
    fontFamily: waldenburgNormal
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: -0.18px
  body:
    fontFamily: waldenburgNormal
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
  body-sm:
    fontFamily: waldenburgNormal
    fontSize: 15px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: -0.15px
  caption:
    fontFamily: waldenburgNormal
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.5
  caption-tight:
    fontFamily: waldenburgNormal
    fontSize: 13px
    fontWeight: 500
    lineHeight: 1.3
    letterSpacing: -0.13px
  meta:
    fontFamily: waldenburgNormal
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: -0.12px
  mono-eyebrow:
    fontFamily: ibmPlexMono
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.5
  mono-caps:
    fontFamily: ibmPlexMono
    fontSize: 11px
    fontWeight: 400
    lineHeight: 1.5
  mono-micro:
    fontFamily: ibmPlexMono
    fontSize: 10px
    fontWeight: 400
    lineHeight: 1.3
  button-lg:
    fontFamily: waldenburgNormal
    fontSize: 16px
    fontWeight: 500
    lineHeight: 1.5
  button-sm:
    fontFamily: waldenburgNormal
    fontSize: 13px
    fontWeight: 500
    lineHeight: 1.3
    letterSpacing: -0.13px
  button-uppercase:
    fontFamily: waldenburgNormal
    fontSize: 11px
    fontWeight: 600
    lineHeight: 1.5

rounded:
  none: 0px
  app-xs: 3px
  app-sm: 4px
  app-md: 5px
  app-lg: 6px
  marketing: 12px
  full: 99999px

spacing:
  xxs: 4px
  xs: 8px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 32px
  xxl: 48px
  section: 64px
  section-lg: 96px

components:
  button-primary:
    backgroundColor: "{colors.canvas-light}"
    textColor: "{colors.ink}"
    typography: "{typography.button-lg}"
    rounded: "{rounded.full}"
    padding: 12px
    height: 44px
  button-primary-on-light:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button-lg}"
    rounded: "{rounded.full}"
    padding: 12px
    height: 44px
  button-brand:
    backgroundColor: "{colors.brand}"
    textColor: "{colors.ink}"
    typography: "{typography.button-lg}"
    rounded: "{rounded.full}"
    padding: 12px
    height: 44px
  button-secondary-dark:
    backgroundColor: "{colors.canvas-soft}"
    textColor: "{colors.ash}"
    typography: "{typography.button-sm}"
    rounded: "{rounded.app-md}"
    padding: 12px
    height: 36px
  button-ghost-dark:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ash}"
    typography: "{typography.button-sm}"
    rounded: "{rounded.full}"
    padding: 12px
    height: 36px
  button-app-tab:
    backgroundColor: "{colors.canvas-soft}"
    textColor: "{colors.ash}"
    typography: "{typography.button-uppercase}"
    rounded: "{rounded.app-sm}"
    padding: 8px
    height: 32px
  nav-bar-dark:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button-lg}"
    height: 64px
    padding: 24px
  nav-link:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button-lg}"
    padding: 8px
  hero-display:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.on-primary}"
    typography: "{typography.display-mega}"
    padding: 48px
  marketing-section-dark:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body}"
    padding: 96px
  marketing-section-light:
    backgroundColor: "{colors.canvas-light}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    padding: 96px
  marketing-section-paper:
    backgroundColor: "{colors.canvas-paper}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    padding: 96px
  feature-card-dark:
    backgroundColor: "{colors.canvas-soft}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body}"
    rounded: "{rounded.marketing}"
    padding: 32px
  feature-card-brand:
    backgroundColor: "{colors.brand}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.marketing}"
    padding: 32px
  feature-card-light:
    backgroundColor: "{colors.canvas-light}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.marketing}"
    padding: 32px
  pricing-card:
    backgroundColor: "{colors.canvas-light}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.marketing}"
    padding: 32px
  pricing-card-featured:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body}"
    rounded: "{rounded.marketing}"
    padding: 32px
  pricing-amount:
    backgroundColor: "{colors.canvas-light}"
    textColor: "{colors.ink}"
    typography: "{typography.display-md}"
  comparison-table-row:
    backgroundColor: "{colors.canvas-light}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    padding: 16px
  studio-window:
    backgroundColor: "{colors.canvas-soft}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.app-lg}"
    padding: 16px
  text-input:
    backgroundColor: "{colors.canvas-light}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.app-xs}"
    padding: 12px
    height: 44px
  text-input-dark:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ash}"
    typography: "{typography.body}"
    rounded: "{rounded.app-xs}"
    padding: 12px
    height: 44px
  text-input-focused:
    backgroundColor: "{colors.canvas-light}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.app-xs}"
    padding: 12px
  textarea:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ash}"
    typography: "{typography.body}"
    rounded: "{rounded.app-xs}"
    padding: 12px
  badge-neutral:
    backgroundColor: "{colors.canvas-light}"
    textColor: "{colors.ink}"
    typography: "{typography.caption}"
    rounded: "{rounded.full}"
    padding: 8px
  badge-filled:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.on-primary}"
    typography: "{typography.caption}"
    rounded: "{rounded.full}"
    padding: 8px
  brand-dot:
    backgroundColor: "{colors.brand}"
    textColor: "{colors.ink}"
    rounded: "{rounded.full}"
    size: 12px
  footer:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body}"
    padding: 64px
  footer-link:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ash}"
    typography: "{typography.caption}"
  footer-eyebrow:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.mute}"
    typography: "{typography.mono-caps}"
  alert-banner:
    backgroundColor: "{colors.surface-blue-bg}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.app-lg}"
    padding: 16px
---

## Overview

Saniti's marketing surface is built around a single, high-conviction idea: a content platform should look like an editorial property. The homepage opens onto a near-black `{colors.canvas}` page where a 112px display headline ("Structure powers intelligence") fills the entire viewport with `{typography.display-mega}` set in the proprietary `waldenburgNormal` sans, cut at -4.48px tracking. White type sits on this dark stage like ink on a printed broadside. A single coral-red accent (`{colors.brand}`) appears sparingly — never on backgrounds, only on a few key CTAs and the brand dot — keeping the page feeling sober rather than promotional.

The system runs in two modes that share the same type system but invert canvas. The dark mode (homepage, content-agent, studio-marketing) is the brand voice: oversized headlines, sparse white body, deep-navy slate accents, and IBM Plex Mono eyebrows lending technical credibility. The light mode (pricing) is the commercial voice: white canvas, black ink, dense 4-tier comparison tables, and the same coral-red `{colors.brand}` reused as the featured pricing tier's accent. Switching between the two modes mid-document is part of the page rhythm — Saniti treats colour theme as section-scoped, not page-scoped.

Two type families do all the work: `waldenburgNormal` for every running text role (display through caption), and `ibmPlexMono` reserved exclusively for technical eyebrows and small-caps labels. Display sizes range from 112px down to 38px in a continuous editorial scale; tracking tightens aggressively on display (-4.48px at 112px) and relaxes to neutral on body (16px). OpenType variants are switched on across the marketing copy (`cv01`, `cv11`, `cv12`, `cv13`, `ss07`) — characters like the single-storey `g` and rounded `t` give the headlines a humanist, slightly literary feel.

**Key Characteristics:**
- Dark-first marketing surface (`{colors.canvas}` `#0b0b0b`) with white type and a single coral-red accent (`{colors.brand}`)
- Oversized editorial display type up to 112px in `waldenburgNormal` with aggressive negative tracking
- Dual-theme rhythm: dark hero/feature sections invert to light pricing/comparison surfaces, both using the same type system
- IBM Plex Mono reserved exclusively for technical eyebrows and small-caps labels — every other role is the proprietary sans
- Pill primary buttons (`{rounded.full}`) for marketing CTAs paired with sharply-cut application radii (3–6px) for in-product Studio screenshots
- 4-tier pricing card grid where the featured tier is signalled by full-fill `{colors.ink}` inversion, not by a coloured ribbon
- Dense feature-comparison tables on `{colors.canvas-light}` with hairline `{colors.hairline}` row dividers — the densest typographic surface in the system

## Colors

### Brand & Accent
- **Coral-Red** (`{colors.brand}` — `#f36458`): The single signature accent. Reserved for the highest-priority CTA per page (one occurrence per viewport on most pages), the brand dot beside the wordmark, and brand-card surface fills on content-agent and select feature panels. Used sparingly enough that a viewer can predict where it will appear.
- **Brand Deep** (`{colors.brand-deep}` — `#dd0000`): The error/destructive variant — never used as a hero or section accent.
- **Black** (`{colors.primary}` — `#0b0b0b`): Default canvas in dark sections; primary action fill on light sections; default text colour on light surfaces. The most-used colour in the system after `{colors.on-primary}`.

### Surface
- **Canvas** (`{colors.canvas}` — `#0b0b0b`): Default dark-section background. Near-black with no warmth.
- **Canvas Soft** (`{colors.canvas-soft}` — `#212121`): Card and panel surface inside dark sections. Used for feature-card-dark and Studio-window mockups. Provides a single-step elevation cue.
- **Canvas Light** (`{colors.canvas-light}` — `#ffffff`): Primary light-mode background. Used for the entire pricing page, marketing-section-light bands, and pricing-card surface.
- **Canvas Paper** (`{colors.canvas-paper}` — `#ededed`): Warm-grey alternate light surface used for some hero-card tiles on the studio page; chosen to lift cards a half-tone above pure white without losing the clean reading feel.
- **Hairline Soft** (`{colors.hairline-soft}` — `#353535`): 1-pixel border colour on dark cards and dialog panels.
- **Hairline** (`{colors.hairline}` — `#ededed`): 1-pixel border on light cards, comparison-table dividers, and feature-grid rules.
- **Surface Blue Bg** (`{colors.surface-blue-bg}` — `#afe3ff`): Soft-blue alert/info surface — the only chromatic surface fill in the system.

### Text
- **Ink** (`{colors.ink}` — `#0b0b0b`): Headlines and body on light surfaces.
- **Ink Soft** (`{colors.ink-soft}` — `#212121`): Secondary text on light surfaces; container background colour for dark cards.
- **Graphite** (`{colors.graphite}` — `#353535`): Tertiary text and dividers in dark sections.
- **Slate** (`{colors.slate}` — `#3c4758`) / **Slate Soft** (`{colors.slate-soft}` — `#505b6c`): Cool blue-grey neutrals used for secondary-link text and de-emphasized rule lines on dark.
- **Mute** (`{colors.mute}` — `#797979`): Mid-grey mono caption colour, footer eyebrows.
- **Ash** (`{colors.ash}` — `#b9b9b9`): Default body text on dark surfaces.
- **On Primary** (`{colors.on-primary}` — `#ffffff`): Headline colour on dark surfaces; ink colour on `{colors.brand}` and `{colors.ink}` filled buttons.

### Semantic
- **Link Blue** (`{colors.link-blue}` — `#0052ef`): Inline link colour on light surfaces; standard hyperlink hue.
- **Link Blue Soft** (`{colors.link-blue-soft}` — `#55beff`): Link colour on dark surfaces.
- **Success** (`{colors.success}` — `#37cd84`): Validation success — used in the Studio status pill and "available" markers in the pricing comparison table.
- **Error** (`{colors.error}` — `#dd0000`): Required-field markers and error messages.

## Typography

### Font Family
The marketing system runs on **waldenburgNormal**, a proprietary humanist sans in the ABC Walden Burn family — uniform stroke contrast, single-storey `a` available via `cv01`, slightly compressed counters, and stylistic alternates (`ss07`, `cv11`–`cv13`) that round terminals and soften the `g`/`y` descenders. The result is editorial — it reads like a contemporary trade magazine more than a typical SaaS sans. **ibmPlexMono** is paired in for two roles only: technical eyebrows and small-caps captions. Helvetica appears in the extracted token data but is a fallback artefact, not a brand specimen.

### Hierarchy

| Token | Size | Weight | Line Height | Letter Spacing | Use |
|---|---|---|---|---|---|
| `{typography.display-mega}` | 112px | 400 | 1.0 | -4.48px | Page-defining hero ("Structure powers intelligence"); maximum one per page |
| `{typography.display-xl}` | 72px | 400 | 1.05 | -2.88px | Section-opening editorial display ("Loved by 1M+ users…") |
| `{typography.display-lg}` | 60px | 400 | 0.8 | 0 | Tightly-leaded display used for emphatic sub-section heads |
| `{typography.display-md}` | 48px | 400 | 1.08 | -1.68px | Standard section headlines, pricing tier amounts |
| `{typography.display-sm}` | 38px | 400 | 1.10 | -1.14px | Sub-section heads, content-agent feature headers |
| `{typography.heading-md}` | 32px | 425 | 1.13 | -0.32px | Card titles, large list-item labels |
| `{typography.heading-sm}` | 24px | 400 | 1.10 | -0.24px | Small section labels, feature-card titles |
| `{typography.subtitle}` | 18px | 400 | 1.5 | -0.18px | Hero sub-copy, lead paragraphs |
| `{typography.body}` | 16px | 400 | 1.5 | 0 | Default running body across both themes |
| `{typography.body-sm}` | 15px | 400 | 1.5 | -0.15px | Comparison-table cells, mid-density reading copy |
| `{typography.caption}` | 13px | 400 | 1.5 | 0 | Card captions, list-item meta |
| `{typography.caption-tight}` | 13px | 500 | 1.3 | -0.13px | Tight metadata, button-sm typography |
| `{typography.meta}` | 12px | 400 | 1.5 | -0.12px | Footnotes, fine print |
| `{typography.mono-eyebrow}` | 13px | 400 | 1.5 | 0 | Section eyebrows in IBM Plex Mono |
| `{typography.mono-caps}` | 11px | 400 | 1.5 | 0 | Small-caps mono labels and footer column heads |
| `{typography.mono-micro}` | 10px | 400 | 1.3 | 0 | Tag chips and very fine technical labels |
| `{typography.button-lg}` | 16px | 500 | 1.5 | 0 | Marketing CTA buttons |
| `{typography.button-sm}` | 13px | 500 | 1.3 | -0.13px | Inline secondary actions, tab buttons |
| `{typography.button-uppercase}` | 11px | 600 | 1.5 | 0 | Studio app-style toolbar tabs (uppercase) |

### Principles
- **One brand sans across every level.** Hierarchy comes from size, weight, and tracking; never from a contrasting display family.
- **Aggressive negative tracking on display sizes.** -4.48px at 112px tightens the silhouette of huge headlines into something readable as a single visual unit rather than a row of letters.
- **Mono is exclusively a labelling system.** IBM Plex Mono is reserved for eyebrows, small-caps tags, and technical-feel captions. Never use mono for body running copy.
- **OpenType features stay enabled across waldenburgNormal display.** `cv01`, `cv11`, `cv12`, `cv13`, `ss07` deliver the single-storey `a`, rounded `t`, soft `g` — these are core to the brand voice. Body sizes drop the OpenType variants and let the default forms render.

### Note on Font Substitutes
If `waldenburgNormal` is unavailable, **ABC Walden** (commercial) is the closest substitute. **Inter** at the same sizes works as a fallback if the OpenType-feature richness is dropped — pull `letter-spacing` 0.5px tighter at display sizes (-5.0px at 112px) to compensate for Inter's looser default tracking. Keep IBM Plex Mono unchanged — it is open-source and ships with the desired feel.

## Layout

### Spacing System
- **Base unit**: 8px, with 4px micro-steps for inline spacing.
- **Tokens (front matter)**: `{spacing.xxs}` 4px · `{spacing.xs}` 8px · `{spacing.sm}` 12px · `{spacing.md}` 16px · `{spacing.lg}` 24px · `{spacing.xl}` 32px · `{spacing.xxl}` 48px · `{spacing.section}` 64px · `{spacing.section-lg}` 96px.
- Card internal padding sits at `{spacing.xl}` (32px) on marketing cards and `{spacing.md}` (16px) on Studio-window mockups. Section vertical rhythm uses `{spacing.section-lg}` (96px) between major modules — this is the constant that holds across home, studio, content-agent, and pricing pages.

### Grid & Container
- Marketing pages render inside a centred container that caps near 1640px on widescreen. The hero typography uses the full container width — display headlines often span the full content area without an enclosing card.
- Pricing uses a 4-tier column grid (Free / Growth / Enterprise / Custom by typical layout pattern) on widescreen, with the featured tier flipping to `{pricing-card-featured}` polarity. Below the tier grid, the comparison table is a single very-wide table spanning the full container; cells are 16px-padded and alternate between feature label and per-tier check/value.
- Content-agent uses an irregular asymmetric grid: a left-side text column at ~50% width, right-side feature cards in a 2-up grid below. This breaks the otherwise-symmetric system rhythm to flag the page as a campaign rather than a product page.
- Studio uses a tight masonry of code-window mockups, each rendered in `{studio-window}` style with sharp `{rounded.app-lg}` corners.

### Whitespace Philosophy
The dark canvas does most of the visual work — generous negative space lets the editorial display headlines breathe. Sections are separated by `{spacing.section-lg}` (96px) verticals; cards inside a section use `{spacing.lg}` (24px) gaps. Padding inside marketing cards is `{spacing.xl}` (32px) — slightly more generous than the `{spacing.lg}` typical in B2B SaaS systems, giving cards an editorial-spread feel. The pricing comparison table is the deliberate exception: row padding tightens to `{spacing.md}` (16px) to fit a 30+ row matrix without overwhelming the page.

## Elevation & Depth

| Level | Treatment | Use |
|---|---|---|
| Flat (Dark) | `{colors.canvas}` background, no shadow, no border | Default dark-section reading surface |
| Card (Dark) | `{colors.canvas-soft}` infill on `{colors.canvas}` page, `{rounded.marketing}` corners, optional 1px `{colors.hairline-soft}` border | Feature cards, Studio-window mockups, content-agent tiles |
| Card (Light) | `{colors.canvas-light}` on `{colors.canvas-paper}` band OR `{colors.canvas-light}` with 1px `{colors.hairline}` border | Pricing cards, marketing-section-light feature tiles |
| Inverted Featured | `{colors.ink}` on `{colors.canvas-light}` page, white text | Featured pricing tier — the polarity flip is the whole "featured" cue |
| Brand Surface | `{colors.brand}` fill | Brand-card, content-agent CTA panels, brand-dot |
| Soft Drop | Subtle `0 4px 24px rgba(0,0,0,0.08)` on light cards only | Resting-state lift on the pricing-card hero panel |

The system avoids heavy drop shadows. Depth is delivered primarily by tonal surface stepping (canvas → canvas-soft → canvas-light) and by the polarity flip between dark and light surfaces. The two extracted shadow values are reserved for very rare lift cues — most cards sit flush.

### Decorative Depth
- **Polarity flip as drama.** Saniti's strongest depth cue is the inversion between dark and light sections. The eye reads a hard edge between two adjacent sections (one canvas, one canvas-light) as a strong layout statement.
- **Brand-card flash.** A single feature card filled with `{colors.brand}` mid-section creates a visual anchor without a shadow or border — the colour change is the depth cue.

## Shapes

### Border Radius Scale

| Token | Value | Use |
|---|---|---|
| `{rounded.none}` | 0px | Comparison table cells, full-width banners |
| `{rounded.app-xs}` | 3px | Text inputs, textarea, application-style fields |
| `{rounded.app-sm}` | 4px | Heading-level pill chips, secondary inputs |
| `{rounded.app-md}` | 5px | Studio toolbar buttons, tab pills, secondary actions |
| `{rounded.app-lg}` | 6px | Studio window mockups, code blocks |
| `{rounded.marketing}` | 12px | Feature cards, pricing cards, content-agent panels |
| `{rounded.full}` | 99999px | Marketing CTAs, badges, brand dot, tag chips |

### Photography Geometry
- **Studio screenshots** are framed inside `{rounded.app-lg}` (6px) windows — chosen to mimic native macOS/Windows application chrome rather than card-rounding, so the screenshots read as "real product."
- **Content-agent illustrations** are full-bleed `{rounded.marketing}` panels with abstract gradient surfaces.
- **Avatar/logo lockups** in the partner band are flat black or white wordmarks with no rounding, evenly spaced across a single row.

## Components

### Buttons

**`button-primary`** — the marketing CTA on dark sections ("Get Started Free")
- Background `{colors.canvas-light}`, text `{colors.ink}`, type `{typography.button-lg}`, padding `{spacing.sm}` × `{spacing.lg}`, rounded `{rounded.full}`, height 44px, with a thin `{colors.ink}` border that paints inside the white pill and reads as a confident edge against the dark canvas.

**`button-primary-on-light`** — the inverse for light-section heroes
- Background `{colors.ink}`, text `{colors.on-primary}`, identical token set otherwise.

**`button-brand`** — the rare brand-coloured CTA reserved for "Contact Sales" or peak-priority prompts
- Background `{colors.brand}`, text `{colors.ink}`, type `{typography.button-lg}`, rounded `{rounded.full}`, padding `{spacing.sm}` × `{spacing.lg}`.

**`button-secondary-dark`** — secondary actions on dark surfaces
- Background `{colors.canvas-soft}`, text `{colors.ash}`, type `{typography.button-sm}`, rounded `{rounded.app-md}`, padding `{spacing.sm}`, height 36px, 1px `{colors.hairline-soft}` border.

**`button-ghost-dark`** — text-style links on dark
- Background `{colors.canvas}` (transparent), text `{colors.ash}`, type `{typography.button-sm}`, rounded `{rounded.full}`.

**`button-app-tab`** — Studio-style toolbar tabs (visible inside Studio screenshot mockups)
- Background `{colors.canvas-soft}`, text `{colors.ash}`, type `{typography.button-uppercase}` (uppercase IBM Plex Mono-feel), rounded `{rounded.app-sm}`, padding `{spacing.xs}`, height 32px.

### Navigation

**`nav-bar-dark`** — the persistent dark top bar
- Background `{colors.canvas}`, height ~64px, padding `{spacing.lg}` horizontal, white text.
- Layout: red `brand-dot` + `Saniti` wordmark left → centred primary menu (Product, Solutions, Resources, Customers, Pricing, Docs) → right cluster (`Sign In` text link, `Book a Demo` `{button-secondary-dark}`, `Get Started Free` `{button-primary}`).
- Sticky on scroll, no border division — the bar is held to the page only by the colour contrast against any light section that scrolls underneath.

**`nav-link`** — primary menu items
- Background `{colors.canvas}`, text `{colors.on-primary}`, type `{typography.button-lg}`, padding `{spacing.xs}` vertical.

### Cards & Containers

**`hero-display`** — the homepage display lockup
- Background `{colors.canvas}`, text `{colors.on-primary}`, type `{typography.display-mega}`. The hero is type-only on the home page; supplementary subtitle, lead paragraph, and primary CTA stack directly below in `{spacing.lg}` increments.

**`feature-card-dark`** — the standard dark-section feature card
- Background `{colors.canvas-soft}`, text `{colors.on-primary}`, padding `{spacing.xl}`, rounded `{rounded.marketing}`, with optional 1px `{colors.hairline-soft}` border.
- Internal stack: optional `{typography.mono-eyebrow}` label → `{typography.heading-sm}` title → `{typography.body}` description → optional `{button-ghost-dark}` link.

**`feature-card-brand`** — the rare brand-coloured highlight card
- Background `{colors.brand}`, text `{colors.ink}`, padding `{spacing.xl}`, rounded `{rounded.marketing}`. Used at most once per page to anchor the eye.

**`feature-card-light`** — light-section feature tile
- Background `{colors.canvas-light}`, text `{colors.ink}`, padding `{spacing.xl}`, rounded `{rounded.marketing}`, 1px `{colors.hairline}` border.

**`pricing-card`** — standard tier card on the pricing page
- Background `{colors.canvas-light}`, text `{colors.ink}`, padding `{spacing.xl}`, rounded `{rounded.marketing}`, 1px `{colors.hairline}` border.
- Internal stack: tier name (`{typography.heading-md}`) → `{typography.body}` description → tier price (`{pricing-amount}`) → primary CTA (`{button-primary-on-light}`) → feature list (`{typography.body-sm}` bullets with `{colors.success}` checks).

**`pricing-card-featured`** — the featured tier
- Background `{colors.ink}` (full inversion), text `{colors.on-primary}`, otherwise identical layout. The black fill is the badge — no ribbon, no border treatment.

**`pricing-amount`** — the dollar/period display
- Background inherited, text `{colors.ink}` or `{colors.on-primary}`, type `{typography.display-md}`.

**`comparison-table-row`** — the rows of the long feature-comparison table on pricing
- Background `{colors.canvas-light}`, text `{colors.ink}`, type `{typography.body-sm}`, padding `{spacing.md}`, rule `{colors.hairline}` between rows. Cells alternate: feature label (left) + per-tier value (centre, repeating).

**`studio-window`** — the framed Studio app screenshot
- Background `{colors.canvas-soft}`, padding `{spacing.md}`, rounded `{rounded.app-lg}` (6px), 1px `{colors.hairline-soft}` border. Internal: a thin chrome bar with three coloured dots (red/yellow/green macOS-style) in the top-left, then the Studio UI screenshot.

**`brand-dot`** — the small `{colors.brand}` filled circle paired with the `Saniti` wordmark
- Background `{colors.brand}`, size 12px, rounded `{rounded.full}`. Always sits 8px to the left of the wordmark.

### Inputs & Forms

**`text-input`** — light-mode text input (pricing form, contact form)
- Background `{colors.canvas-light}`, text `{colors.ink}`, type `{typography.body}`, rounded `{rounded.app-xs}` (3px), padding `{spacing.sm}` × `{spacing.md}`, height 44px, 1px `{colors.hairline}` border.

**`text-input-dark`** — dark-mode input variant (Studio mockups, content-agent forms)
- Background `{colors.canvas}`, text `{colors.ash}`, type `{typography.body}`, rounded `{rounded.app-xs}`, padding `{spacing.sm}` × `{spacing.md}`, 1px `{colors.ink-soft}` border.

**`text-input-focused`** — focus state
- Background `{colors.canvas-light}`, text `{colors.ink}`, 0 outline + 2px `{colors.link-blue}` ring on focus.

**`textarea`** — multi-line variant
- Background `{colors.canvas}`, text `{colors.ash}`, type `{typography.body}`, rounded `{rounded.app-xs}`, padding `{spacing.xs}` × `{spacing.sm}`, 1px `{colors.ink-soft}` border.

**`badge-neutral`** — small white pill ("New", "Beta")
- Background `{colors.canvas-light}`, text `{colors.ink}`, type `{typography.caption}`, rounded `{rounded.full}`, padding `{spacing.xs}`.

**`badge-filled`** — small black pill
- Background `{colors.ink}`, text `{colors.on-primary}`, type `{typography.caption}`, rounded `{rounded.full}`.

**`alert-banner`** — soft-blue informational notice
- Background `{colors.surface-blue-bg}`, text `{colors.ink}`, type `{typography.body-sm}`, rounded `{rounded.app-lg}`, padding `{spacing.md}`.

### Footer

**`footer`** — the dark terminal surface
- Background `{colors.canvas}`, text `{colors.on-primary}`, padding `{spacing.section}` vertical, `{spacing.lg}` horizontal.
- Layout: 6-column link grid → bottom strip with the `brand-dot` + `Saniti` wordmark right-aligned and copyright/social links left-aligned.

**`footer-eyebrow`** — column heading
- Background `{colors.canvas}`, text `{colors.mute}`, type `{typography.mono-caps}` (small-caps IBM Plex Mono). The mono-eyebrow at the footer is what locks in the technical-trade-journal feel.

**`footer-link`** — link-list items
- Background `{colors.canvas}`, text `{colors.ash}`, type `{typography.caption}`.

### Section-level Components

**`marketing-section-dark`** — full-width dark band
- Background `{colors.canvas}`, text `{colors.on-primary}`, padding `{spacing.section-lg}` vertical.

**`marketing-section-light`** — full-width light band
- Background `{colors.canvas-light}`, text `{colors.ink}`, padding `{spacing.section-lg}` vertical.

**`marketing-section-paper`** — warm-grey alternate light band
- Background `{colors.canvas-paper}`, text `{colors.ink}`, padding `{spacing.section-lg}` vertical.

### Signature Components

**Polarity-Flip Section Rhythm** — the most distinctive part of Saniti's marketing layout. Sections alternate between `{marketing-section-dark}` and `{marketing-section-light}` (or `{marketing-section-paper}`) without any transitional surface. The hard cut is the system's most-used depth cue and what gives the long marketing pages their cinematic, scroll-driven cadence.

**Editorial Display + Mono Eyebrow** — the canonical headline lockup. `{typography.mono-eyebrow}` (IBM Plex Mono, 13px) sits above a 48–112px `{typography.display-md}` to `{typography.display-mega}` headline. The mono caption is what marks the system as developer-platform-aware rather than generic-marketing.

**Studio Window Mockup** — every Studio-product screenshot is framed inside the `{studio-window}` chrome. It is the system's main recurring visual asset and what carries the "this is a real product, not a marketing diagram" signal.

## Do's and Don'ts

### Do
- Run dark-mode marketing sections (`{marketing-section-dark}`) as the brand's default voice; use `{marketing-section-light}` for commercial/comparison surfaces (pricing, integrations matrix).
- Pair every editorial display headline with a `{typography.mono-eyebrow}` label above it — the lockup is signature.
- Reserve `{colors.brand}` for one CTA or accent surface per viewport. The colour's power comes from scarcity.
- Use `{rounded.full}` pills for marketing CTAs and `{rounded.app-*}` 3–6px corners for application-style elements (inputs, Studio mockups). Mixing the two corner languages is intentional — it is what differentiates "marketing" from "product UI" in Saniti's voice.
- Set display headlines (>48px) with the OpenType variants `cv01, cv11, cv12, cv13, ss07` enabled — the alternates are core to the brand letterforms.
- Use the polarity flip (dark → light) as the section divider rather than a horizontal rule or background gradient.
- Pair the brand-dot with the `Saniti` wordmark whenever the wordmark appears at >24px size.

### Don't
- Don't use `{colors.brand}` as a background for dark-mode body sections — it must remain a quiet accent, not a section colour.
- Don't introduce additional accent hues (purple, teal, magenta gradients). Saniti's chromatic story is monochrome plus coral-red.
- Don't apply OpenType variants to body running text — keep them on display sizes only. Mixing modes makes the page feel typographically loud.
- Don't use IBM Plex Mono for body or headline text. Mono is reserved for eyebrows, captions, and small-caps labels.
- Don't add a "Most Popular" badge to the featured pricing tier. The polarity inversion (`{pricing-card-featured}`) is the badge.
- Don't break headings into mixed-weight contrast (light + bold). Every heading is regular weight (400) — let tracking carry the silhouette.
- Don't replace the `brand-dot` with a logo glyph in the navigation. The dot + wordmark pairing is the system's primary identification mark.

## Responsive Behavior

### Breakpoints

| Name | Width | Key Changes |
|---|---|---|
| 2xl | 1640px | Full editorial container; pricing 4-tier grid wide; comparison table single-row layout |
| xl | 1440px | Container slightly tightens; `{typography.display-mega}` may step down to 96px |
| lg | 1200px | Default desktop reading view |
| md | 1100px | Pricing 4-tier grid still 4-up but tier text density tightens |
| sm | 960px | Pricing collapses to 2 columns of tiers; nav primary menu collapses to hamburger above this |
| xs | 768px | Section padding drops from `{spacing.section-lg}` to `{spacing.section}`; display sizes step down universally |
| xxs | 480px | Single-column reading; `{typography.display-mega}` drops to ~64px; pricing tiers stack 1-up; comparison table converts to per-tier accordion |
| xxxs | 376px | Footer 6-column grid collapses to 2-column; brand-dot scales to 10px |

### Touch Targets
- `{button-primary}` is 44px tall — meets WCAG AAA touch target. On mobile the height grows to 48px.
- `{button-secondary-dark}` is 36px on desktop; expands to 44px on mobile to maintain target compliance.
- `{nav-link}` items receive `{spacing.sm}` vertical padding inside the mobile menu, expanding the tap target without resizing the type.

### Collapsing Strategy
- **Nav.** Centred desktop menu collapses into a hamburger that opens an overlay sheet at < 960px; the right-side `{button-primary}` "Get Started Free" stays visible above the hamburger.
- **Hero.** The 112px `{typography.display-mega}` steps down to 64px at xxs; tracking proportionally relaxes (-1.92px instead of -4.48px) to remain readable at smaller absolute sizes.
- **Pricing tier grid.** 4-up → 2-up → 1-up. The featured-tier inversion is preserved across all breakpoints.
- **Comparison table.** At xxs, the wide matrix transforms into a per-tier accordion: tap a tier name, expand its full feature list. The polarity rules (alternating row fills) carry over.
- **Section polarity flips.** Preserved at every breakpoint — the dark/light cadence is structural to the brand voice and never collapses.

### Image Behavior
- `{studio-window}` mockups preserve their `{rounded.app-lg}` framing at every breakpoint. On xxs, they switch to a single-column stack and may horizontal-scroll inside the window if the embedded UI doesn't compress.
- Hero atmospheric backgrounds (when present on content-agent and select feature pages) use a tighter mobile crop so the focal subject stays centred.
- Partner-row wordmarks reflow to a 3-up grid at sm and 2-up at xxs.

## Iteration Guide

1. Focus on ONE component at a time. Start with `{hero-display}`, `{button-primary}`, and `{nav-bar-dark}` — they appear on every dark-mode page and anchor the brand voice.
2. Reference component names and tokens directly (`{colors.brand}`, `{button-primary-on-light}`, `{rounded.full}`) — do not paraphrase or substitute hex values.
3. Run `npx @google/design.md lint DESIGN.md` after edits.
4. Add new variants as separate `components:` entries (`-dark`, `-on-light`, `-featured`). Never bury them inside prose.
5. Default body copy to `{typography.body}`. Reserve `{typography.mono-eyebrow}` and `{typography.mono-caps}` for IBM Plex Mono labels only; never use mono for headlines.
6. Keep `{colors.brand}` scarce — at most one brand-coloured CTA or surface per viewport. If a section already has a `{button-brand}` action, secondary actions step down to `{button-secondary-dark}`.
7. When introducing a new section, start by deciding its polarity (`{marketing-section-dark}` vs light vs paper). The polarity choice drives every other token decision in the section.
