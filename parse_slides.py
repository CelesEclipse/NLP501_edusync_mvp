"""Step 2: slides.pdf -> slides.json  (list of {slide, text}).
Usage: python parse_slides.py slides.pdf"""
import json, sys
import pymupdf

doc = pymupdf.open(sys.argv[1])
data = [{"slide": i + 1, "text": p.get_text().strip()} for i, p in enumerate(doc)]
json.dump(data, open("slides.json", "w"), indent=2)
print(len(data), "slides,", sum(len(d["text"]) < 20 for d in data), "near-empty -> slides.json")
