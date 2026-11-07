"""Speaker diarization: assigns speaker labels (teacher 'T', students 'S1', 'S2'...) to speech turns.
Supports:
  1. Source 'tracks': separate audio files per participant in <lesson>/audio/*.m4a or *.wav (e.g. from Zoom
     'record separate audio for each participant'). Uses Silero VAD per track to find active turns.
  2. Source 'pyannote': pyannote.audio on single audio file when pyannote is installed and HF_TOKEN is valid.
  3. Source 'single_speaker': fallback when lesson has 1 speaker (e.g. lectures, ECE TOEIC recordings),
     assigning all segments to Teacher ('T').

Outputs <lesson>/speakers.json and updates <lesson>/transcript.json with 'speaker' field.
Usage: python diarize.py --lesson lessons/<id> [--source auto|tracks|pyannote|single] [--num-speakers N]"""
import argparse, glob, json, os, re, sys
import numpy as np
from faster_whisper import decode_audio
from faster_whisper.vad import get_speech_timestamps

SR = 16000


def vad_turns_from_audio(audio_path):
    """Run Silero VAD on an audio file and return list of (start_sec, end_sec)."""
    audio = decode_audio(audio_path, sampling_rate=SR)
    timestamps = get_speech_timestamps(audio, sampling_rate=SR)
    return [(round(t["start"] / SR, 2), round(t["end"] / SR, 2)) for t in timestamps]


def turns_from_tracks(audio_dir):
    """Process individual participant tracks from audio_dir -> (turns, participant_names)."""
    track_files = sorted(glob.glob(os.path.join(audio_dir, "*.m4a")) +
                         glob.glob(os.path.join(audio_dir, "*.wav")) +
                         glob.glob(os.path.join(audio_dir, "*.mp3")))
    if not track_files:
        return [], []

    raw_turns = []
    names = []
    for f in track_files:
        name = os.path.splitext(os.path.basename(f))[0]
        names.append(name)
        intervals = vad_turns_from_audio(f)
        for t0, t1 in intervals:
            if t1 - t0 >= 0.3:  # drop micro-noise < 300ms
                raw_turns.append({"raw_speaker": name, "start": t0, "end": t1})

    raw_turns.sort(key=lambda x: x["start"])
    return raw_turns, names


def run_pyannote(audio_path, num_speakers=None, hf_token=None):
    """Run pyannote.audio pipeline if available and authorized."""
    try:
        from pyannote.audio import Pipeline
        token = hf_token or os.environ.get("HF_TOKEN")
        if not token:
            token_path = os.path.expanduser("~/.cache/huggingface/token")
            if os.path.exists(token_path):
                token = open(token_path).read().strip()
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=token)
        opts = {"num_speakers": num_speakers} if num_speakers else {}
        diarization = pipeline(audio_path, **opts)
        turns = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            turns.append({"raw_speaker": speaker, "start": round(turn.start, 2), "end": round(turn.end, 2)})
        return turns
    except Exception as e:
        print(f"[diarize] pyannote failed: {e}")
        return None


def assign_roles(raw_turns, forced_teacher=None):
    """Rank speakers by total speech duration. Top speaker is Teacher 'T', others 'S1', 'S2'..."""
    durations = {}
    for t in raw_turns:
        spk = t["raw_speaker"]
        durations[spk] = durations.get(spk, 0.0) + (t["end"] - t["start"])

    if not durations:
        return {}, {}, []

    ranked = sorted(durations.keys(), key=lambda k: -durations[k])
    mapping = {}
    roles = {}

    teacher_raw = forced_teacher if forced_teacher in ranked else ranked[0]
    mapping[teacher_raw] = "T"
    roles["T"] = "teacher"

    s_idx = 1
    for spk in ranked:
        if spk != teacher_raw:
            label = f"S{s_idx}"
            mapping[spk] = label
            roles[label] = "student"
            s_idx += 1

    mapped_turns = []
    for t in raw_turns:
        mapped_turns.append({
            "speaker": mapping[t["raw_speaker"]],
            "raw_speaker": t["raw_speaker"],
            "start": t["start"],
            "end": t["end"]
        })

    return mapping, roles, mapped_turns


def match_speakers_to_transcript(transcript, turns, default_speaker="T"):
    """For each segment in transcript, assign speaker with maximum time overlap in turns."""
    if not turns:
        for seg in transcript:
            seg["speaker"] = default_speaker
        return transcript

    for seg in transcript:
        s0, s1 = seg["start"], seg["end"]
        overlaps = {}
        for turn in turns:
            t0, t1 = turn["start"], turn["end"]
            overlap = max(0.0, min(s1, t1) - max(s0, t0))
            if overlap > 0:
                spk = turn["speaker"]
                overlaps[spk] = overlaps.get(spk, 0.0) + overlap

        if overlaps:
            seg["speaker"] = max(overlaps.keys(), key=lambda k: overlaps[k])
        else:
            # find closest turn
            mid = (s0 + s1) / 2
            closest = min(turns, key=lambda t: min(abs(mid - t["start"]), abs(mid - t["end"])))
            seg["speaker"] = closest["speaker"]

    return transcript


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lesson", default=".", help="lesson folder; all paths are relative to it")
    ap.add_argument("--source", choices=["auto", "tracks", "pyannote", "single"], default="auto",
                    help="diarization source: tracks (audio/ folder), pyannote, single speaker, or auto")
    ap.add_argument("--num-speakers", type=int, help="hint for pyannote")
    ap.add_argument("--teacher", help="name or raw speaker ID to force as teacher role")
    a = ap.parse_args()
    L = lambda f: os.path.join(a.lesson, f)

    lesson_meta = json.load(open(L("lesson.json"))) if os.path.exists(L("lesson.json")) else {}
    audio_dir = L("audio")
    audio_file = L("audio.m4a") if os.path.exists(L("audio.m4a")) else (L("audio.wav") if os.path.exists(L("audio.wav")) else L("video.mp4"))

    source = a.source
    if source == "auto":
        if os.path.isdir(audio_dir) and len(glob.glob(os.path.join(audio_dir, "*.*"))) > 1:
            source = "tracks"
        elif a.num_speakers and a.num_speakers > 1:
            source = "pyannote"
        else:
            source = "single"

    print(f"[diarize] Using source mode: {source} for {a.lesson}")
    raw_turns = []

    if source == "tracks":
        raw_turns, names = turns_from_tracks(audio_dir)
        print(f"[diarize] Found {len(raw_turns)} speech turns across {len(names)} track(s): {names}")
    elif source == "pyannote":
        raw_turns = run_pyannote(audio_file, num_speakers=a.num_speakers)
        if raw_turns is None:
            print("[diarize] Fallback to single-speaker mode.")
            source = "single"

    if source == "single" or not raw_turns:
        source = "single"
        # single speaker lecture: use VAD on main audio or full duration
        if os.path.exists(audio_file):
            vad_intervals = vad_turns_from_audio(audio_file)
            raw_turns = [{"raw_speaker": "T", "start": t0, "end": t1} for t0, t1 in vad_intervals]
        else:
            raw_turns = [{"raw_speaker": "T", "start": 0.0, "end": 999999.0}]

    mapping, roles, turns = assign_roles(raw_turns, forced_teacher=a.teacher)

    talk_time = {}
    for t in turns:
        spk = t["speaker"]
        talk_time[spk] = round(talk_time.get(spk, 0.0) + (t["end"] - t["start"]), 2)

    speakers_data = {
        "source": source,
        "roles": roles,
        "talk_time": talk_time,
        "turns": turns
    }

    out_speakers = L("speakers.json")
    json.dump(speakers_data, open(out_speakers, "w"), ensure_ascii=False, indent=2)
    print(f"[diarize] Wrote {len(turns)} turns, talk times: {talk_time} -> {out_speakers}")

    # update transcript if present
    tr_path = L("transcript.json")
    if os.path.exists(tr_path):
        tr = json.load(open(tr_path))
        tr = match_speakers_to_transcript(tr, turns)
        json.dump(tr, open(tr_path, "w"), ensure_ascii=False, indent=2)
        print(f"[diarize] Updated {len(tr)} transcript segments with speaker tags in {tr_path}")
