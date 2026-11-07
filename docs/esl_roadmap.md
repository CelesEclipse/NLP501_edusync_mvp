# Lộ trình: EduSync cho dạy và học tiếng Anh (bản ghi Meet/Zoom)

Cập nhật: 06/11/2026. Kế hoạch chi tiết của phase đang làm: [phase1_plan.md](phase1_plan.md).

## Mục tiêu

Biến bản ghi một buổi học tiếng Anh trên Google Meet/Zoom (slide, lời giảng, câu hỏi bài tập, ví dụ chữa bài,
tài liệu đính kèm, chat) thành:

- **Trình xem buổi học:** bấm slide hoặc câu bài tập thì video tua tới đúng chỗ; transcript song ngữ, từ vựng
  tô màu theo trình độ CEFR.
- **Gói ôn tập cho học viên:** thẻ từ vựng (nghĩa, ví dụ trong bài, giọng giáo viên đọc), bài tập mới cùng điểm
  ngữ pháp, phản hồi câu trả lời trong chat.
- **Báo cáo cho giáo viên:** các giai đoạn buổi học, tỉ lệ giáo viên nói / học viên nói, loại câu hỏi và cách
  sửa lỗi, lỗi chung của lớp.

Nền tảng là EduSync v2: căn chỉnh slide–video bằng khung hình + lời giảng (sai số trung bình 0,6 s trên bài
giảng CS224N), tìm kiếm trong lời giảng, liên kết tài liệu.

## Đầu vào của một buổi học

```
lessons/<mã buổi>/
  video.mp4            bản ghi Meet/Zoom (chia sẻ màn hình)
  slides.pdf           slide bài giảng
  worksheet.pdf|docx   tài liệu đính kèm (bài tập)
  chat.txt             chat của buổi học (nếu có)
  audio/*.m4a          âm thanh riêng từng người (nếu Zoom bật)
```

## Bảy gói việc (WP)

| WP | Nội dung | Bài toán NLP | Cách đo |
|---|---|---|---|
| WP1 | ASR chen Việt–Anh, biết slide; tách người nói | Nhận dạng tiếng nói, diarization | WER, tỉ lệ nhận đúng từ tiếng Anh, DER |
| WP2 | Phân đoạn giai đoạn; hành động lời nói | Phân đoạn văn bản, phân loại câu | Pk/WindowDiff, macro-F1 |
| WP3 | Trích bài tập; căn chỉnh câu hỏi ↔ đoạn chữa; lấy đáp án | Trích xuất thông tin, căn chỉnh, QA | Hit@1, sai số thời gian, độ chính xác đáp án |
| WP4 | Từ vựng song ngữ theo CEFR, đoạn âm thanh phát âm, thẻ ôn | Xếp trình độ từ/câu, dịch máy | Độ chính xác CEFR, giáo viên chấm nghĩa |
| WP5 | Phản hồi câu trả lời viết trong chat | Sửa lỗi ngữ pháp (GEC), phân loại lỗi | F0.5 (BEA-2019 + chat tự gán), học viên chấm |
| WP6 | Sinh bài tập mới, phương án nhiễu từ lỗi của lớp | Sinh câu hỏi, sinh phương án nhiễu | Tỉ lệ qua bộ lọc, giáo viên chấm |
| WP7 | Báo cáo giáo viên; demo | Tổng hợp từ WP1–WP6 | Giáo viên chấm, nghiên cứu người dùng |

## Các phase

| Phase | Thời gian | Gói việc | Mốc kiểm tra |
|---|---|---|---|
| **1** | Tuần 0–1 | Hạ tầng theo buổi học + WP1 | Transcript có ngôn ngữ, người nói, slide, mốc theo từ; số WER đầu tiên |
| 2 | Tuần 2 | WP2 + WP3 | "Câu n → chỗ chữa" chạy được |
| 3 | Tuần 3 | WP4 + WP5 | Thẻ từ và phản hồi chat |
| 4 | Tuần 4 | WP6 + WP7, chạy trên 3–5 buổi | Demo đầy đủ |
| 5 | Tuần 5 | Đánh giá tổng, nghiên cứu người dùng, báo cáo | Bản nộp |

**Bản gọn 3 tuần:** WP1 (chỉ hotwords theo slide), WP3, WP4, WP5. Bỏ hành động lời nói, WP6; báo cáo giáo viên
chỉ còn tỉ lệ nói.

## Phân công gợi ý

| Mảng | Gói việc | Người phụ trách |
|---|---|---|
| A. Tiếng nói | WP1, cắt âm thanh phát âm (WP4) | [Thành viên 1] |
| B. Hiểu buổi học | WP2, WP3 | [Thành viên 2] |
| C. Ngôn ngữ người học | WP5, WP6 | [Thành viên 3] |
| D. Sản phẩm và đánh giá | CEFR + nghĩa (WP4), WP7, nghiên cứu người dùng, điều phối nhãn | [Thành viên 4] |

## Dữ liệu

- **Đang dùng (07/11/2026):** 3 buổi TOEIC Starter (Unit 1, 4, 5) của ECE English Online, CC BY, giảng bằng tiếng
  Việt; nội dung màn hình được trích lại từ video vì không có slide gốc (xem [phase1_plan.md](phase1_plan.md)).
- 3–5 buổi học 45–90 phút. Làm ngay một **buổi đóng vai** của nhóm (không vướng quyền riêng tư), song song xin
  buổi học thật có phiếu đồng ý của giáo viên và học viên.
- Khi ghi: chia sẻ màn hình với slide toàn khung hình, bật lưu chat, bật âm thanh riêng từng người nếu Zoom cho
  phép, xin slide PDF và worksheet gốc.
- Video, âm thanh, chat gốc và tên thật **không bao giờ** đưa vào git.

## Đánh giá tổng thể

- Mỗi bài toán một chỉ số (bảng WP ở trên).
- Các bước sau WP1 chạy trên cả transcript sửa tay và transcript ASR, để đo lỗi lan truyền.
- Thí nghiệm then chốt: ASR có/không hotwords theo slide; căn chỉnh bài tập có/không thông tin slide; phương án
  nhiễu từ lỗi của lớp so với ngẫu nhiên.
- Nghiên cứu người dùng: 8–10 học viên, nhiệm vụ "tìm chỗ chữa câu n" có/không EduSync; 1–2 giáo viên đánh giá
  báo cáo.

## Rủi ro chính

| Rủi ro | Dự phòng |
|---|---|
| Không có buổi học thật | Buổi đóng vai |
| ASR chen Việt–Anh kém | Model lớn hơn trên Colab; các WP sau chạy trên transcript sửa tay |
| pyannote cần token / chậm | Âm thanh riêng của Zoom, hoặc gán tay |
| LLM bịa đáp án, phản hồi sai | Buộc chọn trong phương án; giáo viên duyệt; đo độ chính xác |
| Giấy phép danh sách CEFR, BEA-2019 | Chỉ dùng cho nghiên cứu, không phân phối lại |

## Cần chốt

1. Nguồn buổi học (thật / đóng vai) và trình độ lớp.
2. LLM: gọi API hay mô hình mở chạy trên máy.
3. Hạn nộp: bản 5 tuần hay 3 tuần.
4. Người phụ trách từng mảng.

## Tài liệu nền

- Tiếng nói: Whisper (arXiv 2212.04356), PhoWhisper (2406.02555), TSPC – ASR chen Việt–Anh (2509.05983),
  SlideSpeech (2309.05396), pyannote.audio (1911.01255).
- Lớp học: TalkMoves (2204.09652), Conversational Uptake (2106.03873), SLA-LENS (2610.24259).
- Người học: CEFR-SP (2210.11766), BEA-2019 (ACL W19-4406), ERRANT (ACL P17-1074), GECToR (2005.12592),
  phản hồi trên 20.000 bài viết EFL (2607.14591), Speak & Improve 2025 (2412.11986).
- Bài tập: CLOTH (1711.03225), RACE (1704.04683), sinh phương án nhiễu (1809.02768),
  lịch ôn tập ngắt quãng (ACL P16-1174).
