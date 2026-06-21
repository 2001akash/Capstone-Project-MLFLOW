# Capstone — Anomaly Detection with MLflow

## Quick start

```bash
cd capstone
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Windows tip:** If install fails with `Microsoft Visual C++ 14.0` or long-path errors:
1. Always upgrade pip first: `python -m pip install --upgrade pip`
2. Use the simplified `requirements.txt` (notebook only, not full `jupyter` meta-package)
3. Optional: enable [Windows Long Paths](https://pip.pypa.io/warnings/enable-long-paths) if Jupyter install still fails

1. Download [creditcard.csv](https://www.kaggle.com/datasets/kartik2112/fraud-detection) → `capstone/data/creditcard.csv`
2. Start MLflow UI:
   ```bash
   mlflow ui --port 5000
   ```
3. Open and run the notebook:
   ```bash
   jupyter notebook notebooks/anomaly_detection_mlflow.ipynb
   ```

## Notebook

`notebooks/anomaly_detection_mlflow.ipynb` — full capstone workflow:

- Load data and inspect class imbalance
- Stratified 70/30 split + SMOTE on training only
- 4 experiments (Logistic Regression, Random Forest, XGBoost, XGBoost + SMOTE)
- MLflow tracking (params, metrics, model artifacts)
- Model Registry (`@challenger` → copy to prod → `@champion`)
- Production inference on test set

## Screenshots

Save MLflow UI screenshots in `screenshots/` before submission.
