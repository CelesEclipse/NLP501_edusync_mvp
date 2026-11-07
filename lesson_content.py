"""screens.json + transcript.json -> content.md (readable lesson notes) and content.json.
Each screen gets its OCR text and what the teacher said while it was shown: the transcript segments whose
midpoint falls in the screen's time span (speech before the first screen goes to the first one).
content.json keeps every segment; content.md joins them into paragraphs, breaking at pauses of --pause s.
Usage: python lesson_content.py --lesson lessons/<id>"""
import argparse, collections, json, os


def mmss(t):
    return f"{int(t) // 60:02d}:{int(t) % 60:02d}"


def paragraphs(segs, pause, max_chars=400):
    out = []
    for s in segs:
        if out and s["start"] - out[-1]["end"] <= pause and len(out[-1]["text"]) < max_chars:
            out[-1].update(end=s["end"], text=out[-1]["text"] + " " + s["text"])
        else:
            out.append({"start": s["start"], "end": s["end"], "text": s["text"]})
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lesson", default=".", help="lesson folder; all paths are relative to it")
    ap.add_argument("--pause", type=float, default=2.0, help="a longer silence starts a new paragraph in content.md")
    a = ap.parse_args()
    L = lambda f: os.path.join(a.lesson, f)
    lesson = json.load(open(L("lesson.json"))) if os.path.exists(L("lesson.json")) else {}
    screens, transcript = json.load(open(L("screens.json"))), json.load(open(L("transcript.json")))

    speech = collections.defaultdict(list)
    for seg in transcript:
        mid = (seg["start"] + seg["end"]) / 2
        k = max([i for i, s in enumerate(screens) if s["start"] <= mid] or [0])
        speech[k].append(seg)
    content = [{"screen": s["id"], "start": s["start"], "end": s["end"], "image": s["image"], "same_as": s["same_as"],
                "screen_text": s["text"], "speech": speech[k]} for k, s in enumerate(screens)]
    json.dump(content, open(L("content.json"), "w"), ensure_ascii=False, indent=1)

    langs = collections.Counter(seg.get("lang") for seg in transcript)
    md = [f"# {lesson.get('title', os.path.basename(os.path.normpath(a.lesson)))}", ""]
    if lesson.get("attribution"):
        md += [f"Nguồn: {lesson['attribution']}", ""]
    md += [f"{len(screens)} màn hình · {len(transcript)} đoạn lời giảng "
           f"(vi {langs['vi']}, en {langs['en']}, mixed {langs['mixed']})", ""]
    for c in content:
        repeat = f" (giống màn hình {c['same_as']})" if c["same_as"] else ""
        md += [f"## Màn hình {c['screen']} · {mmss(c['start'])}–{mmss(c['end'])}{repeat}", "",
               f"![màn hình {c['screen']}]({c['image']})", ""]
        if c["screen_text"]:
            md += ["**Chữ trên màn hình (OCR):**", "", "```text", c["screen_text"], "```", ""]
        if c["speech"]:
            md += ["**Lời giảng:**", ""] + [f"`{mmss(p['start'])}` {p['text']}\n" for p in paragraphs(c["speech"], a.pause)]
    open(L("content.md"), "w").write("\n".join(md))
    print(f"{len(content)} screens, {len(transcript)} segments -> {L('content.md')}, {L('content.json')}")
