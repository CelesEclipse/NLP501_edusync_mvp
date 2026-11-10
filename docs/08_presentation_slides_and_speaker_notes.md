# KỊCH BẢN THUYẾT TRÌNH VÀ LỜI THOẠI TỪNG SLIDE (4 THÀNH VIÊN)
## EduSync: căn chỉnh đa phương thức và phân tích bài giảng luyện thi TOEIC (giảng Việt – Anh)

**Môn học:** NLP501  
**Slide:** [presentation/slides_marp.md](../presentation/slides_marp.md) (17 slide; lời thoại rút gọn nằm trong comment HTML của từng slide)  
**Thời lượng:** 20 phút trình bày + hỏi đáp  
**Nguồn số liệu:** [docs/10_evaluation_results.md](10_evaluation_results.md). Mọi con số trong lời thoại dưới đây đều có trên slide hoặc trong docs/10. Khi nói, không thêm con số nào khác.

---

## 1. Phân công và thời gian

| Thành viên | Nội dung | Slide | Thời lượng | Mốc |
| :--- | :--- | :---: | :---: | :---: |
| **TV1** | Đề tài, vấn đề, bài toán NLP và dữ liệu, kiến trúc, nghiên cứu liên quan | 1–5 | 4,5 phút | 00:00–04:30 |
| **TV2** | Nhận dạng tiếng nói trộn mã, căn chỉnh câu hỏi ↔ lời giảng, kết quả căn chỉnh | 6–8 | 4,5 phút | 04:30–09:00 |
| **TV3** | Liên kết chủ điểm, trích chủ điểm và từ vựng, phát hiện lỗi trong chat | 9–12 | 5,5 phút | 09:00–14:30 |
| **TV4** | Báo cáo giáo viên, demo trực tiếp (khoảng 2 phút), đánh giá, hạn chế, kết luận | 13–17 | 5,5 phút | 14:30–20:00 |

| Slide | Tiêu đề | Người nói | Thời lượng | Mốc |
| :-: | :--- | :-: | :-: | :-: |
| 1 | EduSync (đề tài và phân công) | TV1 | 40 s | 00:00–00:40 |
| 2 | Vấn đề | TV1 | 60 s | 00:40–01:40 |
| 3 | Bài toán NLP và dữ liệu | TV1 | 60 s | 01:40–02:40 |
| 4 | Kiến trúc | TV1 | 65 s | 02:40–03:45 |
| 5 | Nghiên cứu liên quan | TV1 | 45 s | 03:45–04:30 |
| 6 | Nhận dạng lời giảng trộn mã Việt – Anh | TV2 | 80 s | 04:30–05:50 |
| 7 | Căn chỉnh câu hỏi ↔ lời giảng | TV2 | 110 s | 05:50–07:40 |
| 8 | Kết quả căn chỉnh | TV2 | 80 s | 07:40–09:00 |
| 9 | Liên kết câu hỏi ↔ chủ điểm ngữ pháp | TV3 | 90 s | 09:00–10:30 |
| 10 | Kết quả liên kết chủ điểm (Unit 4, 34 câu) | TV3 | 80 s | 10:30–11:50 |
| 11 | Trích xuất chủ điểm và từ vựng | TV3 | 80 s | 11:50–13:10 |
| 12 | Phát hiện lỗi người học trong chat | TV3 | 80 s | 13:10–14:30 |
| 13 | Báo cáo cho giáo viên | TV4 | 60 s | 14:30–15:30 |
| 14 | Demo | TV4 | 120 s | 15:30–17:30 |
| 15 | Đánh giá tái lập được | TV4 | 55 s | 17:30–18:25 |
| 16 | Hạn chế và hướng phát triển | TV4 | 50 s | 18:25–19:15 |
| 17 | Kết luận | TV4 | 45 s | 19:15–20:00 |

**Nguyên tắc khi nói**
- Đọc số đúng như trên slide (dấu phẩy thập phân: "tám phẩy một giây").
- Bốn điều luôn nói rõ, không né: bản ghi **chỉ có một người nói**; chat của Unit 4 là **dữ liệu mô phỏng**; nhãn chuẩn là **bản nháp do AI gán**, nhóm đang kiểm tra lại với video; **chưa có WER**.
- Không dùng lại các khẳng định đã rút (docs/10 §9; danh sách "không nói" ở [docs/09 phần 4](09_teacher_presentation_and_technical_nlp_guide.md)).
- Người nói sau đứng sẵn khi người trước đọc câu chuyển ý.

---

## 2. Lời thoại từng slide

### Phần 1 — TV1 (slide 1–5 · 4,5 phút · 00:00–04:30)

#### Slide 1 · EduSync
**Người nói:** TV1 · **Thời lượng:** 40 s (00:00–00:40)

> "Em chào thầy/cô và các bạn. Nhóm em xin trình bày đề tài EduSync: từ bản ghi một buổi luyện thi TOEIC mà cô giáo giảng xen kẽ tiếng Việt và tiếng Anh, hệ thống tạo ra sổ tay cho học viên và báo cáo cho giáo viên. Đầu vào gồm video quay màn hình, lời giảng trộn mã Việt – Anh và log chat của lớp. Nhóm có bốn thành viên, mỗi người trình bày một phần như ở khung bên phải. Tất cả số liệu trong bài nằm trong file docs/10 và tái tạo được bằng một lệnh."

**Chuyển ý:** "Trước hết, em xin nói vì sao bài toán này đáng làm."

#### Slide 2 · Vấn đề
**Người nói:** TV1 · **Thời lượng:** 60 s (00:40–01:40)

> "Sau một buổi học trực tuyến, thứ còn lại thường chỉ là một video khoảng 60 phút và một file chat. Học viên muốn xem lại đoạn cô chữa một câu thì phải tự tua; Guo và cộng sự năm 2014 ghi nhận thời gian xem trung vị của video bài giảng chỉ khoảng 6 phút, và Kim và cộng sự cùng năm thấy các đỉnh thao tác tua tập trung quanh chỗ chuyển cảnh. Nhiều bạn cũng ngại hỏi lại trước lớp vì sợ bị đánh giá tiêu cực, điều mà Horwitz và cộng sự đã mô tả từ năm 1986. Về phía giáo viên, cô không biết lớp đang sai nhiều ở chủ điểm nào, vì lỗi trong chat trôi mất sau buổi học. Từ đó nhóm đặt năm mục tiêu ở khung bên phải: tua theo câu hỏi, nối câu hỏi với chủ điểm, từ vựng theo CEFR, phát hiện lỗi trong chat, và báo cáo cho giáo viên."

**Chuyển ý:** "Năm mục tiêu này quy về bốn bài toán NLP, em trình bày ở slide sau."

**Nếu bị hỏi ngay trên slide này:** các nghiên cứu này là động lực, không phải kết quả của nhóm. Nhóm **chưa làm khảo sát người dùng**, nên không khẳng định EduSync giúp học viên học tốt hơn.

#### Slide 3 · Bài toán NLP và dữ liệu
**Người nói:** TV1 · **Thời lượng:** 60 s (01:40–02:40)

> "Bài toán thứ nhất là căn chỉnh đơn điệu: mỗi câu hỏi cần một thời điểm cô bắt đầu chữa, và các thời điểm này phải tăng dần. Thứ hai là liên kết câu hỏi với một chủ điểm ngữ pháp, hoặc 'không thuộc chủ điểm nào'; thứ ba là từ vựng theo bậc CEFR; thứ tư là phát hiện sáu mẫu lỗi chuyển di từ tiếng Việt trong chat. Cái khó là lời giảng trộn mã, 73% đoạn tiếng Việt và 26% tiếng Anh, OCR nhiễu, số câu đánh lại từ 1 ở mỗi phần, và câu hỏi thường không có từ nào chung với tên chủ điểm. Dữ liệu là các bài TOEIC Starter của ECE, giấy phép CC BY: Unit 4 dài 58 phút với 34 câu dùng để phát triển, còn Unit 5 với 35 câu chỉ chạy một lần để kiểm tra độc lập. Em xin nói rõ ba giới hạn: bản ghi chỉ có một người nói, 17 tin nhắn chat của Unit 4 là dữ liệu nhóm mô phỏng, và nhãn chuẩn là bản nháp do AI gán, nhóm đang kiểm tra lại với video."

**Chuyển ý:** "Các bài toán này nối với nhau thế nào thì em trình bày ở sơ đồ kiến trúc."

**Nếu bị hỏi ngay trên slide này:** "34 câu nhưng nhãn mốc chỉ có 32?" — 2 trong 34 bản ghi trích từ OCR là đoạn văn, không phải câu hỏi (docs/10 §1–2). "CS224N dùng làm gì?" — chỉ để kiểm tra hồi quy pipeline v1 căn chỉnh slide.

#### Slide 4 · Kiến trúc
**Người nói:** TV1 · **Thời lượng:** 65 s (02:40–03:45)

> "Hệ thống có ba luồng vào: video màn hình, lời giảng Việt – Anh và log chat. Video được tách thành các màn hình và chạy OCR, rồi bóc ra câu hỏi với các lựa chọn A đến D; lời giảng đi qua Whisper và được gán nhãn tiếng Việt hay tiếng Anh; còn chat được ẩn danh tên thành S1 đến SN và trích ra đáp án học viên chọn. Điều em muốn thầy/cô chú ý là bốn chỗ các luồng kết hợp với nhau, đánh số từ 1 đến 4. Số 1, chữ OCR trên màn hình làm gợi ý cho ASR, hiện mới là thử nghiệm; số 2, thời điểm màn hình cộng lời giảng dùng để căn chỉnh câu hỏi; số 3, lời cô giảng khi chữa một câu giúp xác định câu đó thuộc chủ điểm nào; số 4, lỗi trong chat đi qua câu hỏi để tìm ra chủ điểm yếu trong báo cáo. Đầu ra cuối cùng là sổ tay học viên trên web demo và báo cáo cho giáo viên."

**Chuyển ý:** "Trước khi vào chi tiết, em điểm qua các công trình liên quan."

**Nếu bị hỏi ngay trên slide này:** "Bài chỉ có một người nói thì phân vai người nói để làm gì?" — `diarize.py` hỗ trợ ghi âm tách kênh từng người (Zoom) hoặc pyannote; với bài ECE nó rơi về chế độ một người nói, nên báo cáo ghi TTT/STT "chưa đo".

#### Slide 5 · Nghiên cứu liên quan
**Người nói:** TV1 · **Thời lượng:** 45 s (03:45–04:30)

> "Gần nhất với nhóm là MaViLS của Anderer và cộng sự năm 2024, căn chỉnh video bài giảng với slide bằng ASR, OCR, đặc trưng hình ảnh và quy hoạch động. Khác biệt của nhóm là không có file slide gốc, và cần căn chỉnh tới từng câu hỏi trắc nghiệm chứ không phải từng slide. Về nhận dạng tiếng nói, nhóm dùng Whisper và tham khảo Peng và cộng sự về việc dùng prompt để điều khiển Whisper; về liên kết chủ điểm, nhóm dùng bi-encoder, cụ thể là E5 đa ngữ. Với lỗi người học, nhóm dùng ERRANT của Bryant, Felice và Briscoe ở ACL 2017 để gán loại lỗi, còn từ vựng tra theo CEFR-J và Octanove."

**Chuyển ý:** "Em xin mời TV2 trình bày phần nhận dạng tiếng nói và căn chỉnh câu hỏi."

---

### Phần 2 — TV2 (slide 6–8 · 4,5 phút · 04:30–09:00)

#### Slide 6 · Nhận dạng lời giảng trộn mã Việt – Anh
**Người nói:** TV2 · **Thời lượng:** 80 s (04:30–05:50)

> "Em dùng faster-whisper bản large-v3-turbo ở chế độ đa ngữ, chạy trên máy cá nhân. Mỗi đoạn được gán nhãn ngôn ngữ theo mật độ chữ có dấu: trên 0,3 là tiếng Việt, bằng 0 là tiếng Anh, còn lại là trộn. Nhóm có thử một ý tưởng đa phương thức: lấy từ tiếng Anh trên màn hình đang chiếu, qua OCR, đưa vào tham số hotwords của Whisper. Em xin nói thẳng là nhóm chưa có WER, vì năm clip tham chiếu, tổng cộng 10 phút, vẫn là bản nháp chưa sửa tay. Chỉ số gián tiếp ở bảng bên phải cho thấy gợi ý có tác dụng hai chiều: tỉ lệ từ trên màn hình được nói ra tăng từ 48 lên 52 phần trăm so với đối chứng, nhưng số đoạn lặp tăng từ 3 lên 20 đến 27, là dấu hiệu ảo giác. Vì vậy pipeline hiện vẫn dùng bản không gợi ý."

**Chuyển ý:** "Có lời giảng rồi, bài toán chính của em là tìm lúc cô bắt đầu chữa từng câu."

**Nếu bị hỏi ngay trên slide này:** "Proxy đo gì?" — tỉ lệ từ tiếng Anh có trên một màn hình mà transcript ghi là cô nói trong lúc màn hình đó hiện; gợi ý làm proxy tăng một phần chỉ vì Whisper chép lại từ gợi ý, nên không thay được WER. "hotwords khác initial_prompt?" — `initial_prompt` ở đây là prompt cố định của bài (lesson.json); `hotwords` thay đổi theo từng màn hình. Cả hai đều là token văn bản đặt trước phần giải mã trong ngữ cảnh của decoder.

#### Slide 7 · Căn chỉnh câu hỏi ↔ lời giảng
**Người nói:** TV2 · **Thời lượng:** 110 s (05:50–07:40)

> "Mỗi cặp câu hỏi k và đoạn lời giảng j có một điểm: 25 điểm nếu đoạn đó có khẩu lệnh như 'câu số N' hay 'câu thứ tư', cộng 2 điểm cho mỗi từ chung với câu hỏi, cộng 3 điểm nếu màn hình của câu đó đang chiếu. Regex loại các trường hợp 'text', 'page', 'part' hay 'trang N', vì đó không phải số câu. Thay đổi quan trọng nhất là xác minh khẩu lệnh: 'câu N' chỉ được đủ 25 điểm nếu trong 60 giây sau đó cô nói ít nhất một từ của chính câu hỏi, nếu không thì chỉ được 2 điểm. Khung bên phải là tình huống thật ở Unit 4: màn hình chiếu Exercise B nhưng cô chữa Exercise A trong sách trước và nói 'câu số 1' ở 03:09; bản cũ gán câu B1 vào đây và lệch 216 giây, còn bản mới thấy khẩu lệnh không được xác minh nên bỏ qua nó và chọn 07:05, nằm trong đoạn cô chữa câu B1, chỉ trễ 21 giây so với nhãn. Bộ giải mã là quy hoạch động đơn điệu theo công thức D[k][j], tối ưu toàn cục và cho phép bỏ qua câu; sau đó mốc được lùi về các đoạn ngay trước có chung từ với câu hỏi, vì cô thường đọc đề trước rồi mới nói số câu."

**Chuyển ý:** "Em chuyển sang kết quả đo trên bài kiểm tra độc lập."

**Nếu bị hỏi ngay trên slide này:** "Câu không tìm được khẩu lệnh thì sao?" — câu không khớp lấy thời điểm màn hình xuất hiện nhưng bị kẹp giữa hai câu kề nhau, nên không đảo thứ tự. "Các trọng số 25/2/3 lấy đâu ra?" — chỉnh tay trên Unit 4 (dev), giữ nguyên khi chạy Unit 5.

#### Slide 8 · Kết quả căn chỉnh
**Người nói:** TV2 · **Thời lượng:** 80 s (07:40–09:00)

> "Thuật toán được chỉnh trên Unit 4, rồi chỉ chạy một lần trên Unit 5 để kiểm tra. Trên Unit 5, tỉ lệ câu có mốc lệch không quá 10 giây tăng từ 57 lên 80 phần trăm so với bản cũ, sai số trung bình giảm từ 28,5 xuống 8,1 giây, và không còn câu nào bị đảo thứ tự. Để so sánh, nếu chỉ lấy thời điểm màn hình xuất hiện thì đạt 49 phần trăm. Em cũng nói rõ: trên cả hai bài, DP chọn giống hệt greedy, nên phần cải thiện đến từ cách tính điểm, bước lùi mốc và cách xử lý câu không khớp, chứ không phải từ bản thân DP. Lỗi còn lại chủ yếu nằm ở các chỗ trống trong đoạn văn Part 6 và Part 7, nơi cô đọc liền cả đoạn nên rất khó nói câu bắt đầu lúc nào."

**Chuyển ý:** "Em xin mời TV3 trình bày phần liên kết câu hỏi với chủ điểm ngữ pháp."

**Nếu bị hỏi ngay trên slide này:** "Trên Unit 4, regex lấy 'câu N' đầu tiên đạt 71,9% ở ±10 s, cao hơn bản hiện tại (68,8%)?" — đúng, nhóm báo cáo nguyên văn; nhưng regex kém hơn ở ±30 s, sai số trung bình 28,1 s so với 10,0 s, và trên Unit 5 chỉ đạt 71,4% với 2 lần đảo thứ tự. "Nhãn ai gán?" — xem docs/09, Q1.

---

### Phần 3 — TV3 (slide 9–12 · 5,5 phút · 09:00–14:30)

#### Slide 9 · Liên kết câu hỏi ↔ chủ điểm ngữ pháp
**Người nói:** TV3 · **Thời lượng:** 90 s (09:00–10:30)

> "Câu 'The movie was very ___' với các lựa chọn move, moving, moved thuộc chủ điểm 'Participles as Adjectives', nhưng hai bên không có từ nào chung. Bản cũ dùng all-MiniLM-L6-v2, một mô hình chỉ hiểu tiếng Anh, trong khi phần giải thích chủ điểm viết bằng tiếng Việt; để bù, bản cũ ghép thêm từ khóa viết tay, mà trong đó có cả từ đáp án như central, luxury, shined, tức là rò rỉ nhãn. Khi bỏ bộ từ khóa đó, độ chính xác tụt từ 76,5 xuống 61,8 phần trăm. Bản hiện tại dùng multilingual-e5-small, và điểm của một cặp câu hỏi – chủ điểm là trung bình của hai cosine: giữa câu hỏi với chủ điểm, và giữa lời cô giảng trong lúc chữa câu đó với chủ điểm. Lời giảng chính là điểm kết hợp số 3: khi chữa, cô nói những câu như 'chọn động từ thêm ing hay thêm ed để làm tính từ', hay 'công thức nhờ vả'. Nếu điểm cao nhất đạt từ 0,835 trở lên thì gắn chủ điểm, ngược lại không gắn, vì nhiều câu chỉ là câu từ vựng hoặc đọc hiểu."

**Chuyển ý:** "Kết quả của cách làm này ở slide tiếp theo."

**Nếu bị hỏi ngay trên slide này:** "Lời giảng lấy đoạn nào?" — từ mốc bắt đầu chữa câu đó (lấy từ kết quả căn chỉnh) đến mốc của câu kế tiếp, có giới hạn độ dài (`SPEECH_MAX_S` trong `concept_link.py`). Không có mô hình thì dùng TF-IDF trên câu hỏi + lời giảng.

#### Slide 10 · Kết quả liên kết chủ điểm (Unit 4, 34 câu)
**Người nói:** TV3 · **Thời lượng:** 80 s (10:30–11:50)

> "Trước hết cần so với một mốc đơn giản: 22 trên 34 câu là câu từ vựng hoặc đọc hiểu, nên cách 'luôn không gắn' đã đạt 73,5 phần trăm, và bản cũ chỉ hơn mốc này 3 điểm. Biểu đồ bên trái so sánh các phương pháp; bản hiện tại, e5 đa ngữ cộng lời giảng, đạt 91,2 phần trăm. Bảng bên phải là đầu ra thực tế trong demo: độ chính xác tăng từ 58,8 lên 91,2 phần trăm, và trong demo cũ khoảng 61 phần trăm badge gắn sai, còn bản mới chỉ 1 trên 10 badge sai. Đổi lại, recall, tức tỉ lệ câu có chủ điểm được gắn đúng, là 75 phần trăm, nghĩa là vẫn có câu bị bỏ sót. Hạn chế lớn nhất em phải nói rõ: mô hình và ngưỡng được chọn trên chính 34 câu này, nên con số có thể lạc quan, và chưa có tập kiểm tra độc lập cho bài toán này."

**Chuyển ý:** "Ngoài liên kết câu hỏi, hệ thống còn trích chủ điểm và từ vựng từ bài giảng."

**Nếu bị hỏi ngay trên slide này:** "Ngưỡng 0,835 có overfit không?" — có nguy cơ; trong biểu đồ, ngưỡng được chọn leave-one-out (mỗi câu chấm bằng ngưỡng tối ưu trên 33 câu còn lại), nhưng việc chọn mô hình thì làm trên cùng 34 câu; điểm hai nhóm sát nhau (0,81–0,86) nên sang bài mới phải hiệu chỉnh lại (docs/09, Q7).

#### Slide 11 · Trích xuất chủ điểm và từ vựng
**Người nói:** TV3 · **Thời lượng:** 80 s (11:50–13:10)

> "Bốn chủ điểm ngữ pháp được Gemini trích ra ở chế độ JSON, gồm tiêu đề, công thức và lời giải thích; nhưng Gemini chỉ thấy khoảng 30 đoạn lời giảng lấy mẫu, nên mốc thời gian nó trả về thực chất là đoán. Ví dụ phần bị động cô giảng ở 13:16, Gemini lại trả về 55:02, lệch gần 42 phút. Nhóm neo lại mỗi chủ điểm vào cửa sổ lời giảng giống nó nhất theo e5, nhờ đó sai số trung bình giảm từ 882,5 giây xuống 11,2 giây; khi không có mạng thì dùng bảng chủ điểm TOEIC và tìm từ khóa trong lời giảng. Về từ vựng, vocab.py lemma hóa hai lớp, tra từ điển CEFR-J và Octanove 8.845 mục, lọc những từ trùng mặt chữ Việt – Anh như 'hay', 'con', và lấy nghĩa tiếng Việt theo mẫu 'X là, nghĩa là' trong lời giảng. Unit 4 có 80 từ, 52 từ có nghĩa tiếng Việt và 79 clip audio giọng cô; em lưu ý là độ đúng của nghĩa và audio chưa được đánh giá."

**Chuyển ý:** "Phần cuối của em là phát hiện lỗi người học trong chat."

**Nếu bị hỏi ngay trên slide này:** "JSON mode có phải structured output với schema chặt không?" — không; chỉ đặt `responseMimeType=application/json` rồi kiểm tra các trường sau khi parse. "Clip audio cắt thế nào?" — theo ranh giới đoạn ASR có chứa từ (ưu tiên đoạn chỉ có một từ), vì transcript không có timestamp từng từ. "Lọc trùng mặt chữ làm thế nào?" — `hay`, `con`, `cho`, `ra`, `nam`, `sau`… nằm trong danh sách cố định `VI_HOMOPHONES` (41 âm tiết), còn `an`, `can` bị loại qua danh sách stopword tiếng Anh. Bộ lọc không xét ngữ cảnh, và `may` hiện **chưa** được lọc.

#### Slide 12 · Phát hiện lỗi người học trong chat
**Người nói:** TV3 · **Thời lượng:** 80 s (13:10–14:30)

> "Module feedback.py dùng luật cho sáu mẫu lỗi chuyển di từ tiếng Việt: thừa 'be' như 'I am agree', nhầm đuôi -ing và -ed, cấu trúc nhờ vả, 'should to', hòa hợp chủ vị, và thiếu trợ động từ 'do' trong câu hỏi. Mỗi lỗi kèm câu sửa, giải thích tiếng Việt và một loại lỗi ERRANT; các loại trong bảng đã được kiểm chứng bằng thư viện errant 3.0.2 chính thức, ví dụ 'should to increase' là U:VERB:FORM. Bản cũ khớp nguyên văn từng câu chat, nên tỉ lệ 6 trên 6 trước đây không có ý nghĩa. Bản mới được đo trên 70 câu viết độc lập, không xem luật: precision 100 phần trăm, recall 72,7 phần trăm, F1 84,2. Đây không phải mô hình GEC tổng quát, lỗi ngoài sáu nhóm sẽ bị bỏ qua, và trước khi chốt nhóm đã xem tập 70 câu một lần để sửa 3 lỗi cài đặt."

**Chuyển ý:** "Em xin mời TV4 trình bày báo cáo cho giáo viên và demo."

**Nếu bị hỏi ngay trên slide này:** "'I am confusing → confused' sao lại R:VERB:FORM?" — R:VERB:FORM là nhãn mặc định của nhóm -ing/-ed (lấy từ cặp "The movie was moved → moving"); với riêng cặp "confusing → confused", errant 3.0.2 cho R:MORPH. Nếu máy có cài `errant`, `feedback.py` để errant tự gán nhãn từng lỗi. "Precision 100% có đáng tin?" — tập chỉ 70 câu, nhãn cũng là bản nháp; nhưng 10 câu có lỗi ngoài phạm vi không bị báo nhầm câu nào.

---

### Phần 4 — TV4 (slide 13–17 · 5,5 phút · 14:30–20:00)

#### Slide 13 · Báo cáo cho giáo viên
**Người nói:** TV4 · **Thời lượng:** 60 s (14:30–15:30)

> "Báo cáo cho giáo viên giờ chỉ hiển thị những gì tính được từ dữ liệu. Thứ nhất là phân bố lỗi trong chat theo sáu nhóm. Thứ hai là chủ điểm yếu nhất: hệ thống đi từ lỗi trong chat, qua câu hỏi mà tin nhắn đó trả lời, tới chủ điểm của câu hỏi; ở Unit 4 kết quả là Participles, với 2 tin nhắn ở câu 4 và câu 6. Thứ ba là gợi ý cho buổi sau, là câu mẫu điền từ dữ liệu, không dùng LLM, và mỗi dòng đều nêu căn cứ. Còn tỉ lệ thời gian nói TTT/STT, vì bản ghi chỉ có một người nói nên hệ thống ghi 'chưa đo' thay vì báo 100/0 như bản cũ; muốn đo được thì cần ghi âm tách kênh từng người trên Zoom hoặc dùng pyannote."

**Chuyển ý:** "Bây giờ em xin demo trực tiếp."

**Nếu bị hỏi ngay trên slide này:** "Chat là mô phỏng thì chủ điểm yếu nhất có ý nghĩa không?" — không, ở đây chỉ minh họa luồng chat → lỗi → câu hỏi → chủ điểm; cần chat của lớp thật mới kết luận được.

#### Slide 14 · Demo
**Người nói:** TV4 · **Thời lượng:** 120 s (15:30–17:30), phần lớn là demo trực tiếp

*(Chuyển sang trình duyệt đã mở sẵn sổ tay Unit 4.)*

> "Đây là sổ tay học viên của Unit 4: bên trái là video với transcript chạy theo, bên phải là danh sách câu hỏi kèm badge chủ điểm. Em bấm thẻ Question 4, câu 'The movie was very…', video tua đến 15:05, lúc cô nói 'Câu số 4'; câu này có badge Participles as Adjectives, em bấm 'Lý thuyết' thì video tua về 00:44, đoạn cô giảng phân từ ở đầu giờ. Sang tab Vocab, em lọc theo bậc CEFR và bấm nghe audio giọng cô đọc từ. Ở tab Chat & GEC, mỗi tin nhắn có lỗi hiện phần sai, câu sửa và lời giải thích tiếng Việt, tên học viên đã được ẩn danh thành S1, S2. Cuối cùng là tab Analytics, mở thẳng được bằng tham số ?tab=tab-stats, chính là báo cáo em vừa trình bày."

**Chuyển ý:** "Sau phần demo, em trình bày cách nhóm bảo đảm các con số tái lập được."

**Chuẩn bị:** chạy `python demo/prepare.py --lesson lessons/ece-toeic-starter-u4` rồi `cd demo && python -m RangeHTTPServer 8000` trước giờ trình bày; mở sẵn video quay dự phòng. Nếu demo lỗi, chuyển ngay sang video dự phòng, không sửa trực tiếp trước hội đồng. Chỉ thao tác những gì có trên slide. Có 4 thẻ "Question 4": chọn thẻ có đề *movie*. Không lấy làm ví dụ: Question 1 đầu bài (mốc lệch 21 s), Question 5 *shoes* (không khớp được lời giảng) và Question 13 (badge gắn sai).

#### Slide 15 · Đánh giá tái lập được
**Người nói:** TV4 · **Thời lượng:** 55 s (17:30–18:25)

> "Mọi con số trong bài đều tạo lại được bằng một lệnh, python eval/run_all.py, và baseline v1 được chạy lại từ commit 73d9a62 chứ không chép số cũ. Căn chỉnh được chỉnh trên Unit 4 và kiểm tra trên Unit 5; pipeline cũ vẫn qua kiểm tra hồi quy trên CS224N với 9 trên 10 mốc chuyển slide, sai số trung bình 0,6 giây; và pytest chạy đạt 71 trên 71 test, không test nào ghi vào dữ liệu bài học. Bảng bên phải là các bộ nhãn chuẩn: mốc chữa câu của 32 câu Unit 4 và 35 câu Unit 5, mốc lý thuyết của 4 chủ điểm, chủ điểm của 34 câu, 70 câu chat viết độc lập trong đó 54 câu có lỗi và 16 câu đúng, và 5 clip ASR chưa sửa. Tất cả đều là bản nháp do AI gán mà không xem output của hệ thống, và nhóm đang đối chiếu lại với video trước khi bảo vệ."

**Chuyển ý:** "Từ đó, nhóm tự nêu các hạn chế."

**Nếu bị hỏi ngay trên slide này:** "AI gán nhãn thì sao tin được?" — đó là bản nháp, `verified: false`; người gán không xem output hệ thống. Sau khi nhóm sửa nhãn, chạy lại `eval/run_all.py`; nếu số thay đổi thì cập nhật docs/10 trước, rồi đến slide.

#### Slide 16 · Hạn chế và hướng phát triển
**Người nói:** TV4 · **Thời lượng:** 50 s (18:25–19:15)

> "Dữ liệu còn nhỏ: chỉ hai bài có nhãn, một giáo viên, một người nói; nhãn chuẩn chưa được người kiểm tra hết, và chat là dữ liệu mô phỏng. Nhóm chưa đo WER, nên chưa chứng minh được gợi ý từ màn hình có ích; ngưỡng liên kết chủ điểm chọn trên tập phát triển; và bộ phát hiện lỗi chỉ dựa trên luật cho sáu mẫu. Việc đầu tiên nhóm sẽ làm là sửa tay năm clip để có WER thật cho ba cấu hình, và thu bản ghi lớp học thật có tách kênh từng người cùng chat thật để đo TTT/STT. Sau đó là gán nhãn chủ điểm cho Unit 5 làm tập kiểm tra độc lập, thử mô hình sửa câu seq2seq hoặc LLM rồi dùng errant để gán loại lỗi, và mở rộng sang bài giảng IELTS."

**Chuyển ý:** "Em xin tóm tắt lại."

#### Slide 17 · Kết luận
**Người nói:** TV4 · **Thời lượng:** 45 s (19:15–20:00)

> "Nhóm có ba đóng góp chính, mỗi đóng góp đi kèm số liệu đo được. Một là căn chỉnh câu hỏi với lời giảng, có xác minh khẩu lệnh theo ngữ cảnh: 80 phần trăm câu đúng trong 10 giây trên bài kiểm tra độc lập, so với 57 phần trăm của bản cũ. Hai là dùng lời giảng làm tín hiệu liên kết chủ điểm với e5 đa ngữ: 91,2 phần trăm trên 34 câu, so với 58,8 phần trăm, mà không cần từ khóa viết tay. Ba là đánh giá tái lập được, và những gì chưa đo được thì ghi rõ là chưa đo. Em cảm ơn thầy/cô và các bạn đã lắng nghe, nhóm em xin sẵn sàng trả lời câu hỏi."

---

## 3. Phân công trả lời hỏi đáp

Câu trả lời chi tiết ở [docs/09, phần 3](09_teacher_presentation_and_technical_nlp_guide.md). Người trả lời chính nói trước; người khác chỉ bổ sung khi được mời.

| Chủ đề câu hỏi | Trả lời chính | Câu trong docs/09 |
| :--- | :-: | :-: |
| Cách đo 80%, ai gán nhãn; regex "câu N" so với bản hiện tại; DP và greedy | TV2 | Q1–Q3 |
| WER, gợi ý từ màn hình; lỗi lan truyền từ ASR/OCR | TV2 | Q4–Q5 |
| Embedding so với TF-IDF/BM25; ngưỡng 0,835; ERRANT | TV3 | Q6–Q8 |
| Chat thật hay giả, ẩn danh hoá | TV1 | Q9 |
| Tại sao không dùng LLM cho tất cả | TV1 | Q10 |
| Báo cáo giáo viên, TTT/STT | TV4 | Q11 |
| Mở rộng sang IELTS | TV4 | Q12 |

## 4. Chuẩn bị trước buổi bảo vệ
- Kiểm tra nhãn gold theo docs/10 §2, đặt `verified: true`, chạy lại `python eval/run_all.py`. Nếu số thay đổi: sửa docs/10 trước, rồi slide và tài liệu này.
- Tập nói có bấm giờ theo bảng ở mục 1; phần demo không quá 2 phút.
- Mở sẵn: trình duyệt với demo Unit 4, video dự phòng, docs/10 (để tra số khi bị hỏi).
