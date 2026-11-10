#!/usr/bin/env python3
"""
teacher_analytics.py — post-class report for the teacher, computed only from the lesson's outputs.

  1. Talk time (TTT/STT) from speakers.json. Measured only when diarization separated several speakers
     (source 'tracks' or 'pyannote'); a single-speaker recording is reported as "not measurable" instead of 100/0.
  2. Distribution of the learner errors detected in chat (feedback.py categories, with ERRANT types).
  3. Weakest concept: the grammar point whose questions (via exercise_id -> exercise_concept_links.json) attract
     the most chat messages with detected errors. None when there is no such evidence.
  4. Next-lesson suggestions: template sentences filled from 1-3 (no LLM; each line states its evidence).

Outputs <lesson>/teacher_report.json.
"""
import argparse
import collections
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from feedback import DESCRIPTION_VI, ERRANT_TYPE  # noqa: E402

ACTION_TEMPLATES = {
    "BE_VERB": "Warm-up 5 phút: cho lớp sửa nhanh các câu dạng 'I am agree', 'she is not understand' (thừa 'to be' trước động từ thường) — {n} lỗi trong chat.",
    "PARTICIPLE": "Ôn lại cặp tính từ -ing / -ed (boring/bored, confusing/confused) bằng 3 câu trắc nghiệm đầu giờ — {n} lỗi trong chat.",
    "CAUSATIVE": "Nhắc lại cấu trúc have/get + vật + V3/ed với 2 ví dụ trước khi làm bài mới — {n} lỗi trong chat.",
    "MODAL_TO": "Nhắc quy tắc modal + V nguyên mẫu không 'to' (should increase, can go) — {n} lỗi trong chat.",
    "SVA": "Luyện nhanh hòa hợp chủ ngữ ngôi 3 số ít (it makes, he goes, she doesn't) — {n} lỗi trong chat.",
    "WH_DO": "Luyện đặt câu hỏi Wh- có trợ động từ (Why do we...?, How does she...?) — {n} lỗi trong chat.",
}


def _load(path: Path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else default


def generate_teacher_report(lesson_dir: Path, out_name: str = "teacher_report.json") -> dict:
    lesson_dir = Path(lesson_dir)
    speakers = _load(lesson_dir / "speakers.json", {})
    chat_feedback = _load(lesson_dir / "chat_feedback.json", [])
    concept_links = _load(lesson_dir / "exercise_concept_links.json", [])
    lesson_meta = _load(lesson_dir / "lesson.json", {})
    grammar_points = {g["id"]: g for g in _load(lesson_dir / "grammar_points.json", [])}

    # 1. Talk time
    talk_time = speakers.get("talk_time", {})
    source = speakers.get("source", "unknown")
    measurable = source in ("tracks", "pyannote") and len(talk_time) > 1
    if measurable:
        t_sec = talk_time.get("T", 0.0)
        s_sec = sum(v for k, v in talk_time.items() if k != "T")
        t_pct = round(100.0 * t_sec / max(t_sec + s_sec, 1e-9), 1)
        s_pct = round(100.0 - t_pct, 1)
        if t_pct >= 90:
            assessment = f"Giáo viên nói {t_pct}% thời lượng (teacher-dominated); học viên tương tác chủ yếu qua chat."
        elif t_pct >= 70:
            assessment = f"Giáo viên nói {t_pct}%, học viên {s_pct}%: cân đối giữa giảng và phản hồi."
        else:
            assessment = f"Học viên nói {s_pct}% thời lượng: lớp có tính tương tác cao."
    else:
        t_pct = s_pct = None
        assessment = (f"Chưa đo được TTT/STT: bản ghi chỉ có một người nói (diarization source = '{source}'). "
                      "Cần bản ghi tách kênh từng người (Zoom 'record a separate audio file for each participant') "
                      "hoặc chạy pyannote trên bản ghi có nhiều người nói.")

    # 2. Error distribution by category
    student_ids = {c["speaker_id"] for c in chat_feedback if c.get("speaker_id", "").startswith("S")}
    by_cat = collections.defaultdict(list)
    for c in chat_feedback:
        for ed in c.get("edits", []):
            by_cat[ed.get("category") or ed.get("error_type")].append(ed.get("error_type"))
    total_errors = sum(len(v) for v in by_cat.values())
    error_distribution = []
    for cat, types in sorted(by_cat.items(), key=lambda kv: -len(kv[1])):
        error_distribution.append({
            "category": cat,
            "error_type": collections.Counter(types).most_common(1)[0][0] or ERRANT_TYPE.get(cat, ""),
            "count": len(types),
            "percentage": round(100.0 * len(types) / max(total_errors, 1), 1),
            "description": DESCRIPTION_VI.get(cat, "Lỗi ngữ pháp tiếng Anh"),
        })

    # 3. Weakest concept: error messages -> exercise_id -> linked grammar point
    link_by_q = {l["question_id"]: l for l in concept_links}
    evidence = collections.defaultdict(list)
    for c in chat_feedback:
        link = link_by_q.get(c.get("exercise_id"))
        if c.get("has_error") and link and link.get("grammar_point_id"):
            evidence[link["grammar_point_id"]].append(c.get("question_number"))
    weakest_concept = None
    if evidence:
        gp_id = max(evidence, key=lambda k: len(evidence[k]))
        gp = grammar_points.get(gp_id, {})
        n = len(evidence[gp_id])
        weakest_concept = {
            "concept_id": gp_id,
            "title": gp.get("title") or next(l["grammar_title"] for l in concept_links if l.get("grammar_point_id") == gp_id),
            "student_error_count": n,  # chat messages with >=1 detected error (not the number of errors)
            "questions": sorted({q for q in evidence[gp_id] if q is not None}),
            "theory_time_str": gp.get("time_str"),
            "severity": "HIGH" if n >= 2 else "MEDIUM",
            "evidence": "chat messages with detected errors on questions linked to this concept",
        }

    # 4. Suggestions from the evidence above
    plan = []
    for row in error_distribution[:2]:
        tpl = ACTION_TEMPLATES.get(row["category"])
        if tpl:
            plan.append(f"{len(plan) + 1}. " + tpl.format(n=row["count"]))
    if weakest_concept:
        qs = ", ".join(str(q) for q in weakest_concept["questions"]) or "?"
        plan.append(f"{len(plan) + 1}. Ôn lại chủ điểm '{weakest_concept['title']}' (đoạn lý thuyết ở "
                    f"{weakest_concept['theory_time_str']}); các câu có lỗi trong chat: {qs}.")
    if measurable and t_pct >= 90:
        plan.append(f"{len(plan) + 1}. Giảm thời gian giảng liên tục (TTT {t_pct}%): dành 3-5 phút cho học viên tự tìm từ khóa và trả lời.")
    elif not measurable:
        plan.append(f"{len(plan) + 1}. Buổi sau ghi âm tách kênh từng người để đo được tỷ lệ nói giáo viên / học viên.")

    report = {
        "class_meta": {
            "lesson_id": lesson_dir.name,
            "title": lesson_meta.get("title", lesson_dir.name),
            "total_students_active": len(student_ids),
            "total_chat_messages": len(chat_feedback),
            "total_errors_detected": total_errors,
        },
        "interaction_health": {
            "measured": measurable,
            "diarization_source": source,
            "teacher_talk_time_pct": t_pct,
            "student_talk_time_pct": s_pct,
            "assessment": assessment,
        },
        "error_distribution": error_distribution,
        "weakest_concept": weakest_concept,
        "next_lesson_action_plan": plan,
        "action_plan_method": "template sentences filled from the detected errors, concept links and talk time (no LLM)",
    }
    out_path = lesson_dir / out_name
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[teacher_analytics] Generated teacher report -> {out_path}")
    return report


def main():
    parser = argparse.ArgumentParser(description="Generate the post-class report for the teacher.")
    parser.add_argument("lesson_pos", nargs="?", default=None, help="Path to lesson directory (positional)")
    parser.add_argument("--lesson", default=None, help="Path to lesson directory (flag)")
    args = parser.parse_args()
    target_lesson = args.lesson or args.lesson_pos or "lessons/ece-toeic-starter-u4"
    lesson_dir = Path(target_lesson)
    if not lesson_dir.is_dir():
        print(f"Error: {lesson_dir} is not a directory", file=sys.stderr)
        sys.exit(1)
    generate_teacher_report(lesson_dir)


if __name__ == "__main__":
    main()
