"""Build experiment_report.pdf from project results and figures."""
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).parent.parent
REPORTS = ROOT / "reports"
IMAGES = REPORTS / "images"
SCREENSHOTS = ROOT / "screenshots"
# Actual screenshot filenames from MLflow UI
SCREENSHOT_FILES = [
    "Experiments List View.png",
    "Runs Comparison View .png",
    "Individual Run Detail Page.png",
    "Model Registry View.png",
    "Production Model Detail.png",
]
PDF_PATH = REPORTS / "experiment_report.pdf"


def ascii_safe(text: str) -> str:
    """Replace unicode chars for Helvetica PDF compatibility."""
    text = (
        text.replace("\u2014", "-")
        .replace("\u2013", "-")
        .replace("\u2192", "->")
        .replace("\u2022", "-")
        .replace("\u00d7", "x")
    )
    return text.encode("ascii", errors="ignore").decode("ascii")


class ReportPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 9)
            self.set_text_color(100, 100, 100)
            self.cell(0, 8, "Anomaly Detection with MLflow - Experiment Report", align="L")
            self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def section_title(self, title: str):
        self.ln(4)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(30, 60, 120)
        self.cell(0, 10, ascii_safe(title), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(30, 60, 120)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)
        self.set_text_color(0, 0, 0)

    def sub_title(self, title: str):
        self.ln(2)
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 8, ascii_safe(title), new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text: str):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.5, ascii_safe(text))
        self.ln(2)

    def bullet(self, text: str):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.5, f"  -  {ascii_safe(text)}")

    def add_image_if_exists(self, path: Path, w: float = 180):
        if path.exists():
            self.ln(2)
            self.image(str(path), x=15, w=w)
            self.ln(4)
            self.set_x(self.l_margin)
            return True
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(180, 0, 0)
        self.multi_cell(0, 5, f"[Add screenshot: {path.name}]")
        self.set_text_color(0, 0, 0)
        self.ln(2)
        return False

    def metrics_table(self):
        col_w = [45, 22, 28, 28, 28, 22]
        headers = ["Model", "Accuracy", "Recall C0", "Recall C1", "F1 Macro", "SMOTE"]
        rows = [
            ["Random Forest", "0.6207", "0.4815", "0.7419", "0.6091", "No"],
            ["XGBClassifier", "0.5690", "0.5185", "0.6129", "0.5657", "No"],
            ["Logistic Regression", "0.4483", "0.3333", "0.5484", "0.4376", "No"],
            ["XGBoost + SMOTE", "0.5000", "0.4815", "0.5161", "0.4987", "Yes"],
        ]
        self.set_font("Helvetica", "B", 9)
        for i, h in enumerate(headers):
            self.cell(col_w[i], 8, h, border=1, align="C")
        self.ln()
        self.set_font("Helvetica", "", 9)
        for row in rows:
            for i, val in enumerate(row):
                style = "B" if row[0] == "Random Forest" and i == 0 else ""
                self.set_font("Helvetica", style, 9)
                self.cell(col_w[i], 7, val, border=1, align="C")
            self.ln()
        self.ln(3)


def build_pdf():
    pdf = ReportPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Title page
    pdf.ln(35)
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(30, 60, 120)
    pdf.cell(0, 14, "Anomaly Detection with MLflow", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 16)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 10, "Experiment Report", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 7, ascii_safe("Capstone Project - Machine Learning Experimentation Workflow"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font("Helvetica", "", 10)
    for line in [
        "Author: Akash Deep",
        "Date: June 2026",
        "Dataset: Local binary image dataset (data/dataset/no, data/dataset/yes)",
        "MLflow Experiment: anomaly-detection",
        "Tracking URI: http://127.0.0.1:5000",
    ]:
        pdf.cell(0, 7, ascii_safe(line), align="C", new_x="LMARGIN", new_y="NEXT")

    # Executive Summary
    pdf.add_page()
    pdf.section_title("1. Executive Summary")
    pdf.body_text(
        "This report documents a complete anomaly detection workflow built for the MLflow capstone "
        "assignment. Four model configurations were trained on a local binary image dataset, compared "
        "using accuracy, recall (both classes), and macro F1 score, and tracked in a single MLflow "
        "experiment. The best model â€” Random Forest â€” was registered, promoted through the model "
        "registry (@challenger â†’ @champion), and validated with production inference on the held-out test set."
    )
    pdf.body_text(
        "Key finding: Random Forest achieved the highest anomaly recall (74.2%) without SMOTE. "
        "Applying SMOTE to XGBoost actually reduced performance on this small, high-dimensional dataset."
    )

    # Introduction
    pdf.section_title("2. Introduction")
    pdf.body_text(
        "Detecting anomalies in operational data is a common real-world ML challenge. Class imbalance "
        "makes evaluation difficult â€” accuracy alone can be misleading when one class dominates. "
        "This project implements the required experimentation pipeline: stratified splitting, SMOTE "
        "on training data only, four comparable models, MLflow tracking, and model registry workflow."
    )
    pdf.body_text(
        "Dataset: 193 images in two folders â€” no/ (class 0, normal) and yes/ (class 1, anomaly). "
        "Images were resized to 32Ã-32 grayscale and flattened into 1,024 numerical features for "
        "Logistic Regression, Random Forest, and XGBoost."
    )

    # Dataset
    pdf.section_title("3. Dataset and Preprocessing")
    pdf.sub_title("3.1 Class Distribution")
    pdf.body_text(
        "Total: 193 images | Class 0 (no): 89 | Class 1 (yes): 104 | Ratio: ~54:46. "
        "The dataset is mildly imbalanced. SMOTE was applied on the training set as required."
    )
    pdf.add_image_if_exists(IMAGES / "01_class_distribution.png")

    pdf.sub_title("3.2 Train-Test Split (70/30, Stratified)")
    pdf.bullet("Training set: 135 samples")
    pdf.bullet("Test set: 58 samples â€” untouched until final evaluation")
    pdf.ln(2)

    pdf.sub_title("3.3 SMOTE on Training Set Only")
    pdf.body_text(
        "Before SMOTE: Class 0 = 62, Class 1 = 73. After SMOTE: both classes = 73 (146 total training samples)."
    )
    pdf.add_image_if_exists(IMAGES / "02_smote_training.png")

    # Experiments
    pdf.add_page()
    pdf.section_title("4. Experiment Results")

    experiments = [
        (
            "4.1 Logistic Regression (Baseline)",
            "Parameters: C=1, solver=liblinear, used_smote=False",
            "Accuracy: 0.4483 | Recall C0: 0.3333 | Recall C1: 0.5484 | F1 Macro: 0.4376",
            "Weakest performer. Linear model struggled with 1,024 pixel features on limited data.",
        ),
        (
            "4.2 Random Forest",
            "Parameters: n_estimators=30, max_depth=3, used_smote=False",
            "Accuracy: 0.6207 | Recall C0: 0.4815 | Recall C1: 0.7419 | F1 Macro: 0.6091",
            "Best overall model. Highest recall on anomaly class â€” critical for detection tasks.",
        ),
        (
            "4.3 XGBoost (Original Data)",
            "Parameters: eval_metric=logloss, used_smote=False",
            "Accuracy: 0.5690 | Recall C0: 0.5185 | Recall C1: 0.6129 | F1 Macro: 0.5657",
            "Second best. Better than Logistic Regression but below Random Forest.",
        ),
        (
            "4.4 XGBoost with SMOTE",
            "Parameters: eval_metric=logloss, used_smote=True",
            "Accuracy: 0.5000 | Recall C0: 0.4815 | Recall C1: 0.5161 | F1 Macro: 0.4987",
            "SMOTE hurt performance. Oversampling added noise on this small high-dimensional set.",
        ),
    ]
    for title, params, metrics, note in experiments:
        pdf.sub_title(title)
        pdf.body_text(params)
        pdf.set_x(pdf.l_margin)
        pdf.set_font("Helvetica", "B", 10)
        pdf.multi_cell(0, 5.5, ascii_safe(metrics))
        pdf.set_x(pdf.l_margin)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 5.5, ascii_safe(note))
        pdf.ln(2)

    # Comparison
    pdf.add_page()
    pdf.section_title("5. Metric Comparison")
    pdf.metrics_table()
    pdf.add_image_if_exists(IMAGES / "03_metrics_comparison.png")
    pdf.add_image_if_exists(IMAGES / "04_best_model_metrics.png")

    # Class imbalance
    pdf.section_title("6. Observations on Class Imbalance Handling")
    observations = [
        "Dataset imbalance is mild (~54:46), so sample size and feature dimension mattered more than extreme skew.",
        "SMOTE balanced the training set (62â†’73 for class 0) but did not improve XGBoost test performance.",
        "Random Forest without SMOTE achieved the best anomaly recall â€” tree ensembles handled pixel patterns better.",
        "Selection criterion: recall_class_1 first, then f1_score_macro â€” appropriate when missing anomalies is costly.",
        "For production image tasks, a CNN would likely outperform raw pixels; this workflow meets capstone MLflow requirements.",
    ]
    for obs in observations:
        pdf.bullet(obs)
    pdf.ln(3)

    # MLflow
    pdf.add_page()
    pdf.section_title("7. MLflow Tracking and Model Registry")
    pdf.body_text(
        "All runs logged to experiment 'anomaly-detection' on http://127.0.0.1:5000. "
        "Each run recorded hyperparameters, four metrics, and model artifacts."
    )
    pdf.sub_title("Registry Workflow")
    pdf.bullet("Registered best model as anomaly-detector-xgb-smote v1")
    pdf.bullet("Assigned @challenger alias")
    pdf.bullet("Copied to anomaly-detection-prod v1")
    pdf.bullet("Assigned @champion alias")
    pdf.bullet("Loaded models:/anomaly-detection-prod@champion â€” test metrics matched Random Forest")
    pdf.ln(3)

    pdf.sub_title("7.1 Experiments List View")
    pdf.add_image_if_exists(SCREENSHOTS / SCREENSHOT_FILES[0])

    pdf.sub_title("7.2 Runs Comparison View")
    pdf.add_image_if_exists(SCREENSHOTS / SCREENSHOT_FILES[1])

    pdf.sub_title("7.3 Best Run Detail â€” Random Forest")
    pdf.add_image_if_exists(SCREENSHOTS / SCREENSHOT_FILES[2])

    pdf.sub_title("7.4 Model Registry â€” @challenger")
    pdf.add_image_if_exists(SCREENSHOTS / SCREENSHOT_FILES[3])

    pdf.sub_title("7.5 Production Model â€” @champion")
    pdf.add_image_if_exists(SCREENSHOTS / SCREENSHOT_FILES[4])

    # Conclusion
    pdf.add_page()
    pdf.section_title("8. Production Model Justification")
    pdf.body_text(
        "Production model: Random Forest deployed as anomaly-detection-prod @champion."
    )
    pdf.body_text(
        "Justification: Random Forest ranked first on both primary selection metrics â€” recall on class 1 "
        "(0.7419) and macro F1 (0.6091). It correctly identifies ~74% of anomalies on the test set while "
        "maintaining the highest overall balance across classes. Production inference confirmed identical "
        "metrics, validating the end-to-end MLflow registry pipeline."
    )

    pdf.section_title("9. Conclusion")
    pdf.body_text(
        "Four experiments were successfully tracked, compared, and registered in MLflow. Random Forest "
        "was selected for production. SMOTE was valuable to document but not beneficial for XGBoost on "
        "this dataset. The workflow demonstrates reproducible experimentation, metric-driven model "
        "selection, and production-ready model deployment through MLflow model registry."
    )

    pdf.section_title("10. References")
    pdf.bullet("Dataset: Local repository â€” data/dataset/no/, data/dataset/yes/")
    pdf.bullet("MLflow: https://mlflow.org/docs/latest/")
    pdf.bullet("imbalanced-learn SMOTE: https://imbalanced-learn.org/")

    pdf.output(str(PDF_PATH))
    print(f"PDF saved: {PDF_PATH}")


if __name__ == "__main__":
    build_pdf()

