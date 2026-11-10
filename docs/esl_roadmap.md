# Lộ trình Chuyển đổi & Phát triển: EduSync cho Bài giảng Luyện thi Tiếng Anh (TOEIC; IELTS là hướng mở rộng)

**Cập nhật:** 10/11/2026  
**Trạng thái:** Đã cài đặt đủ 7 gói công việc trên nhánh `edusync-v2` và có bộ đánh giá tái tạo được (`python eval/run_all.py`). Còn thiếu: WER của ASR, nhãn chuẩn đã được nhóm kiểm tra (hiện đều là bản nháp AI, `verified: false`), tập kiểm tra độc lập cho liên kết chủ điểm, dữ liệu chat thật và bản ghi nhiều người nói. Số liệu: [docs/10_evaluation_results.md](10_evaluation_results.md).

---

## 1. Mục tiêu Định hướng

Biến bản ghi một buổi học luyện thi trực tuyến trên Google Meet / Zoom (video màn hình đề thi, lời giảng trộn mã Việt–Anh, câu hỏi thực hành, chủ điểm ngữ pháp và log chat học viên) thành:
- **Sổ tay học tập tương tác cho học viên:**
  - Bấm vào câu hỏi trắc nghiệm (TOEIC Part 5/6/7) để tua video tới đoạn giáo viên chữa câu đó.
  - Bấm vào badge ngữ pháp trên câu hỏi để quay về đoạn giáo viên giảng lý thuyết.
  - Học từ vựng của bài theo bậc **CEFR (A1–C2)**, kèm nghĩa tiếng Việt giáo viên nói trong bài và clip phát âm ngắn cắt từ giọng giáo viên.
  - Xem lại câu trả lời của mình trong chat kèm câu sửa, loại lỗi **ERRANT** và giải thích tiếng Việt (cho 6 nhóm lỗi chuyển di L1).
- **Báo cáo cho giáo viên:**
  - Tỉ lệ thời gian nói giáo viên / học viên (**TTT vs STT**) khi bản ghi tách được người nói.
  - Phân bố lỗi của lớp theo nhóm lỗi và chủ điểm có nhiều lỗi nhất (**weakest concept**).
  - Gợi ý cho buổi sau bằng **câu mẫu** điền từ dữ liệu (không dùng LLM).
- **Hướng mở rộng (chưa làm):** bài giảng IELTS (Reading/Listening/Speaking).

---

## 2. Bảy Gói Công việc Kỹ thuật NLP (Work Packages) & Trạng thái Thực tế

| Mã WP | Nội dung | Kỹ thuật NLP Áp dụng | Trạng thái & Kết quả đo được |
| :-: | :--- | :--- | :--- |
| **WP1** | Nhận dạng lời giảng trộn mã Việt–Anh; tách người nói | `faster-whisper` `large-v3-turbo` đa ngữ; gợi ý từ OCR qua `hotwords` (tùy chọn); nhãn ngôn ngữ theo mật độ chữ có dấu; diarization `tracks` / `pyannote` / một người nói | **Một phần.** Đã cài đặt; **WER chưa đo** (bản tham chiếu chưa sửa tay). Proxy: 47% (không gợi ý) → 52% (có gợi ý) nhưng số đoạn lặp tăng 6 → 20–27, chưa kết luận. Nhãn ngôn ngữ U4: 73% `vi`, 26% `en` (chưa đánh giá). TTT/STT không đo được vì bản ghi một người nói. |
| **WP2** | Trích chủ điểm ngữ pháp & mẹo thi | Gemini `gemini-3.5-flash-lite` ở chế độ JSON + taxonomy chủ điểm TOEIC offline; neo mốc lý thuyết bằng `multilingual-e5-small` | **Xong (U4).** 4 chủ điểm; sai số mốc lý thuyết trung bình 11,2 s sau khi neo (Gemini đoán: 882,5 s). Nội dung chủ điểm chưa được đánh giá riêng. |
| **WP3** | Trích câu hỏi từ màn hình & căn chỉnh câu hỏi ↔ đoạn chữa | Apple Vision OCR + quy hoạch động đơn điệu + xác minh khẩu lệnh bằng ngữ cảnh + lùi mốc | **Xong.** Test U5: 80,0% câu lệch ≤10 s, 88,6% ≤30 s, sai số TB 8,1 s, 0 đảo thứ tự (v1: 57,1% / 71,4% / 28,5 s). Dev U4: 68,8% / 84,4% / 10,0 s. Trên cả hai bài DP chọn giống greedy. |
| **WP4** | Liên kết câu hỏi ↔ chủ điểm ngữ pháp | Bi-encoder `multilingual-e5-small`, câu hỏi + lời giảng trong đoạn chữa; ngưỡng 0,835 | **Xong (chỉ có tập phát triển).** 91,2% trên 34 câu U4 (leave-one-out); ngưỡng cố định: link precision 90,0%, recall 75,0%. Lạc quan vì chọn trên chính tập này; độ trễ chưa đo. |
| **WP5** | Từ vựng theo bậc CEFR, nghĩa tiếng Việt & clip phát âm | Lemmatization 2 lớp + CEFR-J/Octanove (8.845 mục) + lọc `VI_HOMOPHONES` + mẫu khai phá nghĩa | **Xong, chưa đánh giá chất lượng.** U4: 80 từ (A1 26, A2 26, B1 18, B2 9, C1 1), 52 từ có nghĩa tiếng Việt, 79 clip `.wav` 0,7–2,2 s. |
| **WP6** | Phát hiện và giải thích lỗi trong chat học viên | Ẩn danh hoá tên người gửi ($S_1 \dots S_N$) + bộ luật 6 nhóm lỗi + loại lỗi ERRANT (Bryant và cộng sự, ACL 2017; kiểm chứng bằng errant 3.0.2) | **Xong.** Trên 70 câu viết độc lập: precision 100%, recall 72,7%, F1 84,2% (v1: 33,3%). Chat U4 là dữ liệu mô phỏng. |
| **WP7** | Báo cáo cho giáo viên & web demo | `teacher_analytics.py` + SPA 6 tab (Exercises, Grammar, Vocab, Chat & GEC, Screens, Analytics) + ô tìm kiếm 5 nguồn | **Xong.** TTT/STT hiển thị "chưa đo"; demo hiển thị số câu khớp được với lời giảng (33/34). **71/71 test** pass. Độ trễ tìm kiếm chưa đo. |

## 3. Việc cần làm tiếp

1. Nhóm kiểm tra lại toàn bộ nhãn nháp (2 tệp `alignment_gold.json`, `concept_gold.json`, 70 câu GEC), đặt `verified: true`, chạy lại `eval/run_all.py`.
2. Sửa tay 5 clip ASR và đo WER cho các cấu hình E2/E2b/E3 (xem [phase1_plan.md](phase1_plan.md)).
3. Thêm một bài kiểm tra độc lập cho liên kết chủ điểm và hiệu chỉnh lại ngưỡng.
4. Thu chat thật (có đồng ý) và bản ghi tách kênh từng người để đo TTT/STT.
