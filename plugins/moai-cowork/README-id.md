# 🗿 MoAI-Cowork

**100 instrumen evolusi diri — Ahli AI yang dipersonalisasi untuk Anda**

[![Version](https://img.shields.io/badge/version-0.1.0-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

🌐 [한국어](README.md) | [English](README-en.md) | [日本語](README-ja.md) | [Español](README-es.md) | [Français](README-fr.md) | [Deutsch](README-de.md) | [Português](README-pt-BR.md) | [中文](README-zh-CN.md) | [Bahasa](README-id.md) | [हिन्दी](README-hi.md) | [Tiếng Việt](README-vi.md) | [ภาษาไทย](README-th.md) | [Italiano](README-it.md) | [Nederlands](README-nl.md) | [Polski](README-pl.md) | [العربية](README-ar.md) | [עברית](README-he.md)

---

## 🎯 Apa itu MoAI?

**MoAI-Cowork** adalah sistem pembelajaran otomatis yang mengubah AI menjadi ahli khusus untuk setiap domain organisasi Anda.

- **100 instrumen**: 10 kategori × 10 domain (akuntansi, hukum, HR, teknologi, pemasaran, dll.)
- **Evolusi diri**: Siklus Self-Refine berdasarkan umpan balik pengguna dan analisis hasil
- **Profil global**: Respons yang dipersonalisasi melalui profil individual, tim, dan organisasi
- **Berbasis plugin**: Integrasi sempurna dengan Claude Code dan ekosistem Cowork

### Fitur Inti

| Fungsi | Deskripsi |
|--------|-----------|
| **Pembelajaran otomatis** | Pencatatan dan analisis kinerja pada setiap interaksi |
| **Spesialisasi domain** | Pengetahuan praktis terdepan di setiap bidang |
| **Adaptasi budaya** | Dukungan praktik bisnis global dan bahasa |
| **Pembaruan real-time** | Termasuk hukum pajak, regulasi, dan informasi pasar terbaru |
| **Dukungan multi-pengguna** | Manajemen profil tingkat tim dan kolaborasi |

---

## 📦 Instalasi

### Persyaratan
- Claude Code (versi terbaru)
- Dukungan plugin Cowork

### Langkah 1: Tambahkan plugin ke Cowork
```bash
# Instalasi melalui Cowork CLI (akan segera tersedia)
cowork install moai-cowork
```

### Langkah 2: Inisialisasi profil
```bash
moai init
```

### Langkah 3: Konfigurasi profil personal
```bash
moai profile --set-personal
```

---

## 🚀 Memulai dengan cepat

### Jalankan kueri pertama Anda

```
@moai Apa jadwal pelaporan pajak pertambahan nilai Indonesia untuk 2026?
```

**Respons**: MoAI secara otomatis:
1. Memuat informasi lokalisasi Indonesia
2. Mengonsultasikan data hukum pajak 2026
3. Menyediakan jadwal PPN yang dipersonalisasi

### Aktifkan pembelajaran otomatis

```
moai learn --feedback "Jawaban sangat akurat"
```

MoAI mencatat umpan balik ini untuk meningkatkan kueri serupa di masa depan.

---

## 📚 Katalog 100 Instrumen

### 10 Kategori

#### 1️⃣ Pajak dan Akuntansi (Tax & Accounting)
- **ID_TAX_001**: Pajak pertambahan nilai Indonesia
- **US_TAX_001**: Pajak penghasilan federal AS
- **JP_TAX_001**: Pajak konsumsi Jepang
- **UK_TAX_001**: VAT Inggris
- **VN_TAX_001**: VAT Vietnam
- **TH_TAX_001**: VAT Thailand
- *(6 lagi)*

#### 2️⃣ Hukum Ketenagakerjaan dan SDM (Labor & HR)
- **ID_HR_001**: Hukum ketenagakerjaan Indonesia
- **US_HR_001**: FLSA dan upah minimum
- **JP_HR_001**: Hukum ketenagakerjaan Jepang
- **UK_HR_001**: Hukum ketenagakerjaan Inggris
- *(6 lagi)*

#### 3️⃣ Data dan Kepatuhan (Data & Compliance)
- **ID_DATA_001**: Perlindungan data pribadi
- **US_DATA_001**: CCPA/HIPAA
- **JP_DATA_001**: Undang-Undang Perlindungan Informasi Pribadi
- **UK_DATA_001**: UK GDPR
- *(6 lagi)*

#### 4️⃣ Operasi Bisnis (Business Operations)
- **ID_BIZ_001**: Praktik bisnis Indonesia
- **US_BIZ_001**: Budaya pertemuan AS
- **JP_BIZ_001**: Budaya kolaborasi Jepang
- *(7 lagi)*

#### 5️⃣ Teknologi dan IT (Technology & IT)
- **TECH_001**: Praktik terbaik pengembangan perangkat lunak
- **TECH_002**: Arsitektur cloud
- *(8 lagi)*

#### 6️⃣ Pemasaran dan Penjualan (Marketing & Sales)
- **MKT_001**: Strategi pemasaran digital
- **MKT_002**: Teknik penjualan B2B
- *(8 lagi)*

#### 7️⃣ Keuangan dan Investasi (Finance & Investment)
- **FIN_001**: Analisis laporan keuangan
- **FIN_002**: Manajemen portofolio investasi
- *(8 lagi)*

#### 8️⃣ Hukum dan Kontrak (Legal & Contracts)
- **LEG_001**: Peninjauan kontrak
- **LEG_002**: Penyusunan NDA
- *(8 lagi)*

#### 9️⃣ Strategi dan Perencanaan (Strategy & Planning)
- **STR_001**: Penetapan strategi bisnis
- **STR_002**: Pengaturan OKR
- *(8 lagi)*

#### 🔟 Pelanggan dan Layanan (Customer & Service)
- **CUS_001**: Analisis kepuasan pelanggan
- **CUS_002**: Rencana peningkatan layanan
- *(8 lagi)*

---

## 👤 Sistem Profil Global

### Profil Pribadi (Personal Profile)
```yaml
name: "Budi Santoso"
role: "CFO"
locale: "id_ID"
industry: "Keuangan"
experience_years: 15
languages: ["Indonesia", "Inggris"]
```

### Profil Tim (Team Profile)
```yaml
team_name: "Tim Keuangan"
region: "Jakarta"
size: 8
focus_areas: ["Pajak", "Akuntansi"]
```

### Profil Organisasi (Organization Profile)
```yaml
company_name: "ABC Corporation"
headquarters: "Jakarta"
founded: 2010
employees: 500
industries: ["Keuangan", "Teknologi"]
expansion_regions: ["Singapura", "Malaysia"]
```

---

## 🔄 Siklus Pembelajaran Diri (Self-Refine)

### Alur pembelajaran

```
1. Jalankan kueri
   ↓
2. Buat respons (menggunakan instrumen)
   ↓
3. Kumpulkan umpan balik pengguna
   ↓
4. Analisis hasil (akurasi, relevansi, utilitas)
   ↓
5. Tingkatkan instrumen (sesuaikan bobot)
   ↓
6. Terapkan ke kueri berikutnya
```

### Jenis umpan balik

| Jenis | Deskripsi | Dampak |
|------|-----------|--------|
| **Positif** | "Sangat akurat" | Bobot instrumen +10% |
| **Parsial** | "Sebagian benar" | Bobot ±5% |
| **Negatif** | "Salah" | Bobot instrumen -15% |
| **Khusus** | "Butuh lebih banyak konten tentang X" | Penguatan area spesifik |

---

## 📖 Contoh Penggunaan

### Contoh 1: Konsultasi pajak
```
T: "Apa prosedur pendaftaran kontribusi untuk karyawan baru di Indonesia?"
→ Aktifkan instrumen ID_HR_001
→ Sediakan batas waktu, dokumen diperlukan, dan prosedur
```

### Contoh 2: Bisnis internasional
```
T: "Apa yang perlu diperhatikan dalam pertemuan bisnis AS?"
→ Aktifkan instrumen US_BIZ_001
→ Panduan adaptasi budaya, manajemen waktu, gaya komunikasi
```

### Contoh 3: Kepatuhan regulasi
```
T: "Prosedur apa yang harus saya ikuti untuk memproses data pelanggan di UE?"
→ Aktifkan instrumen ID_DATA_001 dan GDPR terkait
→ Kepatuhan GDPR, manajemen persetujuan, prosedur transfer
```

---

## 🛠 Cara Berkontribusi (Contributing)

### 1. Usulkan instrumen baru
```bash
# Usulkan domain baru
moai contribute --domain "Hukum komersial Indonesia" --category "legal"
```

### 2. Tingkatkan instrumen yang ada
```bash
# Peningkatan berdasarkan umpan balik
moai improve DOMAIN_ID --feedback "Konten tambahan diperlukan"
```

### 3. Tambahkan lokalisasi baru
```bash
# Tambahkan lokalisasi negara baru
moai add-locale --country "Malaysia" --code "ms_MY"
```

### 4. Tingkatkan dokumentasi
- Edit file lokalisasi di `/skills/moai/references/locale/`
- Kirim Pull Request di GitHub
- Perbarui panduan adaptasi budaya

---

## 📋 Peta Jalan

### Fase 1 (Saat Ini)
- [x] Sistem instrumen dasar
- [x] Panduan lokalisasi global (7 negara)
- [ ] Implementasi siklus Self-Refine

### Fase 2 (2026 Q2)
- [ ] 100 instrumen selesai
- [ ] Antarmuka multibahasa (12 bahasa)
- [ ] Fitur kolaborasi tim

### Fase 3 (2026 Q3)
- [ ] Pembaruan regulasi real-time
- [ ] Proses review AI-ke-Manusia
- [ ] Template spesifik industri

---

## 📞 Dukungan dan Kontak

- **Dokumentasi**: `/skills/moai/references/locale/`
- **GitHub**: (akan segera hadir)
- **Email**: support@moai-cowork.dev

---

## 📄 Lisensi

Lisensi MIT - Bebas untuk digunakan, dimodifikasi, dan didistribusikan

---

## 🙏 Ucapan Terima Kasih

MoAI-Cowork terus berkembang dengan umpan balik dari komunitas Claude dan Cowork.

---

**MoAI-Cowork: Temui ahli AI yang dipersonalisasi untuk Anda.**

*Terakhir diperbarui: 2026-04-04*
