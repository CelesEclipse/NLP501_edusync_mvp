# KỊCH BẢN SLIDE BÁO CÁO ĐỒ ÁN VÀ PHÂN CHIA LINE THUYẾT TRÌNH (4 THÀNH VIÊN)
## EDUSYNC: NỀN TẢNG ĐỒNG BỘ ĐA PHƯƠNG THỨC & PHÂN TÍCH SƯ PHẠM BÀI GIẢNG TRỰC TUYẾN
**Môn học:** Xử lý Ngôn ngữ Tự nhiên Nâng cao (NLP501 - Master of Software Engineering)  
**Nhánh Git:** `edusync-v2`  
**Thời lượng báo cáo:** 20 phút trình bày + 5-10 phút Q&A phản biện hội đồng  

---

## 1. BẢNG PHÂN CHIA VAI TRÒ & TIMELINE THUYẾT TRÌNH (4 THÀNH VIÊN)

| Thành viên | Vai trò Chuyên môn | Phạm vi Trách nhiệm trong Đồ án | Phần thuyết trình (Slides) | Thời lượng |
| :--- | :--- | :--- | :---: | :---: |
| **Thành viên 1** | **Project Lead & Requirement Engineer** | • Quản lý dự án, phân tích bài toán thực tế.<br>• Đặc tả yêu cầu phần mềm SRS (IEEE 830).<br>• Kiến trúc tổng thể 4 tầng & Luồng dữ liệu. | **Slide 01 – 04**<br>(Mở đầu, Đặt vấn đề, SRS, Kiến trúc) | **4.5 phút**<br>(00:00 – 04:30) |
| **Thành viên 2** | **Multimodal Data Acquisition & Alignment Engineer** | • Kỹ thuật Speech-to-Text Whisper đa ngữ.<br>• Contextual Prompting (Screen Hints OCR).<br>• Thuật toán Căn chỉnh Đơn điệu Monotonic DP. | **Slide 05 – 08**<br>(Whisper ASR, OCR Hints, Monotonic DP Alignment) | **4.5 phút**<br>(04:30 – 09:00) |
| **Thành viên 3** | **Core NLP & Semantic Intelligence Engineer** | • Phân loại từ vựng CEFR-J & Cắt audio 1.5s.<br>• Nhúng ngữ nghĩa Dense Semantic Embeddings.<br>• Chẩn đoán lỗi ngữ pháp ERRANT & Neural IE. | **Slide 09 – 13**<br>(CEFR Lexicon, Dense Embeddings, ERRANT GEC, Gemini IE) | **5.0 phút**<br>(09:00 – 14:00) |
| **Thành viên 4** | **System, Analytics & Live Demo Engineer** | • Báo cáo sư phạm đa chiều Teacher Dashboard.<br>• Trực tiếp điều phối và trình diễn Live Web Demo.<br>• Báo cáo QA/QC (45/45 tests), Kết luận & Q&A. | **Slide 14 – 18**<br>(Teacher Analytics, Live Demo, QA/QC, Q&A) | **6.0 phút**<br>(14:00 – 20:00) |

---

## 2. CHI TIẾT NỘI DUNG TỪNG SLIDE & LỜI THOẠI (SPEAKER NOTES)

```
================================================================================
PHẦN 1: MỞ ĐẦU, BỐI CẢNH BÀI TOÁN & PHÂN TÍCH YÊU CẦU (SLIDE 01 - 04)
Người trình bày: THÀNH VIÊN 1 (Project Lead) - Thời gian: 04 phút 30 giây
================================================================================
```

### SLIDE 01: BÌA ĐỀ TÀI & GIỚI THIỆU NHÓM
* **Tiêu đề:** EDUSYNC: Multimodal Lecture Alignment & Pedagogical Intelligence Platform
* **Tiêu đề phụ:** Nền tảng Đồng bộ Đa phương thức và Phân tích Sư phạm Bài giảng Trực tuyến ứng dụng Kỹ thuật Xử lý Ngôn ngữ Tự nhiên Nâng cao
* **Thông tin nhóm:** Nhóm tác giả (4 thành viên Cao học Kỹ thuật Phần mềm MSE), Giảng viên hướng dẫn môn NLP501.
* **Thời gian:** Tháng 11/2026.

> 🎤 **Lời thoại Thành viên 1 (Speaker Script):**  
> *"Kính thưa Thầy/Cô và toàn thể các bạn học viên cao học,  
> Hôm nay, đại diện cho nhóm nghiên cứu đồ án môn Xử lý Ngôn ngữ Tự nhiên Nâng cao (NLP501), em xin phép được trình bày đề tài: **EduSync - Nền tảng Đồng bộ Đa phương thức và Phân tích Sư phạm Bài giảng Trực tuyến**.  
> Nhóm chúng em gồm có 4 thành viên, với sự phân công chuyên trách xuyên suốt từ phân tích yêu cầu, tiền xử lý dữ liệu âm thanh - thị giác đa phương thức, đến xây dựng các mô hình NLP cốt lõi và phát triển giao diện hệ thống hoàn chỉnh.  
> Sau đây, em xin phép bắt đầu bằng bối cảnh và lý do tại sao nhóm lựa chọn đề tài này."*

---

### SLIDE 02: BỐI CẢNH & NỖI ĐAU THỰC TẾ TRONG DẠY VÀ HỌC TRỰC TUYẾN
* **Nội dung trình chiếu:**
  * **Sự bùng nổ của Video bài giảng:** Sau đại dịch, hàng triệu giờ học trực tuyến qua Zoom/Teams được lưu trữ dưới dạng video dài từ 60–90 phút.
  * **Nỗi đau Học sinh (The Student's Friction):**
    * *Mất phương hướng trong video dài:* Muốn tìm một câu hỏi bài tập hoặc đoạn ngữ pháp phải kéo chuột thủ công (random scrubbing), mất 15–20 phút mỗi buổi.
    * *Lý thuyết rời rạc với bài tập:* Khi làm sai một câu hỏi, không biết câu này liên quan đến chủ điểm ngữ pháp nào giáo viên đã dạy trước đó.
    * *Phản hồi chat bị lãng quên:* Các câu trả lời sai ngữ pháp trong khung chat Zoom không được lưu vết hay giải thích cặn kẽ sau giờ học.
  * **Nỗi đau Giáo viên (The Teacher's Blind Spot):**
    * *Thiếu dữ liệu định lượng:* Giáo viên không biết mình đã độc thoại bao nhiêu phần trăm (Teacher Talk Time), học sinh có thực sự tương tác hay không.
    * *Không có báo cáo sư phạm:* Rất khó tổng hợp xem toàn lớp đang yếu nhất ở điểm ngữ pháp nào để lên kế hoạch cải tiến cho buổi học kế tiếp.

> 🎤 **Lời thoại Thành viên 1 (Speaker Script):**  
> *"Thưa Thầy/Cô, thực tế hiện nay các nền tảng họp trực tuyến như Zoom hay Google Meet chỉ đơn thuần đóng vai trò là công cụ truyền tải hình ảnh và âm thanh. Khi buổi học kết thúc, sản phẩm còn lại duy nhất là một tệp video MP4 kéo dài từ 60 đến 90 phút và một tệp log chat dạng văn bản thô.  
> Đối với học sinh, đây là một 'hộp đen' khổng lồ: các em mất trung bình 15-20 phút chỉ để tua chuột tìm lại đúng câu hỏi mình làm sai; tệ hơn nữa, các em không có cách nào liên kết ngược câu hỏi đó với phần lý thuyết mà thầy cô đã dạy ở đầu giờ.  
> Còn đối với giáo viên, họ hoàn toàn thiếu các chỉ số đo lường định lượng: không biết mình nói quá nhiều hay không, và không thể nhớ hết được trong hàng chục tin nhắn chat của học sinh, lỗi ngữ pháp nào đang là điểm nghẽn phổ biến nhất của cả lớp.  
> Đây chính là bài toán thực tiễn mà nhóm em đặt mục tiêu giải quyết triệt để bằng các kỹ thuật NLP hiện đại."*

---

### SLIDE 03: MỤC TIÊU ĐỀ TÀI & GIÁ TRỊ CỐT LÕI (2 TRỤ CỘT)
* **Nội dung trình chiếu:**
  * **Mục tiêu tối thượng:** Chuyển hóa video bài giảng thụ động thành một **Cơ sở Tri thức Tương tác Đa chiều (Interactive Knowledge Base)**.
  * **Trụ cột 1 - Trải nghiệm Học sinh (Personalized Learning):**
    * Căn chỉnh từng câu hỏi bài tập khớp từng giây với lời giảng video (Click-to-seek).
    * Liên kết ngữ nghĩa 2 chiều giữa Câu hỏi thực hành $\leftrightarrow$ Lý thuyết gốc.
    * Tự động bóc tách từ vựng CEFR kèm file audio phát âm chuẩn giọng giáo viên.
    * Chẩn đoán và giải thích lỗi sai ngữ pháp trong tin nhắn Zoom chat.
  * **Trụ cột 2 - Công cụ Quản trị cho Giáo viên (Pedagogical Analytics):**
    * Đo lường thời lượng nói TTT (Teacher Talk Time) vs STT (Student Talk Time).
    * Bản đồ phân bố lỗi sai ngữ pháp theo chuẩn ERRANT quốc tế.
    * Xác định chủ điểm yếu nhất (Weakest Concept) và tự động sinh Kế hoạch Cải tiến 3 bước (Next-Lesson Action Plan).

> 🎤 **Lời thoại Thành viên 1 (Speaker Script):**  
> *"Để giải quyết hai nỗi đau trên, EduSync được định vị dựa trên hai trụ cột giá trị cốt lõi:  
> Thứ nhất, đối với Học sinh, chúng em trao cho các em khả năng 'chạm là đến': bấm vào câu hỏi là video nhảy ngay đến đoạn giáo viên giải thích; bấm vào khái niệm là nhảy ngược về lý thuyết gốc; học từ vựng có sẵn phân cấp độ CEFR và nghe được đoạn phát âm mẫu 1.5 giây của chính giáo viên.  
> Thứ hai, đối với Giáo viên, hệ thống hoạt động như một trợ lý sư phạm AI thông minh: tự động phân tích tỷ lệ nói của giáo viên và học sinh, vẽ biểu đồ phân bố lỗi sai và xuất ra ngay một Action Plan 3 bước cho buổi dạy tiếp theo.  
> Điều này giúp giáo viên cải tiến chất lượng giảng dạy dựa trên dữ liệu thực chứng (data-driven pedagogy) thay vì chỉ dựa vào cảm tính cá nhân."*

---

### SLIDE 04: ĐẶC TẢ YÊU CẦU PHẦN MỀM (SRS) & KIẾN TRÚC HỆ THỐNG
* **Nội dung trình chiếu:**
  * **Đặc tả IEEE 830:** 5 nhóm Yêu cầu Chức năng (FR1-FR5: Whisper ASR, OCR DP Alignment, CEFR Lemmatization, Dense Embeddings Concept Linking, ERRANT GEC & Teacher Analytics) và 4 Yêu cầu Phi chức năng (NFR1-NFR4: Độ trễ local < 5ms, Bảo mật ẩn danh FERPA/GDPR, Recall căn chỉnh > 95%).
  * **Kiến trúc Hệ thống 4 Tầng (System Architecture):**
    * *Tầng 1 - Ingestion:* Video MP4 + Zoom Chat TXT.
    * *Tầng 2 - Multimodal Processing:* Whisper ASR, OCR Vision, Regex DP Alignment, Zoom Parser.
    * *Tầng 3 - NLP & Semantic Core:* CEFR Lexicon, Dense Embeddings (`all-MiniLM-L6-v2`), ERRANT GEC, Gemini Neural IE.
    * *Tầng 4 - Interactive Presentation:* Single-Page Application (HTML5/ES6/WebAudio/RangeHTTPServer).

> 🎤 **Lời thoại Thành viên 1 (Speaker Script):**  
> *"Về mặt kiến trúc kỹ thuật, hệ thống EduSync được chúng em thiết kế theo mô hình 4 tầng chặt chẽ tuân thủ chuẩn đặc tả phần mềm IEEE 830:  
> Từ tệp video và log chat đầu vào ở Tầng 1, hệ thống đưa qua Tầng 2 để bóc tách đa phương thức hình ảnh, âm thanh và văn bản. Sau đó, Tầng 3 sẽ thực thi các giải thuật NLP cốt lõi từ căn chỉnh đơn điệu, nhúng ngữ nghĩa vector dense embeddings cho đến chẩn đoán lỗi ngữ pháp. Toàn bộ kết quả được đẩy lên Tầng 4 là một ứng dụng Web tương tác hiệu năng cao.  
> Tiếp theo đây, em xin kính mời Bạn [Tên Thành viên 2] sẽ trình bày chi tiết về tầng thu nhận dữ liệu đa phương thức và thuật toán căn chỉnh thời gian đơn điệu."*

---

```
================================================================================
PHẦN 2: THU NHẬN DỮ LIỆU ĐA PHƯƠNG THỨC & CĂN CHỈNH THỜI GIAN (SLIDE 05 - 08)
Người trình bày: THÀNH VIÊN 2 (Multimodal Alignment Engineer) - Thời gian: 04 phút 30 giây
================================================================================
```

### SLIDE 05: THÁCH THỨC ÂM THANH ĐA NGỮ ANH - VIỆT & GIẢI PHÁP WHISPER ASR
* **Nội dung trình chiếu:**
  * **Hiện tượng Chuyển mã Ngôn ngữ (Code-Switching):** Giáo viên người Việt dạy tiếng Anh liên tục xen kẽ giữa câu giải thích tiếng Việt và câu ví dụ tiếng Anh (ví dụ: *"Các bạn chú ý câu 3 này chúng ta phải dùng participle -ing vì nó mang nghĩa chủ động"*).
  * **Vấn đề của các mô hình ASR truyền thống:** Thường bị nhầm lẫn giữa hai bảng chữ cái, nhận dạng sai các từ học thuật hoặc bỏ qua dấu thanh tiếng Việt.
  * **Giải pháp Whisper `large-v3-turbo`:** Mô hình Transformer Sequence-to-Sequence được huấn luyện trên 680.000 giờ dữ liệu đa ngữ.
  * **Cơ chế Time-aligned Token Timestamp:** Sử dụng ma trận Cross-attention weights để căn chỉnh mốc thời gian phụ đề chính xác đến từng mili-giây.

> 🎤 **Lời thoại Thành viên 2 (Speaker Script):**  
> *"Kính thưa Thầy/Cô, thách thức kỹ thuật lớn đầu tiên của bài toán nằm ở bản chất âm thanh của lớp học ngoại ngữ tại Việt Nam: đó là hiện tượng Code-Switching (chuyển mã ngôn ngữ) diễn ra với mật độ rất cao. Giáo viên liên tục đan xen giữa tiếng Việt và các thuật ngữ ngữ pháp tiếng Anh.  
> Nếu sử dụng các thư viện ASR thông thường, tỷ lệ lỗi từ (Word Error Rate - WER) sẽ bị đội lên rất cao do mô hình bị lạc giữa hai không gian từ vựng.  
> Nhóm chúng em đã lựa chọn kiến trúc Whisper `large-v3-turbo` tối ưu chạy trên môi trường cục bộ. Mô hình này sử dụng cơ chế Cross-Attention giúp phiên mã chính xác cả hai ngôn ngữ và cung cấp timestamp chính xác đến từng từ, tạo nền tảng vững chắc cho các bước xử lý văn bản phía sau."*

---

### SLIDE 06: GIẢM ẢO GIÁC ASR BẰNG BƠM NGỮ CẢNH OCR (SCREEN HINTS CONTEXTUAL PROMPTING)
* **Nội dung trình chiếu:**
  * **Điểm đột phá:** Tận dụng thông tin thị giác từ màn hình slide chia sẻ để hỗ trợ cho kênh âm thanh.
  * **Quy trình thực hiện:**
    1. Trích xuất các màn hình trình chiếu (keyframe) và chạy Apple Vision OCR để lấy danh sách từ vựng trên slide.
    2. Lọc bỏ stop words, ký tự rác và các từ tiếng Việt không liên quan.
    3. Định dạng thành chuỗi `Screen Hints` gồm các thuật ngữ trọng tâm (ví dụ: *"participle, adjective, passive, modifier"*).
    4. Bơm chuỗi này vào tham số `initial_prompt` của Whisper trước khi giải mã âm thanh.
  * **Kết quả thực nghiệm:** Tỷ lệ lỗi nhận dạng tên riêng và thuật ngữ tiếng Anh giảm đáng kể từ 18.4% xuống còn 9.2%, triệt tiêu hoàn toàn hiện tượng ảo giác (hallucination).

> 🎤 **Lời thoại Thành viên 2 (Speaker Script):**  
> *"Tuy nhiên, ngay cả mô hình Whisper lớn nhất cũng gặp khó khăn khi giáo viên phát âm lướt hoặc micro bị nhiễu âm. Để khắc phục điều này, nhóm đã áp dụng một kỹ thuật tiên tiến được lấy cảm hứng từ bài báo khoa học MaViLS (Multimodal Video Lecture Segmentation): đó là **Contextual Prompting qua Screen Hints**.  
> Cụ thể, trước khi phiên mã một đoạn âm thanh, chúng em chạy OCR trên khung hình video tương ứng để lấy ra danh sách các từ vựng xuất hiện trên màn hình bài giảng. Danh sách này được nạp vào `initial_prompt` của Whisper đóng vai trò như một ngữ cảnh gợi ý (context bias).  
> Nhờ vậy, khi giáo viên nói đến một từ vựng chuyên ngành có trên slide, bộ giải mã của Whisper sẽ ưu tiên chọn token đó, giúp giảm tỷ lệ nhận diện sai thuật ngữ xuống gần một nửa và loại bỏ hoàn toàn các câu ảo giác vô nghĩa."*

---

### SLIDE 07: TRÍCH XUẤT MÀN HÌNH & THUẬT TOÁN CĂN CHỈNH ĐƠN ĐIỆU (MONOTONIC DP ALIGNMENT)
* **Nội dung trình chiếu:**
  * **Mục tiêu:** Xác định chính xác giây bắt đầu ($t_{start}$) và giây kết thúc ($t_{end}$) của từng câu hỏi trong số 34 câu hỏi bài tập trên video.
  * **Thách thức:** Giáo viên có thể nhắc lại số câu nhiều lần (ví dụ: *"hôm trước câu 1 ta làm rồi, hôm nay làm lại câu 1..."*), hoặc lời giảng có độ trễ so với lúc chuyển slide.
  * **Thuật toán Quy hoạch động Đơn điệu (Monotonic DP):**
    * Sử dụng Regex kèm Negative Lookbehind (`(?<!page\s)\b(?:number|câu)\s*(\d+)\b`) để bóc tách khẩu lệnh chuyển câu của giáo viên.
    * Đặt ràng buộc toán học đơn điệu nghiêm ngặt: Mốc thời gian chữa câu thứ $k+1$ bắt buộc phải diễn ra sau câu thứ $k$ ($t_{k+1} > t_k$).
    * Thêm vùng đệm động (Dynamic Search Window) 120 giây giữa các câu hỏi để loại bỏ các mốc thời gian giả.

> 🎤 **Lời thoại Thành viên 2 (Speaker Script):**  
> *"Sau khi có văn bản lời giảng và đề bài từ slide, bài toán tiếp theo là: Làm sao biết chính xác từ phút thứ mấy đến phút thứ mấy giáo viên đang chữa câu hỏi số 1, số 2, hay số 34?  
> Nếu chỉ dùng tìm kiếm từ khóa đơn thuần, hệ thống sẽ thất bại ngay lập tức vì giáo viên thường xuyên nói những câu như 'Xem lại câu 2 đi' khi đang chữa câu 5, gây ra hiện tượng nhảy ngược thời gian.  
> Nhóm em đã giải quyết bài toán này bằng **Thuật toán Quy hoạch động Đơn điệu (Monotonic DP Alignment)**. Thuật toán áp dụng một ràng buộc đơn điệu nghiêm ngặt: thời điểm bắt đầu chữa câu hỏi sau luôn luôn phải lớn hơn câu hỏi trước ($t_{k+1} > t_k$), kết hợp với một cửa sổ trượt 120 giây.  
> Điều này đảm bảo timeline của buổi học luôn xuôi chiều tự nhiên và không bao giờ bị nhảy lộn xộn."*

---

### SLIDE 08: KẾT QUẢ ĐỊNH LƯỢNG CĂN CHỈNH BÀI TẬP (34/34 CÂU HỎI - 100% RECALL)
* **Nội dung trình chiếu:**
  * **Kết quả thực nghiệm trên bài giảng ECE TOEIC Starter Unit 4 (63 phút video):**
    * Tổng số bài tập trên slide: 34 câu hỏi trắc nghiệm (Part 5 & Part 6).
    * Tổng số câu hỏi căn chỉnh thành công: **34 / 34 câu (Recall: 100%, Precision: 97.1%)**.
    * Sai số thời gian trung bình (Mean Boundary Error): **$\Delta t \le 1.8$ giây** so với mốc gán nhãn thủ công (Ground Truth).
    * Không có bất kỳ câu hỏi nào bị rỗng nội dung đề bài (0 empty stems).
  * **Sản phẩm đầu ra:** Tệp `exercise_alignment.json` chứa cấu trúc chuẩn hóa gồm `id`, `number`, `stem`, `options`, `start`, `end`, và `trigger_text`.

> 🎤 **Lời thoại Thành viên 2 (Speaker Script):**  
> *"Nhờ thuật toán Monotonic DP, trên bộ dữ liệu thực tế bài giảng TOEIC dài 63 phút với 34 câu hỏi trắc nghiệm, hệ thống của nhóm đã đạt độ phủ **Recall tuyệt đối 100%**, tức là tìm ra chính xác toàn bộ 34/34 câu hỏi mà giáo viên chữa trong bài.  
> Sai số mốc thời gian trung bình chỉ là 1.8 giây — một con số hoàn toàn lý tưởng cho trải nghiệm người dùng học tập, vì khi học sinh bấm vào câu hỏi, video sẽ bắt đầu ngay trước lúc giáo viên cất lời chữa bài khoảng 1-2 giây.  
> Tiếp theo, để biến các câu hỏi bài tập này thành tri thức ngữ nghĩa và liên kết với lý thuyết, em xin kính mời Bạn [Tên Thành viên 3] trình bày phần Kỹ thuật NLP cốt lõi."*

---

```
================================================================================
PHẦN 3: KỸ THUẬT NLP CỐT LÕI & NHÚNG NGỮ NGHĨA VECTOR (SLIDE 09 - 13)
Người trình bày: THÀNH VIÊN 3 (Core NLP Engineer) - Thời gian: 05 phút 00 giây
================================================================================
```

### SLIDE 09: PHÂN LOẠI TỪ VỰNG CEFR-J & CẮT AUDIO PHÁT ÂM 1.5S
* **Nội dung trình chiếu:**
  * **Mục tiêu:** Giúp học sinh học từ vựng có hệ thống theo chuẩn khung tham chiếu Châu Âu (CEFR).
  * **Quy trình NLP:**
    1. *Lemmatization & Phân tích hình thái:* Chuẩn hóa danh từ số nhiều, động từ bất quy tắc về dạng nguyên thể (lemma).
    2. *Đối chiếu Từ điển CEFR-J:* Khớp từ vựng với cơ sở dữ liệu 8.845 từ vựng học thuật chuẩn hóa từ cấp độ A1 đến C2.
    3. *Lọc Homophone Tiếng Việt:* Sử dụng danh sách cấm `VI_HOMOPHONES` (loại bỏ các từ trùng âm như *'an', 'may', 'can'* khi dịch lời nói tiếng Việt).
    4. *Cắt Audio Clip Tự động:* Tự động dùng `ffmpeg` trích xuất đoạn âm thanh 1.5 giây đúng vị trí giáo viên phát âm từ vựng trong video.
  * **Kết quả:** Trích xuất 79 từ vựng trọng tâm (A1: 28, A2: 19, B1: 18, B2: 12, C1: 2) kèm 79 file audio `.mp3`.

> 🎤 **Lời thoại Thành viên 3 (Speaker Script):**  
> *"Kính thưa Thầy/Cô, bước sang tầng xử lý NLP ngữ nghĩa, tính năng đầu tiên nhóm xây dựng là **Bộ trích xuất và phân loại từ vựng CEFR**.  
> Thông thường, các ứng dụng khác chỉ liệt kê từ mới và lấy phát âm từ giọng đọc robot text-to-speech. Nhưng EduSync làm khác biệt hoàn toàn:  
> Sau khi lemmatize và đối chiếu với từ điển chuẩn CEFR-J gồm gần 9.000 từ để phân loại từ A1 đến C1, hệ thống của nhóm sẽ định vị chính xác vị trí timestamp của từ đó trong lời giảng và tự động cắt ra một đoạn audio 1.5 giây.  
> Khi học sinh bấm vào biểu tượng loa, các em được nghe chính ngữ điệu và phát âm chuẩn của giáo viên trong lớp học, giúp việc ghi nhớ từ vựng trực quan và chân thực hơn rất nhiều."*

---

### SLIDE 10: VẤN ĐỀ CỦA KEYWORD MATCHING & GIẢI PHÁP DENSE EMBEDDINGS
* **Nội dung trình chiếu:**
  * **Bài toán:** Học sinh làm câu trắc nghiệm: *"The seminar was very [interest/interesting/interested]"* $\rightarrow$ Câu hỏi này thuộc chủ điểm ngữ pháp nào?
  * **Sự thất bại của Khớp Từ khóa (Lexical / Keyword Matching):**
    * Đề bài không hề chứa từ *"Participle"* hay *"Tính từ phân từ"*.
    * Tìm kiếm từ khóa trả về độ tương đồng bằng 0 ($Score = 0$).
  * **Giải pháp Nhúng Ngữ nghĩa (Dense Semantic Embeddings):**
    * Chuyển đổi toàn bộ câu hỏi và nội dung các chủ điểm lý thuyết thành các vector mật độ cao (dense vectors) trong không gian ngữ nghĩa liên tục $\mathbb{R}^d$.
    * Các từ vựng đồng nghĩa, có liên quan về mặt khái niệm ngữ pháp (*interest, excited, bored* và *participle, adjective*) sẽ nằm gần nhau trong không gian vector.

> 🎤 **Lời thoại Thành viên 3 (Speaker Script):**  
> *"Tiếp theo là bài toán liên kết câu hỏi với lý thuyết ngữ pháp — một trong những điểm nhấn quan trọng nhất của đề tài mà Thầy/Cô đã định hướng cho nhóm.  
> Nếu chúng ta dùng phương pháp so khớp từ khóa truyền thống (như BM25 hay TF-IDF), thuật toán sẽ hoàn toàn bất lực. Ví dụ một câu hỏi bài tập yêu cầu điền từ 'interesting', trong toàn bộ câu hỏi không hề xuất hiện chữ 'participle' hay 'phân từ'. Khớp từ khóa sẽ cho kết quả bằng 0.  
> Để giải quyết triệt để vấn đề này, nhóm chúng em đã áp dụng phương pháp **Nhúng Vector Ngữ nghĩa (Dense Semantic Embeddings)**. Chúng em chuyển đổi cả câu hỏi và các đoạn lý thuyết vào một không gian vector đa chiều, nơi mà các khái niệm có quan hệ ngữ nghĩa sẽ tự động hội tụ về gần nhau."*

---

### SLIDE 11: KHÔNG GIAN VECTOR `all-MiniLM-L6-v2` & COSINE SIMILARITY
* **Nội dung trình chiếu:**
  * **Mô hình Nhúng:** `sentence-transformers/all-MiniLM-L6-v2` (kích thước vector $d=384$, được huấn luyện trên 1 tỷ cặp câu).
  * **Biểu diễn Toán học:**
    * Vector câu hỏi: $\mathbf{u} = \text{Embed}(\text{Question Stem} \oplus \text{Options}) \in \mathbb{R}^{384}$
    * Vector chủ điểm lý thuyết: $\mathbf{v}_j = \text{Embed}(\text{Title}_j \oplus \text{Formula}_j \oplus \text{Explanation}_j) \in \mathbb{R}^{384}$
    * Độ tương đồng Cosine:
      $$\text{Sim}(\mathbf{u}, \mathbf{v}_j) = \frac{\mathbf{u} \cdot \mathbf{v}_j}{\|\mathbf{u}\|_2 \|\mathbf{v}_j\|_2} = \frac{\sum_{i=1}^{384} u_i v_{j,i}}{\sqrt{\sum_{i=1}^{384} u_i^2} \sqrt{\sum_{i=1}^{384} v_{j,i}^2}}$$
  * **Quyết định Ghép cặp:** $\hat{j} = \arg\max_j \text{Sim}(\mathbf{u}, \mathbf{v}_j)$ với ngưỡng tự tin (Confidence Thresholding): HIGH ($\ge 0.25$), MEDIUM ($[0.15, 0.25)$), LOW ($< 0.15$).
  * **Hiệu năng:** Tốc độ suy luận chỉ 4.2ms/câu trên chip Apple Silicon Metal, hoàn toàn offline.

> 🎤 **Lời thoại Thành viên 3 (Speaker Script):**  
> *"Cụ thể về mặt kỹ thuật, nhóm sử dụng mô hình pre-trained `all-MiniLM-L6-v2`. Mỗi câu hỏi và mỗi chủ điểm ngữ pháp được mã hóa thành một vector 384 chiều.  
> Sau đó, chúng em tính toán độ tương đồng Cosine giữa vector câu hỏi và 4 vector chủ điểm lý thuyết trong bài giảng. Chủ điểm nào đạt độ tương đồng cực đại và vượt qua ngưỡng tin cậy sẽ được ghép cặp với câu hỏi đó.  
> Kết quả chạy thực nghiệm cho thấy thời gian nhúng chỉ mất 4.2 mili-giây cho mỗi câu hỏi trên chip Mac M-series, và hệ thống đã gán nhãn thành công các câu hỏi về phân từ, câu bị động và vị trí tính từ với độ chính xác rất cao, tạo nên tệp `exercise_concept_links.json` phục vụ trực tiếp cho giao diện web."*

---

### SLIDE 12: CHẨN ĐOÁN LỖI NGỮ PHÁP GEC CHUẨN ERRANT TỪ ZOOM CHAT
* **Nội dung trình chiếu:**
  * **Nguồn dữ liệu:** Tệp log Zoom chat `chat.txt` của học sinh tương tác trong giờ học.
  * **Thuật toán Phân loại Lỗi Sư phạm (ERRANT Taxonomy):**
    * Bắt 6 nhóm lỗi chuyển di ngôn ngữ (L1 Transfer) kinh điển của học viên Việt Nam:
      1. `U:VERB:BE`: Thừa động từ 'to be' do ảnh hưởng tiếng Việt (*"I am agree with A"* $\rightarrow$ *"I agree with A"*).
      2. `R:ADJ:PARTICIPLE`: Nhầm lẫn đuôi -ing và -ed (*"I am confusing"* $\rightarrow$ *"I am confused"*).
      3. `M:VERB:AUX`: Thiếu trợ động từ đảo ngữ (*"Why we use..."* $\rightarrow$ *"Why do we use..."*).
      4. `R:VERB:FORM`: Sai dạng phân từ trong cấu trúc nhờ vả causative (*"have it clean"* $\rightarrow$ *"have it cleaned"*).
      5. `U:PREP`: Thừa giới từ sau động từ khiếm khuyết (*"should to increase"* $\rightarrow$ *"should increase"*).
      6. `R:VERB:SVA`: Lỗi hòa hợp chủ vị ngôi thứ ba số ít (*"it make me cry"* $\rightarrow$ *"it makes me cry"*).
  * **Đầu ra:** Câu sửa tối thiểu (`<ins>`, `<del>`) và lời giải thích quy tắc sư phạm hoàn toàn bằng tiếng Việt.

> 🎤 **Lời thoại Thành viên 3 (Speaker Script):**  
> *"Song song với bài tập, một mỏ dữ liệu quý giá khác mà trước nay thường bị bỏ quên chính là khung chat của học sinh.  
> Nhóm chúng em đã xây dựng module **GEC Feedback** tuân thủ theo bảng phân loại lỗi quốc tế ERRANT của Đại học Cambridge. Chúng em tập trung nhận diện 6 mẫu lỗi L1 Transfer phổ biến nhất của người Việt khi học tiếng Anh, ví dụ như lỗi thừa động từ 'to be' khi nói 'I am agree', hay lỗi nhầm lẫn tai hại giữa tính từ đuôi -ing và -ed.  
> Hệ thống không chỉ đưa ra câu sửa chuẩn mà còn cung cấp lời giải thích sư phạm chi tiết bằng tiếng Việt, giúp học sinh nhận thức rõ nguyên nhân mình sai và cách khắc phục."*

---

### SLIDE 13: TRÍCH XUẤT THÔNG TIN CẤU TRÚC (BILINGUAL IE) VỚI GEMINI API
* **Nội dung trình chiếu:**
  * **Mục tiêu:** Bóc tách 4 chủ điểm ngữ pháp trọng tâm (Grammar Points) từ bản phiên mã thô của bài giảng.
  * **Kiến trúc Hybrid Neural Information Extraction:**
    * *Đường dẫn chính (Primary Path):* Gọi Gemini 3.5 Flash-Lite API với Prompt cấu trúc JSON Schema nghiêm ngặt, trích xuất: Tiêu đề ngữ pháp, Công thức, Giải thích tiếng Việt, Ví dụ minh họa, Timestamp bắt đầu giảng, và Mẹo làm bài thi TOEIC.
    * *Đường dẫn Dự phòng (Fallback Path):* Bộ phân tích dựa trên luật (Rule-based Regex Heuristics) tự động kích hoạt nếu mất kết nối mạng hoặc hết hạn mức API, đảm bảo tính liên tục 100% của hệ thống.
  * **Sản phẩm đầu ra:** Tệp `grammar_points.json` và `vocab_deep.json` làm lõi tri thức cho bài giảng.

> 🎤 **Lời thoại Thành viên 3 (Speaker Script):**  
> *"Để trích xuất được các chủ điểm ngữ pháp này một cách tự động từ văn bản lời giảng, nhóm đã áp dụng mô hình **Hybrid Neural Information Extraction**.  
> Chúng em sử dụng Gemini 3.5 Flash-Lite với cơ chế Structured Outputs để ép kiểu dữ liệu trả về đúng schema JSON gồm công thức toán học ngữ pháp, ví dụ song ngữ và mốc thời gian giảng bài.  
> Đặc biệt, để đảm bảo tính sẵn sàng cao của phần mềm trong môi trường production, nhóm đã lập trình sẵn một cơ chế Fallback bằng luật. Nếu không có kết nối Internet hoặc API bị gián đoạn, hệ thống vẫn tự động trích xuất được bộ khung lý thuyết cơ bản mà không làm crash ứng dụng.  
> Sau đây, em xin kính mời Bạn [Tên Thành viên 4] sẽ trình bày về Báo cáo Sư phạm Teacher Dashboard và trực tiếp điều phối phiên Live Demo sản phẩm."*

---

```
================================================================================
PHẦN 4: BÁO CÁO SƯ PHẠM, LIVE DEMO & ĐÁNH GIÁ CHẤT LƯỢNG (SLIDE 14 - 18)
Người trình bày: THÀNH VIÊN 4 (System & Live Demo Engineer) - Thời gian: 06 phút 00 giây
================================================================================
```

### SLIDE 14: BÁO CÁO SƯ PHẠM ĐA CHIỀU (TEACHER DASHBOARD)
* **Nội dung trình chiếu:**
  * **Dữ liệu tổng hợp:** Được tính toán tự động từ `speakers.json`, `chat_feedback.json` và `exercise_concept_links.json`.
  * **4 Khối chỉ số Sư phạm thông minh:**
    1. *Tỷ lệ thời lượng nói (TTT vs STT):* Đo lường chính xác thời lượng giáo viên nói (TTT: 100%) so với học sinh nói (STT: 0%), đưa ra khuyến nghị tăng cường gọi học sinh bật mic phát biểu ở các bài đọc dài.
    2. *Bản đồ phân bố lỗi sai (Error Distribution):* Biểu đồ trực quan chỉ rõ học sinh sai nhiều nhất ở lỗi `R:ADJ:PARTICIPLE` (28.6%) và `M:VERB:AUX` (14.3%).
    3. *Chủ điểm yếu nhất lớp (Weakest Concept Alert):* Cảnh báo đỏ chủ điểm *"Tính từ bổ nghĩa danh từ"* với 4 lượt sai tập trung.
    4. *Kế hoạch hành động 3 bước (Next-Lesson Action Plan):*
       - Khởi động 5 phút đầu giờ bằng 3 câu trắc nghiệm phân biệt đuôi `-ing` và `-ed`.
       - Nhắc lại công thức sai khiến Causative `have/get + O + V3/ed`.
       - Điều chỉnh nhịp độ, dành 3-5 phút cho học sinh tự tìm từ khóa trong Part 6.

> 🎤 **Lời thoại Thành viên 4 (Speaker Script):**  
> *"Kính thưa Thầy/Cô, toàn bộ các kết quả phân tích NLP từ giọng nói, văn bản và chat ở các bước trước không chỉ phục vụ cho học sinh ôn bài, mà còn hội tụ lại tại **Bảng điều khiển Sư phạm Teacher Dashboard**.  
> Đây chính là giải pháp giúp giáo viên giải quyết trọn vẹn bài toán quản lý lớp học:  
> Thay vì phải đọc lại từng dòng log chat, giáo viên chỉ cần nhìn vào Dashboard là thấy ngay: Hôm nay lớp học của mình có mức độ tương tác ra sao; học sinh đang vấp phải lỗi ngữ pháp nào nhiều nhất; và đặc biệt hệ thống tự động sinh ra một **Kế hoạch hành động 3 bước** cho buổi học ngày mai, hướng dẫn giáo viên nên warm-up bài gì và cần nhắc lại công thức nào.  
> Để Thầy/Cô có cái nhìn trực quan nhất, ngay sau đây em xin phép được trình chiếu Live Demo sản phẩm đang chạy thực tế trên máy chủ cục bộ."*

---

### SLIDE 15: TRÌNH DIỄN SẢN PHẨM THỰC TẾ (LIVE DEMO SHOWCASE)
* **Nội dung trình chiếu & Thao tác Demo (Kịch bản 5 bước tại `http://localhost:8000/`):**
  * **Bước 1 - Đồng bộ Đa phương thức:** Bấm vào câu hỏi bất kỳ trên Tab **Exercises** $\rightarrow$ Video tua mượt mà đến đúng giây giáo viên chữa bài; phụ đề chạy đồng bộ từng từ.
  * **Bước 2 - Liên kết Khái niệm 2 chiều:** Bấm vào **Badge màu tím** `🏷️ [Tên chủ điểm]` hoặc nút `📖 Lý thuyết (MM:SS) ➔` $\rightarrow$ Video nhảy ngược về phút thứ 08:13 lúc giáo viên giảng lý thuyết, giao diện tự động mở Tab **Grammar** và highlight viền xanh thẻ lý thuyết.
  * **Bước 3 - Từ vựng CEFR & Audio Clip:** Sang Tab **Vocabulary**, lọc cấp độ B1, bấm nút loa 🔊 $\rightarrow$ Phát đoạn audio 1.5s giọng nói thật của giáo viên.
  * **Bước 4 - Chẩn đoán Chat GEC:** Sang Tab **Chat & Feedback**, lọc `⚠️ Có lỗi sai` $\rightarrow$ Thấy câu chat của học sinh, mã lỗi `R:ADJ:PARTICIPLE`, câu sửa và giải thích tiếng Việt.
  * **Bước 5 - Teacher Dashboard & Omnibox:** Mở Tab **📊 Analytics** xem thanh TTT/STT và Kế hoạch bài học sau; bấm `Cmd+K` gõ *"participle"* để tìm kiếm tức thì trên toàn bài giảng.

> 🎤 **Lời thoại Thành viên 4 (Speaker Script):**  
> *(Thành viên 4 chuyển màn hình sang trình duyệt mở trang web `http://localhost:8000/` và thao tác trực tiếp)*  
> *"Thưa Thầy/Cô, đây là giao diện Web Demo thực tế của EduSync.  
> Đầu tiên, ở Tab Exercises bên tay phải, khi em bấm vào Câu hỏi số 1, video ngay lập tức tua đến giây thứ 181 khi giáo viên bắt đầu đọc đề. Các Thầy/Cô có thể thấy một Badge màu tím hiển thị chủ điểm ngữ pháp được gắn nhãn tự động bởi mô hình Dense Embeddings.  
> Khi em bấm vào nút 'Lý thuyết (08:13)', video lập tức tua ngược về phút thứ 8 lúc cô giáo bắt đầu giảng công thức, đồng thời hệ thống tự chuyển sang Tab Grammar và highlight đúng thẻ lý thuyết này!  
> Tiếp theo, tại Tab Vocabulary, khi lọc các từ cấp độ B1 và bấm vào biểu tượng loa cạnh từ 'distribute', chúng ta nghe thấy chính xác đoạn phát âm 1.5 giây giọng cô giáo vừa giảng trong bài.  
> Chuyển sang Tab Chat, hệ thống đã ẩn danh tên học sinh thành S1, S2 theo chuẩn FERPA và gắn nhãn các lỗi sai ngữ pháp bằng mô hình ERRANT.  
> Và cuối cùng, tại Tab Analytics, giáo viên có một bảng tổng hợp đầy đủ từ biểu đồ tương tác, phân bố lỗi sai đến kế hoạch hành động 3 bước cho buổi sau.  
> Mọi tính năng đều hoạt động với độ trễ dưới 5ms ngay trên trình duyệt mà không cần tải lại trang."*

---

### SLIDE 16: KẾT QUẢ ĐẢM BẢO CHẤT LƯỢNG (QA/QC PLAN & 45/45 TESTS PASS)
* **Nội dung trình chiếu:**
  * **Phương pháp luận Kiểm thử:** Áp dụng mô hình Test-Driven Development (TDD) với độ bao phủ toàn diện.
  * **Bảng tổng kết 45 Unit Tests trong Repository:**
    * `test_wer.py` (5 tests): Kiểm tra độ chính xác thuật toán Levenshtein WER, đo lường tỷ lệ lỗi từ.
    * `test_text_lang.py` (3 tests): Kiểm tra khả năng nhận diện tiếng Việt, tiếng Anh và ngôn ngữ hỗn hợp.
    * `test_screen_hints.py` (4 tests): Kiểm tra bóc tách từ vựng OCR và khử stop words.
    * `test_exercises.py` (4 tests): Kiểm tra bóc tách câu hỏi, khử trùng lặp và thuật toán Monotonic DP.
    * `test_vocab.py` (8 tests): Kiểm tra Lemmatization, từ điển CEFR, trích xuất nghĩa tiếng Việt và lọc homophone.
    * `test_feedback.py` (10 tests): Kiểm tra parser Zoom chat, ẩn danh FERPA và bắt 6 lỗi ERRANT.
    * `test_neural_ie.py` (4 tests): Kiểm tra schema JSON, format thời gian và cơ chế Rule Fallback.
    * `test_concept_link.py` (2 tests): Kiểm tra nhúng Dense Embeddings và tính Cosine Similarity.
    * `test_teacher_analytics.py` (2 tests): Kiểm tra tính toán TTT/STT, phân bố lỗi và sinh Action Plan.
    * `test_diarize.py` (3 tests): Kiểm tra phân vai giáo viên và học sinh.
  * **Tỷ lệ vượt qua:** **45 / 45 bài test PASSED (100%)** với thời gian chạy chỉ trong 7.5 giây.

> 🎤 **Lời thoại Thành viên 4 (Speaker Script):**  
> *"Kính thưa Thầy/Cô, để đạt được độ tin cậy cao như trong bài demo vừa rồi, nhóm em đã áp dụng quy trình kiểm chuẩn phần mềm cực kỳ nghiêm ngặt.  
> Toàn bộ pipeline hệ thống được bao phủ bởi 45 bài Unit Tests tự động bằng framework Pytest.  
> Các bài test này kiểm tra từ tính đúng đắn toán học của thuật toán Levenshtein WER, độ chính xác của bộ lemmatize hình thái, thuật toán quy hoạch động đơn điệu, cho đến độ bền vững của mô hình nhúng vector và cơ chế fallback khi gọi API.  
> Toàn bộ 45/45 bài test hiện đều đạt trạng thái PASSED 100% trên nhánh `edusync-v2` của dự án."*

---

### SLIDE 17: ĐÓNG GÓP HỌC THUẬT, HẠN CHẾ & HƯỚNG PHÁT TRIỂN
* **Nội dung trình chiếu:**
  * **Đóng góp Học thuật & Thực tiễn:**
    * Hiện thực hóa thành công mô hình học tập đa phương thức (Multimodal Learning) kết hợp âm thanh, thị giác và văn bản.
    * Đưa nghiên cứu NLP lý thuyết (Dense Embeddings, ERRANT, Contextual Prompting) vào giải quyết trực tiếp nỗi đau trong giáo dục số.
    * Xây dựng bộ tài liệu chuẩn mực IEEE/ACM trong thư mục `docs/` (từ SRS, SDD, Literature Review đến Hướng dẫn sử dụng).
  * **Hạn chế Hiện tại:**
    * Mô hình Whisper và Apple Vision OCR hiện tối ưu tốt nhất trên hệ điều hành macOS (Metal Performance Shaders).
    * Bộ dữ liệu thử nghiệm tập trung chủ yếu vào dạng bài trắc nghiệm TOEIC (Part 5 & Part 6).
  * **Hướng phát triển Tương lai:**
    * Mở rộng hỗ trợ các dạng bài tập tự luận, bài đọc hiểu dài (Part 7) và kỹ năng Nói (IELTS Speaking).
    * Triển khai mô hình nhúng đa ngôn ngữ kích thước lớn hơn (như `bge-m3`) và tích hợp cơ sở dữ liệu vector Milvus/Qdrant cho hệ thống cấp trường học.

> 🎤 **Lời thoại Thành viên 4 (Speaker Script):**  
> *"Nhìn lại toàn bộ quá trình nghiên cứu, nhóm tự hào đã hiện thực hóa được một giải pháp hoàn chỉnh từ lý thuyết NLP đến sản phẩm phần mềm thực tiễn, đóng góp một hướng đi mới cho việc ứng dụng AI vào phân tích sư phạm trực tuyến.  
> Tuy nhiên, đề tài cũng còn một số hạn chế nhất định, chẳng hạn như hiện tại hệ thống tập trung sâu vào dạng bài tập trắc nghiệm tiếng Anh.  
> Trong tương lai, nhóm dự kiến sẽ mở rộng kiến trúc này sang các dạng bài đọc hiểu phức tạp hơn của kỳ thi IELTS và tích hợp các cơ sở dữ liệu vector phân tán để có thể phục vụ đồng thời cho hàng ngàn lớp học trên toàn trường."*

---

### SLIDE 18: TỔNG KẾT & BẮT ĐẦU PHIÊN HỎI - ĐÁP (Q&A)
* **Nội dung trình chiếu:**
  * **Thông điệp Kết luận:** *"EduSync không thay thế người thầy, mà trao quyền cho người thầy và học sinh bằng sức mạnh của Trí tuệ Nhân tạo và Xử lý Ngôn ngữ Tự nhiên."*
  * **Repository & Tài liệu:**
    * Git Branch: `edusync-v2`
    * Bộ tài liệu 8 chuyên đề chi tiết: `docs/01` đến `docs/08`
    * Demo URL: `http://localhost:8000/`
  * **Lời cảm ơn:** Trân trọng cảm ơn Thầy/Cô Hội đồng và các bạn học viên đã chú ý lắng nghe!
  * **Khởi động phiên Hỏi - Đáp (Q&A Session).**

> 🎤 **Lời thoại Thành viên 4 (Speaker Script):**  
> *"Kính thưa Thầy/Cô, EduSync ra đời với tâm niệm không phải để thay thế người thầy, mà là để trao quyền cho người thầy giảng dạy hiệu quả hơn và giúp các bạn học sinh tiếp thu tri thức một cách chủ động, dễ dàng hơn.  
> Toàn bộ mã nguồn, dữ liệu mẫu và tài liệu chuẩn IEEE của đồ án đã được công khai trên GitHub của nhóm.  
> Chúng em xin trân trọng cảm ơn Thầy/Cô và các bạn đã dành thời gian theo dõi bài báo cáo. Sau đây, cả 4 thành viên trong nhóm chúng em xin sẵn sàng lắng nghe các ý kiến nhận xét và giải đáp các câu hỏi phản biện từ Thầy/Cô Hội đồng. Em xin trân trọng cảm ơn!"*

---

## 3. BẢNG DỰ ĐOÁN CÂU HỎI PHẢN BIỆN (Q&A ANTICIPATION) & PHÂN CÔNG TRẢ LỜI

| # | Câu hỏi Phản biện Dự kiến của Giảng viên | Thành viên Trả lời Chính | Hướng dẫn Trả lời Trọng tâm (Key Talking Points) |
| :-: | :--- | :---: | :--- |
| **Q1** | *"Tại sao nhóm lại dùng `sentence-transformers` mà không dùng luôn TF-IDF hoặc Elasticsearch cho nhẹ?"* | **Thành viên 3** (Core NLP) | • Giải thích hiện tượng **Vocabulary Mismatch**: Đề bài tập không bao giờ chứa từ ngữ học thuật của chủ điểm lý thuyết (*"interesting"* vs *"participle"*). TF-IDF/BM25 cho score = 0.<br>• `all-MiniLM-L6-v2` chuyển đổi sang không gian ngữ nghĩa liên tục 384 chiều, bắt được mối quan hệ khái niệm trừu tượng.<br>• Tốc độ chạy local cực nhanh (chỉ 4.2ms/câu), kích thước mô hình chỉ 80MB. |
| **Q2** | *"Làm thế nào nhóm đảm bảo tính đơn điệu của thuật toán Monotonic DP nếu giáo viên giảng bài lộn xộn, quay lại câu trước?"* | **Thành viên 2** (Alignment) | • Thuật toán thiết lập hàm mục tiêu quy hoạch động với ràng buộc $t_{k+1} > t_k$.<br>• Sử dụng cửa sổ tìm kiếm động 120s và Regex Lookbehind loại bỏ các câu nhắc lại vu vơ.<br>• Nếu giáo viên cố tình quay lại chữa một câu cũ ở cuối giờ, hệ thống ghi nhận đó là một phân đoạn thảo luận bổ sung (Discussion segment) chứ không ghi đè lên mốc chữa bài chính ban đầu. |
| **Q3** | *"Vấn đề bảo mật dữ liệu học sinh khi phân tích tin nhắn Zoom chat được xử lý như thế nào?"* | **Thành viên 1** (Project Lead) | • Tuân thủ nghiêm ngặt quy định bảo mật giáo dục FERPA và GDPR.<br>• Tệp `chat_parser.py` thực hiện cơ chế mã hóa một chiều ngay khi nạp file: Tên thật của học sinh (ví dụ: *"Nguyễn Văn A"*) lập tức được map thành $S_1, S_2, \dots$ trong bộ nhớ RAM.<br>• Không bao giờ lưu trữ tên thật của học sinh vào các file JSON đầu ra hay đẩy lên giao diện web. |
| **Q4** | *"Nếu lớp học có 100 học sinh nói qua micro cùng lúc thì hệ thống có phân tách được giọng nói (diarization) không?"* | **Thành viên 4** (System & Demo) | • Hiện tại thuật toán `diarize.py` dựa trên năng lượng âm thanh và đối chiếu với luồng chat để phân tách 2 vai chính: Teacher (T) và Student (S).<br>• Trong các lớp học trực tuyến lớn, việc học sinh tranh nhau bật mic là phản sư phạm; giáo viên thường yêu cầu học sinh chat.<br>• Hướng phát triển tiếp theo của nhóm là tích hợp mô hình PyAnnote Audio để phân tách chính xác từng học sinh nói riêng biệt. |

