# KẾT QUẢ ĐÁNH GIÁ THỰC NGHIỆM (NGUỒN SỐ LIỆU DUY NHẤT)
## EduSync — đồ án NLP501

**Cập nhật:** 10/11/2026 · **Tái tạo toàn bộ số liệu:** `python eval/run_all.py` (ghi `eval/results/*.json`, `summary.json`)

Mọi con số trong slide và các tài liệu khác phải lấy từ file này. Con số nào không có ở đây thì không được trích dẫn.

---

## 1. Dữ liệu

| Bài | Nguồn | Thời lượng | Màn hình | Đoạn lời giảng | Câu hỏi trích được | Dùng để |
|---|---|---|---|---|---|---|
| ECE TOEIC Starter Unit 4 | YouTube, CC BY | 58 phút | 32 | 2.606 | 34 (2 là đoạn văn, không phải câu hỏi) | **Phát triển** (dev): chỉnh thuật toán |
| ECE TOEIC Starter Unit 5 | YouTube, CC BY | 58 phút | 32 | 1.201 | 35 | **Kiểm tra độc lập** (test): chỉ chạy 1 lần sau khi chốt thuật toán |
| ECE TOEIC Starter Unit 1 | YouTube, CC BY | 65 phút | 46 | 1.690 | — | Chỉ dùng cho ASR/trích màn hình |
| Stanford CS224N (BERT) | YouTube + slide PDF | 54 phút | 43 slide | — | — | Kiểm tra hồi quy pipeline v1 (căn chỉnh slide) |
| **Bộ test đa nguồn**: 8 video TOEIC tiếng Việt của 6 kênh khác ECE | YouTube, CC BY | 3 giờ 9 phút | 1–62 / bài | 86–1.815 / bài | xem mục 3b | **Kiểm tra tổng quát hóa** sang giáo viên, sách, cách trình bày khác (mục 3b) |

Đặc điểm cần nói rõ khi trình bày:
- Lời giảng Unit 4: 73% đoạn tiếng Việt, 26% đoạn tiếng Anh, 5 đoạn trộn mã (phân loại theo mật độ chữ có dấu).
- **Chỉ có một người nói** (giáo viên). Vì vậy **không đo được TTT/STT**; báo cáo hiển thị "chưa đo" thay vì 100%/0%.
- **Log chat (17 tin nhắn, 5 học viên) là dữ liệu mô phỏng** do nhóm soạn để minh họa luồng chat → sửa lỗi → báo cáo; bài giảng YouTube không có chat.
- Nội dung trích từ bài giảng (đề bài, lời giảng) không đưa lên git vì đề bài lấy từ sách của nhà xuất bản (`.gitignore`).

## 2. Bộ nhãn chuẩn (gold) — đều là bản nháp, cần nhóm kiểm tra

| File | Nội dung | Ai gán | Trạng thái |
|---|---|---|---|
| `lessons/ece-toeic-starter-u4/gold/alignment_gold.json` | Mốc bắt đầu chữa của 32/34 câu + mốc giảng lý thuyết của 4 chủ điểm | AI (Claude), đọc transcript, không xem output hệ thống | `verified: false` |
| `lessons/ece-toeic-starter-u5/gold/alignment_gold.json` | Mốc bắt đầu chữa của 35/35 câu (cùng hướng dẫn gán nhãn) | AI, như trên | `verified: false` |
| `lessons/ece-toeic-starter-u4/gold/concept_gold.json` | Chủ điểm của 34 câu: gp_1..gp_4 hoặc "none" (12 câu có chủ điểm, 22 câu none) | AI, như trên | `verified: false` |
| `eval/gold/gec_heldout.json` | 70 câu kiểu chat của học viên (44 có lỗi trong 6 nhóm, 10 lỗi khác, 16 câu đúng) | AI, viết độc lập, không xem luật | `verified: false` |
| `lessons/ece-toeic-starter-u4/gold/asr/` | 5 clip × 2 phút + bản chép | Bản nháp từ ASR, **chưa sửa tay** | `corrected: false` |
| `lessons/toeic-*/gold/questions_gold.json` | Bộ test đa nguồn: danh sách câu giáo viên thực sự chữa + mốc bắt đầu, 68 câu / 8 bài (nhóm phụ: 23 câu / 2 bài) | AI, đọc transcript + OCR và **xem khung hình video**, không mở output hệ thống | `verified: false` |

**Việc nhóm cần làm trước khi bảo vệ:** mở video ở các mốc trong `alignment_gold.json` (67 câu, khoảng 1 giờ) và `questions_gold.json` (68 câu ở 8 video; mỗi câu có ghi chú lý do và mốc thay thế) và sửa chỗ sai, đọc lại 34 nhãn chủ điểm và 70 câu GEC, rồi đặt `verified: true` và chạy lại `eval/run_all.py`.

## 3. Căn chỉnh câu hỏi ↔ lời giảng (`exercise_align.py`)

Độ đo: tỉ lệ câu có mốc dự đoán lệch ≤10 s / ≤30 s so với nhãn; sai số tuyệt đối; số lần đảo thứ tự.

| Phương pháp | Dev U4: ±10 s | ±30 s | Sai số TB | Test U5: ±10 s | ±30 s | Sai số TB | Đảo thứ tự (U5) |
|---|---|---|---|---|---|---|---|
| Thời điểm màn hình xuất hiện | 18,8% | 21,9% | 91,7 s | 48,6% | 62,9% | 33,3 s | 0 |
| Regex "câu N" đầu tiên | 71,9% | 78,1% | 28,1 s | 71,4% | 80,0% | 21,3 s | 2 |
| **v1 (commit 73d9a62)** | 65,6% | 81,2% | 24,6 s | 57,1% | 71,4% | 28,5 s | 2 |
| Greedy (điểm số mới) | 68,8% | 84,4% | 10,5 s | 77,1% | 88,6% | 8,6 s | 0 |
| DP (điểm số mới) | 68,8% | 84,4% | 10,5 s | 77,1% | 88,6% | 8,6 s | 0 |
| **DP + lùi mốc (bản hiện tại)** | **68,8%** | **84,4%** | **10,0 s** | **80,0%** | **88,6%** | **8,1 s** | **0** |

Những thay đổi so với v1 (chỉnh trên U4, rồi kiểm tra trên U5):
1. Regex nhận thêm "câu thứ N", "câu hỏi số N", số đọc bằng chữ ("câu thứ tư"); loại "part N".
2. **Xác minh khẩu lệnh bằng ngữ cảnh:** "câu N" chỉ được 25 điểm nếu trong 60 s sau đó cô nói ít nhất một từ của chính câu hỏi; nếu không thì chỉ được 2 điểm. Lý do: ở U4 cô chữa Exercise A trong sách ("câu số 1, 2") trong khi màn hình chiếu Exercise B.
3. Bỏ stopword khi tính độ trùng từ.
4. **Lùi mốc về đầu đoạn chữa:** lùi qua các đoạn ngay trước đó có chung từ với câu hỏi (cô thường đọc đề trước rồi mới nói số câu).
5. Câu không khớp được rơi về thời điểm màn hình, nhưng bị kẹp giữa hai câu kề nhau, nên không còn đảo thứ tự.
6. Bộ giải mã là **quy hoạch động thật**: `D[k][j] = s(k,j) + max(0, max{D[k'][j'] : k'<k, t(j')<t(j)})`, tối ưu toàn cục và cho phép bỏ qua câu. *Trên cả hai bài, DP chọn giống greedy*; phần cải thiện đến từ cách tính điểm, bước lùi mốc và cách xử lý câu không khớp. DP chỉ khác greedy khi có xung đột (có test minh họa trong `tests/test_exercises.py`).

Lỗi còn lại chủ yếu ở các chỗ trống trong đoạn văn (Part 6/7): cô đọc liền cả đoạn nên "lúc bắt đầu câu" vốn không rõ (nhãn ghi mốc thay thế lệch 5–40 s).

**U4 và U5 cùng một giáo viên, một cuốn sách, một cách trình bày.** Con số 80,0% của U5 vì vậy chỉ cho biết hệ thống chạy tốt trên bài *cùng nguồn*; mục 3b đo trên video của giáo viên khác.

## 3b. Bộ test đa nguồn: video TOEIC tiếng Việt của giáo viên khác (`eval/eval_multisource.py`)

### Tìm video

`fetch_lesson.py` chỉ tải video có giấy phép mở (hoặc có phép của chủ sở hữu, `--allow-standard`). Nhóm đã tìm trên nhiều nền tảng:

| Nền tảng | Cách tìm | Kết quả | Dùng |
|---|---|---|---|
| YouTube | Bộ lọc Creative Commons, khoảng 30 truy vấn tiếng Việt (luyện thi / giải đề / chữa đề TOEIC, Part 1–7, ETS, ngữ pháp, từ vựng) | Khoảng 25 video TOEIC tiếng Việt có CC từ khoảng 15 kênh. Loại: kênh đăng lại bài của người khác, video chỉ phát audio đề thi trên ảnh tĩnh, bản ghi lớp học trực tuyến có giọng và tên sinh viên | **8 video, 6 kênh** |
| Vimeo | API tìm kiếm, `filter=CC` | 3 video TOEIC có CC, không phải bài chữa đề tiếng Việt; Vimeo đòi đăng nhập mới tải được. Các bài tiếng Việt ("Luyện thi TOEIC – Grammar Unit 1–6", "Chữa đề Thực chiến đề thi TOEIC") không ghi giấy phép | 0 (cần phép của tác giả) |
| Internet Archive | API `advancedsearch` | 59 mục "toeic", không mục nào là bài giảng có giấy phép CC | 0 |
| Dailymotion | API | Có vài bài tiếng Việt (TOEIC Speaking), nhưng nền tảng không có giấy phép CC; một kênh đăng lại khóa học trả phí | 0 |
| PeerTube (SepiaSearch), Wikimedia Commons | API | Không có bài TOEIC | 0 |
| MOOC / OER (PSU MOOC, VOER, OER Commons, MIT OCW) | Web | Khóa TOEIC của PSU MOOC có CC BY-NC-SA nhưng phải đăng nhập; các kho còn lại không có bài TOEIC | 0 |

Ngoài YouTube, không tìm được video bài giảng TOEIC tiếng Việt nào vừa có giấy phép mở vừa tải được. `fetch_lesson.py` nay đọc giấy phép theo cách ghi của từng nền tảng: YouTube ghi "Creative Commons…", Vimeo ghi `by-nc`, Internet Archive dùng URL `creativecommons.org`, PeerTube ghi "Attribution". Tool cũng có `--cookies-from-browser` cho trang cần đăng nhập. Khi nhóm xin được phép hoặc có tài khoản thì thêm được bài từ nguồn khác.

### Bộ test

| Bài (`lessons/…`) | Kênh (YouTube, CC BY) | Thời lượng | Thể loại | Nội dung | Số câu |
|---|---|---|---|---|---|
| `toeic-maiphuong-part4` | Cô Vũ Mai Phương Official | 59 phút | Bài giảng | Part 4, 6 bài nghe × 3 câu; slide đánh số 1–3 cho mỗi bài nghe | 18 |
| `toeic-focusrc1-part7` | learning and entertainment ¹ | 46 phút | Bài giảng | Part 7, câu 147–153 trên trang đề scan | 7 |
| `toeic-maiphuong-part2-2014` | TOEIC Cô Mai Phương ² | 23 phút | Bài giảng | Part 2, bảng phấn, phần lớn là lý thuyết | 2 |
| `toeic-ungdung-lientu` | TOEIC ứng dụng | 21 phút | Bài giảng | Part 5 (liên từ), bảng viết tay cuộn dọc; câu 116/120/105/114/140 lấy từ sách ETS/Economy | 5 |
| `toeic-enny-part4` | Enny TOEIC | 13 phút | Bài giảng | Part 4, câu hỏi suy luận | 3 |
| `toeic-tranlong-part2` | Trần Long ³ | 9 phút | Bài giảng | Part 2 "bẫy"; 7 ví dụ không đánh số + 3 câu quiz | 10 |
| `toeic-khoann-part2` | [Khoa NN] Nguyen Trung Hieu | 10 phút | Luyện tập | Audio đề Part 2 phát 2 lần, không có lời giảng | 12 |
| `toeic-khoann-part1-3` | [Khoa NN] Nguyen Trung Hieu | 8 phút | Luyện tập | Audio đề Part 1 và Part 3, không có lời giảng | 11 |

¹ Watermark "Tiếng Anh Thầy Giảng Cô Mai" khác tên kênh. ² Video là bản quay màn hình bài giảng trên moon.vn; mô tả kênh ghi đã chuyển sang kênh mới. ³ Thương hiệu TOEIC Academy / OnThiTOEIC.vn khác tên kênh. **Nhóm cần xác minh chủ sở hữu trước khi chiếu hình ảnh của ba video này.** Giấy phép CC do người đăng tự khai trên YouTube.

Hai video không phải nguồn Việt (một bài giáo viên Nhật, một quiz tiếng Anh của kênh nước ngoài; 23 câu) được giữ ở nhóm phụ `extra` và không tính vào số liệu chính. Video tiếng Thái đã bỏ.

**Nhãn** (`gold/questions_gold.json`) là danh sách câu giáo viên thực sự chữa. Mốc của mỗi câu là đầu đoạn ASR đầu tiên mà giáo viên bắt đầu làm câu đó (đọc số câu, đọc đề hoặc giải thích). Người gán không mở output của hệ thống và kiểm tra bằng khung hình video. Khác với U4/U5 (nhãn gắn vào danh sách câu do hệ thống trích), cách này **đếm được cả những câu hệ thống bỏ sót**.

**Ba phép đo:**
1. **Trích câu:** tỉ lệ câu có trong nhãn mà `exercises.py` tìm được (cùng số câu, văn bản giống ≥ 0,4).
2. **Đầu-cuối:** tỉ lệ câu lệch ≤10 s, tính trên mọi câu có nhãn; câu bị bỏ sót tính là sai.
3. **Oracle:** bộ căn chỉnh nhận danh sách câu đúng và lấy cả video làm cửa sổ tìm. Phép đo này chỉ đo phần căn chỉnh lời giảng.

"Đóng băng" là hệ thống trước khi có bất kỳ thay đổi nào dựa trên bộ này. Danh sách câu trích lúc đó được lưu ở `results/frozen/`.

### Kết quả

| | Trích câu | Đầu-cuối ±10 s | Oracle ±10 s | Oracle: sai số trung vị |
|---|---|---|---|---|
| **Bài giảng, đóng băng** (45 câu, 6 video) | 44,4% | **17,8%** (v1: 8,9%) | **57,8%** | 3,2 s |
| Bài giảng, sau khi sửa `exercises.py` | 55,6% | 26,7% (v1: 17,8%) | 57,8% | 3,2 s |
| Luyện tập (23 câu, 2 video; sửa không đổi gì) | 21,7% | 8,7% (v1: 8,7%) | 78,3% | 0,0 s |
| *Đối chiếu:* U5, cùng nguồn ECE với tập dev | 35/35 | 80,0% | — | — |

Oracle ±10 s theo phương pháp:

| Phương pháp | Bài giảng (45 câu) | Luyện tập (23 câu) |
|---|---|---|
| Regex "câu N" đầu tiên | 24,4% | 73,9% |
| v1 (commit 73d9a62) | 35,6% | 65,2% |
| Greedy + lùi mốc | 24,4% | 78,3% |
| **DP + lùi mốc (bản hiện tại)** | **57,8%** | **78,3%** |

Từng bài (sau khi sửa; số đóng băng ghi trong ngoặc nếu khác):

| Bài | Câu | Trích được | Đầu-cuối ±10 s | Oracle ±10 s | Nguyên nhân chính khi sai |
|---|---|---|---|---|---|
| `maiphuong-part4` | 18 | 17 | 27,8% | 38,9% | Cô đọc câu hỏi tiếng Anh trước khi màn hình của câu hiện ra và không nói "câu N"; số 1–3 lặp lại ở 6 bài nghe |
| `focusrc1-part7` | 7 | 5 (0) | 57,1% (0%) | 100% | Số câu 3 chữ số không được nhận (đã sửa); OCR màn hình đầu lấy nhầm trang sau |
| `maiphuong-part2-2014` | 2 | 0 | 0% | 0% | Bảng phấn viết tay; không đọc số câu |
| `ungdung-lientu` | 5 | 0 | 0% | 0% | Bảng viết cuộn nên chỉ có 1 "màn hình" cho 21 phút; thầy nói "câu này", không đọc số; đáp án (although, despite…) cũng là từ khóa của phần lý thuyết |
| `enny-part4` | 3 | 3 | 100% | 100% | — |
| `tranlong-part2` | 10 | 0 | 0% | 90,0% | Ví dụ không đánh số; OCR chỉ lấy được tiêu đề "bẫy" |
| `khoann-part2` | 12 | 2 | 8,3% | 100% | Lượt nghe đầu phát trên slide tĩnh; câu chỉ hiện trên màn hình ở lượt chữa |
| `khoann-part1-3` | 11 | 3 | 9,1% | 54,5% | Part 1 chỉ có tranh; câu Part 3 không được đọc to |

Nhóm phụ (2 video không phải nguồn Việt, 23 câu): trích câu 56,5%, đầu-cuối 34,8%, oracle DP 91,3%.

### Đọc kết quả

1. **Khoảng cách tổng quát hóa lớn.** Trên U5 hệ thống đúng 80,0%, nhưng trên video của giáo viên khác chỉ đúng 17,8% (đóng băng). Không được trình bày 80% như độ chính xác chung.
2. **Phần lớn lỗi nằm ở bước trích câu từ màn hình, không phải ở bộ căn chỉnh.** Khi có danh sách câu đúng, DP đúng 57,8% trên bài giảng và 78,3% trên luyện tập. `exercises.py` giả định đề in sẵn trên slide với số "N.". Giả định này sai với bảng viết tay, bảng cuộn, câu chỉ có tranh hoặc audio, và ví dụ không đánh số.
3. **Trên dữ liệu lạ, DP tốt hơn rõ rệt.** Với oracle trên bài giảng, DP đúng 57,8%, so với greedy 24,4%, regex 24,4% và v1 35,6%. Trên U4/U5, DP và greedy chọn giống nhau. Khi cửa sổ tìm là cả video, ràng buộc thứ tự toàn cục mới phát huy tác dụng.
4. **Bộ căn chỉnh vẫn dựa nhiều vào việc giáo viên đọc số câu.** Có ba trường hợp nó thất bại: giáo viên chỉ nói "câu này", "ví dụ này" (`ungdung-lientu`, `maiphuong-part2-2014`); giáo viên đọc câu tiếng Anh thay vì đọc số (`maiphuong-part4`); đáp án trùng từ khóa lý thuyết. Trong cả ba trường hợp, độ trùng từ không đủ phân biệt các câu. Cần tín hiệu hình ảnh, tức lúc câu xuất hiện hoặc được khoanh trên màn hình, nhưng bộ dò đổi màn hình hiện tại bỏ lỡ bảng cuộn.
5. **Những gì đã sửa sau khi xem bộ này:** `exercises.py` nhận số câu 1–3 chữ số (TOEIC đánh số 101–200) và nhãn "Number / Question / Câu N". `exercises.json` của U4/U5 không đổi. Lỗi này là lỗi tổng quát, nhưng được tìm ra nhờ bộ test, nên số "sau khi sửa" **không còn là kiểm tra độc lập**; số đóng băng mới là số độc lập. Không chỉnh trọng số hay cửa sổ căn chỉnh theo bộ này.
6. Bộ đánh giá ghép câu theo số câu và độ giống văn bản. Ở `maiphuong-part4`, một câu bị OCR bỏ sót được ghép với bản OCR trùng của một câu cùng số ở bài nghe khác. Lỗi ghép này làm tỉ lệ trích câu cao lên 1 câu, nhưng mốc thời gian của câu đó vẫn bị tính là sai.

## 4. Liên kết câu hỏi ↔ chủ điểm ngữ pháp (`concept_link.py`)

34 câu của U4, 4 chủ điểm. Câu được gắn với chủ điểm có điểm cao nhất nếu điểm ≥ ngưỡng; ngược lại là "none". Ngưỡng chọn bằng leave-one-out (mỗi câu được chấm bằng ngưỡng tối ưu trên 33 câu còn lại).

| Phương pháp | Độ chính xác (34 câu) | Link precision | Link recall | acc@1 trên 12 câu có chủ điểm |
|---|---|---|---|---|
| Luôn trả lời "none" | 73,5% | — | — | — |
| TF-IDF | 82,4% | 85,7% | 58,3% | 83,3% |
| BM25 | 70,6% | 57,1% | 41,7% | 91,7% |
| **MiniLM + từ khóa viết tay (v1)** | 76,5% | 72,7% | 58,3% | 66,7% |
| MiniLM, bỏ từ khóa viết tay | 61,8% | 33,3% | 25,0% | 50,0% |
| paraphrase-multilingual-MiniLM | 76,5% | 71,4% | 50,0% | 75,0% |
| multilingual-e5-small | 85,3% | 80,0% | 75,0% | 91,7% |
| **multilingual-e5-small + lời giảng (bản hiện tại)** | **91,2%** | **83,3%** | **83,3%** | **91,7%** |

Đầu ra thực tế (ngưỡng cố định, đúng như demo hiển thị):

| | Độ chính xác | Link precision | Link recall | Số badge |
|---|---|---|---|---|
| v1 (demo cũ) | 58,8% | 39,1% | 66,7% | 23 |
| Bản hiện tại (ngưỡng 0,835) | **91,2%** | **90,0%** | **75,0%** | 10 |

Nhận xét:
- v1 dựa vào từ khóa viết tay, trong đó có cả từ đáp án (`central`, `luxury`, `shined`…). Bỏ từ khóa thì MiniLM tụt từ 76,5% xuống 61,8%. MiniLM là mô hình chỉ tiếng Anh, trong khi phần giải thích chủ điểm bằng tiếng Việt.
- Bản hiện tại không dùng từ khóa viết tay. Nó cộng thêm **lời giảng của cô trong đoạn chữa câu** (tín hiệu đa phương thức: cô nói "thêm ing hay ed để làm tính từ", "công thức nhờ vả") và dùng mô hình đa ngữ.
- **Hạn chế:** các ví dụ trong `grammar_points.json` do Gemini sinh ra (Gemini được xem 10 câu đầu của bài), nên một số ví dụ gần như chép lại câu hỏi ("The movie was very moving.", "He has his shoes shined every day."). Điều này có lợi cho mọi phương pháp dùng văn bản chủ điểm, nên số liệu có thể lạc quan hơn trên bài mới.
- **Hạn chế:** mô hình và ngưỡng được chọn trên chính 34 câu này, nên kết quả có thể lạc quan. Điểm của hai nhóm "có chủ điểm" và "none" khá sát nhau (0,81–0,86), nên khi sang bài mới cần hiệu chỉnh lại ngưỡng. Chưa có tập kiểm tra độc lập cho bài toán này.

## 5. Mốc thời gian phần lý thuyết (`neural_ie.py --ground-only`)

Gemini chỉ thấy khoảng 30 đoạn lời giảng lấy mẫu nên mốc nó trả về là đoán. Bản hiện tại neo lại mỗi chủ điểm vào cửa sổ lời giảng (6 đoạn) giống chủ điểm nhất theo multilingual-e5-small.

| Chủ điểm | Nhãn | v1 (Gemini) | Sai số v1 | Bản hiện tại | Sai số |
|---|---|---|---|---|---|
| gp_1 Participles | 00:24 | 15:06 | 882,7 s | 00:44 | 20,0 s |
| gp_2 Causative | 15:46 | 17:14 | 88,1 s | 15:38 | 7,5 s |
| gp_3 Passive / require that | 13:16 | 55:02 | 2.505,6 s | 13:18 | 2,3 s |
| gp_4 Noun modifiers | 07:20 | 08:13 | 53,5 s | 07:35 | 14,9 s |
| **Trung bình** | | | **882,5 s** | | **11,2 s** |

## 6. Phát hiện lỗi người học trong chat (`feedback.py`)

Bộ phát hiện dựa trên luật cho 6 nhóm lỗi chuyển di L1, không phải mô hình GEC tổng quát. Đánh giá trên 70 câu viết độc lập với luật.

| | Precision (cấp câu) | Recall (cấp câu) | F1 |
|---|---|---|---|
| v1 (khớp nguyên văn câu, commit 73d9a62) | 90,0% | 20,5% | 33,3% |
| **Bản hiện tại** | **100%** | **72,7%** | **84,2%** |

| Nhóm | Nhãn ERRANT mặc định | Số câu | Precision | Recall |
|---|---|---|---|---|
| BE_VERB ("I am agree") | U:VERB:TENSE | 8 | 100% | 50,0% |
| PARTICIPLE ("the movie was moved") | R:VERB:FORM | 8 | 100% | 87,5% |
| CAUSATIVE ("have my car repair") | R:VERB:FORM | 8 | 100% | 75,0% |
| MODAL_TO ("should to increase") | U:VERB:FORM | 8 | 100% | 100% |
| SVA ("it make me cry") | R:VERB:SVA | 8 | 100% | 62,5% |
| WH_DO ("Why we use…?") | M:VERB:TENSE | 7 | 100% | 42,9% |

- Sửa đúng nguyên câu: 65,9% (44 câu chỉ có lỗi trong phạm vi). Không báo nhầm câu nào trong 10 câu có lỗi ngoài phạm vi (bộ này không bắt các lỗi đó).
- Bộ 70 câu đã được xem **một lần** để sửa 3 lỗi cài đặt (dạng rút gọn I'm/can't, cách lấy từ đứng trước trong luật SVA, động từ đa nghĩa như "like/open"). Không thêm luật mới để khớp tập này.
- **Nhãn ERRANT đã được kiểm chứng** bằng thư viện chính thức errant 3.0.2 (`eval/errant_check.py`, kết quả ở `eval/results/errant_check.txt`). errant có thể cho nhãn lân cận với các cặp câu khác (ví dụ R:MORPH cho "confusing → confused", R:OTHER cho "don't → doesn't"). Nếu cài `errant`, `feedback.py` sẽ tự gán nhãn bằng errant.
- Trên 17 tin nhắn mô phỏng của U4: phát hiện 7 lỗi trong 6 tin nhắn. Con số này không dùng để đo chất lượng vì chat được soạn kèm các lỗi mẫu.

## 7. Nhận dạng tiếng nói (ASR)

**Chưa có WER thật.** Bản chép tham chiếu của 5 clip (10 phút) chưa được sửa tay (`corrected: false`), nên mọi WER hiện tại chỉ là so ASR với ASR. Chỉ số gián tiếp (Unit 4, toàn bài):

| Cấu hình `transcribe.py` | Số đoạn | Lặp liên tiếp | Từ trên màn hình được nói ra (proxy) |
|---|---|---|---|
| Không gợi ý (đang dùng làm `transcript.json`) | 2.606 | 6 | 47% |
| Cắt theo màn hình, không gợi ý (đối chứng) | 545 | 3 | 48% |
| Gợi ý từ OCR (hotwords = từ) | 484 | 20 | 52% |
| Gợi ý từ OCR (hotwords = dòng) | 559 | 27 | 52% |

- Gợi ý từ màn hình tăng proxy thêm khoảng 4 điểm so với đối chứng, nhưng **làm tăng số đoạn lặp** (một dấu hiệu ảo giác). Proxy này cũng có thể tăng do Whisper "chép" từ gợi ý dù cô không nói. Vì vậy chưa kết luận được, và pipeline vẫn dùng bản không gợi ý.
- Gợi ý được truyền qua tham số `hotwords` của faster-whisper, không phải `initial_prompt`.
- Việc cần làm: sửa tay 5 clip trong `gold/asr/`, đặt `"corrected": true`, chạy `python eval/wer.py --lesson lessons/ece-toeic-starter-u4 results/asr_none.json results/asr_chunks.json results/asr_words.json`.
- **Lọc tiếng nói (VAD) dưới nhạc nền.** Trên video giáo viên Nhật (nhóm phụ của mục 3b), Silero VAD chỉ giữ 5% audio vì nhạc nền to. ASR chỉ ra **1 đoạn** cho 5 phút giảng; tắt VAD thì ra 91 đoạn. `transcribe.py --vad auto` (mặc định) nay tự tắt VAD khi VAD giữ dưới 25% audio. U1/U4/U5 có tỉ lệ giữ 97%, các video tiếng Việt của mục 3b từ 66% đến 99%, nên transcript của các bài đó không đổi.
- Nhãn ngôn ngữ của đoạn (`vi` / `en` / `mixed`) dựa vào chữ có dấu tiếng Việt, nên lời giảng bằng tiếng Nhật bị gắn `en`. Nhãn này chỉ dùng được cho bài giảng Việt–Anh.

## 7b. Từ vựng (`vocab.py`) — chỉ có thống kê, chưa đánh giá chất lượng

- Unit 4: 80 từ, gồm A1 26, A2 26, B1 18, B2 9, C1 1 (tra từ điển CEFR-J + Octanove, 8.845 mục).
- 52/80 từ có nghĩa tiếng Việt khai thác từ lời giảng theo mẫu "X là / nghĩa là …". Độ đúng của các nghĩa này **chưa được kiểm tra**.
- 79 clip phát âm `.wav` dài 0,7–2,2 s, cắt theo ranh giới đoạn ASR có chứa từ (ưu tiên đoạn chỉ có một từ). Transcript không có timestamp từng từ.

## 8. Kiểm thử hồi quy & phần mềm

- CS224N (pipeline v1 căn chỉnh slide PDF): 9/10 mốc chuyển slide có nhãn được tìm thấy, sai số trung bình 0,6 s (`python evaluate.py --lesson lessons/cs224n-bert gold/labels.json alignment.json`).
- `pytest`: **75/75 test** pass. Test không còn ghi vào `lessons/` (dùng `tmp_path`).
- Lỗi phần mềm tìm thấy khi chạy pipeline trên bộ đa nguồn, đều đã sửa:
  - `neural_ie.py` crash khi Gemini lỗi mà từ vựng không có mốc thời gian (đã có test hồi quy);
  - `feedback.py` dừng khi bài không có log chat; nay bước này được bỏ qua an toàn.

## 9. Các con số đã rút khỏi tài liệu cũ

| Khẳng định cũ | Lý do rút |
|---|---|
| WER thuật ngữ 18,4% → 9,2%, "triệt tiêu ảo giác" | Không có kết quả đo nào trong repo; bản tham chiếu chưa sửa; số đoạn lặp tăng khi có gợi ý |
| Recall 34/34 (100%), Precision 97,1%, sai số ≤1,8 s | "34/34" chỉ là độ phủ (câu nào cũng có mốc), không có nhãn để đo; 97,1% mâu thuẫn với recall 100%; sai số thật được báo ở mục 3 |
| 4,2 ms/câu | Chưa từng được đo |
| Bắt đúng 6/6 lỗi (100%) | Chat được soạn khớp đúng với regex; nay thay bằng tập 70 câu độc lập (mục 6) |
| U:VERB:BE, R:ADJ:PARTICIPLE, M:VERB:AUX, U:PREP, "ERRANT (ACL 2019)" | Không phải nhãn ERRANT; ERRANT là ACL 2017; nhãn hiện tại kiểm chứng bằng errant 3.0.2 |
| TTT 98,2% / 100%, STT 1,8% / 0% | Bản ghi có một người nói nên không đo được |
| "Chuẩn FERPA" | FERPA là luật Mỹ về hồ sơ học vụ; hệ thống chỉ ẩn danh hoá tên (S1…SN) |
| Kế hoạch hành động "tự động sinh" | Trước đây là văn bản viết sẵn; nay là câu mẫu điền từ dữ liệu (lỗi, chủ điểm, TTT) |
| "Tỷ lệ căn chỉnh 95,6%" trong demo | Giá trị viết cứng trong `demo/index.html`; nay hiển thị số câu khớp được với lời giảng (33/34) |
| Video 63 phút; 79 từ vựng (A1 28/A2 19/B1 18/B2 12/C1 2) | Thực tế 58 phút; `vocab.json` có 80 từ (A1 26/A2 26/B1 18/B2 9/C1 1) |
| 4.950 dòng code | Trước khi sửa: 3.456 dòng Python (cả test). Hiện tại: 4.559 dòng Python (code + test + eval), 6.566 dòng nếu tính `demo/index.html` |
