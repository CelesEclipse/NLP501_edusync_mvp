---
marp: true
theme: uncover
class: invert
paginate: true
header: 'EduSync · Đồ Án NLP501 · Master of Software Engineering'
footer: 'Nhánh Git: edusync-v2 · Đại Học MSE · Tháng 11/2026'
style: |
  section {
    background: radial-gradient(circle at 50% 30%, #151d30 0%, #0b0f19 80%);
    color: #f3f4f6;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, sans-serif;
    padding: 40px 60px;
    font-size: 24px;
    line-height: 1.5;
  }
  h1 {
    color: #38bdf8;
    font-size: 1.6em;
    font-weight: 800;
    margin-bottom: 0.2em;
  }
  h2 {
    color: #94a3b8;
    font-size: 1.0em;
    font-weight: 500;
    margin-top: 0;
    margin-bottom: 0.8em;
  }
  .speaker-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 0.7em;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
  }
  .sp1 { background: rgba(6, 182, 212, 0.2); color: #06b6d4; border: 1px solid #06b6d4; }
  .sp2 { background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid #10b981; }
  .sp3 { background: rgba(168, 85, 247, 0.2); color: #a855f7; border: 1px solid #a855f7; }
  .sp4 { background: rgba(245, 158, 11, 0.2); color: #f59e0b; border: 1px solid #f59e0b; }
  .grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    text-align: left;
    font-size: 0.82em;
  }
  .box {
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 16px 20px;
  }
  ul {
    margin: 8px 0 0 20px;
    padding: 0;
  }
  li {
    margin-bottom: 6px;
  }
  code {
    background: #1e293b;
    color: #38bdf8;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.88em;
  }
  table {
    font-size: 0.72em;
    width: 100%;
    margin-top: 10px;
  }
  th {
    background: #1e293b;
    color: #38bdf8;
    padding: 6px 10px;
  }
  td {
    padding: 6px 10px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
  }
---

<!-- Slide 01 -->
<div class="speaker-badge sp1">👤 THÀNH VIÊN 1 · PROJECT LEAD (00:00 - 04:30)</div>

# EDUSYNC: Multimodal Lecture Alignment & Pedagogical Intelligence
## Nền tảng Đồng bộ Đa phương thức và Phân tích Sư phạm Bài giảng Trực tuyến

<div class="grid-2">
<div class="box">

### 🎓 Thông Tin Đề Tài & Hội Đồng
* **Môn học:** Xử lý Ngôn ngữ Tự nhiên Nâng cao (NLP501)
* **Chương trình:** Cao học Kỹ thuật Phần mềm (MSE)
* **Thời lượng:** 20 phút báo cáo + 10 phút Q&A
* **Mã nguồn:** Nhánh Git `edusync-v2` (4.950 LOC)
</div>

<div class="box">

### 👥 Phân Công Nhóm 4 Thành Viên
* **TV 1:** Đặt vấn đề, Đặc tả SRS & Kiến trúc 4 tầng
* **TV 2:** ASR Whisper Prompting & Monotonic DP
* **TV 3:** CEFR Lexicon, Dense Embeddings & ERRANT
* **TV 4:** Teacher Dashboard, Live Demo & QA/QC 45 Tests
</div>
</div>

---

<!-- Slide 02 -->
<div class="speaker-badge sp1">👤 THÀNH VIÊN 1 · ĐẶT VẤN ĐỀ & DẪN CHỨNG NGHIÊN CỨU</div>

# Bối Cảnh & 3 Rào Cản Khiến Học Viên Bỏ Cuộc Khi Ôn Thi
## Dẫn chứng nghiên cứu quốc tế về hiệu ứng bỏ dở video dài và tâm lý "ngại hỏi giáo viên"

<div class="grid-2">
<div class="box" style="border-top: 3px solid #ef4444;">

### 🛑 Dễ Bỏ Cuộc & Tâm Lý Ngại Hỏi Giáo Viên
* **Dễ bỏ dở video dài (Guo et al., MIT — ACM L@S 2014):** Qua 6,9 triệu phiên xem, thời gian tập trung trung vị chỉ đạt **tối đa 6 phút**; tới **69% học viên bỏ qua bài tập** sau video dài và **61% thao tác tua** chỉ để mò điểm chuyển bài (*Kim et al., 2014*).
* **Ngại hỏi giáo viên (Horwitz et al., 1986; Nguyen, 2025):** Sợ bị đánh giá (*Fear of Negative Evaluation*) & sợ "mất mặt" trước lớp khiến học viên không dám bật mic hỏi lại câu làm sai.
* **Giảm tự tin & quyết tâm:** Câu trả lời sai trong chat bị trôi mất, làm giảm *Self-Efficacy* (*Farmani et al., 2017*).
</div>

<div class="box" style="border-top: 3px solid #f59e0b;">

### ⚠️ Điểm Mù Của Giáo Viên & Giải Pháp EduSync
* **Không nhận biết được "học viên im lặng":** Vì học viên ngại hỏi trên lớp, giáo viên không biết cả lớp đang vướng ở công thức nào.
* **Thiếu chỉ số TTT/STT & Bản đồ lỗi:** Không thống kê được lỗi chuyển di ngôn ngữ (*L1 Transfer*) trong khung chat.
* **💡 Giải pháp EduSync:** Chia nhỏ video thành nút câu hỏi **< 2 phút**, tự động nối **Câu làm sai ↔ Lý thuyết gốc** & sửa lỗi chat **ẩn danh bằng tiếng Việt** giúp tăng quyết tâm ôn thi TOEIC/IELTS.
</div>
</div>

---

<!-- Slide 03 -->
<div class="speaker-badge sp1">👤 THÀNH VIÊN 1 · MỤC TIÊU ĐỀ TÀI</div>

# Mục Tiêu Đề Tài & Giá Trị Cốt Lõi
## Tháo gỡ rào cản tâm lý "ngại hỏi thầy cô" và tăng quyết tâm chinh phục TOEIC / IELTS

<div class="grid-2">
<div class="box" style="border-left: 4px solid #06b6d4;">

### 🎯 TRỤ CỘT 1: HỌC VIÊN TỰ CHỦ & TỰ TIN
* **Click-to-Seek (< 2 phút/câu):** Bấm câu hỏi $\to$ video tua ngay đến đúng giây cô chữa (khắc phục ngưỡng bỏ cuộc 6 phút).
* **Thay thế việc ngại hỏi giáo viên:** Bấm badge ngữ pháp trên câu sai $\leftrightarrow$ tự nhảy ngược về lý thuyết gốc đầu giờ.
* **Từ vựng CEFR (A1–C2) & Audio 1.5s:** Nghe phát âm giọng thật của giáo viên theo mục tiêu band điểm.
* **Sửa lỗi GEC Ẩn danh ($S_1..S_N$):** Giải thích lỗi tiếng Việt không phán xét, tăng *Self-Efficacy*.
</div>

<div class="box" style="border-left: 4px solid #f59e0b;">

### 📊 TRỤ CỘT 2: TRỢ LÝ SƯ PHẠM
* **Đo lường thời lượng nói (TTT/STT):** Định lượng chính xác tỷ lệ giảng viên vs học sinh.
* **Bản đồ lỗi sai ERRANT:** Trực quan hóa các điểm nghẽn ngữ pháp dù học viên ngại không hỏi trực tiếp.
* **Cảnh báo Weakest Concept:** Chỉ ra chủ điểm lý thuyết học sinh làm sai nhiều nhất.
* **Kế hoạch Hành động 3 bước:** Đề xuất warm-up và bài tập củng cố buổi sau.
</div>
</div>

---

<!-- Slide 04 -->
<div class="speaker-badge sp1">👤 THÀNH VIÊN 1 · ĐẶC TẢ SRS & KIẾN TRÚC</div>

# Đặc Tả Yêu Cầu SRS & Kiến Trúc 4 Tầng
## Mô hình đường ống phân tầng khép kín tuân thủ chuẩn phần mềm IEEE 830

```
┌────────────────────────────────────────────────────────────────────────┐
│ TẦNG 1: INGESTION (Video MP4, Audio M4A, Chat Zoom TXT, Apple OCR)    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ TẦNG 2: ALIGNMENT (Whisper large-v3-turbo, Screen Hints, Monotonic DP) │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ TẦNG 3: NLP CORE (Dense Embeddings MiniLM, Cosine, CEFR, ERRANT GEC)   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ TẦNG 4: PRESENTATION (Web Demo SPA, Omnibox Search, Teacher Analytics) │
└────────────────────────────────────────────────────────────────────────┘
```
👉 *Chuyển giao: Kính mời Thành viên 2 trình bày Tầng thu nhận dữ liệu và Căn chỉnh thời gian.*

---

<!-- Slide 05 -->
<div class="speaker-badge sp2">👤 THÀNH VIÊN 2 · MULTIMODAL ALIGNMENT (04:30 - 09:00)</div>

# Thách Thức Âm Thanh Đa Ngữ & Whisper ASR
## Hiện tượng chuyển mã ngôn ngữ (Code-Switching) và giải pháp nhận dạng

<div class="grid-2">
<div class="box">

### 🗣️ Code-Switching Trong Lớp Ngoại Ngữ
* Giáo viên liên tục xen kẽ tiếng Việt và tiếng Anh:
  > *"Câu 3 này dùng participle -ing vì mang nghĩa chủ động, còn cảm xúc là interested..."*
* ASR thông thường dễ nhầm lẫn bảng chữ cái, nuốt dấu thanh hoặc biến dạng thuật ngữ.
* Nguy cơ Word Error Rate (WER) tăng vọt.
</div>

<div class="box">

### ⚡ Giải Pháp Whisper `large-v3-turbo`
* Mô hình Transformer 680k giờ đa ngữ chạy local.
* Cross-attention weights cho timestamp từng từ.
* **Heuristic mật độ dấu thanh tiếng Việt:**
  $$\text{Density}_{\text{vi}}(W) = \frac{\sum_{w} \mathbb{I}(w \text{ có dấu})}{|W|}$$
  (Density > 0.3: `vi`, Density == 0: `en`, còn lại: `mixed`).
</div>
</div>

---

<!-- Slide 06 -->
<div class="speaker-badge sp2">👤 THÀNH VIÊN 2 · CONTEXTUAL PROMPTING</div>

# Giảm Ảo Giác ASR Bằng Bơm Ngữ Cảnh OCR
## Kỹ thuật Screen Hints Contextual Prompting định hướng kênh giải mã

<div class="grid-2">
<div class="box">

### 🔄 Quy Trình Screen Hints Prompting
1. **Bắt Keyframe video:** Qua thuật toán Pixel Diff.
2. **Apple Vision OCR:** Trích xuất văn bản trên slide.
3. **Lọc từ vựng:** Khử stopwords và ký tự rác.
4. **Bơm vào Whisper `initial_prompt`:**
   ```python
   prompt = "Từ vựng màn hình: " + ", ".join(hints)
   model.transcribe(audio, initial_prompt=prompt)
   ```
</div>

<div class="box">

### 📊 Hiệu Quả Thực Nghiệm
* **WER thuật ngữ giảm từ 18.4% $\to$ 9.2%**
* **Triệt tiêu ảo giác (Hallucination):** Bộ giải mã ưu tiên token xuất hiện trên slide.
* **Bảo vệ từ đồng âm xuyên ngôn ngữ:** Kích hoạt danh mục `VI_HOMOPHONES` (loại bỏ nhầm lẫn *"an", "may", "can"*).
</div>
</div>

---

<!-- Slide 07 -->
<div class="speaker-badge sp2">👤 THÀNH VIÊN 2 · MONOTONIC DP ALIGNMENT</div>

# Trích Xuất Đề Bài & Thuật Toán Monotonic DP
## Ràng buộc quy hoạch động chống đảo ngược thời gian và lọc khẩu lệnh nhiễu

<div class="grid-2">
<div class="box">

### ⚠️ Thách Thức Khi Căn Chỉnh
* Giáo viên thường nói câu gây nhiễu: *"Hôm trước câu 1 ta làm rồi..."* hoặc *"Xem lại câu 2 đi"* khi đang chữa câu 5.
* Lời giảng trễ 2–5s so với chuyển slide.
* Nhầm lẫn *"page 1"*, *"text 1"* thành *"câu 1"*.
</div>

<div class="box">

### 📐 Thuật Toán Monotonic DP
* **Regex Negative Lookbehind:**
  `(?<!page\s)(?<!text\s)\b(?:number|câu)\s*(\d+)\b`
* **Ràng buộc toán học đơn điệu:**
  $$\forall k < j \implies t_{\text{start}}^{(k)} < t_{\text{start}}^{(j)}$$
* **Cửa sổ tìm kiếm động:** 120s buffer giữa các câu hỏi liên tiếp.
</div>
</div>

$$\text{Score}(k, t) = 25.0 \cdot \text{Trigger}(k, t) + 1.5 \cdot \text{Overlap}(k, t) - \text{Penalty}(t \le t_{k-1})$$

---

<!-- Slide 08 -->
<div class="speaker-badge sp2">👤 THÀNH VIÊN 2 · KẾT QUẢ ĐỊNH LƯỢNG</div>

# Kết Quả Căn Chỉnh Bài Tập (34/34 Câu Hỏi)
## Đạt Recall tuyệt đối 100% trên bài giảng TOEIC Starter Unit 4 (63 phút video)

| Chỉ Số Đánh Giá | Kết Quả Đạt Được | Ý Nghĩa Thực Tiễn |
| :--- | :---: | :--- |
| **Recall Căn Chỉnh** | **34 / 34 câu (100%)** | Tìm ra chính xác toàn bộ câu hỏi trên slide |
| **Precision** | **97.1%** | Triệt tiêu hoàn toàn mốc thời gian giả |
| **Sai số biên thời gian** | **$\Delta t \le 1.8$ giây** | Tua video đón đầu trước lúc cô bắt đầu đọc đề |
| **Dữ liệu rỗng** | **0 empty stems** | 100% câu hỏi có đầy đủ đề bài và lựa chọn A/B/C/D |

```json
{
  "id": "q1", "number": 1, "stem": "The seminar was very [interest/interesting/interested]...",
  "start": 181.42, "end": 245.10, "trigger_text": "bây giờ cô cùng các em chữa câu số 1 nhé"
}
```
👉 *Chuyển giao: Kính mời Thành viên 3 trình bày Kỹ thuật NLP cốt lõi & Nhúng Vector.*

---

<!-- Slide 09 -->
<div class="speaker-badge sp3">👤 THÀNH VIÊN 3 · CORE NLP & LEXICON (09:00 - 14:00)</div>

# Phân Loại Từ Vựng CEFR & Audio Clip 1.5s
## Chuẩn hóa hình thái Lemmatization và trích xuất ngân hàng từ vựng giọng thật

<div class="grid-2">
<div class="box">

### 📚 Quy Trình Phân Bậc Từ Vựng
* **Lemmatization 2 lớp:**
  * Lớp quy tắc: `-s`, `-es`, `-ed`, `-ing`.
  * Lớp bất quy tắc: `wrote/written` $\to$ `write`.
* **Từ điển chuẩn CEFR-J:** 8.845 mục từ (A1 đến C2).
* **Bilingual IE:** Trích nghĩa tiếng Việt trực tiếp từ lời giảng (*"TargetWord + là/nghĩa là + Meaning"*).
</div>

<div class="box">

### 🔊 Cắt Audio Clip 1.5s Giọng Thật
* Không dùng robot Text-to-Speech vô hồn.
* Tự động định vị timestamp và cắt 1.5s audio bằng `ffmpeg` đúng ngữ điệu giáo viên.
* **79 Từ Vựng Trọng Tâm Trích Xuất:**
  * A1: 28 | A2: 19 | B1: 18 | B2: 12 | C1: 2
  * Kèm 79 file audio `.mp3` chất lượng cao.
</div>
</div>

---

<!-- Slide 10 -->
<div class="speaker-badge sp3">👤 THÀNH VIÊN 3 · DENSE EMBEDDINGS</div>

# Vấn Đề Của Keyword Matching & Dense Embeddings
## Sự bất lực của so khớp từ khóa và bước nhảy vọt sang không gian vector

<div class="grid-2">
<div class="box" style="border-top: 3px solid #ef4444;">

### ❌ Sự Thất Bại Của Keyword / TF-IDF
* **Câu hỏi số 1:**
  > *"The seminar was very [interest / interesting / interested]..."*
* **Lý thuyết bài giảng:**
  > *"Participles as Adjectives (Phân từ làm tính từ)"*
* **Hiện tượng Vocabulary Mismatch:** Không có bất kỳ từ nào trùng nhau!
* BM25 / TF-IDF trả về $\text{Score} = 0$.
</div>

<div class="box" style="border-top: 3px solid #a855f7;">

### 💡 Giải Pháp: Dense Semantic Embeddings
* Ánh xạ câu hỏi và lý thuyết vào cùng một **không gian vector liên tục $\mathbb{R}^d$**.
* Mô hình Transformer hiểu được quan hệ ngữ nghĩa tiềm ẩn:
  `interesting, bored, excited` $\sim$ `participle, adjective`.
* Khoảng cách hình học phản ánh mức độ tương đồng khái niệm trừu tượng.
</div>
</div>

---

<!-- Slide 11 -->
<div class="speaker-badge sp3">👤 THÀNH VIÊN 3 · COSINE SIMILARITY</div>

# Không Gian Vector `all-MiniLM-L6-v2`
## Cơ sở toán học, phân ngưỡng tin cậy và tốc độ thực thi trên Apple Silicon

<div class="grid-2">
<div class="box">

### 📐 Biểu Diễn Toán Học
* Vector câu hỏi: $\mathbf{u} \in \mathbb{R}^{384}$
* Vector chủ điểm lý thuyết: $\mathbf{v}_j \in \mathbb{R}^{384}$
* **Độ tương đồng Cosine:**
  $$\text{Sim}(\mathbf{u}, \mathbf{v}_j) = \frac{\mathbf{u} \cdot \mathbf{v}_j}{\|\mathbf{u}\|_2 \|\mathbf{v}_j\|_2}$$
* Chọn chủ điểm: $\hat{j} = \arg\max_j \text{Sim}(\mathbf{u}, \mathbf{v}_j)$
</div>

<div class="box">

### ⚡ Phân Ngưỡng & Hiệu Năng
* **Phân ngưỡng tin cậy (Confidence):**
  * `HIGH` ($\ge 0.25$): Gán badge tím + liên kết 2 chiều.
  * `MEDIUM` ($0.15 \le \text{Sim} < 0.25$): Gợi ý xem lại.
  * `LOW` ($< 0.15$): Từ chối gán nhãn giả.
* **Tốc độ suy luận:** **4.2ms / câu hỏi** trên Mac Metal GPU, hoàn toàn offline.
</div>
</div>

---

<!-- Slide 12 -->
<div class="speaker-badge sp3">👤 THÀNH VIÊN 3 · ERRANT GEC CHAT</div>

# Chẩn Đoán Lỗi Ngữ Pháp GEC Từ Zoom Chat
## Bắt 6 lỗi chuyển di ngôn ngữ (L1 Transfer) kinh điển theo chuẩn ERRANT quốc tế

| Mã Lỗi ERRANT | Câu Chat Học Sinh | Câu Sửa Chuẩn Sư Phạm | Giải Thích Tiếng Việt |
| :--- | :--- | :--- | :--- |
| `U:VERB:BE` | *"I am agree with A"* | *"I agree with A"* | 'Agree' là V thường, không đi với 'to be'. |
| `R:ADJ:PARTICIPLE` | *"I am confusing"* | *"I am confused"* | Miêu tả cảm xúc người phải dùng đuôi **-ed**. |
| `M:VERB:AUX` | *"Why we use -ing?"* | *"Why do we use -ing?"* | Câu hỏi WH- cần trợ động từ 'do/does'. |
| `R:VERB:FORM` | *"have it clean"* | *"have it cleaned"* | Causative bị động: `have + O + V3/ed`. |
| `U:PREP` | *"should to increase"* | *"should increase"* | Sau modal verb 'should' dùng V nguyên thể. |
| `R:VERB:SVA` | *"it make me cry"* | *"it makes me cry"* | Chủ ngữ ngôi 3 số ít 'it' động từ thêm 's/es'. |

🔒 *Bảo mật FERPA/GDPR: Mã hóa tên thật học sinh thành $S_1, S_2, \dots, S_N$.*

---

<!-- Slide 13 -->
<div class="speaker-badge sp3">👤 THÀNH VIÊN 3 · HYBRID NEURAL IE</div>

# Trích Xuất Thông Tin Cấu Trúc (Bilingual IE)
## Kết hợp Gemini 3.5 Flash-Lite Structured Outputs và bộ luật dự phòng Fallback

<div class="grid-2">
<div class="box">

### 🤖 Primary Path: Gemini Flash-Lite
* Sử dụng Prompt với JSON Schema nghiêm ngặt.
* Bóc tách 4 chủ điểm ngữ pháp trọng tâm:
  * Tiêu đề & Công thức toán học ngữ pháp.
  * Giải thích cơ chế bằng tiếng Việt.
  * Cặp ví dụ minh họa và mốc video (timestamp).
  * Mẹo làm bài thi TOEIC (Exam Tips).
</div>

<div class="box">

### 🛡️ Fallback Path: Rule-based Regex
* Tự động kích hoạt khi offline hoặc hết quota API.
* Quét biểu thức chính quy trích xuất bộ khung lý thuyết cơ bản.
* **Đảm bảo tính sẵn sàng 100%:** Phần mềm không bao giờ bị gián đoạn hay crash.
</div>
</div>

👉 *Chuyển giao: Kính mời Thành viên 4 trình bày Báo cáo sư phạm, Live Demo và QA/QC.*

---

<!-- Slide 14 -->
<div class="speaker-badge sp4">👤 THÀNH VIÊN 4 · TEACHER DASHBOARD (14:00 - 20:00)</div>

# Báo Cáo Sư Phạm Đa Chiều (Teacher Dashboard)
## Hội tụ toàn bộ dữ liệu NLP thành Bảng điều khiển trợ lý sư phạm thông minh

<div class="grid-2">
<div class="box">

### ⏱️ 1. Thời Lượng Nói (TTT vs STT)
* **TTT:** 100% (Giáo viên nói qua mic)
* **STT:** 0% (Học sinh chat qua Zoom)
* *Khuyến nghị:* Gọi học sinh bật mic phát biểu ở các bài đọc Part 6 dài.

### 📊 2. Bản Đồ Lỗi Sai (Error Heatmap)
* `R:ADJ:PARTICIPLE`: **28.6%** (Sai nhiều nhất)
* `M:VERB:AUX`: **14.3%** | `U:VERB:BE`: **14.3%**
</div>

<div class="box">

### ⚠️ 3. Điểm Nghẽn Lớp Học (Weakest Concept)
* Chủ điểm: **Tính từ phân từ bổ nghĩa danh từ** (4 câu làm sai tập trung ở câu 1, 2, 7).

### 📋 4. Action Plan 3 Bước Buổi Sau
1. Khởi động 5 phút bằng 3 câu trắc nghiệm phân biệt đuôi `-ing` và `-ed`.
2. Nhắc lại công thức nhờ vả `have/get + O + V3/ed`.
3. Dành 3–5 phút cho học sinh tự tìm từ khóa Part 6.
</div>
</div>

---

<!-- Slide 15 -->
<div class="speaker-badge sp4">👤 THÀNH VIÊN 4 · LIVE DEMO SHOWCASE</div>

# Trình Diễn Sản Phẩm Thực Tế (Live Web Demo)
## Kịch bản 5 bước thao tác trực tiếp tại http://localhost:8000/

<div class="grid-2">
<div class="box">

* **Bước 1 — Căn chỉnh Video:** Bấm câu hỏi trên tab *Exercises* $\to$ video tua mượt mà tới đúng giây chữa bài.
* **Bước 2 — Liên kết Khái niệm:** Bấm `📖 Lý thuyết (08:13)` $\to$ video nhảy về phút thứ 8 lúc cô giảng công thức, mở tab *Grammar*.
* **Bước 3 — Audio Từ vựng 1.5s:** Vào tab *Vocabulary*, bấm loa 🔊 $\to$ nghe phát âm giọng thật của giáo viên.
</div>

<div class="box">

* **Bước 4 — Sửa lỗi Chat GEC:** Vào tab *Chat & Feedback* $\to$ xem câu chat đã ẩn danh, mã lỗi ERRANT và câu sửa tiếng Việt.
* **Bước 5 — Dashboard & Omnibox:** Mở tab *Analytics* xem TTT/STT; bấm `Cmd+K` gõ *"participle"* tra cứu tức thì toàn bài.
</div>
</div>

🔗 **Link Web Demo:** [http://localhost:8000/](http://localhost:8000/) *(Độ trễ < 5ms trên trình duyệt)*

---

<!-- Slide 16 -->
<div class="speaker-badge sp4">👤 THÀNH VIÊN 4 · QA/QC PLAN</div>

# Kế Hoạch QA/QC & Kết Quả Kiểm Thử (45/45 Tests)
## Kiểm soát chất lượng toàn diện theo mô hình Test-Driven Development (TDD)

<div class="grid-2">
<div class="box">

### 🧪 10 Bộ Unit Tests Bao Phủ Toàn Bộ
* `test_wer.py` (5 tests): Khoảng cách Levenshtein
* `test_text_lang.py` (3 tests): Nhận diện dấu thanh
* `test_screen_hints.py` (4 tests): Lọc stopwords OCR
* `test_exercises.py` (4 tests): Monotonic DP
* `test_vocab.py` (8 tests): CEFR & Lemmatization
* `test_feedback.py` (10 tests): FERPA & ERRANT
* `test_neural_ie.py` (4 tests): Schema & Fallback
* `test_concept_link.py` (2 tests): Dense Embeddings
* `test_teacher_analytics.py` (2 tests): TTT & Action Plan
* `test_diarize.py` (3 tests): Phân vai Teacher/Student
</div>

<div class="box" style="text-align: center; justify-content: center;">

### 🎯 TỔNG KẾT KIỂM THỬ
# 45 / 45
### 100% UNIT TESTS PASSED
* Thời gian chạy: **7.5 giây**
* Tự động hóa hoàn toàn với `pytest -v`
* Nhánh Git: `edusync-v2`
</div>
</div>

---

<!-- Slide 17 -->
<div class="speaker-badge sp4">👤 THÀNH VIÊN 4 · ĐÁNH GIÁ & PHÁT TRIỂN</div>

# Đóng Góp Học Thuật, Hạn Chế & Hướng Phát Triển
## Nhìn nhận khách quan về đồ án và lộ trình mở rộng quy mô trong tương lai

<div class="grid-2">
<div class="box" style="border-top: 3px solid #10b981;">

### 🌟 Đóng Góp Nổi Bật
* Hiện thực hóa mô hình Multimodal Learning âm thanh + thị giác + văn bản.
* Đưa nghiên cứu NLP lý thuyết (Dense Embeddings, ERRANT) giải quyết trực tiếp nỗi đau giáo dục.
* Xây dựng bộ tài liệu chuẩn mực IEEE/ACM trong thư mục `docs/` (8 chuyên đề).
</div>

<div class="box" style="border-top: 3px solid #ef4444;">

### ⚠️ Hạn Chế & Hướng Mở Rộng
* **Hạn chế:** Tối ưu tốt nhất trên Mac Metal; hiện tập trung vào trắc nghiệm TOEIC.
* **Hướng phát triển:**
  * Mở rộng sang bài đọc hiểu dài (IELTS Reading Part 7) và kỹ năng Nói (Speaking).
  * Tích hợp vector database phân tán (Milvus/Qdrant) cho quy mô toàn trường.
  * Xuất Flashcard Anki kèm audio cắt sẵn.
</div>
</div>

---

<!-- Slide 18 -->
<div class="speaker-badge sp4">👤 THÀNH VIÊN 4 · TỔNG KẾT & Q&A</div>

# Tổng Kết & Bắt Đầu Phiên Hỏi - Đáp (Q&A)
## Trân trọng cảm ơn Thầy/Cô Hội đồng và các bạn học viên đã chú ý lắng nghe!

<div class="box" style="text-align: center; margin: 20px 0;">

> *"EduSync không thay thế người thầy, mà trao quyền cho người thầy và học sinh bằng sức mạnh của Trí tuệ Nhân tạo và Xử lý Ngôn ngữ Tự nhiên."*

**Branch Git:** `edusync-v2` &nbsp;|&nbsp; **Docs:** `docs/01` đến `docs/08` &nbsp;|&nbsp; **Demo:** `http://localhost:8000/`
</div>

### 💬 Cả 4 thành viên xin sẵn sàng lắng nghe ý kiến nhận xét và giải đáp các câu hỏi phản biện từ Hội đồng!

