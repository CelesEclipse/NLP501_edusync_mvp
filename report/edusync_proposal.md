# EduSync: đề xuất chủ đề nhóm

> **Đồng bộ video bài giảng với slide, và liên kết từng slide tới đúng mục trong tài liệu gốc**

NLP501 · [Tên nhóm] · [Thành viên] · Tháng 11/2026

---

## 1. Vấn đề: sinh viên mất thời gian ở ba chỗ

| | Nỗi đau | Ví dụ |
|---|---|---|
| 1 | **Slide quá cô đọng** | Vài gạch đầu dòng, công thức, sơ đồ vắn tắt. Đọc một mình khó hiểu bản chất. |
| 2 | **Video quá dài** | Lời giảng dài 1–3 giờ. Muốn ôn slide 15 phải tua mò từ phút 20 đến phút 60. |
| 3 | **Trích dẫn không chỉ chỗ đọc** *(hướng mới)* | Slide ghi "(Liu et al, 2019)", nhưng bài báo dài hàng chục trang: đọc mục nào? |

Nỗi đau 1 và 2 là của chủ đề ban đầu. Nỗi đau 3 là hướng thầy gợi ý.

---

## 2. Ý tưởng: mỗi slide là một nút tri thức

Mỗi slide được nối với ba nguồn, và các ứng dụng học tập được dựng trên những nút này.

```
   VIDEO                         SLIDE                        TÀI LIỆU GỐC
   11:44 – 13:14     ◄────►      Slide 13: "Masked LM"   ◄────►   BERT §3.1 › Task #1: Masked LM
   (đoạn thầy giảng,             (chữ, ảnh, khái niệm)          (đúng đoạn trong bài báo,
    kèm lời giảng)                                               link có anchor)
                                      │
                    ┌─────────────────┴─────────────────┐
                    ▼                                   ▼
            Sổ tay bài giảng                  Hỏi đáp có dẫn chứng
       (tóm tắt, khái niệm, đọc thêm)    (trích slide · giây video · mục bài báo)
```

Ví dụ trên lấy từ bài giảng thật (CS224N, BERT):
- Hệ thống hiện tại đã tìm ra slide 13 bắt đầu ở **11:44**.
- Hiện đã trỏ được tới **trang 4** của bài BERT (nơi có mục 3.1). Trỏ tới đúng đoạn "Task #1" là mục tiêu của Trụ cột 2.

---

## 3. Đề tài đề xuất

**Tiếng Việt:** EduSync – Đồng bộ đa phương thức video bài giảng với slide, và liên kết tri thức học thuật cho từng slide

**Tiếng Anh:** EduSync – Multimodal Slide–Video Alignment and Slide-to-Literature Grounding for Lecture Study

**Mục tiêu:** bấm vào một slide thì video tua tới đúng giây thầy bắt đầu giảng slide đó (và ngược lại); mỗi slide trỏ tới đúng section, figure hoặc table trong bài báo gốc; từ đó sinh sổ tay bài giảng và hỏi đáp có dẫn chứng.

**Câu hỏi nghiên cứu:**

| | Câu hỏi |
|---|---|
| **RQ1 – Đồng bộ** | Trộn hình ảnh video với lời giảng có giúp căn chỉnh slide chính xác và bền hơn so với chỉ dùng văn bản không? |
| **RQ2 – Liên kết** | Có thể tự động trỏ mỗi slide tới đúng section, figure, table trong tài liệu gốc không? Lời giảng giúp được bao nhiêu? |
| **RQ3 – Ứng dụng** | Sổ tay và hỏi đáp dựng trên các liên kết này có trích dẫn đúng và trung thực không? |

---

## 4. Ba trụ cột và mức độ hoàn thành

| Trụ cột | Làm gì | Trạng thái |
|---|---|---|
| **1. Đồng bộ đa phương thức** | Slide ↔ video, chính xác tới từng giây | **Đã làm.** Sai số trung bình 0,6 s |
| **2. Liên kết tài liệu gốc** | Slide → section / đoạn / figure / table trong bài báo và giáo trình | **Một phần.** Mới liên kết ở cấp tài liệu và cấp trang |
| **3. Bộ công cụ học tập** | Sổ tay bài giảng, hỏi đáp có dẫn chứng | **Kế hoạch** |

---

## 5. Dữ liệu thử nghiệm

| Hạng mục | Giá trị |
|---|---|
| Bài giảng | Stanford CS224N (2020), "BERT and Other Pre-trained Language Models", Jacob Devlin |
| Video | 54 phút, 1080p, chiếu slide toàn màn hình |
| Slide | 43 trang PDF; 19 trang có ảnh chèn sẵn (hình, bảng); 4 trang là sơ đồ giảng viên tự vẽ |
| Lời giảng | 1297 đoạn (faster-whisper `small`) |
| Nhãn | 10 nhãn tay (thời điểm bắt đầu slide) + 39 nhãn tự động sinh từ video |
| Tài liệu | 24 mục: 17 bài báo arXiv (đều có bản HTML ar5iv) + 7 giáo trình, bài hướng dẫn |

---

## 6. Trụ cột 1: đồng bộ video và slide (đã làm)

### 6.1 Cách làm

```
Lời giảng:  âm thanh → Whisper → cửa sổ 30 s → độ giống với chữ slide (TF-IDF / bge)  ─┐
                                                                                        ├─► chuẩn hoá z-score theo slide
Hình ảnh:   khung hình mỗi 2 s → ảnh thu nhỏ 96×54 → tương quan chéo với ảnh slide  ──┘    trộn: 1,0 × hình + 0,5 × lời
                                                                                              │
                                     quy hoạch động: slide chỉ đứng yên hoặc tiến lên  ◄──────┘
                                                      │
                                                      ▼
                                        giây bắt đầu của mỗi slide
```

- Lúc camera quay giảng viên (khoảng 12% thời lượng), khung hình không khớp slide nào. Khi đó hình ảnh bị bỏ qua và lời giảng quyết định.
- Phần hình ảnh không cần mô hình hay GPU, chạy khoảng 35 giây cho cả video.

### 6.2 Kết quả trên 10 nhãn tay

| Chỉ số | MVP gốc (chỉ lời giảng) | Hiện tại (video + lời giảng) |
|---|---|---|
| Số slide tìm được | 9/10 | 9/10 |
| Sai số trung bình / trung vị | 21,7 s / 16,2 s | **0,6 s / 1,0 s** |
| Số slide lệch ≤ 5 s | 2/10 | **9/10** |
| Sai số khi tính cả slide bị sót | 23,1 s | **2,7 s** |
| Số slide bấm được trong demo | 32/43 | **42/43** |
| Tỉ lệ thời lượng video hiển thị đúng slide* | 61,0% | 99,4% |

\* Tham chiếu của dòng này sinh từ chính tín hiệu video, nên chỉ để tham khảo.

Slide 42 là slide phân mục không bao giờ được chiếu lên màn hình. Nhãn 52:36 nhiều khả năng thuộc slide 43, cần kiểm tra lại.

### 6.3 Slide ít chữ không còn là điểm mù

Đây là vấn đề thầy chỉ ra trong MVP: slide thuần hình, sơ đồ và slide phân mục có ít hoặc không có chữ, khiến thuật toán chỉ dùng văn bản thất bại.

| Loại slide | Slide | MVP gốc | Hiện tại |
|---|---|---|---|
| Tiêu đề, phân mục | 1, 37 | 0/2 tìm được | **2/2**, lệch 0 s |
| Sơ đồ | 5, 6, 7, 12, 18, 19 | 4/6, lệch trung vị 10 s | **6/6**, lệch 0 s |
| Bảng, biểu đồ | 20, 22, 23, 24, 30, 40 | 6/6, lệch trung vị 52 s | **6/6**, lệch 0 s |

Lưu ý: bảng này đo trên nhãn tự động sinh từ video. Cần thêm 10–15 nhãn tay theo từng loại slide để khẳng định chính thức.

### 6.4 Độ bền: khi camera rời slide, lời giảng giữ hệ thống đứng vững

Mô phỏng: che ngẫu nhiên các khối 60 s của hình ảnh, lấy trung bình 3 lần chạy, chấm trên 10 nhãn tay (sai số có tính slide bị sót).

| Phần hình bị che | Chỉ video | Video + lời giảng |
|---|---|---|
| 0% | 0,7 s | 2,7 s |
| 25% | 3,3 s | 4,6 s |
| 50% | 29,5 s | **11,7 s** |
| 75% | 107,6 s | **24,2 s** |
| 90% | 468,2 s | **33,4 s** |

- Chỉ dùng video thì hệ thống sụp đổ khi mất từ nửa số hình trở lên.
- Có thêm lời giảng thì sai số tăng từ từ, tiến về mức của phương pháp chỉ dùng văn bản (khoảng 35 s).
- Đây mới là mô phỏng, cần kiểm chứng trên một video thật mà camera thường rời slide.

---

## 7. Trụ cột 2: liên kết slide tới đúng mục trong tài liệu gốc

### 7.1 Hiện có và mục tiêu

| Hiện có | Mục tiêu |
|---|---|
| 24 tài liệu; 17 bài arXiv lấy thẳng từ API (tiêu đề, tác giả, tóm tắt chính xác) | Tự phát hiện khái niệm trên từng slide |
| 22 liên kết "cited": slide nhắc tên bài nào thì trỏ đúng bài đó | Trỏ tới **section, đoạn, figure, table** (equation nếu có) |
| Liên kết "related" ở cấp trang (bài BERT) | Link ar5iv có anchor: bấm vào là tới đúng chỗ |
| Chuẩn hoá z-score sửa thiên lệch: trước đó bài BERT đứng đầu 36/38 slide | Mỗi liên kết kèm bằng chứng giải thích vì sao |

Ví dụ link đích (đã kiểm tra, mở ra đúng đoạn "Task #1: Masked LM"):
`https://ar5iv.labs.arxiv.org/html/1810.04805#S3.SS1.SSS0.Px1`

### 7.2 Bốn bước

| Bước | Nội dung | Căn cứ đã kiểm tra |
|---|---|---|
| **1. Tách bài báo** | Từ ar5iv HTML lấy ra section, đoạn, figure (kèm ảnh), table, equation (mã LaTeX) | 17/17 bài chuyển đổi không lỗi; anchor tới cấp đoạn |
| **2. Phát hiện khái niệm** | Chữ slide + OCR ảnh trong slide + **lời giảng của đúng đoạn video**; lọc theo từ vựng của bài báo để không bịa khái niệm | Lời giảng đã có nhờ Trụ cột 1 |
| **3. Tìm và xếp hạng** | Ưu tiên bài được trích dẫn → tìm bằng bge + z-score → xếp hạng lại bằng cross-encoder | Phần phát hiện trích dẫn đã cho 22 liên kết đúng |
| **4. Bằng chứng và từ chối** | Ghép figure bằng ảnh (SIFT/ORB); so con số trong bảng; điểm thấp thì không liên kết | 19 slide có ảnh trích thẳng từ PDF |

Lời giảng do Trụ cột 1 tạo ra là đầu vào của bước 2, nên hai trụ cột bổ trợ nhau.

### 7.3 Ví dụ: slide dùng lại hình của bài báo

![Slide 18: Fine-Tuning Procedure](../demo/slides/slide_18.png)

*(Ảnh cần chạy `demo/prepare.py` trước mới hiển thị.)*

Slide 18 chính là **Figure 1** của bài BERT (`#S2.F1`). Các cặp khác dự kiến sẽ xác nhận khi gán nhãn:

| Slide | Đơn vị trong bài BERT | Trạng thái |
|---|---|---|
| 18 Fine-Tuning Procedure | Figure 1 `#S2.F1` | Đã đối chiếu bằng mắt |
| 16 Input Representation | Figure 2 `#S3.F2` | Dự kiến |
| 14 Masked LM (80/10/10) | Table 8 `#A3.T8` (ablation các cách mask) | Dự kiến |
| 22 Effect of Pre-training Task | Table 5 `#S5.T5` | Dự kiến |
| 23 Directionality & Training Time | Figure 5 `#A3.F5` | Dự kiến |
| 24 Effect of Model Size | Table 6 `#S5.T6` | Dự kiến |

---

## 8. Trụ cột 3: sổ tay bài giảng và hỏi đáp có dẫn chứng (kế hoạch)

### 8.1 Sổ tay bài giảng (minh hoạ)

Mỗi slide có một mục, sinh tự động từ lời giảng đã căn chỉnh và kết quả liên kết. Xuất ra Markdown hoặc PDF, mọi link bấm được về video và bài báo.

> **Slide 13 · Masked LM** · ▶ 11:44 – 13:14
>
> **Ý chính**
> - Che ngẫu nhiên k% từ đầu vào rồi dự đoán các từ bị che; BERT dùng k = 15%.
> - Che quá ít thì tốn công huấn luyện; che quá nhiều thì thiếu ngữ cảnh.
>
> **Khái niệm:** Masked LM · token [MASK] · ngữ cảnh hai chiều
>
> **Đọc thêm:** BERT §3.1 › Task #1: Masked LM · BERT Phụ lục A.1

### 8.2 Hỏi đáp có dẫn chứng ba chiều (minh hoạ)

> **Hỏi:** Vì sao BERT không thay tất cả các từ được chọn bằng [MASK]?
>
> **Đáp:** Vì token [MASK] không bao giờ xuất hiện lúc fine-tune. BERT chọn 15% từ để dự đoán; trong số đó 80% thay bằng [MASK], 10% thay bằng một từ ngẫu nhiên, 10% giữ nguyên.
>
> **Dẫn chứng:** `Slide 14` · `Video 13:14` · `BERT §3.1` · `BERT Table 8`

- **Dẫn chứng ba chiều:** mỗi câu trả lời trích slide, giây trong video và mục trong bài báo; bấm vào là nhảy tới.
- **Hai chiều:** từ câu hỏi tìm tới slide và video; từ một slide gợi ý các câu hỏi liên quan.
- **Truy xuất theo nút tri thức:** mỗi nút gồm slide, lời giảng và các đơn vị tài liệu đã liên kết.
- **Chống bịa:** chỉ trả lời từ nội dung đã truy xuất; nếu không đủ căn cứ thì trả lời "không biết".

---

## 9. Kế hoạch đánh giá

| Trụ cột | Câu hỏi | Thang đo | Nhãn cần có |
|---|---|---|---|
| Đồng bộ | Slide bắt đầu đúng giây không? | Sai số trung bình, trung vị; % lệch ≤ 5 s; sai số có tính slide bị sót | 10 nhãn có sẵn + 10–15 nhãn tay theo loại slide |
| Liên kết | Trỏ đúng mục không? | Hit@1, Hit@3, MRR; đúng bài → đúng section → đúng đơn vị | 25 slide gán đơn vị đúng |
| Hỏi đáp | Trả lời đúng và dẫn đúng không? | Độ chính xác trích dẫn, độ trung thực, từ chối đúng lúc | 30–50 câu hỏi có đáp án |

**Thí nghiệm then chốt:** so sánh truy vấn chỉ dùng chữ slide với truy vấn dùng chữ slide + lời giảng. Kết quả sẽ cho thấy Trụ cột 1 giúp Trụ cột 2 được bao nhiêu (trả lời RQ2).

---

## 10. Lộ trình 4 tuần

| Tuần | Công việc | Mốc kiểm tra |
|---|---|---|
| 1 | Bộ nhãn (đồng bộ + liên kết); tách 17 bài báo từ ar5iv; trích ảnh và OCR slide | Có bộ nhãn và dữ liệu đơn vị tài liệu |
| 2 | Phát hiện khái niệm; liên kết cấp mục; các thí nghiệm so sánh đầu tiên | Liên kết chạy hết pipeline, có số Hit@k |
| 3 | Ghép figure và bảng; sổ tay bài giảng; hỏi đáp bản đầu | Sổ tay cho cả 43 slide |
| 4 | Đánh giá hỏi đáp; bài giảng thứ hai; demo và báo cáo | Bản nộp |

**Hạn nộp:** [__/__]. Nếu gấp, bỏ phần equation, giáo trình SLP3 và bài giảng thứ hai.

---

## 11. Phân công gợi ý

| Mảng | Người phụ trách | Việc chính |
|---|---|---|
| A. Đồng bộ và đánh giá | [Thành viên 1] | Nhãn tay theo loại slide; bài giảng thứ hai; thí nghiệm độ bền |
| B. Tài liệu và liên kết | [Thành viên 2] | Parser ar5iv; tìm kiếm + cross-encoder; bộ nhãn liên kết |
| C. Hình ảnh và OCR | [Thành viên 3] | Trích ảnh slide, OCR; ghép figure, so con số trong bảng |
| D. Ứng dụng | [Thành viên 4] | Sổ tay bài giảng; hỏi đáp có dẫn chứng; demo |

Nếu nhóm ít người hơn: gộp C vào B, và D vào A.

---

## 12. Rủi ro và cách xử lý

| Rủi ro | Cách xử lý |
|---|---|
| Mới có một bài giảng, mà video chiếu slide toàn màn hình (trường hợp dễ) | Thêm bài giảng có camera hay rời slide; dùng ghép điểm đặc trưng cho slide chiếu chéo góc |
| Bộ nhãn nhỏ, chỉ một người gán | Viết hướng dẫn gán nhãn; người thứ hai gán lại 10 slide để đo mức đồng thuận |
| Bài giảng này gần như không có công thức | Ghi equation là ngoài phạm vi, hoặc thêm một bài giảng nhiều toán |
| Sổ tay và hỏi đáp dùng LLM có thể bịa nội dung | Chỉ trả lời từ nội dung đã truy xuất, bắt buộc trích dẫn, đo độ trung thực |
| Bản quyền bài báo và video | Chỉ lưu đệm trên máy, chia sẻ bằng đường dẫn |

---

## 13. Cần nhóm chốt

1. **Tên và phạm vi đề tài:** giữ cả ba trụ cột? Equation và giáo trình SLP3 để làm phần mở rộng?
2. **Hạn nộp** và **người phụ trách** từng mảng.
3. **LLM cho sổ tay và hỏi đáp:** gọi API hay dùng mô hình mở chạy trên máy (cân nhắc chi phí và khả năng chạy lại cho cùng kết quả)?
4. **Bài giảng thứ hai:** ưu tiên video mà camera hay rời slide, để kiểm chứng RQ1.
