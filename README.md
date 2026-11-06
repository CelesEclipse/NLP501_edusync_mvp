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

# download the lecture into demo/ (not in git: ~200 MB)
yt-dlp -f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]" -o demo/lecture.mp4 "https://www.youtube.com/watch?v=knTc-NQSjKA"
```

`transcript.json`, `slides.json`, `visual.npz` and `materials/catalog.json` are committed, so steps 1, 2, 3b
and 7a can be skipped.

## Pipeline

```bash
python transcribe.py demo/lecture.mp4 --device cpu          # 1  -> transcript.json  (--device cuda on a GPU)
python parse_slides.py demo/slides.pdf                      # 2  -> slides.json
python visual.py demo/lecture.mp4 demo/slides.pdf           # 3b -> visual.npz  (frame x slide image similarity, ~1 min)
python align.py --method bge-base --visual visual.npz --out alignment_fused.json   # 3-5 text + video
python evaluate.py labels.json alignment_fused.json         # 6
python fetch_materials.py --pdf 1810.04805                  # 7a -> materials/catalog.json (+ BERT paper PDF)
python link_materials.py --alignment alignment_fused.json --out links.json         # 7b -> links.json
```

Compare variants by running `align.py` several times and passing all outputs to `evaluate.py`:

```bash
python align.py --method tfidf --out results/text_tfidf.json                       # text only (30 s windows)
python align.py --method none --visual visual.npz --out results/visual.json        # video frames only
python align.py --method bge-base --visual visual.npz --drop-visual 0.5 --seed 0 --out r.json  # robustness test
python evaluate.py labels.json results/*.json
python make_labels.py results/visual.json                    # silver labels for all 39 shown slides
python evaluate.py labels_silver.json results/text_*.json
```

## Demo

```bash
cd demo
python prepare.py slides.pdf --alignment ../alignment_fused.json --transcript ../transcript.json --links ../links.json
python -m RangeHTTPServer 8000      # open http://localhost:8000
```

Click a slide to jump the video, play the video to follow the slides, read the linked papers for the current
slide (with page numbers for downloaded PDFs), and search the transcript to jump to where a term is explained.

## Files

| File | Purpose |
|---|---|
| `transcribe.py` | faster-whisper speech-to-text with timestamps |
| `parse_slides.py` | extract text per slide with PyMuPDF |
| `visual.py` | sample a frame every 2 s, normalized cross-correlation against every rendered slide |
| `align.py` | windowing, similarity (TF-IDF / bge), normalization, optional fusion with video scores, order-constrained DP |
| `evaluate.py` | boundary error vs. labels; `all` column also scores missed slides |
| `make_labels.py` | silver labels (first on-screen time of each slide) from a visual alignment |
| `fetch_materials.py` | reading list from the arXiv API plus a few hand-picked tutorials -> `materials/catalog.json` |
| `link_materials.py` | link each slide (slide text + what was said on it) to cited and related materials |
| `labels.json` | hand-labeled slide start times (`mm:ss`) for the CS224N BERT lecture |
| `results/` | alignment outputs and heatmaps behind the report tables |

## Notes
- Lecture: Stanford CS224N Winter 2020, "BERT and Other Pre-trained Language Models" (Jacob Devlin).
- `faster-whisper` 1.2 breaks with `av` 16 (`metadata_errors` error); `requirements.txt` pins `av<16`.
- Colab: `faster-whisper` can conflict with Colab's CUDA and `av` versions; use `--device cpu` if the GPU path fails.
