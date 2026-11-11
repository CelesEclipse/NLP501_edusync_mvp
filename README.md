# EduSync: Đồng bộ Đa phương thức & Phân tích Sư phạm cho Bài giảng Luyện thi Tiếng Anh (thử nghiệm trên TOEIC)

**EduSync** là pipeline Xử lý Ngôn ngữ Tự nhiên (NLP) đa phương thức biến bản ghi một buổi học luyện thi tiếng Anh trực tuyến (Zoom / Google Meet / YouTube) thành **sổ tay học tập tương tác cho học viên** (bấm câu hỏi để tua tới lúc cô chữa, liên kết câu hỏi với lý thuyết, từ vựng CEFR).

Dữ liệu thử nghiệm: 3 bài **ECE TOEIC Starter** (YouTube, CC BY; Unit 4 = 58 phút, một giáo viên giảng). Log chat của Unit 4 (17 tin nhắn, 5 học viên) là **dữ liệu mô phỏng** do nhóm soạn. IELTS chỉ là hướng mở rộng, chưa có dữ liệu hay kết quả nào.

**Bộ test đa nguồn** (`eval/eval_multisource.py`, docs/10 §3b): 8 video TOEIC tiếng Việt của 6 kênh YouTube khác ECE (CC BY, 3 giờ 9 phút, 68 câu có nhãn) để kiểm tra tổng quát hóa. Trên video của giáo viên khác, căn chỉnh chỉ đúng 17,8% (±10 s), so với 80,0% trên Unit 5 cùng nguồn. Các bài này nằm trong `lessons/toeic-*/` và không đưa lên git, trừ `lesson.json`. `fetch_lesson.py` chỉ tải video có giấy phép mở (hoặc `--allow-standard` khi có phép của chủ sở hữu); nó đọc giấy phép CC theo cách ghi của YouTube, Vimeo, Internet Archive và PeerTube, và có `--cookies-from-browser` cho trang cần đăng nhập.

---

## 📚 Bộ Tài liệu của Đồ án (`docs/`)

Tài liệu của đồ án môn **Xử lý Ngôn ngữ Tự nhiên Nâng cao (NLP501 - MSE)** nằm trong [`docs/`](docs/). **Mọi con số đều lấy từ [`docs/10_evaluation_results.md`](docs/10_evaluation_results.md)**; con số không có ở đó thì không được trích dẫn.

| STT | Tài liệu | Mô tả |
| :---: | :--- | :--- |
| 📖 | [**`docs/README.md`**](docs/README.md) | Mục lục & bản đồ 7 kỹ thuật NLP ↔ tính năng |
| ⭐ | [**`10_evaluation_results.md`**](docs/10_evaluation_results.md) | **Kết quả đánh giá thực nghiệm — nguồn số liệu duy nhất** (dữ liệu, nhãn gold nháp, căn chỉnh, liên kết chủ điểm, GEC, ASR, các con số đã rút) |
| ⭐ | [**`09_teacher_presentation_and_technical_nlp_guide.md`**](docs/09_teacher_presentation_and_technical_nlp_guide.md) | Cẩm nang trình bày cho giảng viên, 7 điểm Technical NLP & câu hỏi phản biện |
| 01 | [**`01_project_proposal.md`**](docs/01_project_proposal.md) | Đề xuất đề tài: bài toán, câu hỏi nghiên cứu & kết quả đo được |
| 02 | [**`02_nlp_architecture_and_literature.md`**](docs/02_nlp_architecture_and_literature.md) | Cơ sở lý thuyết NLP & tổng quan nghiên cứu |
| 03 | [**`03_requirements_analysis_srs.md`**](docs/03_requirements_analysis_srs.md) | Đặc tả & phân tích yêu cầu phần mềm (SRS) |
| 04 | [**`04_detailed_design_and_qa_plan.md`**](docs/04_detailed_design_and_qa_plan.md) | Thiết kế chi tiết (SDD) & kế hoạch kiểm soát chất lượng |
| 05 | [**`05_solution_dense_embeddings_guide.md`**](docs/05_solution_dense_embeddings_guide.md) | Chuyên đề: liên kết câu hỏi ↔ chủ điểm ngữ pháp bằng `multilingual-e5-small` + lời giảng (kèm bảng ablation) |
| 06 | [**`06_user_guide_and_demo.md`**](docs/06_user_guide_and_demo.md) | Kịch bản demo 90 giây & hướng dẫn sử dụng web demo |
| 07 | [**`07_feature_detailed_design_matrix.md`**](docs/07_feature_detailed_design_matrix.md) | Ma trận 10 tính năng ↔ kỹ thuật NLP ↔ mã nguồn ↔ test |
| 08 | [**`08_presentation_slides_and_speaker_notes.md`**](docs/08_presentation_slides_and_speaker_notes.md) | Kịch bản slide thuyết trình & lời thoại cho 4 thành viên |
| 🖥️ | [**`docs/slides.html`**](docs/slides.html) | Slide thuyết trình: bản xuất Marp (18 slide) của `presentation/slides_marp.md`; lời thoại ở `08_presentation_slides_and_speaker_notes.md` |

---

## 🚀 Khởi chạy Nhanh: Kiểm thử, Đánh giá & Web Demo

```bash
# 1. Kích hoạt môi trường ảo
source .venv/bin/activate

# 2. Chạy bộ kiểm thử tự động (75 test, không test nào ghi vào lessons/)
pytest -v

# 3. Tái tạo toàn bộ số liệu trong docs/10 (ghi eval/results/*.json và summary.json)
python eval/run_all.py                 # thêm --skip-concepts để bỏ phần nạp 3 mô hình embedding (~1-2 phút)

# 4. Nạp bài TOEIC Unit 4 vào thư mục demo và mở web server (hỗ trợ HTTP Range để tua video)
python demo/prepare.py --lesson lessons/ece-toeic-starter-u4
cd demo && ../.venv/bin/python -m RangeHTTPServer 8000
# Mở trình duyệt tại: http://localhost:8000/
```

**Mẹo khi trình bày:** mở thẳng một tab bằng tham số `?tab=`, ví dụ `http://localhost:8000/?tab=tab-stats`. Các giá trị hợp lệ: `tab-exercises`, `tab-grammar`, `tab-vocab`, `tab-chat`, `tab-screens`.

---

## 🧠 Tóm tắt 7 Điểm Áp dụng Kỹ thuật NLP

Số liệu dưới đây lấy từ [`docs/10_evaluation_results.md`](docs/10_evaluation_results.md). Nhãn gold đều là **bản nháp** (do AI gán, không xem output hệ thống, `verified: false`), nhóm cần kiểm tra lại.

1. **ASR đa ngữ + thử nghiệm gợi ý từ màn hình (`transcribe.py`):** `faster-whisper` `large-v3-turbo` chế độ đa ngữ; `initial_prompt` là lời nhắc tĩnh của bài (trong `lesson.json`). Tuỳ chọn `--screen-hints` truyền từ OCR trên màn hình vào tham số **`hotwords`** của faster-whisper. **Chưa đo được WER** (bản chép tham chiếu 5 clip chưa sửa tay). Chỉ số gián tiếp: gợi ý tăng tỉ lệ từ trên màn hình được nói ra khoảng 4 điểm (48% → 52%) nhưng làm tăng số đoạn lặp (3 → 20–27), nên `transcript.json` đang dùng là bản **không gợi ý**.
2. **Nhận diện trộn mã Việt–Anh & lọc đồng âm (`transcribe.py`, `vocab.py`):** gán nhãn `vi` / `en` / `mixed` cho từng đoạn theo tỉ lệ từ có dấu tiếng Việt (> 0,3 → vi, 0 → en, còn lại mixed). Unit 4: 73% đoạn tiếng Việt, 26% tiếng Anh, 5 đoạn trộn mã. `VI_HOMOPHONES` loại các từ tiếng Việt không dấu trùng mặt chữ tiếng Anh (*hay, con, to, ...*) khỏi danh sách từ vựng.
3. **Căn chỉnh câu hỏi ↔ lời giảng bằng quy hoạch động đơn điệu (`exercises.py`, `exercise_align.py`):** điểm = 25·khẩu lệnh "câu N" (chỉ 2 nếu 60 s sau đó không có từ nào của câu hỏi) + 2·số từ nội dung trùng + 3·đang trên màn hình; regex nhận "câu số/thứ/hỏi số N", số đọc bằng chữ, loại "text/page/part/trang N"; sau đó lùi mốc về đầu đoạn chữa. Kết quả (±10 s): dev U4 **68,8%** (v1: 65,6%), test độc lập U5 **80,0%** (v1: 57,1%); sai số TB 10,0 s / 8,1 s; 0 lần đảo thứ tự. Trên cả hai bài DP chọn giống greedy; cải thiện đến từ cách tính điểm, bước lùi mốc và cách xử lý câu không khớp. U5 cùng nguồn với U4: trên video của 6 kênh khác chỉ đúng 17,8%, chủ yếu do bước tách câu hỏi từ màn hình.
4. **Liên kết câu hỏi ↔ chủ điểm ngữ pháp bằng embedding đa ngữ (`concept_link.py`):** bi-encoder `intfloat/multilingual-e5-small`; điểm = trung bình cos(câu hỏi, chủ điểm) và cos(lời giảng của cô trong đoạn chữa câu, chủ điểm); gắn chủ điểm khi điểm ≥ **0,835**, ngược lại "none"; TF-IDF làm phương án dự phòng. Đã bỏ bộ từ khóa viết tay `KEYWORD_CUES` (chứa cả từ đáp án). Độ chính xác trên 34 câu U4: **91,2%** (luôn "none": 73,5%; TF-IDF: 82,4%; v1 MiniLM + từ khóa: 76,5%). **Hạn chế:** mô hình và ngưỡng được chọn trên chính 34 câu này, chưa có tập kiểm tra độc lập.
5. **Từ vựng: chuẩn hóa hình thái 2 lớp & phân bậc CEFR (`vocab.py`):** bảng bất quy tắc + cắt hậu tố, tra từ điển CEFR-J + Octanove (8.845 mục), khai thác nghĩa tiếng Việt từ lời giảng theo mẫu "X là / nghĩa là …", cắt clip phát âm theo ranh giới đoạn ASR. Unit 4: 80 từ (A1 26, A2 26, B1 18, B2 9, C1 1), 52 từ có nghĩa tiếng Việt, 79 clip `.wav` dài 0,7–2,2 s. **Chưa đánh giá chất lượng.**
6. **Trích xuất chủ điểm ngữ pháp lai (`neural_ie.py`):** Gemini (`gemini-3.5-flash-lite`) ở **JSON mode** (kiểm tra các trường sau khi parse), thấy khoảng 30 đoạn lời giảng lấy mẫu; khi offline dùng bộ phân loại ngữ pháp TOEIC chung, khớp theo cụm từ gợi ý trong lời giảng (không bịa nội dung). Mốc thời gian lý thuyết được neo lại vào cửa sổ lời giảng giống nhất theo `multilingual-e5-small` (`--ground-only`): sai số TB **882,5 s → 11,2 s** trên 4 chủ điểm.
7. **Phát hiện lỗi người học trong chat (`chat_parser.py`, `feedback.py`):** ẩn danh hoá tên học viên thành `S1…SN` (pseudonymization); bộ phát hiện **dựa trên luật** cho 6 nhóm lỗi chuyển di L1 (BE_VERB, PARTICIPLE, CAUSATIVE, MODAL_TO, SVA, WH_DO), mỗi lỗi kèm loại lỗi ERRANT (Bryant, Felice & Briscoe, ACL 2017) đã kiểm chứng bằng errant 3.0.2. Trên tập 70 câu viết độc lập: precision **100%**, recall **72,7%**, F1 **84,2%** (v1: recall 20,5%). Đây không phải mô hình GEC tổng quát, cung cấp câu sửa mẫu và giải thích tiếng Việt cho từng lỗi.

---

## 📂 Cấu trúc Thư mục Mã nguồn

| Tệp / Thư mục | Chức năng |
| :--- | :--- |
| `pipeline.py` | Chạy lần lượt các bước cho một bài trong `lessons/<id>/`, bỏ qua bước đã có output |
| `extract_screens.py` | Phát hiện chuyển màn hình theo độ khác biệt điểm ảnh, lưu khung hình ổn định và OCR Việt–Anh (Apple Vision) |
| `transcribe.py` | ASR `faster-whisper` `large-v3-turbo` đa ngữ, tuỳ chọn gợi ý OCR qua `hotwords`, gán nhãn ngôn ngữ từng đoạn |
| `diarize.py` | Phân tách người nói: kênh riêng từng người (Silero VAD) / pyannote 3.1 / một người nói |
| `exercises.py` | Tách câu hỏi trắc nghiệm (đề + lựa chọn A–D) từ OCR (U4: 34 bản ghi, 2 là đoạn văn) |
| `exercise_align.py` | Quy hoạch động đơn điệu căn mỗi câu hỏi với lúc cô bắt đầu chữa (có baseline greedy) |
| `neural_ie.py` | Trích chủ điểm ngữ pháp, công thức, mẹo (Gemini JSON mode + fallback theo bộ phân loại chung) và neo mốc thời gian lý thuyết |
| `concept_link.py` | Liên kết câu hỏi ↔ chủ điểm: `multilingual-e5-small` + lời giảng, ngưỡng 0,835, dự phòng TF-IDF |
| `vocab.py` | Lemmatizer 2 lớp, phân bậc CEFR-J/Octanove, nghĩa tiếng Việt từ lời giảng, clip phát âm 0,7–2,2 s |
| `chat_parser.py` | Đọc chat Zoom/Meet, ẩn danh hoá `S1…SN`, nhận số câu và đáp án ("em chọn C"), nối với câu hỏi gần nhất có số đó |
| `feedback.py` | Phát hiện & sửa 6 nhóm lỗi L1 bằng luật, gán loại lỗi ERRANT, giải thích tiếng Việt |
| `fetch_lesson.py` | Tải video bài giảng có giấy phép mở (CC) vào `lessons/<id>/` |
| `eval/` | `run_all.py` tái tạo mọi số liệu; `eval_alignment.py`, `eval_multisource.py`, `eval_concepts.py`, `eval_gec.py`, `errant_check.py`, `wer.py`, `asr_screen_terms.py`; nhãn gold nháp trong `eval/gold/` và `lessons/<id>/gold/` |
| `demo/` | Web demo một trang (`index.html`, `prepare.py`): tab Exercises / Grammar / Vocab / Chat & GEC / Screens |
| `tests/` | 10 tệp, **75 test** (`pytest`), không test nào ghi vào `lessons/` |
