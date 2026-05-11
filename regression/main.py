import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.pipeline import Pipeline


# load the dataset
df = pd.read_csv("heart copy.csv")

print(df.shape)
print(df.head())
print(df.info())
print(df.isnull().sum())
print(df.describe())
print(df['target'].value_counts())


# -------------------------------------------------------
# PREPROCESSING
# -------------------------------------------------------

# split features and label
X = df.drop('target', axis=1)
y = df['target']

# train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print("Train size:", X_train.shape)
print("Test size:", X_test.shape)

# standard scaling (needed for KNN)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# minmax scaling (needed for Multinomial NB since it needs non-negative values)
mm = MinMaxScaler()
X_train_mm = mm.fit_transform(X_train)
X_test_mm = mm.transform(X_test)


# -------------------------------------------------------
# KNN MODEL
# -------------------------------------------------------

# find the best k value
train_acc = []
test_acc = []

for k in range(1, 31):
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train_scaled, y_train)
    train_acc.append(accuracy_score(y_train, knn.predict(X_train_scaled)))
    test_acc.append(accuracy_score(y_test, knn.predict(X_test_scaled)))

best_k = np.argmax(test_acc) + 1
print("Best K:", best_k)

# plot k vs accuracy
plt.figure(figsize=(10, 5))
plt.plot(range(1, 31), train_acc, label='Train Accuracy', marker='o')
plt.plot(range(1, 31), test_acc, label='Test Accuracy', marker='s')
plt.axvline(x=best_k, color='red', linestyle='--', label=f'Best K = {best_k}')
plt.xlabel('K Value')
plt.ylabel('Accuracy')
plt.title('KNN - K vs Accuracy')
plt.legend()
plt.tight_layout()
plt.savefig('knn_k_vs_accuracy.png')
plt.show()

# train final knn with best k
knn_model = KNeighborsClassifier(n_neighbors=best_k, weights='distance', metric='euclidean')
knn_model.fit(X_train_scaled, y_train)

y_pred_knn = knn_model.predict(X_test_scaled)
y_prob_knn = knn_model.predict_proba(X_test_scaled)[:, 1]

print("KNN Accuracy:", accuracy_score(y_test, y_pred_knn))
print("KNN ROC AUC:", roc_auc_score(y_test, y_prob_knn))
print(classification_report(y_test, y_pred_knn))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_knn))

# cross validation
cv_knn = cross_val_score(knn_model, X_train_scaled, y_train, cv=5)
print("KNN CV Accuracy:", cv_knn.mean(), "+-", cv_knn.std())


# -------------------------------------------------------
# RANDOM FOREST MODEL
# -------------------------------------------------------

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

y_pred_rf = rf_model.predict(X_test)
y_prob_rf = rf_model.predict_proba(X_test)[:, 1]

print("Random Forest Accuracy:", accuracy_score(y_test, y_pred_rf))
print("Random Forest ROC AUC:", roc_auc_score(y_test, y_prob_rf))
print(classification_report(y_test, y_pred_rf))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_rf))

# cross validation
cv_rf = cross_val_score(rf_model, X_train, y_train, cv=5)
print("RF CV Accuracy:", cv_rf.mean(), "+-", cv_rf.std())

# feature importance
feat_imp = pd.Series(rf_model.feature_importances_, index=X.columns).sort_values(ascending=False)
print(feat_imp)

plt.figure(figsize=(10, 6))
sns.barplot(x=feat_imp.values, y=feat_imp.index, palette='viridis')
plt.title('Random Forest - Feature Importances')
plt.xlabel('Importance')
plt.tight_layout()
plt.savefig('rf_feature_importances.png')
plt.show()


# -------------------------------------------------------
# GRIDSEARCHCV - HYPERPARAMETER TUNING
# -------------------------------------------------------

# grid search on KNN
knn_params = {
    'n_neighbors': [3, 5, 7, 9, 11, 13, 15],
    'weights': ['uniform', 'distance'],
    'metric': ['euclidean', 'manhattan']
}

knn_grid = GridSearchCV(KNeighborsClassifier(), knn_params, cv=5, scoring='accuracy', n_jobs=-1, verbose=1)
knn_grid.fit(X_train_scaled, y_train)

print("Best KNN Params:", knn_grid.best_params_)
print("Best KNN CV Score:", knn_grid.best_score_)

y_pred_knn_gs = knn_grid.best_estimator_.predict(X_test_scaled)
y_prob_knn_gs = knn_grid.best_estimator_.predict_proba(X_test_scaled)[:, 1]

print("KNN (GridSearchCV) Accuracy:", accuracy_score(y_test, y_pred_knn_gs))
print(classification_report(y_test, y_pred_knn_gs))


# grid search on Random Forest
rf_params = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 5, 10, 15],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['sqrt', 'log2']
}

rf_grid = GridSearchCV(RandomForestClassifier(random_state=42), rf_params, cv=5, scoring='accuracy', n_jobs=-1, verbose=1)
rf_grid.fit(X_train, y_train)

print("Best RF Params:", rf_grid.best_params_)
print("Best RF CV Score:", rf_grid.best_score_)

y_pred_rf_gs = rf_grid.best_estimator_.predict(X_test)
y_prob_rf_gs = rf_grid.best_estimator_.predict_proba(X_test)[:, 1]

print("RF (GridSearchCV) Accuracy:", accuracy_score(y_test, y_pred_rf_gs))
print(classification_report(y_test, y_pred_rf_gs))

# top 5 RF results
rf_results = pd.DataFrame(rf_grid.cv_results_)
top5 = rf_results.sort_values('mean_test_score', ascending=False).head(5)[['params', 'mean_test_score', 'std_test_score']]
print(top5)


# -------------------------------------------------------
# MULTINOMIAL NAIVE BAYES
# -------------------------------------------------------

# baseline model with default alpha
mnb = MultinomialNB(alpha=1.0)
mnb.fit(X_train_mm, y_train)

y_pred_mnb = mnb.predict(X_test_mm)
y_prob_mnb = mnb.predict_proba(X_test_mm)[:, 1]

print("Multinomial NB Accuracy:", accuracy_score(y_test, y_pred_mnb))
print("Multinomial NB ROC AUC:", roc_auc_score(y_test, y_prob_mnb))
print(classification_report(y_test, y_pred_mnb))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_mnb))

cv_mnb = cross_val_score(mnb, X_train_mm, y_train, cv=5)
print("MNB CV Accuracy:", cv_mnb.mean(), "+-", cv_mnb.std())

# grid search on MNB - tuning alpha (smoothing)
mnb_params = {
    'alpha': [0.001, 0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0],
    'fit_prior': [True, False]
}

mnb_grid = GridSearchCV(MultinomialNB(), mnb_params, cv=5, scoring='accuracy', n_jobs=-1, verbose=1)
mnb_grid.fit(X_train_mm, y_train)

print("Best MNB Params:", mnb_grid.best_params_)
print("Best MNB CV Score:", mnb_grid.best_score_)

y_pred_mnb_gs = mnb_grid.best_estimator_.predict(X_test_mm)
y_prob_mnb_gs = mnb_grid.best_estimator_.predict_proba(X_test_mm)[:, 1]

print("MNB (GridSearchCV) Accuracy:", accuracy_score(y_test, y_pred_mnb_gs))
print(classification_report(y_test, y_pred_mnb_gs))

# -------------------------------------------------------
# MODEL COMPARISON
# -------------------------------------------------------

results = {
    'KNN': accuracy_score(y_test, y_pred_knn),
    'KNN (GridSearchCV)': accuracy_score(y_test, y_pred_knn_gs),
    'Random Forest': accuracy_score(y_test, y_pred_rf),
    'RF (GridSearchCV)': accuracy_score(y_test, y_pred_rf_gs),
    'Multinomial NB': accuracy_score(y_test, y_pred_mnb),
    'MNB (GridSearchCV)': accuracy_score(y_test, y_pred_mnb_gs)
}

results_df = pd.DataFrame(list(results.items()), columns=['Model', 'Accuracy'])
results_df = results_df.sort_values('Accuracy', ascending=False)
print(results_df)

plt.figure(figsize=(12, 6))
plt.bar(results_df['Model'], results_df['Accuracy'],
        color=['steelblue', 'cornflowerblue', 'seagreen', 'mediumseagreen', 'darkorange', 'sandybrown'],
        edgecolor='black')
plt.xticks(rotation=30, ha='right')
plt.ylim(0.7, 1.0)
plt.ylabel('Accuracy')
plt.title('Model Comparison - Heart Disease Prediction')
plt.tight_layout()
plt.savefig('model_comparison.png')
plt.show()

# ROC curves for all models
plt.figure(figsize=(9, 7))
for label, probs in [
    ('KNN', y_prob_knn),
    ('KNN (GS)', y_prob_knn_gs),
    ('Random Forest', y_prob_rf),
    ('RF (GS)', y_prob_rf_gs),
    ('Multinomial NB', y_prob_mnb),
    ('MNB (GS)', y_prob_mnb_gs)
]:
    fpr, tpr, _ = roc_curve(y_test, probs)
    auc = roc_auc_score(y_test, probs)
    plt.plot(fpr, tpr, label=f'{label} (AUC = {auc:.3f})')

plt.plot([0, 1], [0, 1], 'k--', label='Random')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curves - All Models')
plt.legend(loc='lower right')
plt.tight_layout()
plt.savefig('roc_curves.png')
plt.show()