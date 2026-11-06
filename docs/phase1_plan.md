# Phase 1: hạ tầng theo buổi học và xử lý tiếng nói

Thời gian: tuần 0–1 (khoảng 8 ngày làm việc). Thuộc lộ trình [esl_roadmap.md](esl_roadmap.md): hạ tầng + WP1.

## Mục tiêu

1. Pipeline chạy theo từng buổi học (`lessons/<id>/`) thay cho các file cố định ở thư mục gốc.
2. Transcript cho lời giảng chen Việt–Anh, mỗi đoạn có: ngôn ngữ, slide đang chiếu, người nói, mốc thời gian theo từ.
3. Bộ đo cho tiếng nói: WER, tỉ lệ nhận đúng từ tiếng Anh mục tiêu, DER.
4. Một buổi học đóng vai có nhãn chuẩn để đo.

**Không làm trong phase này:** phân đoạn giai đoạn, hành động lời nói, bài tập, từ vựng, phản hồi (phase 2–4).

## Căn cứ kỹ thuật đã kiểm tra (06/11/2026)

| Hạng mục | Kết quả |
|---|---|
| faster-whisper 1.2.1 (đang cài) | Có `multilingual` (ngôn ngữ theo đoạn), `hotwords`, `clip_timestamps`, `word_timestamps`, `initial_prompt` |
| PhoWhisper (`vinai/PhoWhisper-small`, `-medium`) | Công khai, định dạng transformers → chuyển sang CTranslate2 bằng `ct2-transformers-converter` (đi kèm ctranslate2) |
| `pyannote/speaker-diarization-3.1` | Model gated: cần tài khoản Hugging Face, chấp nhận điều khoản, đặt biến `HF_TOKEN` |
| `BAAI/bge-m3` | Công khai (dùng ở phase sau cho truy xuất Việt–Anh) |

## Cấu trúc thư mục sau phase 1

```
lessons/
  cs224n-bert/                 dữ liệu v2 chuyển vào đây (kiểm thử hồi quy)
    lesson.json  slides.pdf  slides.json  visual.npz  slide_align.json  transcript.json
    gold/labels.json
  roleplay-01/                 buổi đóng vai của nhóm
    video.mp4  slides.pdf  worksheet.pdf  chat.txt  audio/        (gốc, không đưa vào git)
    lesson.json  audio.wav  chat.json  slide_align.json  transcript.json  speakers.json
    gold/transcript_ref.json  gold/terms.json  gold/speakers_ref.rttm
pipeline.py                    chạy tuần tự các bước cho một buổi học
ingest.py  transcribe.py  diarize.py  visual.py  align.py  ...
eval/wer.py  eval/terms.py  eval/der.py
annotation/guidelines.md
tools/convert_phowhisper.sh
tests/
private/                       bảng đối chiếu tên thật (gitignore)
```

**Quy ước:**
- Mọi script nhận `--lesson <thư mục>` (mặc định `.`, để các lệnh cũ vẫn chạy) và đọc/ghi tên file chuẩn trong đó.
- `python pipeline.py lessons/<id>` chạy các bước còn thiếu đầu ra; `--force <bước>` để chạy lại một bước.
- `.gitignore` thêm: `lessons/*/video.*`, `lessons/*/audio/`, `lessons/*/audio.wav`, `lessons/*/chat.txt`, `private/`.

## Định dạng dữ liệu

**`lesson.json`**
```json
{"id": "roleplay-01", "title": "Present perfect", "level": "B1",
 "language": {"instruction": "vi", "target": "en"},
 "files": {"video": "video.mp4", "slides": "slides.pdf", "worksheet": ["worksheet.pdf"],
           "chat": "chat.txt", "audio_tracks": ["audio/S1.m4a"]},
 "duration": 2712.4, "fps": 30.0,
 "participants": [{"id": "T", "role": "teacher"}, {"id": "S1", "role": "student"}]}
```

**`transcript.json`** (mỗi phần tử là một đoạn; các trường mới so với v2: `lang`, `slide`, `speaker`, `words`)
```json
{"start": 12.3, "end": 15.8, "text": "Hôm nay mình học present perfect nhé",
 "lang": "vi", "slide": 4, "speaker": "T",
 "words": [{"w": "present", "start": 13.9, "end": 14.3, "p": 0.91}]}
```

**`speakers.json`**
```json
{"source": "pyannote|tracks|manual",
 "turns": [{"start": 0.0, "end": 41.2, "speaker": "T"}],
 "roles": {"T": "teacher", "S1": "student"}}
```

**`chat.json`**
```json
[{"t": 312.0, "speaker": "S2", "text": "I have went to Da Nang"}]
```

## Công việc

### T1. Chuyển sang cấu trúc theo buổi học (0,5–1 ngày)
- Thêm `--lesson` cho `parse_slides.py`, `visual.py`, `align.py`, `evaluate.py`, `make_labels.py`,
  `link_materials.py`, `demo/prepare.py`.
- `git mv` dữ liệu CS224N vào `lessons/cs224n-bert/`.
- Viết `pipeline.py`: danh sách bước (đầu vào, đầu ra, lệnh), bỏ qua bước đã có đầu ra.
- **Xong khi:** `python pipeline.py lessons/cs224n-bert` rồi `evaluate.py` cho lại đúng số v2
  (9/10 slide, sai số trung bình 0,6 s).

### T2. `ingest.py` (1 ngày)
- Kiểm tra thư mục buổi học, nhận diện file theo tên và đuôi.
- Đọc thời lượng, fps bằng OpenCV.
- Tách âm thanh 16 kHz mono thành `audio.wav` bằng PyAV (đã cài), dùng chung cho ASR và tách người nói.
- Đọc chat của Zoom và Meet. Viết parser dựa trên **file chat mẫu thật** (định dạng đổi theo phiên bản);
  không nhận ra định dạng thì báo lỗi rõ ràng.
- Ẩn danh: thay tên người tham gia bằng `T`, `S1`, `S2`…; bảng đối chiếu tên thật ghi vào `private/names.json`.
- Ghi `lesson.json`, `chat.json`.
- **Xong khi:** chạy được trên `cs224n-bert` (không có chat) và `roleplay-01`; có test cho parser chat.

### T3. Nâng cấp `transcribe.py` (2 ngày)
- **Thứ tự mới:** `visual.py` → `align.py --method none` → `transcribe.py`. Căn chỉnh bằng hình ảnh không cần
  transcript, nên biết trước slide nào đang chiếu ở từng giây.
- Với mỗi đoạn slide: `clip_timestamps=[start, end]`, `hotwords` = các từ tiếng Anh trên slide đó (bỏ stopword,
  giữ từ từ 3 ký tự, ưu tiên thuật ngữ; tối đa khoảng 30 từ để không vượt độ dài prompt).
- `multilingual=True` để có ngôn ngữ theo đoạn; `word_timestamps=True`.
- Ghi `lang`, `slide`, `words` vào từng đoạn.
- Cờ cho thí nghiệm: `--no-slide-hotwords`, `--model small|medium|large-v3`, `--backend whisper|phowhisper`.
- `tools/convert_phowhisper.sh`: chuyển PhoWhisper sang CTranslate2 (int8). Biến thể E5 chạy lại các đoạn
  `lang=vi` bằng PhoWhisper; không bật mặc định.
- Kiểm tra sớm trên một đoạn 2–3 phút rằng `multilingual=True` cho ngôn ngữ từng đoạn như mong đợi; nếu không,
  dự phòng bằng cách phát hiện ngôn ngữ riêng cho từng đoạn VAD.
- **Xong khi:** transcript có đủ trường mới; bản CS224N (toàn tiếng Anh) không kém bản v2 (WER trên 5 phút
  sửa tay không tăng).

### T4. `diarize.py` (1–1,5 ngày)
- **Nguồn A – âm thanh riêng từng người (Zoom):** VAD trên từng track → lượt nói; tên track → mã ẩn danh.
- **Nguồn B – pyannote 3.1** trên `audio.wav` (cần `HF_TOKEN`), có `--num-speakers` nếu biết trước.
- Gán vai: giáo viên = người nói nhiều nhất; ghi đè được trong `lesson.json`.
- Gắn người nói vào transcript: mỗi từ lấy người nói có thời gian chồng lấn lớn nhất; tách đoạn nếu đổi người
  giữa đoạn.
- Ghi `speakers.json`, cập nhật trường `speaker` trong transcript.
- **Xong khi:** chạy được nguồn A hoặc B trên `roleplay-01`; có test cho hàm gắn người nói.

### T5. Bộ đo `eval/` (1 ngày)
- `eval/wer.py`: chuẩn hóa (chữ thường, bỏ dấu câu, giữ dấu tiếng Việt); WER tổng và theo ngôn ngữ; dùng `jiwer`.
- `eval/terms.py`: với mỗi từ tiếng Anh mục tiêu trong nhãn (từ, thời điểm), kiểm tra transcript có từ đó trong
  ±2 s → tỉ lệ nhận đúng. Đo thêm **từ bị chèn sai**: hotwords có thể khiến Whisper "nghe thấy" từ trên slide dù
  giáo viên không nói.
- `eval/der.py`: DER theo khung 10 ms, bỏ qua 0,25 s quanh mỗi ranh giới lượt nói.

### T6. Nhãn và dữ liệu (song song từ ngày 1, khoảng 2 ngày công)
- `annotation/guidelines.md` cho ba loại nhãn của phase 1: transcript chuẩn, từ mục tiêu, lượt người nói.
- Buổi đóng vai: kịch bản 30–45 phút (chủ đề và trình độ do nhóm chọn), worksheet khoảng 10 câu, chat có lỗi
  cố ý, giáo viên giảng chen Việt–Anh; danh sách kiểm tra cấu hình Zoom/Meet trước khi ghi.
- Gán nhãn: 10 phút transcript chuẩn, khoảng 100 lần xuất hiện từ tiếng Anh mục tiêu, 10 phút lượt người nói.
- Phiếu đồng ý mẫu cho buổi học thật.

### T7. Kiểm thử và tài liệu (0,5 ngày)
- `tests/`: parser chat, trích hotwords từ slide, gắn người nói, chuẩn hóa WER.
- README: cách tạo một buổi học mới và chạy pipeline.

## Thứ tự và lịch

```
T6 (kịch bản, ghi buổi đóng vai, gán nhãn) ─────────────────────────────►
T1 ──► T2 ──► T3 ─┬─► T5 ──► chạy thí nghiệm ──► T7
              T4 ─┘
```

| Ngày | Việc |
|---|---|
| 1 | T1; viết kịch bản buổi đóng vai (T6) |
| 2 | T2; ghi buổi đóng vai |
| 3–4 | T3; bắt đầu gán nhãn |
| 5 | T4 |
| 6 | T5; hoàn tất nhãn |
| 7 | Chạy thí nghiệm E1–E5, D1 |
| 8 | T7; tổng hợp kết quả, bàn giao phase 2 |

Nếu buổi đóng vai chưa có đúng hạn: phát triển T3–T5 trên `cs224n-bert` trước rồi chạy lại khi có dữ liệu.

## Thí nghiệm

| Mã | Cấu hình | Câu hỏi |
|---|---|---|
| E1 | Whisper small như v2 | Mốc so sánh |
| E2 | E1 + `multilingual` | Có xác định đúng ngôn ngữ từng đoạn không |
| E3 | E2 + hotwords theo slide | **Từ tiếng Anh có được nhận đúng hơn không** (giả thuyết chính) |
| E4 | E3 với medium / large-v3 (Colab) | Model lớn hơn giúp bao nhiêu |
| E5 | E3 + PhoWhisper cho đoạn tiếng Việt | Phần tiếng Việt có tốt hơn không (tùy chọn) |
| D1 | pyannote so với âm thanh riêng từng người | DER |

Bảng kết quả: WER (tổng, đoạn tiếng Việt, đoạn tiếng Anh), tỉ lệ nhận đúng và tỉ lệ chèn sai từ mục tiêu, DER,
thời gian chạy.

## Tiêu chí hoàn thành phase 1

- [ ] `pipeline.py` chạy hết trên `cs224n-bert` và `roleplay-01`
- [ ] Hồi quy CS224N: 9/10 slide, sai số trung bình 0,6 s
- [ ] Có bảng E1–E3 (E4, E5 nếu kịp) và D1
- [ ] Test trong `tests/` chạy qua
- [ ] Không có video, âm thanh, chat gốc hay tên thật nào trong git

## Thư viện thêm

`jiwer`, `pytest`; `pyannote.audio` (tùy chọn, cần `HF_TOKEN`). Chuyển PhoWhisper dùng `ct2-transformers-converter`
đi kèm `ctranslate2` (đã cài cùng faster-whisper) và `transformers` (đã có).

## Rủi ro của phase 1

| Rủi ro | Dự phòng |
|---|---|
| `multilingual` nhận diện sai ngôn ngữ ở đoạn chen ngắn | Phát hiện ngôn ngữ riêng cho từng đoạn VAD |
| Hotwords khiến Whisper chèn từ trên slide dù giáo viên không nói | Đo tỉ lệ chèn sai; giới hạn số hotwords |
| pyannote vướng token hoặc chậm trên CPU | Nguồn A (âm thanh riêng), hoặc gán tay 10 phút để đo |
| Chưa có buổi đóng vai đúng hạn | Phát triển trên `cs224n-bert` trước |

## Bàn giao cho phase 2

`transcript.json` có `lang`, `slide`, `speaker`, `words`; `chat.json`; `speakers.json` → đầu vào cho phân đoạn
giai đoạn, hành động lời nói và trích bài tập (WP2, WP3).
