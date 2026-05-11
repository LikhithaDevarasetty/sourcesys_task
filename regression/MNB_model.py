"""
naive_bayes_model.py
--------------------
Multinomial Naive Bayes classifier for heart disease prediction.
Includes:
  - Baseline MNB (alpha=1.0) with MinMax-scaled features
  - Cross-validation
  - GridSearchCV hyperparameter tuning (alpha, fit_prior)
"""

import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.metrics import (
    accuracy_score, classification_report,
    confusion_matrix, roc_auc_score, roc_curve
)

from preprocessing import load_and_split, get_minmax_scaled


# ── Data ──────────────────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = load_and_split("heart.csv")
# MultinomialNB requires non-negative features → MinMaxScaler
X_train_mm, X_test_mm, _ = get_minmax_scaled(X_train, X_test)


# ── Baseline MNB ──────────────────────────────────────────────────────────────
mnb_model = MultinomialNB(alpha=1.0)
mnb_model.fit(X_train_mm, y_train)

y_pred = mnb_model.predict(X_test_mm)
y_prob = mnb_model.predict_proba(X_test_mm)[:, 1]

print("\n── Multinomial NB (baseline, alpha=1.0) ─────")
print("Accuracy :", accuracy_score(y_test, y_pred))
print("ROC AUC  :", roc_auc_score(y_test, y_prob))
print(classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

cv_scores = cross_val_score(mnb_model, X_train_mm, y_train, cv=5)
print(f"CV Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")


# ── GridSearchCV ──────────────────────────────────────────────────────────────
param_grid = {
    "alpha":     [0.001, 0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0],
    "fit_prior": [True, False],
}

grid = GridSearchCV(
    MultinomialNB(), param_grid,
    cv=5, scoring="accuracy", n_jobs=-1, verbose=1
)
grid.fit(X_train_mm, y_train)

print("\n── Multinomial NB (GridSearchCV) ────────────")
print("Best params :", grid.best_params_)
print("Best CV score:", grid.best_score_)

y_pred_gs = grid.best_estimator_.predict(X_test_mm)
y_prob_gs = grid.best_estimator_.predict_proba(X_test_mm)[:, 1]

print("Accuracy :", accuracy_score(y_test, y_pred_gs))
print(classification_report(y_test, y_pred_gs))


# ── ROC curve ─────────────────────────────────────────────────────────────────
plt.figure(figsize=(7, 6))
for label, probs in [("MNB (baseline)", y_prob), ("MNB (GridSearchCV)", y_prob_gs)]:
    fpr, tpr, _ = roc_curve(y_test, probs)
    auc = roc_auc_score(y_test, probs)
    plt.plot(fpr, tpr, label=f"{label} (AUC={auc:.3f})")
plt.plot([0, 1], [0, 1], "k--", label="Random")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Multinomial NB – ROC Curves")
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig("mnb_roc_curve.png")
plt.show()
