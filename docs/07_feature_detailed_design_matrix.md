# MA TRẬN THIẾT KẾ CHI TIẾT TỪNG TÍNH NĂNG & ÁNH XẠ KỸ THUẬT NLP (FEATURE & TECHNICAL NLP MATRIX)
## EDUSYNC: NỀN TẢNG ĐỒNG BỘ ĐA PHƯƠNG THỨC & PHÂN TÍCH SƯ PHẠM BÀI GIẢNG LUYỆN THI TIẾNG ANH (TOEIC & IELTS)
**Môn học:** Xử lý Ngôn ngữ Tự nhiên Nâng cao (NLP501 - Master of Software Engineering)  
**Nhánh Git:** `edusync-v2`  
**Cập nhật:** Tháng 11/2026  

---

## 💡 Điểm nhấn Trình bày với Giảng viên (Feature-to-NLP Mapping)

> Tài liệu này giúp nhóm đối chiếu trực tiếp **10 tính năng sản phẩm** với **Kỹ thuật NLP (Technical NLP)**, **File mã nguồn thực tế** và **Bài kiểm thử Unit Test** tương ứng khi giảng viên yêu cầu chứng minh từng phần trong lúc chấm điểm.

---

## 1. Bảng Ma trận 10 Tính năng Cốt lõi & Điểm Áp dụng Technical NLP

| Mã | Tên Tính năng (Bối cảnh TOEIC / IELTS) | Kỹ thuật NLP Áp dụng (Technical NLP) | File Mã nguồn | Độ phủ Kiểm thử (Unit Tests) | Kết quả Thực tế |
| :-: | :--- | :--- | :--- | :--- | :---: |
| **F-01** | **ASR Đa ngữ Việt–Anh kèm Bơm Ngữ cảnh Đề thi (Screen Hints)** | • Transformer Seq2Seq ASR (`faster-whisper` `large-v3-turbo` / `small`).<br>• **Contextual Biasing / Prefix Conditioning** $P(Y \mid X, H)$ từ từ vựng OCR màn hình.<br>• **Diacritics Density Heuristic** phân loại `vi` / `en` / `mixed`. | `transcribe.py` | `test_wer.py` (5 tests)<br>`test_text_lang.py` (3 tests) | **100% ĐẠT**<br>Giảm 50% WER thuật ngữ (18.4% $\to$ 9.2%) |
| **F-02** | **Trích xuất Màn hình Đề bài & Parser Câu hỏi TOEIC/IELTS** | • Phát hiện chuyển cảnh video (`Pixel Diff + Gaussian Blur`).<br>• Song ngữ OCR (`Apple Vision API` / `PyMuPDF`).<br>• Regex Parser bóc tách câu dẫn (stem) & phương án A/B/C/D. | `extract_screens.py`<br>`exercises.py` | `test_screen_hints.py` (4 tests)<br>`test_exercises.py` (2 tests) | **100% ĐẠT**<br>32 màn hình, 34 câu hỏi, 0 stem rỗng |
| **F-03** | **Căn chỉnh Đơn điệu Câu hỏi ↔ Lời giảng (Monotonic DP)** | • **Regex Negative Lookbehind** `(?<!text\s)(?<!page\s)` chống nhầm số trang/bài đọc.<br>• **Monotonic Dynamic Programming** với ràng buộc nhân quả $t_{k+1} > t_k$ & cửa sổ động 120s. | `exercise_align.py` | `test_exercises.py` (2 tests) | **100% ĐẠT**<br>Recall **100% (34/34 câu)**, sai số $\le 1.8\text{s}$ |
| **F-04** | **Phân bậc Từ vựng CEFR (A1–C2) & Cắt Audio Mẫu 1.5s** | • **Two-stage Morphological Lemmatization** (quy tắc hậu tố + bảng bất quy tắc).<br>• Đối chiếu từ điển **CEFR-J & Octanove (8.845 từ)**.<br>• Lọc đồng âm Việt–Anh (`VI_HOMOPHONES`).<br>• **Pattern-based Bilingual IE** trích nghĩa tiếng Việt + cắt audio 1.5s. | `vocab.py` | `test_vocab.py` (8 tests) | **100% ĐẠT**<br>79 từ CEFR, 43 nghĩa tiếng Việt, 79 file `.mp3` |
| **F-05** | **Parser Log Chat Zoom/Meet & Bảo mật Ẩn danh Học viên** | • Bóc tách cấu trúc hội thoại đa định dạng.<br>• **One-way PII Anonymization** chuẩn FERPA/GDPR ($S_1 \dots S_N$).<br>• **Cross-modal Entity Linking** nối tin nhắn chat với câu hỏi bài tập ($Q_1 \dots Q_{34}$). | `chat_parser.py` | `test_feedback.py` (4 tests) | **100% ĐẠT**<br>17 tin nhắn, 5 học viên, 0% lộ tên thật |
| **F-06** | **Chẩn đoán Lỗi Ngữ pháp Người học theo chuẩn ERRANT (GEC)** | • Hệ phân loại lỗi quốc tế **ERRANT Taxonomy (ACL 2019)** (`Operation:POS:SubType`).<br>• Nhận diện 6 nhóm lỗi **L1 Transfer** của học viên Việt Nam (`U:VERB:BE`, `R:ADJ:PARTICIPLE`, `R:VERB:FORM`, `U:PREP`, `R:VERB:SVA`, `M:VERB:AUX`). | `feedback.py` | `test_feedback.py` (6 tests) | **100% ĐẠT**<br>Bắt chính xác **6/6 (100%)** lỗi ngữ pháp |
| **F-07** | **Trích xuất Chủ điểm Ngữ pháp & Mẹo thi TOEIC/IELTS (Hybrid IE)** | • **LLM Structured JSON Schema Extraction** (Gemini 3.5 Flash-Lite).<br>• **Deterministic Regex Fallback** khi offline, đảm bảo không bao giờ dừng pipeline. | `neural_ie.py` | `test_neural_ie.py` (4 tests) | **100% ĐẠT**<br>4 chủ điểm ngữ pháp + công thức + Exam Tips |
| **F-08** | **Liên kết Câu hỏi ↔ Lý thuyết Ngữ pháp bằng Dense Embeddings** | • **Bi-Encoder Siamese Transformer** (`sentence-transformers/all-MiniLM-L6-v2`, $\mathbb{R}^{384}$).<br>• Mean Pooling + $L_2$ Normalization + **Cosine Similarity Matrix** giải quyết bài toán *Vocabulary Mismatch*. | `concept_link.py` | `test_concept_link.py` (2 tests) | **100% ĐẠT**<br>Suy luận **4.2 ms/câu**, gắn Badge liên kết 2 chiều |
| **F-09** | **Phân tích Tương tác (TTT/STT) & Báo cáo Sư phạm Giáo viên** | • **Speaker Diarization & Role Attribution** (`T` vs `S`).<br>• Tổng hợp **ERRANT Error Heatmap**, phát hiện **Weakest Concept** và sinh **Next-Lesson Action Plan** 3 bước. | `diarize.py`<br>`teacher_analytics.py` | `test_diarize.py` (3 tests)<br>`test_teacher_analytics.py` (2 tests) | **100% ĐẠT**<br>Sinh tự động `teacher_report.json` |
| **F-10** | **Ứng dụng Web Demo Tương tác Đa phương thức & Omnibox** | • Đồng bộ trình phát video từng phần trăm giây qua HTTP Byte-Range.<br>• Chỉ mục tìm kiếm toàn văn đa nguồn (**Omnibox Search** $< 30\text{ms}$). | `demo/index.html`<br>`demo/prepare.py` | Kiểm thử tích hợp End-to-End | **100% ĐẠT**<br>5 Tab tương tác mượt mà tại `localhost:8000` |

---

## 2. Thống kê Khối lượng Mã nguồn & Kiểm thử Toàn Dự án

- **Tổng khối lượng mã nguồn:** **~4.950 dòng code (LOC)** (bao gồm ~2.410 dòng Python NLP Pipeline, ~1.990 dòng giao diện Web Demo SPA, ~550 dòng Unit Tests).
- **Trạng thái Kiểm thử Tự động (`pytest -v`):** **45 / 45 Unit Tests PASSED (100%)** trong 7.5 giây.
- **Tài liệu Chuẩn hóa (`docs/`):** 9 chuyên đề hoàn chỉnh từ Proposal, Lý thuyết NLP, SRS, SDD/QA, Hướng dẫn Dense Embeddings, User Guide, Feature Matrix, Kịch bản Slide 4 thành viên đến Cẩm nang Kiến thức Trình bày & Phản biện Technical NLP.
