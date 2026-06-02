# utils/ml_model.py
import pandas as pd
import numpy as np
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.dummy import DummyClassifier

# ── Telco-default column sets (used only for the built-in dataset) ──────────
_DEFAULT_CATEGORICAL = [
    'gender', 'SeniorCitizen', 'Partner', 'Dependents',
    'PhoneService', 'MultipleLines', 'InternetService',
    'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
    'TechSupport', 'StreamingTV', 'StreamingMovies',
    'Contract', 'PaperlessBilling', 'PaymentMethod'
]
_DEFAULT_NUMERIC = ['tenure', 'MonthlyCharges', 'TotalCharges']


def _detect_columns(df):
    """
    Auto-detect which categorical and numeric columns are actually present
    in the DataFrame and usable for churn modelling.
    Churn / target column is excluded from feature sets.
    """
    exclude = {'Churn', 'customerID', 'TenureGroup', 'Row ID', 'Customer ID'}

    numeric_candidates = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_candidates = df.select_dtypes(include=['object', 'category']).columns.tolist()

    numeric_cols = [c for c in numeric_candidates if c not in exclude]
    categorical_cols = [c for c in cat_candidates if c not in exclude]

    return categorical_cols, numeric_cols


@st.cache_resource
def train_churn_model(df):
    """
    Train a GradientBoosting churn model on whatever columns exist in df.
    Falls back to DummyClassifier when the target has fewer than 2 classes.
    """
    # ── 1. Detect which columns are actually present ────────────────────────
    categorical_cols, numeric_cols = _detect_columns(df)

    # We need at least a Churn column to train
    if 'Churn' not in df.columns:
        df = df.copy()
        df['Churn'] = 'No'

    model_df = df[categorical_cols + numeric_cols + ['Churn']].copy()

    # ── 2. Encode target ────────────────────────────────────────────────────
    # Always convert via string mapping first — avoids dtype issues with
    # ArrowDtype string columns in newer pandas (can't cast str → int directly)
    churn_col = model_df['Churn'].fillna('No')
    model_df['Churn'] = churn_col.apply(
        lambda v: 1 if str(v).strip().lower() in ('yes', '1', 'true', 'churned') else 0
    ).astype(int)

    # ── 3. Build feature matrix ─────────────────────────────────────────────
    # Categorical → one-hot
    if categorical_cols:
        X_cat = pd.get_dummies(model_df[categorical_cols], drop_first=True, dtype=int)
    else:
        X_cat = pd.DataFrame(index=model_df.index)

    # Numeric → keep + log-transform TotalCharges if present
    X_num = model_df[numeric_cols].copy()
    if 'TotalCharges' in X_num.columns:
        X_num['TotalCharges_Log'] = np.log1p(X_num['TotalCharges'])
        X_num = X_num.drop(columns=['TotalCharges'])

    X = pd.concat([X_cat, X_num], axis=1)
    y = model_df['Churn']

    feature_columns = X.columns.tolist()
    unique_classes = y.nunique()

    # ── 4. Train ────────────────────────────────────────────────────────────
    if unique_classes < 2 or len(X) < 10:
        # Not enough data / only one class → dummy fallback
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        model = DummyClassifier(strategy="most_frequent")
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        roc_auc = 0.5
        feature_importances = {col: 0.0 for col in feature_columns}
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        model = GradientBoostingClassifier(
            n_estimators=150,
            learning_rate=0.05,
            max_depth=4,
            subsample=0.8,
            min_samples_leaf=20,
            random_state=42
        )
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]

        accuracy = accuracy_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        feature_importances = (
            pd.Series(model.feature_importances_, index=feature_columns)
            .sort_values(ascending=False)
            .to_dict()
        )

    return {
        "model": model,
        "feature_columns": feature_columns,
        "categorical_cols": categorical_cols,
        "numeric_cols": [c for c in numeric_cols if c != 'TotalCharges'],  # after log-transform
        "has_total_charges": 'TotalCharges' in numeric_cols,
        "accuracy": accuracy,
        "roc_auc": roc_auc,
        "feature_importances": feature_importances,
        "train_columns_template": pd.DataFrame(columns=feature_columns)
    }


def predict_single_churn(model_pack, inputs):
    """
    Run inference for a single customer profile dict.
    Only uses the columns that were actually trained on.
    """
    model = model_pack["model"]
    feature_cols = model_pack["feature_columns"]
    cat_cols = model_pack["categorical_cols"]
    num_cols = model_pack["numeric_cols"]
    has_total_charges = model_pack.get("has_total_charges", True)

    # Build a 1-row dataframe with only the columns the model knows about
    input_subset = {k: v for k, v in inputs.items() if k in cat_cols + num_cols + ['TotalCharges']}
    raw_df = pd.DataFrame([input_subset])

    # One-hot encode the categorical columns that exist
    present_cat = [c for c in cat_cols if c in raw_df.columns]
    if present_cat:
        encoded_cat = pd.get_dummies(raw_df[present_cat], dtype=int)
    else:
        encoded_cat = pd.DataFrame(index=raw_df.index)

    # Start from a zero-filled template (ensures all trained columns are present)
    pred_dict = {col: 0.0 for col in feature_cols}

    # Fill in one-hot values
    for col in encoded_cat.columns:
        if col in pred_dict:
            pred_dict[col] = float(encoded_cat.iloc[0][col])

    # Fill in numeric values
    for nc in num_cols:
        if nc in inputs:
            pred_dict[nc] = float(inputs[nc])

    # Handle TotalCharges log-transform
    if has_total_charges and 'TotalCharges_Log' in pred_dict:
        tc = float(inputs.get('TotalCharges', 0))
        pred_dict['TotalCharges_Log'] = float(np.log1p(tc))

    pred_df = pd.DataFrame([pred_dict])[feature_cols]

    probas = model.predict_proba(pred_df)
    if probas.shape[1] < 2:
        return float(model.classes_[0])
    return float(probas[0, 1])


def get_recommendation_plan(inputs, churn_prob):
    recommendations = []
    if churn_prob < 0.3:
        return [
            "🟢 **Stable Account**: Maintain regular service quality.",
            "💡 **Upsell opportunity**: Suggest adding value-added features like StreamingTV."
        ]

    if inputs.get('Contract') == 'Month-to-month':
        recommendations.append("📅 **Upgrade Contract**: Move to a **1-Year or 2-Year Contract** to lock in loyalty (Month-to-month contracts are high risk).")

    if inputs.get('InternetService') == 'Fiber optic' and inputs.get('TechSupport') == 'No':
        recommendations.append("🛡️ **Add Tech Support**: Fiber optic accounts without support are high risk. Offer a 3-month free trial.")

    if inputs.get('OnlineSecurity') == 'No':
        recommendations.append("🔒 **Add Online Security**: Bundle security features to improve account stickiness.")

    if inputs.get('PaymentMethod') == 'Electronic check':
        recommendations.append("💳 **Automate Billing**: Encourage transition to **Auto-Pay (Credit Card or Bank Transfer)**.")

    if inputs.get('tenure', 12) < 6:
        recommendations.append("🎁 **Onboarding Call**: Customer is in onboarding phase (< 6 months). Trigger a customer success check-in.")

    if not recommendations:
        recommendations.append("💸 **Loyalty Check**: Reach out with a discount offer to secure their retention.")

    return recommendations
