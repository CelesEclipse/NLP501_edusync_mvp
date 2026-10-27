# EduSync: slide-video alignment

Aligns a lecture video with its PDF slides, so each slide gets a start time in the video.
Full results and error analysis: see `edusync_mvp_report.md`.

## Pipeline

```bash
pip install -r requirements.txt

# Run this to download video
yt-dlp "https://www.youtube.com/watch?v=knTc-NQSjKA&t=36s"

# remember to rename the video to `lecture.mp4`
```

```bash
# No need to run these things, skip to the demo section
python transcribe.py lecture.mp4 --device cuda        # -> transcript.json   (use --device cpu without a GPU)
python parse_slides.py slides.pdf                     # -> slides.json
python align.py --method bge-base --out alignment_bge_base.json --plot heatmap.png
python evaluate.py labels.json alignment_bge_base.json
```

Compare variants by running `align.py` several times and passing all outputs to `evaluate.py`:

```bash
python align.py --method tfidf --out a_tfidf_dp.json
python align.py --method bge-base --decode argmax --no-normalize --out a_bge_raw.json
python evaluate.py labels.json a_tfidf_dp.json a_bge_raw.json alignment_bge_base.json
```

Then run the demo (`demo/`): copy `alignment_bge_base.json` there and run `python prepare.py slides.pdf`.
```bash
# add lecture.mp4 to the demo folder then :
cd demo
python prepare.py slides.pdf
python -m RangeHTTPServer 8000
```

## Files

| File | Purpose |
|---|---|
| `transcribe.py` | faster-whisper speech-to-text with timestamps |
| `parse_slides.py` | extract text per slide with PyMuPDF |
| `align.py` | windowing, similarity (TF-IDF / bge), normalization, order-constrained DP |
| `evaluate.py` | boundary error vs. hand labels |
| `labels.json` | hand-labeled slide start times (`mm:ss`) for the CS224N BERT lecture |

## Notes
- Lecture: Stanford CS224N Winter 2020, "BERT and Other Pre-trained Language Models" (Jacob Devlin). Video and slides are not included; get them from the course site.
- Colab: `faster-whisper` can conflict with Colab's CUDA and `av` versions; use `--device cpu` if the GPU path fails.
