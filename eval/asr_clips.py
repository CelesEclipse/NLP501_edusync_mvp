"""Reference clips for WER: cuts --n clips of --seconds, spread evenly over the lesson, from its audio to
gold/asr/clip_NN.wav, plus clip_NN.txt holding a draft transcript to correct by ear (one paragraph; keep the
Vietnamese diacritics; write English words as the teacher says them). gold/asr/clips.json lists the windows.
The draft comes from --draft (default: the plain transcript without screen hints), so any bias of
post-editing favours that system: if a hinted transcript still scores better, the gain is not an artefact.
Usage: python eval/asr_clips.py --lesson lessons/<id> [--draft results/asr_none.json] [--n 5] [--seconds 120]"""
import argparse, json, os, wave
import numpy as np
from faster_whisper import decode_audio

if __name__ == "__main__":
    SR = 16000
    ap = argparse.ArgumentParser()
    ap.add_argument("--lesson", default=".", help="lesson folder; the other paths are relative to it")
    ap.add_argument("--draft", default="results/asr_none.json")
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--seconds", type=float, default=120)
    ap.add_argument("--media", help="default: audio.m4a if the lesson has one, else video.mp4")
    a = ap.parse_args()
    L = lambda f: os.path.join(a.lesson, f)

    audio = decode_audio(L(a.media or ("audio.m4a" if os.path.exists(L("audio.m4a")) else "video.mp4")), sampling_rate=SR)
    dur, draft = len(audio) / SR, json.load(open(L(a.draft)))
    os.makedirs(L("gold/asr"), exist_ok=True)
    clips = []
    for i, c in enumerate(np.linspace(0, 1, a.n + 2)[1:-1], 1):  # centres at 1/(n+1), 2/(n+1), ... of the lesson
        t0 = round(max(0.0, c * dur - a.seconds / 2), 1)
        t1 = round(min(dur, t0 + a.seconds), 1)
        with wave.open(L(f"gold/asr/clip_{i:02d}.wav"), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((np.clip(audio[int(t0 * SR):int(t1 * SR)], -1, 1) * 32767).astype(np.int16).tobytes())
        text = " ".join(s["text"] for s in draft if t0 <= (s["start"] + s["end"]) / 2 < t1)
        txt = L(f"gold/asr/clip_{i:02d}.txt")
        if os.path.exists(txt):
            print("keeping", txt, "(already corrected?)")
        else:
            open(txt, "w").write(text + "\n")
        clips.append({"clip": i, "start": t0, "end": t1, "wav": f"gold/asr/clip_{i:02d}.wav", "ref": f"gold/asr/clip_{i:02d}.txt"})
    json.dump({"draft": a.draft, "corrected": False, "clips": clips}, open(L("gold/asr/clips.json"), "w"), indent=1)
    print(f"{len(clips)} clips of {a.seconds:.0f} s -> {L('gold/asr')}; correct the .txt files, then set corrected: true in clips.json")
