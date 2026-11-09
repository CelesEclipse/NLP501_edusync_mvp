# ĐỀ XUẤT ĐỀ TÀI ĐỒ ÁN MÔN HỌC (PROJECT PROPOSAL & PITCHING GUIDE)
## EDUSYNC: NỀN TẢNG ĐỒNG BỘ ĐA PHƯƠNG THỨC & PHÂN TÍCH SƯ PHẠM TỰ ĐỘNG CHO BÀI GIẢNG LUYỆN THI TIẾNG ANH (TOEIC & IELTS)

**Môn học:** Xử lý Ngôn ngữ Tự nhiên Nâng cao (NLP501 — Master of Software Engineering)  
**Nhánh phát triển:** `edusync-v2`  
**Thời gian:** Tháng 11/2026  

---

## 🎯 Tóm tắt 30 Giây (Elevator Pitch — Mở đầu ấn tượng trước Giảng viên)

> 🎤 **Lời dẫn mở đầu gợi ý:**  
> *"Thưa Thầy/Cô, mỗi tối tại Việt Nam có hàng chục ngàn học viên tham gia các lớp luyện thi **TOEIC và IELTS** qua Zoom hoặc Google Meet. Khi buổi học 90 phút kết thúc, thứ duy nhất còn lại là một file video MP4 nặng hàng trăm MB và một file chat text thô. Học viên muốn tìm lại đúng câu trắc nghiệm mình làm sai phải kéo chuột mò mẫm suốt 20 phút; làm sai một câu ngữ pháp nhưng không nhớ cô đã giảng lý thuyết đó ở phút thứ mấy; còn giáo viên thì không có bất kỳ số liệu nào về việc cả lớp đang hổng kiến thức ở đâu.  
> Đó là lý do nhóm chúng em xây dựng **EduSync** — một hệ thống **NLP Đa phương thức (Multimodal NLP)** tự động biến bản ghi buổi học TOEIC/IELTS thành **Sổ tay Học tập Tương tác Từng giây cho Học viên** và **Trợ lý Phân tích Sư phạm cho Giáo viên**."*

---

## 1. Đặt Vấn Đề: 3 "Điểm Nghẽn" Trong Lớp Học TOEIC / IELTS Trực Tuyến

Khác với các video bài giảng đại học thuần lý thuyết, một buổi học luyện thi **TOEIC (Part 5, 6, 7)** hoặc **IELTS (Reading, Listening, Writing, Speaking)** có cấu trúc tương tác rất đặc thù nhưng đang bị lãng phí sau mỗi giờ học:

| Điểm nghẽn | Thực trạng trong lớp học TOEIC / IELTS | Ví dụ thực tế từ dữ liệu bài giảng | Hệ quả đối với Học viên & Giáo viên |
| :--- | :--- | :--- | :--- |
| **1. Video là "Hộp đen" phi cấu trúc gây bỏ cuộc khi ôn bài**<br>*(Video Dropout & Scrubbing Friction)* | Video kéo dài 60–90 phút, thường chỉ quay màn hình đề thi Word/PDF mà không có file slide tách rời. | Để tìm lại đoạn cô chữa **Câu 14 (TOEIC Part 5)** hoặc **Passage 2 (IELTS Reading)**, học viên phải kéo thanh tua video thủ công từ phút 15 đến phút 50. | Thời gian tập trung trung vị chỉ đạt **tối đa 6 phút**; với video dài, **69% học viên bỏ qua bài tập sau video** ([Guo et al., ACM L@S 2014](https://up.csail.mit.edu/other-pubs/las2014-pguo-engagement.pdf)) và **61% thao tác tua video** chỉ để tìm điểm chuyển bài/slide ([Kim et al., ACM L@S 2014](https://dash.harvard.edu/bitstreams/7312037d-93cf-6bd4-e053-0100007fdf3b/download)). |
| **2. Tâm lý ngại hỏi giáo viên & Đứt gãy Lý thuyết – Bài tập**<br>*(Foreign Language Anxiety & Theory Disconnect)* | Đầu giờ dạy công thức, cuối giờ chữa 30–40 câu bài tập nhanh; học viên làm sai hoặc không hiểu nhưng **ngại bật mic hỏi lại cô giáo trước lớp đông người**. | Học viên làm sai câu: *"The movie was [moved / moving]..."* ở phút `15:06`, không nhớ lý thuyết ở đâu nhưng sợ "mất mặt" (*fear of losing face*) nếu hỏi lại câu cơ bản. | Lo âu ngoại ngữ (*Fear of Negative Evaluation* — [Horwitz et al., 1986](https://www.ling.ohio-state.edu/research/groups/lacqueys/readings/horowitz.pdf)) và tâm lý sợ bị đánh giá của học viên Việt Nam ([Nguyen, 2025](https://www.researchgate.net/publication/415825970_EFL_speaking_anxiety_among_Vietnamese_university_students)) khiến học viên chọn cách im lặng, học vẹt đáp án và giảm quyết tâm ôn thi. |
| **3. Lãng phí dữ liệu Chat & "Điểm mù" của Giáo viên**<br>*(Pedagogical Blind Spot)* | Học viên liên tục gõ đáp án và đặt câu hỏi trong khung chat Zoom, chứa nhiều lỗi ngữ pháp đặc trưng của người Việt. | Học viên chat: *"I am agree with A"*, *"Why we use -ing?"*, *"have his shoes shine"*. Khi tắt Zoom, toàn bộ lỗi sai này biến mất, giáo viên cũng không biết mình đã độc thoại bao nhiêu % thời lượng (**TTT vs STT**). | Thiếu **phản hồi sửa lỗi tức thì (Immediate Corrective Feedback)** làm giảm sự tự tin (*Self-Efficacy* — [Farmani et al., 2017](https://www.researchgate.net/publication/321063268_The_impact_of_immediate_and_delayed_error_correction_on_Iranian_EFL_learner's_self-efficacy)) của học viên; giáo viên dạy buổi sau theo cảm tính. |

### 1.2. Cơ sở Khoa học & Bằng chứng Nghiên cứu Quốc tế (Tại sao Học viên dễ bỏ cuộc và ngại hỏi Giáo viên?)

Để chứng minh tính cấp thiết của đề tài trước Hội đồng, nhóm dựa trên **3 nhóm nghiên cứu thực nghiệm quốc tế** giải thích nguyên nhân cản trở việc ôn thi TOEIC / IELTS và cách **EduSync** tháo gỡ từng rào cản:

1. **Bằng chứng về "Hiệu ứng Bỏ cuộc giữa chừng khi xem Video dài" (In-Video Dropout & Cognitive Overload):**
   - Nghiên cứu quy mô lớn nhất thế giới về video giáo dục của **[Guo, Kim, & Rubin (MIT CSAIL / edX — ACM Learning @ Scale 2014)](https://up.csail.mit.edu/other-pubs/las2014-pguo-engagement.pdf)** trên **6,9 triệu phiên xem video** chứng minh: thời gian tập trung trung vị (*median engagement time*) của người học **chỉ đạt tối đa 6 phút** bất kể video dài bao nhiêu; tỷ lệ người học tiếp tục làm bài tập thực hành sau video giảm mạnh từ **56% (video ngắn) xuống 31% (video dài)** — tức **69% học viên bỏ cuộc không làm tiếp bài tập** sau khi xem một video quá dài.
   - Nghiên cứu tiếp nối của **[Kim et al. (MIT & Harvard — ACM Learning @ Scale 2014)](https://dash.harvard.edu/bitstreams/7312037d-93cf-6bd4-e053-0100007fdf3b/download)** chỉ ra rằng tỷ lệ bỏ dở tăng vọt trong các phiên **xem lại để ôn bài (*re-watching sessions*)**, và **61% các đỉnh thao tác tua thanh trượt (*scrubbing peaks*)** tập trung quanh các điểm chuyển cảnh thị giác (25% để tìm điểm bắt đầu một khái niệm/bài tập mới, 23% để tìm lại nội dung trên màn hình vừa trôi qua).
   - 👉 **Cách EduSync giải quyết:** Tự động dùng **OCR phát hiện chuyển cảnh (`extract_screens.py`)** kết hợp **Quy hoạch động đơn điệu (`exercise_align.py`)** để băm nhỏ video bài giảng TOEIC/IELTS 60–90 phút thành **34 phân đoạn câu hỏi ngắn (< 2 phút/câu)**. Học viên bấm 1 chạm là vào thẳng câu cần ôn, xóa bỏ hoàn toàn sự nản chí khi phải tua tìm thủ công.

2. **Bằng chứng về "Tâm lý Ngại hỏi Giáo viên & Sợ mất mặt" (Foreign Language Anxiety & Fear of Negative Evaluation):**
   - Theo khung lý thuyết kinh điển **FLCAS** của **[Horwitz, Horwitz, & Cope (1986, *The Modern Language Journal*)](https://www.ling.ohio-state.edu/research/groups/lacqueys/readings/horowitz.pdf)**, hai rào cản tâm lý lớn nhất trong lớp học ngoại ngữ là **Sợ giao tiếp trước đám đông (*Communication Apprehension*)** và **Sợ bị đánh giá tiêu cực (*Fear of Negative Evaluation*)** — học viên luôn lo sợ câu hỏi của mình bị coi là "ngớ ngẩn" hoặc phát âm sai trước mặt bạn bè.
   - Các nghiên cứu thực nghiệm trên sinh viên học tiếng Anh (EFL) tại Việt Nam ([Ho & Truong, 2022; Nguyen, 2025](https://www.researchgate.net/publication/415825970_EFL_speaking_anxiety_among_Vietnamese_university_students); [Phenomenological Analysis of Vietnamese EFL Learners, 2024](https://www.researchgate.net/publication/381382699_A_Phenomenological_Analysis_of_the_Obstacles_Impeding_Vietnamese_EFL_Learners'_Willingness_to_Communicate_in_English)) khẳng định rào cản văn hóa **sợ mất thể diện (*fear of losing face*)** trước lớp khiến đa số học viên Việt Nam chọn cách giữ im lặng (*classroom silence*) ngay cả khi không hiểu tại sao câu trắc nghiệm TOEIC/IELTS đó lại chọn đáp án B.
   - 👉 **Cách EduSync giải quyết (Học tập an toàn tâm lý — Psychological Safety):** Thay vì phải ngại ngùng giơ tay hỏi lại giáo viên giữa lớp:
     - Học viên tự bấm vào **Badge Ngữ pháp** trên câu làm sai (do mô hình **Dense Embeddings `all-MiniLM-L6-v2`** tự động nối) để nhảy ngược về đúng phút cô giảng công thức gốc (`00:49`), tự nghe lại đoạn phát âm mẫu 1.5s bao nhiêu lần tùy thích.
     - Mọi câu trả lời trong khung chat được **ẩn danh hoàn toàn thành `S1, S2...` (chuẩn FERPA)** trước khi sửa lỗi, giúp học viên biết rõ lỗi sai của mình mà không bao giờ sợ bị bạn bè chê cười.

3. **Bằng chứng về "Phản hồi Tức thì giúp Tăng sự Tự tin & Quyết tâm Ôn thi" (Self-Efficacy & Learner Autonomy):**
   - Nghiên cứu của **[Farmani, Akbari, & Ghanizadeh (2017)](https://www.researchgate.net/publication/321063268_The_impact_of_immediate_and_delayed_error_correction_on_Iranian_EFL_learner's_self-efficacy)** (dựa trên Lý thuyết Tự hiệu quả *Self-Efficacy* của Bandura, 1997) và **[Nghiên cứu về Phản hồi Sửa lỗi bằng AI cho người học EFL](https://pdfs.semanticscholar.org/2e0c/e108d8a4d775b137e7b02014720296fae4e5.pdf)** chỉ ra rằng: khi người học nhận được **phản hồi sửa lỗi tức thì, rõ ràng và không phán xét (*immediate, non-judgmental corrective feedback*)**, họ phát triển năng lực tự kiểm soát lỗi (*self-monitoring*), giảm lo âu thi cử và tăng mạnh **sự tự tin (*self-efficacy*)** cũng như **quyết tâm kiên trì ôn tập (*persistence & motivation*)**.
   - 👉 **Cách EduSync giải quyết:** Module **ERRANT GEC (`feedback.py`)** tự động bắt 6 nhóm lỗi chuyển di ngôn ngữ Việt–Anh (*L1 Transfer*) ngay trong tin nhắn chat và giải thích cặn kẽ bằng tiếng Việt, kết hợp phân tầng từ vựng **CEFR (A1–C2)** rõ ràng giúp học viên thấy lộ trình chinh phục bài thi TOEIC/IELTS nằm trong tầm tay.

> 💡 **Điểm nhấn trình bày với Giảng viên:**  
> Ba nỗi đau trên không thể giải quyết bằng các công cụ cắt ghép video thông thường, mà đòi hỏi **Xử lý Ngôn ngữ Tự nhiên Đa phương thức (Multimodal NLP)** vì dữ liệu đầu vào bị trộn mã Việt–Anh (*Code-switching*), lệch từ vựng (*Vocabulary Mismatch*) giữa đề bài và lý thuyết, và chứa ngôn ngữ người học có nhiễu (*Noisy Learner Text*).

---

## 2. Ý Tưởng Đột Phá: Mô Hình "Nút Tri Thức Đa Phương Thức" (Multimodal Knowledge Node)

EduSync không xem buổi học là một luồng video tuyến tính, mà tự động bóc tách và liên kết **4 luồng dữ liệu** (Âm thanh lời giảng Việt–Anh, Hình ảnh màn hình đề thi, Khung lý thuyết ngữ pháp/từ vựng, và Luồng Chat học viên) thành các **Nút Tri thức Tương tác 2 Chiều**:

```text
                ┌──────────────────────────────────────────────────────────┐
                │      BẢN GHI BUỔI HỌC TOEIC / IELTS (ZOOM / MEET)        │
                │   🎥 Video màn hình + 🎙️ Audio Việt-Anh + 💬 Log Chat     │
                └────────────────────────────┬─────────────────────────────┘
                                             │
                       [Đường ống 7 Kỹ thuật NLP Cốt lõi (EduSync)]
                                             ▼
   ┌─────────────────────────┐     ┌─────────────────────┐     ┌──────────────────────────┐
   │  ⏱️ LÝ THUYẾT GỐC       │     │ 📝 CÂU HỎI BÀI TẬP  │     │ 💬 PHẢN HỒI CHAT & VOCAB │
   │  Phút 00:49 – 08:13     │◄───►│ Câu 4 (Phút 15:06)  │◄───►│ • Chat: "movie was moved"│
   │  Chủ điểm: Participles  │Liên │ "The movie was ___  │Liên │   ➔ Lỗi R:ADJ:PARTICIPLE │
   │  (-ing: bản chất sự vật │kết  │  because it made me │kết  │ • Vocab: moving (B1)     │
   │   -ed: cảm xúc người)   │Vector│  cry." (A/B/C/D)   │Thực │   ➔ Audio cô đọc 1.5s    │
   └─────────────────────────┘     └─────────────────────┘thể  └──────────────────────────┘
                 │                            │                              │
                 └────────────────────────────┼──────────────────────────────┘
                                              ▼
         ┌────────────────────────────────────┴────────────────────────────────────┐
         ▼                                                                         ▼
🎓 SỔ TAY TƯƠNG TÁC CHO HỌC VIÊN                                📊 DASHBOARD SƯ PHẠM CHO GIÁO VIÊN
• Bấm câu hỏi ➔ Tua đúng giây cô chữa (15:06)                  • Đo tỷ lệ nói TTT (98.2%) vs STT (1.8%)
• Bấm Badge Ngữ pháp ➔ Tua ngược về Lý thuyết (00:49)          • Bản đồ nhiệt 6 loại lỗi ngữ pháp ERRANT
• Lọc từ vựng CEFR (A1–C2) + Nghe audio 1.5s giọng cô          • Cảnh báo chủ điểm lớp sai nhiều nhất
• Xem sửa lỗi ngữ pháp chat + Giải thích tiếng Việt            • Tự động sinh Kế hoạch 3 bước buổi học sau
```

---

## 3. So Sánh Trực Quan: Trước và Sau Khi Có EduSync

| Tiêu chí | ❌ Trước khi có EduSync (Cách học cũ) | ✅ Sau khi có EduSync (Ứng dụng NLP) | Kỹ thuật NLP đứng sau |
| :--- | :--- | :--- | :--- |
| **Tìm câu chữa bài tập TOEIC / IELTS** | Kéo thanh trượt video mò mẫm 15–20 phút cho 1 câu sai. | **Click 1 chạm (< 50ms):** Bấm vào Câu 4, video nhảy ngay tới giây `15:06` lúc cô bắt đầu chữa. | **Monotonic DP Alignment** + Regex Negative Lookbehind (`exercise_align.py`) |
| **Ôn lại công thức ngữ pháp gốc** | Không biết câu trắc nghiệm này thuộc quy tắc ngữ pháp nào. | **Liên kết 2 chiều:** Bấm Badge `🏷️ Participles (-ing/-ed)` nhảy thẳng về phút `00:49` nghe lại lý thuyết. | **Dense Semantic Embeddings** `all-MiniLM-L6-v2` + Cosine Similarity (`concept_link.py`) |
| **Học từ vựng & Luyện phát âm** | Tự tra từ điển rời rạc, nghe giọng đọc robot vô hồn. | **79 thẻ từ vựng phân bậc CEFR (A1–C2)** kèm nghĩa tiếng Việt cô giảng & **Audio 1.5s giọng thật của cô**. | **2-Stage Lemmatizer + CEFR-J Lexicon** + Pattern Bilingual IE (`vocab.py`) |
| **Sửa lỗi ngữ pháp khi tương tác Chat** | Bình luận sai trong Zoom chat bị trôi mất, không ai sửa. | Tự động gạch lỗi sai (`<del>`), gợi ý từ đúng (`<ins>`) và **giải thích quy tắc bằng tiếng Việt**. | **ERRANT Taxonomy GEC** (6 nhóm lỗi L1 Transfer) + Ẩn danh FERPA (`feedback.py`) |
| **Đánh giá chất lượng buổi dạy (Giáo viên)** | Kết thúc lớp không có số liệu, dạy buổi sau theo cảm tính. | Có ngay **Dashboard định lượng:** Tỷ lệ nói TTT/STT, Biểu đồ lỗi sai cả lớp & **Action Plan 3 bước**. | **Speaker Diarization** + Pedagogical Analytics Engine (`teacher_analytics.py`) |

---

## 4. Ba Câu Hỏi Nghiên Cứu (Research Questions) & Đóng Góp Kỹ Thuật NLP

Để thuyết phục Hội đồng chấm đồ án về **hàm lượng học thuật NLP**, đề tài đặt ra và giải quyết 3 câu hỏi nghiên cứu cốt lõi:

### 🔹 RQ1 (Tầng Tiếng nói & Đa phương thức): Làm sao nhận diện chính xác lời giảng trộn mã Việt–Anh (Code-switching) và căn chỉnh đúng tới từng giây cho 100% câu hỏi khi video không có file Slide PDF gốc?
- **Thách thức NLP:** Giáo viên giảng bằng tiếng Việt (~74%) xen lẫn đọc đề và từ vựng tiếng Anh (~26%). Mô hình ASR thông thường dễ biến từ tiếng Anh đọc lướt thành từ sai (*"his shoes shined"* $\to$ *"his sue signed"*), còn khi căn chỉnh câu hỏi thì dễ bị nhảy lùi thời gian khi giáo viên nhắc lại câu cũ (*"câu 6 này giống câu 2 lúc nãy"*).
- **Giải pháp Technical NLP:**
  1. **Contextual Biasing ASR (`Screen Hints`):** Bóc tách khung hình đề bài từ video bằng biến đổi pixel (`extract_screens.py`), chạy OCR lấy các từ vựng tiếng Anh trên đề thi làm `initial_prompt` bơm vào bộ giải mã của `faster-whisper` (`large-v3-turbo`), giúp **giảm 50% lỗi WER thuật ngữ (từ 18.4% xuống 9.2%)**.
  2. **Monotonic Dynamic Programming Alignment (`exercise_align.py`):** Cài đặt quy hoạch động đơn điệu ép ràng buộc nhân quả $t_{\text{start}}^{(1)} < t_{\text{start}}^{(2)} < \dots < t_{\text{start}}^{(N)}$ kết hợp Regex Negative Lookbehind `(?<!text\s)(?<!page\s)` (tránh nhầm *Text 1, Page 2* thành *Câu 1, Câu 2*), đạt **Recall 100% (34/34 câu hỏi)** với sai số biên trung bình chỉ **$\le 1.8$ giây**.

### 🔹 RQ2 (Tầng Ngữ nghĩa Vector): Làm sao tự động nối một câu hỏi bài tập TOEIC/IELTS về đúng chủ điểm ngữ pháp lý thuyết khi không có bất kỳ từ khóa nào trùng nhau?
- **Thách thức NLP (Lexical Gap / Vocabulary Mismatch):** Câu hỏi trắc nghiệm chỉ chứa từ vựng tình huống (*"I think the movie was _____ because it made me cry"*), trong khi chủ điểm lý thuyết chứa thuật ngữ trừu tượng (*"Participles as Adjectives"*). Các phương pháp khớp từ khóa như TF-IDF hay BM25 trả về điểm tương đồng bằng $0$.
- **Giải pháp Technical NLP:**
  - Sử dụng mạng **Siamese Bi-Encoder Transformer (`sentence-transformers/all-MiniLM-L6-v2`)** nhúng cả câu hỏi (Stem + Options + Lời giảng) và chủ điểm ngữ pháp vào không gian vector đơn vị $\mathbb{R}^{384}$ ($\|\vec{v}\|_2 = 1$).
  - Tính ma trận tích vô hướng **Cosine Similarity** $S = Q \cdot G^T$ để tìm chủ điểm ngữ pháp có độ tương đồng ngữ nghĩa cực đại trong **4.2 ms/câu**, kết hợp **Hybrid Neural IE** (`neural_ie.py` dùng Gemini Flash-Lite JSON Schema + Rule Fallback) để bóc tách công thức và mẹo thi TOEIC/IELTS.

### 🔹 RQ3 (Tầng Ngôn ngữ Người học & Phân tích Sư phạm): Làm sao tự động phân bậc từ vựng CEFR theo mục tiêu điểm TOEIC/IELTS và chẩn đoán lỗi ngữ pháp của học viên Việt Nam trong khung chat?
- **Thách thức NLP:** Từ vựng trong bài giảng xuất hiện ở dạng biến cách (*moved, cities, bought*) và dễ lẫn với từ tiếng Việt không dấu (*an, may, can, hay, con*). Đồng thời, câu chat của học viên ngắn, chứa lỗi chuyển di ngôn ngữ mẹ đẻ (*L1 Negative Transfer*).
- **Giải pháp Technical NLP:**
  1. **Morphological Lemmatizer 2 lớp & Từ điển CEFR-J (8.845 từ):** Khử biến cách, lọc từ đồng âm xuyên ngôn ngữ (`VI_HOMOPHONES`), phân loại từ vựng từ **A1 đến C2** (tương ứng TOEIC 450–900+ và IELTS Band 5.0–8.0+), trích xuất nghĩa tiếng Việt qua mẫu quan hệ cú pháp (`Word + "nghĩa là" + Nghĩa`) và cắt tự động **79 file audio 1.5s** giọng thật giáo viên.
  2. **Chẩn đoán lỗi chuẩn quốc tế ERRANT (ACL 2019):** Ẩn danh học viên chuẩn FERPA ($S_1 \dots S_N$) và phân loại 6 nhóm lỗi L1 Transfer (`U:VERB:BE`, `R:ADJ:PARTICIPLE`, `R:VERB:FORM`, `U:PREP`, `R:VERB:SVA`, `M:VERB:AUX`), đạt độ chính xác **100% (6/6 lỗi)** trên tập kiểm thử lớp học.

---

## 5. Khả Năng Đáp Ứng Đa Dạng Bài Giảng: Từ TOEIC Đến IELTS 4 Kỹ Năng

Hệ thống EduSync được thiết kế tổng quát cho mọi bài giảng luyện thi tiếng Anh chuẩn hóa:

| Khía cạnh | Ứng dụng trên Bài giảng TOEIC (Part 1 – Part 7) | Ứng dụng trên Bài giảng IELTS (Academic & General) |
| :--- | :--- | :--- |
| **Căn chỉnh Bài tập & Đề thi** | Căn chỉnh từng câu trắc nghiệm **Part 5 (Incomplete Sentences)**, **Part 6 (Text Completion)** và các đoạn đọc **Part 7**. | Căn chỉnh từng câu hỏi **IELTS Reading / Listening** (Multiple Choice, Gap-fill, Matching) với đoạn giáo viên phân tích *Paraphrase & Keywords*. |
| **Liên kết Lý thuyết & Chiến thuật** | Nối câu hỏi từ loại, chia thì, phân từ, mệnh đề quan hệ về đúng công thức ngữ pháp và **Mẹo tránh bẫy TOEIC**. | Nối câu hỏi về đúng chiến thuật làm bài (*Skimming, Scanning, True/False/Not Given*) hoặc cấu trúc câu ăn điểm **IELTS Writing Task 1 & 2**. |
| **Từ vựng theo Mục tiêu Điểm số** | Lọc từ vựng thương mại & giao tiếp công sở bậc **A2 – B2** (mục tiêu **TOEIC 550 – 800+**). | Lọc từ vựng học thuật (*Academic Word List*) bậc **B2 – C2** (mục tiêu **IELTS Band 6.5 – 8.0+**). |
| **Sửa lỗi GEC & Phân tích Tương tác** | Sửa lỗi ngữ pháp khi học viên giải thích đáp án trong chat; đo tỷ lệ tương tác của lớp chữa đề. | Chẩn đoán lỗi tiêu chí **Grammatical Range & Accuracy (GRA)** trong câu viết của học viên và đo thời lượng nói **IELTS Speaking (TTT/STT)**. |

---

## 6. Kết Quả Thực Nghiệm & Kiểm Chứng Chất Lượng (45/45 Unit Tests PASS)

Toàn bộ giải pháp đã được hiện thực hóa thành mã nguồn hoàn chỉnh (~4.950 dòng code) và kiểm nghiệm trên dữ liệu thực tế:

| Hạng mục Đánh giá | Bộ Dữ liệu / Công cụ Kiểm chứng | Kết quả Đạt được | Ý nghĩa khi Báo cáo với Giảng viên |
| :--- | :--- | :--- | :--- |
| **Độ chính xác ASR Thuật ngữ** | Bài giảng ECE TOEIC Starter (Unit 1, 4, 5 — ~3 giờ video) | Giảm WER từ **18.4% $\to$ 9.2%** | Chứng minh hiệu quả thực sự của kỹ thuật *OCR Screen Hints Prompting*. |
| **Căn chỉnh Câu hỏi Bài tập** | 34 câu hỏi trắc nghiệm Part 5 & Part 6 (Unit 4 - 63 phút) | **Recall 100% (34/34 câu)**, Precision **97.1%**, sai số $\le 1.8\text{s}$ | Không bỏ sót câu nào, không bị nhảy lùi thời gian nhờ *Monotonic DP*. |
| **Kiểm chuẩn Hồi quy Học thuật** | Bài giảng chuẩn Stanford CS224N (43 slides, 54 phút) | Khớp **9/10 mốc nhãn chuẩn**, sai số trung bình **0.6 giây** | Khẳng định thuật toán căn chỉnh đạt độ chính xác cao trên cả benchmark quốc tế. |
| **Khai phá Từ vựng & Audio** | Toàn bộ phụ đề song ngữ Việt–Anh của bài giảng | **79 từ vựng CEFR (A1–C1)** + **43 nghĩa tiếng Việt** + **79 file `.mp3`** | Tạo bộ học liệu sống động từ chính giọng đọc và lời giảng của giáo viên. |
| **Liên kết Khái niệm & GEC Chat** | 34 câu hỏi + 4 chủ điểm ngữ pháp + 17 tin nhắn Zoom chat | Suy luận **4.2 ms/câu**; bắt đúng **6/6 (100%) lỗi ERRANT** | Giải quyết trọn vẹn bài toán *Vocabulary Mismatch* và chẩn đoán lỗi *L1 Transfer*. |
| **Kiểm thử Phần mềm Tự động** | 10 bộ kiểm thử `pytest -v` trong thư mục `tests/` | **45 / 45 Unit Tests PASSED (100%)** trong 7.5 giây | Đảm bảo chất lượng kỹ thuật phần mềm theo chuẩn chương trình Thạc sĩ MSE. |

---

## 7. Phân Công Nhóm (4 Thành Viên) & Lộ Trình Trình Bày 20 Phút

| Thành viên | Vai trò trong Dự án | Các Module Phụ trách | Phần Trình bày trong Buổi Bảo vệ |
| :--- | :--- | :--- | :--- |
| **Thành viên 1** | **Project Lead & Requirement Engineer** | Phân tích bài toán sư phạm TOEIC/IELTS, đặc tả SRS (IEEE 830), kiến trúc 4 tầng & bảo mật FERPA. | **Phần 1 (Slide 01–04 | 4.5 phút):** Đặt vấn đề, 3 điểm nghẽn lớp học TOEIC/IELTS, mục tiêu 2 trụ cột & kiến trúc tổng thể. |
| **Thành viên 2** | **Multimodal & Alignment Engineer** | Thu nhận video/OCR (`extract_screens.py`), Whisper Screen Hints (`transcribe.py`), Monotonic DP (`exercise_align.py`). | **Phần 2 (Slide 05–08 | 4.5 phút):** Xử lý âm thanh Code-switching Việt–Anh, bơm ngữ cảnh OCR và thuật toán quy hoạch động đơn điệu. |
| **Thành viên 3** | **Core NLP & Semantic Engineer** | Phân bậc từ vựng CEFR & cắt audio (`vocab.py`), Dense Embeddings (`concept_link.py`), ERRANT GEC (`feedback.py`), Neural IE (`neural_ie.py`). | **Phần 3 (Slide 09–13 | 5.0 phút):** Lemmatization CEFR-J, không gian vector `all-MiniLM-L6-v2` (Cosine Similarity), bắt lỗi ERRANT & Hybrid IE. |
| **Thành viên 4** | **System, Analytics & QA Engineer** | Phân tách người nói (`diarize.py`), Teacher Dashboard (`teacher_analytics.py`), Web Demo SPA (`demo/`) & 45 Unit Tests (`tests/`). | **Phần 4 (Slide 14–18 | 6.0 phút):** Báo cáo sư phạm cho giáo viên, **Trình diễn Live Demo trực tiếp** tại `http://localhost:8000/` & tổng kết QA/QC. |

---

## 🔗 Tài Liệu Tham Chiếu Nhanh Khi Trình Bày
- **Xem chi tiết 7 kỹ thuật NLP & 8 câu hỏi phản biện của Giảng viên:** [`09_teacher_presentation_and_technical_nlp_guide.md`](09_teacher_presentation_and_technical_nlp_guide.md)
- **Mở trực tiếp bộ Slide HTML tương tác (có đồng hồ & lời thoại phím `N`):** [`slides.html`](slides.html)
- **Xem kịch bản 5 bước thao tác Live Demo (90 giây):** [`06_user_guide_and_demo.md`](06_user_guide_and_demo.md)
