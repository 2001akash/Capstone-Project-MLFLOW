"""Generate figures for the experiment report PDF."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).parent / "images"
OUT.mkdir(parents=True, exist_ok=True)

plt.style.use("seaborn-v0_8-whitegrid")

# --- Figure 1: Class distribution ---
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

labels = ["Class 0 (no)", "Class 1 (yes)"]
counts = [89, 104]
colors = ["#4C72B0", "#DD8452"]

axes[0].bar(labels, counts, color=colors, edgecolor="white", linewidth=1.2)
axes[0].set_title("Dataset Class Distribution", fontsize=13, fontweight="bold")
axes[0].set_ylabel("Number of Images")
for i, v in enumerate(counts):
    axes[0].text(i, v + 2, str(v), ha="center", fontweight="bold")

axes[1].pie(
    counts,
    labels=[f"{l}\n({v})" for l, v in zip(labels, counts)],
    autopct="%1.1f%%",
    colors=colors,
    startangle=90,
    textprops={"fontsize": 10},
)
axes[1].set_title("Class Proportion (~54:46)", fontsize=13, fontweight="bold")

plt.tight_layout()
fig.savefig(OUT / "01_class_distribution.png", dpi=150, bbox_inches="tight")
plt.close()

# --- Figure 2: SMOTE before/after ---
fig, ax = plt.subplots(figsize=(7, 4))
smote_labels = ["Before SMOTE", "After SMOTE"]
class0 = [62, 73]
class1 = [73, 73]
x = np.arange(len(smote_labels))
w = 0.35
ax.bar(x - w / 2, class0, w, label="Class 0", color="#4C72B0")
ax.bar(x + w / 2, class1, w, label="Class 1", color="#DD8452")
ax.set_xticks(x)
ax.set_xticklabels(smote_labels)
ax.set_ylabel("Training Samples")
ax.set_title("SMOTE Effect on Training Set Only", fontsize=13, fontweight="bold")
ax.legend()
for i, (a, b) in enumerate(zip(class0, class1)):
    ax.text(i - w / 2, a + 1, str(a), ha="center", fontsize=9)
    ax.text(i + w / 2, b + 1, str(b), ha="center", fontsize=9)
plt.tight_layout()
fig.savefig(OUT / "02_smote_training.png", dpi=150, bbox_inches="tight")
plt.close()

# --- Figure 3: Metrics comparison ---
models = [
    "Logistic\nRegression",
    "Random\nForest",
    "XGBoost",
    "XGBoost\n+ SMOTE",
]
accuracy = [0.4483, 0.6207, 0.5690, 0.5000]
recall_1 = [0.5484, 0.7419, 0.6129, 0.5161]
f1_macro = [0.4376, 0.6091, 0.5657, 0.4987]

x = np.arange(len(models))
w = 0.25
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(x - w, accuracy, w, label="Accuracy", color="#55A868")
ax.bar(x, recall_1, w, label="Recall Class 1", color="#C44E52")
ax.bar(x + w, f1_macro, w, label="F1 Macro", color="#8172B3")
ax.set_xticks(x)
ax.set_xticklabels(models)
ax.set_ylim(0, 0.85)
ax.set_ylabel("Score")
ax.set_title("Model Metrics Comparison (Test Set)", fontsize=13, fontweight="bold")
ax.legend(loc="upper right")
ax.axhline(0.5, color="gray", linestyle="--", alpha=0.5, linewidth=0.8)
plt.tight_layout()
fig.savefig(OUT / "03_metrics_comparison.png", dpi=150, bbox_inches="tight")
plt.close()

# --- Figure 4: Best model highlight ---
fig, ax = plt.subplots(figsize=(6, 4))
metrics_names = ["Accuracy", "Recall\nClass 0", "Recall\nClass 1", "F1 Macro"]
rf_values = [0.6207, 0.4815, 0.7419, 0.6091]
bars = ax.bar(metrics_names, rf_values, color=["#4C72B0", "#55A868", "#C44E52", "#8172B3"])
ax.set_ylim(0, 0.85)
ax.set_title("Best Model: Random Forest (Production @champion)", fontsize=12, fontweight="bold")
for bar, val in zip(bars, rf_values):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 0.02, f"{val:.2f}", ha="center", fontweight="bold")
plt.tight_layout()
fig.savefig(OUT / "04_best_model_metrics.png", dpi=150, bbox_inches="tight")
plt.close()

print(f"Saved figures to {OUT}")
