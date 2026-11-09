# Báo Cáo Thực Nghiệm Giai Đoạn 1: Hạ Tầng Đa Phương Thức & Xử Lý Tiếng Nói Trộn Mã Việt – Anh (TOEIC / IELTS)

**Thuộc lộ trình:** [`esl_roadmap.md`](esl_roadmap.md)  
**Cập nhật:** Tháng 11/2026  

---

## 1. Dữ liệu Bài giảng Luyện thi Tiếng Anh & Trích xuất Đa phương thức

- **Nguồn dữ liệu thực nghiệm:** 3 buổi giảng luyện thi **TOEIC Starter (Unit 1, Unit 4, Unit 5)** của kênh ECE English Online (giấy phép Creative Commons CC BY), giảng bằng tiếng Việt kết hợp đọc đề và giải thích từ vựng tiếng Anh (`lessons/ece-toeic-starter-u1|u4|u5/`, tổng thời lượng ~3 giờ).
- **Đặc trưng thách thức thực tế:** Video quay màn hình bài giảng, **không có tệp Slide PDF gốc**. Toàn bộ khung hình đề bài, từ vựng và đáp án giáo viên chữa trực tiếp trên màn hình được tự động bóc tách qua pipeline thị giác và ngôn ngữ.
- **Kết quả trích xuất trên 3 buổi học (Unit 1 / Unit 4 / Unit 5):**
  - Số màn hình đề bài không trùng lặp: **46 / 32 / 32 màn hình**.
  - Số phân đoạn lời giảng (`transcript.json`): **1.690 / 2.606 / 1.201 phân đoạn** (trung bình ~74% phân đoạn tiếng Việt, ~26% phân đoạn tiếng Anh, ~1% phân đoạn trộn mã trực tiếp).

---

## 2. Thực nghiệm Lựa chọn Mô hình ASR & Kỹ thuật Contextual Prompting

Khi thử nghiệm trên bài giảng **TOEIC Starter Unit 4**, nhóm đã tiến hành so sánh các cấu hình mô hình `faster-whisper`:

| Cấu hình Thử nghiệm | Hiện tượng Quan sát được trên Dữ liệu Thực tế | Kết quả & Quyết định Kỹ thuật |
| :--- | :--- | :--- |
| **E1: `whisper-small` (Mặc định)** | Sai nhiều từ tiếng Việt đồng âm (*"đáp án"* $\to$ *"đã bán"*, *"tiếng ồn"* $\to$ *"tiếng hồn"*) và mất từ tiếng Anh đọc lướt. | Dùng làm baseline so sánh tốc độ trên CPU. |
| **E2: `whisper-large-v3-turbo` (Multilingual)** | Nhận diện tiếng Việt chính xác vượt trội, tốc độ tương đương `small` (35s so với 28s cho 120s âm thanh nhờ rút gọn Decoder còn 4 tầng). Tuy nhiên vẫn còn lỗi ở các cụm tiếng Anh đọc nhanh (*"his shoes shined"* $\to$ *"his sue signed"*). | Chọn làm mô hình ASR chính cho bài giảng tiếng Anh. |
| **E3: `large-v3-turbo` + OCR `Screen Hints` Prompting** | Trích xuất từ vựng tiếng Anh trên màn hình đang chiếu qua Apple Vision OCR và nạp vào `initial_prompt` của Whisper. Các từ vựng mục tiêu (*shined, participle, moved, annoying, wholesale*) được nhận diện chính xác. | **Giảm 50% lỗi WER thuật ngữ tiếng Anh (từ 18.4% xuống 9.2%)**, triệt tiêu ảo giác (hallucination). |

---

## 3. Lược đồ Chuẩn hóa Dữ liệu Đầu ra cho Các Tầng NLP Phía sau

1. **`lesson.json`:** Lưu metadata buổi học (tiêu đề, trình độ CEFR/TOEIC/IELTS, ngôn ngữ giảng dạy `vi`, ngôn ngữ mục tiêu `en`, cấu hình ASR prompt).
2. **`screens.json` & `exercises.json`:** Danh sách khung hình đề bài đã khử trùng lặp và 34 câu hỏi trắc nghiệm (stem + options A/B/C/D).
3. **`transcript.json`:** Chuỗi phân đoạn lời giảng kèm `start`, `end`, `lang` (`vi` / `en` / `mixed`), `speaker` (`T` / `S`) và `words` (timestamp cấp độ từng từ).
4. **`exercise_alignment.json` & `exercise_concept_links.json`:** Mốc thời gian chữa từng câu hỏi (Monotonic DP) và liên kết ngữ nghĩa 2 chiều tới chủ điểm ngữ pháp (`all-MiniLM-L6-v2`).
5. **`vocab.json` & `vocab_audio/*.mp3`:** Danh mục 79 từ vựng phân bậc CEFR (A1–C1), nghĩa tiếng Việt trong bài và 79 đoạn âm thanh phát âm mẫu 1.5s của giáo viên.
6. **`chat_feedback.json` & `teacher_report.json`:** Kết quả chẩn đoán lỗi ngữ pháp ERRANT từ hộp chat đã ẩn danh FERPA ($S_1 \dots S_N$) và báo cáo sư phạm cho giáo viên.
