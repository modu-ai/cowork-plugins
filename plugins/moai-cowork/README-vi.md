# 🗿 MoAI-Cowork

**100 công cụ tự tiến hóa — Chuyên gia AI được cá nhân hóa của bạn**

[![Version](https://img.shields.io/badge/version-0.1.0-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

🌐 [한국어](README.md) | [English](README-en.md) | [日本語](README-ja.md) | [Español](README-es.md) | [Français](README-fr.md) | [Deutsch](README-de.md) | [Português](README-pt-BR.md) | [中文](README-zh-CN.md) | [Bahasa](README-id.md) | [हिन्दी](README-hi.md) | [Tiếng Việt](README-vi.md) | [ภาษาไทย](README-th.md) | [Italiano](README-it.md) | [Nederlands](README-nl.md) | [Polski](README-pl.md) | [العربية](README-ar.md) | [עברית](README-he.md)

---

## 🎯 MoAI là gì?

**MoAI-Cowork** là một hệ thống học tập tự động biến AI thành các chuyên gia chuyên biệt cho mỗi lĩnh vực của tổ chức bạn.

- **100 công cụ**: 10 danh mục × 10 lĩnh vực (kế toán, pháp luật, nhân sự, công nghệ, tiếp thị, v.v.)
- **Tự tiến hóa**: Chu kỳ Self-Refine dựa trên phản hồi của người dùng và phân tích kết quả
- **Hồ sơ toàn cầu**: Phản hồi được cá nhân hóa thông qua hồ sơ cá nhân, nhóm và tổ chức
- **Dựa trên plugin**: Tích hợp liền mạch với Claude Code và hệ sinh thái Cowork

### Các tính năng chính

| Chức năng | Mô tả |
|----------|--------|
| **Học tập tự động** | Ghi lại và phân tích hiệu suất ở mỗi tương tác |
| **Chuyên môn lĩnh vực** | Kiến thức thực tế hàng đầu trong mỗi lĩnh vực |
| **Thích ứng văn hóa** | Hỗ trợ các thông lệ kinh doanh toàn cầu và ngôn ngữ |
| **Cập nhật thời gian thực** | Bao gồm luật thuế, quy định và thông tin thị trường mới nhất |
| **Hỗ trợ đa người dùng** | Quản lý hồ sơ cấp độ nhóm và cộng tác |

---

## 📦 Cài đặt

### Yêu cầu
- Claude Code (phiên bản mới nhất)
- Hỗ trợ plugin Cowork

### Bước 1: Thêm plugin vào Cowork
```bash
# Cài đặt qua Cowork CLI (sắp có)
cowork install moai-cowork
```

### Bước 2: Khởi tạo hồ sơ
```bash
moai init
```

### Bước 3: Cấu hình hồ sơ cá nhân
```bash
moai profile --set-personal
```

---

## 🚀 Bắt đầu nhanh

### Chạy truy vấn đầu tiên của bạn

```
@moai Lịch khai báo thuế GTGT của Việt Nam năm 2026 là gì?
```

**Phản hồi**: MoAI tự động:
1. Tải thông tin địa phương hóa của Việt Nam
2. Tham khảo dữ liệu luật thuế 2026
3. Cung cấp lịch GTGT được cá nhân hóa

### Kích hoạt học tập tự động

```
moai learn --feedback "Câu trả lời rất chính xác"
```

MoAI ghi lại phản hồi này để cải thiện các truy vấn tương tự trong tương lai.

---

## 📚 Danh mục 100 công cụ

### 10 Danh mục

#### 1️⃣ Thuế và Kế toán (Tax & Accounting)
- **VN_TAX_001**: Thuế GTGT Việt Nam
- **US_TAX_001**: Thuế thu nhập liên bang Mỹ
- **JP_TAX_001**: Thuế tiêu thụ Nhật Bản
- **UK_TAX_001**: VAT Vương quốc Anh
- **VN_TAX_001**: VAT Việt Nam
- **TH_TAX_001**: VAT Thái Lan
- *(6 thêm)*

#### 2️⃣ Luật lao động và Nhân sự (Labor & HR)
- **VN_HR_001**: Luật lao động Việt Nam
- **US_HR_001**: FLSA và lương tối thiểu
- **JP_HR_001**: Luật lao động Nhật Bản
- **UK_HR_001**: Luật việc làm Anh
- *(6 thêm)*

#### 3️⃣ Dữ liệu và Tuân thủ (Data & Compliance)
- **VN_DATA_001**: Bảo vệ dữ liệu cá nhân
- **US_DATA_001**: CCPA/HIPAA
- **JP_DATA_001**: Luật bảo vệ thông tin cá nhân
- **UK_DATA_001**: UK GDPR
- *(6 thêm)*

#### 4️⃣ Hoạt động kinh doanh (Business Operations)
- **VN_BIZ_001**: Thông lệ kinh doanh Việt Nam
- **US_BIZ_001**: Văn hóa họp mặt Mỹ
- **JP_BIZ_001**: Văn hóa hợp tác Nhật Bản
- *(7 thêm)*

#### 5️⃣ Công nghệ và CNTT (Technology & IT)
- **TECH_001**: Các thực hành tốt nhất phát triển phần mềm
- **TECH_002**: Kiến trúc đám mây
- *(8 thêm)*

#### 6️⃣ Tiếp thị và Bán hàng (Marketing & Sales)
- **MKT_001**: Chiến lược tiếp thị kỹ thuật số
- **MKT_002**: Kỹ thuật bán hàng B2B
- *(8 thêm)*

#### 7️⃣ Tài chính và Đầu tư (Finance & Investment)
- **FIN_001**: Phân tích báo cáo tài chính
- **FIN_002**: Quản lý danh mục đầu tư
- *(8 thêm)*

#### 8️⃣ Pháp luật và Hợp đồng (Legal & Contracts)
- **LEG_001**: Xem xét hợp đồng
- **LEG_002**: Soạn thảo NDA
- *(8 thêm)*

#### 9️⃣ Chiến lược và Lập kế hoạch (Strategy & Planning)
- **STR_001**: Thiết lập chiến lược kinh doanh
- **STR_002**: Cài đặt OKR
- *(8 thêm)*

#### 🔟 Khách hàng và Dịch vụ (Customer & Service)
- **CUS_001**: Phân tích sự hài lòng của khách hàng
- **CUS_002**: Kế hoạch cải thiện dịch vụ
- *(8 thêm)*

---

## 👤 Hệ thống hồ sơ toàn cầu

### Hồ sơ cá nhân (Personal Profile)
```yaml
name: "Nguyễn Văn A"
role: "CFO"
locale: "vi_VN"
industry: "Tài chính"
experience_years: 15
languages: ["Tiếng Việt", "Tiếng Anh"]
```

### Hồ sơ nhóm (Team Profile)
```yaml
team_name: "Nhóm tài chính"
region: "Hà Nội"
size: 8
focus_areas: ["Thuế", "Kế toán"]
```

### Hồ sơ tổ chức (Organization Profile)
```yaml
company_name: "ABC Corporation"
headquarters: "Hà Nội"
founded: 2010
employees: 500
industries: ["Tài chính", "Công nghệ"]
expansion_regions: ["Thái Lan", "Campuchia"]
```

---

## 🔄 Chu kỳ học tập tự động (Self-Refine)

### Luồng học tập

```
1. Chạy truy vấn
   ↓
2. Tạo phản hồi (sử dụng công cụ)
   ↓
3. Thu thập phản hồi của người dùng
   ↓
4. Phân tích kết quả (độ chính xác, mức độ liên quan, tiện ích)
   ↓
5. Cải thiện công cụ (điều chỉnh trọng số)
   ↓
6. Áp dụng vào truy vấn tiếp theo
```

### Các loại phản hồi

| Loại | Mô tả | Tác động |
|------|--------|---------|
| **Tích cực** | "Rất chính xác" | Trọng số công cụ +10% |
| **Một phần** | "Một phần đúng" | Trọng số ±5% |
| **Tiêu cực** | "Sai" | Trọng số công cụ -15% |
| **Tùy chỉnh** | "Cần thêm nội dung về X" | Tăng cường lĩnh vực cụ thể |

---

## 📖 Ví dụ sử dụng

### Ví dụ 1: Tư vấn thuế
```
H: "Quy trình đăng ký bảo hiểm xã hội cho nhân viên mới ở Việt Nam là gì?"
→ Kích hoạt công cụ VN_HR_001
→ Cung cấp thời hạn, tài liệu cần thiết và quy trình
```

### Ví dụ 2: Kinh doanh quốc tế
```
H: "Tôi nên chú ý điều gì trong cuộc họp kinh doanh tại Mỹ?"
→ Kích hoạt công cụ US_BIZ_001
→ Hướng dẫn thích ứng văn hóa, quản lý thời gian, phong cách giao tiếp
```

### Ví dụ 3: Tuân thủ quy định
```
H: "Tôi phải tuân theo những quy trình nào để xử lý dữ liệu khách hàng ở EU?"
→ Kích hoạt công cụ VN_DATA_001 và GDPR liên quan
→ Tuân thủ GDPR, quản lý sự đồng ý, quy trình chuyển dữ liệu
```

---

## 🛠 Cách đóng góp (Contributing)

### 1. Đề xuất công cụ mới
```bash
# Đề xuất lĩnh vực mới
moai contribute --domain "Luật thương mại Việt Nam" --category "legal"
```

### 2. Cải thiện công cụ hiện có
```bash
# Cải thiện dựa trên phản hồi
moai improve DOMAIN_ID --feedback "Cần thêm nội dung"
```

### 3. Thêm địa phương hóa mới
```bash
# Thêm địa phương hóa quốc gia mới
moai add-locale --country "Lào" --code "lo_LA"
```

### 4. Cải thiện tài liệu
- Chỉnh sửa tệp địa phương hóa trong `/skills/moai/references/locale/`
- Gửi Pull Request trên GitHub
- Cập nhật hướng dẫn thích ứng văn hóa

---

## 📋 Lộ trình

### Giai đoạn 1 (Hiện tại)
- [x] Hệ thống công cụ cơ bản
- [x] Hướng dẫn địa phương hóa toàn cầu (7 quốc gia)
- [ ] Triển khai chu kỳ Self-Refine

### Giai đoạn 2 (2026 Q2)
- [ ] 100 công cụ hoàn tất
- [ ] Giao diện đa ngôn ngữ (12 ngôn ngữ)
- [ ] Tính năng cộng tác nhóm

### Giai đoạn 3 (2026 Q3)
- [ ] Cập nhật quy định thời gian thực
- [ ] Quy trình đánh giá AI-to-Human
- [ ] Mẫu dành riêng cho ngành

---

## 📞 Hỗ trợ và liên hệ

- **Tài liệu**: `/skills/moai/references/locale/`
- **GitHub**: (sắp có)
- **Email**: support@moai-cowork.dev

---

## 📄 Giấy phép

Giấy phép MIT - Tự do sử dụng, sửa đổi và phân phối

---

## 🙏 Lời cảm ơn

MoAI-Cowork tiếp tục phát triển với phản hồi từ cộng đồng Claude và Cowork.

---

**MoAI-Cowork: Gặp chuyên gia AI được cá nhân hóa của bạn.**

*Cập nhật lần cuối: 2026-04-04*
