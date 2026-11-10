# KẾT QUẢ ĐÁNH GIÁ THỰC NGHIỆM (NGUỒN SỐ LIỆU DUY NHẤT)
## EduSync — đồ án NLP501

**Cập nhật:** 10/11/2026 · **Tái tạo toàn bộ số liệu:** `python eval/run_all.py` (ghi `eval/results/*.json`, `summary.json`)

Mọi con số trong slide và các tài liệu khác phải lấy từ file này. Con số nào không có ở đây thì không được trích dẫn.

---

## 1. Dữ liệu

| Bài | Nguồn | Thời lượng | Màn hình | Đoạn lời giảng | Câu hỏi trích được | Dùng để |
|---|---|---|---|---|---|---|
| ECE TOEIC Starter Unit 4 | YouTube, CC BY | 58 phút | 32 | 2.606 | 34 (2 là đoạn văn, không phải câu hỏi) | **Phát triển** (dev): chỉnh thuật toán |
| ECE TOEIC Starter Unit 5 | YouTube, CC BY | 58 phút | 32 | 1.201 | 35 | **Kiểm tra độc lập** (test): chỉ chạy 1 lần sau khi chốt thuật toán |
| ECE TOEIC Starter Unit 1 | YouTube, CC BY | 65 phút | 46 | 1.690 | — | Chỉ dùng cho ASR/trích màn hình |
| Stanford CS224N (BERT) | YouTube + slide PDF | 54 phút | 43 slide | — | — | Kiểm tra hồi quy pipeline v1 (căn chỉnh slide) |

Đặc điểm cần nói rõ khi trình bày:
- Lời giảng Unit 4: 73% đoạn tiếng Việt, 26% đoạn tiếng Anh, 5 đoạn trộn mã (phân loại theo mật độ chữ có dấu).
- **Chỉ có một người nói** (giáo viên). Vì vậy **không đo được TTT/STT**; báo cáo hiển thị "chưa đo" thay vì 100%/0%.
- **Log chat (17 tin nhắn, 5 học viên) là dữ liệu mô phỏng** do nhóm soạn để minh họa luồng chat → sửa lỗi → báo cáo; bài giảng YouTube không có chat.
- Nội dung trích từ bài giảng (đề bài, lời giảng) không đưa lên git vì đề bài lấy từ sách của nhà xuất bản (`.gitignore`).

## 2. Bộ nhãn chuẩn (gold) — đều là bản nháp, cần nhóm kiểm tra

| File | Nội dung | Ai gán | Trạng thái |
|---|---|---|---|
| `lessons/ece-toeic-starter-u4/gold/alignment_gold.json` | Mốc bắt đầu chữa của 32/34 câu + mốc giảng lý thuyết của 4 chủ điểm | AI (Claude), đọc transcript, không xem output hệ thống | `verified: false` |
| `lessons/ece-toeic-starter-u5/gold/alignment_gold.json` | Mốc bắt đầu chữa của 35/35 câu (cùng hướng dẫn gán nhãn) | AI, như trên | `verified: false` |
| `lessons/ece-toeic-starter-u4/gold/concept_gold.json` | Chủ điểm của 34 câu: gp_1..gp_4 hoặc "none" (12 câu có chủ điểm, 22 câu none) | AI, như trên | `verified: false` |
| `eval/gold/gec_heldout.json` | 70 câu kiểu chat của học viên (44 có lỗi trong 6 nhóm, 10 lỗi khác, 16 câu đúng) | AI, viết độc lập, không xem luật | `verified: false` |
| `lessons/ece-toeic-starter-u4/gold/asr/` | 5 clip × 2 phút + bản chép | Bản nháp từ ASR, **chưa sửa tay** | `corrected: false` |

**Việc nhóm cần làm trước khi bảo vệ:** mở video ở các mốc trong `alignment_gold.json` (67 câu, khoảng 1 giờ) và sửa chỗ sai, đọc lại 34 nhãn chủ điểm và 70 câu GEC, rồi đặt `verified: true` và chạy lại `eval/run_all.py`.

## 3. Căn chỉnh câu hỏi ↔ lời giảng (`exercise_align.py`)

Độ đo: tỉ lệ câu có mốc dự đoán lệch ≤10 s / ≤30 s so với nhãn; sai số tuyệt đối; số lần đảo thứ tự.

| Phương pháp | Dev U4: ±10 s | ±30 s | Sai số TB | Test U5: ±10 s | ±30 s | Sai số TB | Đảo thứ tự (U5) |
|---|---|---|---|---|---|---|---|
| Thời điểm màn hình xuất hiện | 18,8% | 21,9% | 91,7 s | 48,6% | 62,9% | 33,3 s | 0 |
| Regex "câu N" đầu tiên | 71,9% | 78,1% | 28,1 s | 71,4% | 80,0% | 21,3 s | 2 |
| **v1 (commit 73d9a62)** | 65,6% | 81,2% | 24,6 s | 57,1% | 71,4% | 28,5 s | 2 |
| Greedy (điểm số mới) | 68,8% | 84,4% | 10,5 s | 77,1% | 88,6% | 8,6 s | 0 |
| DP (điểm số mới) | 68,8% | 84,4% | 10,5 s | 77,1% | 88,6% | 8,6 s | 0 |
| **DP + lùi mốc (bản hiện tại)** | **68,8%** | **84,4%** | **10,0 s** | **80,0%** | **88,6%** | **8,1 s** | **0** |

Những thay đổi so với v1 (chỉnh trên U4, rồi kiểm tra trên U5):
1. Regex nhận thêm "câu thứ N", "câu hỏi số N", số đọc bằng chữ ("câu thứ tư"); loại "part N".
2. **Xác minh khẩu lệnh bằng ngữ cảnh:** "câu N" chỉ được 25 điểm nếu trong 60 s sau đó cô nói ít nhất một từ của chính câu hỏi; nếu không thì chỉ được 2 điểm. Lý do: ở U4 cô chữa Exercise A trong sách ("câu số 1, 2") trong khi màn hình chiếu Exercise B.
3. Bỏ stopword khi tính độ trùng từ.
4. **Lùi mốc về đầu đoạn chữa:** lùi qua các đoạn ngay trước đó có chung từ với câu hỏi (cô thường đọc đề trước rồi mới nói số câu).
5. Câu không khớp được rơi về thời điểm màn hình, nhưng bị kẹp giữa hai câu kề nhau, nên không còn đảo thứ tự.
6. Bộ giải mã là **quy hoạch động thật**: `D[k][j] = s(k,j) + max(0, max{D[k'][j'] : k'<k, t(j')<t(j)})`, tối ưu toàn cục và cho phép bỏ qua câu. *Trên cả hai bài, DP chọn giống greedy*; phần cải thiện đến từ cách tính điểm, bước lùi mốc và cách xử lý câu không khớp. DP chỉ khác greedy khi có xung đột (có test minh họa trong `tests/test_exercises.py`).

Lỗi còn lại chủ yếu ở các chỗ trống trong đoạn văn (Part 6/7): cô đọc liền cả đoạn nên "lúc bắt đầu câu" vốn không rõ (nhãn ghi mốc thay thế lệch 5–40 s).

## 4. Liên kết câu hỏi ↔ chủ điểm ngữ pháp (`concept_link.py`)

34 câu của U4, 4 chủ điểm. Câu được gắn với chủ điểm có điểm cao nhất nếu điểm ≥ ngưỡng; ngược lại là "none". Ngưỡng chọn bằng leave-one-out (mỗi câu được chấm bằng ngưỡng tối ưu trên 33 câu còn lại).

| Phương pháp | Độ chính xác (34 câu) | Link precision | Link recall | acc@1 trên 12 câu có chủ điểm |
|---|---|---|---|---|
| Luôn trả lời "none" | 73,5% | — | — | — |
| TF-IDF | 82,4% | 85,7% | 58,3% | 83,3% |
| BM25 | 70,6% | 57,1% | 41,7% | 91,7% |
| **MiniLM + từ khóa viết tay (v1)** | 76,5% | 72,7% | 58,3% | 66,7% |
| MiniLM, bỏ từ khóa viết tay | 61,8% | 33,3% | 25,0% | 50,0% |
| paraphrase-multilingual-MiniLM | 76,5% | 71,4% | 50,0% | 75,0% |
| multilingual-e5-small | 85,3% | 80,0% | 75,0% | 91,7% |
| **multilingual-e5-small + lời giảng (bản hiện tại)** | **91,2%** | **83,3%** | **83,3%** | **91,7%** |

Đầu ra thực tế (ngưỡng cố định, đúng như demo hiển thị):

| | Độ chính xác | Link precision | Link recall | Số badge |
|---|---|---|---|---|
| v1 (demo cũ) | 58,8% | 39,1% | 66,7% | 23 |
| Bản hiện tại (ngưỡng 0,835) | **91,2%** | **90,0%** | **75,0%** | 10 |

Nhận xét:
- v1 dựa vào từ khóa viết tay, trong đó có cả từ đáp án (`central`, `luxury`, `shined`…). Bỏ từ khóa thì MiniLM tụt từ 76,5% xuống 61,8%. MiniLM là mô hình chỉ tiếng Anh, trong khi phần giải thích chủ điểm bằng tiếng Việt.
- Bản hiện tại không dùng từ khóa viết tay. Nó cộng thêm **lời giảng của cô trong đoạn chữa câu** (tín hiệu đa phương thức: cô nói "thêm ing hay ed để làm tính từ", "công thức nhờ vả") và dùng mô hình đa ngữ.
- **Hạn chế:** các ví dụ trong `grammar_points.json` do Gemini sinh ra (Gemini được xem 10 câu đầu của bài), nên một số ví dụ gần như chép lại câu hỏi ("The movie was very moving.", "He has his shoes shined every day."). Điều này có lợi cho mọi phương pháp dùng văn bản chủ điểm, nên số liệu có thể lạc quan hơn trên bài mới.
- **Hạn chế:** mô hình và ngưỡng được chọn trên chính 34 câu này, nên kết quả có thể lạc quan. Điểm của hai nhóm "có chủ điểm" và "none" khá sát nhau (0,81–0,86), nên khi sang bài mới cần hiệu chỉnh lại ngưỡng. Chưa có tập kiểm tra độc lập cho bài toán này.

## 5. Mốc thời gian phần lý thuyết (`neural_ie.py --ground-only`)

Gemini chỉ thấy khoảng 30 đoạn lời giảng lấy mẫu nên mốc nó trả về là đoán. Bản hiện tại neo lại mỗi chủ điểm vào cửa sổ lời giảng (6 đoạn) giống chủ điểm nhất theo multilingual-e5-small.

| Chủ điểm | Nhãn | v1 (Gemini) | Sai số v1 | Bản hiện tại | Sai số |
|---|---|---|---|---|---|
| gp_1 Participles | 00:24 | 15:06 | 882,7 s | 00:44 | 20,0 s |
| gp_2 Causative | 15:46 | 17:14 | 88,1 s | 15:38 | 7,5 s |
| gp_3 Passive / require that | 13:16 | 55:02 | 2.505,6 s | 13:18 | 2,3 s |
| gp_4 Noun modifiers | 07:20 | 08:13 | 53,5 s | 07:35 | 14,9 s |
| **Trung bình** | | | **882,5 s** | | **11,2 s** |

## 6. Phát hiện lỗi người học trong chat (`feedback.py`)

Bộ phát hiện dựa trên luật cho 6 nhóm lỗi chuyển di L1, không phải mô hình GEC tổng quát. Đánh giá trên 70 câu viết độc lập với luật.

| | Precision (cấp câu) | Recall (cấp câu) | F1 |
|---|---|---|---|
| v1 (khớp nguyên văn câu, commit 73d9a62) | 90,0% | 20,5% | 33,3% |
| **Bản hiện tại** | **100%** | **72,7%** | **84,2%** |

| Nhóm | Nhãn ERRANT mặc định | Số câu | Precision | Recall |
|---|---|---|---|---|
| BE_VERB ("I am agree") | U:VERB:TENSE | 8 | 100% | 50,0% |
| PARTICIPLE ("the movie was moved") | R:VERB:FORM | 8 | 100% | 87,5% |
| CAUSATIVE ("have my car repair") | R:VERB:FORM | 8 | 100% | 75,0% |
| MODAL_TO ("should to increase") | U:VERB:FORM | 8 | 100% | 100% |
| SVA ("it make me cry") | R:VERB:SVA | 8 | 100% | 62,5% |
| WH_DO ("Why we use…?") | M:VERB:TENSE | 7 | 100% | 42,9% |

- Sửa đúng nguyên câu: 65,9% (44 câu chỉ có lỗi trong phạm vi). Không báo nhầm câu nào trong 10 câu có lỗi ngoài phạm vi (bộ này không bắt các lỗi đó).
- Bộ 70 câu đã được xem **một lần** để sửa 3 lỗi cài đặt (dạng rút gọn I'm/can't, cách lấy từ đứng trước trong luật SVA, động từ đa nghĩa như "like/open"). Không thêm luật mới để khớp tập này.
- **Nhãn ERRANT đã được kiểm chứng** bằng thư viện chính thức errant 3.0.2 (`eval/errant_check.py`, kết quả ở `eval/results/errant_check.txt`). errant có thể cho nhãn lân cận với các cặp câu khác (ví dụ R:MORPH cho "confusing → confused", R:OTHER cho "don't → doesn't"). Nếu cài `errant`, `feedback.py` sẽ tự gán nhãn bằng errant.
- Trên 17 tin nhắn mô phỏng của U4: phát hiện 7 lỗi trong 6 tin nhắn. Con số này không dùng để đo chất lượng vì chat được soạn kèm các lỗi mẫu.

## 7. Nhận dạng tiếng nói (ASR)

**Chưa có WER thật.** Bản chép tham chiếu của 5 clip (10 phút) chưa được sửa tay (`corrected: false`), nên mọi WER hiện tại chỉ là so ASR với ASR. Chỉ số gián tiếp (Unit 4, toàn bài):

| Cấu hình `transcribe.py` | Số đoạn | Lặp liên tiếp | Từ trên màn hình được nói ra (proxy) |
|---|---|---|---|
| Không gợi ý (đang dùng làm `transcript.json`) | 2.606 | 6 | 47% |
| Cắt theo màn hình, không gợi ý (đối chứng) | 545 | 3 | 48% |
| Gợi ý từ OCR (hotwords = từ) | 484 | 20 | 52% |
| Gợi ý từ OCR (hotwords = dòng) | 559 | 27 | 52% |

- Gợi ý từ màn hình tăng proxy thêm khoảng 4 điểm so với đối chứng, nhưng **làm tăng số đoạn lặp** (một dấu hiệu ảo giác). Proxy này cũng có thể tăng do Whisper "chép" từ gợi ý dù cô không nói. Vì vậy chưa kết luận được, và pipeline vẫn dùng bản không gợi ý.
- Gợi ý được truyền qua tham số `hotwords` của faster-whisper, không phải `initial_prompt`.
- Việc cần làm: sửa tay 5 clip trong `gold/asr/`, đặt `"corrected": true`, chạy `python eval/wer.py --lesson lessons/ece-toeic-starter-u4 results/asr_none.json results/asr_chunks.json results/asr_words.json`.

## 7b. Từ vựng (`vocab.py`) — chỉ có thống kê, chưa đánh giá chất lượng

- Unit 4: 80 từ, gồm A1 26, A2 26, B1 18, B2 9, C1 1 (tra từ điển CEFR-J + Octanove, 8.845 mục).
- 52/80 từ có nghĩa tiếng Việt khai thác từ lời giảng theo mẫu "X là / nghĩa là …". Độ đúng của các nghĩa này **chưa được kiểm tra**.
- 79 clip phát âm `.wav` dài 0,7–2,2 s, cắt theo ranh giới đoạn ASR có chứa từ (ưu tiên đoạn chỉ có một từ). Transcript không có timestamp từng từ.

## 8. Kiểm thử hồi quy & phần mềm

- CS224N (pipeline v1 căn chỉnh slide PDF): 9/10 mốc chuyển slide có nhãn được tìm thấy, sai số trung bình 0,6 s (`python evaluate.py --lesson lessons/cs224n-bert gold/labels.json alignment.json`).
- `pytest`: **71/71 test** pass. Test không còn ghi vào `lessons/` (dùng `tmp_path`).

## 9. Các con số đã rút khỏi tài liệu cũ

| Khẳng định cũ | Lý do rút |
|---|---|
| WER thuật ngữ 18,4% → 9,2%, "triệt tiêu ảo giác" | Không có kết quả đo nào trong repo; bản tham chiếu chưa sửa; số đoạn lặp tăng khi có gợi ý |
| Recall 34/34 (100%), Precision 97,1%, sai số ≤1,8 s | "34/34" chỉ là độ phủ (câu nào cũng có mốc), không có nhãn để đo; 97,1% mâu thuẫn với recall 100%; sai số thật được báo ở mục 3 |
| 4,2 ms/câu | Chưa từng được đo |
| Bắt đúng 6/6 lỗi (100%) | Chat được soạn khớp đúng với regex; nay thay bằng tập 70 câu độc lập (mục 6) |
| U:VERB:BE, R:ADJ:PARTICIPLE, M:VERB:AUX, U:PREP, "ERRANT (ACL 2019)" | Không phải nhãn ERRANT; ERRANT là ACL 2017; nhãn hiện tại kiểm chứng bằng errant 3.0.2 |
| TTT 98,2% / 100%, STT 1,8% / 0% | Bản ghi có một người nói nên không đo được |
| "Chuẩn FERPA" | FERPA là luật Mỹ về hồ sơ học vụ; hệ thống chỉ ẩn danh hoá tên (S1…SN) |
| Kế hoạch hành động "tự động sinh" | Trước đây là văn bản viết sẵn; nay là câu mẫu điền từ dữ liệu (lỗi, chủ điểm, TTT) |
| "Tỷ lệ căn chỉnh 95,6%" trong demo | Giá trị viết cứng trong `demo/index.html`; nay hiển thị số câu khớp được với lời giảng (33/34) |
| Video 63 phút; 79 từ vựng (A1 28/A2 19/B1 18/B2 12/C1 2) | Thực tế 58 phút; `vocab.json` có 80 từ (A1 26/A2 26/B1 18/B2 9/C1 1) |
| 4.950 dòng code | Trước khi sửa: 3.456 dòng Python (cả test). Hiện tại: 4.454 dòng Python (code + test + eval), 6.461 dòng nếu tính `demo/index.html` |
