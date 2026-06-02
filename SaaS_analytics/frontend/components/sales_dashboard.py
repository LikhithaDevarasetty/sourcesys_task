# components/sales_dashboard.py
"""
Executive Sales Dashboard Component
Displays high-level SaaS financial indicators (MRR, ARR, Margin)
and generates beautifully-styled, interactive Plotly visualizations
for product sales, client industries, regional geographics, and discount impacts.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import get_saas_metrics

def render_sales_dashboard(df):
    """
    Renders the executive sales analytics workspace.
    """
    # 1. Fetch aggregate metrics
    metrics = get_saas_metrics(df)
    
    st.markdown('<h1 class="platform-title" style="text-align: left; font-size: 2.2rem; margin-bottom: 5px;">Executive Sales Analytics Workspace</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="platform-subtitle" style="text-align: left; margin-bottom: 25px;">Real-time business performance metrics updated through {metrics["latest_month"]}</p>', unsafe_allow_html=True)
    # 2. Executive KPI Cards Grid (using Streamlit columns)
    col1, col2, col3, col4 = st.columns(4)
    
    # KPI 1: Estimated MRR
    with col1:
        st.markdown(
            f"""
            <div class="glass-card glass-card-accent-violet">
                <div class="metric-label">Estimated MRR</div>
                <div class="metric-value">${metrics["mrr_estimate"]:,.2f}</div>
                <div class="metric-delta-up">▲ Active Month Sales</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    # KPI 2: Estimated ARR
    with col2:
        st.markdown(
            f"""
            <div class="glass-card glass-card-accent-teal">
                <div class="metric-label">Estimated ARR</div>
                <div class="metric-value">${metrics["arr_estimate"]:,.2f}</div>
                <div class="metric-delta-up">▲ 12x MRR projection</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    # KPI 3: Total Sales & Margin
    with col3:
        st.markdown(
            f"""
            <div class="glass-card glass-card-accent-emerald">
                <div class="metric-label">Cumulative Sales</div>
                <div class="metric-value">${metrics["total_sales"]:,.2f}</div>
                <div class="metric-delta-up" style="color:#00b894;">★ {metrics["avg_margin"]*100:.1f}% Avg Margin</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    # KPI 4: Total Customers & Volume
    with col4:
        st.markdown(
            f"""
            <div class="glass-card glass-card-accent-amber">
                <div class="metric-label">Active Clients</div>
                <div class="metric-value">{metrics["unique_customers"]:,}</div>
                <div class="metric-delta-up" style="color:#fdcb6e;">● {metrics["total_quantity"]:,} Licenses Sold</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    # 3. Main Analytics Chart Rows
    st.markdown('<div style="margin-top: 15px;"></div>', unsafe_allow_html=True)
    
    # Row 1: Time-series Monthly Growth (Full Width)
    st.markdown(
        """
        <div class="glass-card" style="margin-bottom: 15px;">
            <div class="card-title" style="margin-bottom: 0px;">📈 Monthly Growth Trends (Revenue & Net Profit)</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Group by month string for line charts
    monthly_data = df.groupby('Order_Month_Str').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    monthly_data = monthly_data.sort_values('Order_Month_Str')
    
    fig_growth = go.Figure()
    fig_growth.add_trace(go.Scatter(
        x=monthly_data['Order_Month_Str'], y=monthly_data['Sales'],
        name='Gross Sales (Revenue)', mode='lines+markers',
        line=dict(color='#6c5ce7', width=3),
        marker=dict(size=6, color='#8172ff')
    ))
    fig_growth.add_trace(go.Scatter(
        x=monthly_data['Order_Month_Str'], y=monthly_data['Profit'],
        name='Net Profit', mode='lines+markers',
        line=dict(color='#00cec9', width=3),
        marker=dict(size=6, color='#00b894')
    ))
    
    fig_growth.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#a0a0c0', title="Transaction Month"),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#a0a0c0', title="Financial Amount ($)"),
        legend=dict(font=dict(color='#e0e0ff')),
        margin=dict(l=20, r=20, t=10, b=20),
        height=320,
        hovermode="x unified"
    )
    st.plotly_chart(fig_growth, use_container_width=True)
    
    # Row 2: Product Breakdown and Industry Stacked segments (Two columns)
    st.markdown('<div style="margin-top: 15px;"></div>', unsafe_allow_html=True)
    col_left, col_right = st.columns(2)
    
    # Left Column: Product Sales (Horizontal Bar Chart)
    with col_left:
        st.markdown(
            """
            <div class="glass-card" style="margin-bottom: 15px;">
                <div class="card-title" style="margin-bottom: 0px;">📦 Product Performance Breakdown (Sales & Margin)</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        prod_data = df.groupby('Product').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
        prod_data['Margin_Pct'] = (prod_data['Profit'] / prod_data['Sales'] * 100).round(1)
        prod_data = prod_data.sort_values('Sales', ascending=True)
        
        # Color mapping based on HSL tailored colors
        fig_prod = px.bar(
            prod_data, x='Sales', y='Product',
            orientation='h',
            color='Sales',
            color_continuous_scale=['#6c5ce7', '#00cec9'],
            text='Sales'
        )
        
        fig_prod.update_traces(
            texttemplate='$%{x:,.0f}', textposition='inside',
            hovertemplate='<b>%{y}</b><br>Sales: $%{x:,.2f}<br>Profit Margin: %{customdata}%',
            customdata=prod_data['Margin_Pct']
        )
        
        fig_prod.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#a0a0c0', title="Sales Volume ($)"),
            yaxis=dict(color='#e0e0ff', title=None),
            coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=10, b=10),
            height=300
        )
        st.plotly_chart(fig_prod, use_container_width=True)
        
    # Right Column: Stacked segments by Client Industry
    with col_right:
        st.markdown(
            """
            <div class="glass-card" style="margin-bottom: 15px;">
                <div class="card-title" style="margin-bottom: 0px;">💼 Sales Contribution by Industry & Segment</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        ind_seg = df.groupby(['Industry', 'Segment'])['Sales'].sum().reset_index()
        
        # Custom premium color scheme
        color_discrete_map = {
            'SMB': '#00cec9',
            'Strategic': '#fdcb6e',
            'Enterprise': '#6c5ce7'
        }
        
        fig_ind = px.bar(
            ind_seg, x='Industry', y='Sales',
            color='Segment',
            color_discrete_map=color_discrete_map,
            category_orders={"Segment": ["SMB", "Strategic", "Enterprise"]}
        )
        
        fig_ind.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, color='#a0a0c0', title=None),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#a0a0c0', title="Sales Amount ($)"),
            legend=dict(font=dict(color='#e0e0ff'), title=None, orientation="h", y=1.1, x=0),
            margin=dict(l=10, r=10, t=10, b=10),
            height=300,
            barmode='stack'
        )
        st.plotly_chart(fig_ind, use_container_width=True)

    # Row 3: Geographic Distribution and Discount Analysis
    st.markdown('<div style="margin-top: 15px;"></div>', unsafe_allow_html=True)
    col_geo, col_disc = st.columns([3, 2])
    
    # Left Geo Horizontal Bars
    with col_geo:
        st.markdown(
            """
            <div class="glass-card" style="margin-bottom: 15px;">
                <div class="card-title" style="margin-bottom: 0px;">🌍 Regional Sales Distribution (Top 10 Countries)</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        geo_data = df.groupby('Country')['Sales'].sum().reset_index()
        geo_data = geo_data.sort_values('Sales', ascending=True).tail(10)
        
        fig_geo = px.bar(
            geo_data, x='Sales', y='Country',
            orientation='h',
            color_discrete_sequence=['#8172ff']
        )
        
        fig_geo.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#a0a0c0', title="Sales Volume ($)"),
            yaxis=dict(color='#e0e0ff', title=None),
            margin=dict(l=10, r=10, t=10, b=10),
            height=280
        )
        st.plotly_chart(fig_geo, use_container_width=True)
        
    # Right Discount Impact Scatter
    with col_disc:
        st.markdown(
            """
            <div class="glass-card" style="margin-bottom: 15px;">
                <div class="card-title" style="margin-bottom: 0px;">✂️ Discount Impact on Profit Margin</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # We bucket discount levels into ranges
        disc_impact = df.groupby('Discount').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Row ID': 'count'
        }).reset_index()
        
        disc_impact['Margin_Pct'] = (disc_impact['Profit'] / disc_impact['Sales'] * 100).round(1)
        disc_impact['Discount_Pct'] = (disc_impact['Discount'] * 10).astype(int) # Standardize index representation
        
        fig_disc = px.scatter(
            disc_impact, x='Discount_Pct', y='Margin_Pct',
            size='Sales',
            color='Margin_Pct',
            color_continuous_scale=['#d63031', '#fdcb6e', '#00b894'],
            hover_name='Discount_Pct'
        )
        
        fig_disc.update_traces(
            hovertemplate='<b>Discount Rate: %{x}%</b><br>Profit Margin: %{y}%<br>Sales Volume: $%{marker.size:,.2f}'
        )
        
        fig_disc.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#a0a0c0', title="Discount Rate Offered (%)"),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#a0a0c0', title="Profit Margin (%)"),
            coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=10, b=10),
            height=280
        )
        st.plotly_chart(fig_disc, use_container_width=True)
