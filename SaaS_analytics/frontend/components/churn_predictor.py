# components/churn_predictor.py
"""
AI Customer Churn Prediction Component
Combines machine learning analytics with interactive "What-If" sliders
to allow management to run risk simulations on any customer profile
and generates direct, actionable customer support recommendations.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.ml_model import train_churn_model, predict_single_churn, get_recommendation_plan

def render_churn_predictor(df):
    """
    Renders the Machine Learning Churn Analysis and Prediction panel.
    """
    st.markdown('<h1 class="platform-title" style="text-align: left; font-size: 2.2rem; margin-bottom: 5px;">Customer Churn Risk Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p class="platform-subtitle" style="text-align: left; margin-bottom: 25px;">Predict customer churn probability and generate structured retention playbooks based on customer attributes</p>', unsafe_allow_html=True)
    
    # 1. Train the ML model dynamically (cached)
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
                <p style="color:#a0a0c0; font-size:0.85rem; margin:0;">Adjust the indicators below to simulate a real customer profile and calculate their churn risk in real-time.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Organize form fields elegantly in nested columns
        fcol1, fcol2 = st.columns(2)
        
        with fcol1:
            tenure = st.slider("Customer Tenure (Months Active)", min_value=1, max_value=72, value=12, step=1)
            monthly_charges = st.slider("Monthly Charges ($)", min_value=18.0, max_value=120.0, value=65.0, step=0.5)
            contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
            internet = st.selectbox("Internet Service Type", ["Fiber optic", "DSL", "No"])
            tech_support = st.selectbox("Tech Support Active?", ["No", "Yes"])
            online_sec = st.selectbox("Online Security Active?", ["No", "Yes"])
            
        with fcol2:
            payment = st.selectbox("Payment Method", [
                "Electronic check", "Mailed check", 
                "Bank transfer (automatic)", "Credit card (automatic)"
            ])
            paperless = st.selectbox("Paperless Billing?", ["Yes", "No"])
            multiple_lines = st.selectbox("Multiple Phone Lines?", ["No", "Yes"])
            partner = st.selectbox("Has Partner?", ["No", "Yes"])
            dependents = st.selectbox("Has Dependents?", ["No", "Yes"])
            senior = st.selectbox("Senior Citizen?", ["No", "Yes"])
            gender = st.selectbox("Customer Gender", ["Female", "Male"])
            
        # Pack inputs into dict
        user_inputs = {
            'gender': gender,
            'SeniorCitizen': senior,
            'Partner': partner,
            'Dependents': dependents,
            'tenure': tenure,
            'PhoneService': "Yes" if multiple_lines != "No phone service" else "No",
            'MultipleLines': multiple_lines,
            'InternetService': internet,
            'OnlineSecurity': online_sec,
            'OnlineBackup': "No",       # Filled default values for omitted categoricals
            'DeviceProtection': "No",
            'TechSupport': tech_support,
            'StreamingTV': "No",
            'StreamingMovies': "No",
            'Contract': contract,
            'PaperlessBilling': paperless,
            'PaymentMethod': payment,
            'MonthlyCharges': monthly_charges,
            'TotalCharges': tenure * monthly_charges # Estimated TotalCharges
        }
        
        # Run live model inference!
        churn_probability = predict_single_churn(model_pack, user_inputs)
        
    # --- RIGHT COLUMN: PREDICTION CARD & FEATURE IMPORTANCE ---
    with col_right:
        # Glow color based on Churn probability threshold
        if churn_probability < 0.3:
            glow_class = "glass-card-accent-emerald"
            text_color = "#2ed573"
            risk_label = "Low Churn Risk"
            alert_bg = "notification-success"
        elif churn_probability < 0.6:
            glow_class = "glass-card-accent-amber"
            text_color = "#ffa502"
            risk_label = "Moderate Churn Risk"
            alert_bg = "notification-info"
        else:
            glow_class = "glass-card-accent-crimson"
            text_color = "#ff4757"
            risk_label = "HIGH CHURN RISK"
            alert_bg = "notification-banner" # Will custom style or standard fallback
            
        # Prediction Output card
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
        
        # Actionable Support Recommendations card
        recommendations = get_recommendation_plan(user_inputs, churn_probability)
        rec_html = "".join([f'<div style="font-size:0.9rem; color:#e0e0ff; margin-bottom:10px; line-height:1.4;">{rec}</div>' for rec in recommendations])
        
        st.markdown(
            f"""
            <div class="glass-card" style="margin-top:-10px;">
                <div class="card-title" style="margin-bottom: 12px;">💡 Actionable Intervention Playbook</div>
                {rec_html}
            </div>
            """,
            unsafe_allow_html=True
        )

    # 3. Model Feature Importances (Bottom Full Width)
    st.markdown('<div style="margin-top: 15px;"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="glass-card" style="margin-bottom: 15px;">
            <div class="card-title" style="margin-bottom: 0px;">🔍 Churn Risk Drivers (Top 8 Feature Importances)</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Grab features from model output pack
    feat_imp = pd.Series(model_pack["feature_importances"]).reset_index()
    feat_imp.columns = ['Feature', 'Importance']
    
    # Make names friendly for management slides
    feat_name_map = {
        'Contract_One year': 'Contract: 1-Year Tier',
        'Contract_Two year': 'Contract: 2-Year Tier',
        'InternetService_Fiber optic': 'Internet: Fiber Optic Line',
        'InternetService_No': 'No Internet Service',
        'PaymentMethod_Credit card (automatic)': 'Pay: Auto Credit Card',
        'PaymentMethod_Electronic check': 'Pay: Electronic Check',
        'PaymentMethod_Mailed check': 'Pay: Mailed Check',
        'OnlineSecurity_Yes': 'Active Online Security',
        'TechSupport_Yes': 'Active Tech Support',
        'PaperlessBilling_Yes': 'Paperless Billing Activated',
        'MultipleLines_Yes': 'Multiple Phone Lines',
        'Dependents_Yes': 'Account has Dependents',
        'Partner_Yes': 'Account has Partner',
        'SeniorCitizen_Yes': 'Senior Citizen Account',
        'tenure': 'Tenure Length (Loyalty)',
        'MonthlyCharges': 'Monthly Subscription Cost'
    }
    feat_imp['Feature'] = feat_imp['Feature'].map(lambda x: feat_name_map.get(x, x))
    feat_imp = feat_imp.sort_values('Importance', ascending=True).tail(8)
    
    fig_imp = px.bar(
        feat_imp, x='Importance', y='Feature',
        orientation='h',
        color='Importance',
        color_continuous_scale=['#00cec9', '#6c5ce7']
    )
    
    fig_imp.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#a0a0c0', title="Feature Weight Contribution"),
        yaxis=dict(color='#e0e0ff', title=None),
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=10, b=10),
        height=260
    )
    st.plotly_chart(fig_imp, use_container_width=True)
