# components/sales_dashboard.py
"""
Executive Sales Dashboard Component — fully hardened.
Renders gracefully whether or not every expected column exists.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import get_saas_metrics


def _safe_col(df, col, default=0):
    """Return df[col] if it exists, else a Series of defaults."""
    if col in df.columns:
        return df[col]
    return pd.Series([default] * len(df), index=df.index)


def render_sales_dashboard(df):
    """Renders the executive sales analytics workspace."""

    # Guard: empty dataframe
    if df is None or len(df) == 0:
        st.warning("⚠️ The dataset is empty. Please upload a valid CSV.")
        return

    # Ensure required derived columns exist ─────────────────────────────────
    try:
        if 'Order Date' in df.columns and 'Order_Month_Str' not in df.columns:
            df = df.copy()
            df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
            df = df.dropna(subset=['Order Date'])
            df['Order_Month_Str'] = df['Order Date'].dt.strftime('%Y-%m')
        if 'Sales' not in df.columns:
            df = df.copy()
            df['Sales'] = 0.0
        if 'Profit' not in df.columns:
            df = df.copy()
            df['Profit'] = df['Sales'] * 0.15
        if 'Quantity' not in df.columns:
            df = df.copy()
            df['Quantity'] = 1
        if 'Customer ID' not in df.columns:
            df = df.copy()
            df['Customer ID'] = range(len(df))
    except Exception as e:
        st.error(f"Error preparing dataset: {e}")
        return

    # ── Metrics ──────────────────────────────────────────────────────────────
    try:
        metrics = get_saas_metrics(df)
    except Exception as e:
        st.error(f"Could not compute metrics: {e}")
        return

    st.markdown(
        '<h1 class="platform-title" style="text-align:left;font-size:2.2rem;margin-bottom:5px;">'
        'Executive Sales Analytics Workspace</h1>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<p class="platform-subtitle" style="text-align:left;margin-bottom:25px;">'
        f'Real-time business performance metrics updated through {metrics.get("latest_month","N/A")}</p>',
        unsafe_allow_html=True
    )

    # ── KPI Cards ────────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    kpis = [
        (col1, "glass-card-accent-violet",  "Estimated MRR",   f'${metrics.get("mrr_estimate",0):,.2f}',  "▲ Active Month Sales"),
        (col2, "glass-card-accent-teal",    "Estimated ARR",   f'${metrics.get("arr_estimate",0):,.2f}',  "▲ 12x MRR projection"),
        (col3, "glass-card-accent-emerald", "Cumulative Sales", f'${metrics.get("total_sales",0):,.2f}',  f'★ {metrics.get("avg_margin",0)*100:.1f}% Avg Margin'),
        (col4, "glass-card-accent-amber",   "Active Clients",  f'{metrics.get("unique_customers",0):,}',  f'● {metrics.get("total_quantity",0):,} Units Sold'),
    ]
    for col, cls, label, value, delta in kpis:
        with col:
            st.markdown(
                f'<div class="glass-card {cls}">'
                f'<div class="metric-label">{label}</div>'
                f'<div class="metric-value">{value}</div>'
                f'<div class="metric-delta-up">{delta}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown('<div style="margin-top:15px;"></div>', unsafe_allow_html=True)

    # ── Monthly Growth Chart ──────────────────────────────────────────────────
    try:
        if 'Order_Month_Str' in df.columns:
            st.markdown(
                '<div class="glass-card" style="margin-bottom:15px;">'
                '<div class="card-title" style="margin-bottom:0px;">📈 Monthly Growth Trends (Revenue & Net Profit)</div>'
                '</div>',
                unsafe_allow_html=True
            )
            monthly_data = (df.groupby('Order_Month_Str')
                              .agg({'Sales': 'sum', 'Profit': 'sum'})
                              .reset_index()
                              .sort_values('Order_Month_Str'))

            fig_growth = go.Figure()
            fig_growth.add_trace(go.Scatter(
                x=monthly_data['Order_Month_Str'], y=monthly_data['Sales'],
                name='Gross Sales', mode='lines+markers',
                line=dict(color='#6c5ce7', width=3), marker=dict(size=6, color='#8172ff')
            ))
            fig_growth.add_trace(go.Scatter(
                x=monthly_data['Order_Month_Str'], y=monthly_data['Profit'],
                name='Net Profit', mode='lines+markers',
                line=dict(color='#00cec9', width=3), marker=dict(size=6, color='#00b894')
            ))
            fig_growth.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)',
                           color='#a0a0c0', title="Transaction Month"),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)',
                           color='#a0a0c0', title="Financial Amount ($)"),
                legend=dict(font=dict(color='#e0e0ff')),
                margin=dict(l=20, r=20, t=10, b=20), height=320, hovermode="x unified"
            )
            st.plotly_chart(fig_growth, use_container_width=True)
    except Exception as e:
        st.info(f"Monthly growth chart unavailable: {e}")

    st.markdown('<div style="margin-top:15px;"></div>', unsafe_allow_html=True)
    col_left, col_right = st.columns(2)

    # ── Product Breakdown ────────────────────────────────────────────────────
    with col_left:
        try:
            if 'Product' in df.columns:
                st.markdown(
                    '<div class="glass-card" style="margin-bottom:15px;">'
                    '<div class="card-title" style="margin-bottom:0px;">📦 Product Performance Breakdown</div>'
                    '</div>',
                    unsafe_allow_html=True
                )
                prod_data = (df.groupby('Product')
                               .agg({'Sales': 'sum', 'Profit': 'sum'})
                               .reset_index())
                prod_data['Margin_Pct'] = (prod_data['Profit'] / prod_data['Sales'].replace(0, np.nan) * 100).round(1).fillna(0)
                prod_data = prod_data.sort_values('Sales', ascending=True)

                fig_prod = px.bar(
                    prod_data, x='Sales', y='Product', orientation='h',
                    color='Sales', color_continuous_scale=['#6c5ce7', '#00cec9'], text='Sales'
                )
                fig_prod.update_traces(
                    texttemplate='$%{x:,.0f}', textposition='inside',
                    hovertemplate='<b>%{y}</b><br>Sales: $%{x:,.2f}<br>Margin: %{customdata}%',
                    customdata=prod_data['Margin_Pct']
                )
                fig_prod.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)',
                               color='#a0a0c0', title="Sales Volume ($)"),
                    yaxis=dict(color='#e0e0ff', title=None),
                    coloraxis_showscale=False,
                    margin=dict(l=10, r=10, t=10, b=10), height=300
                )
                st.plotly_chart(fig_prod, use_container_width=True)
            else:
                st.info("No 'Product' column found — product breakdown not available.")
        except Exception as e:
            st.info(f"Product chart unavailable: {e}")

    # ── Industry/Segment Breakdown ───────────────────────────────────────────
    with col_right:
        try:
            has_industry = 'Industry' in df.columns
            has_segment  = 'Segment' in df.columns

            st.markdown(
                '<div class="glass-card" style="margin-bottom:15px;">'
                '<div class="card-title" style="margin-bottom:0px;">💼 Sales Contribution by Industry & Segment</div>'
                '</div>',
                unsafe_allow_html=True
            )

            if has_industry and has_segment:
                ind_seg = df.groupby(['Industry', 'Segment'])['Sales'].sum().reset_index()
                color_map = {'SMB': '#00cec9', 'Strategic': '#fdcb6e', 'Enterprise': '#6c5ce7'}
                fig_ind = px.bar(
                    ind_seg, x='Industry', y='Sales', color='Segment',
                    color_discrete_map=color_map,
                    category_orders={"Segment": ["SMB", "Strategic", "Enterprise"]}
                )
            elif has_industry:
                ind_data = df.groupby('Industry')['Sales'].sum().reset_index()
                fig_ind = px.bar(ind_data, x='Industry', y='Sales',
                                 color_discrete_sequence=['#6c5ce7'])
            elif has_segment:
                seg_data = df.groupby('Segment')['Sales'].sum().reset_index()
                fig_ind = px.bar(seg_data, x='Segment', y='Sales',
                                 color_discrete_sequence=['#00cec9'])
            else:
                st.info("No 'Industry' or 'Segment' column found.")
                fig_ind = None

            if fig_ind:
                fig_ind.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=False, color='#a0a0c0', title=None),
                    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)',
                               color='#a0a0c0', title="Sales Amount ($)"),
                    legend=dict(font=dict(color='#e0e0ff'), title=None,
                                orientation="h", y=1.1, x=0),
                    margin=dict(l=10, r=10, t=10, b=10), height=300, barmode='stack'
                )
                st.plotly_chart(fig_ind, use_container_width=True)
        except Exception as e:
            st.info(f"Industry chart unavailable: {e}")

    st.markdown('<div style="margin-top:15px;"></div>', unsafe_allow_html=True)
    col_geo, col_disc = st.columns([3, 2])

    # ── Geographic Distribution ──────────────────────────────────────────────
    with col_geo:
        try:
            if 'Country' in df.columns:
                st.markdown(
                    '<div class="glass-card" style="margin-bottom:15px;">'
                    '<div class="card-title" style="margin-bottom:0px;">🌍 Regional Sales Distribution (Top 10)</div>'
                    '</div>',
                    unsafe_allow_html=True
                )
                geo_data = (df.groupby('Country')['Sales'].sum()
                              .reset_index()
                              .sort_values('Sales', ascending=True)
                              .tail(10))
                fig_geo = px.bar(
                    geo_data, x='Sales', y='Country', orientation='h',
                    color_discrete_sequence=['#8172ff']
                )
                fig_geo.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)',
                               color='#a0a0c0', title="Sales Volume ($)"),
                    yaxis=dict(color='#e0e0ff', title=None),
                    margin=dict(l=10, r=10, t=10, b=10), height=280
                )
                st.plotly_chart(fig_geo, use_container_width=True)
            else:
                st.info("No 'Country' column found — geographic chart not available.")
        except Exception as e:
            st.info(f"Geographic chart unavailable: {e}")

    # ── Discount Impact ──────────────────────────────────────────────────────
    with col_disc:
        try:
            if 'Discount' in df.columns:
                st.markdown(
                    '<div class="glass-card" style="margin-bottom:15px;">'
                    '<div class="card-title" style="margin-bottom:0px;">✂️ Discount Impact on Profit Margin</div>'
                    '</div>',
                    unsafe_allow_html=True
                )
                id_col = 'Row ID' if 'Row ID' in df.columns else df.columns[0]
                disc_impact = df.groupby('Discount').agg(
                    Sales=('Sales', 'sum'),
                    Profit=('Profit', 'sum'),
                    Count=(id_col, 'count')
                ).reset_index()
                disc_impact['Margin_Pct'] = (
                    disc_impact['Profit'] / disc_impact['Sales'].replace(0, np.nan) * 100
                ).round(1).fillna(0)
                disc_impact['Discount_Pct'] = (disc_impact['Discount'] * 100).round(0).astype(int)

                fig_disc = px.scatter(
                    disc_impact, x='Discount_Pct', y='Margin_Pct', size='Sales',
                    color='Margin_Pct',
                    color_continuous_scale=['#d63031', '#fdcb6e', '#00b894'],
                    hover_name='Discount_Pct'
                )
                fig_disc.update_traces(
                    hovertemplate='<b>Discount: %{x}%</b><br>Margin: %{y}%<br>Sales: $%{marker.size:,.2f}'
                )
                fig_disc.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)',
                               color='#a0a0c0', title="Discount Rate (%)"),
                    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)',
                               color='#a0a0c0', title="Profit Margin (%)"),
                    coloraxis_showscale=False,
                    margin=dict(l=10, r=10, t=10, b=10), height=280
                )
                st.plotly_chart(fig_disc, use_container_width=True)
            else:
                st.info("No 'Discount' column found — discount analysis not available.")
        except Exception as e:
            st.info(f"Discount chart unavailable: {e}")
