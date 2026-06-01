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
