"""
knn_model.py
------------
K-Nearest Neighbours classifier for heart disease prediction.
Includes:
  - Finding the best K by accuracy curve
  - Final KNN with best K (distance-weighted, Euclidean)
  - Cross-validation
  - GridSearchCV hyperparameter tuning
"""

import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.metrics import (
    accuracy_score, classification_report,
    confusion_matrix, roc_auc_score, roc_curve
)

from preprocessing import load_and_split, get_standard_scaled


# ── Data ──────────────────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = load_and_split("heart.csv")
X_train_scaled, X_test_scaled, _ = get_standard_scaled(X_train, X_test)


# ── Find best K ───────────────────────────────────────────────────────────────
train_acc, test_acc = [], []

for k in range(1, 31):
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train_scaled, y_train)
    train_acc.append(accuracy_score(y_train, knn.predict(X_train_scaled)))
    test_acc.append(accuracy_score(y_test,  knn.predict(X_test_scaled)))

best_k = int(np.argmax(test_acc)) + 1
print(f"\nBest K (by test accuracy): {best_k}")

plt.figure(figsize=(10, 5))
plt.plot(range(1, 31), train_acc, label="Train Accuracy", marker="o")
plt.plot(range(1, 31), test_acc,  label="Test Accuracy",  marker="s")
plt.axvline(x=best_k, color="red", linestyle="--", label=f"Best K = {best_k}")
plt.xlabel("K Value")
plt.ylabel("Accuracy")
plt.title("KNN – K vs Accuracy")
plt.legend()
plt.tight_layout()
plt.savefig("knn_k_vs_accuracy.png")
plt.show()
print("Saved: knn_k_vs_accuracy.png")


# ── Final KNN model ───────────────────────────────────────────────────────────
knn_model = KNeighborsClassifier(
    n_neighbors=best_k, weights="distance", metric="euclidean"
)
knn_model.fit(X_train_scaled, y_train)

y_pred = knn_model.predict(X_test_scaled)
y_prob = knn_model.predict_proba(X_test_scaled)[:, 1]

print("\n── KNN (best K) ─────────────────────────────")
print("Accuracy :", accuracy_score(y_test, y_pred))
print("ROC AUC  :", roc_auc_score(y_test, y_prob))
print(classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

cv_scores = cross_val_score(knn_model, X_train_scaled, y_train, cv=5)
print(f"CV Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")


# ── GridSearchCV ──────────────────────────────────────────────────────────────
param_grid = {
    "n_neighbors": [3, 5, 7, 9, 11, 13, 15],
    "weights":     ["uniform", "distance"],
    "metric":      ["euclidean", "manhattan"],
}

grid = GridSearchCV(
    KNeighborsClassifier(), param_grid,
    cv=5, scoring="accuracy", n_jobs=-1, verbose=1
)
grid.fit(X_train_scaled, y_train)

print("\n── KNN (GridSearchCV) ───────────────────────")
print("Best params :", grid.best_params_)
print("Best CV score:", grid.best_score_)

y_pred_gs = grid.best_estimator_.predict(X_test_scaled)
y_prob_gs = grid.best_estimator_.predict_proba(X_test_scaled)[:, 1]

print("Accuracy :", accuracy_score(y_test, y_pred_gs))
print(classification_report(y_test, y_pred_gs))


# ── ROC curve ─────────────────────────────────────────────────────────────────
plt.figure(figsize=(7, 6))
for label, probs in [("KNN (best K)", y_prob), ("KNN (GridSearchCV)", y_prob_gs)]:
    fpr, tpr, _ = roc_curve(y_test, probs)
    auc = roc_auc_score(y_test, probs)
    plt.plot(fpr, tpr, label=f"{label} (AUC={auc:.3f})")
plt.plot([0, 1], [0, 1], "k--", label="Random")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("KNN – ROC Curves")
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig("knn_roc_curve.png")
plt.show()
