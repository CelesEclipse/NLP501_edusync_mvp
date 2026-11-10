"""Rule-based detector and corrector for six error patterns typical of Vietnamese learners (L1 transfer) in English
chat messages, with Vietnamese explanations. Outputs <lesson>/chat_feedback.json.

Scope and honesty notes
  - This is a pattern detector, not a general GEC model: it only finds the six categories below and misses every
    other error. eval/eval_gec.py measures it on a held-out set written independently of these rules.
  - Each edit carries our category tag and an ERRANT error type (Bryant, Felice & Briscoe, ACL 2017). If the
    official `errant` package is installed, the type is computed by errant on the (original, corrected) message pair.
    Otherwise the category's default type below is used; the defaults are what errant 3.0.2 assigns to the
    canonical example pairs (eval/errant_check.py, output in eval/results/errant_check.txt). errant can give a
    neighbouring type for other pairs (e.g. R:MORPH for "confusing -> confused", R:OTHER for "don't -> doesn't").

Categories
  BE_VERB     unnecessary "be" before a lexical verb          "I am agree"            -> "I agree"
  PARTICIPLE  -ing / -ed / base form of an emotion adjective  "The lesson was bored"  -> "The lesson was boring"
  CAUSATIVE   have/get + thing + base verb                    "have my car repair"    -> "have my car repaired"
  MODAL_TO    "to" after a modal verb                         "should to increase"    -> "should increase"
  SVA         he/she/it + base verb                           "it make me cry"        -> "it makes me cry"
  WH_DO       wh-question without do/does                     "Why we use -ing?"      -> "Why do we use -ing?"

Usage: python feedback.py --lesson lessons/<id> [--out chat_feedback.json]"""
import argparse, json, os, re

VI_CHARS = re.compile(r"[ăâđêôơưàáạảãằắặẳẵầấậẩẫèéẹẻẽềếệểễìíịỉĩòóọỏõồốộổỗờớợởỡùúụủũừứựửữỳýỵỷỹ]", re.I)

# ERRANT type of each category's canonical pair, as produced by the errant toolkit (see module docstring).
ERRANT_TYPE = {
    "BE_VERB": "U:VERB:TENSE",
    "PARTICIPLE": "R:VERB:FORM",
    "CAUSATIVE": "R:VERB:FORM",
    "MODAL_TO": "U:VERB:FORM",
    "SVA": "R:VERB:SVA",
    "WH_DO": "M:VERB:TENSE",
}

try:  # optional: exact ERRANT typing when the toolkit is installed
    import errant as _errant
    _ANNOTATOR = _errant.load("en")
except Exception:  # not installed, or spaCy model missing
    _ANNOTATOR = None


def errant_types(original, corrected):
    """ERRANT types of the edits between two strings, or [] when errant is unavailable."""
    if _ANNOTATOR is None:
        return []
    try:
        return [e.type for e in _ANNOTATOR.annotate(_ANNOTATOR.parse(original), _ANNOTATOR.parse(corrected))]
    except Exception:
        return []

DESCRIPTION_VI = {
    "BE_VERB": "Thừa 'to be' trước động từ thường (vd: 'I am agree')",
    "PARTICIPLE": "Nhầm tính từ đuôi -ing (tính chất) / -ed (cảm xúc) hoặc dùng động từ nguyên mẫu (vd: 'I am confusing')",
    "CAUSATIVE": "Sai dạng động từ trong cấu trúc nhờ vả have/get + vật + V3/ed (vd: 'have my car repair')",
    "MODAL_TO": "Thừa 'to' sau động từ khuyết thiếu (vd: 'should to increase')",
    "SVA": "Sai hòa hợp chủ ngữ ngôi 3 số ít – động từ (vd: 'it make me cry')",
    "WH_DO": "Thiếu trợ động từ do/does trong câu hỏi Wh- (vd: 'Why we use...?')",
}

# ---------------------------------------------------------------- lexicons -------------------------------------
PRONOUN_PERSON = {"i", "you", "we", "they", "he", "she"}
PERSON_NOUNS = set("""baby babies child children kid kids people person student students teacher teachers customer
customers guest guests manager managers employee employees staff audience everyone everybody someone somebody man woman
men women boy boys girl girls friend friends parent parents class team boss mother father mom dad sister brother
learner learners viewers readers fans players""".split())
EMOTION = set("""bore interest excite confuse annoy tire please surprise disappoint embarrass frighten amaze satisfy worry
frustrate exhaust amuse shock terrify relax depress fascinate thrill overwhelm move irritate puzzle astonish scare
delight""".split())
COMMON_VERBS = set("""agree disagree understand know think like love hate want need come go live work study remember
forget believe mean see hear feel have make do take give get use say tell try ask call keep start show help play run
read write speak watch explain cry learn teach sell buy pay meet cost open close finish begin leave bring find look
listen answer choose prefer enjoy depend belong contain include seem become happen wait walk talk sleep eat drink
practice practise""".split())
CAUSATIVE_VERBS = set("""repair fix clean cut check wash paint deliver shine print translate review install type correct
change service photocopy design build sign test mark grade publish send cook iron polish dye style decorate renovate
replace remove inspect update edit format proofread copy repaint deliver""".split())
PAST_PARTICIPLE = {"cut": "cut", "put": "put", "set": "set", "hit": "hit", "build": "built", "send": "sent",
                   "make": "made", "do": "done", "write": "written", "take": "taken", "give": "given", "buy": "bought",
                   "bring": "brought", "teach": "taught", "sell": "sold", "tell": "told", "shine": "shined",
                   "dye": "dyed", "proofread": "proofread", "read": "read", "pay": "paid", "find": "found",
                   "speak": "spoken", "eat": "eaten", "see": "seen", "know": "known", "go": "gone", "come": "come",
                   "begin": "begun", "drink": "drunk", "choose": "chosen", "forget": "forgotten",
                   "understand": "understood", "think": "thought", "feel": "felt", "leave": "left", "meet": "met",
                   "sleep": "slept", "keep": "kept", "run": "run", "get": "got", "have": "had", "say": "said",
                   "hear": "heard", "mean": "meant", "lose": "lost", "stand": "stood", "sit": "sat"}
PAST_SIMPLE = {"go": "went", "come": "came", "see": "saw", "eat": "ate", "drink": "drank", "speak": "spoke",
               "write": "wrote", "take": "took", "give": "gave", "begin": "began", "choose": "chose",
               "forget": "forgot", "know": "knew", "run": "ran", "get": "got"}
MODALS = "can't|cannot|won't|wouldn't|shouldn't|couldn't|mustn't|should|can|could|will|would|must|may|might|shall"
BE = r"(?:\s+(?:am|is|are|was|were)|'m|'re|'s)"   # with its leading space, so contractions (I'm, he's) match
# verbs that are also common adjectives/nouns/prepositions after "be" ("he's like his father", "it is open")
AMBIGUOUS_AFTER_BE = {"like", "mean", "open", "close", "live", "work", "practice", "practise", "answer", "show", "look"}
INTENS = r"(?:(?:very|so|really|quite|too|extremely|a\s+bit|kind\s+of)\s+)?"
DET = r"(?:the|this|that|these|those|my|your|our|their|his|her|its|a|an)"
NO_SUBJ_VERB_AFTER = set("make makes made let lets help helps have has had watch see saw hear heard to did does do "
                         "will would can could should must may might shall".split())


def _vowel(c):
    return c in "aeiou"


def ed_form(v):
    """Regular -ed spelling for the verbs used here (tire->tired, worry->worried, stop->stopped)."""
    if v.endswith("e"):
        return v + "d"
    if v.endswith("y") and not _vowel(v[-2]):
        return v[:-1] + "ied"
    if len(v) <= 4 and not _vowel(v[-1]) and _vowel(v[-2]) and not _vowel(v[-3]) and v[-1] not in "wxy":
        return v + v[-1] + "ed"
    return v + "ed"


def ing_form(v):
    if v.endswith("ie"):
        return v[:-2] + "ying"
    if v.endswith("e") and not v.endswith("ee"):
        return v[:-1] + "ing"
    return v + "ing"


def past_participle(v):
    return PAST_PARTICIPLE.get(v, ed_form(v))


def past_simple(v):
    return PAST_SIMPLE.get(v, PAST_PARTICIPLE.get(v) if v in ("make", "do", "buy", "say", "think", "feel") and v != "do"
                           else ed_form(v)) if v != "do" else "did"


def third_person(v):
    if v == "have":
        return "has"
    if v == "do":
        return "does"
    if v == "go":
        return "goes"
    if re.search(r"(s|sh|ch|x|z|o)$", v):
        return v + "es"
    if v.endswith("y") and not _vowel(v[-2]):
        return v[:-1] + "ies"
    return v + "s"


def base_from_third(v):
    """Undo 3rd-person -s for COMMON_VERBS (goes->go, studies->study, has->have)."""
    if v == "has":
        return "have"
    if v == "does":
        return "do"
    for cand in (v[:-3] + "y" if v.endswith("ies") else None, v[:-2] if v.endswith("es") else None,
                 v[:-1] if v.endswith("s") else None):
        if cand and cand in COMMON_VERBS:
            return cand
    return None


EMO_BASE = {e: e for e in EMOTION}
EMO_ING = {ing_form(e): e for e in EMOTION}
EMO_ED = {ed_form(e): e for e in EMOTION}


def _keep_case(src, rep):
    return rep[0].upper() + rep[1:] if src[:1].isupper() and rep else rep


# ---------------------------------------------------------------- rules ----------------------------------------
class GECRuleEngine:
    """Six pattern rules. check_sentence() returns (edits, corrected_text)."""

    def __init__(self):
        verbs = "|".join(sorted(COMMON_VERBS, key=len, reverse=True))
        be_verbs = "|".join(sorted(COMMON_VERBS - AMBIGUOUS_AFTER_BE, key=len, reverse=True))
        emo_ing = "|".join(sorted(EMO_ING, key=len, reverse=True))
        emo_ed = "|".join(sorted(EMO_ED, key=len, reverse=True))
        emo_base = "|".join(sorted(EMO_BASE, key=len, reverse=True))
        caus = "|".join(sorted(CAUSATIVE_VERBS, key=len, reverse=True))
        self.rules = [
            # BE_VERB: subject + be (+ not) + lexical base verb  ("I am agree", "she is not understand")
            ("BE_VERB", re.compile(rf"\b(i|you|we|they|he|she|it)({BE})\s+(not\s+)?({be_verbs})\b(?!-)", re.I),
             self._fix_be_verb,
             "'{v}' là động từ thường nên không đi kèm 'to be' (lỗi dịch từng từ 'tôi thì đồng ý'). Phủ định dùng do/does/did + not."),
            # PARTICIPLE (a): person subject + be/feel + emotion V-ing  ("I am confusing", "we felt boring")
            ("PARTICIPLE", re.compile(rf"\b(i|we|you|they|{'|'.join(PERSON_NOUNS)})(\s+(?:am|are|was|were|feel|feels|felt|get|got|become|became)|'m|'re)\s+{INTENS}({emo_ing})\b", re.I),
             lambda m: self._swap_last(m, EMO_ING, ed_form),
             "Khi nói về cảm xúc của người, dùng tính từ đuôi -ed ('{fix}'); đuôi -ing ('{orig}') mô tả tính chất gây ra cảm xúc."),
            # PARTICIPLE (b): thing subject + be + emotion V-ed  ("the lesson was bored", "movie was moved")
            ("PARTICIPLE", re.compile(rf"\b(?:{DET}\s+)?([a-z]+)(\s+(?:is|was|are|were)|'s)\s+{INTENS}({emo_ed})\b(?!\s+(?:to|from|by|into|out|away|with|about|at|in|of|that)\b)", re.I),
             lambda m: None if (m.group(1).lower() in PERSON_NOUNS | PRONOUN_PERSON | {"it", "who", "that", "i"}) else self._swap_last(m, EMO_ED, ing_form),
             "Chủ ngữ là sự vật/sự việc gây ra cảm xúc nên dùng tính từ đuôi -ing ('{fix}'), không dùng -ed ('{orig}')."),
            # PARTICIPLE (c): be + emotion base verb  ("this noise is very annoy", "I am very interest")
            ("PARTICIPLE", re.compile(rf"\b([a-z]+)({BE}|\s+(?:feel|feels|felt))\s+{INTENS}({emo_base})\b(?!-)", re.I),
             self._fix_emo_base,
             "Sau 'to be/feel' cần tính từ, không dùng động từ nguyên mẫu '{orig}': người cảm thấy -> '-ed', sự vật gây cảm xúc -> '-ing' ('{fix}')."),
            # CAUSATIVE: have/get + determiner + thing (+ word) + base verb -> V3
            ("CAUSATIVE", re.compile(rf"\b(have|has|had|having|get|gets|got|getting)\s+({DET}\s+(?:[a-z]+\s+)?[a-z]+)\s+({caus})\b(?!-)", re.I),
             self._fix_causative,
             "Cấu trúc nhờ vả: have/get + vật + V3/ed ('{fix}'), vì đồ vật không tự thực hiện hành động."),
            # MODAL_TO: modal (+ subject in a question) (+ not) + to + verb
            ("MODAL_TO", re.compile(rf"\b({MODALS})(\s+(?:i|you|we|they|he|she|it))?(\s+not)?\s+to\s+(?=[a-z])", re.I),
             lambda m: (m.group(0), f"{m.group(1)}{m.group(2) or ''}{m.group(3) or ''} "),
             "Sau động từ khuyết thiếu '{modal}' dùng động từ nguyên mẫu không 'to'."),
            # SVA: he/she/it + base verb (not after make/let/to/modals...), and he/she/it + don't
            ("SVA", re.compile(rf"\b()(he|she|it)\s+(don't|do\s+not|{verbs})\b(?!-)", re.I),
             self._fix_sva,
             "Chủ ngữ ngôi thứ ba số ít ('{subj}') ở hiện tại đơn: động từ thêm -s/-es, phủ định dùng 'doesn't'."),
            # WH_DO: clause-initial wh-word + subject + verb without auxiliary
            ("WH_DO", re.compile(rf"((?:^|[.!?,;:]\s*|\bơi\s+|\bạ\s+|\bcô\s+|\bthầy\s+)(?:[^\x00-\x7f\s]+\s+|em\s+|cho\s+)*)(why|what|how|where|when)\s+(i|you|we|they|he|she|it)\s+([a-z]+)\b", re.I),
             self._fix_wh_do,
             "Câu hỏi Wh- ở hiện tại đơn cần trợ động từ do/does đứng trước chủ ngữ ('{fix}')."),
        ]

    # -- fixers return (original_span, replacement_span) or None ----------------------------------------------
    def _fix_be_verb(self, m):
        subj, be, neg, verb = m.group(1), m.group(2).strip().lower(), m.group(3), m.group(4).lower()
        past = be in ("was", "were")
        s = subj.lower()
        if neg:
            aux = "did" if past else ("does" if s in ("he", "she", "it") else "do")
            return m.group(0), f"{subj} {aux} not {verb}"
        if past:
            return m.group(0), f"{subj} {past_simple(verb)}"
        return m.group(0), f"{subj} {third_person(verb) if s in ('he', 'she', 'it') else verb}"

    def _swap_last(self, m, table, make):
        word = m.group(m.lastindex)
        base = table.get(word.lower())
        if not base:
            return None
        new = make(base)
        span = m.group(0)
        return span, span[: len(span) - len(word)] + _keep_case(word, new)

    def _fix_emo_base(self, m):
        subj, word = m.group(1).lower(), m.group(3)
        verb = m.group(2).strip().lower()
        person = subj in PRONOUN_PERSON | PERSON_NOUNS or verb in ("feel", "feels", "felt", "am", "'m")
        new = ed_form(word.lower()) if person else ing_form(word.lower())
        span = m.group(0)
        return span, span[: len(span) - len(word)] + new

    def _fix_causative(self, m):
        obj, verb = m.group(2), m.group(3)
        head = obj.split()[-1].lower()
        if head in PERSON_NOUNS or verb.lower() in ("cut", "set", "put", "hit", "proofread", "read"):
            return None  # "have the mechanic fix it" is correct; cut/set/put look the same as V3
        return m.group(0), f"{m.group(1)} {obj} {past_participle(verb.lower())}"

    def _fix_sva(self, m):
        before = re.findall(r"[a-z']+", m.string[: m.start(2)].lower())
        prev, subj, verb = (before[-1] if before else ""), m.group(2), m.group(3)
        if prev in NO_SUBJ_VERB_AFTER or prev in ("why", "what", "how", "where", "when", "does", "did"):
            return None
        v = verb.lower()
        if v in ("don't", "do not"):
            new = "doesn't" if v == "don't" else "does not"
        else:
            new = third_person(v)
        span = m.group(0)
        return span, span[: len(span) - len(verb)] + new

    def _fix_wh_do(self, m):
        lead, wh, subj, verb = m.group(1), m.group(2), m.group(3), m.group(4).lower()
        if verb in ("do", "does", "did", "am", "is", "are", "was", "were", "can", "could", "will", "would", "should",
                    "must", "may", "might", "have", "has", "had") or verb.endswith("ing"):
            return None
        base = verb if verb in COMMON_VERBS else base_from_third(verb)
        if base is None:
            return None
        aux = "does" if subj.lower() in ("he", "she", "it") else "do"
        span = m.group(0)
        return span, f"{lead}{wh} {aux} {subj} {base}"

    # -- main --------------------------------------------------------------------------------------------------
    def check_sentence(self, text):
        """Apply the rules left to right; return (edits, corrected_text)."""
        edits, corrected = [], text
        for cat, pat, fixer, expl in self.rules:
            pos = 0
            while True:
                m = pat.search(corrected, pos)
                if not m:
                    break
                fix = fixer(m)
                if not fix or fix[0] == fix[1]:
                    pos = m.start() + 1
                    continue
                orig, rep = fix
                start = m.start() + m.group(0).find(orig)
                corrected = corrected[:start] + rep + corrected[start + len(orig):]
                o_words, r_words = orig.split(), rep.split()
                typed = errant_types(orig, rep)
                edits.append({
                    "category": cat,
                    "error_type": typed[0] if len(typed) == 1 else ERRANT_TYPE[cat],
                    "errant_source": "errant" if len(typed) == 1 else "category_default",
                    "original": orig.strip(),
                    "replacement": rep.strip(),
                    "explanation_vi": expl.format(v=(m.group(4) if cat == "BE_VERB" else ""),
                                                  fix=" ".join(r_words[-2:]), orig=" ".join(o_words[-2:]),
                                                  modal=m.group(1) if cat == "MODAL_TO" else "",
                                                  subj=m.group(2) if cat == "SVA" else ""),
                })
                pos = start + len(rep)
        return edits, corrected

    def extract_english_clauses(self, text):
        """English spans (>= 2 English words, no Vietnamese diacritics) of a code-mixed message."""
        parts = re.split(r"(?:^|[,\.\?!]|\bcâu\s+\d+\b|\btext\s+\d+\b|\bem\s+(?:chọn|nghĩ|thấy)\b|\bcô\s+ơi\b|\bạ\b)",
                         text, flags=re.I)
        return [p.strip() for p in parts if len(re.findall(r"[A-Za-z]+", p)) >= 2 and not VI_CHARS.search(p)]


def generate_feedback(chat_entries):
    """Analyze chat messages and produce diagnostic feedback records."""
    engine = GECRuleEngine()
    feedbacks = []
    for c in chat_entries:
        msg = c.get("message", "")
        edits, corrected = engine.check_sentence(msg)
        has_error = bool(edits)
        feedbacks.append({
            "chat_id": c["id"],
            "timestamp": c["timestamp"],
            "time_str": c["time_str"],
            "speaker_id": c["speaker_id"],
            "speaker_name": c["speaker_name"],
            "original_message": msg,
            "question_number": c.get("question_number"),
            "exercise_id": c.get("exercise_id"),
            "answer_choice": c.get("answer_choice"),
            "has_error": has_error,
            "corrected_message": corrected if has_error else msg,
            "edits": edits,
            "status": "needs_correction" if has_error else "correct_or_general",
        })
    return feedbacks


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lesson", default=".", help="lesson folder; all paths are relative to it")
    ap.add_argument("--chat", default="chat.json", help="parsed chat json filename")
    ap.add_argument("--out", default="chat_feedback.json", help="output feedback json filename")
    a = ap.parse_args()
    L = lambda f: os.path.join(a.lesson, f)

    chat_file = L(a.chat)
    if not os.path.exists(chat_file):
        print(f"[feedback] Missing {chat_file}; skipping.")
        exit(0)

    chat_entries = json.load(open(chat_file, encoding="utf-8"))
    feedbacks = generate_feedback(chat_entries)

    err_count = sum(1 for f in feedbacks if f["has_error"])
    out_path = L(a.out)
    json.dump(feedbacks, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"[feedback] Processed {len(feedbacks)} messages ({err_count} with detected errors) -> {out_path}")
