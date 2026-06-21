# MLflow Screenshot Guide

Open **http://127.0.0.1:5000** (MLflow must be running).

Save all 5 screenshots as `.png` files in this folder.

---

## Screenshot 1 — Experiments list

**Where:** MLflow home → left sidebar **Experiments**

**What to capture:**
- Experiment name: `anomaly-detection`
- All **4 runs** visible with run names:
  - Logistic Regression
  - Random Forest
  - XGBClassifier
  - XGBClassifier With SMOTE

**Save as:** `01_experiments_list.png`

**Direct link:** http://127.0.0.1:5000/#/experiments/594281079765530894

---

## Screenshot 2 — Runs comparison

**Where:** Open experiment `anomaly-detection` → check all 4 runs → click **Compare**

**What to capture:**
- Side-by-side comparison table
- All four metrics visible:
  - accuracy
  - recall_class_0
  - recall_class_1
  - f1_score_macro

**Save as:** `02_runs_comparison.png`

---

## Screenshot 3 — Best run detail (Random Forest)

**Where:** Click the **Random Forest** run (best performer)

**What to capture:**
- Run name: Random Forest
- **Parameters:** n_estimators, max_depth, used_smote
- **Metrics:** accuracy, recall_class_0, recall_class_1, f1_score_macro
- **Artifacts:** `model` folder listed

**Save as:** `03_best_run_random_forest.png`

**Direct link:** http://127.0.0.1:5000/#/experiments/594281079765530894/runs/f41fbcf586a944bba6eb0bd47ec9eab0

---

## Screenshot 4 — Model registry (@challenger)

**Where:** Top menu → **Models** → click `anomaly-detector-xgb-smote`

**What to capture:**
- Model name: `anomaly-detector-xgb-smote`
- Version **1**
- Alias **`challenger`** assigned
- Source run linked to Random Forest

**Save as:** `04_registry_challenger.png`

---

## Screenshot 5 — Production model (@champion)

**Where:** **Models** → click `anomaly-detection-prod`

**What to capture:**
- Model name: `anomaly-detection-prod`
- Version **1**
- Alias **`champion`** assigned
- Source shows it was copied from `anomaly-detector-xgb-smote`

**Save as:** `05_production_champion.png`

---

## How to take the screenshot (Windows)

1. Open the MLflow page
2. Press **Win + Shift + S** (Snipping Tool)
3. Select the area
4. Save into `Capstone Project/screenshots/`

## Convert report to PDF

Open `reports/experiment_report.md` in Word or VS Code → export/print to PDF → save as `reports/experiment_report.pdf`
