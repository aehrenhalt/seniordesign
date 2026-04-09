"""
Annual Planning Program Dashboard — Operations Intelligence
Simplified Command Center | USA Theme
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import io

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Operations Command", page_icon="🇺🇸", layout="wide")

# ─── STYLING ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    :root { --navy: #0A1628; --navy-mid: #132040; --red: #C8102E; --silver: #C0C8D8; --white: #F0F4FF; }
    html, body, [class*="css"] { background-color: var(--navy) !important; color: var(--white) !important; font-family: sans-serif; }
    .kpi-card { background: var(--navy-mid); border-top: 3px solid var(--red); padding: 1rem; text-align: center; border-radius: 4px; }
    .kpi-value { font-size: 2rem; font-weight: bold; color: var(--white); }
    .kpi-label { font-size: 0.7rem; color: var(--silver); text-transform: uppercase; letter-spacing: 1px; }
    .section-header { font-size: 1.2rem; font-weight: bold; border-left: 4px solid var(--red); padding-left: 10px; margin: 1.5rem 0 1rem; }
</style>
""", unsafe_allow_html=True)

# ─── DATA LOADING ─────────────────────────────────────────────────────────────
VALID_COLS = [
    "major_work_type", "start_time", "employee_title", "work_center_id",
    "contractor_flag", "cluster", "employee_work_center_id", "tech_id",
    "end_time", "shift_date", "shift_length", "shift_type"
]

def get_data(uploaded):
    if uploaded:
        df = pd.read_csv(uploaded) if uploaded.name.endswith('.csv') else pd.read_excel(uploaded)
        # Filter only to requested columns
        df = df[[c for c in df.columns if c in VALID_COLS]]
        return df
    # Empty state if no upload
    return pd.DataFrame(columns=VALID_COLS)

# ─── CHARTS ───────────────────────────────────────────────────────────────────
def plot_shift_dist(df):
    counts = df['shift_type'].value_counts()
    fig = go.Figure(go.Pie(labels=counts.index, values=counts.values, hole=0.5))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
                      font=dict(color="#C0C8D8"), margin=dict(t=0, b=0, l=0, r=0))
    return fig

def plot_workload(df):
    # Grouping by work_center_id (Location)
    loc_data = df.groupby('work_center_id')['shift_length'].sum().reset_index()
    fig = go.Figure(go.Bar(x=loc_data['work_center_id'], y=loc_data['shift_length'], marker_color='#C8102E'))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#0A1628", 
                      font=dict(color="#C0C8D8"), xaxis_title="Work Center", yaxis_title="Total Hours")
    return fig

# ─── MAIN APP ─────────────────────────────────────────────────────────────────
def main():
    # Header
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; background: var(--navy-mid); padding: 1rem; border-radius: 4px;">
        <div><h2 style="margin:0;">🇺🇸 Operations Command</h2><p style="margin:0; font-size:0.8rem; color:var(--silver);">PLANNING & ANALYSIS</p></div>
        <div style="text-align:right;"><b>{datetime.now().strftime("%b %d, %Y")}</b></div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    st.sidebar.title("📁 Data Control")
    uploaded = st.sidebar.file_uploader("Upload Schedule", type=["csv", "xlsx"])
    
    df = get_data(uploaded)

    if df.empty:
        st.info("Please upload a schedule file to begin analysis.")
        return

    # KPI Row
    st.markdown('<div class="section-header">QUICK STATS</div>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{len(df)}</div><div class="kpi-label">Total Shifts</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{df["work_center_id"].nunique()}</div><div class="kpi-label">Active Work Centers</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{df["shift_length"].sum():,.0f}</div><div class="kpi-label">Total Man-Hours</div></div>', unsafe_allow_html=True)
    with k4:
        contractor_pct = (df['contractor_flag'] == 'Y').mean() * 100
        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{contractor_pct:.1f}%</div><div class="kpi-label">Contractor Mix</div></div>', unsafe_allow_html=True)

    # Tabs
    t1, t2, t3 = st.tabs(["📊 Analytics", "🗂 Raw Data", "⚙️ Export"])

    with t1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="section-header">SHIFT TYPE MIX</div>', unsafe_allow_html=True)
            st.plotly_chart(plot_shift_dist(df), use_container_width=True)
        with c2:
            st.markdown('<div class="section-header">HOURS BY WORK CENTER</div>', unsafe_allow_html=True)
            st.plotly_chart(plot_workload(df), use_container_width=True)

    with t2:
        st.markdown('<div class="section-header">DATA PREVIEW</div>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True)

    with t3:
        st.markdown('<div class="section-header">PREPARE DOWNLOAD</div>', unsafe_allow_html=True)
        towrite = io.BytesIO()
        df.to_excel(towrite, index=False, engine='xlsxwriter')
        st.download_button(label="⬇️ Download Cleaned Data (.xlsx)", 
                           data=towrite.getvalue(), 
                           file_name=f"Ops_Export_{datetime.now().strftime('%Y%m%d')}.xlsx",
                           mime="application/vnd.ms-excel")

if __name__ == "__main__":
    main()
