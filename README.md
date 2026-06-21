# Capstone Project — Anomaly Detection with MLflow

Binary classification capstone using a local image dataset with MLflow experiment tracking and model registry.

## Dataset

**Source:** Local dataset (included in this repository)

**Location:**

```
Capstone Project/
└── data/
    └── dataset/
        ├── no/     ← class 0 (non-anomaly)
        └── yes/    ← class 1 (anomaly)
```

Images in `no/` and `yes/` are converted to numerical pixel features inside the notebook so they work with Logistic Regression, Random Forest, and XGBoost.

**Alternative:** You may swap in [Kaggle Fraud Detection (creditcard.csv)](https://www.kaggle.com/datasets/kartik2112/fraud-detection) if you prefer a tabular dataset. Place the file at `data/creditcard.csv` and adjust the loading section in the notebook.

## Project structure

```
Capstone Project/
├── data/
│   └── dataset/
│       ├── no/
│       └── yes/
├── notebooks/
│   └── anomaly_detection_mlflow.ipynb
├── screenshots/          ← MLflow UI snapshots for submission
├── reports/              ← experiment report PDF
├── requirements.txt
└── README.md
```

## Quick start

```powershell
cd "Capstone Project"
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Windows tip:** If install fails with `Microsoft Visual C++ 14.0` or long-path errors:
1. Always upgrade pip first: `python -m pip install --upgrade pip`
2. Install greenlet wheel first: `pip install "greenlet>=3.0.0,<4.0.0" --only-binary=:all:`
3. Then run: `pip install -r requirements.txt`
4. If you see `WinError 32` (file in use), close all Jupyter/Python terminals, then retry
5. Optional: enable [Windows Long Paths](https://pip.pypa.io/warnings/enable-long-paths) if Jupyter install still fails

### Run the workflow

1. Confirm images are in `data/dataset/no/` and `data/dataset/yes/`
2. Start MLflow UI (separate terminal):
   ```powershell
   cd "Capstone Project"
   .\venv\Scripts\Activate.ps1
   mlflow ui --port 5000
   ```
   If `mlflow` command fails, use: `python -m mlflow ui --port 5000`
3. Open and run the notebook:
   ```powershell
   jupyter notebook notebooks/anomaly_detection_mlflow.ipynb
   ```
4. View experiments at http://localhost:5000

## Notebook workflow

`notebooks/anomaly_detection_mlflow.ipynb` covers the full capstone:

- Load images from `data/dataset/no/` and `data/dataset/yes/`
- Inspect class imbalance
- Stratified 70/30 train-test split + SMOTE on training only
- 4 experiments (Logistic Regression, Random Forest, XGBoost, XGBoost + SMOTE)
- MLflow tracking (params, metrics, model artifacts)
- Model Registry (`@challenger` → copy to prod → `@champion`)
- Production inference on the held-out test set


## Screenshots

Save these MLflow UI snapshots as `.png` files in `screenshots/`:

1. Experiments list with all four runs
2. Runs comparison with metrics
3. Best run detail (params, metrics, artifact)
4. Model registry with `@challenger` alias
5. Production model `anomaly-detection-prod` with `@champion` alias
