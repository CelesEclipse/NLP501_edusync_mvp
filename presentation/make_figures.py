"""Charts for the slides, drawn from eval/results/summary.json (run eval/run_all.py first).
Usage: python presentation/make_figures.py"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = json.load(open(os.path.join(ROOT, "eval/results/summary.json")))
OUT = os.path.join(ROOT, "presentation/figures")
NEW, OLD, MUTED = "#2a78d6", "#eb6834", "#b9b8b0"
INK, INK2, GRID, SURF = "#1f1f1d", "#5f5e58", "#e6e5e0", "#fcfcfb"
plt.rcParams.update({"font.family": "Helvetica Neue", "font.size": 15, "axes.edgecolor": GRID,
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                     "figure.facecolor": SURF, "axes.facecolor": SURF})


def style(ax):
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)


# 1. alignment accuracy, v1 vs new, dev and held-out test
v1k = next(k for k in S["alignment_dev"] if k.startswith("v1"))
groups = [("Unit 4 (dev)\n±10 s", "alignment_dev", "acc_10s"), ("Unit 4 (dev)\n±30 s", "alignment_dev", "acc_30s"),
          ("Unit 5 (test)\n±10 s", "alignment_test", "acc_10s"), ("Unit 5 (test)\n±30 s", "alignment_test", "acc_30s")]
fig, ax = plt.subplots(figsize=(9, 4.6), dpi=200)
w = 0.36
for i, (lab, split, m) in enumerate(groups):
    old, new = S[split][v1k][m] * 100, S[split]["dp+refine"][m] * 100
    ax.bar(i - w / 2 - 0.01, old, w, color=OLD, label="Bản cũ (v1)" if i == 0 else None)
    ax.bar(i + w / 2 + 0.01, new, w, color=NEW, label="Bản mới (DP + xác minh + lùi mốc)" if i == 0 else None)
    ax.text(i - w / 2 - 0.01, old + 1.5, f"{old:.0f}%", ha="center", color=INK2, fontsize=13)
    ax.text(i + w / 2 + 0.01, new + 1.5, f"{new:.0f}%", ha="center", color=INK, fontsize=13, fontweight="bold")
ax.set_xticks(range(len(groups)), [g[0] for g in groups])
ax.set_ylim(0, 105)
ax.set_yticks([0, 25, 50, 75, 100], ["0", "25", "50", "75", "100%"])
ax.yaxis.grid(True, color=GRID, lw=0.8)
ax.set_axisbelow(True)
style(ax)
ax.legend(frameon=False, loc="upper left", ncol=2, fontsize=13, bbox_to_anchor=(0, 1.13))
fig.tight_layout()
fig.savefig(os.path.join(OUT, "alignment_accuracy.png"))

# 2. concept linking accuracy (34 questions, leave-one-out threshold)
R = S["concepts_dev"]["results"]
rows = [("Luôn 'không gắn' (đa số)", "majority(none)"), ("BM25", "bm25"), ("TF-IDF", "tfidf"),
        ("MiniLM (bỏ từ khóa tay)", "minilm"), ("MiniLM + từ khóa tay (v1)", "minilm+cues (v1)"),
        ("Multilingual MiniLM", "mminilm"), ("multilingual-e5", "me5"), ("multilingual-e5 + lời giảng", "me5+speech")]
fig, ax = plt.subplots(figsize=(9, 4.8), dpi=200)
for i, (lab, key) in enumerate(rows):
    v = R[key]["acc_with_none_loo"] * 100
    c = NEW if key == "me5+speech" else OLD if key.endswith("(v1)") else MUTED
    ax.barh(i, v, 0.62, color=c)
    ax.text(v + 1, i, f"{v:.1f}%", va="center", color=INK if c != MUTED else INK2, fontsize=13,
            fontweight="bold" if c == NEW else "normal")
ax.set_yticks(range(len(rows)), [r[0] for r in rows])
ax.set_xlim(0, 105)
ax.set_xticks([0, 25, 50, 75, 100], ["0", "25", "50", "75", "100%"])
ax.xaxis.grid(True, color=GRID, lw=0.8)
ax.set_axisbelow(True)
style(ax)
ax.set_xlabel("Độ chính xác trên 34 câu (gồm nhãn 'không gắn'), ngưỡng chọn leave-one-out", fontsize=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "concept_linking.png"))

# 3. multi-source test set (other Vietnamese teachers): end-to-end vs same-source U5, and the aligner alone (oracle)
F, A = S["alignment_multisource_frozen"]["lecture"], S["alignment_multisource"]["lecture"]
n = F["n_gold"]
left = [("Unit 5\ncùng nguồn ECE", S["alignment_test"]["dp+refine"]["acc_10s"], MUTED),
        ("6 video khác\nđóng băng", F["end_to_end"]["dp+refine"]["acc_10s"], NEW),
        ("6 video khác\nsau sửa", A["end_to_end"]["dp+refine"]["acc_10s"], NEW)]
right = [("Regex\n\"câu N\"", F["oracle"]["trigger_first"]["acc_10s"], MUTED),
         ("Greedy", F["oracle"]["greedy+refine"]["acc_10s"], MUTED),
         ("v1", F["oracle"]["v1"]["acc_10s"], OLD),
         ("DP\n(hiện tại)", F["oracle"]["dp+refine"]["acc_10s"], NEW)]
fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6), dpi=200, gridspec_kw={"width_ratios": [1, 1.25]})
for ax, bars, title in ((axes[0], left, "Đầu-cuối (trích câu + căn chỉnh)"),
                        (axes[1], right, f"Chỉ căn chỉnh, cho trước {n} câu đúng")):
    for i, (lab, v, c) in enumerate(bars):
        ax.bar(i, v * 100, 0.62, color=c)
        ax.text(i, v * 100 + 2, f"{v * 100:.0f}%", ha="center", color=INK if c != MUTED else INK2, fontsize=13,
                fontweight="bold" if c == NEW else "normal")
    ax.set_xticks(range(len(bars)), [b[0] for b in bars], fontsize=12)
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 25, 50, 75, 100], ["0", "25", "50", "75", "100%"])
    ax.yaxis.grid(True, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=13, color=INK, loc="left")
    style(ax)
fig.supylabel("Mốc lệch ≤ 10 s", fontsize=12, color=INK2)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "multisource_alignment.png"))
print("figures ->", OUT)
