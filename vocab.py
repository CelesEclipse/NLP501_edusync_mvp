"""Extract, profile (CEFR A1-C1), and produce 1-2s audio pronunciation clips for lesson vocabulary.
Scans screen OCR (screens.json) and teacher speech (transcript.json), detects teacher's Vietnamese definitions,
and slices crisp audio clips of the teacher pronouncing each target word into <lesson>/vocab_audio/<lemma>.wav.
Outputs <lesson>/vocab.json.
Usage: python vocab.py --lesson lessons/<id> [--audio] [--max-vocab 80] [--out vocab.json]"""
import argparse, json, os, re, wave
import numpy as np

VI_CHARS = re.compile(r"[ăâđêôơưàáạảãằắặẳẵầấậẩẫèéẹẻẽềếệểễìíịỉĩòóọỏõồốộổỗờớợởỡùúụủũừứựửữỳýỵỷỹ]", re.I)
BAD_DEF = re.compile(r"^(?:cộng|thì|các bạn|chúng ta|bị tác động|lưu ý|dễ dàng|ở đây|trong|với lại|tiếp theo|cứ bổ nghĩa|câu số|bài số|trang)\b", re.I)

VI_HOMOPHONES = {
    "hay", "con", "cho", "to", "ra", "va", "ve", "dung", "dong", "la", "ma", "co",
    "den", "di", "em", "anh", "chi", "chua", "roi", "nguoi", "mot", "hai", "ba",
    "bon", "nam", "sau", "bay", "tam", "chin", "muoi", "hi", "ph", "ha", "nha",
    "thi", "neu", "vi", "cau", "bai", "so", "trang"
}

STOPWORDS = set(
    "a an the and or but if because as what when where who whom which why how all any each few "
    "more most other some such no nor not only own same so than too very can will just should now "
    "of at by for with about against between into through during before after above below to from "
    "up down in out on off over under again further then once here there is are was were be been "
    "being have has had do does did i you he she it we they me him her us them my your his its "
    "our their this that these those am".split()
)

IRREGULAR = {
    "wrote": "write", "written": "write", "bought": "buy", "thought": "think",
    "taught": "teach", "caught": "catch", "felt": "feel", "found": "find",
    "heard": "hear", "paid": "pay", "said": "say", "sold": "sell",
    "sent": "send", "spent": "spend", "understood": "understand", "won": "win",
    "began": "begin", "begun": "begin", "chose": "choose", "chosen": "choose",
    "drove": "drive", "driven": "drive", "gave": "give", "given": "give",
    "knew": "know", "known": "know", "ran": "run", "saw": "see",
    "seen": "see", "spoke": "speak", "spoken": "speak", "took": "take", "taken": "take",
    "left": "leave", "lost": "lose", "met": "meet", "sat": "sit", "told": "tell"
}

CEFR_WEIGHTS = {"A1": 0.5, "A2": 1.5, "B1": 3.0, "B2": 4.0, "C1": 5.0, "C2": 4.0}


def load_cefr_lexicon(lexicon_path="data/cefr_lexicon.json"):
    """Load CEFR vocabulary profile dictionary."""
    if not os.path.exists(lexicon_path):
        return {}
    return json.load(open(lexicon_path))


def resolve_lemma(w, lexicon):
    """Normalize English word to base lemma using morphology and irregular verb rules."""
    w = w.lower().strip("'\"-")
    if not w or not re.match(r"^[a-z][a-z'-]+$", w) or len(w) < 2:
        return w, None
    if w in lexicon:
        return w, lexicon[w]
    if w in IRREGULAR and IRREGULAR[w] in lexicon:
        return IRREGULAR[w], lexicon[IRREGULAR[w]]
    # Plural / 3rd person singular forms
    if w.endswith("ies") and (w[:-3] + "y") in lexicon:
        return w[:-3] + "y", lexicon[w[:-3] + "y"]
    if w.endswith("es") and w[:-2] in lexicon:
        return w[:-2], lexicon[w[:-2]]
    if w.endswith("s") and w[:-1] in lexicon:
        return w[:-1], lexicon[w[:-1]]
    # Past tense / participles
    if w.endswith("ied") and (w[:-3] + "y") in lexicon:
        return w[:-3] + "y", lexicon[w[:-3] + "y"]
    if w.endswith("ed") and w[:-1] in lexicon:
        return w[:-1], lexicon[w[:-1]]
    if w.endswith("ed") and w[:-2] in lexicon:
        return w[:-2], lexicon[w[:-2]]
    # Gerund / progressive forms
    if w.endswith("ing") and (w[:-3] + "e") in lexicon:
        return w[:-3] + "e", lexicon[w[:-3] + "e"]
    if w.endswith("ing") and w[:-3] in lexicon:
        return w[:-3], lexicon[w[:-3]]
    return w, None


def extract_meanings_from_speech(transcript, lexicon):
    """Mine teacher's explicit bilingual definitions from classroom speech."""
    patterns = [
        re.compile(r"\b([A-Za-z][A-Za-z -]{1,20})\s+(?:có nghĩa là|nghĩa là|là)\s+([^\.,;\n]{2,35})", re.I),
        re.compile(r"(?:từ|động từ|danh từ|tính từ)\s+([A-Za-z][A-Za-z -]{1,20})\s+là\s+([^\.,;\n]{2,35})", re.I),
    ]
    meanings = {}

    for i, seg in enumerate(transcript):
        text = seg.get("text", "")
        for pat in patterns:
            for m in pat.finditer(text):
                raw_w = m.group(1).strip().lower()
                lemma, info = resolve_lemma(raw_w, lexicon)
                if info and lemma not in STOPWORDS and lemma not in VI_HOMOPHONES:
                    vi = m.group(2).strip()
                    vi = re.sub(r"^(?:là|nghĩa là|có nghĩa là)\s*", "", vi).strip()
                    if VI_CHARS.search(vi) and len(vi) >= 2 and not BAD_DEF.search(vi):
                        if lemma not in meanings or len(vi) > len(meanings[lemma][0]):
                            meanings[lemma] = (vi, seg["start"], text)

        # Check consecutive segments (e.g. Seg 1 = English word, Seg 2 = Vietnamese translation)
        if i + 1 < len(transcript):
            s1, s2 = seg, transcript[i + 1]
            t1 = s1.get("text", "").strip()
            t2 = s2.get("text", "").strip()
            t1_words = re.findall(r"[A-Za-z]+", t1)
            # If s1 is a short English word/phrase and s2 is Vietnamese within 2.5 seconds
            if t1_words and len(t1_words) <= 2 and not VI_CHARS.search(t1) and s2["start"] - s1["end"] <= 2.5:
                lemma, info = resolve_lemma(t1_words[0].lower(), lexicon)
                if info and lemma not in STOPWORDS and lemma not in VI_HOMOPHONES and lemma not in meanings:
                    t2_clean = re.sub(r"^(?:là|nghĩa là|có nghĩa là)\s*", "", t2).strip()
                    if VI_CHARS.search(t2_clean) and len(t2_clean) >= 2 and not BAD_DEF.search(t2_clean):
                        meanings[lemma] = (t2_clean, s1["start"], f"{t1} {t2}")

    return meanings


def find_audio_pronunciation_candidate(lemma, transcript):
    """Find the best audio snippet where the teacher clearly pronounces the target word."""
    candidates = []
    lemma_pat = re.compile(rf"\b{re.escape(lemma)}\b", re.I)

    for seg in transcript:
        text = seg.get("text", "")
        if not lemma_pat.search(text):
            continue

        words = re.findall(r"[a-zA-Z]+", text)
        dur = seg["end"] - seg["start"]

        # Quality tier 1: Standalone single word (e.g. "Prosperity.", "Written.")
        if len(words) == 1 and 0.3 <= dur <= 2.2:
            return seg["start"], seg["end"], text, 10.0

        # Quality tier 2: Short phrase (2-3 words) with duration <= 2.5s
        if 1 <= len(words) <= 3 and 0.4 <= dur <= 2.5:
            candidates.append((seg["start"], seg["end"], text, 7.0))
        # Quality tier 3: Longer sentence
        elif 0.5 <= dur <= 5.0:
            candidates.append((seg["start"], seg["end"], text, 3.0))

    if candidates:
        candidates.sort(key=lambda c: -c[3])
        return candidates[0]
    return None


def extract_vocabulary(screens, transcript, lexicon, max_vocab=80, min_score=2.5):
    """Profile lesson vocabulary across screen OCR and spoken explanations."""
    screen_freq = {}
    screen_sources = {}
    for s in screens:
        text = s.get("text", "")
        raw_words = set(re.findall(r"[a-zA-Z]{2,}", text.lower()))
        for rw in raw_words:
            if rw in STOPWORDS or rw in VI_HOMOPHONES:
                continue
            lemma, info = resolve_lemma(rw, lexicon)
            if info:
                screen_freq[lemma] = screen_freq.get(lemma, 0) + 1
                screen_sources.setdefault(lemma, set()).add(s["id"])

    speech_freq = {}
    speech_timestamps = {}
    for seg in transcript:
        text = seg.get("text", "")
        raw_words = set(re.findall(r"[a-zA-Z]{2,}", text.lower()))
        for rw in raw_words:
            if rw in STOPWORDS or rw in VI_HOMOPHONES:
                continue
            lemma, info = resolve_lemma(rw, lexicon)
            if info:
                speech_freq[lemma] = speech_freq.get(lemma, 0) + 1
                speech_timestamps.setdefault(lemma, []).append(seg["start"])

    # Combine unique lemmas
    all_lemmas = set(screen_freq.keys()) | set(speech_freq.keys())
    meanings = extract_meanings_from_speech(transcript, lexicon)

    items = []
    for lemma in all_lemmas:
        info = lexicon.get(lemma, {})
        level = info.get("level", "B1")
        pos = info.get("pos", "noun")

        s_count = screen_freq.get(lemma, 0)
        sp_count = speech_freq.get(lemma, 0)
        has_meaning = lemma in meanings
        audio_cand = find_audio_pronunciation_candidate(lemma, transcript)

        # Pedagogical ranking score
        score = (s_count * 3.0) + (sp_count * 1.5) + CEFR_WEIGHTS.get(level, 2.0)
        if has_meaning:
            score += 6.0
        if audio_cand and audio_cand[3] >= 7.0:
            score += 4.0

        if score < min_score:
            continue

        meaning_vi = meanings[lemma][0] if has_meaning else ""
        first_time = speech_timestamps[lemma][0] if lemma in speech_timestamps else None
        if has_meaning and meanings[lemma][1] is not None:
            first_time = meanings[lemma][1]
        elif audio_cand:
            first_time = audio_cand[0]

        context_example = meanings[lemma][2] if has_meaning else (audio_cand[2] if audio_cand else "")

        items.append({
            "word": lemma,
            "lemma": lemma,
            "level": level,
            "pos": pos,
            "meaning_vi": meaning_vi,
            "score": round(score, 1),
            "occurrences": {
                "screen_count": s_count,
                "speech_count": sp_count,
                "screens": sorted(list(screen_sources.get(lemma, [])))
            },
            "timestamp": round(first_time, 2) if first_time is not None else None,
            "audio_candidate": audio_cand,
            "example_context": context_example
        })

    # Sort descending by score, prioritizing words with teacher explanations
    items.sort(key=lambda it: (-it["score"], it["level"]))
    selected = items[:max_vocab]

    for idx, it in enumerate(selected):
        it["id"] = f"v_{idx + 1}"

    return selected


def slice_audio_clips(vocab_items, media_file, out_dir):
    """Slice 1-2s audio clips for vocabulary pronunciation using faster-whisper decode_audio."""
    from faster_whisper import decode_audio

    os.makedirs(out_dir, exist_ok=True)
    print(f"[vocab] Decoding {media_file} for audio pronunciation slicing...")
    SR = 16000
    audio = decode_audio(media_file, sampling_rate=SR)
    audio_dur = len(audio) / SR

    saved_count = 0
    for it in vocab_items:
        cand = it.pop("audio_candidate", None)
        if not cand:
            continue

        t0, t1, text, _ = cand
        # Add 0.15s padding before and after, clamp to 2.2s duration
        start_sec = max(0.0, t0 - 0.15)
        end_sec = min(audio_dur, t1 + 0.25)
        if end_sec - start_sec > 2.2:
            end_sec = start_sec + 2.2

        clip = audio[int(start_sec * SR):int(end_sec * SR)]
        pcm16 = (clip * 32767).clip(-32768, 32767).astype(np.int16)

        clip_name = f"{it['lemma']}.wav"
        clip_rel = os.path.join("vocab_audio", clip_name)
        clip_path = os.path.join(out_dir, clip_name)

        with wave.open(clip_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(SR)
            wf.writeframes(pcm16.tobytes())

        it["audio"] = clip_rel
        it["audio_duration"] = round(len(clip) / SR, 2)
        saved_count += 1

    print(f"[vocab] Sliced {saved_count} pronunciation clips into {out_dir}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lesson", default=".", help="lesson folder; all paths are relative to it")
    ap.add_argument("--lexicon", default="data/cefr_lexicon.json", help="CEFR lexicon file")
    ap.add_argument("--media", help="audio or video file (default: audio.m4a or video.mp4)")
    ap.add_argument("--no-audio", action="store_true", help="skip audio clip slicing")
    ap.add_argument("--max-vocab", type=int, default=80, help="max vocab entries")
    ap.add_argument("--min-score", type=float, default=2.5, help="minimum relevance score")
    ap.add_argument("--out", default="vocab.json", help="output json filename")
    a = ap.parse_args()
    L = lambda f: os.path.join(a.lesson, f)

    lexicon = load_cefr_lexicon(a.lexicon)
    if not lexicon and not os.path.isabs(a.lexicon):
        root_lex = os.path.join(os.path.dirname(os.path.abspath(__file__)), a.lexicon)
        lexicon = load_cefr_lexicon(root_lex)

    screens_file = L("screens.json")
    transcript_file = L("transcript.json")

    if not os.path.exists(screens_file) or not os.path.exists(transcript_file):
        print(f"[vocab] Missing {screens_file} or {transcript_file}; skipping.")
        exit(0)

    screens = json.load(open(screens_file))
    transcript = json.load(open(transcript_file))

    vocab_list = extract_vocabulary(screens, transcript, lexicon, max_vocab=a.max_vocab, min_score=a.min_score)
    print(f"[vocab] Extracted and profiled {len(vocab_list)} CEFR vocabulary items.")

    if not a.no_audio and vocab_list:
        media_file = a.media or ("audio.m4a" if os.path.exists(L("audio.m4a")) else "video.mp4")
        media_path = L(media_file)
        if os.path.exists(media_path):
            slice_audio_clips(vocab_list, media_path, L("vocab_audio"))
        else:
            print(f"[vocab] Audio media file {media_path} not found; skipping audio slicing.")

    out_path = L(a.out)
    json.dump(vocab_list, open(out_path, "w"), ensure_ascii=False, indent=2)
    print(f"[vocab] Wrote {len(vocab_list)} vocabulary items -> {out_path}")
