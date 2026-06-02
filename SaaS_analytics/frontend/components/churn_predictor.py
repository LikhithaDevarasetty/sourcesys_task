# components/churn_predictor.py
"""
AI Customer Churn Prediction Component — fully hardened.
Adapts dynamically to any dataset. Never crashes on missing columns,
empty data, or unexpected dtypes.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.ml_model import train_churn_model, predict_single_churn, get_recommendation_plan

# ── Telco friendly widget definitions ────────────────────────────────────────
_TELCO_CAT_WIDGETS = {
    'Contract':         ("Contract Type",              ["Month-to-month", "One year", "Two year"]),
    'InternetService':  ("Internet Service Type",      ["Fiber optic", "DSL", "No"]),
    'TechSupport':      ("Tech Support Active?",       ["No", "Yes"]),
    'OnlineSecurity':   ("Online Security Active?",    ["No", "Yes"]),
    'PaymentMethod':    ("Payment Method",             ["Electronic check", "Mailed check",
                                                        "Bank transfer (automatic)", "Credit card (automatic)"]),
    'PaperlessBilling': ("Paperless Billing?",         ["Yes", "No"]),
    'MultipleLines':    ("Multiple Phone Lines?",      ["No", "Yes"]),
    'Partner':          ("Has Partner?",               ["No", "Yes"]),
    'Dependents':       ("Has Dependents?",            ["No", "Yes"]),
    'SeniorCitizen':    ("Senior Citizen?",            ["No", "Yes"]),
    'gender':           ("Customer Gender",            ["Female", "Male"]),
    'PhoneService':     ("Phone Service Active?",      ["Yes", "No"]),
    'OnlineBackup':     ("Online Backup?",             ["No", "Yes"]),
    'DeviceProtection': ("Device Protection?",         ["No", "Yes"]),
    'StreamingTV':      ("Streaming TV?",              ["No", "Yes"]),
    'StreamingMovies':  ("Streaming Movies?",          ["No", "Yes"]),
}

_TELCO_NUM_WIDGETS = {
    'tenure':         ("Customer Tenure (Months Active)", 1,    72,     12,   1),
    'MonthlyCharges': ("Monthly Charges ($)",             18.0, 120.0,  65.0, 0.5),
    'TotalCharges':   ("Total Charges ($)",               0.0,  10000.0,780.0,10.0),
}

# Friendly display names for feature importance chart
_FEAT_NAME_MAP = {
    'Contract_One year':                     'Contract: 1-Year Tier',
    'Contract_Two year':                     'Contract: 2-Year Tier',
    'InternetService_Fiber optic':           'Internet: Fiber Optic',
    'InternetService_No':                    'No Internet Service',
    'PaymentMethod_Credit card (automatic)': 'Pay: Auto Credit Card',
    'PaymentMethod_Electronic check':        'Pay: Electronic Check',
    'PaymentMethod_Mailed check':            'Pay: Mailed Check',
    'OnlineSecurity_Yes':                    'Active Online Security',
    'TechSupport_Yes':                       'Active Tech Support',
    'PaperlessBilling_Yes':                  'Paperless Billing',
    'MultipleLines_Yes':                     'Multiple Phone Lines',
    'Dependents_Yes':                        'Account has Dependents',
    'Partner_Yes':                           'Account has Partner',
    'SeniorCitizen_Yes':                     'Senior Citizen Account',
    'tenure':                                'Tenure Length (Loyalty)',
    'MonthlyCharges':                        'Monthly Subscription Cost',
    'TotalCharges_Log':                      'Total Charges (log)',
}


def _safe_col_uniques(df, col, max_cats=30):
    """Return up to max_cats unique non-null string values for a column."""
    try:
        vals = df[col].dropna().astype(str).unique().tolist()
        return vals[:max_cats] if vals else ['Unknown']
    except Exception:
        return ['Unknown']


def _safe_col_range(df, col):
    """Return (min, max, median, step) for a numeric column."""
    try:
        s = pd.to_numeric(df[col], errors='coerce').dropna()
        if len(s) == 0:
            return 0.0, 100.0, 50.0, 1.0
        mn, mx, med = float(s.min()), float(s.max()), float(s.median())
        if mn == mx:
            mx = mn + 1.0
        step = max(0.01, round((mx - mn) / 100, 2))
        return mn, mx, med, step
    except Exception:
        return 0.0, 100.0, 50.0, 1.0


def _render_dynamic_form(df, model_pack):
    """
    Render What-If widgets for every column the model was trained on.
    Returns user_inputs dict. Never raises.
    """
    cat_cols  = model_pack.get("categorical_cols", [])
    num_cols  = model_pack.get("numeric_cols", [])
    has_tc    = model_pack.get("has_total_charges", False)

    num_cols_full = list(num_cols) + (['TotalCharges'] if has_tc else [])

    user_inputs = {}
    all_items   = [(c, 'cat') for c in cat_cols] + [(c, 'num') for c in num_cols_full]
    mid         = max(1, (len(all_items) + 1) // 2)

    fcol1, fcol2 = st.columns(2)

    for i, (col, kind) in enumerate(all_items):
        target_col = fcol1 if i < mid else fcol2
        with target_col:
            try:
                if kind == 'cat':
                    widget_def = _TELCO_CAT_WIDGETS.get(col)
                    if widget_def:
                        label, options = widget_def
                    else:
                        label = col
                        options = _safe_col_uniques(df, col)
                    user_inputs[col] = st.selectbox(label, options, key=f"c_cat_{col}")
                else:
                    widget_def = _TELCO_NUM_WIDGETS.get(col)
                    if widget_def:
                        label, mn, mx, default, step = widget_def
                        user_inputs[col] = st.slider(label, min_value=mn, max_value=mx,
                                                     value=default, step=step, key=f"c_num_{col}")
                    else:
                        mn, mx, med, step = _safe_col_range(df, col)
                        user_inputs[col] = st.number_input(
                            col, min_value=mn, max_value=mx, value=med,
                            step=step, key=f"c_num_{col}"
                        )
            except Exception:
                # If a widget fails, give it a safe default and keep going
                user_inputs[col] = 0 if kind == 'num' else 'Unknown'

    # Compute TotalCharges if it wasn't directly collected
    if has_tc and 'TotalCharges' not in user_inputs:
        try:
            tenure  = float(user_inputs.get('tenure', 12) or 12)
            monthly = float(user_inputs.get('MonthlyCharges', 65.0) or 65.0)
            user_inputs['TotalCharges'] = tenure * monthly
        except Exception:
            user_inputs['TotalCharges'] = 780.0

    return user_inputs


def render_churn_predictor(df):
    """
    Renders the ML Churn Analysis panel.
    Works with any dataset; shows meaningful messages on degenerate data.
    """
    st.markdown(
        '<h1 class="platform-title" style="text-align:left;font-size:2.2rem;margin-bottom:5px;">'
        'Customer Churn Risk Analysis</h1>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="platform-subtitle" style="text-align:left;margin-bottom:25px;">'
        'Predict customer churn probability and generate structured retention playbooks '
        'based on customer attributes</p>',
        unsafe_allow_html=True
    )

    # Guard: empty dataframe
    if df is None or len(df) == 0:
        st.warning("⚠️ The dataset is empty. Please upload a valid CSV with at least a few rows.")
        return

    # 1. Train (always returns a dict, never raises)
    with st.spinner("Loading Churn Prediction Model..."):
        model_pack = train_churn_model(df, _version=5)

    # Show training error message if model failed
    if model_pack.get("error"):
        st.error(f"⚠️ Model could not be trained: {model_pack['error']}\n\n"
                 "The dataset may not have enough variety to build a churn model. "
                 "Please check your CSV has a 'Churn' column (Yes/No) and varied feature columns.")
        return

    col_left, col_right = st.columns([5, 4])

    # ── LEFT: What-If form ───────────────────────────────────────────────────
    with col_left:
        st.markdown(
            """
            <div class="glass-card" style="margin-bottom:20px;">
                <div class="card-title">🔮 Customer Churn Risk Simulator</div>
                <p style="color:#a0a0c0;font-size:0.85rem;margin:0;">
                Adjust the indicators below to simulate a customer profile and calculate
                their churn risk in real-time.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if not model_pack["categorical_cols"] and not model_pack["numeric_cols"]:
            st.info("No feature columns detected — please check your dataset structure.")
            churn_probability = 0.5
        else:
            user_inputs      = _render_dynamic_form(df, model_pack)
            churn_probability = predict_single_churn(model_pack, user_inputs)

    # ── RIGHT: Prediction card ───────────────────────────────────────────────
    with col_right:
        if churn_probability < 0.3:
            glow_class = "glass-card-accent-emerald"
            text_color = "#2ed573"
            risk_label = "Low Churn Risk"
        elif churn_probability < 0.6:
            glow_class = "glass-card-accent-amber"
            text_color = "#ffa502"
            risk_label = "Moderate Churn Risk"
        else:
            glow_class = "glass-card-accent-crimson"
            text_color = "#ff4757"
            risk_label = "HIGH CHURN RISK"

        st.markdown(
            f"""
            <div class="glass-card {glow_class}">
                <div class="card-title" style="color:{text_color};margin-bottom:12px;">
                    ⚡ Risk Assessment Analysis</div>
                <div class="predict-box">
                    <div class="risk-level" style="color:{text_color};">{risk_label}</div>
                    <div class="predict-percentage" style="color:{text_color};">
                        {churn_probability*100:.1f}%</div>
                    <p style="color:#a0a0c0;font-size:0.85rem;margin-top:5px;">
                        Model Accuracy: {model_pack['accuracy']*100:.1f}%</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        recommendations = get_recommendation_plan(
            user_inputs if model_pack["categorical_cols"] or model_pack["numeric_cols"] else {},
            churn_probability
        )
        rec_html = "".join(
            f'<div style="font-size:0.9rem;color:#e0e0ff;margin-bottom:10px;line-height:1.4;">{r}</div>'
            for r in recommendations
        )
        st.markdown(
            f"""
            <div class="glass-card" style="margin-top:-10px;">
                <div class="card-title" style="margin-bottom:12px;">
                    💡 Actionable Intervention Playbook</div>
                {rec_html}
            </div>
            """,
            unsafe_allow_html=True
        )

    # ── Feature Importance chart ─────────────────────────────────────────────
    st.markdown('<div style="margin-top:15px;"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="glass-card" style="margin-bottom:15px;">
            <div class="card-title" style="margin-bottom:0px;">
                🔍 Churn Risk Drivers (Top 8 Feature Importances)</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    try:
        feat_imp = pd.Series(model_pack["feature_importances"]).reset_index()
        feat_imp.columns = ['Feature', 'Importance']
        feat_imp['Feature'] = feat_imp['Feature'].map(
            lambda x: _FEAT_NAME_MAP.get(x, x)
        )
        feat_imp = (feat_imp[feat_imp['Importance'] > 0]
                    .sort_values('Importance', ascending=True)
                    .tail(8))

        if feat_imp.empty:
            st.info("Feature importance not available for this dataset.")
        else:
            fig_imp = px.bar(
                feat_imp, x='Importance', y='Feature',
                orientation='h', color='Importance',
                color_continuous_scale=['#00cec9', '#6c5ce7']
            )
            fig_imp.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)',
                           color='#a0a0c0', title="Feature Weight Contribution"),
                yaxis=dict(color='#e0e0ff', title=None),
                coloraxis_showscale=False,
                margin=dict(l=10, r=10, t=10, b=10),
                height=260
            )
            st.plotly_chart(fig_imp, use_container_width=True)
    except Exception as e:
        st.info(f"Feature importance chart could not be rendered: {e}")
