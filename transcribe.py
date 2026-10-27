"""Step 1: audio/video -> transcript.json  (list of {start, end, text}).
Usage: python transcribe.py lecture.mp4 [--device cuda|cpu] [--prompt "keywords..."]"""
import argparse, json
from faster_whisper import WhisperModel

ap = argparse.ArgumentParser()
ap.add_argument("media")
ap.add_argument("--model", default="small")
ap.add_argument("--device", default="cpu")
ap.add_argument("--prompt", default="Lecture on NLP: transformer, attention, embeddings, BERT, GLUE, SQuAD, CoLA.")
ap.add_argument("--out", default="transcript.json")
a = ap.parse_args()

compute = "float16" if a.device == "cuda" else "int8"
model = WhisperModel(a.model, device=a.device, compute_type=compute)
segments, _ = model.transcribe(a.media, initial_prompt=a.prompt, vad_filter=True)
data = [{"start": s.start, "end": s.end, "text": s.text.strip()} for s in segments]
json.dump(data, open(a.out, "w"), indent=2)
print(len(data), "segments ->", a.out)
