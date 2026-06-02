# utils/ml_model.py
"""
Churn ML Model — fully hardened against all known failure modes.
Never raises an uncaught exception from any public function.
"""
import pandas as pd
import numpy as np
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.dummy import DummyClassifier

# Columns that are NEVER features
_EXCLUDE = {
    'Churn', 'customerID', 'TenureGroup', 'Row ID', 'Customer ID',
    'Order Date', 'Order_Month', 'Order_Month_Str', 'Order_Year',
    'Profit_Margin', 'index'
}


def _detect_columns(df):
    """Auto-detect categorical and numeric columns from df, skipping excludes and zero-variance cols."""
    usable = [c for c in df.columns if c not in _EXCLUDE]
    cat_cols, num_cols = [], []
    for col in usable:
        try:
            series = df[col]
            non_null = pd.to_numeric(series, errors='coerce').dropna()
            total_non_null = series.dropna()
            if len(total_non_null) == 0:
                continue
            numeric_ratio = len(non_null) / len(total_non_null)
            if numeric_ratio >= 0.8:
                if non_null.nunique() > 1:
                    num_cols.append(col)
            else:
                str_series = series.dropna().astype(str)
                if 1 < str_series.nunique() <= 50:
                    cat_cols.append(col)
        except Exception:
            continue
    return cat_cols, num_cols


def _impute_X(X):
    """Fill all NaN in feature matrix with column medians. Returns (X_clean, medians_dict)."""
    col_medians = {}
    X = X.copy()
    for col in X.columns:
        try:
            X[col] = pd.to_numeric(X[col], errors='coerce')
        except Exception:
            X[col] = 0.0
        median_val = X[col].median()
        if pd.isna(median_val):
            median_val = 0.0
        col_medians[col] = float(median_val)
        X[col] = X[col].fillna(median_val)
    return X, col_medians


def _encode_churn(series):
    """Map any representation of churn to 0/1 int. Never raises."""
    def _map(v):
        try:
            return 1 if str(v).strip().lower() in ('yes', '1', 'true', 'churned', 'churn') else 0
        except Exception:
            return 0
    return series.fillna('No').apply(_map).astype(int)


def _get_importances(model, X_test, y_test, feature_columns):
    """
    Return feature importances as {col: float} dict.
    Uses native feature_importances_ if available (RF, GBC, etc.).
    Falls back to permutation_importance, then zero weights if everything fails.
    """
    # Try native feature importances first (extremely fast, zero overhead)
    try:
        if hasattr(model, 'feature_importances_'):
            return (
                pd.Series(model.feature_importances_, index=feature_columns)
                .sort_values(ascending=False)
                .to_dict()
            )
    except Exception:
        pass

    # Try permutation importance as a fallback
    try:
        from sklearn.inspection import permutation_importance
        perm = permutation_importance(
            model, X_test, y_test, n_repeats=5, random_state=42, n_jobs=-1
        )
        return (
            pd.Series(perm.importances_mean, index=feature_columns)
            .sort_values(ascending=False)
            .to_dict()
        )
    except Exception:
        return {col: 0.0 for col in feature_columns}


@st.cache_resource
def train_churn_model(df, _version=5):
    """
    Train a churn model on whatever columns exist in df.
    Always returns a dict — never raises. On failure, returns {error: message}.
    """
    try:
        if df is None or len(df) < 5:
            raise ValueError("Dataset too small (need at least 5 rows).")

        df = df.copy()

        if 'Churn' not in df.columns:
            df['Churn'] = 'No'

        categorical_cols, numeric_cols = _detect_columns(df)

        if not categorical_cols and not numeric_cols:
            raise ValueError("No usable feature columns found in dataset.")

        y = _encode_churn(df['Churn'])

        # Build categorical features
        if categorical_cols:
            cat_df = df[categorical_cols].copy()
            for c in categorical_cols:
                try:
                    cat_df[c] = cat_df[c].astype(str).replace('nan', np.nan)
                except Exception:
                    cat_df[c] = 'Unknown'
            X_cat = pd.get_dummies(cat_df, drop_first=True, dtype=float)
            X_cat = X_cat.fillna(0.0)
        else:
            X_cat = pd.DataFrame(index=df.index)

        # Build numeric features
        if numeric_cols:
            X_num = df[numeric_cols].copy()
            for nc in numeric_cols:
                X_num[nc] = pd.to_numeric(X_num[nc], errors='coerce')
            if 'TotalCharges' in X_num.columns:
                X_num['TotalCharges_Log'] = np.log1p(X_num['TotalCharges'].fillna(0))
                X_num = X_num.drop(columns=['TotalCharges'])
        else:
            X_num = pd.DataFrame(index=df.index)

        X = pd.concat([X_cat, X_num], axis=1)
        X, col_medians = _impute_X(X)
        feature_columns = X.columns.tolist()

        if len(feature_columns) == 0:
            raise ValueError("Feature matrix is empty after processing.")

        unique_classes = y.nunique()

        if unique_classes < 2 or len(X) < 10:
            # Degenerate dataset — use dummy model
            split_size = min(0.2, max(1, len(X) // 5) / len(X))
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=split_size, random_state=42
            )
            model = DummyClassifier(strategy="most_frequent")
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            accuracy = float(accuracy_score(y_test, y_pred))
            roc_auc = 0.5
            feature_importances = {col: 0.0 for col in feature_columns}
        else:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            model = RandomForestClassifier(
                n_estimators=100, max_depth=8,
                min_samples_leaf=5, random_state=42, n_jobs=-1
            )
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            accuracy = float(accuracy_score(y_test, y_pred))
            try:
                roc_auc = float(roc_auc_score(y_test, y_pred_proba))
            except Exception:
                roc_auc = 0.5
            feature_importances = _get_importances(model, X_test, y_test, feature_columns)

        return {
            "model": model,
            "feature_columns": feature_columns,
            "categorical_cols": categorical_cols,
            "numeric_cols": [c for c in (numeric_cols or []) if c != 'TotalCharges'],
            "has_total_charges": 'TotalCharges' in (numeric_cols or []),
            "col_medians": col_medians,
            "accuracy": accuracy,
            "roc_auc": roc_auc,
            "feature_importances": feature_importances,
            "error": None,
        }

    except Exception as e:
        return {
            "model": None,
            "feature_columns": [],
            "categorical_cols": [],
            "numeric_cols": [],
            "has_total_charges": False,
            "col_medians": {},
            "accuracy": 0.0,
            "roc_auc": 0.0,
            "feature_importances": {},
            "error": str(e),
        }


def predict_single_churn(model_pack, inputs):
    """Run inference for one customer profile. Returns float in [0, 1]. Never raises."""
    try:
        model = model_pack.get("model")
        if model is None:
            return 0.5

        feature_cols = model_pack["feature_columns"]
        cat_cols = model_pack["categorical_cols"]
        num_cols = model_pack["numeric_cols"]
        has_total_charges = model_pack.get("has_total_charges", False)
        col_medians = model_pack.get("col_medians", {})

        if not feature_cols:
            return 0.5

        # One-hot encode categoricals
        present_cat = [c for c in cat_cols if c in inputs]
        if present_cat:
            cat_input = {c: str(inputs[c]) for c in present_cat}
            raw_df = pd.DataFrame([cat_input])
            encoded_cat = pd.get_dummies(raw_df[present_cat], dtype=float)
        else:
            encoded_cat = pd.DataFrame()

        # Start from median-filled template
        pred_dict = {col: col_medians.get(col, 0.0) for col in feature_cols}

        # Fill one-hot values
        for col in encoded_cat.columns:
            if col in pred_dict:
                try:
                    pred_dict[col] = float(encoded_cat.iloc[0][col])
                except Exception:
                    pass

        # Fill numeric values
        for nc in num_cols:
            if nc in inputs:
                try:
                    pred_dict[nc] = float(inputs[nc])
                except Exception:
                    pass

        # Log-transform TotalCharges
        if has_total_charges and 'TotalCharges_Log' in pred_dict:
            try:
                tc = float(inputs.get('TotalCharges', 0) or 0)
                pred_dict['TotalCharges_Log'] = float(np.log1p(tc))
            except Exception:
                pred_dict['TotalCharges_Log'] = 0.0

        pred_df = pd.DataFrame([pred_dict])[feature_cols]

        # Final NaN safety
        for col in pred_df.columns:
            if pred_df[col].isna().any():
                pred_df[col] = pred_df[col].fillna(col_medians.get(col, 0.0))

        probas = model.predict_proba(pred_df)
        if probas.shape[1] < 2:
            return float(probas[0, 0])
        return float(np.clip(probas[0, 1], 0.0, 1.0))

    except Exception:
        return 0.5


def get_recommendation_plan(inputs, churn_prob):
    """Return list of recommendation strings. Never raises."""
    try:
        if churn_prob < 0.3:
            return [
                "🟢 **Stable Account**: Maintain regular service quality.",
                "💡 **Upsell opportunity**: Suggest adding value-added features like StreamingTV."
            ]
        recommendations = []
        if inputs.get('Contract') == 'Month-to-month':
            recommendations.append("📅 **Upgrade Contract**: Move to a **1-Year or 2-Year Contract** to lock in loyalty.")
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
    except Exception:
        return ["💡 **Review this account** for potential retention actions."]
