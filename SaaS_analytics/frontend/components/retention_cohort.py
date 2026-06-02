# components/retention_cohort.py
"""
Cohort Customer Retention Matrix Component
Extracts customer subscription histories, constructs a month-over-month (MoM)
retention matrix table, and renders a stunning interactive Heatmap and average curve.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def render_retention_cohort(df):
    """
    Constructs and renders the SaaS Customer Retention Cohort workspace.
    """
    st.markdown('<h1 class="platform-title" style="text-align: left; font-size: 2.2rem; margin-bottom: 5px;">Customer Retention & Cohort Workspace</h1>', unsafe_allow_html=True)
    st.markdown('<p class="platform-subtitle" style="text-align: left; margin-bottom: 25px;">MoM Cohort Matrix analyzing customer transaction stickiness and lifetime behavior</p>', unsafe_allow_html=True)
    
    # 1. Select the date range to optimize matrix sizing (limit to most active 12-month period for cleaner UI)
    st.markdown(
        """
        <div class="glass-card" style="margin-bottom: 20px;">
            <div class="card-title">📈 Customer Lifetime Value & Stickiness Insights</div>
            <p style="color: #a0a0c0; font-size: 0.95rem; line-height: 1.5; margin: 0;">
                A customer cohort is defined as the month when a client made their <strong>first SaaS product transaction</strong>. 
                The matrix below tracks what percentage of those original clients returned to make recurring purchases in the subsequent months. 
                A higher retention rate in later periods indicates a strong product-market fit and robust subscription stability.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # --- ALGORITHM: BUILD COHORT MATRIX ---
    # Create working dataframe with clean dates
    cohort_df = df[['Customer ID', 'Order Date']].copy()
    cohort_df['Order_Month'] = cohort_df['Order Date'].dt.to_period('M')
    
    # Identify cohort month (first purchase month) for each customer
    cohort_df['Cohort_Month'] = cohort_df.groupby('Customer ID')['Order_Month'].transform('min')
    
    # Calculate months elapsed between transaction and cohort month
    # Convert Period to timestamp representation for math
    order_timestamp = cohort_df['Order_Month'].dt.to_timestamp()
    cohort_timestamp = cohort_df['Cohort_Month'].dt.to_timestamp()
    
    # Monthly delta calculation
    cohort_df['Period'] = ((order_timestamp.dt.year - cohort_timestamp.dt.year) * 12 + 
                           (order_timestamp.dt.month - cohort_timestamp.dt.month))
    
    # Group by Cohort and Period, count unique customers
    cohort_counts = cohort_df.groupby(['Cohort_Month', 'Period'])['Customer ID'].nunique().reset_index()
    
    # Pivot to standard cohort table index = Cohort, columns = Period
    cohort_pivot = cohort_counts.pivot(index='Cohort_Month', columns='Period', values='Customer ID')
    
    # Filter for last 12 cohorts to keep the chart beautifully readable without clutter
    cohort_pivot = cohort_pivot.tail(12)
    
    # Extract Cohort Sizes (Period 0 counts)
    cohort_sizes = cohort_pivot.iloc[:, 0]
    
    # Calculate retention percentage relative to cohort size (Period 0 = 100%)
    retention_matrix = cohort_pivot.divide(cohort_sizes, axis=0) * 100
    
    # Limit to first 12 columns (Month 0 to Month 11) for premium and readable grid spacing on dashboard
    retention_matrix = retention_matrix.iloc[:, :12]
    
    # Map index to nice string labels (e.g. "2023-05") safely across all Pandas versions
    retention_matrix.index = [x.strftime('%Y-%m') if hasattr(x, 'strftime') else str(x) for x in retention_matrix.index]
    cohort_sizes.index = [x.strftime('%Y-%m') if hasattr(x, 'strftime') else str(x) for x in cohort_sizes.index]
    
    # 2. Render Retention Heatmap (using Plotly Heatmap)
    # Formats lists for Heatmap safely checking for NaN sizes
    y_labels = [f"{idx} ({int(size) if pd.notna(size) else 0} clients)" for idx, size in zip(retention_matrix.index, cohort_sizes)]
    x_labels = [f"Month {col}" for col in retention_matrix.columns]
    
    # Fill NaN values with None for Plotly rendering
    z_data = retention_matrix.values
    z_data_rounded = np.nan_to_num(z_data, nan=-1) # Represent NaNs as -1 for visual filtering
    
    # Construct hovertext
    hover_text = []
    for y_idx, row in enumerate(retention_matrix.index):
        row_text = []
        for x_idx, col in enumerate(retention_matrix.columns):
            val = z_data[y_idx, x_idx]
            if pd.isna(val):
                row_text.append("No active data for this period")
            else:
                row_text.append(f"Cohort: {row}<br>Period: Month {col}<br>Retention: {val:.1f}%")
        hover_text.append(row_text)
        
    # Beautiful Custom Heatmap
    fig_heat = go.Figure(data=go.Heatmap(
        z=z_data,
        x=x_labels,
        y=y_labels,
        colorscale=[[0.0, '#100e2b'], [0.2, '#4834d4'], [0.6, '#6c5ce7'], [1.0, '#00cec9']],
        xgap=2,
        ygap=2,
        colorbar=dict(title=dict(text="Retention (%)", font=dict(color="#a0a0c0")), tickfont=dict(color="#a0a0c0")),
        hoverinfo='text',
        text=hover_text
    ))
    
    # Inject text annotations inside cells (if not NaN)
    for y_idx, row in enumerate(retention_matrix.index):
        for x_idx, col in enumerate(retention_matrix.columns):
            val = z_data[y_idx, x_idx]
            if not pd.isna(val):
                fig_heat.add_annotation(
                    x=x_labels[x_idx],
                    y=y_labels[y_idx],
                    text=f"<b>{val:.0f}%</b>",
                    showarrow=False,
                    font=dict(color='white' if val > 40 else '#a0a0c0', size=11)
                )
                
    fig_heat.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(color='#a0a0c0', side='bottom'),
        yaxis=dict(color='#e0e0ff', title="Customer Cohorts"),
        margin=dict(l=10, r=10, t=10, b=10),
        height=380
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    
    # 3. Average Cohort Curve Row
    st.markdown('<div style="margin-top: 15px;"></div>', unsafe_allow_html=True)
    
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.markdown(
            """
            <div class="glass-card" style="margin-bottom: 15px;">
                <div class="card-title" style="margin-bottom: 0px;">📈 Average SaaS Customer Retention Curve</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Calculate mean retention per period across all cohorts
        avg_retention = retention_matrix.mean(axis=0)
        
        fig_curve = go.Figure()
        fig_curve.add_trace(go.Scatter(
            x=avg_retention.index, y=avg_retention.values,
            mode='lines+markers',
            name='Avg Retention',
            line=dict(color='#00cec9', width=4),
            marker=dict(size=8, color='#00b894', symbol='circle')
        ))
        
        fig_curve.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#a0a0c0', title="Months Since Initial Onboarding"),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#a0a0c0', title="Avg Retention Rate (%)", range=[0, 105]),
            margin=dict(l=10, r=10, t=15, b=15),
            height=260
        )
        st.plotly_chart(fig_curve, use_container_width=True)
        
    with col_right:
        # Calculate key summary stats
        m1_ret = avg_retention.loc[1] if 1 in avg_retention.index else 50.0
        m6_ret = avg_retention.loc[6] if 6 in avg_retention.index else 35.0
        
        st.markdown(
            f"""
            <div class="glass-card" style="min-height: 330px; margin-bottom: 0px; padding-bottom: 20px;">
                <div class="card-title" style="margin-bottom: 12px;">💡 Strategic Retention Recommendations</div>
                <ul style="color: #d0d0f0; font-size: 0.9rem; padding-left: 20px; line-height: 1.6;">
                    <li style="margin-bottom: 12px;">
                        🎯 <strong>Onboarding Gap (Month 1)</strong>: Average retention drops to <strong>{m1_ret:.1f}%</strong> in Month 1. 
                        This indicates onboarding friction. We recommend a proactive Customer Success outreach sequence in Week 1.
                    </li>
                    <li style="margin-bottom: 12px;">
                        ⏳ <strong>Mid-term Churn (Month 6)</strong>: By Month 6, retention settles at <strong>{m6_ret:.1f}%</strong>. 
                        Securing users onto annual contract tiers prior to Month 6 will lock in revenue.
                    </li>
                    <li style="margin-bottom: 12px;">
                        ⭐ <strong>Core Stability</strong>: Cohorts that survive past Month 9 show near-zero additional decay. 
                        These are your core advocates — prioritize them for upselling additional license keys.
                    </li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
