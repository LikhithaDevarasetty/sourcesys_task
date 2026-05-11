# Heart Disease Prediction – ML Classification

A machine learning project that predicts the presence of heart disease using three classification algorithms: **K-Nearest Neighbours (KNN)**, **Random Forest**, and **Multinomial Naive Bayes**. Each model is trained, evaluated, and tuned via GridSearchCV, with results compared side-by-side.

---

## Dataset

**File:** `heart.csv`  
**Source:** Kaggle Heart Disease Dataset  
**Rows:** 303 patients | **Columns:** 14 (13 features + 1 target)

| Column | Description |
|--------|-------------|
| `age` | Age of the patient |
| `sex` | Sex (1 = male, 0 = female) |
| `cp` | Chest pain type (0–3) |
| `trestbps` | Resting blood pressure (mm Hg) |
| `chol` | Serum cholesterol (mg/dl) |
| `fbs` | Fasting blood sugar > 120 mg/dl (1 = true) |
| `restecg` | Resting ECG results (0–2) |
| `thalach` | Maximum heart rate achieved |
| `exang` | Exercise-induced angina (1 = yes) |
| `oldpeak` | ST depression induced by exercise |
| `slope` | Slope of peak exercise ST segment |
| `ca` | Number of major vessels coloured by fluoroscopy (0–3) |
| `thal` | Thalassemia type (1–3) |
| `target` | **1 = Heart Disease, 0 = No Disease** |

---

## Project Structure

```
├── heart.csv                  # Dataset
├── preprocessing.py           # Shared data loading & scaling utilities
├── knn_model.py               # KNN classifier (best-K search + GridSearchCV)
├── random_forest_model.py     # Random Forest (feature importance + GridSearchCV)
├── naive_bayes_model.py       # Multinomial Naive Bayes (alpha tuning + GridSearchCV)
├── model_comparison.py        # Runs all models and compares results
└── README.md                  # Project documentation
```

---

## File Descriptions

### `preprocessing.py`
Shared utility module imported by all model scripts. Contains:
- `load_and_split()` — loads CSV, prints EDA summary, returns stratified 80/20 train/test split
- `get_standard_scaled()` — applies `StandardScaler` (used by KNN)
- `get_minmax_scaled()` — applies `MinMaxScaler` (used by Multinomial NB, which requires non-negative input)

Run standalone to verify data and scaling:
```bash
python preprocessing.py
```

---

### `knn_model.py`
K-Nearest Neighbours classifier pipeline:
- Loops K from 1–30 and plots train vs test accuracy to find the optimal K
- Trains final KNN with `weights='distance'` and `metric='euclidean'`
- 5-fold cross-validation
- GridSearchCV over `n_neighbors`, `weights`, and `metric`
- Saves: `knn_k_vs_accuracy.png`, `knn_roc_curve.png`

---

### `random_forest_model.py`
Random Forest classifier pipeline:
- Baseline model with 100 estimators
- Feature importance bar chart
- 5-fold cross-validation
- GridSearchCV over `n_estimators`, `max_depth`, `min_samples_split`, `min_samples_leaf`, `max_features`
- Prints top-5 GridSearchCV configurations
- Saves: `rf_feature_importances.png`, `rf_roc_curve.png`

---

### `naive_bayes_model.py`
Multinomial Naive Bayes classifier pipeline:
- Uses MinMax-scaled features (required for non-negative input)
- Baseline model with `alpha=1.0` (Laplace smoothing)
- 5-fold cross-validation
- GridSearchCV over `alpha` (0.001–10.0) and `fit_prior`
- Saves: `mnb_roc_curve.png`

---

### `model_comparison.py`
Runs all three models end-to-end and produces:
- Accuracy comparison table (printed to console)
- Bar chart of all 6 model variants (baseline + tuned for each)
- Combined ROC curve plot for all models
- Saves: `model_comparison.png`, `roc_curves_all.png`

---


## Models & Methodology

| Step | Detail |
|------|--------|
| Train/Test Split | 80% train, 20% test, stratified by target |
| Scaling (KNN) | `StandardScaler` — zero mean, unit variance |
| Scaling (MNB) | `MinMaxScaler` — range [0, 1] |
| Scaling (RF) | None — tree models are scale-invariant |
| Tuning | `GridSearchCV` with 5-fold cross-validation |
| Evaluation | Accuracy, ROC-AUC, Precision, Recall, F1, Confusion Matrix |

---

