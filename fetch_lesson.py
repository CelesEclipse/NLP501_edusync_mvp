"""Download a YouTube lesson into lessons/<id>/ and write its lesson.json (source, licence, attribution).
Video and audio are fetched as two files (video.mp4 without sound, audio.m4a), so no ffmpeg is needed.
Videos that are not Creative Commons are refused unless --allow-standard (use that only with the owner's
permission). Files that already exist are not downloaded again.
Usage: python fetch_lesson.py thu4-KGapkA lessons/ece-toeic-starter-u1 --language vi --prompt "Luyện thi TOEIC ..." """
import argparse, json, os
from yt_dlp import YoutubeDL

ap = argparse.ArgumentParser()
ap.add_argument("video", help="YouTube id or URL")
ap.add_argument("lesson", help="lesson folder to create")
ap.add_argument("--language", default="vi", help="language the teacher explains in")
ap.add_argument("--target", default="en", help="language being taught")
ap.add_argument("--prompt", help="ASR prompt saved as lesson.json asr.prompt")
ap.add_argument("--asr-model", default="large-v3-turbo", help="Whisper model saved as lesson.json asr.model")
ap.add_argument("--multilingual", action="store_true", help="saved as lesson.json asr.multilingual")
ap.add_argument("--max-height", type=int, default=720)
ap.add_argument("--allow-standard", action="store_true", help="download a non-CC video (needs the owner's permission)")
a = ap.parse_args()

info = YoutubeDL({"quiet": True, "no_warnings": True}).extract_info(a.video, download=False)
licence = info.get("license") or "Standard YouTube License"
if "creative commons" not in licence.lower() and not a.allow_standard:
    raise SystemExit(f"{info['id']}: {licence} -> not downloaded (needs the owner's permission; see --allow-standard)")

os.makedirs(a.lesson, exist_ok=True)
for name, fmt in (("video.mp4", f"bv*[ext=mp4][height<={a.max_height}]"), ("audio.m4a", "ba[ext=m4a]")):
    path = os.path.join(a.lesson, name)
    if not os.path.exists(path):
        # downloads go to <name>.part and are renamed only when complete, so an existing file is a whole file
        YoutubeDL({"quiet": True, "no_warnings": True, "noprogress": True, "format": fmt,
                   "outtmpl": path}).download([info["webpage_url"]])
    print(f"{path}: {os.path.getsize(path) / 1e6:.0f} MB")

url = info["webpage_url"]
lesson = {
    "id": os.path.basename(os.path.normpath(a.lesson)),
    "title": info["title"],
    "source": url,
    "channel": info.get("channel"),
    "channel_url": info.get("channel_url"),
    "license": licence,
    "attribution": f"\"{info['title']}\" by {info.get('channel')} ({url}), {licence}",
    "upload_date": info.get("upload_date"),
    "duration": info.get("duration"),
    "language": {"instruction": a.language, "target": a.target},
    "files": {"video": "video.mp4", "audio": "audio.m4a"},
}
lesson["asr"] = {"model": a.asr_model, "multilingual": a.multilingual}
if a.prompt:
    lesson["asr"]["prompt"] = a.prompt
json.dump(lesson, open(os.path.join(a.lesson, "lesson.json"), "w"), ensure_ascii=False, indent=1)
print("->", os.path.join(a.lesson, "lesson.json"))
