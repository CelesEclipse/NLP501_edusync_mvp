---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section {
    background: #fcfcfb; color: #1f1f1d;
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 21px; line-height: 1.38; padding: 40px 54px 46px;
    display: flex !important; flex-direction: column !important; justify-content: flex-start !important;
  }
  h1 { font-size: 32px; margin: 0 0 2px; color: #1f1f1d; font-weight: 700; }
  h2 { font-size: 19px; margin: 0 0 16px; color: #5f5e58; font-weight: 400; }
  h3 { font-size: 20px; margin: 0 0 6px; color: #1c5cab; }
  strong { color: #1c5cab; }
  ul, ol { margin: 4px 0 0 0; padding-left: 22px; }
  li { margin-bottom: 4px; }
  table { font-size: 17px; border-collapse: collapse; margin: 6px 0; }
  th { background: #eef4fc; color: #1f1f1d; font-weight: 600; padding: 5px 10px; border: none; }
  td { padding: 4px 10px; border: none; border-bottom: 1px solid #e6e5e0; background: transparent; }
  tr:nth-child(2n) td { background: transparent; }
  code { background: #f1f0ec; color: #1f1f1d; padding: 1px 5px; border-radius: 4px; font-size: 0.86em; }
  footer { font-size: 12px; color: #8a8980; }
  section::after { font-size: 13px; color: #8a8980; }
  .who { position: absolute; top: 16px; right: 54px; font-size: 13px; font-weight: 600; letter-spacing: .4px;
         padding: 3px 10px; border-radius: 6px; }
  .tv1 { background: #e3eefb; color: #1c5cab; } .tv2 { background: #fdeee6; color: #a8461d; }
  .tv3 { background: #e2f5ec; color: #11734f; } .tv4 { background: #fdf3dc; color: #8a5b00; }
  .cols { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
  .cols-62 { display: grid; grid-template-columns: 1.25fr 1fr; gap: 26px; }
  .box { background: #f4f4f1; border-radius: 10px; padding: 12px 16px; }
  .note { font-size: 15.5px; color: #5f5e58; }
  .big { font-size: 40px; font-weight: 700; color: #1c5cab; line-height: 1.1; }
  .formula { font-family: "SF Mono", Menlo, monospace; font-size: 17px; background: #f1f0ec; border-radius: 8px;
             padding: 8px 12px; margin: 6px 0; }
  img { display: block; }
  section.lead { justify-content: center !important; }
  section.lead h1 { font-size: 52px; color: #1c5cab; }
  section.lead h2 { font-size: 24px; margin-bottom: 28px; }
---

<!-- _class: lead -->

<div class="who tv1">TV1 · 00:00</div>

# EduSync
## Căn chỉnh đa phương thức và phân tích bài giảng luyện thi TOEIC

<div class="cols">
<div class="box">

### Đề tài
- Đầu vào: video quay màn hình, lời giảng có cả Tiếng Việt - Anh, log chat
- Đầu ra: **sổ tay học viên** (tua theo câu hỏi, chủ điểm, từ vựng, phản hồi chat)
- Môn NLP501

</div>
<div class="box">

### Thành viên thực hiện
- Phạm Đức Bình
- An Ngọc Quang
- Tạ Quang Minh
- Nguyễn Minh Châu

</div>
</div>

<!--
TV1: Chào thầy/cô. Nhóm em trình bày EduSync: từ bản ghi một buổi luyện thi TOEIC, hệ thống tạo sổ tay học tập tương tác cho học viên. Tất cả số liệu trong bài nằm ở docs/10 và tái tạo được bằng một lệnh.
-->

---

<div class="who tv1">TV1</div>

# Vấn đề
## Sau buổi học qua Online chỉ còn video dài hàng giờ và một file chat

<div class="cols">
<div>

### Học viên
- Muốn xem lại đoạn chữa một câu phải tua thủ công. Thời gian xem trung vị của video bài giảng chỉ khoảng **6 phút** (Guo et al., L@S 2014); các đỉnh tua tập trung quanh chỗ chuyển cảnh (Kim et al., L@S 2014).
- Ngại hỏi lại trước lớp: sợ bị đánh giá tiêu cực (Horwitz et al., 1986).
- Lỗi sai trong chat trôi mất sau buổi học, thiếu phản hồi sửa lỗi kịp thời.

</div>
<div class="box">

### Mục tiêu của EduSync
1. Bấm một câu hỏi → video tua đến lúc cô **bắt đầu chữa** câu đó
2. Câu hỏi → **chủ điểm ngữ pháp** → đoạn giảng lý thuyết
3. Từ vựng theo bậc **CEFR**, nghĩa tiếng Việt cô giảng, audio giọng cô
4. Chat: phát hiện **lỗi điển hình của người Việt**, giải thích bằng tiếng Việt

</div>
</div>

<!--
TV1: Khó khăn của học viên khi học online: tìm lại đoạn chữa bài, ngại hỏi lại, và lỗi trong chat bị trôi mất. Bốn mục tiêu bên phải tương ứng với các bài toán NLP ở slide sau.
-->

---

<div class="who tv1">TV1</div>

# Bài toán NLP và dữ liệu

<div class="cols-62">
<div>

### Bốn bài toán con
1. **Căn chỉnh đơn điệu**: câu hỏi $e_k$ → thời điểm $t_k$, với $t_1 < t_2 < \dots$
2. **Liên kết** câu hỏi → chủ điểm $g \in G \cup \{\text{none}\}$
3. **Từ vựng**: lemma, bậc CEFR, nghĩa tiếng Việt lấy từ lời giảng
4. **Lỗi người học** trong chat: 6 mẫu chuyển di từ tiếng Việt

### Thách thức
- Lời giảng có cả Tiếng Việt - Anh: 73% đoạn tiếng Việt, 26% tiếng Anh
- OCR nhiễu; số câu đánh lại từ 1 ở mỗi phần
- Câu hỏi và tên chủ điểm thường không có từ chung

</div>
<div>

| Bài (YouTube, CC BY) | Dài | Vai trò |
|---|---|---|
| ECE TOEIC Starter Unit 4 | 58′ · 34 câu | phát triển |
| ECE TOEIC Starter Unit 5 | 58′ · 35 câu | **kiểm tra độc lập** |
| ECE TOEIC Starter Unit 1 | 65′ | ASR |
| **8 video TOEIC tiếng Việt, 6 kênh khác** | 3 giờ 9′ · 68 câu | **kiểm tra tổng quát hóa** |

<p class="note">Unit 4 / Unit 5 có <b>một người nói</b> (giáo viên). Chat của Unit 4 (17 tin nhắn) là <b>dữ liệu mô phỏng</b>. Nhãn chuẩn là bản nháp do AI gán, chưa xem output hệ thống; nhóm đang kiểm tra lại với video.</p>

</div>
</div>

<!--
TV1: Bốn bài toán con. Về dữ liệu: em nói rõ ba điểm giới hạn — một người nói, chat là mô phỏng, nhãn là bản nháp. Thuật toán được chỉnh trên Unit 4 và chỉ chạy một lần trên Unit 5 để kiểm tra. Vì Unit 4 và Unit 5 cùng một giáo viên, nhóm thêm 8 video TOEIC tiếng Việt của 6 kênh khác để kiểm tra tổng quát hóa; kết quả ở phần của TV2.
-->

---

<div class="who tv1">TV1</div>

# Kiến trúc
## Ba điểm kết hợp giữa các luồng dữ liệu (①–③)

<svg viewBox="0 0 1180 420" width="1170" height="400" xmlns="http://www.w3.org/2000/svg" font-family="Helvetica Neue, Arial" font-size="15">
  <defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8a8980"/></marker></defs>
  <g fill="#eef4fc" stroke="#2a78d6" stroke-width="1.5">
    <rect x="10" y="40" width="170" height="56" rx="8"/><rect x="10" y="190" width="170" height="56" rx="8"/><rect x="10" y="340" width="170" height="56" rx="8"/>
  </g>
  <g fill="#1f1f1d" font-weight="600"><text x="95" y="73" text-anchor="middle">Video màn hình</text><text x="95" y="215" text-anchor="middle">Lời giảng</text><text x="95" y="234" text-anchor="middle" font-weight="400" font-size="13">Tiếng Việt - Anh</text><text x="95" y="365" text-anchor="middle">Log chat</text><text x="95" y="384" text-anchor="middle" font-weight="400" font-size="13">(mô phỏng)</text></g>
  <g fill="#f4f4f1" stroke="#b9b8b0" stroke-width="1.2">
    <rect x="240" y="30" width="230" height="56" rx="8"/><rect x="240" y="125" width="230" height="56" rx="8"/><rect x="240" y="225" width="230" height="56" rx="8"/><rect x="240" y="335" width="230" height="56" rx="8"/>
    <rect x="550" y="25" width="250" height="56" rx="8"/><rect x="550" y="105" width="250" height="56" rx="8"/><rect x="550" y="185" width="250" height="56" rx="8"/><rect x="550" y="265" width="250" height="56" rx="8"/><rect x="550" y="335" width="250" height="56" rx="8"/>
  </g>
  <g fill="#1f1f1d" text-anchor="middle">
    <text x="355" y="52">Tách màn hình + OCR</text><text x="355" y="70" font-size="12" fill="#5f5e58">extract_screens.py</text>
    <text x="355" y="147">Bóc câu hỏi A–D</text><text x="355" y="165" font-size="12" fill="#5f5e58">exercises.py</text>
    <text x="355" y="247">ASR (Whisper) + nhãn vi/en</text><text x="355" y="267" font-size="12" fill="#5f5e58">transcribe.py</text>
    <text x="355" y="357">Ẩn danh S1…SN + đáp án</text><text x="355" y="377" font-size="12" fill="#5f5e58">chat_parser.py</text>
    <text x="675" y="47">Căn chỉnh câu hỏi (DP)</text><text x="675" y="67" font-size="12" fill="#5f5e58">exercise_align.py</text>
    <text x="675" y="127">Liên kết câu hỏi ↔ chủ điểm</text><text x="675" y="147" font-size="12" fill="#5f5e58">concept_link.py · e5 + lời giảng</text>
    <text x="675" y="207">Chủ điểm + neo mốc lý thuyết</text><text x="675" y="227" font-size="12" fill="#5f5e58">neural_ie.py · Gemini + e5</text>
    <text x="675" y="287">Từ vựng CEFR + audio</text><text x="675" y="305" font-size="12" fill="#5f5e58">vocab.py</text>
    <text x="675" y="357">Phát hiện 6 nhóm lỗi</text><text x="675" y="377" font-size="12" fill="#5f5e58">feedback.py</text>
  </g>
  <g fill="#e8f6ef" stroke="#1baf7a" stroke-width="1.5"><rect x="890" y="145" width="270" height="130" rx="8"/></g>
  <g fill="#1f1f1d" text-anchor="middle" font-weight="600" font-size="18"><text x="1025" y="205">Sổ tay học viên</text></g>
  <g fill="#5f5e58" text-anchor="middle" font-size="13"><text x="1025" y="235">demo/index.html</text></g>
  <g stroke="#8a8980" stroke-width="1.4" fill="none" marker-end="url(#a)">
    <path d="M180,68 L238,58"/><path d="M355,86 L355,123"/><path d="M180,218 L238,253"/><path d="M180,368 L238,363"/>
    <path d="M470,150 L548,53"/><path d="M470,245 L548,63"/><path d="M470,253 L548,213"/><path d="M470,263 L548,293"/><path d="M470,363 L548,363"/>
    <path d="M675,185 L675,163"/><path d="M800,53 L888,180"/><path d="M800,133 L888,195"/><path d="M800,213 L888,210"/><path d="M800,293 L888,225"/><path d="M800,363 L888,240"/>
  </g>
  <path d="M470,58 H495 V245 H472" stroke="#2a78d6" stroke-width="1.6" stroke-dasharray="6 4" fill="none" marker-end="url(#a)"/>
  <path d="M675,81 L675,103" stroke="#2a78d6" stroke-width="2" fill="none" marker-end="url(#a)"/>
  <g font-weight="700" font-size="15" fill="#fff">
    <circle cx="505" cy="148" r="12" fill="#2a78d6"/><text x="505" y="153" text-anchor="middle">1</text>
    <circle cx="522" cy="78" r="12" fill="#2a78d6"/><text x="522" y="83" text-anchor="middle">2</text>
    <circle cx="700" cy="94" r="12" fill="#2a78d6"/><text x="700" y="99" text-anchor="middle">3</text>
  </g>
</svg>

<p class="note"><b>ASR</b> (Automatic Speech Recognition): nhận dạng tiếng nói tự động, chuyển âm thanh lời giảng thành văn bản transcript.<br>① chữ OCR của màn hình đang chiếu làm gợi ý cho ASR (thử nghiệm) · ② thời điểm màn hình + lời giảng → căn chỉnh · ③ lời giảng trong đoạn chữa câu → liên kết chủ điểm</p>

<!--
TV1: Ba luồng vào: video, lời giảng, chat. Điểm đáng chú ý là ba chỗ các luồng kết hợp với nhau, đánh số 1 đến 3. Ví dụ số 3: lời cô giảng khi chữa một câu giúp xác định câu đó thuộc chủ điểm nào. Em mời TV2.
-->

---

<div class="who tv1">TV1</div>

# Nghiên cứu liên quan

| Công trình | Ý chính | EduSync dùng / khác gì |
|---|---|---|
| Anderer et al. 2024, MaViLS (arXiv 2409.16765) | Căn chỉnh video ↔ slide bằng ASR + OCR + đặc trưng hình ảnh, quy hoạch động | Không có slide gốc; căn chỉnh tới **từng câu hỏi** |
| Radford et al., ICML 2023 (Whisper) | ASR đa ngữ quy mô lớn, điều kiện hóa bằng văn bản đi trước | ASR lời giảng có cả Tiếng Việt - Anh; thử gợi ý từ màn hình |
| Peng et al., Interspeech 2023 | Dùng prompt để điều khiển Whisper zero-shot | Cơ sở cho gợi ý theo ngữ cảnh màn hình |
| Reimers & Gurevych 2019; Wang et al. 2022/2024 (E5, mE5) | Bi-encoder câu; embedding đa ngữ | Liên kết câu hỏi tiếng Anh ↔ chủ điểm giảng bằng tiếng Việt |
| Bryant, Felice & Briscoe, ACL 2017 (ERRANT) | Tự động gán loại lỗi cho cặp câu gốc / câu sửa | Gán loại lỗi; nhãn kiểm chứng bằng errant 3.0.2 |
| CEFR-J Wordlist; English Vocabulary Profile | Từ vựng phân bậc A1–C2 | Từ điển 8.845 mục (CEFR-J + Octanove) |

<!--
TV1: Gần nhất với nhóm là MaViLS: căn chỉnh video với slide bằng quy hoạch động. Khác biệt của nhóm là không có slide gốc và cần căn chỉnh tới từng câu hỏi trắc nghiệm.
-->

---

<div class="who tv2">TV2 · 04:30</div>

# Nhận dạng lời giảng có cả Tiếng Việt - Anh

<div class="box">

### Cách làm
- `faster-whisper large-v3-turbo`, chế độ đa ngữ, chạy trên máy cá nhân
- Gán ngôn ngữ cho từng đoạn theo **mật độ chữ có dấu**: > 0,3 → `vi`; 0 → `en`; còn lại → `mixed`
- Thử nghiệm: lấy từ tiếng Anh trên **màn hình đang chiếu** (OCR) làm `hotwords` cho Whisper ①

</div>

<!--
TV2: Bọn em chưa có WER, vì bản chép tham chiếu chưa sửa tay xong. Thử nghiệm gợi ý từ màn hình có tác dụng hai chiều: nhận được nhiều từ trên màn hình hơn, nhưng số đoạn lặp tăng. Vì vậy pipeline chưa bật gợi ý.
-->

---

<div class="who tv2">TV2</div>

# Căn chỉnh câu hỏi ↔ lời giảng
## Quy hoạch động đơn điệu với khẩu lệnh có xác minh ngữ cảnh

<div class="cols">
<div>

<div class="formula">s(k, j) = 25·trigger + 2·|từ chung| + 3·đang_chiếu</div>

- **trigger**: đoạn $j$ nói "câu (số/thứ) N", "câu hỏi số N", "câu thứ tư"; loại "text / page / part / trang N"
- **Xác minh**: nếu 60 s sau đó không có từ nào của câu hỏi thì trigger chỉ được **2** điểm thay vì 25

<div class="formula">D[k][j] = s(k,j) + max(0, max D[k′][j′]) với k′ &lt; k, t(j′) &lt; t(j)</div>

- Tối ưu toàn cục, cho phép bỏ qua câu; sau đó **lùi mốc** về các đoạn ngay trước có chung từ với câu hỏi

</div>
<div class="box">

### Tình huống thật ở Unit 4
Màn hình chiếu **Exercise B**, nhưng cô chữa **Exercise A trong sách** trước:

> "…chúng ta sẽ bước vào làm câu số 1." (03:09): nói về Exercise A, không có từ nào của câu B1

Bản cũ gán câu B1 vào 03:09 (lệch 216 s). Bản mới bỏ qua khẩu lệnh không được xác minh này và chọn 07:05, trong đoạn cô chữa câu B1 (lệch 21 s so với nhãn 06:45).

</div>
</div>

<!--
TV2: Điểm của mỗi đoạn gồm khẩu lệnh "câu N", số từ trùng với câu hỏi, và việc màn hình câu đó có đang chiếu không. Thay đổi quan trọng nhất là xác minh khẩu lệnh: "câu số 1" chỉ được tính đủ điểm nếu ngay sau đó cô nói về đúng câu này. Bộ giải mã là DP đơn điệu tối ưu toàn cục.
-->

---

<div class="who tv2">TV2</div>

# Kết quả căn chỉnh

<div class="cols-62">
<div>

![w:640](figures/alignment_accuracy.png)

</div>
<div>

### Trên bài kiểm tra độc lập (Unit 5)
- Đúng trong ±10 s: **57% → 80%**
- Sai số trung bình: **28,5 s → 8,1 s**
- Đảo thứ tự câu: **2 → 0**

### Ghi chú trung thực
- Trên cả hai bài, **DP chọn giống greedy**; phần cải thiện đến từ cách tính điểm, bước lùi mốc và cách xử lý câu không khớp
- Lỗi còn lại chủ yếu ở chỗ trống trong đoạn văn (Part 6/7): cô đọc liền cả đoạn nên khó xác định lúc bắt đầu
- Chuẩn so sánh: chỉ dùng thời điểm màn hình đạt 49% (±10 s)
- Unit 4 và Unit 5 cùng giáo viên, cùng sách → slide sau kiểm tra trên video khác

</div>
</div>

<!--
TV2: Thuật toán được chỉnh trên Unit 4 và chỉ chạy một lần trên Unit 5. Trên Unit 5, độ chính xác trong 10 giây tăng từ 57 lên 80 phần trăm. Em nói rõ: DP và greedy cho cùng kết quả trên hai bài này. Nhưng Unit 5 cùng nguồn với Unit 4, nên slide sau là phép thử khó hơn.
-->

---

<div class="who tv2">TV2</div>

# Trên video của giáo viên khác
## 8 video TOEIC tiếng Việt, 6 kênh YouTube (CC BY), 68 câu có nhãn; không chỉnh thuật toán theo bộ này

<div class="cols-62">
<div>

![w:640](figures/multisource_alignment.png)

<p class="note">6 video bài giảng, 45 câu. "Đóng băng" = hệ thống trước khi xem bộ này. "Sau sửa" = <code>exercises.py</code> nhận số câu 3 chữ số (TOEIC 101–200), không còn là kiểm tra độc lập.</p>

</div>
<div>

### Kết quả
- Đầu-cuối: **18%** đúng ±10 s (Unit 5 cùng nguồn: 80%) → **80% không phải độ chính xác chung**
- Cho trước danh sách câu đúng: DP **58%**, gấp đôi greedy và regex (24%)

### Vì sao sai
- **Trích câu từ màn hình** chỉ hợp slide in sẵn "N.": hỏng với bảng viết tay, bảng cuộn, câu chỉ có tranh/audio (tìm được 44% số câu)
- Giáo viên nói "câu này" thay vì "câu 116"; đọc câu hỏi tiếng Anh trước khi màn hình của câu hiện ra

</div>
</div>

<!--
TV2: Unit 4 và Unit 5 cùng một cô, cùng một cuốn sách, nên nhóm tìm thêm video của giáo viên khác. Ngoài YouTube, nhóm không tìm được video bài giảng TOEIC tiếng Việt nào có giấy phép mở. Có 8 video của 6 kênh, gán nhãn 68 câu. Kết quả: hệ thống đóng băng chỉ đúng 18 phần trăm, so với 80 phần trăm trên Unit 5. Khi cho trước danh sách câu đúng thì DP đúng 58 phần trăm, gấp đôi greedy. Như vậy lỗi chính nằm ở bước trích câu từ màn hình, và DP thực sự có ích khi dữ liệu lạ. Em mời TV3.
-->

---

<div class="who tv3">TV3 · 09:40</div>

# Liên kết câu hỏi ↔ chủ điểm ngữ pháp

<div class="cols">
<div>

### Vấn đề
"The movie was very ___ (A) move (B) moving (C) moved" ↔ *Participles as Adjectives*: không có từ chung.

### Bản cũ (v1)
- `all-MiniLM-L6-v2`: chỉ hiểu tiếng Anh, trong khi phần giải thích chủ điểm bằng tiếng Việt
- Ghép thêm **từ khóa viết tay**, trong đó có cả từ đáp án (`central`, `luxury`, `shined`…) → **rò rỉ nhãn**
- Bỏ từ khóa: 76,5% → **61,8%**

</div>
<div class="box">

### Bản hiện tại
<div class="formula">score(q, c) = ½ [cos(E(câu hỏi), E(c)) + cos(E(lời giảng khi chữa q), E(c))]</div>

- E = `multilingual-e5-small` (đa ngữ, 384 chiều)
- Lời giảng ③: *"chọn động từ thêm ing hay thêm ed để làm tính từ"*, *"công thức nhờ vả"*
- Gắn nếu score ≥ 0,835, ngược lại là "không gắn" (câu từ vựng / đọc hiểu)
- Không dùng từ khóa viết tay; dự phòng bằng TF-IDF

</div>
</div>

<!--
TV3: Bản cũ đạt điểm nhờ từ khóa viết tay có chứa cả đáp án; bỏ đi thì tụt xuống 62 phần trăm. Bản mới dùng mô hình đa ngữ, và quan trọng là dùng lời cô giảng trong lúc chữa câu đó — đây chính là tín hiệu đa phương thức.
-->

---

<div class="who tv3">TV3</div>

# Kết quả liên kết chủ điểm (Unit 4, 34 câu)

<div class="cols-62">
<div>

![w:620](figures/concept_linking.png)

</div>
<div>

### Đầu ra thực tế trong demo

| | v1 | Hiện tại |
|---|---|---|
| Độ chính xác | 58,8% | **91,2%** |
| Badge đúng (precision) | 39,1% | **90,0%** |
| Câu có chủ điểm được gắn (recall) | 66,7% | **75,0%** |
| Số badge | 23 | 10 |

<p class="note">22/34 câu là từ vựng / đọc hiểu nên "luôn không gắn" đã đạt 73,5%. Mô hình và ngưỡng được chọn trên chính 34 câu này, và một số ví dụ chủ điểm do Gemini sinh chép gần nguyên câu hỏi, nên kết quả có thể lạc quan; chưa có tập kiểm tra độc lập cho bài toán này.</p>

</div>
</div>

<!--
TV3: Cần so với mốc 73,5 phần trăm của cách "luôn không gắn", vì đa số câu là từ vựng hoặc đọc hiểu. Bản cũ chỉ hơn mốc này 3 điểm. Trong demo cũ, 61 phần trăm badge gắn sai; bản mới còn 1 trên 10.
-->

---

<div class="who tv3">TV3</div>

# Trích xuất chủ điểm và từ vựng

<div class="cols">
<div>

### Chủ điểm: Gemini (JSON mode) + neo mốc
Gemini chỉ thấy khoảng 30 đoạn lấy mẫu nên mốc thời gian nó trả về là đoán. Neo lại vào cửa sổ lời giảng giống chủ điểm nhất (e5):

| Chủ điểm | Nhãn | v1 | Hiện tại |
|---|---|---|---|
| Participles | 00:24 | 15:06 | **00:44** |
| Causative | 15:46 | 17:14 | **15:38** |
| Passive / require that | 13:16 | 55:02 | **13:18** |
| Noun modifiers | 07:20 | 08:13 | **07:35** |

Sai số trung bình: **882,5 s → 11,2 s**. Khi không có mạng: dùng bảng chủ điểm TOEIC và tìm từ khóa trong lời giảng.

</div>
<div>

### Từ vựng (`vocab.py`)
- Lemma 2 lớp (bảng bất quy tắc + bỏ hậu tố)
- Tra **CEFR-J + Octanove** (8.845 mục)
- Lọc từ tiếng Việt trùng mặt chữ tiếng Anh: *hay, con, cho, ra, nam, sau…*
- Lấy nghĩa từ lời giảng: "X là / nghĩa là …"

**Unit 4:** 80 từ (A1 26 · A2 26 · B1 18 · B2 9 · C1 1); 52 từ có nghĩa tiếng Việt; 79 clip audio 0,7–2,2 s giọng cô

<p class="note">Độ đúng của nghĩa và audio chưa được đánh giá.</p>

</div>
</div>

<!--
TV3: Mốc "Lý thuyết" trước đây là do Gemini đoán và lệch gần 42 phút với phần bị động. Neo lại bằng embedding giảm sai số trung bình còn 11 giây.
-->

---

<div class="who tv3">TV3</div>

# Phát hiện lỗi người học trong chat
## Luật cho 6 mẫu lỗi chuyển di từ tiếng Việt; nhãn loại lỗi kiểm chứng bằng errant 3.0.2

| Nhóm | Ví dụ → sửa | Loại ERRANT | Recall |
|---|---|---|---|
| Thừa *be* | I am agree → I agree | U:VERB:TENSE | 50% |
| -ing / -ed | the movie was moved → moving | R:VERB:FORM | 88% |
| Nhờ vả | have my car repair → repaired | R:VERB:FORM | 75% |
| Modal + to | should to increase → should increase | U:VERB:FORM | 100% |
| Hòa hợp chủ vị | it make → it makes | R:VERB:SVA | 63% |
| Thiếu *do* | Why we use…? → Why do we use…? | M:VERB:TENSE | 43% |

<div class="cols">
<div>

**Tập độc lập 70 câu** (viết riêng, không xem luật): v1 P 90% / R 21% → hiện tại **P 100% / R 72,7% / F1 84,2%**

</div>
<div class="note">

Không phải mô hình GEC tổng quát: bỏ qua mọi lỗi ngoài 6 nhóm. Tên học viên được ẩn danh thành S1…SN. Trước khi chốt, tập 70 câu được xem một lần để sửa 3 lỗi cài đặt.

</div>
</div>

<!--
TV3: Bản cũ khớp nguyên văn từng câu chat nên tỉ lệ 6/6 không có ý nghĩa. Bản mới dùng luật tổng quát và được đo trên 70 câu viết độc lập: precision 100 phần trăm, recall 73 phần trăm. Nhãn ERRANT chạy bằng thư viện chính thức. Em mời TV4.
-->

---

<div class="who tv4">TV4 · 14:50</div>

# Demo

<div class="cols-62">
<div>

![w:640](figures/demo_exercises_card.png)

<p class="note">Bên trái của giao diện là video + transcript chạy theo; bên phải là danh sách câu hỏi với badge chủ điểm.</p>

</div>
<div>

1. Tab **Exercises**: bấm Question 4 (*The movie was very…*) → video tua đến 15:05, lúc cô bắt đầu chữa
2. Badge *Participles* → **Lý thuyết (00:44)**: tua về đoạn giảng đầu giờ
3. Tab **Vocab**: lọc theo CEFR, nghe audio
4. Tab **Chat & GEC**: lỗi, câu sửa, giải thích tiếng Việt

<p class="note">Chạy: <code>python demo/prepare.py --lesson lessons/ece-toeic-starter-u4</code> rồi <code>cd demo && python -m RangeHTTPServer 8000</code>. Có video quay sẵn để dự phòng.</p>

</div>
</div>

<!--
TV4: (Demo trực tiếp khoảng 2 phút.) Question 4 "The movie was very…": bấm vào, video tua đến 15:05; badge Participles tua về 00:44. Sau đó vào tab Vocab và Chat & GEC.
-->

---

<div class="who tv4">TV4</div>

# Hạn chế và hướng phát triển

<div class="cols">
<div class="box">

### Hạn chế
- Chỉnh trên 1 giáo viên: video của kênh khác chỉ đúng **18%** (±10 s)
- Trích câu từ màn hình cần slide in sẵn số câu
- Nhãn chuẩn do AI gán, chưa được người kiểm tra hết
- Chat là dữ liệu mô phỏng
- Chưa đo WER; gợi ý từ màn hình chưa chứng minh được hiệu quả
- Ngưỡng liên kết chủ điểm chọn trên tập phát triển
- Phát hiện lỗi dựa trên luật, chỉ 6 mẫu

</div>
<div class="box">

### Hướng phát triển
- Nhận câu hỏi từ chữ viết tay / bảng cuộn và chỗ giáo viên đang khoanh trên màn hình
- Sửa 5 clip ASR → WER thật cho 3 cấu hình
- Thu bản ghi lớp thật: tương tác giữa giáo viên và học viên trong lớp thực tế
- Tập kiểm tra độc lập cho liên kết chủ điểm (Unit 5)
- Phát hiện lỗi bằng mô hình sửa câu (seq2seq / LLM) + errant để gán loại
- Mở rộng sang bài giảng IELTS

</div>
</div>

<!--
TV4: Nhóm nêu rõ các giới hạn. Lớn nhất là thuật toán được chỉnh trên một giáo viên: trên video kênh khác, kết quả giảm từ 80 xuống 18 phần trăm, chủ yếu vì bước trích câu từ màn hình. Việc tiếp theo là nhận câu hỏi từ chữ viết tay, sửa tay 5 clip để có WER thật, và thu bản ghi lớp học thật.
-->

---

<div class="who tv4">TV4</div>

# Kết luận

<div class="cols">
<div>

1. **Căn chỉnh câu hỏi ↔ lời giảng** với khẩu lệnh có xác minh ngữ cảnh: **80%** câu đúng trong ±10 s trên bài kiểm tra cùng nguồn (v1: 57%); trên video của 6 kênh khác chỉ **18%**, do bước trích câu từ màn hình
2. **Lời giảng làm tín hiệu liên kết chủ điểm** (e5 đa ngữ): **91,2%** trên 34 câu (v1: 58,8%), không dùng từ khóa viết tay
3. **Đánh giá tái lập được**: nhãn, script, baseline; số liệu chưa đo được ghi rõ là chưa đo

</div>
<div class="box">

### Tài liệu
- `docs/10_evaluation_results.md`: toàn bộ số liệu
- `eval/run_all.py`: tái tạo số liệu
- `demo/`: sổ tay học viên tương tác

<p class="big" style="margin-top:22px">Hỏi – đáp</p>

</div>
</div>

<!--
TV4: Ba đóng góp chính, mỗi đóng góp đi kèm số liệu đo được. Cảm ơn thầy/cô, nhóm em sẵn sàng trả lời câu hỏi.
-->
