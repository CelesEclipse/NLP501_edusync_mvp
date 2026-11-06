"""Step 1: audio/video -> transcript.json  (list of {start, end, text}).
Usage: python transcribe.py --lesson lessons/<id> [--device cuda|cpu]   (reads <lesson>/video.mp4)
       python transcribe.py lecture.mp4 [--prompt "keywords..."]       (paths relative to the current folder)"""
import argparse, json, os
from faster_whisper import WhisperModel

ap = argparse.ArgumentParser()
ap.add_argument("media", nargs="?", default="video.mp4")
ap.add_argument("--lesson", default=".", help="lesson folder; the other paths are relative to it")
ap.add_argument("--model", default="small")
ap.add_argument("--device", default="cpu")
ap.add_argument("--prompt", default="Lecture on NLP: transformer, attention, embeddings, BERT, GLUE, SQuAD, CoLA.")
ap.add_argument("--out", default="transcript.json")
a = ap.parse_args()
out = os.path.join(a.lesson, a.out)

compute = "float16" if a.device == "cuda" else "int8"
model = WhisperModel(a.model, device=a.device, compute_type=compute)
segments, _ = model.transcribe(os.path.join(a.lesson, a.media), initial_prompt=a.prompt, vad_filter=True)
data = [{"start": s.start, "end": s.end, "text": s.text.strip()} for s in segments]
json.dump(data, open(out, "w"), indent=2)
print(len(data), "segments ->", out)
