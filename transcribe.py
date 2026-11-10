"""Step 1: audio/video -> transcript.json  (list of {start, end, text, lang}).
Usage: python transcribe.py --lesson lessons/<id> [--model small] [--multilingual] [--device cuda|cpu]
The lesson's audio.m4a is used when present (else video.mp4). Model, prompt and multilingual default to
lesson.json ("asr": {"model": ..., "prompt": ..., "multilingual": true}). --multilingual lets Whisper switch language between
30 s windows (Vietnamese explanations with English examples). 'lang' is a text heuristic: vi when many words
carry Vietnamese diacritics, en when none do, mixed otherwise.
--screen-hints words|lines (default: asr.screen_hints) transcribes the audio screen by screen (screens.json from
extract_screens.py) and gives Whisper the English OCR text of the screen on view as hotwords, which Whisper
re-reads before every 30 s window: 'words' = its content words, 'lines' = its English lines as written.
'chunks' cuts the audio the same way without hotwords (the control for the two).
--vad auto (default) runs Silero VAD first and drops it when it keeps less than VAD_MIN_SPEECH of the audio: loud
background music (common in YouTube lessons) can hide the voice from VAD, which then deletes almost all speech
(a 5-minute Japanese lesson came out as one segment). Without VAD Whisper is slower but keeps the speech."""
import argparse, json, os, re
from faster_whisper import WhisperModel, decode_audio
from faster_whisper.vad import get_speech_timestamps

VI_CHARS = re.compile("[ăâđêôơưàáạảãằắặẳẵầấậẩẫèéẹẻẽềếệểễìíịỉĩòóọỏõồốộổỗờớợởỡùúụủũừứựửữỳýỵỷỹ]", re.I)
STOP = set("the a an and or of to in on at for is are was were be been it its this that these those with as by from "
           "you your he she they we his her their our my me him them not no do does did has have had will would can".split())
SR = 16000
VAD_MIN_SPEECH = 0.25  # U1/U4/U5 lectures: VAD keeps well above this; music-backed videos far below


def text_lang(text):
    words = re.findall(r"[^\W\d_]+", text)
    if not words:
        return None
    vi = sum(bool(VI_CHARS.search(w)) for w in words) / len(words)
    return "vi" if vi > 0.3 else "en" if vi == 0 else "mixed"


def screen_hints(ocr_text, mode, max_words=60):
    """English OCR lines of one screen -> hotwords: its content words, or the lines themselves without blanks."""
    if mode == "chunks":
        return ""
    lines =[re.sub(r"[.…_]{2,}", " ", l) for l in ocr_text.splitlines() if l.strip() and not VI_CHARS.search(l)]
    if mode == "lines":
        words = re.sub(r"\(\s*[A-D]\s*\)", " ", " ".join(lines)).split()
    else:
        seen, words = set(), []
        for w in re.findall(r"[A-Za-z][A-Za-z'-]+", " ".join(lines)):
            if len(w) > 2 and w.lower() not in STOP and w.lower() not in seen:
                seen.add(w.lower())
                words.append(w)
    return " ".join(words[:max_words])


def vad_speech_share(audio):
    """Share of the audio that Silero VAD (faster-whisper defaults) marks as speech."""
    return sum(t["end"] - t["start"] for t in get_speech_timestamps(audio, sampling_rate=SR)) / max(len(audio), 1)


def segment(s, offset=0.0, **extra):
    return {"start": round(s.start + offset, 2), "end": round(s.end + offset, 2), "text": s.text.strip(),
            "lang": text_lang(s.text), "logprob": round(s.avg_logprob, 3), "no_speech": round(s.no_speech_prob, 3), **extra}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("media", nargs="?", help="default: audio.m4a if the lesson has one, else video.mp4")
    ap.add_argument("--lesson", default=".", help="lesson folder; the other paths are relative to it")
    ap.add_argument("--model", help="default: asr.model from lesson.json, else small")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--prompt", help="default: asr.prompt from lesson.json")
    ap.add_argument("--language", help="force a language code such as vi; default: detect")
    ap.add_argument("--multilingual", action="store_true", help="re-detect the language for every 30 s window")
    ap.add_argument("--screen-hints", choices=["none", "chunks", "words", "lines"],
                    help="hotwords from the OCR text of the screen on view (default: asr.screen_hints, else none)")
    ap.add_argument("--vad", choices=["auto", "on", "off"], default="auto",
                    help="voice-activity filter; auto = on unless it keeps < VAD_MIN_SPEECH of the audio")
    ap.add_argument("--out", default="transcript.json")
    a = ap.parse_args()
    L = lambda f: os.path.join(a.lesson, f)
    media = a.media or ("audio.m4a" if os.path.exists(L("audio.m4a")) else "video.mp4")
    asr = json.load(open(L("lesson.json"))).get("asr", {}) if os.path.exists(L("lesson.json")) else {}
    prompt = a.prompt if a.prompt is not None else asr.get("prompt")

    hints = a.screen_hints or asr.get("screen_hints", "none")

    compute = "float16" if a.device == "cuda" else "int8"
    model = WhisperModel(a.model or asr.get("model", "small"), device=a.device, compute_type=compute)
    audio = decode_audio(L(media), sampling_rate=SR)
    vad = a.vad == "on"
    if a.vad == "auto":
        share = vad_speech_share(audio)
        vad = share >= VAD_MIN_SPEECH
        print(f"VAD keeps {share:.0%} of the audio -> vad_filter={vad}")
    opts = dict(initial_prompt=prompt, vad_filter=vad, language=a.language,
                multilingual=a.multilingual or asr.get("multilingual", False))
    if hints == "none":
        segments, info = model.transcribe(audio, **opts)
        data, langs = [segment(s) for s in segments], [info.language]
    else:
        # one chunk per screen, from its start to the next screen's (the first chunk starts at 0), so no audio is skipped
        screens = json.load(open(L("screens.json")))
        bounds = [0.0] + [s["start"] for s in screens[1:]] + [len(audio) / SR]
        data, langs = [], []
        for s, t0, t1 in zip(screens, bounds, bounds[1:]):
            hw = screen_hints(s["text"], hints) or None
            segments, info = model.transcribe(audio[int(t0 * SR):int(t1 * SR)], hotwords=hw, **opts)
            data += [segment(x, t0, screen=s["id"]) for x in segments]
            langs.append(info.language)
    json.dump(data, open(L(a.out), "w"), ensure_ascii=False, indent=2)
    print(f"{len(data)} segments (screen hints: {hints}; detected {sorted(set(langs))}) ->", L(a.out))
