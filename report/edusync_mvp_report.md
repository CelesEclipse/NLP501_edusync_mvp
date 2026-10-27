# EduSync MVP Report: Slide-Video Alignment

**Status:** MVP core pipeline working on one lecture. Results are preliminary (1 lecture, 10 hand-labeled slides).

## 1. Goal

Given a lecture video and its PDF slides, automatically find the time range in the video where the instructor explains each slide, so that clicking a slide jumps the video to that moment (and vice versa).

## 2. Data

| Item | Value |
|---|---|
| Lecture | Stanford CS224N, Winter 2020, "BERT and Other Pre-trained Language Models" (guest lecturer Jacob Devlin) |
| Video length | about 54 min (transcript ends at 3263 s) |
| Slides | 43 (3 near-empty: title or divider slides) |
| Transcript | 721 Whisper segments, merged into 101 windows of about 30 s |
| Ground truth | 10 slides labeled by hand from the YouTube video (slides 15, 21, 25, 27, 30, 31, 32, 33, 38, 42) |

## 3. Pipeline

1. **Transcribe:** `faster-whisper` (small model) gives timestamped segments.
2. **Parse slides:** PyMuPDF extracts text per slide.
3. **Window:** merge segments into about 30 s windows.
4. **Score:** embed windows and slides (`bge-base-en-v1.5`), cosine similarity gives a matrix of windows x slides. A TF-IDF baseline (unigrams + bigrams) is built the same way.
5. **Normalize:** z-score each slide's column, because short or generic slides otherwise score low against everything. Then smooth over 3 neighboring windows.
6. **Decode:** dynamic programming (Viterbi-style) finds the best path where the slide number can only move forward, with a small penalty for skipping slides.
7. **Evaluate:** predicted start time of each labeled slide vs. the hand-labeled time.

## 4. Results

Error = predicted slide start minus true slide start, in seconds. Mean and median are computed over slides that were found (assigned at least one window).

| Method | Slides found | Mean abs. error | Median abs. error | Within 30 s | Within 60 s |
|---|---|---|---|---|---|
| TF-IDF, raw argmax | 8/10 | 371.5 s | 120.9 s | 4/10 | 4/10 |
| TF-IDF, normalized argmax | 8/10 | 61.6 s | 20.5 s | 6/10 | 6/10 |
| **TF-IDF, normalized + DP** | 8/10 | **16.7 s** | **15.7 s** | **8/10** | 8/10 |
| bge-base, raw argmax | 6/10 | 797.4 s | 685.2 s | 1/10 | 2/10 |
| bge-base, normalized argmax | 10/10 | 455.8 s | 47.3 s | 4/10 | 6/10 |
| bge-base, normalized + smoothing, argmax | 8/10 | 443.2 s | 39.7 s | 4/10 | 5/10 |
| **bge-base, normalized + DP** | 9/10 | 21.7 s | 16.2 s | 7/10 | **9/10** |
| bge-base, DP, penalty 0.05 / 0.30 | 9/10 | 21.7 s | 16.2 s | 7/10 | 9/10 |

Slides missed: TF-IDF + DP misses slides 30 and 42; bge-base + DP misses slide 31.

### Per-slide errors (bge-base + DP)

| Slide | True start | Predicted | Error |
|---|---|---|---|
| 15 | 14:28 | about 14:36 | about +8 s |
| 21 | 26:01 | about 25:42 | about -19 s |
| 25 | 31:07 | about 31:24 | about +17 s |
| 27 | 33:15 | about 34:12 | about +57 s |
| 30 | 38:04 | about 38:00 | about -4 s |
| 31 | 38:28 | missed | n/a |
| 32 | 39:56 | about 39:06 | about -50 s |
| 33 | 41:19 | about 41:18 | about -1 s |
| 38 | 45:53 | about 45:24 | about -29 s |
| 42 | 52:36 | about 52:42 | about +6 s |

Predicted times in this table come from output rounded to 0.1 min, so treat them as accurate to about 3 s. The aggregate numbers in the results table were computed exactly by the scoring code.

## 5. Findings

1. **Normalization and the order constraint matter far more than the model choice.** Going from raw argmax to normalization to DP cuts the mean error from several minutes to about 17-22 s for both TF-IDF and bge-base.
2. **bge-base is not clearly better than TF-IDF on this lecture.** TF-IDF has a slightly lower mean error and more slides within 30 s, while bge-base finds one more slide and has more slides within 60 s. With 10 labels this is a tie, not a win for either.
3. **Argmax-only means are dominated by a few large outliers** (a wrong slide placed many minutes away), so the median is the more informative number for those rows.
4. **The jump penalty had no effect** between 0.05 and 0.30 on bge-base (and between 0.05 and 0.15 on TF-IDF). The alignment is insensitive to it in this range, and it did not fix the missed slide.

## 6. Error analysis

- **Neighboring slides on the same topic are hard to separate.** Slides 31 and 32 (both ALBERT) were merged: slide 31 was skipped and slide 32 was predicted about 50 s too early. Slides 13/14 (Masked LM) and 28/29/30 (XLNet) have the same risk.
- **Slides with almost no text** (dividers such as 2, 10, 26, 37, 42, and the two "Fine-Tuning Procedure" diagram slides 18-19) cannot be matched by text. Slide 27 (RoBERTa) was about 57 s late, possibly because slide 26 is a text-free divider just before it (this is a guess, not verified).
- **A stretch of the lecture matches no slide well** (around windows 42-48, about 21-24 min): the instructor discusses the GLUE/CoLA/MultiNLI examples out loud, so the transcript has little overlap with slide text.
- **ASR errors on technical terms** (for example "CoLA" transcribed as "Kola"; "XLNet" and "ELECTRA" never appear verbatim in the transcript) reduce keyword overlap, which hurts TF-IDF in particular.

## 7. Limitations

- One lecture only, and only 10 labeled slides, chosen partly because they were disagreement points. Numbers may not generalize.
- Time resolution is limited by the 30 s windows and by rounding in some printed values.
- Mean error covers found slides only, so methods that miss hard slides look better than they are. Always read the "found" column together with the error.
- Penalty values were not tuned (to avoid overfitting 10 labels).

## 8. Next steps

| Priority | Task |
|---|---|
| 1 | Demo UI (Streamlit or Gradio): video beside slides, clicking a slide seeks the video, playback highlights the current slide |
| 2 | Add 2-4 more lectures with about 10 labeled slides each, to test generalization |
| 3 | Add comparisons: bge-small, BM25, a cross-encoder reranker; optionally fine-tune a small embedding model on labeled pairs |
| 4 | Reduce window size (for example 15 s) and test ASR keyword prompting / term correction |
| 5 | Optional: slide-aware Q&A (chunk by slide, cite clickable timestamps), kept small |

## 9. Reproducing

Inputs: `transcript.json` (start, end, text per segment), `slides.json` (slide number, text). Output: per-window slide assignment (`alignment_bge_base.json`). The scoring function compares the first window assigned to each labeled slide with the labeled start time.
