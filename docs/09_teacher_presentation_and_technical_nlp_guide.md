# HƯỚNG DẪN LẬP LUẬN, KIẾN THỨC TRÌNH BÀY CHO GIẢNG VIÊN & PHÂN TÍCH ĐIỂM ÁP DỤNG TECHNICAL NLP
## EDUSYNC: CĂN CHỈNH ĐA PHƯƠNG THỨC & PHÂN TÍCH BÀI GIẢNG LUYỆN THI TIẾNG ANH (THỬ NGHIỆM TRÊN TOEIC)
**Môn học:** Xử lý Ngôn ngữ Tự nhiên Nâng cao (NLP501 - Master of Software Engineering)  
**Tài liệu chuyên biệt:** Cẩm nang bảo vệ đồ án trước Giảng viên / Hội đồng chấm thi  
**Cập nhật:** 10/11/2026  
**Đi kèm:** slide [presentation/slides_marp.md](../presentation/slides_marp.md) (17 slide), lời thoại [docs/08](08_presentation_slides_and_speaker_notes.md), số liệu [docs/10_evaluation_results.md](10_evaluation_results.md) (nguồn duy nhất, tái tạo bằng `python eval/run_all.py`)

---

## PHẦN 1: CẤU TRÚC LẬP LUẬN KHI TRÌNH BÀY VỚI GIẢNG VIÊN (STORYTELLING)

Đừng liệt kê tính năng như một đồ án web. Bài trình bày đi theo mạch **"Vấn đề sư phạm → Bài toán NLP → Chỗ các luồng dữ liệu kết hợp → Phương pháp, baseline và kết quả đo được → Những gì chưa đo"**. Mỗi bước ứng với một nhóm slide:

| Bước | Slide | Thông điệp cần đọng lại |
| :--- | :-: | :--- |
| 1. Vấn đề | 1–2 | Sau buổi học chỉ còn một video khoảng 60 phút và một file chat. Học viên phải tua thủ công, ngại hỏi lại; giáo viên không biết lớp sai ở đâu. |
| 2. Bài toán NLP và dữ liệu | 3 | Bốn bài toán con: căn chỉnh đơn điệu, liên kết câu hỏi ↔ chủ điểm, từ vựng CEFR, lỗi người học. Dữ liệu tách bạch: Unit 4 để phát triển, Unit 5 để kiểm tra độc lập. Ba giới hạn được nói ngay từ đầu. |
| 3. Kiến trúc | 4–5 | Phần "đa phương thức" nằm ở bốn điểm kết hợp ①–④, không chỉ ở việc có nhiều đầu vào. Khác MaViLS: không có slide gốc, căn chỉnh tới từng câu hỏi. |
| 4. Phương pháp + kết quả | 6–12 | Kết quả nào cũng đặt cạnh baseline (v1 chạy lại từ commit `73d9a62`, và baseline đơn giản như "thời điểm màn hình", "luôn không gắn"). Cái gì chưa đo thì nói là chưa đo (WER). |
| 5. Sản phẩm | 13–14 | Báo cáo giáo viên chỉ hiển thị số tính được từ dữ liệu; demo tua theo câu hỏi và theo chủ điểm. |
| 6. Tái lập và hạn chế | 15–16 | Một lệnh tạo lại mọi số liệu; nhãn chuẩn là bản nháp; danh sách hạn chế do nhóm tự nêu. |
| 7. Kết luận | 17 | Ba đóng góp, mỗi đóng góp có một con số. |

### 1.1. Ba thông điệp chính (trùng với slide 17)
1. **Căn chỉnh câu hỏi ↔ lời giảng có xác minh khẩu lệnh theo ngữ cảnh:** 80,0% câu có mốc lệch ≤10 s trên bài kiểm tra độc lập Unit 5 (v1: 57,1%), sai số trung bình 8,1 s, 0 lần đảo thứ tự.
2. **Lời giảng làm tín hiệu liên kết chủ điểm** với `multilingual-e5-small`: độ chính xác 91,2% trên 34 câu Unit 4 (đầu ra demo v1: 58,8%), không dùng từ khóa viết tay. Có thể lạc quan vì chọn trên chính tập này.
3. **Đánh giá tái lập được:** nhãn, script, baseline chạy lại từ commit cũ; số nào chưa đo được thì ghi "chưa đo".

### 1.2. Nguyên tắc trung thực (nói chủ động, đừng đợi bị hỏi)
- Bản ghi ECE **chỉ có một người nói** (giáo viên) → TTT/STT "chưa đo".
- Log chat Unit 4 (17 tin nhắn, 5 học viên) là **dữ liệu mô phỏng** do nhóm soạn; video YouTube không có chat.
- Mọi nhãn chuẩn là **bản nháp do AI (Claude) gán**, đọc transcript, không xem output hệ thống, `verified: false`. Trước khi bảo vệ nhóm phải đối chiếu với video (docs/10 §2), đặt `verified: true` và chạy lại `eval/run_all.py`.
- **Chưa có WER**: 5 clip tham chiếu chưa sửa tay; chỉ có chỉ số gián tiếp.
- Ngưỡng và mô hình liên kết chủ điểm được chọn trên chính 34 câu Unit 4; chưa có tập kiểm tra độc lập cho bài toán này.
- Toàn bộ dữ liệu và kết quả là **TOEIC**; IELTS chỉ là hướng phát triển.

### 1.3. Cơ sở nghiên cứu cho phần động lực (slide 2)
Các nghiên cứu sau chỉ là **động lực**, nhóm chưa làm khảo sát người dùng nên không khẳng định EduSync cải thiện việc học:
- [Guo, Kim & Rubin, ACM L@S 2014](https://up.csail.mit.edu/other-pubs/las2014-pguo-engagement.pdf): thời gian xem trung vị của video bài giảng chỉ khoảng 6 phút.
- [Kim et al., ACM L@S 2014](https://dash.harvard.edu/bitstreams/7312037d-93cf-6bd4-e053-0100007fdf3b/download): các đỉnh thao tác tua tập trung quanh chỗ chuyển cảnh.
- [Horwitz, Horwitz & Cope, 1986](https://www.ling.ohio-state.edu/research/groups/lacqueys/readings/horowitz.pdf): lo âu ngoại ngữ, sợ bị đánh giá tiêu cực.
- Các nghiên cứu khác về người học EFL Việt Nam và phản hồi sửa lỗi: xem [docs/01, mục 1.2](01_project_proposal.md).

### 1.4. Vì sao dữ liệu này giàu tính NLP
1. **Trộn mã Việt – Anh:** lời giảng Unit 4 có 73% đoạn tiếng Việt, 26% đoạn tiếng Anh, 5 đoạn trộn (phân loại theo mật độ chữ có dấu). Cô giải thích bằng tiếng Việt nhưng đọc đề, ví dụ và từ vựng bằng tiếng Anh.
2. **Cấu trúc bài học bán định hình:** giảng chủ điểm ngữ pháp, rồi chữa nhiều câu TOEIC Part 5/6/7; số câu đánh lại từ 1 ở mỗi phần (Exercise A/B, Text 1/2…).
3. **Khoảng cách từ vựng (lexical gap):** câu hỏi chỉ có từ tình huống (*"The movie was very ___"*), còn chủ điểm dùng thuật ngữ (*Participles as Adjectives*) và lời giải thích tiếng Việt.
4. **Ngôn ngữ người học có lỗi:** lỗi chuyển di từ tiếng Việt (*"I am agree"*, *"should to increase"*). Vì chat là mô phỏng, chất lượng được đo trên một tập 70 câu viết riêng.

---

## PHẦN 2: BẢN ĐỒ 7 ĐIỂM ÁP DỤNG KỸ THUẬT NLP CỐT LÕI (TECHNICAL NLP DEEP-DIVE)

Bảng dưới mô tả đúng những gì mã nguồn đang làm. Cột cuối chỉ dùng số trong [docs/10](10_evaluation_results.md).

| STT | Điểm áp dụng | Phân ngành NLP | File mã nguồn | Mô hình / thuật toán | Đánh giá (docs/10) |
| :-: | :--- | :--- | :--- | :--- | :--- |
| **1** | **ASR lời giảng trộn mã, gán nhãn ngôn ngữ, thử gợi ý từ màn hình** | Speech recognition, language ID, contextual biasing | `transcribe.py` | `faster-whisper` `large-v3-turbo` đa ngữ; nhãn `vi`/`en`/`mixed` theo mật độ chữ có dấu (>0,3 / 0 / còn lại); tuỳ chọn `hotwords` = từ hoặc dòng OCR của màn hình đang chiếu | **Chưa có WER.** Proxy "từ trên màn hình được nói ra": 47% (không gợi ý), 48% (đối chứng), 52% (gợi ý); đoạn lặp 6 / 3 / 20–27 → pipeline chưa bật gợi ý |
| **2** | **Tách màn hình, OCR và bóc câu hỏi** | OCR + trích xuất thông tin bằng luật | `extract_screens.py`, `exercises.py` | Phát hiện chuyển màn hình bằng sai khác điểm ảnh; Apple Vision OCR (vi + en); regex tách đề và lựa chọn A–D | Chưa đánh giá riêng. U4: 32 màn hình, 34 bản ghi (2 là đoạn văn, không phải câu hỏi); U5: 35 câu |
| **3** | **Căn chỉnh câu hỏi ↔ lời giảng** | Căn chỉnh chuỗi theo thời gian, trích khẩu lệnh bằng regex | `exercise_align.py` | s = 25·trigger (chỉ 2 nếu không xác minh được) + 2·số từ chung + 3·đang chiếu; DP đơn điệu cho phép bỏ câu; lùi mốc về đầu đoạn chữa; câu không khớp kẹp giữa hai câu kề | Test U5: ±10 s **80,0%** (v1 57,1%), ±30 s 88,6%, sai số TB 8,1 s, 0 đảo thứ tự. Dev U4: 68,8% / 84,4% / 10,0 s |
| **4** | **Liên kết câu hỏi ↔ chủ điểm ngữ pháp** | Biểu diễn câu, truy hồi ngữ nghĩa đa ngữ | `concept_link.py` | Bi-encoder `intfloat/multilingual-e5-small` (384 chiều, chuẩn hóa L2, tiền tố `query:`/`passage:`); score = ½[cos(câu hỏi, c) + cos(lời giảng khi chữa, c)]; gắn nếu ≥ 0,835; dự phòng TF-IDF | 34 câu U4: **91,2%** (luôn none 73,5%, TF-IDF 82,4%, v1 76,5%); demo: P 90,0%, R 75,0%, 10 badge. Chọn trên chính tập này |
| **5** | **Trích chủ điểm ngữ pháp + neo mốc lý thuyết** | IE bằng LLM + grounding bằng embedding | `neural_ie.py` | Gemini `gemini-3.5-flash-lite` ở JSON mode (kiểm tra trường sau khi parse); dự phòng: bảng chủ điểm TOEIC chung + cụm từ gợi ý trong lời giảng; neo mốc bằng e5 trên cửa sổ 6 đoạn | Sai số mốc TB **11,2 s** trên 4 chủ điểm (Gemini một mình: 882,5 s) |
| **6** | **Từ vựng theo CEFR** | Hình thái học, từ điển học, trích quan hệ song ngữ | `vocab.py` | Lemmatizer 2 lớp (bảng bất quy tắc + cắt hậu tố có tra từ điển); CEFR-J + Octanove 8.845 mục; lọc `VI_HOMOPHONES`; nghĩa theo mẫu "X là / nghĩa là"; clip `.wav` theo ranh giới đoạn ASR | Chỉ thống kê: 80 từ (A1 26, A2 26, B1 18, B2 9, C1 1), 52 có nghĩa tiếng Việt, 79 clip 0,7–2,2 s. **Chưa đánh giá chất lượng** |
| **7** | **Phát hiện lỗi người học trong chat + ẩn danh hoá** | Phân tích ngôn ngữ người học, gán loại lỗi GEC | `chat_parser.py`, `feedback.py` | Ẩn danh hoá S1…SN; trích đáp án ("em chọn C"); 6 luật L1 (BE_VERB, PARTICIPLE, CAUSATIVE, MODAL_TO, SVA, WH_DO); loại lỗi ERRANT mặc định kiểm chứng bằng errant 3.0.2, nếu cài `errant` thì errant tự gán | 70 câu độc lập: P **100%**, R **72,7%**, F1 **84,2%** (v1: P 90,0%, R 20,5%); sửa đúng nguyên câu 65,9% |

Ngoài 7 điểm trên, `diarize.py` (tách kênh từng người bằng Silero VAD / pyannote 3.1 / rơi về một người nói) và `teacher_analytics.py` (tổng hợp báo cáo, không dùng LLM) là phần tổng hợp, không phải mô hình NLP.

---

### Chi tiết kỹ thuật từng điểm để giải thích cho giảng viên

#### Điểm NLP 1: ASR trộn mã Việt – Anh và gợi ý từ màn hình
- **Vấn đề:** cô giảng bằng tiếng Việt, đọc đề và từ vựng bằng tiếng Anh, thường đọc lướt; mô hình đơn ngữ không xử lý được.
- **Cách làm:**
  - `faster-whisper` `large-v3-turbo` ở chế độ đa ngữ (`--multilingual`: Whisper được đổi ngôn ngữ giữa các cửa sổ 30 s), có lọc VAD. `initial_prompt` là prompt cố định của bài trong `lesson.json`.
  - Nhãn ngôn ngữ từng đoạn: $\text{Density}_{vi}(W) = \frac{|\{w \in W : w \text{ chứa chữ cái riêng của tiếng Việt}\}|}{|W|}$; `vi` nếu > 0,3, `en` nếu = 0, còn lại `mixed`. Đây là heuristic: từ tiếng Việt không dấu (*con, hai*) không được tính là tiếng Việt.
  - Thử nghiệm ① (`--screen-hints words|lines`): cắt audio theo từng màn hình và truyền chữ tiếng Anh OCR của màn hình đó vào tham số **`hotwords`** của faster-whisper (không phải `initial_prompt`). Cấu hình `chunks` cắt y hệt nhưng không gợi ý, làm đối chứng.
- **Cơ chế (nói cho đúng):** faster-whisper đặt `hotwords` vào phần prompt (văn bản "đứng trước") của decoder. Khi sinh token $y_t$, các token gợi ý $H$ nằm trong ngữ cảnh mà **self-attention của decoder** nhìn vào; **cross-attention** nhìn vào trạng thái audio của encoder, không nhìn vào token gợi ý:
  $$P(Y \mid X, H) = \prod_{t} P\big(y_t \mid H, y_{<t}, \text{Enc}(X)\big)$$
  Không fine-tune mô hình. Đây là thiên lệch mềm, và mặt trái là decoder có thể chép lại từ gợi ý dù cô không nói (ảo giác). Cơ sở: Radford et al., ICML 2023 (Whisper); Peng et al., Interspeech 2023 (prompt cho Whisper).
- **Đánh giá:** chưa có WER. Proxy tăng khoảng 4 điểm khi có gợi ý nhưng số đoạn lặp tăng từ 3 lên 20–27, nên chưa kết luận và chưa bật.

#### Điểm NLP 2: Tách màn hình, OCR và bóc câu hỏi
- **Cách làm:** lấy mẫu khung hình; màn hình mới bắt đầu khi khung hình ổn định khác màn hình hiện tại ở đủ nhiều điểm ảnh (bỏ qua thay đổi nhỏ như con trỏ, tô sáng). OCR bằng Apple Vision (tiếng Việt + tiếng Anh). `exercises.py` dùng regex tách số câu, đề và lựa chọn A–D cho Part 5 (câu rời) và Part 6 (chỗ trống trong đoạn văn).
- **Điều phải nói rõ:** bước này chưa có đánh giá riêng. Lỗi đã biết: ở Unit 4 có 2 trong 34 bản ghi là đoạn văn bị tách nhầm thành câu hỏi; nhãn căn chỉnh vì thế chỉ có 32 câu.

#### Điểm NLP 3: Căn chỉnh câu hỏi ↔ lời giảng bằng quy hoạch động đơn điệu
- **Vấn đề:** cần mốc cô **bắt đầu chữa** từng câu trong 2.606 đoạn lời giảng của Unit 4. Tìm "câu N" đơn thuần sai vì: số câu lặp lại giữa các phần; "text 1", "part 5", "trang 3" không phải số câu; ở Unit 4 cô chữa Exercise A trong sách ("câu số 1") khi màn hình đang chiếu Exercise B.
- **Hàm điểm:**
  $$s(k, j) = 25\cdot\text{trigger}(k,j) + 2\cdot|\text{từ}(e_k) \cap \text{từ}(S_j)| + 3\cdot\text{đang\_chiếu}(k,j)$$
  - `trigger`: regex nhận "câu (số|thứ|hỏi số) N", "question/number N", số viết bằng chữ ("câu thứ tư"); lookbehind phủ định loại "text/page/part/trang N".
  - **Xác minh ngữ cảnh:** nếu 60 s sau khẩu lệnh không có từ nào của câu hỏi, trigger chỉ được 2 điểm thay vì 25.
  - Từ chung tính sau khi bỏ stopword. Ứng viên chỉ lấy trong khoảng [màn hình bắt đầu − 30 s, màn hình kết thúc + 120 s] và cần điểm ≥ 3.
- **Bộ giải mã:** $D[k][j] = s(k,j) + \max\big(0, \max\{D[k'][j'] : k' < k,\ t(j') < t(j)\}\big)$. Số 0 trong max cho phép bỏ qua các câu trước (câu không khớp). Cài đặt bằng bảng max tiền tố của các trạng thái trước sắp theo thời gian + tìm nhị phân, rồi truy vết ngược. Tính đơn điệu là ràng buộc cứng của DP.
- **Hậu xử lý:** lùi mốc qua các đoạn ngay trước có chung từ với câu hỏi (cô đọc đề trước rồi mới nói số câu); câu không khớp lấy thời điểm màn hình nhưng kẹp giữa hai câu kề → không đảo thứ tự.
- **Kết quả (Unit 5, test, ±10 s):** thời điểm màn hình 48,6% → regex "câu N" đầu tiên 71,4% → v1 57,1% → greedy và DP với điểm mới 77,1% → DP + lùi mốc **80,0%**. DP và greedy cho kết quả giống nhau trên cả hai bài (xem Q3).

#### Điểm NLP 4: Liên kết câu hỏi ↔ chủ điểm bằng bi-encoder đa ngữ + lời giảng
- **Vấn đề:** lexical gap giữa câu hỏi và chủ điểm; 22/34 câu Unit 4 không thuộc chủ điểm nào nên hệ thống phải biết từ chối gắn.
- **Cách làm:**
  - Văn bản câu hỏi = đề + lựa chọn (OCR). Văn bản chủ điểm = tiêu đề + công thức + ví dụ tiếng Anh + giải thích tiếng Việt (từ `grammar_points.json`). Văn bản lời giảng = những gì cô nói từ mốc bắt đầu chữa câu đó đến câu kế tiếp, tối đa 90 s (`SPEECH_MAX_S`).
  - Mã hoá bằng `multilingual-e5-small`, tiền tố `query:` cho câu hỏi/lời giảng và `passage:` cho chủ điểm, chuẩn hóa L2 nên cosine bằng tích vô hướng:
    $$\text{score}(q,c) = \tfrac{1}{2}\big[\cos(E(q), E(c)) + \cos(E(\text{lời giảng}_q), E(c))\big]$$
  - Gắn $\hat c = \arg\max_c \text{score}(q,c)$ nếu score ≥ 0,835 (giữa vùng ổn định 0,830–0,840 trên Unit 4, ghi trong code), ngược lại "none". Không có `sentence-transformers` thì dùng TF-IDF trên câu hỏi + lời giảng.
  - Bỏ bộ từ khóa viết tay `KEYWORD_CUES` của v1 (có cả từ đáp án *central, luxury, shined* → rò rỉ nhãn).
- **Ablation (34 câu, ngưỡng leave-one-out):** MiniLM + từ khóa (v1) 76,5% → bỏ từ khóa 61,8% → paraphrase-multilingual-MiniLM 76,5% → e5 85,3% → **e5 + lời giảng 91,2%**. Phần lời giảng chủ yếu tăng recall (link recall 75,0% → 83,3%).
- **Điều phải nói rõ:** chọn mô hình và ngưỡng trên chính 34 câu; điểm hai nhóm "có chủ điểm" và "none" sát nhau (0,81–0,86).

#### Điểm NLP 5: Trích chủ điểm bằng LLM và neo mốc lý thuyết bằng embedding
- **Cách làm:** Gemini (`gemini-3.5-flash-lite`) ở **JSON mode** (`responseMimeType=application/json`); các trường bắt buộc được kiểm tra sau khi parse, không phải JSON schema chặt. Gemini chỉ thấy khoảng 30 đoạn lời giảng lấy mẫu, nên mốc thời gian nó trả về là đoán.
- **Neo mốc (`--ground-only`):** chia transcript thành cửa sổ 6 đoạn liên tiếp, mã hoá bằng e5, lấy cửa sổ giống chủ điểm nhất làm mốc "Lý thuyết".
- **Dự phòng khi không có API key / mạng:** bảng chủ điểm ngữ pháp TOEIC chung, chỉ giữ chủ điểm có cụm từ gợi ý xuất hiện trong lời giảng (không bịa nội dung).
- **Kết quả:** sai số TB 882,5 s → 11,2 s; ví dụ Passive / require that: nhãn 13:16, Gemini 55:02, sau khi neo 13:18.

#### Điểm NLP 6: Từ vựng theo CEFR
- **Lemmatizer 2 lớp:** bảng động từ bất quy tắc (*wrote → write, bought → buy*), rồi cắt hậu tố (`-ies`, `-es`, `-s`, `-ied`, `-ed`, `-ing`); chỉ chấp nhận kết quả nếu dạng gốc có trong từ điển, để tránh cắt sai.
- **Phân bậc:** tra CEFR-J + Octanove (8.845 mục).
- **Lọc trùng mặt chữ Việt – Anh:** danh sách `VI_HOMOPHONES` (*hay, con, cho, to, ra…*) cộng danh sách stopword tiếng Anh (*an, can…*). Lưu ý: *may* hiện chưa được lọc.
- **Nghĩa tiếng Việt:** mẫu "X là / nghĩa là / có nghĩa là …" trong lời giảng, hoặc một đoạn tiếng Anh ngắn ngay sau là đoạn tiếng Việt.
- **Audio:** clip `.wav` 0,7–2,2 s cắt theo ranh giới đoạn ASR có chứa từ (ưu tiên đoạn chỉ có một từ), vì transcript không có timestamp từng từ.
- **Điều phải nói rõ:** 80 từ, 52 nghĩa, 79 clip chỉ là thống kê; độ đúng của nghĩa và audio chưa được kiểm tra.

#### Điểm NLP 7: Phát hiện lỗi người học trong chat, loại lỗi ERRANT và ẩn danh hoá
- **`chat_parser.py`:** đọc chat kiểu Zoom/Meet, **ẩn danh hoá** tên thành S1…SN (pseudonymization), trích số câu và đáp án ("em chọn C"), nối tin nhắn với câu hỏi gần nhất có số đó theo mốc đã căn chỉnh (số câu đánh lại ở mỗi phần).
- **`feedback.py`:** bộ phát hiện **dựa trên luật** cho 6 mẫu lỗi chuyển di, sinh câu sửa (`<del>`/`<ins>`) và giải thích tiếng Việt. Mỗi lỗi có nhãn nhóm của nhóm và loại lỗi ERRANT:

  | Nhóm | Ví dụ → sửa | Loại ERRANT (errant 3.0.2) |
  | :--- | :--- | :--- |
  | BE_VERB | I am agree → I agree | U:VERB:TENSE |
  | PARTICIPLE | The movie was moved → moving | R:VERB:FORM |
  | CAUSATIVE | I have my car repair → repaired | R:VERB:FORM |
  | MODAL_TO | should to increase → should increase | U:VERB:FORM |
  | SVA | it make me cry → it makes me cry | R:VERB:SVA |
  | WH_DO | Why we use -ing? → Why do we use -ing? | M:VERB:TENSE |

  ERRANT: Bryant, Felice & Briscoe, ACL 2017. Nếu cài `errant`, `feedback.py` để errant tự gán loại cho từng cặp (câu gốc, câu sửa); nếu không thì dùng loại mặc định ở bảng trên.
- **Đánh giá:** 70 câu kiểu chat viết độc lập với luật (44 có lỗi trong 6 nhóm, 10 lỗi khác, 16 câu đúng): P 100%, R 72,7%, F1 84,2% ở cấp câu; recall theo nhóm từ 42,9% (WH_DO) đến 100% (MODAL_TO). Không báo nhầm câu nào trong 10 câu có lỗi ngoài phạm vi.

---

## PHẦN 3: BỘ 12 CÂU HỎI PHẢN BIỆN CỦA GIẢNG VIÊN & CÁCH TRẢ LỜI

Trả lời ngắn, có số, nói thẳng giới hạn. Người trả lời chính ghi trong ngoặc (phân công ở [docs/08, mục 3](08_presentation_slides_and_speaker_notes.md)).

#### Q1. "Số 80% đo thế nào, ai gán nhãn?" (TV2)
- 80,0% là tỉ lệ câu của **Unit 5** (35 câu, bài kiểm tra độc lập) mà mốc hệ thống dự đoán lệch **không quá 10 s** so với nhãn "lúc cô bắt đầu chữa câu đó". Cùng bảng: ±30 s 88,6%, sai số tuyệt đối trung bình 8,1 s, 0 lần đảo thứ tự.
- Thuật toán được chỉnh trên Unit 4 và chỉ chạy **một lần** trên Unit 5 sau khi chốt.
- Nhãn do **AI (Claude) gán bản nháp**: đọc transcript theo cùng một hướng dẫn, **không xem output hệ thống**, đang ở trạng thái `verified: false`. Nhóm đang mở video ở các mốc trong `alignment_gold.json` để sửa, rồi chạy lại `eval/run_all.py`; nếu số thay đổi, nhóm sẽ cập nhật.
- Hai giới hạn nên tự nói: nhãn dựa trên mốc của transcript nên sai lệch thời gian của chính ASR không bị tính; và với chỗ trống trong đoạn văn (Part 6/7) "lúc bắt đầu câu" vốn không rõ (nhãn ghi mốc thay thế lệch 5–40 s).

#### Q2. "Trên Unit 4, regex lấy 'câu N' đầu tiên đạt 71,9% ở ±10 s, cao hơn bản hiện tại (68,8%). Sao không dùng regex?" (TV2)
- Đúng, nhóm báo cáo nguyên văn. Nhưng regex kém hơn ở mọi chỉ số còn lại: ±30 s 78,1% so với 84,4%, sai số TB 28,1 s so với 10,0 s trên Unit 4.
- Trên Unit 5 (test), regex đạt 71,4% so với 80,0%, sai số TB 21,3 s so với 8,1 s, và **đảo thứ tự 2 lần**, nghĩa là học viên bấm câu sau lại bị tua về trước câu trước.
- Regex "câu N đầu tiên" chính là lỗi ở tình huống Exercise A/B (slide 7): khẩu lệnh đúng số nhưng sai câu.

#### Q3. "DP khác greedy ở đâu nếu kết quả giống nhau?" (TV2)
- **Greedy:** đi từ trái sang phải, mỗi câu lấy đoạn có điểm cao nhất sau mốc của câu trước. Nếu một câu "chiếm" một đoạn muộn có điểm cao, các câu sau bị đẩy ra sau đó và có thể mất mốc đúng.
- **DP:** tối đa **tổng điểm toàn bài** dưới ràng buộc mốc tăng dần, và được phép bỏ qua câu. Ví dụ trong `tests/test_exercises.py`: câu 1 có khẩu lệnh mạnh ở t = 50 s nhưng thật ra được bàn ở t = 10 s, câu 2 được chữa ở t = 30 s; greedy lấy câu 1 ở 50 s và mất câu 2, còn DP chọn câu 1 ở 10 s và câu 2 ở 30 s.
- **Trên Unit 4 và Unit 5, DP chọn giống hệt greedy** (docs/10 §3), nên phần cải thiện đến từ hàm điểm (xác minh khẩu lệnh, bỏ stopword), bước lùi mốc và cách xử lý câu không khớp. Nhiều khả năng là vì sau khi khẩu lệnh không xác minh bị hạ còn 2 điểm và ứng viên bị giới hạn quanh thời điểm màn hình, không còn xung đột nào để greedy mắc bẫy.
- Nhóm vẫn giữ DP vì nó cho lời giải tối ưu đúng với định nghĩa bài toán, chi phí thêm không đáng kể, và an toàn hơn ở bài có xung đột. Nhóm không nhận DP là nguồn cải thiện.

#### Q4. "Vì sao chưa có WER? Gợi ý từ màn hình có tác dụng không?" (TV2)
- WER cần bản chép tham chiếu do người sửa. 5 clip × 2 phút trong `gold/asr/` hiện chỉ là bản nháp từ ASR (`corrected: false`); tính WER lúc này là so ASR với ASR, vô nghĩa. Script `eval/wer.py` đã có và có test; chỉ thiếu bản chép đã sửa.
- Con số WER thuật ngữ trong tài liệu cũ **không có phép đo nào đứng sau** và đã bị rút (docs/10 §9).
- Về gợi ý: proxy tăng từ 48% (đối chứng) lên 52%, nhưng đoạn lặp tăng từ 3 lên 20–27; proxy lại có thể tăng chỉ vì Whisper chép từ gợi ý. Nên câu trả lời đúng là **"chưa biết"**, và pipeline dùng bản không gợi ý.
- Khi có bản chép: chạy WER cho 3 cấu hình (không gợi ý, gợi ý = từ, gợi ý = dòng). Nên báo thêm WER riêng cho đoạn `vi` và `en`; lưu ý chữ Việt viết cách theo âm tiết, nên WER tách theo khoảng trắng của phần tiếng Việt thực chất là lỗi theo âm tiết.

#### Q5. "Lỗi lan truyền từ ASR/OCR sang các bước sau xử lý thế nào?" (TV2, TV1 bổ sung)
- Nói thẳng: nhóm **chưa đo lỗi lan truyền đầu – cuối** (chưa có WER, chưa đánh giá OCR riêng). Những gì có là các cơ chế giảm thiểu:
  1. **Căn chỉnh không dựa vào một tín hiệu:** khẩu lệnh (ASR), từ chung với câu hỏi (ASR × OCR), thời điểm màn hình (video). ASR nghe sai "câu 3" thì hai tín hiệu kia vẫn còn; khẩu lệnh không được xác minh thì chỉ còn 2 điểm.
  2. **Giới hạn thiệt hại:** ứng viên chỉ nằm quanh thời điểm màn hình; câu không khớp rơi về thời điểm màn hình nhưng kẹp giữa hai câu kề, nên 0 lần đảo thứ tự trên Unit 5.
  3. **Liên kết chủ điểm lấy trung bình** của câu hỏi (OCR) và lời giảng (ASR), nên một kênh nhiễu không tự quyết định.
  4. **Từ vựng:** chỉ nhận lemma có trong từ điển; lọc `VI_HOMOPHONES` và stopword.
  5. **Không để kênh nhiễu chảy sang kênh khác khi chưa chứng minh:** gợi ý OCR → ASR chưa bật vì làm tăng đoạn lặp.
- Lỗi lan truyền đã thấy: 2 đoạn văn bị OCR/parse tách thành "câu hỏi" ở Unit 4.

#### Q6. "Sao không dùng TF-IDF hay BM25 cho nhẹ?" (TV3)
- Nhóm **có** chạy: TF-IDF 82,4%, BM25 70,6%, so với 91,2% của e5 + lời giảng (34 câu, ngưỡng leave-one-out). TF-IDF không phải "bằng 0": nó khá ở câu có từ trùng và ở việc trả lời "none".
- Khác biệt nằm ở **recall**: TF-IDF gắn đúng 58,3% câu có chủ điểm, e5 + lời giảng 83,3%. Lý do là lexical gap ("moving/moved" và "Participles as Adjectives") và giải thích chủ điểm bằng tiếng Việt, nên cần mô hình đa ngữ.
- Trên 34 câu, chênh lệch giữa các phương pháp chỉ là vài câu; nhóm không khẳng định có ý nghĩa thống kê. TF-IDF vẫn được giữ làm phương án dự phòng khi không có mô hình.

#### Q7. "Ngưỡng 0,835 có bị overfit không?" (TV3)
- **Có nguy cơ, và nhóm ghi rõ trên slide.** Có hai mức chọn:
  1. **Ngưỡng:** trong bảng so sánh, mỗi câu được chấm bằng ngưỡng tối ưu trên 33 câu còn lại (leave-one-out), nên không câu nào được chấm bằng ngưỡng chỉnh trên chính nó. Ngưỡng cố định 0,835 trong demo là giữa vùng ổn định 0,830–0,840 trên Unit 4, tức là chọn trong mẫu.
  2. **Mô hình và đặc trưng** (e5 + lời giảng) được chọn trong nhiều biến thể trên cùng 34 câu → con số có thể lạc quan.
- Điểm của nhóm "có chủ điểm" và "none" sát nhau (0,81–0,86): cosine của E5 dồn trong một dải hẹp ở mức cao, nên giá trị tuyệt đối của ngưỡng phụ thuộc bài học. Sang bài mới phải hiệu chỉnh lại.
- Cách sửa: gán nhãn chủ điểm cho 35 câu Unit 5 làm tập kiểm tra độc lập với mô hình và ngưỡng giữ nguyên; thử ngưỡng tương đối (khoảng cách với chủ điểm đứng thứ hai) thay vì ngưỡng tuyệt đối.

#### Q8. "ERRANT dùng ở đâu, nhãn có đúng chuẩn không?" (TV3)
- ERRANT (Bryant, Felice & Briscoe, ACL 2017, *Automatic Annotation and Evaluation of Error Types for Grammatical Error Correction*) tự động gán loại lỗi cho một cặp câu gốc / câu sửa theo dạng `Thao tác:Loại`: M (thiếu), U (thừa), R (thay thế). Đây cũng là công cụ dùng trong BEA-2019 shared task (Bryant, Felice, Andersen & Briscoe, 2019).
- Trong EduSync, ERRANT **chỉ dùng để gán loại** cho mỗi lỗi mà `feedback.py` phát hiện. Việc phát hiện và sửa là do luật; việc đánh giá là precision/recall cấp câu trên 70 câu, không phải điểm ERRANT.
- Các loại mặc định đã được **kiểm chứng bằng thư viện errant 3.0.2** (`eval/errant_check.py`, kết quả ở `eval/results/errant_check.txt`). Ví dụ: *"should to increase" → U:VERB:FORM*, vì ERRANT xếp "to" của động từ nguyên mẫu vào VERB:FORM chứ không vào giới từ; *"I am agree" → U:VERB:TENSE* và *"Why we use" → M:VERB:TENSE*, vì ERRANT xếp thêm/bớt trợ động từ vào VERB:TENSE.
- Các nhãn trong tài liệu cũ không có trong bảng loại của ERRANT và đã bị bỏ (docs/10 §9).
- errant có thể cho loại lân cận với cặp câu khác: R:MORPH cho *confusing → confused*, R:OTHER cho *don't → doesn't*. Nếu máy có cài `errant`, `feedback.py` dùng loại do errant gán cho từng lỗi.

#### Q9. "Chat là thật hay giả? Dữ liệu học viên được bảo vệ thế nào?" (TV1)
- **Giả lập.** Bài giảng ECE trên YouTube không có chat; 17 tin nhắn của 5 học viên ở Unit 4 do nhóm soạn để minh họa luồng chat → lỗi → câu hỏi → báo cáo. Kết quả 7 lỗi trong 6 tin nhắn trên chat này **không dùng để đo chất lượng**, vì chat được soạn kèm lỗi mẫu.
- Chất lượng phát hiện lỗi được đo trên tập 70 câu riêng, viết độc lập với luật (cũng là bản nháp do AI viết, `verified: false`).
- Tên học viên được **ẩn danh hoá** thành S1…SN trước khi phân tích. Đây là pseudonymization, không phải "tuân thủ FERPA" (FERPA là luật Mỹ về hồ sơ học vụ; nhóm không đánh giá tuân thủ pháp lý).
- Bước tiếp theo: thu chat của lớp thật, có sự đồng ý của học viên.

#### Q10. "Tại sao không dùng LLM cho tất cả, ví dụ đưa cả video vào Gemini?" (TV1)
- **Dẫn chứng ngay trong đồ án:** Gemini chỉ thấy khoảng 30 đoạn lấy mẫu và trả về mốc lý thuyết lệch trung bình 882,5 s; neo lại bằng embedding còn 11,2 s. Mốc thời gian chính xác là chỗ LLM yếu, mà sản phẩm cần đúng từng mốc.
- **Đo được từng bước:** pipeline tách bước cho phép mỗi bước có nhãn và chỉ số riêng (căn chỉnh, liên kết, mốc lý thuyết, GEC), và so với baseline.
- **Tái lập và chạy cục bộ:** `eval/run_all.py` cho cùng kết quả mỗi lần chạy, không cần API; chat học viên không phải gửi ra ngoài.
- Nhóm **có dùng LLM** ở chỗ hợp lý: tóm tắt chủ điểm (tiêu đề, công thức, giải thích). Hướng tiếp theo cũng dùng mô hình sinh (seq2seq / LLM) để sửa câu rồi errant để gán loại. Nhóm chưa so sánh trực tiếp với một hệ thống thuần LLM, nên không khẳng định về chi phí hay tốc độ.

#### Q11. "Báo cáo giáo viên tính thế nào? Sao không có TTT/STT?" (TV4)
- **TTT/STT** chỉ tính khi tách được người nói: ghi âm tách kênh từng người (Zoom; dùng Silero VAD trên từng kênh) hoặc pyannote 3.1. Bản ghi ECE chỉ có giáo viên nói, nên báo cáo ghi **"chưa đo"** thay vì 100%/0% như bản cũ.
- **Phân bố lỗi:** đếm lỗi trong chat theo 6 nhóm.
- **Chủ điểm yếu nhất:** lỗi trong chat → câu hỏi mà tin nhắn trả lời (`exercise_id`) → chủ điểm của câu đó; chọn chủ điểm có nhiều tin nhắn có lỗi nhất, không có bằng chứng thì để trống. Unit 4: Participles (2 tin nhắn, câu 4 và 6), nhưng chat là mô phỏng nên chỉ minh họa.
- **Gợi ý buổi sau:** câu mẫu điền từ dữ liệu, không dùng LLM, mỗi dòng nêu căn cứ.
- Demo cũ có giá trị viết cứng "tỷ lệ căn chỉnh 95,6%"; nay hiển thị số câu khớp được với lời giảng (33/34). Đây là độ phủ, không phải độ chính xác.

#### Q12. "Mở rộng sang IELTS thế nào?" (TV4, TV1 bổ sung)
- Hiện **chưa có dữ liệu IELTS, chưa chạy thử, chưa có kết quả**; mọi số liệu là TOEIC.
- Cần thay đổi:
  1. **Bóc câu hỏi:** `exercises.py` đang giả định lựa chọn A–D; IELTS Reading/Listening có gap-fill, matching, True/False/Not Given → cần parser mới và nhãn mới.
  2. **Liên kết:** "chủ điểm" chủ yếu là chiến thuật làm bài (skimming, scanning, T/F/NG) thay vì ngữ pháp; phải gán nhãn và hiệu chỉnh lại ngưỡng.
  3. **Từ vựng:** trọng tâm B2–C2; tham chiếu Cambridge: B1 ≈ IELTS 4.0–5.0, B2 ≈ 5.5–6.5, C1 ≈ 7.0–8.0, C2 ≈ 8.5+.
  4. **Lỗi người học:** bài viết Writing có nhiều loại lỗi hơn 6 mẫu → cần mô hình GEC tổng quát + errant; luật hiện tại chỉ là một phần.
  5. **Speaking:** cần bản ghi nhiều người nói và tách người nói để đo thời lượng nói của học viên.

---

## PHẦN 4: NHỮNG CÂU KHÔNG ĐƯỢC NÓI (ĐÃ RÚT KHỎI TÀI LIỆU CŨ)

Các con số và nhãn cũ đã rút được liệt kê kèm lý do ở docs/10 §9; không nhắc lại chúng khi trình bày. Nếu hội đồng hỏi về số cũ, nói rõ là đã rút và vì sao. Khi nói về các chủ đề sau, chỉ dùng cách nói ở cột phải:

| Chủ đề | Nói như sau |
| :--- | :--- |
| ASR | Chưa có WER; gợi ý từ màn hình làm tăng đoạn lặp, chưa bật |
| Căn chỉnh | ±10 s: 68,8% (U4, dev), 80,0% (U5, test); sai số TB 10,0 s / 8,1 s. "33/34 câu khớp" là độ phủ, không phải độ chính xác |
| Liên kết chủ điểm | `multilingual-e5-small` + lời giảng (MiniLM chỉ còn là baseline v1); 91,2% trên 34 câu, có thể lạc quan; chưa đo tốc độ |
| Lỗi trong chat | P 100%, R 72,7% trên 70 câu độc lập; loại lỗi kiểm chứng bằng errant 3.0.2; ERRANT là ACL 2017 |
| Báo cáo giáo viên | TTT/STT "chưa đo" (một người nói); gợi ý là câu mẫu điền từ dữ liệu, không dùng LLM |
| Dữ liệu học viên | Ẩn danh hoá tên thành S1…SN; không nói "chuẩn" pháp lý nào |
| Gemini | JSON mode, kiểm tra trường sau khi parse; không phải JSON schema chặt |
| Quy mô | Video 58 phút; 80 từ / 52 nghĩa / 79 clip `.wav`; 4.454 dòng Python; 71/71 test |
| Whisper | Nếu nhắc dữ liệu huấn luyện: `large-v3` khoảng 1 triệu giờ nhãn yếu + 4 triệu giờ nhãn giả (680.000 giờ là của Whisper v1/v2), như docs/02 §3.1; token gợi ý nằm trong ngữ cảnh self-attention của decoder, cross-attention nhìn vào audio |
| IELTS | Chỉ là hướng phát triển; không có kết quả nào trên IELTS |
