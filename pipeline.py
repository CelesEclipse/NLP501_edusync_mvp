"""Run the EduSync steps for one lesson folder, skipping steps whose outputs already exist.
Usage: python pipeline.py lessons/<id> [--force align links | --force all] [--dry-run]
A lesson folder holds the inputs (video.mp4, slides.pdf) and every step's output under a fixed name.
When gold/labels.json exists, the final alignment is scored against it at the end."""
import argparse, os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
# name, inputs, outputs, script + arguments (paths inside the lesson)
STEPS = [
    ("slides", ["slides.pdf"], ["slides.json"], ["parse_slides.py"]),
    ("visual", ["video.mp4", "slides.pdf"], ["visual.npz"], ["visual.py"]),
    ("transcribe", ["video.mp4"], ["transcript.json"], ["transcribe.py"]),
    ("align", ["transcript.json", "slides.json", "visual.npz"], ["alignment.json"],
     ["align.py", "--method", "bge-base", "--visual", "visual.npz"]),
    ("links", ["slides.json", "transcript.json", "alignment.json"], ["links.json"], ["link_materials.py"]),
]

ap = argparse.ArgumentParser()
ap.add_argument("lesson")
ap.add_argument("--force", nargs="+", default=[], choices=[s[0] for s in STEPS] + ["all"],
                help="rerun these steps even if their outputs exist")
ap.add_argument("--dry-run", action="store_true", help="only print what would run")
a = ap.parse_args()
if not os.path.isdir(a.lesson):
    sys.exit(f"no lesson folder {a.lesson}")
has = lambda f: os.path.exists(os.path.join(a.lesson, f))


def run(script, *args):
    cmd = [sys.executable, os.path.join(ROOT, script), *args, "--lesson", a.lesson]
    if subprocess.run(cmd).returncode:
        sys.exit(f"step failed: {' '.join(cmd)}")


for name, inputs, outputs, cmd in STEPS:
    forced = name in a.force or "all" in a.force
    if all(map(has, outputs)) and not forced:
        print(f"[{name}] skip, have {', '.join(outputs)}", flush=True)
        continue
    missing = [f for f in inputs if not has(f)]
    if missing:
        sys.exit(f"[{name}] missing {', '.join(missing)} in {a.lesson} "
                 f"(videos are not in git; see README)")
    print(f"[{name}] run {' '.join(cmd)}", flush=True)
    if not a.dry_run:
        run(*cmd)

if has("gold/labels.json") and has("alignment.json") and not a.dry_run:
    print("[evaluate] alignment.json vs gold/labels.json", flush=True)
    run("evaluate.py", "gold/labels.json", "alignment.json")
