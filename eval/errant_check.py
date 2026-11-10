"""Check which ERRANT type the official toolkit assigns to the canonical example pairs of each feedback.py category.
Needs `pip install errant` and spaCy's en_core_web_sm (not required by the rest of the project).
Output of the last run is saved in eval/results/errant_check.txt.
Usage: python eval/errant_check.py"""
import errant

PAIRS = {
    "BE_VERB": [("I am agree with A", "I agree with A"), ("She is not understand", "She does not understand")],
    "PARTICIPLE": [("I am confusing", "I am confused"), ("The movie was moved", "The movie was moving"),
                   ("This noise is very annoy", "This noise is very annoying")],
    "CAUSATIVE": [("He has his shoes shine every day", "He has his shoes shined every day"),
                  ("I have my car repair", "I have my car repaired")],
    "MODAL_TO": [("Sales should to increase", "Sales should increase"), ("I can't to hear you", "I can't hear you")],
    "SVA": [("it make me cry", "it makes me cry"), ("she don't like it", "she doesn't like it")],
    "WH_DO": [("Why we use -ing?", "Why do we use -ing?"), ("How she know the answer?", "How does she know the answer?")],
}

if __name__ == "__main__":
    ann = errant.load("en")
    print("errant", getattr(errant, "__version__", "?"))
    for cat, pairs in PAIRS.items():
        for o, c in pairs:
            edits = ann.annotate(ann.parse(o), ann.parse(c))
            print(f"{cat:11s} {o!r:42s} -> {[(x.o_str, x.c_str, x.type) for x in edits]}")
