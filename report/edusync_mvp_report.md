# EduSync MVP Report: Slide-Video Alignment

**Status:** MVP core pipeline working on one lecture. Results are preliminary (1 lecture, 10 hand-labeled slides). Sections 1-9 describe v1 (text only); section 10 adds video fusion and links to learning materials (v2).

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

## 10. v2: video fusion and learning-material links

### 10.1 What changed

| Component | v1 | v2 |
|---|---|---|
| Evidence | transcript text only | text + video frames (`visual.py`) |
| Time grid | about 30 s windows | 2 s frames (text score of the enclosing window is copied to each frame) |
| Score | z-scored text similarity | `1.0 x z(visual) + 0.5 x z(text)`; frames that match no slide (camera on the speaker, 12% of frames) get 0 visual score |
| Evaluation | 10 hand labels, found slides only | + `all` column that scores missed slides; + 39 silver labels |
| Learning materials | none | 24-item reading list (17 arXiv papers via the arXiv API, 7 papers/tutorials/textbook); every slide linked to cited and related items, with page numbers for downloaded PDFs |
| Demo | slide list + video | + readings panel for the current slide, + transcript search that jumps to the moment a term is said |

**Visual score.** The lecture video shows the slides full screen for most of its length. Each sampled frame and each
rendered PDF page are reduced to a blurred 96x54 grayscale thumbnail; their normalized cross-correlation is the
visual similarity. No model and no GPU are needed (about 35 s for the 54 min video on an M1 Pro). The best
match is 1.00 on a typical slide frame; 199 of 1635 frames match nothing (below 0.5) and are camera shots.

**Transcript.** `transcript.json` was regenerated locally (faster-whisper 1.2.1, `small`, CPU int8): 1297 segments,
against 721 in the v1 Colab run. The text-only rows below therefore differ from section 4; the v1 file is kept as a
reference row.

### 10.2 Results on the 10 hand labels

`all` = mean absolute error over all 10 labels, with a missed slide predicted at the start of the next found slide.

| Method | Found | Mean | Median | All | <=5 s | <=30 s | <=60 s | Missed |
|---|---|---|---|---|---|---|---|---|
| v1: bge-base + DP (Colab transcript) | 9/10 | 21.7 s | 16.2 s | 23.1 s | 2/10 | 7/10 | 9/10 | 31 |
| Text: TF-IDF + DP | 8/10 | 18.0 s | 18.7 s | 20.4 s | 0/10 | 8/10 | 8/10 | 30, 42 |
| Text: bge-small + DP | 8/10 | 32.4 s | 26.9 s | 40.3 s | 0/10 | 5/10 | 7/10 | 31, 38 |
| Text: bge-base + DP | 7/10 | 25.1 s | 14.7 s | 34.7 s | 0/10 | 5/10 | 6/10 | 31, 33, 38 |
| Video only + DP | 9/10 | **0.6 s** | 1.0 s | **0.7 s** | 9/10 | 9/10 | 9/10 | 42 |
| Video + TF-IDF + DP | 9/10 | 1.2 s | 1.0 s | 6.5 s | 8/10 | 9/10 | 9/10 | 42 |
| **Video + bge-base + DP** | 9/10 | **0.6 s** | 1.0 s | 2.7 s | 9/10 | 9/10 | 9/10 | 42 |

Video alone and video + argmax give the same numbers; with this video the DP is not needed when frames are clean.

**Slide 42 is probably a labeling ambiguity, not a miss.** Slide 42 is a title-only "Conclusions" divider and never
appears on screen: the video cuts from a camera shot straight to slide 43 (also titled "Conclusions") at 52:34, two
seconds before the 52:36 label. The label most likely marks slide 43. `labels.json` is left unchanged. The fused
run starts slide 43 at 52:14, during the camera shot, because the speaker starts concluding before the slide changes;
this is why its `all` is 2.7 s against 0.7 s for video only.

### 10.3 Silver labels: text methods on 39 slides

Video-only alignment matches every hand label it finds to within 1 s, so the first on-screen time of each slide
(`make_labels.py`, slides on screen for at least 6 s) is used as a silver label for 39 of the 43 slides
(dividers 2, 10, 26 and 42 are skipped). These labels come from the video, so they are only used to compare
**text** methods with each other; they cannot judge video or fused methods fairly.

| Method | Found | Mean | Median | All | <=30 s | <=60 s |
|---|---|---|---|---|---|---|
| v1: bge-base + DP (Colab transcript) | 31/39 | 27.0 s | 17.8 s | 27.7 s | 25/39 | 29/39 |
| Text: TF-IDF + DP | 31/39 | 28.1 s | 19.8 s | 28.2 s | 24/39 | 30/39 |
| Text: bge-small + DP | 28/39 | 32.7 s | 19.4 s | 47.7 s | 20/39 | 23/39 |
| Text: bge-base + DP | 28/39 | 37.9 s | 18.9 s | 50.6 s | 19/39 | 23/39 |

With 39 slides the v1 conclusion holds: TF-IDF is at least as good as bge on this lecture, and a text-only system
misses 8-11 slides (title, divider, and diagram slides such as 1, 8, 12, 19).

### 10.4 Robustness: what if the camera leaves the slides?

Many lecture recordings show the speaker or a wide room shot for long stretches. To simulate this, `--drop-visual p`
hides a random fraction p of 60 s blocks of frames (mean of 3 seeds). Errors are `all` errors, in seconds.

| Hidden | Video only (10 hand / 39 silver) | Video + bge-base (10 hand / 39 silver) |
|---|---|---|
| 0% | 0.7 / 0.0 | 2.7 / 0.9 |
| 25% | 3.3 / 10.4 | 4.6 / **6.0** |
| 50% | 29.5 / 32.3 | **11.7 / 18.3** |
| 75% | 107.6 / 138.5 | **24.2 / 31.6** |
| 90% | 468.2 / 449.4 | **33.4 / 48.5** |

Video alone collapses once half of the frames are hidden (the DP has no evidence and stays on the last seen
slide). With text added, the error degrades smoothly towards the text-only level (about 35-50 s). The text branch is
therefore what makes the system usable on recordings that do not show the slides all the time.

### 10.5 Links to learning materials

`fetch_materials.py` builds the reading list from the arXiv API (titles, authors, years and abstracts are not typed
by hand) and adds GloVe, GPT-1, Bucila et al. 2006, Jurafsky & Martin SLP3, two Illustrated tutorials, and the
Hugging Face course. `link_materials.py` then links each slide:

- **Query** = slide text + everything said while the slide was on screen (from the fused alignment).
- **Cited**: the slide names the material (paper title on the slide, or an alias such as "XLNet" in the slide title).
  22 cited links, e.g. RoBERTa, XLNet, ALBERT, T5 and ELECTRA slides to their papers, slide 39 to Bucila 2006 and
  Hinton 2015, slide 40 to Turc et al. 2020, GLUE and SQuAD 2.0 slides to their dataset papers.
- **Related**: bge-base cosine between the query and each passage (abstract, or 150-word chunk of a downloaded PDF
  page), z-scored per passage over all slides, kept when z >= 1.0 and cosine >= 0.6, at most 3 per slide.

The z-score matters for the same reason as in the alignment: before it, the BERT paper (100 page chunks) was the
top related item on 36 of the 38 slides that got related links, because one of its many chunks is always close. After it, related links become
specific: slide 3 (word embeddings) links GloVe, word2vec and ELMo; slide 8 (Transformer) links "Attention Is All
You Need" and The Illustrated Transformer; slide 13 (Masked LM) links page 4 of the BERT paper, which is its
"Masked LM" section; the fine-tuning slides 18-19 link page 5.

Remaining noise (not yet measured): a few loose related links such as GloVe on an XLNet slide or Hinton 2015 on a
Masked LM slide. Link quality has not been evaluated with labels; precision@3 against a small hand-made set of
slide-to-reading pairs is the next step.

### 10.6 Next steps

| Priority | Task |
|---|---|
| 1 | Test on 2-4 more lectures, including at least one where the camera often leaves the slides (where fusion matters) |
| 2 | Label 3-5 relevant readings per slide for 10-15 slides and report precision@3 for the links |
| 3 | Learn the fusion weight per lecture (e.g. weight video by the share of frames that match a slide) instead of the fixed 1.0 / 0.5 |
| 4 | OCR or CLIP features for videos where the slide is small or filmed at an angle (thumbnail correlation needs a full-screen slide) |
| 5 | Use the aligned slide-transcript pairs as training data: fine-tune the text embedding, and slide-aware Q&A that cites timestamps and readings |
