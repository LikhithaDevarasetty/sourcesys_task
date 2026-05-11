import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve

from preprocessing import load_and_split, get_standard_scaled, get_minmax_scaled


# ── Data ──────────────────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = load_and_split("heart.csv")
X_train_scaled, X_test_scaled, _ = get_standard_scaled(X_train, X_test)
X_train_mm,    X_test_mm,     _ = get_minmax_scaled(X_train, X_test)


# ── KNN ───────────────────────────────────────────────────────────────────────
# Find best K
test_acc = []
for k in range(1, 31):
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train_scaled, y_train)
    test_acc.append(accuracy_score(y_test, knn.predict(X_test_scaled)))
best_k = int(np.argmax(test_acc)) + 1

knn_model = KNeighborsClassifier(n_neighbors=best_k, weights="distance", metric="euclidean")
knn_model.fit(X_train_scaled, y_train)
y_prob_knn = knn_model.predict_proba(X_test_scaled)[:, 1]

knn_gs = GridSearchCV(
    KNeighborsClassifier(),
    {"n_neighbors": [3,5,7,9,11,13,15], "weights": ["uniform","distance"], "metric": ["euclidean","manhattan"]},
    cv=5, scoring="accuracy", n_jobs=-1
)
knn_gs.fit(X_train_scaled, y_train)
y_prob_knn_gs = knn_gs.best_estimator_.predict_proba(X_test_scaled)[:, 1]


# ── Random Forest ─────────────────────────────────────────────────────────────
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
y_prob_rf = rf_model.predict_proba(X_test)[:, 1]

rf_gs = GridSearchCV(
    RandomForestClassifier(random_state=42),
    {
        "n_estimators": [50, 100, 200],
        "max_depth": [None, 5, 10, 15],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
        "max_features": ["sqrt", "log2"],
    },
    cv=5, scoring="accuracy", n_jobs=-1
)
rf_gs.fit(X_train, y_train)
y_prob_rf_gs = rf_gs.best_estimator_.predict_proba(X_test)[:, 1]


# ── Multinomial NB ────────────────────────────────────────────────────────────
mnb_model = MultinomialNB(alpha=1.0)
mnb_model.fit(X_train_mm, y_train)
y_prob_mnb = mnb_model.predict_proba(X_test_mm)[:, 1]

mnb_gs = GridSearchCV(
    MultinomialNB(),
    {"alpha": [0.001, 0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0], "fit_prior": [True, False]},
    cv=5, scoring="accuracy", n_jobs=-1
)
mnb_gs.fit(X_train_mm, y_train)
y_prob_mnb_gs = mnb_gs.best_estimator_.predict_proba(X_test_mm)[:, 1]


# ── Accuracy comparison ───────────────────────────────────────────────────────
models = {
    "KNN":               accuracy_score(y_test, knn_model.predict(X_test_scaled)),
    "KNN (GridSearchCV)":accuracy_score(y_test, knn_gs.best_estimator_.predict(X_test_scaled)),
    "Random Forest":     accuracy_score(y_test, rf_model.predict(X_test)),
    "RF (GridSearchCV)": accuracy_score(y_test, rf_gs.best_estimator_.predict(X_test)),
    "Multinomial NB":    accuracy_score(y_test, mnb_model.predict(X_test_mm)),
    "MNB (GridSearchCV)":accuracy_score(y_test, mnb_gs.best_estimator_.predict(X_test_mm)),
}

print("\n── Model Accuracy Comparison ─────────────────")
for name, acc in sorted(models.items(), key=lambda x: -x[1]):
    print(f"  {name:<25} {acc:.4f}")

colors = ["steelblue","cornflowerblue","seagreen","mediumseagreen","darkorange","sandybrown"]
plt.figure(figsize=(12, 6))
plt.bar(list(models.keys()), list(models.values()), color=colors, edgecolor="black")
plt.xticks(rotation=30, ha="right")
plt.ylim(0.7, 1.0)
plt.ylabel("Accuracy")
plt.title("Model Comparison – Heart Disease Prediction")
plt.tight_layout()
plt.savefig("model_comparison.png")
plt.show()



# ── ROC curves ────────────────────────────────────────────────────────────────
plt.figure(figsize=(9, 7))
for label, probs in [
    ("KNN",              y_prob_knn),
    ("KNN (GS)",         y_prob_knn_gs),
    ("Random Forest",    y_prob_rf),
    ("RF (GS)",          y_prob_rf_gs),
    ("Multinomial NB",   y_prob_mnb),
    ("MNB (GS)",         y_prob_mnb_gs),
]:
    fpr, tpr, _ = roc_curve(y_test, probs)
    auc = roc_auc_score(y_test, probs)
    plt.plot(fpr, tpr, label=f"{label} (AUC={auc:.3f})")

plt.plot([0, 1], [0, 1], "k--", label="Random")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curves – All Models")
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig("roc_curves_all.png")
plt.show()
