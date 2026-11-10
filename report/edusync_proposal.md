# ĐỀ XUẤT ĐỀ TÀI ĐỒ ÁN MÔN HỌC (PROJECT PROPOSAL & PITCHING GUIDE)
## EDUSYNC: ĐỒNG BỘ ĐA PHƯƠNG THỨC & PHÂN TÍCH SƯ PHẠM CHO BÀI GIẢNG LUYỆN THI TIẾNG ANH (THỬ NGHIỆM TRÊN TOEIC)

**Môn học:** Xử lý Ngôn ngữ Tự nhiên Nâng cao (NLP501 — Master of Software Engineering)  
**Nhánh phát triển:** `edusync-v2`  
**Thời gian:** Tháng 11/2026  
**Nguồn số liệu:** mọi con số trong tài liệu này lấy từ [`10_evaluation_results.md`](10_evaluation_results.md) (tái tạo bằng `python eval/run_all.py`).

---

## 🎯 Tóm tắt 30 Giây (Elevator Pitch)

> 🎤 **Lời dẫn mở đầu gợi ý:**  
> *"Thưa Thầy/Cô, mỗi tối tại Việt Nam có rất nhiều học viên tham gia các lớp luyện thi tiếng Anh như **TOEIC** qua Zoom hoặc Google Meet. Khi buổi học kết thúc, thứ còn lại là một file video dài và một file chat thô. Học viên muốn tìm lại đúng câu mình làm sai phải kéo thanh tua video thủ công; làm sai một câu ngữ pháp nhưng không nhớ cô đã giảng lý thuyết đó ở phút thứ mấy; còn giáo viên thì không có số liệu nào về việc lớp đang hổng kiến thức ở đâu.  
> Nhóm em xây dựng **EduSync** — một pipeline **NLP đa phương thức** biến bản ghi buổi học thành **sổ tay học tập tương tác cho học viên** và **báo cáo sau buổi học cho giáo viên**. Nhóm thử nghiệm trên 3 bài giảng TOEIC công khai và đo kết quả trên nhãn tự gán; các con số và hạn chế được trình bày ở mục 6."*

---

## 1. Đặt Vấn Đề: 3 "Điểm Nghẽn" Trong Lớp Học Luyện Thi Tiếng Anh Trực Tuyến

Khác với video bài giảng đại học thuần lý thuyết, một buổi học luyện thi **TOEIC (Part 5, 6, 7)** có cấu trúc tương tác đặc thù (giảng công thức → chữa nhiều câu trắc nghiệm → học viên trả lời trong chat) nhưng phần lớn thông tin bị bỏ phí sau giờ học:

| Điểm nghẽn | Thực trạng trong lớp luyện thi | Ví dụ từ dữ liệu bài giảng (ECE TOEIC Starter Unit 4) | Hệ quả đối với Học viên & Giáo viên |
| :--- | :--- | :--- | :--- |
| **1. Video là "hộp đen" khó ôn lại**<br>*(Video Dropout & Scrubbing Friction)* | Video dài 60–90 phút, thường chỉ quay màn hình đề thi Word/PDF mà không có file slide tách rời. | Để tìm lại đoạn cô chữa câu *"The movie was very ___"* (Part 5), học viên phải tự tua video; trong bản ghi 58 phút, cô bắt đầu chữa câu này ở phút `15:05`. | Thời gian tập trung trung vị chỉ đạt **tối đa 6 phút**; với video dài, **69% học viên bỏ qua bài tập sau video** ([Guo et al., ACM L@S 2014](https://up.csail.mit.edu/other-pubs/las2014-pguo-engagement.pdf)) và **61% thao tác tua video** tập trung quanh các điểm chuyển cảnh ([Kim et al., ACM L@S 2014](https://dash.harvard.edu/bitstreams/7312037d-93cf-6bd4-e053-0100007fdf3b/download)). |
| **2. Ngại hỏi giáo viên & đứt gãy lý thuyết – bài tập**<br>*(Foreign Language Anxiety & Theory Disconnect)* | Đầu giờ dạy công thức, sau đó chữa nhiều câu bài tập nhanh; học viên không hiểu nhưng **ngại bật mic hỏi lại trước lớp**. | Học viên làm sai câu *"The movie was very ___ (move / moving / moved / movement)"*, không nhớ phần lý thuyết phân từ (-ing/-ed) cô giảng ngay đầu giờ, nhưng ngại hỏi lại câu cơ bản. | Lo âu ngoại ngữ (*Fear of Negative Evaluation* — [Horwitz et al., 1986](https://www.ling.ohio-state.edu/research/groups/lacqueys/readings/horowitz.pdf)) và tâm lý sợ bị đánh giá của học viên Việt Nam ([Nguyen, 2025](https://www.researchgate.net/publication/415825970_EFL_speaking_anxiety_among_Vietnamese_university_students)) khiến học viên chọn cách im lặng, học vẹt đáp án. |
| **3. Lãng phí dữ liệu chat & "điểm mù" của giáo viên**<br>*(Pedagogical Blind Spot)* | Học viên gõ đáp án và đặt câu hỏi trong khung chat Zoom, thường kèm lỗi ngữ pháp đặc trưng của người Việt. | Các câu chat kiểu *"I am agree with your answer"*, *"Why we use written here?"*, *"He has his shoes shine every day"* (log chat U4 do nhóm **mô phỏng**, vì video YouTube không có chat). Khi tắt Zoom, các lỗi này biến mất; giáo viên cũng không biết mình nói bao nhiêu phần trăm thời lượng (**TTT vs STT**). | Thiếu **phản hồi sửa lỗi kịp thời** làm giảm sự tự tin (*Self-Efficacy* — [Farmani et al., 2017](https://www.researchgate.net/publication/321063268_The_impact_of_immediate_and_delayed_error_correction_on_Iranian_EFL_learner's_self-efficacy)) của học viên; giáo viên chuẩn bị buổi sau theo cảm tính. |

### 1.2. Cơ sở Khoa học (Tại sao Học viên dễ bỏ cuộc và ngại hỏi Giáo viên?)

Nhóm dựa trên **3 nhóm nghiên cứu thực nghiệm** giải thích các rào cản khi ôn thi và cách **EduSync** hướng tới giảm từng rào cản:

1. **Bỏ cuộc giữa chừng khi xem video dài (In-Video Dropout & Cognitive Overload):**
   - Nghiên cứu quy mô lớn về video giáo dục của **[Guo, Kim, & Rubin (MIT CSAIL / edX — ACM Learning @ Scale 2014)](https://up.csail.mit.edu/other-pubs/las2014-pguo-engagement.pdf)** trên **6,9 triệu phiên xem video** cho thấy thời gian tập trung trung vị (*median engagement time*) **chỉ đạt tối đa 6 phút** bất kể video dài bao nhiêu; tỷ lệ người học tiếp tục làm bài tập sau video giảm từ **56% (video ngắn) xuống 31% (video dài)**.
   - Nghiên cứu tiếp nối của **[Kim et al. (MIT & Harvard — ACM Learning @ Scale 2014)](https://dash.harvard.edu/bitstreams/7312037d-93cf-6bd4-e053-0100007fdf3b/download)** chỉ ra rằng tỷ lệ bỏ dở cao hơn trong các phiên **xem lại để ôn bài (*re-watching sessions*)**, và **61% các đỉnh thao tác tua (*scrubbing peaks*)** tập trung quanh các điểm chuyển cảnh thị giác (25% để tìm điểm bắt đầu một khái niệm/bài tập mới, 23% để tìm lại nội dung trên màn hình vừa trôi qua).
   - 👉 **Cách EduSync tiếp cận:** phát hiện chuyển màn hình và OCR (`extract_screens.py`), tách câu hỏi trắc nghiệm (`exercises.py`), rồi dùng **quy hoạch động đơn điệu (`exercise_align.py`)** gắn cho mỗi câu mốc thời gian cô bắt đầu chữa. Học viên bấm vào câu để tua tới đó. Đo trên nhãn nháp: mốc lệch ≤10 s ở **68,8%** câu của Unit 4 (dev) và **80,0%** câu của Unit 5 (kiểm tra độc lập); các câu còn lại học viên vẫn phải tua thêm.

2. **Ngại hỏi giáo viên & sợ mất mặt (Foreign Language Anxiety & Fear of Negative Evaluation):**
   - Theo khung **FLCAS** của **[Horwitz, Horwitz, & Cope (1986, *The Modern Language Journal*)](https://www.ling.ohio-state.edu/research/groups/lacqueys/readings/horowitz.pdf)**, hai rào cản tâm lý lớn trong lớp học ngoại ngữ là **sợ giao tiếp trước đám đông (*Communication Apprehension*)** và **sợ bị đánh giá tiêu cực (*Fear of Negative Evaluation*)**.
   - Các nghiên cứu trên sinh viên học tiếng Anh (EFL) tại Việt Nam ([Ho & Truong, 2022; Nguyen, 2025](https://www.researchgate.net/publication/415825970_EFL_speaking_anxiety_among_Vietnamese_university_students); [Phenomenological Analysis of Vietnamese EFL Learners, 2024](https://www.researchgate.net/publication/381382699_A_Phenomenological_Analysis_of_the_Obstacles_Impeding_Vietnamese_EFL_Learners'_Willingness_to_Communicate_in_English)) cho thấy rào cản văn hóa **sợ mất thể diện (*fear of losing face*)** khiến nhiều học viên giữ im lặng (*classroom silence*) ngay cả khi không hiểu vì sao đáp án đúng là B.
   - 👉 **Cách EduSync tiếp cận (tự ôn lại mà không cần hỏi):**
     - Trên câu có liên kết chủ điểm (10/34 câu của Unit 4), học viên bấm **badge ngữ pháp** để tua về đoạn cô giảng lý thuyết (ví dụ: chủ điểm phân từ -ing/-ed ở `00:44`). Liên kết do `concept_link.py` tính bằng mô hình embedding đa ngữ **`multilingual-e5-small`** kết hợp lời giảng của cô trong đoạn chữa câu; độ chính xác 91,2% trên 34 câu (chọn mô hình và ngưỡng trên chính tập này, xem mục 4).
     - Tên học viên trong chat được **ẩn danh hoá thành `S1, S2...`** (pseudonymization) trước khi phân tích, để báo cáo lỗi không gắn với tên thật.

3. **Phản hồi kịp thời giúp tăng sự tự tin & quyết tâm ôn thi (Self-Efficacy & Learner Autonomy):**
   - Nghiên cứu của **[Farmani, Akbari, & Ghanizadeh (2017)](https://www.researchgate.net/publication/321063268_The_impact_of_immediate_and_delayed_error_correction_on_Iranian_EFL_learner's_self-efficacy)** (dựa trên lý thuyết *Self-Efficacy* của Bandura, 1997) và **[nghiên cứu về phản hồi sửa lỗi bằng AI cho người học EFL](https://pdfs.semanticscholar.org/2e0c/e108d8a4d775b137e7b02014720296fae4e5.pdf)** chỉ ra rằng phản hồi sửa lỗi **kịp thời, rõ ràng và không phán xét** giúp người học tự kiểm soát lỗi (*self-monitoring*), giảm lo âu và tăng **sự tự tin (*self-efficacy*)**.
   - 👉 **Cách EduSync tiếp cận:** `feedback.py` là **bộ phát hiện dựa trên luật** cho 6 nhóm lỗi chuyển di Việt–Anh (*L1 transfer*) trong tin nhắn chat, đề xuất câu sửa và giải thích bằng tiếng Việt, mỗi lỗi kèm loại lỗi theo hệ ERRANT. Từ vựng của bài được phân bậc **CEFR** để học viên biết từ nào thuộc trình độ nào.

> 💡 **Điểm nhấn trình bày với Giảng viên:**  
> Ba khó khăn trên cần đến **NLP đa phương thức** vì dữ liệu đầu vào trộn mã Việt–Anh (*code-switching*), câu hỏi bài tập và phần lý thuyết dùng từ ngữ khác nhau (*vocabulary mismatch*), và văn bản của người học có lỗi (*noisy learner text*).

---

## 2. Ý Tưởng: Mô Hình "Nút Tri Thức Đa Phương Thức" (Multimodal Knowledge Node)

EduSync không xem buổi học là một luồng video tuyến tính, mà bóc tách và liên kết **4 luồng dữ liệu** (lời giảng Việt–Anh, màn hình đề thi, chủ điểm ngữ pháp/từ vựng, chat học viên) thành các nút có liên kết hai chiều. Ví dụ dưới đây là dữ liệu thật của Unit 4 (chat là dữ liệu mô phỏng):

```text
                ┌──────────────────────────────────────────────────────────┐
                │       BẢN GHI BUỔI HỌC LUYỆN THI (ZOOM / MEET / YOUTUBE) │
                │   🎥 Video màn hình + 🎙️ Audio Việt-Anh + 💬 Log chat     │
                └────────────────────────────┬─────────────────────────────┘
                                             │
                              [Pipeline 7 kỹ thuật NLP (EduSync)]
                                             ▼
   ┌─────────────────────────┐     ┌─────────────────────┐     ┌──────────────────────────┐
   │  ⏱️ LÝ THUYẾT GỐC       │     │ 📝 CÂU HỎI BÀI TẬP  │     │ 💬 CHAT & TỪ VỰNG        │
   │  Mốc 00:44              │◄───►│ Question 4 (15:05)  │◄───►│ • Chat: "movie was moved"│
   │  Chủ điểm: Participles  │Embed│ "The movie was      │Số   │   ➔ R:VERB:FORM          │
   │  (-ing: tính chất sự vật│+ lời│  very ___"          │câu +│   (nhóm PARTICIPLE)      │
   │   -ed: cảm xúc người)   │giảng│  (A/B/C/D)          │thời │ • Clip giọng cô 0,7–2,2 s│
   └─────────────────────────┘     └─────────────────────┘gian └──────────────────────────┘
                 │                            │                              │
                 └────────────────────────────┼──────────────────────────────┘
                                              ▼
         ┌────────────────────────────────────┴────────────────────────────────────┐
         ▼                                                                         ▼
🎓 SỔ TAY TƯƠNG TÁC CHO HỌC VIÊN                                📊 BÁO CÁO SAU BUỔI HỌC CHO GIÁO VIÊN
• Bấm câu hỏi ➔ tua tới lúc cô chữa (15:05)                    • TTT/STT: "chưa đo" (bản ghi 1 người nói)
• Bấm badge ngữ pháp ➔ tua về lý thuyết (00:44)                • Phân bố lỗi theo 6 nhóm (kèm loại ERRANT)
• Lọc từ vựng theo bậc CEFR + nghe clip giọng cô               • Chủ điểm có nhiều lỗi trong chat nhất
• Xem câu sửa lỗi chat + giải thích tiếng Việt                 • Gợi ý buổi sau: câu mẫu điền từ dữ liệu
```

---

## 3. So Sánh: Trước và Sau Khi Có EduSync

| Tiêu chí | ❌ Trước (cách học cũ) | ✅ Với EduSync | Kỹ thuật NLP đứng sau |
| :--- | :--- | :--- | :--- |
| **Tìm đoạn chữa một câu bài tập** | Kéo thanh trượt video để tìm. | Bấm thẻ câu hỏi, video tua tới mốc hệ thống căn (ví dụ `15:05` cho câu *"The movie was very ___"*). Mốc lệch ≤10 s ở 68,8% (U4) / 80,0% (U5) số câu. | **Quy hoạch động đơn điệu** + regex "câu N" + lùi mốc (`exercise_align.py`) |
| **Ôn lại công thức ngữ pháp gốc** | Không biết câu này thuộc chủ điểm nào, giảng ở đâu. | Trên 10/34 câu có badge chủ điểm (ví dụ `🏷️ Participles as Adjectives`), bấm để tua về `00:44`. | **`multilingual-e5-small` + lời giảng**, cosine, ngưỡng 0,835 (`concept_link.py`); mốc lý thuyết neo lại bằng embedding (`neural_ie.py`) |
| **Học từ vựng & luyện phát âm** | Tự tra từ điển rời rạc. | 80 từ của bài phân bậc CEFR (A1–C1), 52 từ có nghĩa tiếng Việt lấy từ lời giảng (chưa kiểm tra độ đúng), 79 clip giọng cô dài 0,7–2,2 s. | **Lemmatizer 2 lớp + CEFR-J/Octanove** + trích nghĩa theo mẫu (`vocab.py`) |
| **Sửa lỗi ngữ pháp trong chat** | Câu sai trong chat trôi mất, không ai sửa. | Đánh dấu phần sai (`<del>`), gợi ý sửa (`<ins>`) và giải thích tiếng Việt cho 6 nhóm lỗi L1. | **Luật cho 6 nhóm lỗi L1** + loại lỗi ERRANT + ẩn danh hoá `S1…SN` (`chat_parser.py`, `feedback.py`) |
| **Báo cáo buổi dạy cho giáo viên** | Không có số liệu, dạy buổi sau theo cảm tính. | Phân bố lỗi trong chat, chủ điểm có nhiều lỗi nhất, gợi ý buổi sau theo câu mẫu; TTT/STT chỉ đo được khi có bản ghi tách kênh từng người. | **Phân tách người nói** (`diarize.py`) + tổng hợp báo cáo (`teacher_analytics.py`, không dùng LLM) |

---

## 4. Ba Câu Hỏi Nghiên Cứu (Research Questions) & Kết Quả Đo Được

Các kết quả dưới đây đo trên **nhãn gold bản nháp** (do AI gán, không xem output hệ thống, `verified: false`); nhóm cần kiểm tra lại nhãn trước khi bảo vệ. Chi tiết ở [`10_evaluation_results.md`](10_evaluation_results.md).

### 🔹 RQ1 (Tiếng nói & đa phương thức): Có thể xác định lúc giáo viên bắt đầu chữa từng câu hỏi trong bản ghi giảng trộn mã Việt–Anh, khi không có file slide gốc, chính xác đến mức nào?
- **Thách thức NLP:** Lời giảng Unit 4 có 73% đoạn tiếng Việt, 26% đoạn tiếng Anh và 5 đoạn trộn mã. Tiếng Anh đọc lướt dễ bị ASR nhận sai (ví dụ *"He has his shoes"* thành *"He has his sue"* trong transcript). Khi căn chỉnh, số câu bị lặp lại giữa các phần (Exercise A/B, Text 1/2...) và cô có thể nói "câu số 1, 2" của bài trong sách trong khi màn hình chiếu bài khác.
- **Giải pháp:**
  1. **ASR đa ngữ + thử nghiệm gợi ý từ màn hình:** `faster-whisper` `large-v3-turbo` ở chế độ đa ngữ. Tuỳ chọn `--screen-hints` truyền từ tiếng Anh OCR trên màn hình vào tham số `hotwords` (không phải `initial_prompt`).
  2. **Quy hoạch động đơn điệu (`exercise_align.py`):** điểm = 25·khẩu lệnh "câu N" (chỉ 2 điểm nếu 60 s sau đó không có từ nào của câu hỏi) + 2·số từ nội dung trùng + 3·đang trên màn hình; regex nhận "câu số/thứ/hỏi số N" và số đọc bằng chữ, loại "text/page/part/trang N"; ràng buộc mốc tăng dần, cho phép bỏ qua câu; sau đó lùi mốc về đầu đoạn chữa; câu không khớp lấy thời điểm màn hình nhưng kẹp giữa hai câu kề nhau.
- **Kết quả đo:**
  - Căn chỉnh (mốc lệch ≤10 s): dev U4 **68,8%** (v1: 65,6%), test độc lập U5 **80,0%** (v1: 57,1%); sai số TB 10,0 s (U4) và 8,1 s (U5); 0 lần đảo thứ tự. Lưu ý: trên U4, chỉ lấy câu "câu N" đầu tiên bằng regex đạt 71,9% ở ±10 s, cao hơn bản hiện tại, nhưng kém hơn ở ±30 s (78,1%), sai số TB (28,1 s) và bị đảo thứ tự 2 lần trên U5. Trên cả hai bài DP chọn giống greedy — phần cải thiện đến từ cách tính điểm, bước lùi mốc và cách xử lý câu không khớp. Lỗi còn lại chủ yếu ở chỗ trống trong đoạn văn (Part 6/7), nơi "lúc bắt đầu câu" vốn không rõ.
  - ASR: **chưa có WER thật** (5 clip tham chiếu chưa sửa tay). Chỉ số gián tiếp: gợi ý từ màn hình tăng tỉ lệ từ trên màn hình được nói ra từ 48% lên 52% nhưng làm tăng số đoạn lặp liên tiếp (3 → 20–27), nên chưa kết luận được; pipeline vẫn dùng bản không gợi ý.

### 🔹 RQ2 (Ngữ nghĩa): Có thể tự động nối một câu hỏi bài tập về đúng chủ điểm ngữ pháp đã giảng (hoặc "không thuộc chủ điểm nào") không?
- **Thách thức NLP:** Câu hỏi chỉ chứa từ vựng tình huống (*"The movie was very ___"*, lựa chọn *move / moving / moved / movement*), còn chủ điểm dùng thuật ngữ (*"Participles as Adjectives"*) và lời giải thích tiếng Việt. Ngoài ra 22/34 câu của Unit 4 là câu từ vựng / đọc hiểu, không thuộc chủ điểm nào, nên hệ thống phải biết từ chối gắn.
- **Giải pháp:** bi-encoder **`intfloat/multilingual-e5-small`** (384 chiều, chuẩn hóa L2); điểm = trung bình cos(câu hỏi, chủ điểm) và cos(lời giảng của cô từ lúc bắt đầu chữa câu đến câu kế tiếp, tối đa 90 s, với chủ điểm); gắn chủ điểm khi điểm ≥ 0,835, ngược lại "none"; khi không có mô hình thì dùng TF-IDF. Bộ từ khóa viết tay của v1 (có cả từ đáp án như *central, luxury, shined*) đã bị bỏ. Song song, `neural_ie.py` trích 4 chủ điểm bằng Gemini (`gemini-3.5-flash-lite`, JSON mode) và neo mốc lý thuyết vào đoạn lời giảng giống chủ điểm nhất.
- **Kết quả đo (34 câu U4):** độ chính xác **91,2%** so với 73,5% của "luôn trả lời none", 82,4% của TF-IDF và 76,5% của v1 (MiniLM + từ khóa viết tay); bỏ từ khóa viết tay thì MiniLM chỉ còn 61,8%. Với ngưỡng cố định như demo: precision 90,0%, recall 75,0%, 10 badge. Mốc lý thuyết: sai số TB **11,2 s** (Gemini một mình: 882,5 s).
- **Hạn chế:** mô hình và ngưỡng được chọn trên chính 34 câu này nên kết quả có thể lạc quan; điểm của hai nhóm "có chủ điểm" và "none" sát nhau (0,81–0,86), sang bài mới cần hiệu chỉnh lại ngưỡng; chưa có tập kiểm tra độc lập cho bài toán này.

### 🔹 RQ3 (Ngôn ngữ người học & phân tích sư phạm): Có thể phân bậc từ vựng của bài theo CEFR và phát hiện các lỗi ngữ pháp điển hình của người Việt trong chat không?
- **Thách thức NLP:** Từ vựng xuất hiện ở dạng biến cách (*moved, cities, bought*) và dễ lẫn với từ tiếng Việt không dấu (*hay, con, to*). Câu chat của học viên ngắn, trộn tiếng Việt, chứa lỗi chuyển di ngôn ngữ mẹ đẻ (*L1 transfer*).
- **Giải pháp:**
  1. **Lemmatizer 2 lớp & từ điển CEFR-J + Octanove (8.845 mục):** khử biến cách (bảng bất quy tắc + cắt hậu tố), lọc `VI_HOMOPHONES`, phân bậc CEFR, trích nghĩa tiếng Việt theo mẫu "X là / nghĩa là …", cắt clip phát âm theo ranh giới đoạn ASR (transcript không có timestamp từng từ).
  2. **Bộ phát hiện lỗi dựa trên luật (`feedback.py`):** 6 nhóm BE_VERB, PARTICIPLE, CAUSATIVE, MODAL_TO, SVA, WH_DO; mỗi lỗi có loại lỗi ERRANT (Bryant, Felice & Briscoe, ACL 2017, *"Automatic Annotation and Evaluation of Error Types for Grammatical Error Correction"*) — mặc định U:VERB:TENSE, R:VERB:FORM, R:VERB:FORM, U:VERB:FORM, R:VERB:SVA, M:VERB:TENSE, đã kiểm chứng bằng errant 3.0.2. Tên học viên được ẩn danh hoá `S1…SN` trước khi phân tích.
- **Kết quả đo:**
  - GEC trên **70 câu viết độc lập với luật**: precision **100%**, recall **72,7%**, F1 **84,2%** (v1 khớp nguyên văn: recall 20,5%); sửa đúng nguyên câu 65,9%. Tập này đã được xem một lần để sửa 3 lỗi cài đặt. Đây không phải mô hình GEC tổng quát: lỗi ngoài 6 nhóm không được bắt.
  - Từ vựng Unit 4: 80 từ (A1 26, A2 26, B1 18, B2 9, C1 1), 52 từ có nghĩa tiếng Việt, 79 clip 0,7–2,2 s — **mới có thống kê, chưa đánh giá chất lượng** (độ đúng của nghĩa chưa kiểm tra).
  - TTT/STT: **chưa đo** — các bài ECE chỉ có một người nói.

---

## 5. Phạm Vi Hiện Tại (TOEIC) & Hướng Mở Rộng (IELTS — chưa thực hiện)

Toàn bộ dữ liệu và kết quả hiện có là của bài giảng **TOEIC**. Cột IELTS chỉ mô tả hướng mở rộng; chưa có dữ liệu, chưa chạy thử và chưa có kết quả.

| Khía cạnh | Đã làm trên bài giảng TOEIC | Hướng mở rộng cho IELTS (chưa làm) |
| :--- | :--- | :--- |
| **Căn chỉnh bài tập & đề thi** | Căn từng câu trắc nghiệm **Part 5 (Incomplete Sentences)**, chỗ trống **Part 6 (Text Completion)** và câu hỏi đọc hiểu **Part 7** với lúc cô chữa. | Căn câu hỏi **IELTS Reading / Listening** (Multiple Choice, Gap-fill, Matching) với đoạn giáo viên phân tích. |
| **Liên kết lý thuyết** | Nối câu hỏi với chủ điểm ngữ pháp đã giảng trong bài (4 chủ điểm ở Unit 4) hoặc "none". | Nối câu hỏi với chiến thuật làm bài (*Skimming, Scanning, True/False/Not Given*). |
| **Từ vựng theo trình độ** | Phân bậc CEFR A1–C1 cho từ vựng của bài. Tham chiếu ngưỡng CEFR của ETS cho TOEIC Listening & Reading: A1 120, A2 225, B1 550, B2 785, C1 945. | Từ vựng học thuật bậc B2–C2; tham chiếu Cambridge: B1 ≈ IELTS 4.0–5.0, B2 ≈ 5.5–6.5, C1 ≈ 7.0–8.0, C2 ≈ 8.5+. |
| **Sửa lỗi & phân tích tương tác** | Phát hiện 6 nhóm lỗi L1 trong chat (chat U4 là dữ liệu mô phỏng); TTT/STT khi có bản ghi tách kênh. | Phân tích câu viết của học viên theo tiêu chí *Grammatical Range & Accuracy*; đo thời lượng nói trong lớp Speaking. |

---

## 6. Kết Quả Thực Nghiệm & Kiểm Chứng (theo [`10_evaluation_results.md`](10_evaluation_results.md))

Dữ liệu: ECE TOEIC Starter Unit 4 (58 phút, dev — dùng để chỉnh thuật toán), Unit 5 (58 phút, test độc lập — chạy 1 lần sau khi chốt thuật toán), Unit 1 (65 phút, chỉ dùng cho ASR/trích màn hình); Stanford CS224N để kiểm tra hồi quy pipeline v1. Nhãn gold đều là bản nháp, `verified: false`.

| Hạng mục | Dữ liệu / cách đo | Kết quả | Ghi chú khi báo cáo |
| :--- | :--- | :--- | :--- |
| **Căn chỉnh câu hỏi ↔ lời giảng** | 32/34 câu U4 (dev), 35/35 câu U5 (test) có nhãn mốc bắt đầu chữa | ±10 s: **68,8%** (U4), **80,0%** (U5); ±30 s: 84,4% / 88,6%; sai số TB 10,0 s / 8,1 s; 0 lần đảo thứ tự | v1: 65,6% / 57,1%. Demo hiển thị 33/34 câu khớp được với lời giảng (đây là độ phủ, không phải độ chính xác). |
| **Liên kết câu hỏi ↔ chủ điểm** | 34 câu U4, 4 chủ điểm (12 câu có chủ điểm, 22 câu none) | Độ chính xác **91,2%** (luôn none: 73,5%; TF-IDF: 82,4%; v1: 76,5%); ngưỡng cố định: P 90,0% / R 75,0%, 10 badge | Mô hình và ngưỡng chọn trên chính 34 câu → có thể lạc quan; chưa có tập test độc lập. |
| **Mốc thời gian phần lý thuyết** | 4 chủ điểm U4 | Sai số TB **11,2 s** (Gemini một mình: 882,5 s) | Mốc hiện tại: 00:44, 15:38, 13:18, 07:35. |
| **Phát hiện lỗi trong chat (GEC)** | 70 câu kiểu chat viết độc lập với luật (44 có lỗi trong 6 nhóm, 10 lỗi khác, 16 câu đúng) | P **100%**, R **72,7%**, F1 **84,2%** (v1: P 90,0%, R 20,5%) | Bộ dựa trên luật, chỉ 6 nhóm. Trên 17 tin nhắn mô phỏng U4: 7 lỗi trong 6 tin — không dùng để đo chất lượng. |
| **ASR** | 5 clip × 2 phút U4 | **Chưa có WER thật** | Bản chép tham chiếu chưa sửa tay; chỉ có chỉ số gián tiếp (mục 4, RQ1). |
| **Từ vựng & audio** | Unit 4 | 80 từ (A1 26, A2 26, B1 18, B2 9, C1 1); 52 nghĩa tiếng Việt; 79 clip `.wav` 0,7–2,2 s | Chỉ là thống kê, chưa đánh giá chất lượng. |
| **TTT / STT** | Unit 4 | **Chưa đo** | Bản ghi chỉ có một người nói. |
| **Kiểm tra hồi quy (pipeline v1)** | Stanford CS224N (43 slide, 54 phút) | 9/10 mốc chuyển slide có nhãn được tìm thấy, sai số TB 0,6 s | Bài toán khác (căn chỉnh slide PDF). |
| **Kiểm thử phần mềm** | 10 tệp `pytest` trong `tests/` | **71/71 test pass** | Không test nào ghi vào `lessons/`. Mã nguồn hiện có 4.454 dòng Python (code + test + eval). |

---

## 7. Phân Công Nhóm (4 Thành Viên) & Lộ Trình Trình Bày 20 Phút

| Thành viên | Vai trò trong Dự án | Các Module Phụ trách | Phần Trình bày trong Buổi Bảo vệ |
| :--- | :--- | :--- | :--- |
| **Thành viên 1** | **Project Lead & Requirement Engineer** | Phân tích bài toán sư phạm, đặc tả yêu cầu (SRS), kiến trúc pipeline, ẩn danh hoá dữ liệu chat. | **Phần 1 (Slide 01–05 \| 4.5 phút, 00:00–04:30):** Đề tài & phân công, vấn đề của lớp luyện thi, bài toán NLP & dữ liệu, kiến trúc (4 điểm kết hợp), nghiên cứu liên quan. |
| **Thành viên 2** | **Multimodal & Alignment Engineer** | Trích màn hình & OCR (`extract_screens.py`), ASR + thử nghiệm gợi ý OCR qua `hotwords` (`transcribe.py`), tách câu hỏi (`exercises.py`), quy hoạch động đơn điệu (`exercise_align.py`). | **Phần 2 (Slide 06–08 \| 4.5 phút, 04:30–09:00):** Xử lý lời giảng trộn mã Việt–Anh, thử nghiệm gợi ý từ màn hình (chưa có WER), căn chỉnh câu hỏi và kết quả dev/test. |
| **Thành viên 3** | **Core NLP & Semantic Engineer** | Từ vựng CEFR & clip phát âm (`vocab.py`), liên kết chủ điểm (`concept_link.py`), phát hiện lỗi chat (`feedback.py`), trích chủ điểm ngữ pháp (`neural_ie.py`). | **Phần 3 (Slide 09–12 \| 5.5 phút, 09:00–14:30):** `multilingual-e5-small` + lời giảng (ablation), Gemini JSON mode + neo mốc, lemmatizer & CEFR-J, bộ luật 6 lỗi L1 với loại ERRANT. |
| **Thành viên 4** | **System, Analytics & QA Engineer** | Phân tách người nói (`diarize.py`), báo cáo giáo viên (`teacher_analytics.py`), web demo (`demo/`), 71 test (`tests/`) & bộ đánh giá (`eval/`). | **Phần 4 (Slide 13–17 \| 5.5 phút, 14:30–20:00, gồm ~2 phút demo):** Báo cáo cho giáo viên, **demo trực tiếp** tại `http://localhost:8000/`, đánh giá tái lập được, hạn chế & kết luận. |

---

## 🔗 Tài Liệu Tham Chiếu Nhanh Khi Trình Bày
- **Nguồn số liệu duy nhất:** [`10_evaluation_results.md`](10_evaluation_results.md)
- **7 kỹ thuật NLP & câu hỏi phản biện:** [`09_teacher_presentation_and_technical_nlp_guide.md`](09_teacher_presentation_and_technical_nlp_guide.md)
- **Slide HTML (đồng hồ & lời thoại phím `N`):** [`slides.html`](slides.html)
- **Kịch bản demo 5 bước (90 giây):** [`06_user_guide_and_demo.md`](06_user_guide_and_demo.md)
