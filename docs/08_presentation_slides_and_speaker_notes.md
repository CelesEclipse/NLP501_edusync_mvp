# KỊCH BẢN THUYẾT TRÌNH VÀ LỜI THOẠI TỪNG SLIDE (4 THÀNH VIÊN)
## EduSync: căn chỉnh đa phương thức và phân tích bài giảng luyện thi TOEIC (giảng Việt – Anh)

**Môn học:** NLP501  
**Slide:** [presentation/slides_marp.md](../presentation/slides_marp.md) (16 slide; lời thoại rút gọn nằm trong comment HTML của từng slide)  
**Thời lượng:** 20 phút trình bày + hỏi đáp  
**Nguồn số liệu:** [docs/10_evaluation_results.md](10_evaluation_results.md). Mọi con số trong lời thoại dưới đây đều có trên slide hoặc trong docs/10. Khi nói, không thêm con số nào khác.

---

## 1. Phân công và thời gian

| Thành viên | Nội dung | Slide | Thời lượng | Mốc |
| :--- | :--- | :---: | :---: | :---: |
| **TV1** | Đề tài, vấn đề, bài toán NLP và dữ liệu, kiến trúc, nghiên cứu liên quan | 1–5 | 4,5 phút | 00:00–04:30 |
| **TV2** | Nhận dạng tiếng nói trộn mã, căn chỉnh câu hỏi ↔ lời giảng, kết quả căn chỉnh, kết quả trên video của giáo viên khác | 6–9 | 5 phút 10 s | 04:30–09:40 |
| **TV3** | Liên kết chủ điểm, trích chủ điểm và từ vựng, phát hiện lỗi trong chat | 10–13 | 5 phút 10 s | 09:40–14:50 |
| **TV4** | Demo trực tiếp (khoảng 2 phút), hạn chế, kết luận | 14–16 | 4 phút 20 s | 14:50–19:10 |

| Slide | Tiêu đề | Người nói | Thời lượng | Mốc |
| :-: | :--- | :-: | :-: | :-: |
| 1 | EduSync (đề tài và phân công) | TV1 | 40 s | 00:00–00:40 |
| 2 | Vấn đề | TV1 | 60 s | 00:40–01:40 |
| 3 | Bài toán NLP và dữ liệu | TV1 | 60 s | 01:40–02:40 |
| 4 | Kiến trúc | TV1 | 65 s | 02:40–03:45 |
| 5 | Nghiên cứu liên quan | TV1 | 45 s | 03:45–04:30 |
| 6 | Nhận dạng lời giảng có cả Tiếng Việt - Anh | TV2 | 80 s | 04:30–05:50 |
| 7 | Căn chỉnh câu hỏi ↔ lời giảng | TV2 | 110 s | 05:50–07:40 |
| 8 | Kết quả căn chỉnh | TV2 | 60 s | 07:40–08:40 |
| 9 | Trên video của giáo viên khác | TV2 | 60 s | 08:40–09:40 |
| 10 | Liên kết câu hỏi ↔ chủ điểm ngữ pháp | TV3 | 85 s | 09:40–11:05 |
| 11 | Kết quả liên kết chủ điểm (Unit 4, 34 câu) | TV3 | 75 s | 11:05–12:20 |
| 12 | Trích xuất chủ điểm và từ vựng | TV3 | 75 s | 12:20–13:35 |
| 13 | Phát hiện lỗi người học trong chat | TV3 | 75 s | 13:35–14:50 |
| 14 | Demo | TV4 | 140 s | 14:50–17:10 |
| 15 | Hạn chế và hướng phát triển | TV4 | 60 s | 17:10–18:10 |
| 16 | Kết luận | TV4 | 60 s | 18:10–19:10 |

**Nguyên tắc khi nói**
- Đọc số đúng như trên slide (dấu phẩy thập phân: "tám phẩy một giây").
- Năm điều luôn nói rõ, không né: bản ghi **chỉ có một người nói**; chat của Unit 4 là **dữ liệu mô phỏng**; nhãn chuẩn là **bản nháp do AI gán**, nhóm đang kiểm tra lại với video; **chưa có WER**; 80% căn chỉnh là trên bài **cùng nguồn** với tập phát triển, trên video của giáo viên khác chỉ 18%.
- Không dùng lại các khẳng định đã rút (docs/10 §9; danh sách "không nói" ở [docs/09 phần 4](09_teacher_presentation_and_technical_nlp_guide.md)).
- Người nói sau đứng sẵn khi người trước đọc câu chuyển ý.

---

## 2. Lời thoại từng slide

### Phần 1 — TV1 (slide 1–5 · 4,5 phút · 00:00–04:30)

#### Slide 1 · EduSync
**Người nói:** TV1 · **Thời lượng:** 40 s (00:00–00:40)

> "Em chào thầy/cô và các bạn. Nhóm em xin trình bày đề tài EduSync: từ bản ghi một buổi luyện thi TOEIC mà cô giáo giảng xen kẽ tiếng Việt và tiếng Anh, hệ thống tạo ra sổ tay học tập tương tác cho học viên. Đầu vào gồm video quay màn hình, lời giảng có cả Tiếng Việt - Anh và log chat của lớp. Nhóm có bốn thành viên, mỗi người trình bày một phần như ở khung bên phải. Tất cả số liệu trong bài nằm trong file docs/10 và tái tạo được bằng một lệnh."

**Chuyển ý:** "Trước hết, em xin nói vì sao bài toán này đáng làm."

#### Slide 2 · Vấn đề
**Người nói:** TV1 · **Thời lượng:** 60 s (00:40–01:40)

> "Sau một buổi học trực tuyến, thứ còn lại thường chỉ là một video dài hàng giờ và một file chat. Học viên muốn xem lại đoạn cô chữa một câu thì phải tự tua; Guo và cộng sự năm 2014 ghi nhận thời gian xem trung vị của video bài giảng chỉ khoảng 6 phút, và Kim và cộng sự cùng năm thấy các đỉnh thao tác tua tập trung quanh chỗ chuyển cảnh. Nhiều bạn cũng ngại hỏi lại trước lớp vì sợ bị đánh giá tiêu cực, điều mà Horwitz và cộng sự đã mô tả từ năm 1986. Lỗi sai trong chat cũng trôi mất sau buổi học, thiếu phản hồi sửa lỗi kịp thời. Từ đó nhóm đặt bốn mục tiêu ở khung bên phải: tua theo câu hỏi, nối câu hỏi với chủ điểm, từ vựng theo CEFR, và phát hiện lỗi trong chat kèm giải thích tiếng Việt."

**Chuyển ý:** "Bốn mục tiêu này quy về bốn bài toán NLP, em trình bày ở slide sau."

**Nếu bị hỏi ngay trên slide này:** các nghiên cứu này là động lực, không phải kết quả của nhóm. Nhóm **chưa làm khảo sát người dùng**, nên không khẳng định EduSync giúp học viên học tốt hơn.

#### Slide 3 · Bài toán NLP và dữ liệu
**Người nói:** TV1 · **Thời lượng:** 60 s (01:40–02:40)

> "Bài toán thứ nhất là căn chỉnh đơn điệu: mỗi câu hỏi cần một mốc cô bắt đầu chữa, và các mốc phải tăng dần. Thứ hai là liên kết câu hỏi với chủ điểm ngữ pháp, hoặc 'không gắn'; thứ ba là từ vựng theo bậc CEFR; thứ tư là sáu mẫu lỗi chuyển di từ tiếng Việt trong chat. Cái khó là lời giảng có cả Tiếng Việt - Anh, 73% đoạn tiếng Việt và 26% tiếng Anh, OCR nhiễu, số câu đánh lại từ 1 ở mỗi phần, và câu hỏi thường không có từ chung với tên chủ điểm. Dữ liệu chính là bài TOEIC Starter của ECE, giấy phép CC BY: Unit 4, 34 câu, để phát triển; Unit 5, 35 câu, chỉ chạy một lần để kiểm tra độc lập. Vì hai bài này cùng một cô, nhóm thêm 8 video TOEIC tiếng Việt của 6 kênh khác, 68 câu, để kiểm tra tổng quát hóa; kết quả ở phần của TV2. Ba giới hạn: bản ghi chỉ có một người nói, chat của Unit 4 là dữ liệu mô phỏng, và nhãn chuẩn là bản nháp do AI gán, nhóm đang kiểm tra lại với video."

**Chuyển ý:** "Các bài toán này nối với nhau thế nào thì em trình bày ở sơ đồ kiến trúc."

**Nếu bị hỏi ngay trên slide này:** "34 câu nhưng nhãn mốc chỉ có 32?" — 2 trong 34 bản ghi trích từ OCR là đoạn văn, không phải câu hỏi (docs/10 §1–2).

#### Slide 4 · Kiến trúc
**Người nói:** TV1 · **Thời lượng:** 65 s (02:40–03:45)

> "Hệ thống có ba luồng vào: video màn hình, lời giảng có cả Tiếng Việt - Anh và log chat. Video được tách thành các màn hình và chạy OCR, rồi bóc ra câu hỏi với các lựa chọn A đến D; lời giảng đi qua Whisper và được gán nhãn tiếng Việt hay tiếng Anh; còn chat được ẩn danh tên thành S1 đến SN và trích ra đáp án học viên chọn. Điều em muốn thầy/cô chú ý là ba chỗ các luồng kết hợp với nhau, đánh số từ 1 đến 3. Số 1, chữ OCR trên màn hình làm gợi ý cho ASR, hiện mới là thử nghiệm; số 2, thời điểm màn hình cộng lời giảng dùng để căn chỉnh câu hỏi; số 3, lời cô giảng khi chữa một câu giúp xác định câu đó thuộc chủ điểm nào. Đầu ra cuối cùng là sổ tay học viên tương tác trên web demo."

**Chuyển ý:** "Trước khi vào chi tiết, em điểm qua các công trình liên quan."

#### Slide 5 · Nghiên cứu liên quan
**Người nói:** TV1 · **Thời lượng:** 45 s (03:45–04:30)

> "Gần nhất với nhóm là MaViLS của Anderer và cộng sự năm 2024, căn chỉnh video bài giảng với slide bằng ASR, OCR, đặc trưng hình ảnh và quy hoạch động. Khác biệt của nhóm là không có file slide gốc, và cần căn chỉnh tới từng câu hỏi trắc nghiệm chứ không phải từng slide. Về nhận dạng tiếng nói, nhóm dùng Whisper và tham khảo Peng và cộng sự về việc dùng prompt để điều khiển Whisper; về liên kết chủ điểm, nhóm dùng bi-encoder, cụ thể là E5 đa ngữ. Với lỗi người học, nhóm dùng ERRANT của Bryant, Felice và Briscoe ở ACL 2017 để gán loại lỗi, còn từ vựng tra theo CEFR-J và Octanove."

**Chuyển ý:** "Em xin mời TV2 trình bày phần nhận dạng tiếng nói và căn chỉnh câu hỏi."

---

### Phần 2 — TV2 (slide 6–9 · 5 phút 10 s · 04:30–09:40)

#### Slide 6 · Nhận dạng lời giảng có cả Tiếng Việt - Anh
**Người nói:** TV2 · **Thời lượng:** 80 s (04:30–05:50)

> "Em dùng faster-whisper bản large-v3-turbo ở chế độ đa ngữ, chạy trên máy cá nhân. Mỗi đoạn được gán nhãn ngôn ngữ theo mật độ chữ có dấu: trên 0,3 là tiếng Việt, bằng 0 là tiếng Anh, còn lại là trộn. Nhóm có thử một ý tưởng đa phương thức: lấy từ tiếng Anh trên màn hình đang chiếu, qua OCR, đưa vào tham số hotwords của Whisper. Em xin nói thẳng là nhóm chưa có WER, vì năm clip tham chiếu, tổng cộng 10 phút, vẫn là bản nháp chưa sửa tay. Thử nghiệm gợi ý có tác dụng hai chiều: Whisper nhận ra nhiều từ trên màn hình hơn, nhưng số đoạn lặp tăng, là dấu hiệu ảo giác. Vì vậy pipeline hiện vẫn dùng bản không gợi ý. Khi chưa có WER thì các chỉ số gián tiếp chưa kết luận được gì, nên nhóm không đưa số liệu ASR lên slide."

**Chuyển ý:** "Có lời giảng rồi, bài toán chính của em là tìm lúc cô bắt đầu chữa từng câu."

**Nếu bị hỏi ngay trên slide này:** "Proxy đo gì?" — tỉ lệ từ tiếng Anh có trên một màn hình mà transcript ghi là cô nói trong lúc màn hình đó hiện; gợi ý làm proxy tăng một phần chỉ vì Whisper chép lại từ gợi ý, nên không thay được WER. Nếu được hỏi số cụ thể: chỉ số gián tiếp nằm ở `docs/10_evaluation_results.md` mục 7. "hotwords khác initial_prompt?" — `initial_prompt` ở đây là prompt cố định của bài (lesson.json); `hotwords` thay đổi theo từng màn hình. Cả hai đều là token văn bản đặt trước phần giải mã trong ngữ cảnh của decoder.

#### Slide 7 · Căn chỉnh câu hỏi ↔ lời giảng
**Người nói:** TV2 · **Thời lượng:** 110 s (05:50–07:40)

> "Mỗi cặp câu hỏi k và đoạn lời giảng j có một điểm: 25 điểm nếu đoạn đó có khẩu lệnh như 'câu số N' hay 'câu thứ tư', cộng 2 điểm cho mỗi từ chung với câu hỏi, cộng 3 điểm nếu màn hình của câu đó đang chiếu. Regex loại các trường hợp 'text', 'page', 'part' hay 'trang N', vì đó không phải số câu. Thay đổi quan trọng nhất là xác minh khẩu lệnh: 'câu N' chỉ được đủ 25 điểm nếu trong 60 giây sau đó cô nói ít nhất một từ của chính câu hỏi, nếu không thì chỉ được 2 điểm. Khung bên phải là tình huống thật ở Unit 4: màn hình chiếu Exercise B nhưng cô chữa Exercise A trong sách trước và nói 'câu số 1' ở 03:09; bản cũ gán câu B1 vào đây và lệch 216 giây, còn bản mới thấy khẩu lệnh không được xác minh nên bỏ qua nó và chọn 07:05, nằm trong đoạn cô chữa câu B1, chỉ trễ 21 giây so với nhãn. Bộ giải mã là quy hoạch động đơn điệu theo công thức D[k][j], tối ưu toàn cục và cho phép bỏ qua câu; sau đó mốc được lùi về các đoạn ngay trước có chung từ với câu hỏi, vì cô thường đọc đề trước rồi mới nói số câu."

**Chuyển ý:** "Em chuyển sang kết quả đo trên bài kiểm tra độc lập."

**Nếu bị hỏi ngay trên slide này:** "Câu không tìm được khẩu lệnh thì sao?" — câu không khớp lấy thời điểm màn hình xuất hiện nhưng bị kẹp giữa hai câu kề nhau, nên không đảo thứ tự. "Các trọng số 25/2/3 lấy đâu ra?" — chỉnh tay trên Unit 4 (dev), giữ nguyên khi chạy Unit 5.

#### Slide 8 · Kết quả căn chỉnh
**Người nói:** TV2 · **Thời lượng:** 60 s (07:40–08:40)

> "Thuật toán được chỉnh trên Unit 4, rồi chỉ chạy một lần trên Unit 5. Trên Unit 5, tỉ lệ câu có mốc lệch không quá 10 giây tăng từ 57 lên 80 phần trăm so với bản cũ, sai số trung bình giảm từ 28,5 xuống 8,1 giây, và không còn câu nào bị đảo thứ tự; chỉ lấy thời điểm màn hình xuất hiện thì đạt 49 phần trăm. Em nói rõ: trên cả hai bài, DP chọn giống hệt greedy, nên phần cải thiện đến từ cách tính điểm, bước lùi mốc và cách xử lý câu không khớp. Lỗi còn lại chủ yếu ở chỗ trống trong đoạn văn Part 6 và Part 7, nơi cô đọc liền cả đoạn. Nhưng Unit 4 và Unit 5 cùng một cô, cùng một cuốn sách, nên 80 phần trăm chỉ cho biết hệ thống chạy tốt trên bài cùng nguồn."

**Chuyển ý:** "Slide sau là phép thử khó hơn: video của giáo viên khác."

**Nếu bị hỏi ngay trên slide này:** "Trên Unit 4, regex lấy 'câu N' đầu tiên đạt 71,9% ở ±10 s, cao hơn bản hiện tại (68,8%)?" — đúng, nhóm báo cáo nguyên văn; nhưng regex kém hơn ở ±30 s, sai số trung bình 28,1 s so với 10,0 s, và trên Unit 5 chỉ đạt 71,4% với 2 lần đảo thứ tự. "Nhãn ai gán?" — xem docs/09, Q1.

#### Slide 9 · Trên video của giáo viên khác
**Người nói:** TV2 · **Thời lượng:** 60 s (08:40–09:40)

**Trên slide:**
- Phụ đề: 8 video TOEIC tiếng Việt, 6 kênh YouTube (CC BY), 68 câu có nhãn; không chỉnh thuật toán theo bộ này.
- Bên trái: biểu đồ `figures/multisource_alignment.png` trên 6 video bài giảng (45 câu); "đóng băng" là hệ thống trước khi xem bộ này, "sau sửa" là khi `exercises.py` nhận số câu 3 chữ số (TOEIC 101–200), không còn là kiểm tra độc lập.
- Kết quả: đầu-cuối 18% đúng ±10 s (U5 cùng nguồn: 80%), nên 80% không phải độ chính xác chung; cho trước danh sách câu đúng, DP 58%, gấp đôi greedy và regex (24%).
- Vì sao sai: bước trích câu từ màn hình chỉ hợp slide in sẵn "N." nên hỏng với bảng viết tay, bảng cuộn, câu chỉ có tranh/audio (tìm được 44% số câu); giáo viên nói "câu này" thay vì "câu 116", hoặc đọc câu hỏi tiếng Anh trước khi màn hình của câu hiện ra.

> "Ngoài YouTube, nhóm không tìm được video bài giảng TOEIC tiếng Việt nào vừa có giấy phép mở vừa tải được, nên bộ test gồm 8 video của 6 kênh YouTube, giấy phép CC BY, 68 câu có nhãn. Hệ thống được đóng băng trước khi xem bộ này. Trên 6 video bài giảng, nó chỉ đúng 18 phần trăm trong 10 giây, so với 80 phần trăm trên Unit 5; vì vậy 80 phần trăm không phải độ chính xác chung. Khi cho trước danh sách câu đúng, DP đúng 58 phần trăm, gấp đôi greedy và regex. Như vậy lỗi chính nằm ở bước trích câu từ màn hình: bước này giả định đề in sẵn có số câu, nên hỏng với bảng viết tay, bảng cuộn hay câu chỉ có tranh, và chỉ tìm được 44 phần trăm số câu. Giáo viên cũng hay nói 'câu này' thay vì đọc số. Ngược lại, DP thực sự có ích khi dữ liệu lạ."

**Chuyển ý:** "Em xin mời TV3 trình bày phần liên kết câu hỏi với chủ điểm ngữ pháp."

**Nếu bị hỏi ngay trên slide này:** "Sửa `exercises.py` rồi thì được bao nhiêu?" — trên bài giảng, trích câu 44,4% → 55,6%, đầu-cuối 17,8% → 26,7%; nhưng lỗi được tìm ra nhờ chính bộ này nên số sau khi sửa không còn là kiểm tra độc lập, số độc lập là 17,8%. Không chỉnh trọng số hay cửa sổ căn chỉnh theo bộ này; `exercises.json` của U4/U5 không đổi. "Nhãn gán thế nào?" — là danh sách câu giáo viên thực sự chữa và mốc bắt đầu, do AI gán từ transcript, OCR và khung hình video, không mở output hệ thống, `verified: false`; vì vậy đếm được cả câu hệ thống bỏ sót. "Hai video luyện tập?" — chỉ phát audio đề, không có lời giảng: đầu-cuối 8,7%, cho trước danh sách câu đúng 78,3%. Chi tiết: docs/10 §3b, docs/09 Q13.

---

### Phần 3 — TV3 (slide 10–13 · 5 phút 10 s · 09:40–14:50)

#### Slide 10 · Liên kết câu hỏi ↔ chủ điểm ngữ pháp
**Người nói:** TV3 · **Thời lượng:** 85 s (09:40–11:05)

> "Câu 'The movie was very ___' với các lựa chọn move, moving, moved thuộc chủ điểm 'Participles as Adjectives', nhưng hai bên không có từ nào chung. Bản cũ dùng all-MiniLM-L6-v2, một mô hình chỉ hiểu tiếng Anh, trong khi phần giải thích chủ điểm viết bằng tiếng Việt; để bù, bản cũ ghép thêm từ khóa viết tay, mà trong đó có cả từ đáp án như central, luxury, shined, tức là rò rỉ nhãn. Khi bỏ bộ từ khóa đó, độ chính xác tụt từ 76,5 xuống 61,8 phần trăm. Bản hiện tại dùng multilingual-e5-small, và điểm của một cặp câu hỏi – chủ điểm là trung bình của hai cosine: giữa câu hỏi với chủ điểm, và giữa lời cô giảng trong lúc chữa câu đó với chủ điểm. Lời giảng chính là điểm kết hợp số 3: khi chữa, cô nói những câu như 'chọn động từ thêm ing hay thêm ed để làm tính từ', hay 'công thức nhờ vả'. Nếu điểm cao nhất đạt từ 0,835 trở lên thì gắn chủ điểm, ngược lại không gắn, vì nhiều câu chỉ là câu từ vựng hoặc đọc hiểu."

**Chuyển ý:** "Kết quả của cách làm này ở slide tiếp theo."

**Nếu bị hỏi ngay trên slide này:** "Lời giảng lấy đoạn nào?" — từ mốc bắt đầu chữa câu đó (lấy từ kết quả căn chỉnh) đến mốc của câu kế tiếp, có giới hạn độ dài (`SPEECH_MAX_S` trong `concept_link.py`). Không có mô hình thì dùng TF-IDF trên câu hỏi + lời giảng.

#### Slide 11 · Kết quả liên kết chủ điểm (Unit 4, 34 câu)
**Người nói:** TV3 · **Thời lượng:** 75 s (11:05–12:20)

> "Trước hết cần so với một mốc đơn giản: 22 trên 34 câu là câu từ vựng hoặc đọc hiểu, nên cách 'luôn không gắn' đã đạt 73,5 phần trăm, và bản cũ chỉ hơn mốc này 3 điểm. Biểu đồ bên trái so sánh các phương pháp; bản hiện tại, e5 đa ngữ cộng lời giảng, đạt 91,2 phần trăm. Bảng bên phải là đầu ra thực tế trong demo: độ chính xác tăng từ 58,8 lên 91,2 phần trăm, và trong demo cũ khoảng 61 phần trăm badge gắn sai, còn bản mới chỉ 1 trên 10 badge sai. Đổi lại, recall, tức tỉ lệ câu có chủ điểm được gắn đúng, là 75 phần trăm, nghĩa là vẫn có câu bị bỏ sót. Hạn chế lớn nhất em phải nói rõ: mô hình và ngưỡng được chọn trên chính 34 câu này, nên con số có thể lạc quan, và chưa có tập kiểm tra độc lập cho bài toán này."

**Chuyển ý:** "Ngoài liên kết câu hỏi, hệ thống còn trích chủ điểm và từ vựng từ bài giảng."

**Nếu bị hỏi ngay trên slide này:** "Ngưỡng 0,835 có overfit không?" — có nguy cơ; trong biểu đồ, ngưỡng được chọn leave-one-out (mỗi câu chấm bằng ngưỡng tối ưu trên 33 câu còn lại), nhưng việc chọn mô hình thì làm trên cùng 34 câu; điểm hai nhóm sát nhau (0,81–0,86) nên sang bài mới phải hiệu chỉnh lại (docs/09, Q7).

#### Slide 12 · Trích xuất chủ điểm và từ vựng
**Người nói:** TV3 · **Thời lượng:** 75 s (12:20–13:35)

> "Bốn chủ điểm ngữ pháp được Gemini trích ra ở chế độ JSON, gồm tiêu đề, công thức và lời giải thích; nhưng Gemini chỉ thấy khoảng 30 đoạn lời giảng lấy mẫu, nên mốc thời gian nó trả về thực chất là đoán. Ví dụ phần bị động cô giảng ở 13:16, Gemini lại trả về 55:02, lệch gần 42 phút. Nhóm neo lại mỗi chủ điểm vào cửa sổ lời giảng giống nó nhất theo e5, nhờ đó sai số trung bình giảm từ 882,5 giây xuống 11,2 giây; khi không có mạng thì dùng bảng chủ điểm TOEIC và tìm từ khóa trong lời giảng. Về từ vựng, vocab.py lemma hóa hai lớp, tra từ điển CEFR-J và Octanove 8.845 mục, lọc những từ trùng mặt chữ Việt – Anh như 'hay', 'con', và lấy nghĩa tiếng Việt theo mẫu 'X là, nghĩa là' trong lời giảng. Unit 4 có 80 từ, 52 từ có nghĩa tiếng Việt và 79 clip audio giọng cô; em lưu ý là độ đúng của nghĩa và audio chưa được đánh giá."

**Chuyển ý:** "Phần cuối của em là phát hiện lỗi người học trong chat."

**Nếu bị hỏi ngay trên slide này:** "JSON mode có phải structured output với schema chặt không?" — không; chỉ đặt `responseMimeType=application/json` rồi kiểm tra các trường sau khi parse. "Clip audio cắt thế nào?" — theo ranh giới đoạn ASR có chứa từ (ưu tiên đoạn chỉ có một từ), vì transcript không có timestamp từng từ. "Lọc trùng mặt chữ làm thế nào?" — `hay`, `con`, `cho`, `ra`, `nam`, `sau`… nằm trong danh sách cố định `VI_HOMOPHONES` (41 âm tiết), còn `an`, `can` bị loại qua danh sách stopword tiếng Anh. Bộ lọc không xét ngữ cảnh, và `may` hiện **chưa** được lọc.

#### Slide 13 · Phát hiện lỗi người học trong chat
**Người nói:** TV3 · **Thời lượng:** 75 s (13:35–14:50)

> "Module feedback.py dùng luật cho sáu mẫu lỗi chuyển di từ tiếng Việt: thừa 'be' như 'I am agree', nhầm đuôi -ing và -ed, cấu trúc nhờ vả, 'should to', hòa hợp chủ vị, và thiếu trợ động từ 'do' trong câu hỏi. Mỗi lỗi kèm câu sửa, giải thích tiếng Việt và một loại lỗi ERRANT; các loại trong bảng đã được kiểm chứng bằng thư viện errant 3.0.2 chính thức, ví dụ 'should to increase' là U:VERB:FORM. Bản cũ khớp nguyên văn từng câu chat, nên tỉ lệ 6 trên 6 trước đây không có ý nghĩa. Bản mới được đo trên 70 câu viết độc lập, không xem luật: precision 100 phần trăm, recall 72,7 phần trăm, F1 84,2. Đây không phải mô hình GEC tổng quát, lỗi ngoài sáu nhóm sẽ bị bỏ qua, và trước khi chốt nhóm đã xem tập 70 câu một lần để sửa 3 lỗi cài đặt."

**Chuyển ý:** "Em xin mời TV4 trình bày phần demo hệ thống."

**Nếu bị hỏi ngay trên slide này:** "'I am confusing → confused' sao lại R:VERB:FORM?" — R:VERB:FORM là nhãn mặc định của nhóm -ing/-ed (lấy từ cặp "The movie was moved → moving"); với riêng cặp "confusing → confused", errant 3.0.2 cho R:MORPH. Nếu máy có cài `errant`, `feedback.py` để errant tự gán nhãn từng lỗi. "Precision 100% có đáng tin?" — tập chỉ 70 câu, nhãn cũng là bản nháp; nhưng 10 câu có lỗi ngoài phạm vi không bị báo nhầm câu nào.

---

### Phần 4 — TV4 (slide 14–16 · 4 phút 20 s · 14:50–19:10)

#### Slide 14 · Demo
**Người nói:** TV4 · **Thời lượng:** 140 s (14:50–17:10), phần lớn là demo trực tiếp

*(Chuyển sang trình duyệt đã mở sẵn sổ tay Unit 4.)*

> "Đây là sổ tay học viên của Unit 4: bên trái là video với transcript chạy theo, bên phải là danh sách câu hỏi kèm badge chủ điểm. Em bấm thẻ Question 4, câu 'The movie was very…', video tua đến 15:05, lúc cô nói 'Câu số 4'; câu này có badge Participles as Adjectives, em bấm 'Lý thuyết' thì video tua về 00:44, đoạn cô giảng phân từ ở đầu giờ. Sang tab Vocab, em lọc theo bậc CEFR và bấm nghe audio giọng cô đọc từ. Ở tab Chat & GEC, mỗi tin nhắn có lỗi hiện phần sai, câu sửa và lời giải thích tiếng Việt, tên học viên đã được ẩn danh thành S1, S2."

**Chuyển ý:** "Từ các kết quả trên, nhóm tự nêu các hạn chế và hướng phát triển."

**Chuẩn bị:** chạy `python demo/prepare.py --lesson lessons/ece-toeic-starter-u4` rồi `cd demo && python -m RangeHTTPServer 8000` trước giờ trình bày; mở sẵn video quay dự phòng. Nếu demo lỗi, chuyển ngay sang video dự phòng, không sửa trực tiếp trước hội đồng. Chỉ thao tác những gì có trên slide. Có 4 thẻ "Question 4": chọn thẻ có đề *movie*. Không lấy làm ví dụ: Question 1 đầu bài (mốc lệch 21 s), Question 5 *shoes* (không khớp được lời giảng) và Question 13 (badge gắn sai).

#### Slide 15 · Hạn chế và hướng phát triển
**Người nói:** TV4 · **Thời lượng:** 60 s (17:10–18:10)

> "Hạn chế lớn nhất là thuật toán được chỉnh trên một giáo viên: trên video của kênh khác, tỉ lệ đúng trong 10 giây giảm từ 80 xuống 18 phần trăm, chủ yếu vì bước trích câu từ màn hình cần slide in sẵn số câu. Ngoài ra, nhãn chuẩn chưa kiểm tra hết, chat là dữ liệu mô phỏng, chưa đo WER, ngưỡng liên kết chủ điểm chọn trên tập phát triển, và phát hiện lỗi chỉ dùng luật cho sáu mẫu. Việc tiếp theo: nhận câu hỏi từ chữ viết tay, bảng cuộn và chỗ giáo viên khoanh trên màn hình; sửa tay năm clip để có WER; thu bản ghi lớp thật có tương tác thực tế giữa giáo viên và học viên. Xa hơn là tập kiểm tra cho liên kết chủ điểm, mô hình sửa câu kèm errant, và IELTS."

**Chuyển ý:** "Em xin tóm tắt lại."

#### Slide 16 · Kết luận
**Người nói:** TV4 · **Thời lượng:** 60 s (18:10–19:10)

> "Nhóm có ba đóng góp, mỗi đóng góp có số đo. Một là căn chỉnh câu hỏi với lời giảng, có xác minh khẩu lệnh theo ngữ cảnh: 80 phần trăm câu đúng trong 10 giây trên bài kiểm tra cùng nguồn, so với 57 phần trăm của bản cũ; trên video của 6 kênh khác chỉ 18 phần trăm, do bước trích câu từ màn hình. Hai là dùng lời giảng làm tín hiệu liên kết chủ điểm với e5 đa ngữ: 91,2 phần trăm trên 34 câu, so với 58,8 phần trăm, không cần từ khóa viết tay. Ba là đánh giá tái lập được; cái gì chưa đo thì ghi là chưa đo. Sản phẩm hoàn chỉnh là sổ tay học viên tương tác trong thư mục demo/. Em cảm ơn thầy/cô và các bạn đã lắng nghe, nhóm em xin sẵn sàng trả lời câu hỏi."

---

## 3. Phân công trả lời hỏi đáp

Câu trả lời chi tiết ở [docs/09, phần 3](09_teacher_presentation_and_technical_nlp_guide.md). Người trả lời chính nói trước; người khác chỉ bổ sung khi được mời.

| Chủ đề câu hỏi | Trả lời chính | Câu trong docs/09 |
| :--- | :-: | :-: |
| Cách đo 80%, ai gán nhãn; regex "câu N" so với bản hiện tại; DP và greedy | TV2 | Q1–Q3 |
| WER, gợi ý từ màn hình; lỗi lan truyền từ ASR/OCR | TV2 | Q4–Q5 |
| Video của giáo viên khác (bộ test đa nguồn) | TV2 | Q13 |
| Embedding so với TF-IDF/BM25; ngưỡng 0,835; ERRANT | TV3 | Q6–Q8 |
| Chat thật hay giả, ẩn danh hoá | TV1 | Q9 |
| Tại sao không dùng LLM cho tất cả | TV1 | Q10 |
| Mở rộng sang IELTS | TV4 | Q12 |

## 4. Chuẩn bị trước buổi bảo vệ
- Kiểm tra nhãn gold theo docs/10 §2, đặt `verified: true`, chạy lại `python eval/run_all.py`. Nếu số thay đổi: sửa docs/10 trước, rồi slide và tài liệu này.
- Tập nói có bấm giờ theo bảng ở mục 1; phần demo không quá 2 phút.
- Mở sẵn: trình duyệt với demo Unit 4, video dự phòng, docs/10 (để tra số khi bị hỏi).
