# MA TRẬN THIẾT KẾ CHI TIẾT TỪNG TÍNH NĂNG & ÁNH XẠ KỸ THUẬT NLP (FEATURE & TECHNICAL NLP MATRIX)
## EDUSYNC: ĐỒNG BỘ ĐA PHƯƠNG THỨC & PHÂN TÍCH SƯ PHẠM BÀI GIẢNG LUYỆN THI TIẾNG ANH (THỬ NGHIỆM TRÊN TOEIC)
**Môn học:** Xử lý Ngôn ngữ Tự nhiên Nâng cao (NLP501 - Master of Software Engineering)  
**Nhánh Git:** `edusync-v2`  
**Cập nhật:** 10/11/2026  
**Nguồn số liệu:** [`10_evaluation_results.md`](10_evaluation_results.md) (tái tạo bằng `python eval/run_all.py`)

---

## 💡 Điểm nhấn Trình bày với Giảng viên (Feature-to-NLP Mapping)

> Tài liệu này đối chiếu **10 tính năng** với **kỹ thuật NLP**, **file mã nguồn**, **test tự động** (`pytest`) và **kết quả đo** tương ứng, để chỉ ra ngay khi giảng viên yêu cầu chứng minh từng phần.
> - Cột "Test" cho biết số test kiểm tra **tính đúng của mã** (hàm trả về đúng trên ví dụ nhỏ); test pass **không** có nghĩa là tính năng chính xác trên dữ liệu thật. Chất lượng trên dữ liệu thật nằm ở cột "Kết quả đo", lấy từ docs/10.
> - Nhãn gold dùng để đo đều là **bản nháp** (`verified: false`). Log chat Unit 4 là **dữ liệu mô phỏng**. Chỉ dùng dữ liệu TOEIC.

---

## 1. Bảng Ma trận 10 Tính năng

| Mã | Tính năng | Kỹ thuật NLP áp dụng | File mã nguồn | Test (số test) | Kết quả đo (docs/10) |
| :-: | :--- | :--- | :--- | :--- | :--- |
| **F-01** | **ASR đa ngữ Việt–Anh & gắn nhãn ngôn ngữ** | • `faster-whisper` `large-v3-turbo`, chế độ đa ngữ; `initial_prompt` là lời nhắc tĩnh của bài (`lesson.json`).<br>• `--vad auto` (mặc định): tự bỏ lọc VAD khi VAD giữ dưới 25% audio (video có nhạc nền).<br>• Tuỳ chọn `--screen-hints words\|lines`: từ / dòng tiếng Anh OCR trên màn hình đang chiếu được truyền vào tham số **`hotwords`**; `chunks` là đối chứng cắt theo màn hình không gợi ý.<br>• Nhãn `vi` / `en` / `mixed` theo tỉ lệ từ có dấu tiếng Việt (> 0,3 / 0 / còn lại).<br>• WER (căn chỉnh Levenshtein theo từ) trong `eval/wer.py`. | `transcribe.py`<br>`eval/wer.py`<br>`eval/asr_screen_terms.py` | `test_text_lang.py` (3)<br>`test_screen_hints.py` (4)<br>`test_wer.py` (5) | **Chưa có WER thật** (5 clip tham chiếu chưa sửa tay). Proxy: gợi ý tăng tỉ lệ từ trên màn hình được nói ra 48% → 52% nhưng tăng đoạn lặp 3 → 20–27; `transcript.json` dùng bản không gợi ý. U4: 73% đoạn vi, 26% en, 5 đoạn trộn mã. Nhãn `vi`/`en`/`mixed` chỉ dùng được cho bài giảng Việt–Anh (lời giảng tiếng Nhật bị gắn `en`). VAD giữ 97% audio ở U1/U4/U5 nên `--vad auto` không đổi transcript của các bài này. |
| **F-02** | **Trích màn hình đề bài & tách câu hỏi** | • Phát hiện chuyển màn hình: so khác biệt điểm ảnh của khung hình thu nhỏ, làm mờ Gaussian; giữ khung hình ổn định cuối cùng của mỗi màn hình.<br>• OCR Việt + Anh bằng Apple Vision (`ocrmac`).<br>• Regex tách đề (stem) và lựa chọn A–D, loại trùng lặp; số câu 1–3 chữ số (TOEIC 101–200) và nhãn "Number / Question / Câu N". | `extract_screens.py`<br>`exercises.py` | `test_exercises.py` (6 / 11: tách đề & lựa chọn kiểu `(A)` và `A.`, loại trùng; nhận số câu TOEIC Part 7 (147/148); nhận nhãn "Number 7" / "Question 8:"; không lấy năm / số lượng như "2016, Test 1", "200 customers" làm số câu) | U4: 32 màn hình, 34 bản ghi câu hỏi (2 là đoạn văn, không phải câu hỏi). U5: 32 màn hình, 35 câu. Video của 6 kênh khác (6 bài giảng, 45 câu): tìm được **44,4%** số câu (đóng băng) → 55,6% sau khi sửa (không còn là kiểm tra độc lập; U4/U5 không đổi); hỏng với bảng viết tay, bảng cuộn, câu chỉ có tranh/audio, ví dụ không đánh số. Độ chính xác OCR chưa đo riêng. |
| **F-03** | **Căn chỉnh câu hỏi ↔ lời giảng (quy hoạch động đơn điệu)** | • Điểm = 25·khẩu lệnh "câu N" (chỉ 2 nếu 60 s sau không có từ nào của câu hỏi) + 2·số từ nội dung trùng + 3·đang trên màn hình.<br>• Regex nhận "câu (số\|thứ\|hỏi số) N", số đọc bằng chữ; loại "text/page/part/trang N" bằng negative lookbehind.<br>• DP đơn điệu `D[k][j] = s(k,j) + max(0, max D[k'][j'])`, cho phép bỏ qua câu; lùi mốc về đầu đoạn chữa; câu không khớp lấy thời điểm màn hình, kẹp giữa hai câu kề nhau. | `exercise_align.py` | `test_exercises.py` (5 / 11: đơn điệu, DP tìm tối ưu toàn cục khi greedy sai, hạ điểm khẩu lệnh không được xác minh, số thứ tự / số đọc bằng chữ, câu không khớp giữ thứ tự) | Mốc lệch ≤10 s: dev U4 **68,8%**, test U5 **80,0%** (v1: 65,6% / 57,1%; chỉ regex "câu N" đầu tiên: 71,9% / 71,4%, nhưng sai số TB 28,1 s / 21,3 s); ±30 s: 84,4% / 88,6%; sai số TB 10,0 s / 8,1 s; 0 lần đảo thứ tự. DP chọn giống greedy trên cả hai bài. U5 cùng nguồn với U4. Video của 6 kênh khác (docs/10 §3b), hệ thống đóng băng: 6 bài giảng (45 câu) đầu-cuối ±10 s **17,8%** (v1: 8,9%); cho trước danh sách câu đúng: DP 57,8%, greedy 24,4%, regex 24,4%, v1 35,6%. 2 video luyện tập (23 câu): đầu-cuối 8,7%, cho trước danh sách câu đúng 78,3%. |
| **F-04** | **Từ vựng phân bậc CEFR & clip phát âm** | • Lemmatizer 2 lớp: bảng bất quy tắc + cắt hậu tố.<br>• Tra từ điển CEFR-J + Octanove (8.845 mục).<br>• Lọc đồng âm Việt–Anh không dấu (`VI_HOMOPHONES`).<br>• Trích nghĩa tiếng Việt từ lời giảng theo mẫu "X là / nghĩa là …".<br>• Cắt clip `.wav` theo ranh giới đoạn ASR chứa từ (không có timestamp từng từ). | `vocab.py` | `test_vocab.py` (8) | U4: 80 từ (A1 26, A2 26, B1 18, B2 9, C1 1); 52 từ có nghĩa tiếng Việt; 79 clip 0,7–2,2 s. **Chưa đánh giá chất lượng.** |
| **F-05** | **Đọc chat Zoom/Meet & ẩn danh hoá học viên** | • Tách giờ / người gửi / nội dung theo định dạng chat Zoom/Meet.<br>• **Ẩn danh hoá** (pseudonymization) tên thành `S1…SN`.<br>• Nhận số câu ("câu 4") và đáp án ("em chọn C"); nối với câu gần nhất có số đó theo thời gian căn chỉnh (số câu bắt đầu lại ở mỗi phần). | `chat_parser.py` | `test_feedback.py` (6 / 26: đọc mốc giờ, đọc chat Zoom, ẩn danh, nối chat ↔ câu hỏi, nhận đáp án, nối câu gần nhất cùng số) | U4: 17 tin nhắn **mô phỏng**, 5 học viên → `S1..S5`. Không đo độ chính xác của bước nối chat ↔ câu hỏi. |
| **F-06** | **Phát hiện lỗi người học trong chat (dựa trên luật) + loại lỗi ERRANT** | • Luật cho 6 nhóm lỗi chuyển di L1: BE_VERB, PARTICIPLE, CAUSATIVE, MODAL_TO, SVA, WH_DO; đề xuất câu sửa và giải thích tiếng Việt.<br>• Mỗi lỗi kèm loại lỗi ERRANT (Bryant, Felice & Briscoe, ACL 2017): mặc định `U:VERB:TENSE`, `R:VERB:FORM`, `R:VERB:FORM`, `U:VERB:FORM`, `R:VERB:SVA`, `M:VERB:TENSE`, kiểm chứng bằng errant 3.0.2; nếu cài `errant` thì errant tự gán.<br>• Không phải mô hình GEC tổng quát. | `feedback.py`<br>`eval/eval_gec.py`<br>`eval/errant_check.py` | `test_feedback.py` (20 / 26: 8 test phát hiện & tổng quát hoá từng nhóm, 12 câu đúng không được báo lỗi) | 70 câu viết độc lập với luật: P **100%**, R **72,7%**, F1 **84,2%** (v1: P 90,0%, R 20,5%); sửa đúng nguyên câu 65,9%. Trên chat mô phỏng U4: 7 lỗi / 6 tin (chỉ minh họa). |
| **F-07** | **Trích chủ điểm ngữ pháp & mẹo thi (IE lai)** | • Gemini `gemini-3.5-flash-lite` ở **JSON mode** (`responseMimeType=application/json`), kiểm tra các trường sau khi parse; thấy khoảng 30 đoạn lời giảng lấy mẫu.<br>• Fallback offline: bộ phân loại ngữ pháp TOEIC chung, khớp theo cụm từ gợi ý trong lời giảng (không bịa nội dung).<br>• Neo mốc lý thuyết vào cửa sổ 6 đoạn lời giảng giống chủ điểm nhất theo `multilingual-e5-small` (`--ground-only`). | `neural_ie.py` | `test_neural_ie.py` (7) | U4: 4 chủ điểm; mốc lý thuyết sai số TB **11,2 s** (Gemini một mình: 882,5 s). Nội dung công thức / mẹo chưa được đánh giá. |
| **F-08** | **Liên kết câu hỏi ↔ chủ điểm ngữ pháp** | • Bi-encoder `intfloat/multilingual-e5-small` (384 chiều, chuẩn hóa L2, tiền tố `query:` / `passage:`).<br>• Điểm = trung bình cos(câu hỏi, chủ điểm) và cos(lời giảng trong đoạn chữa câu, chủ điểm); gắn khi ≥ 0,835, ngược lại "none".<br>• Dự phòng TF-IDF; đã bỏ từ khóa viết tay `KEYWORD_CUES` (rò rỉ đáp án). | `concept_link.py`<br>`eval/eval_concepts.py` | `test_concept_link.py` (4: không còn `KEYWORD_CUES`, cửa sổ lời giảng dừng ở câu kế tiếp, TF-IDF dự phòng, chạy trên bản sao bài thật) | 34 câu U4: độ chính xác **91,2%** (luôn none 73,5%, TF-IDF 82,4%, v1 76,5%); ngưỡng cố định: P 90,0%, R 75,0%, 10 badge. Chọn trên chính tập này, chưa có test độc lập. |
| **F-10** | **Web demo tương tác** | • SPA một trang, 5 tab: Exercises / Grammar / Vocab / Chat & GEC / Screens; `?tab=<id>` mở thẳng một tab.<br>• Tua video qua HTTP Range (`RangeHTTPServer`).<br>• Ô tìm kiếm chuỗi con trên 5 nguồn (lời giảng, bài tập, từ vựng, chat, chủ điểm).<br>• Badge chủ điểm chỉ hiện trên câu được gắn (10/34). | `demo/index.html`<br>`demo/prepare.py` | Không có test tự động; kiểm tra thủ công theo kịch bản trong [`06_user_guide_and_demo.md`](06_user_guide_and_demo.md) | Hiển thị số câu khớp được với lời giảng (33/34) thay cho con số "95,6%" viết cứng trước đây. |

**Tổng:** 10 tệp test, **75 test** (3 + 4 + 5 + 11 + 8 + 26 + 7 + 4 + 3 + 4), tất cả pass. Không test nào ghi vào `lessons/` (dùng `tmp_path`).

---

## 2. Bộ Đánh giá Tái lập (`eval/`)

| Script | Đo gì | Mục trong docs/10 |
| :--- | :--- | :--- |
| `eval/run_all.py` | Chạy toàn bộ đánh giá, ghi `eval/results/*.json` và `summary.json`; baseline v1 = commit `73d9a62` | Tất cả |
| `eval/eval_alignment.py` | Căn chỉnh câu hỏi: thời điểm màn hình, regex "câu N" đầu tiên, v1, greedy, DP, DP + lùi mốc; dev U4, test U5 | §3 |
| `eval/eval_multisource.py` | Bộ test đa nguồn (8 video, 6 kênh, 68 câu): trích câu, căn chỉnh đầu-cuối và căn chỉnh khi cho trước danh sách câu đúng | §3b |
| `eval/eval_concepts.py` | Liên kết chủ điểm (TF-IDF, BM25, MiniLM ± từ khóa, multilingual MiniLM, e5-small ± lời giảng; ngưỡng leave-one-out) và mốc lý thuyết | §4, §5 |
| `eval/eval_gec.py` | Phát hiện lỗi chat trên 70 câu viết độc lập (`eval/gold/gec_heldout.json`) | §6 |
| `eval/errant_check.py` | Loại lỗi ERRANT mà errant 3.0.2 gán cho cặp câu mẫu của từng nhóm | §6 |
| `eval/asr_clips.py`, `eval/wer.py` | Cắt 5 clip tham chiếu; WER khi bản chép đã được sửa tay (`corrected: true`) | §7 |
| `eval/asr_screen_terms.py` | Chỉ số gián tiếp của ASR khi chưa có tham chiếu: số đoạn, đoạn lặp, tỉ lệ từ trên màn hình được nói ra | §7 |

---

## 3. Thống kê Khối lượng Mã nguồn & Kiểm thử

- **Mã nguồn Python:** 4.559 dòng (code + test + eval); 6.566 dòng nếu tính cả `demo/index.html`.
- **Kiểm thử tự động (`pytest`):** **75/75 test pass**, 10 tệp trong `tests/`.
- **Tài liệu (`docs/`):** 10 tài liệu đánh số 01–10; [`10_evaluation_results.md`](10_evaluation_results.md) là nguồn số liệu duy nhất.
