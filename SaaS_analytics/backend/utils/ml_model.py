# utils/ml_model.py
import pandas as pd
import numpy as np
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score

@st.cache_resource
def train_churn_model(df):
    categorical_cols = [
        'gender', 'SeniorCitizen', 'Partner', 'Dependents', 
        'PhoneService', 'MultipleLines', 'InternetService', 
        'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
        'TechSupport', 'StreamingTV', 'StreamingMovies', 
        'Contract', 'PaperlessBilling', 'PaymentMethod'
    ]
    numeric_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
    
    model_df = df[categorical_cols + numeric_cols + ['Churn']].copy()
    model_df['Churn'] = model_df['Churn'].map({'Yes': 1, 'No': 0}).fillna(0).astype(int)
    
    X_cat = pd.get_dummies(model_df[categorical_cols], drop_first=True, dtype=int)
    X_num = model_df[numeric_cols].copy()
    
    X_num['TotalCharges_Log'] = np.log1p(X_num['TotalCharges'])
    X_num = X_num.drop(columns=['TotalCharges'])
    
    X = pd.concat([X_cat, X_num], axis=1)
    y = model_df['Churn']
    
    feature_columns = X.columns.tolist()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        min_samples_leaf=4,
        random_state=42,
        class_weight='balanced'
    )
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    return {
        "model": model,
        "feature_columns": feature_columns,
        "categorical_cols": categorical_cols,
        "numeric_cols": numeric_cols,
        "accuracy": accuracy_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_pred_proba),
        "feature_importances": pd.Series(model.feature_importances_, index=feature_columns).sort_values(ascending=False).to_dict(),
        "train_columns_template": pd.DataFrame(columns=feature_columns)
    }

def predict_single_churn(model_pack, inputs):
    model = model_pack["model"]
    feature_cols = model_pack["feature_columns"]
    cat_cols = model_pack["categorical_cols"]
    
    raw_df = pd.DataFrame([inputs])
    encoded_cat = pd.get_dummies(raw_df[cat_cols], dtype=int)
    
    pred_dict = {col: 0.0 for col in feature_cols}
    for col in encoded_cat.columns:
        if col in pred_dict:
            pred_dict[col] = float(encoded_cat.loc[0, col])
            
    pred_dict['tenure'] = float(inputs.get('tenure', 12))
    pred_dict['MonthlyCharges'] = float(inputs.get('MonthlyCharges', 50.0))
    
    total_charges = float(inputs.get('TotalCharges', pred_dict['tenure'] * pred_dict['MonthlyCharges']))
    pred_dict['TotalCharges_Log'] = float(np.log1p(total_charges))
    
    pred_df = pd.DataFrame([pred_dict])[feature_cols]
    return model.predict_proba(pred_df)[0, 1]

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
