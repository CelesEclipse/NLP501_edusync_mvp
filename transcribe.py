"""Step 1: audio/video -> transcript.json  (list of {start, end, text, lang}).
Usage: python transcribe.py --lesson lessons/<id> [--model small] [--multilingual] [--device cuda|cpu]
The lesson's audio.m4a is used when present (else video.mp4). Model, prompt and multilingual default to
lesson.json ("asr": {"model": ..., "prompt": ..., "multilingual": true}). --multilingual lets Whisper switch language between
30 s windows (Vietnamese explanations with English examples). 'lang' is a text heuristic: vi when many words
carry Vietnamese diacritics, en when none do, mixed otherwise."""
import argparse, json, os, re
from faster_whisper import WhisperModel

VI_CHARS = re.compile("[ăâđêôơưàáạảãằắặẳẵầấậẩẫèéẹẻẽềếệểễìíịỉĩòóọỏõồốộổỗờớợởỡùúụủũừứựửữỳýỵỷỹ]", re.I)


def text_lang(text):
    words = re.findall(r"[^\W\d_]+", text)
    if not words:
        return None
    vi = sum(bool(VI_CHARS.search(w)) for w in words) / len(words)
    return "vi" if vi > 0.3 else "en" if vi == 0 else "mixed"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("media", nargs="?", help="default: audio.m4a if the lesson has one, else video.mp4")
    ap.add_argument("--lesson", default=".", help="lesson folder; the other paths are relative to it")
    ap.add_argument("--model", help="default: asr.model from lesson.json, else small")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--prompt", help="default: asr.prompt from lesson.json")
    ap.add_argument("--language", help="force a language code such as vi; default: detect")
    ap.add_argument("--multilingual", action="store_true", help="re-detect the language for every 30 s window")
    ap.add_argument("--out", default="transcript.json")
    a = ap.parse_args()
    L = lambda f: os.path.join(a.lesson, f)
    media = a.media or ("audio.m4a" if os.path.exists(L("audio.m4a")) else "video.mp4")
    asr = json.load(open(L("lesson.json"))).get("asr", {}) if os.path.exists(L("lesson.json")) else {}
    prompt = a.prompt if a.prompt is not None else asr.get("prompt")

    compute = "float16" if a.device == "cuda" else "int8"
    model = WhisperModel(a.model or asr.get("model", "small"), device=a.device, compute_type=compute)
    segments, info = model.transcribe(L(media), initial_prompt=prompt, vad_filter=True, language=a.language,
                                      multilingual=a.multilingual or asr.get("multilingual", False))
    data = [{"start": s.start, "end": s.end, "text": s.text.strip(), "lang": text_lang(s.text)} for s in segments]
    json.dump(data, open(L(a.out), "w"), ensure_ascii=False, indent=2)
    print(f"{len(data)} segments (detected {info.language}) ->", L(a.out))
