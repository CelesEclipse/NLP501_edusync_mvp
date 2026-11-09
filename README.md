# EduSync: Nền tảng Đồng bộ Đa phương thức & Phân tích Sư phạm cho Bài giảng Tiếng Anh (TOEIC & IELTS)

**EduSync** là nền tảng Xử lý Ngôn ngữ Tự nhiên (NLP) đa phương thức giúp chuyển hóa bản ghi các buổi học luyện thi **TOEIC & IELTS** trực tuyến (Zoom / Google Meet / YouTube) thành **Sổ tay Học tập Tương tác Từng giây cho Học viên** và **Bảng điều khiển Phân tích Sư phạm Tự động cho Giáo viên**.

---

## 📚 Bộ Tài liệu Chính thức của Đồ án (`docs/`)

Toàn bộ tài liệu học thuật, thiết kế kỹ thuật và cẩm nang thuyết trình của đồ án môn học **Xử lý Ngôn ngữ Tự nhiên Nâng cao (NLP501 - MSE)** được chuẩn hóa tại thư mục [`docs/`](docs/):

| STT | Tài liệu | Mô tả Trọng tâm |
| :---: | :--- | :--- |
| 📖 | [**`docs/README.md`**](docs/README.md) | **Mục lục Trung tâm & Bản đồ Ánh xạ 7 Kỹ thuật NLP** |
| ⭐ | [**`09_teacher_presentation_and_technical_nlp_guide.md`**](docs/09_teacher_presentation_and_technical_nlp_guide.md) | **Cẩm nang Kiến thức Trình bày cho Giảng viên, 7 Điểm Technical NLP & 8 Câu hỏi Phản biện** |
| 01 | [**`01_project_proposal.md`**](docs/01_project_proposal.md) | Đề xuất Đề tài: Bài toán Lớp học TOEIC/IELTS, Câu hỏi Nghiên cứu & Kết quả Thực nghiệm |
| 02 | [**`02_nlp_architecture_and_literature.md`**](docs/02_nlp_architecture_and_literature.md) | Cơ sở Lý thuyết Toán học & Kỹ thuật NLP Chuyên sâu + Tổng quan Nghiên cứu Quốc tế |
| 03 | [**`03_requirements_analysis_srs.md`**](docs/03_requirements_analysis_srs.md) | Đặc tả & Phân tích Yêu cầu Phần mềm (SRS - Chuẩn IEEE 830) |
| 04 | [**`04_detailed_design_and_qa_plan.md`**](docs/04_detailed_design_and_qa_plan.md) | Thiết kế Chi tiết Hệ thống (SDD) & Kế hoạch Kiểm soát Chất lượng (45/45 Unit Tests) |
| 05 | [**`05_solution_dense_embeddings_guide.md`**](docs/05_solution_dense_embeddings_guide.md) | Chuyên đề Kỹ thuật: Nhúng Vector Ngữ nghĩa (`all-MiniLM-L6-v2`) nối Câu hỏi ↔ Ngữ pháp |
| 06 | [**`06_user_guide_and_demo.md`**](docs/06_user_guide_and_demo.md) | Kịch bản Demo 90 Giây trước Giảng viên & Sổ tay Hướng dẫn Sử dụng Web Demo |
| 07 | [**`07_feature_detailed_design_matrix.md`**](docs/07_feature_detailed_design_matrix.md) | Ma trận Đối chiếu 10 Tính năng ↔ Kỹ thuật NLP ↔ Mã nguồn & Unit Tests |
| 08 | [**`08_presentation_slides_and_speaker_notes.md`**](docs/08_presentation_slides_and_speaker_notes.md) | Kịch bản 18 Slides Thuyết trình & Lời thoại Chi tiết cho 4 Thành viên |
| 🖥️ | [**`docs/slides.html`**](docs/slides.html) | **Slide Thuyết trình HTML Tương tác** (Tích hợp Timer, Lời thoại phím `N`, Grid phím `O`) |

---

## 🚀 Khởi chạy Nhanh Web Demo & Kiểm thử

```bash
# 1. Kích hoạt môi trường ảo
source .venv/bin/activate

# 2. Chạy bộ kiểm thử tự động (45/45 Unit Tests)
pytest -v

# 3. Đồng bộ dữ liệu bài giảng TOEIC vào thư mục demo và mở Web Server
python demo/prepare.py --lesson lessons/ece-toeic-starter-u4
cd demo && ../.venv/bin/python -m RangeHTTPServer 8000
# Mở trình duyệt tại: http://localhost:8000/
```

---

## 🧠 Tóm tắt 7 Điểm Áp dụng Kỹ thuật NLP (Technical NLP Highlights)

1. **Multimodal Contextual Biasing ASR (`transcribe.py`):** Trích xuất từ vựng tiếng Anh trên màn hình đề thi qua Apple Vision OCR làm `Screen Hints` bơm vào `initial_prompt` của `faster-whisper` (`large-v3-turbo`), giảm 50% lỗi WER thuật ngữ (từ 18.4% xuống **9.2%**).
2. **Code-Switching Identification & Cross-Lingual Homophone Disambiguation (`transcribe.py`, `vocab.py`):** Phân loại ngôn ngữ `vi` / `en` / `mixed` theo mật độ dấu thanh tiếng Việt ($\text{Density}_{\text{vi}}$) và lọc từ đồng âm xuyên ngôn ngữ (`VI_HOMOPHONES`: *an, may, can, hay, con*).
3. **Monotonic Dynamic Programming Alignment (`exercises.py`, `exercise_align.py`):** Căn chỉnh đơn điệu 100% câu hỏi trắc nghiệm TOEIC/IELTS (**34/34 câu**, sai số $\le 1.8\text{s}$) với lời giảng bằng ràng buộc nhân quả $t_{k+1} > t_k$ và Regex Negative Lookbehind `(?<!text\s)(?<!page\s)`.
4. **Dense Semantic Embeddings cho Question-to-Concept Grounding (`concept_link.py`):** Mã hóa câu hỏi và chủ điểm lý thuyết bằng mô hình Bi-Encoder `sentence-transformers/all-MiniLM-L6-v2` ($\mathbb{R}^{384}$) và tính **Cosine Similarity**, giải quyết hiện tượng *Vocabulary Mismatch* trong **4.2 ms/câu**.
5. **Morphological Lemmatization, CEFR-J Profiling & Bilingual IE (`vocab.py`):** Chuẩn hóa hình thái 2 lớp (quy tắc + bất quy tắc), phân bậc độ khó theo từ điển **CEFR-J & Octanove (8.845 từ, A1–C2)**, trích xuất nghĩa tiếng Việt từ lời giảng và cắt tự động **79 đoạn audio 1.5s** giọng thật giáo viên.
6. **Hybrid Neural + Rule-based Information Extraction (`neural_ie.py`):** Kết hợp Gemini Flash-Lite Structured JSON Schema với bộ Regex Fallback tất định để bóc tách chủ điểm ngữ pháp, công thức và mẹo làm bài thi TOEIC/IELTS.
7. **Learner Grammatical Error Correction theo chuẩn ERRANT (`chat_parser.py`, `feedback.py`, `teacher_analytics.py`):** Ẩn danh học viên chuẩn FERPA ($S_1 \dots S_N$), bắt 6 nhóm lỗi chuyển di ngôn ngữ mẹ đẻ (*L1 Transfer*) theo hệ phân loại quốc tế **ERRANT (ACL 2019)** và tự động tổng hợp **Teacher Pedagogical Dashboard** (TTT/STT, Error Heatmap, Weakest Concept, Next-Lesson Action Plan).

---

## 📂 Cấu trúc Thư mục Mã nguồn

| Tệp / Thư mục | Chức năng Chính |
| :--- | :--- |
| `pipeline.py` | Điều phối chạy toàn bộ các bước NLP end-to-end cho một bài giảng trong `lessons/<id>/` |
| `extract_screens.py` | Phát hiện chuyển cảnh video, trích xuất khung hình đề bài ổn định và chạy OCR song ngữ Việt–Anh |
| `transcribe.py` | Nhận dạng tiếng nói `faster-whisper` kết hợp `Screen Hints` và gán nhãn ngôn ngữ phân đoạn |
| `exercises.py` | Bóc tách cấu trúc câu hỏi trắc nghiệm TOEIC/IELTS (câu dẫn stem + lựa chọn A/B/C/D) từ OCR |
| `exercise_align.py` | Thuật toán Quy hoạch động Đơn điệu (Monotonic DP) căn chỉnh từng câu hỏi với mốc thời gian lời giảng |
| `neural_ie.py` | Trích xuất cấu trúc các chủ điểm ngữ pháp lý thuyết, công thức và mẹo thi (Gemini API + Regex Fallback) |
| `concept_link.py` | Nhúng vector ngữ nghĩa (`all-MiniLM-L6-v2`) và tính Cosine Similarity nối Câu hỏi $\leftrightarrow$ Lý thuyết |
| `vocab.py` | Bộ phân tích hình thái học, phân bậc từ vựng CEFR-J (A1–C2), khai phá nghĩa tiếng Việt & cắt audio 1.5s |
| `chat_parser.py` | Bóc tách log chat Zoom/Meet, ẩn danh học viên ($S_1 \dots S_N$) và liên kết tin nhắn với câu hỏi bài tập |
| `feedback.py` | Chẩn đoán lỗi ngữ pháp L1 Transfer theo chuẩn quốc tế ERRANT và sinh giải thích sư phạm tiếng Việt |
| `diarize.py` | Phân tách lượt nói và thống kê thời lượng nói Giáo viên (TTT) vs Học viên (STT) |
| `teacher_analytics.py` | Tổng hợp báo cáo sư phạm `teacher_report.json` (TTT/STT, Error Heatmap, Weakest Concept, Action Plan) |
| `demo/` | Giao diện Web Demo tương tác (`index.html`, `prepare.py`) dành cho Học viên và Giáo viên |
| `tests/` | Bộ 10 tệp kiểm thử tự động (`45/45 Unit Tests PASSED`) |
