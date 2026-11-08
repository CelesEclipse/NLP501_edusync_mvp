# EduSync: Multimodal Online Lecture Alignment & Pedagogical Analytics

EduSync is an educational NLP platform that turns online classroom recordings (Zoom/Google Meet/YouTube) into structured, interactive study notebooks for students and automated pedagogical quality dashboards for teachers.

---

## 📚 Official Project Documentation Suite (`docs/`)

Toàn bộ tài liệu chính thức của đồ án môn học NLP (NLP501 - MSE) được chuẩn hóa và duy trì tại thư mục [`docs/`](docs/):

| STT | Tài liệu | Mô tả Trọng tâm |
| :---: | :--- | :--- |
| 📖 | [**`docs/README.md`**](docs/README.md) | **Mục lục Trung tâm & Hướng dẫn duyệt tài liệu** |
| 01 | [**`01_project_proposal.md`**](docs/01_project_proposal.md) | Đề xuất Đề tài, Bối cảnh Sư phạm & Nghiên cứu Khả thi |
| 02 | [**`02_nlp_architecture_and_literature.md`**](docs/02_nlp_architecture_and_literature.md) | Cơ sở Lý thuyết NLP sâu, Đa phương thức & Tổng quan Nghiên cứu |
| 03 | [**`03_requirements_analysis_srs.md`**](docs/03_requirements_analysis_srs.md) | Đặc tả & Phân tích Yêu cầu Bài toán (SRS - IEEE 830) |
| 04 | [**`04_detailed_design_and_qa_plan.md`**](docs/04_detailed_design_and_qa_plan.md) | Thiết kế Chi tiết Hệ thống (SDD) & Kế hoạch Kiểm soát Chất lượng (QA/QC) |
| 05 | [**`05_solution_dense_embeddings_guide.md`**](docs/05_solution_dense_embeddings_guide.md) | Hướng dẫn Kỹ thuật Giải pháp Nhúng Vector Ngữ nghĩa (Sentence-Transformers) |
| 06 | [**`06_user_guide_and_demo.md`**](docs/06_user_guide_and_demo.md) | Sổ tay Hướng dẫn Sử dụng Web Demo cho Học sinh và Giáo viên |

> ⚠️ **Quy ước Dự án (Project Convention):** Thư mục `docs/` là **Nguồn Chân lý Duy nhất (Single Source of Truth - SSOT)** cho toàn bộ tài liệu kỹ thuật, kiến trúc và báo cáo của dự án. Mọi thay đổi, bổ sung về giải pháp kỹ thuật bắt buộc phải được cập nhật trực tiếp tại đây.

---

## Quick Start & Web Demo

Khởi chạy Web Demo tương tác chỉ với 2 lệnh:
```bash
# 1. Đồng bộ dữ liệu bài học
python demo/prepare.py --lesson lessons/ece-toeic-starter-u4

# 2. Khởi chạy máy chủ Web
cd demo && ../.venv/bin/python -m RangeHTTPServer 8000
# Mở trình duyệt tại: http://localhost:8000/
```

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# download the CS224N lecture into its lesson folder (not in git: ~200 MB)
yt-dlp -f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]" -o lessons/cs224n-bert/video.mp4 "https://www.youtube.com/watch?v=knTc-NQSjKA"
```

## Layout

```
lessons/<id>/            one folder per lesson
  lesson.json            title, source, licence/attribution, languages, ASR settings
  video.mp4  audio.m4a  slides.pdf    inputs (video and audio are never committed)
  slides.json  visual.npz  transcript.json  alignment.json  links.json    outputs, lessons with a slides PDF
  screens/  screens.json  transcript.json  content.md                     outputs, lessons without one
  gold/                  hand labels (labels.json) and silver labels
  results/               experiment outputs behind the report tables
materials/               shared reading library (catalog.json; downloaded PDFs are not committed)
demo/                    web demo, filled from one lesson by demo/prepare.py
```

Lessons: `cs224n-bert` (English lecture with its slides PDF, the alignment benchmark) and
`ece-toeic-starter-u1/u4/u5` (TOEIC Starter lessons taught in Vietnamese by ECE English Online, CC BY; no
slides PDF, so their content is extracted from the screen). Content extracted from these videos stays local
(see `.gitignore`), because it includes exercises from the textbook shown on screen.

## Pipeline

```bash
python pipeline.py lessons/cs224n-bert                       # runs only the steps whose outputs are missing
python pipeline.py lessons/cs224n-bert --force align links   # rerun chosen steps (or --force all)
```

Steps for a lesson **with** `slides.pdf`: `slides` (parse_slides.py) → `visual` (visual.py, ~1 min) →
`transcribe` (transcribe.py, ~9 min on CPU with `small`) → `align` (align.py, video + transcript) → `links`
(link_materials.py); then the alignment is scored against `gold/labels.json` when the lesson has one.
Steps for a lesson **without** one: `screens` (extract_screens.py: one image per screen + OCR, ~1–2 min) →
`transcribe` (Whisper model and prompt from `lesson.json`; `large-v3-turbo` takes ~1 min of CPU per minute of
audio) → `content` (lesson_content.py: `content.md`, each screen with its text and what the teacher said).
Every script also runs on its own with `--lesson <folder>`; its file paths are then relative to that folder.

Adding a YouTube lesson (only Creative Commons videos are downloaded unless you pass `--allow-standard`):

```bash
python fetch_lesson.py thu4-KGapkA lessons/ece-toeic-starter-u1 --language vi --multilingual \
    --prompt "Luyện thi TOEIC Starter. Thầy giảng bằng tiếng Việt và đọc câu tiếng Anh: Part 5, Part 6, ..."
python pipeline.py lessons/ece-toeic-starter-u1
```

Compare variants by writing them to `results/` and passing them all to `evaluate.py`:

```bash
L=lessons/cs224n-bert
python align.py --lesson $L --method tfidf --out results/text_tfidf.json                       # text only
python align.py --lesson $L --method none --visual visual.npz --out results/visual.json        # video only
python align.py --lesson $L --method bge-base --visual visual.npz --drop-visual 0.5 --out results/r.json  # robustness
python evaluate.py --lesson $L gold/labels.json results/text_tfidf.json results/visual.json alignment.json
python make_labels.py --lesson $L results/visual.json --out gold/labels_silver.json           # silver labels
python evaluate.py --lesson $L gold/labels_silver.json results/text_tfidf.json
python fetch_materials.py --pdf 1810.04805      # rebuild materials/catalog.json (+ the BERT paper PDF)
```

## Demo

```bash
python demo/prepare.py --lesson lessons/cs224n-bert
cd demo && python -m RangeHTTPServer 8000       # open http://localhost:8000
```

Click a slide to jump the video, play the video to follow the slides, read the linked papers for the current
slide (with page numbers for downloaded PDFs), and search the transcript to jump to where a term is explained.

## Files

| File | Purpose |
|---|---|
| `pipeline.py` | run the steps for one lesson, skipping those whose outputs exist |
| `fetch_lesson.py` | download a Creative Commons YouTube lesson (video + audio) and write its `lesson.json` |
| `extract_screens.py` | split a screen recording into screens (new page/slide), keep each one's last image, OCR it (vi + en) |
| `lesson_content.py` | `content.md` / `content.json`: every screen with its OCR text and the teacher's speech |
| `transcribe.py` | faster-whisper speech-to-text with timestamps; tags each segment vi / en / mixed; `--screen-hints` feeds the English OCR text of the screen on view to Whisper |
| `eval/asr_clips.py` | cut 2-min audio clips with a draft transcript, for the team to correct by ear (reference for WER) |
| `eval/wer.py` | WER against the corrected clips, and accuracy on the English words shown on screen |
| `eval/asr_screen_terms.py` | proxy without references: share of on-screen English words found in the speech of that screen |
| `parse_slides.py` | extract text per slide with PyMuPDF |
| `visual.py` | sample a frame every 2 s, normalized cross-correlation against every rendered slide |
| `align.py` | windowing, similarity (TF-IDF / bge), normalization, optional fusion with video scores, order-constrained DP |
| `evaluate.py` | boundary error vs. labels; `all` column also scores missed slides |
| `make_labels.py` | silver labels (first on-screen time of each slide) from a visual alignment |
| `fetch_materials.py` | reading list from the arXiv API plus a few hand-picked tutorials -> `materials/catalog.json` |
| `link_materials.py` | link each slide (slide text + what was said on it) to cited and related materials |
| `lessons/cs224n-bert/gold/labels.json` | hand-labeled slide start times (`mm:ss`) for the CS224N BERT lecture |

## Notes
- Lecture: Stanford CS224N Winter 2020, "BERT and Other Pre-trained Language Models" (Jacob Devlin).
- `faster-whisper` 1.2 breaks with `av` 16 (`metadata_errors` error); `requirements.txt` pins `av<16`.
- Colab: `faster-whisper` can conflict with Colab's CUDA and `av` versions; use `--device cpu` if the GPU path fails.
