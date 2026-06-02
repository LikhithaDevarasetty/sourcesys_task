# components/churn_predictor.py
"""
AI Customer Churn Prediction Component
Combines machine learning analytics with interactive "What-If" sliders
to allow management to run risk simulations on any customer profile
and generates direct, actionable customer support recommendations.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.ml_model import train_churn_model, predict_single_churn, get_recommendation_plan


# ── Telco-specific widget definitions (used only when the Telco dataset is active) ──
_TELCO_CATEGORICAL_WIDGETS = {
    'Contract':        ("Contract Type",              ["Month-to-month", "One year", "Two year"]),
    'InternetService': ("Internet Service Type",       ["Fiber optic", "DSL", "No"]),
    'TechSupport':     ("Tech Support Active?",        ["No", "Yes"]),
    'OnlineSecurity':  ("Online Security Active?",     ["No", "Yes"]),
    'PaymentMethod':   ("Payment Method",              ["Electronic check", "Mailed check",
                                                        "Bank transfer (automatic)", "Credit card (automatic)"]),
    'PaperlessBilling':("Paperless Billing?",          ["Yes", "No"]),
    'MultipleLines':   ("Multiple Phone Lines?",       ["No", "Yes"]),
    'Partner':         ("Has Partner?",                ["No", "Yes"]),
    'Dependents':      ("Has Dependents?",             ["No", "Yes"]),
    'SeniorCitizen':   ("Senior Citizen?",             ["No", "Yes"]),
    'gender':          ("Customer Gender",             ["Female", "Male"]),
    'PhoneService':    ("Phone Service Active?",       ["Yes", "No"]),
    'OnlineBackup':    ("Online Backup?",              ["No", "Yes"]),
    'DeviceProtection':("Device Protection?",          ["No", "Yes"]),
    'StreamingTV':     ("Streaming TV?",               ["No", "Yes"]),
    'StreamingMovies': ("Streaming Movies?",           ["No", "Yes"]),
}

_TELCO_NUMERIC_WIDGETS = {
    'tenure':         ("Customer Tenure (Months Active)", 1,   72,   12,   1),
    'MonthlyCharges': ("Monthly Charges ($)",             18.0, 120.0, 65.0, 0.5),
    'TotalCharges':   ("Total Charges ($)",               0.0, 10000.0, 780.0, 10.0),
}


def _get_col_uniques(df, col, max_cats=30):
    """Return unique non-null string values for a column (if cardinality is manageable)."""
    vals = df[col].dropna().unique().tolist()
    return [str(v) for v in vals[:max_cats]]


def _render_dynamic_form(df, model_pack):
    """
    Render What-If input widgets dynamically based on what columns exist in df.
    Returns a dict of user inputs.
    """
    cat_cols = model_pack["categorical_cols"]
    num_cols_trained = model_pack["numeric_cols"]
    has_total_charges = model_pack.get("has_total_charges", False)

    # Reconstruct the full numeric list (include TotalCharges if trained)
    num_cols_full = list(num_cols_trained)
    if has_total_charges:
        num_cols_full.append('TotalCharges')

    user_inputs = {}

    # Split widgets across two columns
    cat_items = [(c, _TELCO_CATEGORICAL_WIDGETS.get(c)) for c in cat_cols]
    num_items = [(c, _TELCO_NUMERIC_WIDGETS.get(c)) for c in num_cols_full]

    all_items = cat_items + num_items
    mid = (len(all_items) + 1) // 2

    fcol1, fcol2 = st.columns(2)

    for i, (col, widget_def) in enumerate(all_items):
        target_col = fcol1 if i < mid else fcol2

        with target_col:
            if col in cat_cols:
                # Use Telco widget spec if available, else derive from data
                if widget_def:
                    label, options = widget_def
                else:
                    label = col
                    options = _get_col_uniques(df, col)
                    if not options:
                        options = ["Unknown"]
                user_inputs[col] = st.selectbox(label, options, key=f"churn_cat_{col}")

            else:
                # Numeric widget
                if widget_def:
                    label, mn, mx, default, step = widget_def
                    user_inputs[col] = st.slider(label, min_value=mn, max_value=mx, value=default, step=step)
                else:
                    # Derive range from data
                    col_data = df[col].dropna()
                    mn = float(col_data.min()) if len(col_data) else 0.0
                    mx = float(col_data.max()) if len(col_data) else 100.0
                    default = float(col_data.median()) if len(col_data) else (mn + mx) / 2
                    step = max(0.01, (mx - mn) / 100)
                    # Use number_input for arbitrary numeric cols (safer than slider)
                    user_inputs[col] = st.number_input(col, min_value=mn, max_value=mx,
                                                       value=default, step=step, key=f"churn_num_{col}")

    # Compute TotalCharges if it wasn't directly collected
    if has_total_charges and 'TotalCharges' not in user_inputs:
        tenure = float(user_inputs.get('tenure', 12))
        monthly = float(user_inputs.get('MonthlyCharges', 65.0))
        user_inputs['TotalCharges'] = tenure * monthly

    return user_inputs


def render_churn_predictor(df):
    """
    Renders the Machine Learning Churn Analysis and Prediction panel.
    Works with both the built-in Telco dataset and any custom uploaded CSV.
    """
    st.markdown(
        '<h1 class="platform-title" style="text-align: left; font-size: 2.2rem; margin-bottom: 5px;">'
        'Customer Churn Risk Analysis</h1>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="platform-subtitle" style="text-align: left; margin-bottom: 25px;">'
        'Predict customer churn probability and generate structured retention playbooks '
        'based on customer attributes</p>',
        unsafe_allow_html=True
    )

    # 1. Train the ML model dynamically (cached per unique dataframe hash)
    with st.spinner("Loading Churn Prediction Model..."):
        model_pack = train_churn_model(df)

    # 2. Layout columns: Left for What-if Form, Right for Predictions & Feature Importances
    col_left, col_right = st.columns([5, 4])

    # --- LEFT COLUMN: WHAT-IF SIMULATION PANEL ---
    with col_left:
        st.markdown(
            """
            <div class="glass-card" style="margin-bottom: 20px;">
                <div class="card-title">🔮 Customer Churn Risk Simulator</div>
                <p style="color:#a0a0c0; font-size:0.85rem; margin:0;">Adjust the indicators below to simulate
                a real customer profile and calculate their churn risk in real-time.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Dynamic form — adapts to whatever columns the dataset has
        user_inputs = _render_dynamic_form(df, model_pack)

        # Run live model inference
        churn_probability = predict_single_churn(model_pack, user_inputs)

    # --- RIGHT COLUMN: PREDICTION CARD & FEATURE IMPORTANCE ---
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
                <div class="card-title" style="color: {text_color}; margin-bottom: 12px;">⚡ Risk Assessment Analysis</div>
                <div class="predict-box">
                    <div class="risk-level" style="color: {text_color};">{risk_label}</div>
                    <div class="predict-percentage" style="color: {text_color};">{churn_probability*100:.1f}%</div>
                    <p style="color: #a0a0c0; font-size: 0.85rem; margin-top: 5px;">Model Accuracy: {model_pack["accuracy"]*100:.1f}%</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Actionable Support Recommendations
        recommendations = get_recommendation_plan(user_inputs, churn_probability)
        rec_html = "".join(
            [f'<div style="font-size:0.9rem; color:#e0e0ff; margin-bottom:10px; line-height:1.4;">{rec}</div>'
             for rec in recommendations]
        )
        st.markdown(
            f"""
            <div class="glass-card" style="margin-top:-10px;">
                <div class="card-title" style="margin-bottom: 12px;">💡 Actionable Intervention Playbook</div>
                {rec_html}
            </div>
            """,
            unsafe_allow_html=True
        )

    # 3. Model Feature Importances (Full Width Bottom)
    st.markdown('<div style="margin-top: 15px;"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="glass-card" style="margin-bottom: 15px;">
            <div class="card-title" style="margin-bottom: 0px;">🔍 Churn Risk Drivers (Top 8 Feature Importances)</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    feat_imp = pd.Series(model_pack["feature_importances"]).reset_index()
    feat_imp.columns = ['Feature', 'Importance']

    # Friendly name map (Telco-specific; generic columns keep their raw name)
    feat_name_map = {
        'Contract_One year':                     'Contract: 1-Year Tier',
        'Contract_Two year':                     'Contract: 2-Year Tier',
        'InternetService_Fiber optic':           'Internet: Fiber Optic Line',
        'InternetService_No':                    'No Internet Service',
        'PaymentMethod_Credit card (automatic)': 'Pay: Auto Credit Card',
        'PaymentMethod_Electronic check':        'Pay: Electronic Check',
        'PaymentMethod_Mailed check':            'Pay: Mailed Check',
        'OnlineSecurity_Yes':                    'Active Online Security',
        'TechSupport_Yes':                       'Active Tech Support',
        'PaperlessBilling_Yes':                  'Paperless Billing Activated',
        'MultipleLines_Yes':                     'Multiple Phone Lines',
        'Dependents_Yes':                        'Account has Dependents',
        'Partner_Yes':                           'Account has Partner',
        'SeniorCitizen_Yes':                     'Senior Citizen Account',
        'tenure':                                'Tenure Length (Loyalty)',
        'MonthlyCharges':                        'Monthly Subscription Cost',
        'TotalCharges_Log':                      'Total Charges (log)',
    }
    feat_imp['Feature'] = feat_imp['Feature'].map(lambda x: feat_name_map.get(x, x))
    feat_imp = feat_imp[feat_imp['Importance'] > 0].sort_values('Importance', ascending=True).tail(8)

    if feat_imp.empty:
        st.info("Feature importance not available (model trained on single-class data or too few samples).")
    else:
        fig_imp = px.bar(
            feat_imp, x='Importance', y='Feature',
            orientation='h',
            color='Importance',
            color_continuous_scale=['#00cec9', '#6c5ce7']
        )
        fig_imp.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#a0a0c0',
                       title="Feature Weight Contribution"),
            yaxis=dict(color='#e0e0ff', title=None),
            coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=10, b=10),
            height=260
        )
        st.plotly_chart(fig_imp, use_container_width=True)
