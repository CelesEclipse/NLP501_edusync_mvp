# Báo Cáo Thực Nghiệm Giai Đoạn 1: Hạ Tầng Đa Phương Thức & Xử Lý Tiếng Nói Trộn Mã Việt – Anh (TOEIC)

**Thuộc lộ trình:** [`esl_roadmap.md`](esl_roadmap.md)  
**Cập nhật:** 10/11/2026  
**Nguồn số liệu:** [docs/10_evaluation_results.md](10_evaluation_results.md)

---

## 1. Dữ liệu Bài giảng Luyện thi Tiếng Anh & Trích xuất Đa phương thức

- **Nguồn dữ liệu thực nghiệm:** 3 buổi **TOEIC Starter (Unit 1, Unit 4, Unit 5)** của kênh ECE English Online (Creative Commons CC BY), một giáo viên giảng bằng tiếng Việt, đọc đề và giải thích từ vựng tiếng Anh (`lessons/ece-toeic-starter-u1|u4|u5/`; 65 / 58 / 58 phút). U4 dùng để phát triển, U5 để kiểm tra độc lập, U1 chỉ dùng cho ASR và trích màn hình. Chưa có dữ liệu IELTS.
- **Đặc trưng:** video quay màn hình bài giảng, **không có slide PDF gốc**; đề bài, từ vựng và đáp án được trích tự động từ màn hình (pixel diff + Apple Vision OCR).
- **Kết quả trích xuất (Unit 1 / Unit 4 / Unit 5):**
  - Số màn hình: **46 / 32 / 32**.
  - Số đoạn lời giảng (`transcript.json`): **1.690 / 2.606 / 1.201**.
  - Câu hỏi trích được: U4 34 bản ghi (2 bản ghi là đoạn văn, không phải câu hỏi), U5 35.
  - Nhãn ngôn ngữ trên U4 (heuristic mật độ chữ có dấu, chưa được đánh giá): 73% đoạn `vi`, 26% đoạn `en`, 5 đoạn `mixed`.
- **Lưu ý:** chỉ có **một người nói** (giáo viên) nên không đo được TTT/STT; log chat U4 (17 tin nhắn, 5 học viên) là **dữ liệu mô phỏng** do nhóm soạn.

---

## 2. Thực nghiệm Lựa chọn Mô hình ASR & Gợi ý Ngữ cảnh từ Màn hình

Trên bài giảng **TOEIC Starter Unit 4**, nhóm so sánh các cấu hình `faster-whisper`. **Chưa có WER** cho cấu hình nào vì bản chép tham chiếu (5 clip × 2 phút trong `gold/asr/`) chưa được sửa tay; các nhận xét về `small` và `large-v3-turbo` dưới đây là quan sát định tính, không phải số đo.

| Cấu hình Thử nghiệm | Quan sát / Chỉ số | Kết quả & Quyết định |
| :--- | :--- | :--- |
| **E1: `whisper-small`** | Quan sát: sai nhiều từ tiếng Việt đồng âm và mất từ tiếng Anh đọc lướt. | Không dùng. |
| **E2: `whisper-large-v3-turbo` (đa ngữ)** — không gợi ý | Quan sát: tiếng Việt tốt hơn rõ, vẫn sai một số chỗ (vd. *"mệnh đề phân từ"* → *"bệnh đề phân từ"*, *"verb-ing"* → *"verb in"*). Proxy "từ trên màn hình được nói ra": 47%; 2.606 đoạn; 6 đoạn lặp liên tiếp. | **Đang dùng làm `transcript.json`.** |
| **E2b: cắt audio theo màn hình, không gợi ý** (đối chứng) | Proxy 48%; 545 đoạn; 3 đoạn lặp. | Đối chứng cho E3. |
| **E3: `large-v3-turbo` + gợi ý từ OCR qua `hotwords`** (`--screen-hints words` / `lines`) | Proxy 52% / 52%; 484 / 559 đoạn; **20 / 27 đoạn lặp**. | Proxy tăng khoảng 4 điểm so với đối chứng nhưng số đoạn lặp (dấu hiệu ảo giác) cũng tăng, và proxy có thể tăng chỉ vì Whisper chép lại từ gợi ý. **Chưa kết luận; chưa dùng.** |

Gợi ý được truyền qua tham số `hotwords` của faster-whisper (không phải `initial_prompt`; `initial_prompt` là câu mô tả bài học cố định trong `lesson.json`). **Việc còn lại của WP1:** sửa tay 5 clip, đặt `"corrected": true`, chạy `python eval/wer.py --lesson lessons/ece-toeic-starter-u4 results/asr_none.json results/asr_chunks.json results/asr_words.json`.

---

## 3. Lược đồ Chuẩn hóa Dữ liệu Đầu ra cho Các Tầng NLP Phía sau

1. **`lesson.json`:** metadata buổi học (tiêu đề, nguồn, giấy phép, thời lượng, ngôn ngữ giảng `vi`, ngôn ngữ mục tiêu `en`, cấu hình ASR: mô hình, prompt cố định, đa ngữ).
2. **`screens.json` & `exercises.json`:** các màn hình đã khử trùng lặp kèm văn bản OCR; các câu hỏi (số câu, đề bài, lựa chọn A–D, cửa sổ màn hình).
3. **`transcript.json`:** các đoạn lời giảng với `start`, `end`, `text`, `lang` (`vi` / `en` / `mixed`). Không có timestamp từng từ.
4. **`exercise_alignment.json` & `exercise_concept_links.json`:** mốc chữa từng câu hỏi (DP đơn điệu, kèm `matched`) và liên kết tới chủ điểm ngữ pháp (`multilingual-e5-small` + lời giảng).
5. **`vocab.json` & `vocab_audio/*.wav`:** U4 có 80 từ phân bậc CEFR (A1 26, A2 26, B1 18, B2 9, C1 1), 52 từ có nghĩa tiếng Việt khai thác từ lời giảng (chưa kiểm tra độ đúng) và 79 clip `.wav` 0,7–2,2 s cắt theo ranh giới đoạn ASR.
6. **`chat_feedback.json`:** lỗi phát hiện trong chat đã ẩn danh hoá ($S_1 \dots S_N$), mỗi lỗi kèm loại ERRANT, câu sửa chuẩn xác và giải thích tiếng Việt.
