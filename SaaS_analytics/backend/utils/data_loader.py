# utils/data_loader.py
import os
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAAS_SALES_PATH = os.path.join(BASE_DIR, "SaaS-Sales.csv")
CHURN_DATA_PATH = os.path.join(BASE_DIR, "WA_Fn-UseC_-Telco-Customer-Churn.csv")

@st.cache_data
def load_saas_sales_data():
    if not os.path.exists(SAAS_SALES_PATH):
        raise FileNotFoundError(f"Missing SaaS-Sales.csv")
        
    df = pd.read_csv(SAAS_SALES_PATH)
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    df = df.dropna(subset=['Order Date'])
    
    df['Order_Year'] = df['Order Date'].dt.year
    df['Order_Month'] = df['Order Date'].dt.to_period('M')
    df['Order_Month_Str'] = df['Order Date'].dt.strftime('%Y-%m')
    
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce').fillna(0)
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0).astype(int)
    df['Discount'] = pd.to_numeric(df['Discount'], errors='coerce').fillna(0)
    df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce').fillna(0)
    
    df['Profit_Margin'] = df.apply(lambda r: r['Profit'] / r['Sales'] if r['Sales'] != 0 else 0, axis=1)
    return df

@st.cache_data
def load_churn_data():
    if not os.path.exists(CHURN_DATA_PATH):
        raise FileNotFoundError(f"Missing Churn CSV")
        
    df = pd.read_csv(CHURN_DATA_PATH)
    df['TotalCharges'] = df['TotalCharges'].replace(' ', '0')
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)
    df['MonthlyCharges'] = pd.to_numeric(df['MonthlyCharges'], errors='coerce').fillna(0)
    df['SeniorCitizen'] = df['SeniorCitizen'].map({1: 'Yes', 0: 'No'})
    
    service_cols = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
    for col in service_cols:
        if col in df.columns:
            df[col] = df[col].replace('No internet service', 'No')
            
    if 'MultipleLines' in df.columns:
        df['MultipleLines'] = df['MultipleLines'].replace('No phone service', 'No')
        
    def group_tenure(t):
        if t <= 12: return '0-1 Year'
        elif t <= 24: return '1-2 Years'
        elif t <= 36: return '2-3 Years'
        elif t <= 48: return '3-4 Years'
        elif t <= 60: return '4-5 Years'
        else: return '5+ Years'
            
    df['TenureGroup'] = df['tenure'].apply(group_tenure)
    return df

def get_saas_metrics(df):
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    avg_margin = total_profit / total_sales if total_sales != 0 else 0
    total_quantity = df['Quantity'].sum()
    unique_customers = df['Customer ID'].nunique()
    
    latest_month = df['Order_Month_Str'].max()
    latest_data = df[df['Order_Month_Str'] == latest_month]
    mrr_estimate = latest_data['Sales'].sum()
    arr_estimate = mrr_estimate * 12
    
    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "avg_margin": avg_margin,
        "total_quantity": total_quantity,
        "unique_customers": unique_customers,
        "mrr_estimate": mrr_estimate,
        "arr_estimate": arr_estimate,
        "latest_month": latest_month
    }


def process_custom_sales_data(uploaded_file):
    """
    Process a user-uploaded sales CSV.
    Fills any missing standard columns with sensible defaults.
    Never raises — returns (df, absent_columns) always.
    """
    import numpy as np

    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        raise ValueError(f"Could not read CSV file: {e}")

    if df.empty:
        raise ValueError("Uploaded CSV file is empty.")

    required_sales_cols = [
        'Sales', 'Profit', 'Quantity', 'Discount',
        'Customer ID', 'Order Date', 'Product',
        'Industry', 'Segment', 'Country', 'Row ID'
    ]
    absent_columns = [col for col in required_sales_cols if col not in df.columns]

    try:
        # Row ID
        if 'Row ID' not in df.columns:
            df['Row ID'] = range(1, len(df) + 1)

        # Order Date
        if 'Order Date' not in df.columns:
            df['Order Date'] = pd.date_range(start='2024-01-01', periods=len(df), freq='h')
        else:
            df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
        df = df.dropna(subset=['Order Date'])
        if len(df) == 0:
            raise ValueError("No valid dates found in 'Order Date' column.")

        # Numeric columns
        if 'Sales' not in df.columns:
            df['Sales'] = 100.0
        else:
            df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce').fillna(0)

        if 'Profit' not in df.columns:
            df['Profit'] = df['Sales'] * 0.15
        else:
            df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce').fillna(0)

        if 'Quantity' not in df.columns:
            df['Quantity'] = 1
        else:
            df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0).astype(int)

        if 'Discount' not in df.columns:
            df['Discount'] = 0.0
        else:
            df['Discount'] = pd.to_numeric(df['Discount'], errors='coerce').fillna(0)

        # String columns
        if 'Customer ID' not in df.columns:
            df['Customer ID'] = [f"CUST-{1000 + i}" for i in range(len(df))]
        if 'Product' not in df.columns:
            df['Product'] = "Standard Subscription"
        if 'Industry' not in df.columns:
            df['Industry'] = "SaaS Analytics Clients"
        if 'Segment' not in df.columns:
            df['Segment'] = "Enterprise"
        if 'Country' not in df.columns:
            df['Country'] = "United States"

        # Derived date columns
        df['Order_Year']      = df['Order Date'].dt.year
        df['Order_Month']     = df['Order Date'].dt.to_period('M')
        df['Order_Month_Str'] = df['Order Date'].dt.strftime('%Y-%m')
        df['Profit_Margin']   = df.apply(
            lambda r: r['Profit'] / r['Sales'] if r['Sales'] != 0 else 0, axis=1
        )
    except Exception as e:
        raise ValueError(f"Error processing sales data: {e}")

    return df, absent_columns


def process_custom_churn_data(uploaded_file):
    """
    Process a user-uploaded churn CSV.
    - Only cleans / normalises columns that actually exist in the file.
    - Does NOT inject fake Telco columns — the model auto-detects available features.
    - Ensures 'Churn' target column exists (defaults to 'No' if absent).
    """
    import numpy as np

    df = pd.read_csv(uploaded_file)

    # Columns that existed in the original Telco reference set (for absent-tracking only)
    reference_cols = [
        'gender', 'SeniorCitizen', 'Partner', 'Dependents',
        'PhoneService', 'MultipleLines', 'InternetService',
        'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
        'TechSupport', 'StreamingTV', 'StreamingMovies',
        'Contract', 'PaperlessBilling', 'PaymentMethod',
        'tenure', 'MonthlyCharges', 'TotalCharges', 'Churn'
    ]
    absent_columns = [col for col in reference_cols if col not in df.columns]

    # ── Mandatory: ensure a Churn column exists ──────────────────────────────
    if 'Churn' not in df.columns:
        df['Churn'] = 'No'

    # ── Clean numeric columns only if they are present ───────────────────────
    if 'tenure' in df.columns:
        df['tenure'] = pd.to_numeric(df['tenure'], errors='coerce').fillna(12).astype(int)

    if 'MonthlyCharges' in df.columns:
        df['MonthlyCharges'] = pd.to_numeric(df['MonthlyCharges'], errors='coerce').fillna(50.0)

    if 'TotalCharges' in df.columns:
        df['TotalCharges'] = df['TotalCharges'].replace(' ', '0')
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)

    # ── Normalise SeniorCitizen encoding if column exists ────────────────────
    if 'SeniorCitizen' in df.columns:
        df['SeniorCitizen'] = df['SeniorCitizen'].map(
            {1: 'Yes', 0: 'No', '1': 'Yes', '0': 'No'}
        ).fillna(df['SeniorCitizen'])

    # ── Normalise "No internet service" / "No phone service" if cols exist ───
    service_cols = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                    'TechSupport', 'StreamingTV', 'StreamingMovies']
    for col in service_cols:
        if col in df.columns:
            df[col] = df[col].replace('No internet service', 'No')

    if 'MultipleLines' in df.columns:
        df['MultipleLines'] = df['MultipleLines'].replace('No phone service', 'No')

    # ── Add TenureGroup helper if tenure is available ─────────────────────────
    if 'tenure' in df.columns:
        def group_tenure(t):
            if t <= 12:   return '0-1 Year'
            elif t <= 24: return '1-2 Years'
            elif t <= 36: return '2-3 Years'
            elif t <= 48: return '3-4 Years'
            elif t <= 60: return '4-5 Years'
            else:         return '5+ Years'
        df['TenureGroup'] = df['tenure'].apply(group_tenure)

    return df, absent_columns
