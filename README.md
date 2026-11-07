# EduSync: slide-video alignment

Aligns a lecture video with its PDF slides, so each slide gets a start time in the video, and links every
slide to the papers and tutorials that explain it.
Full results and error analysis: see [report/edusync_mvp_report.md](report/edusync_mvp_report.md).

**Next direction:** English-language lessons recorded on Google Meet/Zoom (slides, teacher speech, exercises,
worked examples, attachments, chat). Roadmap: [docs/esl_roadmap.md](docs/esl_roadmap.md); current phase:
[docs/phase1_plan.md](docs/phase1_plan.md) (both in Vietnamese).

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
| `transcribe.py` | faster-whisper speech-to-text with timestamps; tags each segment vi / en / mixed |
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
