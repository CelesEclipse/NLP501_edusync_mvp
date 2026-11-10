"""Download a lesson video into lessons/<id>/ and write its lesson.json (source, platform, licence, attribution).
Works for any site yt-dlp supports (YouTube, Vimeo, Internet Archive, PeerTube, Dailymotion, ...).
Video and audio are fetched as two files (video.mp4 without sound, audio.m4a), so no ffmpeg is needed; sites that
only offer one combined file are saved as video.mp4 alone (transcribe.py then reads the audio from it).
Videos without an open (Creative Commons / public-domain) licence are refused unless --allow-standard (use that
only with the owner's permission). Files that already exist are not downloaded again.
Usage: python fetch_lesson.py thu4-KGapkA lessons/ece-toeic-starter-u1 --language vi --prompt "Luyện thi TOEIC ..."
       python fetch_lesson.py https://vimeo.com/<id> lessons/<id> --cookies-from-browser chrome   (sites that need a login)"""
import argparse, json, os, re
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

# how the platforms write an open licence: YouTube "Creative Commons Attribution license (reuse allowed)",
# Vimeo "by-nc" / "cc0", Internet Archive "http://creativecommons.org/licenses/by/4.0/", PeerTube "Attribution - Share Alike"
CC_CODE = re.compile(r"^(cc[- ]?)?(by(-nc)?(-sa|-nd)?|cc0|pd|public[- ]domain.*)$", re.I)


def open_licence(licence):
    s = (licence or "").strip().lower()
    return bool(s) and ("creative commons" in s or "creativecommons.org" in s or s.startswith("attribution")
                        or s.startswith("public domain") or bool(CC_CODE.match(s)))


def fetch(url, path, fmt, opts):
    """Download one format into path; False if the site has no such format."""
    if os.path.exists(path):
        return True
    try:
        # downloads go to <name>.part and are renamed only when complete, so an existing file is a whole file
        YoutubeDL({**opts, "noprogress": True, "format": fmt, "outtmpl": path}).download([url])
        return os.path.exists(path)
    except DownloadError as e:
        if "Requested format is not available" in str(e):
            return False
        raise


ap = argparse.ArgumentParser()
ap.add_argument("video", help="YouTube id or any video URL yt-dlp supports")
ap.add_argument("lesson", help="lesson folder to create")
ap.add_argument("--language", default="vi", help="language the teacher explains in")
ap.add_argument("--target", default="en", help="language being taught")
ap.add_argument("--prompt", help="ASR prompt saved as lesson.json asr.prompt")
ap.add_argument("--asr-model", default="large-v3-turbo", help="Whisper model saved as lesson.json asr.model")
ap.add_argument("--multilingual", action="store_true", help="saved as lesson.json asr.multilingual")
ap.add_argument("--max-height", type=int, default=720)
ap.add_argument("--cookies-from-browser", help="browser to read the site's login cookies from (e.g. chrome)")
ap.add_argument("--allow-standard", action="store_true", help="download a non-CC video (needs the owner's permission)")
a = ap.parse_args()

opts = {"quiet": True, "no_warnings": True}
if a.cookies_from_browser:
    opts["cookiesfrombrowser"] = (a.cookies_from_browser,)
info = YoutubeDL(opts).extract_info(a.video, download=False)
platform = info.get("extractor_key") or info.get("extractor")
licence = info.get("license") or f"Standard {platform} licence (none stated)"
if not open_licence(info.get("license")) and not a.allow_standard:
    raise SystemExit(f"{info['id']}: {licence} -> not downloaded (needs the owner's permission; see --allow-standard)")

os.makedirs(a.lesson, exist_ok=True)
url = info["webpage_url"]
L = lambda f: os.path.join(a.lesson, f)
files = {"video": "video.mp4"}
if fetch(url, L("video.mp4"), f"bv*[ext=mp4][height<={a.max_height}]", opts):
    if fetch(url, L("audio.m4a"), "ba[ext=m4a]/ba", opts):
        files["audio"] = "audio.m4a"
else:  # one combined file (Vimeo progressive, Internet Archive, ...)
    fetch(url, L("video.mp4"), f"b[ext=mp4][height<={a.max_height}]/b[height<={a.max_height}]/b", opts)
for f in files.values():
    print(f"{L(f)}: {os.path.getsize(L(f)) / 1e6:.0f} MB")

channel = info.get("channel") or info.get("uploader")
lesson = {
    "id": os.path.basename(os.path.normpath(a.lesson)),
    "title": info["title"],
    "source": url,
    "platform": platform,
    "channel": channel,
    "channel_url": info.get("channel_url") or info.get("uploader_url"),
    "license": licence,
    "attribution": f"\"{info['title']}\" by {channel} ({url}), {licence}",
    "upload_date": info.get("upload_date"),
    "duration": info.get("duration"),
    "language": {"instruction": a.language, "target": a.target},
    "files": files,
}
lesson["asr"] = {"model": a.asr_model, "multilingual": a.multilingual}
if a.prompt:
    lesson["asr"]["prompt"] = a.prompt
json.dump(lesson, open(L("lesson.json"), "w"), ensure_ascii=False, indent=1)
print("->", L("lesson.json"))
