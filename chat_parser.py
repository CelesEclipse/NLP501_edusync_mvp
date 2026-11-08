"""Parse, anonymize, and align online classroom chat logs (Zoom/Meet) to lecture timeline.
Reads <lesson>/chat.txt and maps student names to anonymous identifiers (S1, S2, ...).
Associates chat messages with corresponding exercise questions based on regex and timestamps.
Outputs <lesson>/chat.json.
Usage: python chat_parser.py --lesson lessons/<id> [--out chat.json]"""
import argparse, json, os, re


def parse_timestamp(time_str):
    """Convert HH:MM:SS or MM:SS to float seconds."""
    parts = [int(p) for p in time_str.strip().split(":")]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    elif len(parts) == 2:
        return parts[0] * 60 + parts[1]
    return 0.0


def parse_chat_log(text):
    """Parse Zoom or Google Meet style chat text into raw entries."""
    # Pattern 1: Zoom format:
    # 00:03:12 From Nguyen Hoang Minh to Everyone:
    # Message body...
    # or single line
    zoom_pattern = re.compile(
        r"^(\d{1,2}:\d{2}:\d{2})\s+From\s+([^:]+?)\s+to\s+[^:]+:\s*(.*)$",
        re.MULTILINE
    )

    # Split lines and parse blocks
    entries = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        zm = zoom_pattern.match(line)
        if zm:
            t_str, sender, inline_msg = zm.groups()
            msg_lines = [inline_msg] if inline_msg else []
            # Gather subsequent lines until next header
            i += 1
            while i < len(lines):
                nxt = lines[i].strip()
                if not nxt:
                    i += 1
                    continue
                if zoom_pattern.match(nxt):
                    break
                msg_lines.append(nxt)
                i += 1
            msg = " ".join(msg_lines).strip()
            entries.append({
                "time_str": t_str,
                "timestamp": parse_timestamp(t_str),
                "sender": sender.strip(),
                "message": msg
            })
        else:
            # Fallback format: [00:03:12] Sender: Message
            m = re.match(r"^\[?(\d{1,2}:\d{2}(?::\d{2})?)\]?\s+([^:]+):\s*(.*)$", line)
            if m:
                t_str, sender, msg = m.groups()
                entries.append({
                    "time_str": t_str,
                    "timestamp": parse_timestamp(t_str),
                    "sender": sender.strip(),
                    "message": msg.strip()
                })
            i += 1

    return entries


def anonymize_and_link(entries, exercises=None):
    """Anonymize student names to S1, S2, ... and link messages to exercises."""
    speaker_map = {}
    next_id = 1

    linked = []
    for idx, e in enumerate(entries):
        raw_name = e["sender"]
        if raw_name not in speaker_map:
            # Check if teacher
            if "teacher" in raw_name.lower() or "giáo viên" in raw_name.lower():
                speaker_map[raw_name] = {"id": "T", "name": "Teacher"}
            else:
                s_id = f"S{next_id}"
                speaker_map[raw_name] = {"id": s_id, "name": f"Student {next_id}"}
                next_id += 1

        spk_info = speaker_map[raw_name]
        msg = e["message"]
        t = e["timestamp"]

        # 1. Detect question number in message (e.g. "Câu 4", "Q4", "Text 1 câu 1")
        ex_num = None
        m_q = re.search(r"\b(?:câu|question|q)\s*(\d+)\b", msg, re.I)
        if m_q:
            ex_num = int(m_q.group(1))

        # 2. Match with aligned exercises
        matched_ex_id = None
        if exercises:
            # First try matching by explicit question number
            if ex_num is not None:
                # Find exercise matching this question number nearest in time
                cands = [x for x in exercises if x.get("number") == ex_num]
                if cands:
                    cands.sort(key=lambda c: abs(c.get("start", 0) - t))
                    matched_ex_id = cands[0].get("id")

            # Fallback: if no explicit number, match by active exercise window
            if not matched_ex_id:
                for x in exercises:
                    if x.get("start", 0) - 15.0 <= t <= x.get("end", x.get("start", 0) + 60.0) + 30.0:
                        matched_ex_id = x.get("id")
                        if ex_num is None:
                            ex_num = x.get("number")
                        break

        linked.append({
            "id": f"c_{idx + 1}",
            "timestamp": t,
            "time_str": e["time_str"],
            "speaker_id": spk_info["id"],
            "speaker_name": spk_info["name"],
            "message": msg,
            "question_number": ex_num,
            "exercise_id": matched_ex_id
        })

    return linked, speaker_map


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lesson", default=".", help="lesson folder; all paths are relative to it")
    ap.add_argument("--chat", default="chat.txt", help="chat log filename")
    ap.add_argument("--out", default="chat.json", help="output json filename")
    a = ap.parse_args()
    L = lambda f: os.path.join(a.lesson, f)

    chat_file = L(a.chat)
    if not os.path.exists(chat_file):
        print(f"[chat_parser] No chat log found at {chat_file}; skipping.")
        exit(0)

    raw_text = open(chat_file, "r", encoding="utf-8").read()
    raw_entries = parse_chat_log(raw_text)

    # Load exercises if present
    ex_file = L("exercise_alignment.json")
    if not os.path.exists(ex_file):
        ex_file = L("exercises.json")
    exercises = json.load(open(ex_file)) if os.path.exists(ex_file) else []

    parsed_chat, spk_map = anonymize_and_link(raw_entries, exercises)

    out_path = L(a.out)
    json.dump(parsed_chat, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"[chat_parser] Parsed {len(parsed_chat)} chat messages from {len(spk_map)} speakers -> {out_path}")
