"""Run the EduSync steps for one lesson folder, skipping steps whose outputs already exist.
Usage: python pipeline.py lessons/<id> [--force align links | --force all] [--dry-run]
A lesson folder holds the inputs and every step's output under a fixed name. With slides.pdf the lesson is
aligned to its slides (when gold/labels.json exists, the alignment is scored at the end); without one,
the screens are extracted from the video and combined with the transcript into content.md."""
import argparse, os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
AUDIO = ("audio.m4a", "video.mp4")  # either one will do
# name, inputs, outputs, script + arguments (paths inside the lesson), when: "pdf" | "no-pdf" | "any"
STEPS = [
    ("slides", ["slides.pdf"], ["slides.json"], ["parse_slides.py"], "pdf"),
    ("visual", ["video.mp4", "slides.pdf"], ["visual.npz"], ["visual.py"], "pdf"),
    ("screens", ["video.mp4"], ["screens.json"], ["extract_screens.py"], "no-pdf"),
    ("transcribe", [AUDIO], ["transcript.json"], ["transcribe.py"], "any"),
    ("diarize", ["transcript.json"], ["speakers.json"], ["diarize.py"], "any"),
    ("align", ["transcript.json", "slides.json", "visual.npz"], ["alignment.json"],
     ["align.py", "--method", "bge-base", "--visual", "visual.npz"], "pdf"),
    ("links", ["slides.json", "transcript.json", "alignment.json"], ["links.json"], ["link_materials.py"], "pdf"),
    ("exercises", ["screens.json"], ["exercises.json"], ["exercises.py"], "no-pdf"),
    ("exercise_align", ["exercises.json", "transcript.json"], ["exercise_alignment.json"], ["exercise_align.py"], "no-pdf"),
    ("vocab", ["screens.json", "transcript.json"], ["vocab.json"], ["vocab.py"], "no-pdf"),
    ("chat", ["chat.txt"], ["chat.json"], ["chat_parser.py"], "no-pdf"),
    ("feedback", ["chat.json"], ["chat_feedback.json"], ["feedback.py"], "no-pdf"),
    ("neural_ie", ["transcript.json", "exercises.json"], ["grammar_points.json", "vocab_deep.json"], ["neural_ie.py"], "no-pdf"),
    ("concept_link", ["exercises.json", "grammar_points.json"], ["exercise_concept_links.json"], ["concept_link.py"], "no-pdf"),
    ("teacher_analytics", ["speakers.json", "chat_feedback.json"], ["teacher_report.json"], ["teacher_analytics.py"], "no-pdf"),
    ("content", ["screens.json", "transcript.json"], ["content.md"], ["lesson_content.py"], "no-pdf"),
]

ap = argparse.ArgumentParser()
ap.add_argument("lesson")
ap.add_argument("--force", nargs="+", default=[], choices=[s[0] for s in STEPS] + ["all"],
                help="rerun these steps even if their outputs exist")
ap.add_argument("--dry-run", action="store_true", help="only print what would run")
a = ap.parse_args()
if not os.path.isdir(a.lesson):
    sys.exit(f"no lesson folder {a.lesson}")
has = lambda f: any(map(has, f)) if isinstance(f, tuple) else os.path.exists(os.path.join(a.lesson, f))
profile = "pdf" if has("slides.pdf") else "no-pdf"


def run(script, *args):
    cmd = [sys.executable, os.path.join(ROOT, script), *args, "--lesson", a.lesson]
    if subprocess.run(cmd).returncode:
        sys.exit(f"step failed: {' '.join(cmd)}")


planned = set()  # outputs of the steps run in this pass, so later steps may rely on them
ready = lambda f: has(f) or (any(x in planned for x in f) if isinstance(f, tuple) else f in planned)
for name, inputs, outputs, cmd, when in STEPS:
    if when not in ("any", profile):
        continue
    if name in ("chat", "feedback") and not (has("chat.txt") or has("chat.json")):
        continue
    forced = name in a.force or "all" in a.force
    if all(map(has, outputs)) and not forced:
        print(f"[{name}] skip, have {', '.join(outputs)}", flush=True)
        continue
    planned.update(outputs)
    missing = [" or ".join(f) if isinstance(f, tuple) else f for f in inputs if not ready(f)]
    if missing:
        sys.exit(f"[{name}] missing {', '.join(missing)} in {a.lesson} "
                 f"(videos are not in git; see README)")
    print(f"[{name}] run {' '.join(cmd)}", flush=True)
    if not a.dry_run:
        run(*cmd)

if has("gold/labels.json") and has("alignment.json") and not a.dry_run:
    print("[evaluate] alignment.json vs gold/labels.json", flush=True)
    run("evaluate.py", "gold/labels.json", "alignment.json")
