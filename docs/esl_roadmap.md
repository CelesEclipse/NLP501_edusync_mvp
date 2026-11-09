# Lộ trình Chuyển đổi & Phát triển: EduSync cho Bài giảng Luyện thi Tiếng Anh (TOEIC & IELTS)

**Cập nhật:** Tháng 11/2026  
**Trạng thái:** Đã hoàn thành toàn bộ các gói công việc cốt lõi trên nhánh `edusync-v2` (xem chi tiết tại [`01_project_proposal.md`](01_project_proposal.md) và [`09_teacher_presentation_and_technical_nlp_guide.md`](09_teacher_presentation_and_technical_nlp_guide.md)).

---

## 1. Mục tiêu Định hướng TOEIC & IELTS

Biến bản ghi một buổi học luyện thi **TOEIC hoặc IELTS** trực tuyến trên Google Meet / Zoom (video màn hình đề thi, lời giảng trộn mã Việt–Anh, danh sách câu hỏi thực hành, chủ điểm ngữ pháp và log chat học viên) thành:
- **Sổ tay Học tập Tương tác cho Học viên (Interactive Learner Notebook):**
  - Bấm vào câu hỏi trắc nghiệm (TOEIC Part 5/6/7 hoặc IELTS Reading/Listening) để tua video tới đúng giây giáo viên chữa câu đó.
  - Bấm vào Badge Ngữ pháp trên câu hỏi để nhảy ngược về đúng phút giáo viên giảng công thức lý thuyết đầu giờ.
  - Học từ vựng phân tầng theo khung tham chiếu châu Âu **CEFR (A1–C2)** tương ứng các mốc điểm TOEIC (450–900+) và IELTS (Band 5.0–8.0+), kèm nghĩa tiếng Việt trong bài và đoạn âm thanh mẫu 1.5s cắt từ giọng thật của giáo viên.
  - Xem lại câu trả lời của mình trong khung chat đã được chẩn đoán lỗi ngữ pháp theo chuẩn **ERRANT** kèm lời giải thích tiếng Việt.
- **Bảng điều khiển Sư phạm cho Giáo viên (Teacher Pedagogical Dashboard):**
  - Đo lường tự động tỷ lệ thời gian nói của giáo viên và học viên (**TTT vs STT**).
  - Thống kê bản đồ phân bố lỗi ngữ pháp của cả lớp (**ERRANT Error Heatmap**) và cảnh báo chủ điểm lý thuyết học viên sai nhiều nhất (**Weakest Concept**).
  - Đề xuất tự động **Kế hoạch Hành động 3 bước (Next-Lesson Action Plan)** cho buổi dạy tiếp theo.

---

## 2. Bảy Gói Công việc Kỹ thuật NLP (Work Packages) & Kết quả Thực tế

| Mã WP | Nội dung Sư phạm (TOEIC / IELTS) | Kỹ thuật NLP Áp dụng | Chỉ số Đánh giá & Kết quả Đạt được |
| :-: | :--- | :--- | :--- |
| **WP1** | Nhận dạng lời giảng trộn mã Việt–Anh biết ngữ cảnh đề thi; tách người nói | `faster-whisper` (`large-v3-turbo`) + OCR `Screen Hints` Prompting + Diacritics Density + VAD Diarization | Giảm 50% WER thuật ngữ tiếng Anh (từ 18.4% $\to$ **9.2%**); phân loại chuẩn 74% `vi`, 26% `en` |
| **WP2** | Bóc tách các chủ điểm ngữ pháp lý thuyết & mẹo làm bài thi TOEIC/IELTS | **Hybrid Neural IE** (Gemini 3.5 Flash-Lite JSON Schema + Deterministic Regex Fallback) | Trích xuất chính xác 4 chủ điểm ngữ pháp trọng tâm + công thức + timestamp + Exam Tips |
| **WP3** | Bóc tách câu hỏi bài tập từ màn hình & căn chỉnh Câu hỏi ↔ Đoạn chữa | Apple Vision OCR + **Monotonic Dynamic Programming** ($t_{k+1} > t_k$) + Regex Negative Lookbehind | **Recall 100% (34/34 câu hỏi)**, Precision **97.1%**, sai số biên $\le 1.8\text{s}$ |
| **WP4** | Liên kết ngữ nghĩa 2 chiều giữa Câu hỏi thực hành ↔ Chủ điểm Ngữ pháp gốc | **Dense Semantic Embeddings** (`sentence-transformers/all-MiniLM-L6-v2`, $\mathbb{R}^{384}$) + Cosine Similarity | Giải quyết 100% bài toán *Vocabulary Mismatch*, suy luận local **4.2 ms/câu** |
| **WP5** | Khai phá từ vựng học thuật theo bậc CEFR, trích nghĩa tiếng Việt & cắt audio 1.5s | Lemmatization 2 lớp + Từ điển **CEFR-J/Octanove (8.845 từ)** + Lọc `VI_HOMOPHONES` + Pattern Relation IE | Trích xuất **79 từ vựng CEFR (A1–C1)**, **43 định nghĩa tiếng Việt**, **79 file audio `.mp3`** |
| **WP6** | Chẩn đoán và giải thích lỗi ngữ pháp trong hộp chat học viên | Ẩn danh FERPA ($S_1 \dots S_N$) + Hệ phân loại lỗi quốc tế **ERRANT Taxonomy (ACL 2019)** | Bắt đúng **6/6 (100%)** lỗi chuyển di ngôn ngữ L1 Transfer trong benchmark lớp học |
| **WP7** | Tổng hợp báo cáo sư phạm cho giáo viên & Ứng dụng Web Demo | `teacher_analytics.py` + Giao diện SPA 5 Tabs + Thanh tìm kiếm toàn bài Omnibox | Độ trễ tìm kiếm $< 30\text{ms}$; vượt qua **45/45 Unit Tests (100% PASS)** |
