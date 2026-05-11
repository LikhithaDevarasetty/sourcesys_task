"""
random_forest_model.py
----------------------
Random Forest classifier for heart disease prediction.
Includes:
  - Baseline Random Forest (100 trees)
  - Feature importance plot
  - Cross-validation
  - GridSearchCV hyperparameter tuning with top-5 results
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.metrics import (
    accuracy_score, classification_report,
    confusion_matrix, roc_auc_score, roc_curve
)

from preprocessing import load_and_split


# ── Data ──────────────────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = load_and_split("heart.csv")
# Random Forest does not require scaling


# ── Baseline Random Forest ────────────────────────────────────────────────────
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)
y_prob = rf_model.predict_proba(X_test)[:, 1]

print("\n── Random Forest (baseline) ─────────────────")
print("Accuracy :", accuracy_score(y_test, y_pred))
print("ROC AUC  :", roc_auc_score(y_test, y_prob))
print(classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

cv_scores = cross_val_score(rf_model, X_train, y_train, cv=5)
print(f"CV Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")


# ── Feature importances ───────────────────────────────────────────────────────
feat_imp = (
    pd.Series(rf_model.feature_importances_, index=X_train.columns)
    .sort_values(ascending=False)
)
print("\nFeature Importances:\n", feat_imp)

plt.figure(figsize=(10, 6))
sns.barplot(x=feat_imp.values, y=feat_imp.index, palette="viridis")
plt.title("Random Forest – Feature Importances")
plt.xlabel("Importance")
plt.tight_layout()
plt.savefig("rf_feature_importances.png")
plt.show()
print("Saved: rf_feature_importances.png")


# ── GridSearchCV ──────────────────────────────────────────────────────────────
param_grid = {
    "n_estimators":     [50, 100, 200],
    "max_depth":        [None, 5, 10, 15],
    "min_samples_split":[2, 5, 10],
    "min_samples_leaf": [1, 2, 4],
    "max_features":     ["sqrt", "log2"],
}

grid = GridSearchCV(
    RandomForestClassifier(random_state=42), param_grid,
    cv=5, scoring="accuracy", n_jobs=-1, verbose=1
)
grid.fit(X_train, y_train)

print("\n── Random Forest (GridSearchCV) ─────────────")
print("Best params :", grid.best_params_)
print("Best CV score:", grid.best_score_)

y_pred_gs = grid.best_estimator_.predict(X_test)
y_prob_gs = grid.best_estimator_.predict_proba(X_test)[:, 1]

print("Accuracy :", accuracy_score(y_test, y_pred_gs))
print(classification_report(y_test, y_pred_gs))

# Top 5 configurations
rf_results = pd.DataFrame(grid.cv_results_)
top5 = (
    rf_results
    .sort_values("mean_test_score", ascending=False)
    .head(5)[["params", "mean_test_score", "std_test_score"]]
)
print("\nTop-5 GridSearchCV results:\n", top5.to_string(index=False))


# ── ROC curve ─────────────────────────────────────────────────────────────────
plt.figure(figsize=(7, 6))
for label, probs in [("RF (baseline)", y_prob), ("RF (GridSearchCV)", y_prob_gs)]:
    fpr, tpr, _ = roc_curve(y_test, probs)
    auc = roc_auc_score(y_test, probs)
    plt.plot(fpr, tpr, label=f"{label} (AUC={auc:.3f})")
plt.plot([0, 1], [0, 1], "k--", label="Random")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Random Forest – ROC Curves")
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig("rf_roc_curve.png")
plt.show()
