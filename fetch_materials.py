"""Step 7a: build materials/catalog.json, the reading list that slides get linked to.
arXiv papers are fetched from the arXiv API (title, authors, year, abstract) so nothing is typed by hand;
EXTRA holds non-arXiv items with a short description used for matching.
With --pdf, also downloads each arXiv PDF to materials/<id>.pdf so link_materials.py can link to pages.
Usage: python fetch_materials.py [--pdf 1810.04805 1907.11692 ...]"""
import argparse, json, os, re, urllib.request
import xml.etree.ElementTree as ET

# Papers cited on the CS224N BERT slides, plus a few standard follow-ups.  aliases = names that, when they
# appear in a slide title, mark the paper as cited by that slide.
ARXIV = {
    "1301.3781": ["word2vec"], "1511.01432": [], "1802.05365": ["ELMo"], "1706.03762": ["Transformer"],
    "1810.04805": ["BERT"], "1609.08144": ["WordPiece"], "1804.07461": ["GLUE"], "1806.03822": ["SQuAD"],
    "1907.11692": ["RoBERTa"], "1906.08237": ["XLNet"], "1901.02860": ["Transformer-XL"],
    "1909.11942": ["ALBERT"], "1910.10683": ["T5"], "2003.10555": ["ELECTRA"],
    "1503.02531": ["Distillation"], "1908.08962": [], "1910.01108": ["DistilBERT"],
}
EXTRA = [
    {"id": "glove", "kind": "paper", "aliases": ["GloVe"], "year": 2014,
     "title": "GloVe: Global Vectors for Word Representation", "authors": "Pennington, Socher, Manning",
     "url": "https://aclanthology.org/D14-1162/",
     "text": "Word vectors trained on global word-word co-occurrence statistics from a corpus."},
    {"id": "gpt1", "kind": "paper", "aliases": ["GPT"], "year": 2018,
     "title": "Improving Language Understanding by Generative Pre-Training", "authors": "Radford et al.",
     "url": "https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf",
     "text": "OpenAI GPT: pre-train a 12-layer left-to-right Transformer language model, then fine-tune it on classification and other tasks."},
    {"id": "bucila2006", "kind": "paper", "aliases": [], "year": 2006,
     "title": "Model Compression", "authors": "Bucila, Caruana, Niculescu-Mizil",
     "url": "https://www.cs.cornell.edu/~caruana/compression.kdd06.pdf",
     "text": "Compress a large ensemble into a small fast model by training it on pseudo-labeled data from the ensemble."},
    {"id": "slp3", "kind": "textbook", "aliases": [], "year": None,
     "title": "Speech and Language Processing (3rd ed. draft)", "authors": "Jurafsky, Martin",
     "url": "https://web.stanford.edu/~jurafsky/slp3/",
     "text": "Textbook chapters on word embeddings, neural language models, the Transformer, large language models, "
             "masked language models and BERT, fine-tuning, and question answering."},
    {"id": "illustrated-bert", "kind": "tutorial", "aliases": [], "year": 2018,
     "title": "The Illustrated BERT, ELMo, and co.", "authors": "Jay Alammar",
     "url": "https://jalammar.github.io/illustrated-bert/",
     "text": "Visual explanation of contextual embeddings: ELMo, ULMFiT, OpenAI Transformer, BERT masked language "
             "model, next sentence prediction, fine-tuning BERT for classification, feature extraction."},
    {"id": "illustrated-transformer", "kind": "tutorial", "aliases": [], "year": 2018,
     "title": "The Illustrated Transformer", "authors": "Jay Alammar",
     "url": "https://jalammar.github.io/illustrated-transformer/",
     "text": "Visual walkthrough of the Transformer: multi-headed self-attention, feed-forward layers, positional "
             "encoding, residual connections and layer normalization, encoder and decoder."},
    {"id": "hf-course", "kind": "tutorial", "aliases": [], "year": None,
     "title": "Hugging Face LLM Course", "authors": "Hugging Face",
     "url": "https://huggingface.co/learn/llm-course/chapter1/1",
     "text": "Hands-on course: using pre-trained Transformer models, tokenizers, fine-tuning a pretrained model on a "
             "dataset, sharing models, question answering and text classification pipelines."},
]


def fetch_arxiv(ids):
    url = "https://export.arxiv.org/api/query?max_results=100&id_list=" + ",".join(ids)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(urllib.request.urlopen(url, timeout=60).read())
    out = []
    for e in root.findall("a:entry", ns):
        aid = re.sub(r"v\d+$", "", e.find("a:id", ns).text.rsplit("/", 1)[-1])
        clean = lambda s: " ".join(s.split())
        names = [a.find("a:name", ns).text for a in e.findall("a:author", ns)]
        out.append({"id": aid, "kind": "paper", "aliases": ARXIV[aid], "year": int(e.find("a:published", ns).text[:4]),
                    "title": clean(e.find("a:title", ns).text),
                    "authors": ", ".join(names[:3]) + (" et al." if len(names) > 3 else ""),
                    "url": f"https://arxiv.org/abs/{aid}", "pdf": f"https://arxiv.org/pdf/{aid}",
                    "text": clean(e.find("a:summary", ns).text)})
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", nargs="*", default=[], help="arXiv ids whose PDFs to download for page-level links")
    ap.add_argument("--dir", default="materials")
    a = ap.parse_args()

    os.makedirs(a.dir, exist_ok=True)
    catalog = fetch_arxiv(list(ARXIV)) + EXTRA
    json.dump(catalog, open(f"{a.dir}/catalog.json", "w"), indent=1)
    print(len(catalog), "materials ->", f"{a.dir}/catalog.json")
    for aid in a.pdf:
        urllib.request.urlretrieve(f"https://arxiv.org/pdf/{aid}", f"{a.dir}/{aid}.pdf")
        print("downloaded", f"{a.dir}/{aid}.pdf")
