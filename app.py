"""
Annual Planning Program Program Dash — Operations Intelligence Dashboard
Python / Streamlit  |  USA Theme (Navy & Red)
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import json, os, io

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="American Airlines Command",
    page_icon="🇺🇸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Source+Sans+3:wght@300;400;600&display=swap');

:root {
    --navy:      #0A1628;
    --navy-mid:  #132040;
    --navy-light:#1E3060;
    --red:        #C8102E;
    --red-light: #E8193A;
    --silver:    #C0C8D8;
    --white:     #F0F4FF;
    --gold:      #D4AF37;
}

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
    background-color: var(--navy) !important;
    color: var(--white) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

.block-container {
    padding: 1.5rem 2rem 2rem !important;
    max-width: 1400px !important;
}

.ops-header {
    background: linear-gradient(135deg, var(--navy-mid) 0%, var(--navy-light) 100%);
    border-left: 5px solid var(--red);
    border-radius: 4px;
    padding: 1.1rem 1.5rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.ops-header-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.2rem;
    letter-spacing: 3px;
    color: var(--white);
    text-shadow: 0 0 20px rgba(200,16,46,0.4);
}
.ops-header-badge {
    background: var(--red);
    color: white;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 2px;
    padding: 4px 12px;
    border-radius: 2px;
    text-transform: uppercase;
}

[data-testid="stSidebar"] {
    background: var(--navy-mid) !important;
    border-right: 2px solid rgba(200,16,46,0.3);
}
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--white) !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
    font-family: 'Bebas Neue', sans-serif;
    letter-spacing: 2px;
    color: var(--silver) !important;
    font-size: 1.1rem;
    border-bottom: 1px solid rgba(200,16,46,0.4);
    padding-bottom: 6px;
    margin-bottom: 10px;
}

.kpi-card {
    background: var(--navy-mid);
    border: 1px solid rgba(200,16,46,0.25);
    border-top: 3px solid var(--red);
    border-radius: 4px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.kpi-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.4rem;
    letter-spacing: 2px;
    color: var(--white);
    line-height: 1;
}
.kpi-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    color: var(--silver);
    text-transform: uppercase;
    margin-top: 4px;
}
.kpi-delta-good { color: #4CAF50; font-size: 0.75rem; margin-top: 3px; }
.kpi-delta-warn { color: var(--red); font-size: 0.75rem; margin-top: 3px; }

.section-header {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.3rem;
    letter-spacing: 2px;
    color: var(--white);
    border-left: 4px solid var(--red);
    padding-left: 10px;
    margin: 1.5rem 0 1rem 0;
}

[data-testid="stFileUploader"] {
    background: var(--navy-light) !important;
    border: 2px dashed rgba(200,16,46,0.4) !important;
    border-radius: 4px !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: var(--navy-mid) !important;
    border-bottom: 2px solid rgba(200,16,46,0.3) !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Source Sans 3', sans-serif !important;
    font-weight: 600 !important;
    color: var(--silver) !important;
}
.stTabs [aria-selected="true"] {
    color: var(--white) !important;
    border-bottom: 3px solid var(--red) !important;
}
.stButton > button {
    background: var(--red) !important;
    color: white !important;
    border: none !important;
    border-radius: 3px !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
}
.stButton > button:hover { background: var(--red-light) !important; 
}
/* ── Targets the 'Upload' text inside the uploader ── */
[data-testid="stFileUploader"] section div div {
    color: #C0C8D8 !important;
}

/* ── Targets the '200MB per file' subtext ── */
[data-testid="stFileUploader"] small {
    color: #C0C8D8 !important;
    opacity: 0.8;
}

/* ── Targets the Radio button labels (Operations/Scheduling View) ── */
div[data-testid="stSidebar"] .stRadio label p {
    color: #C0C8D8 !important;
    font-size: 0.95rem !important;
    font-weight: 400 !important;
}

</style>
""", unsafe_allow_html=True)

# ─── DATA LAYER ───────────────────────────────────────────────────────────────

SAMPLE_DATA = {
    "major_work_type": ["Line", "Base", "Line", "AOG", "Shop"] * 3,
    "start_time": ["06:00", "07:00", "14:00", "06:00", "22:00"] * 3,
    "end_time": ["14:00", "15:00", "22:00", "10:00", "06:00"] * 3,
    "employee_title": ["Tech", "Lead", "Tech", "Tech", "Supervisor"] * 3,
    "work_center_id": ["D01", "M02", "D01", "A03", "S04"] * 3,
    "contractor_flag": ["N", "N", "N", "Y", "N"] * 3,
    "cluster": ["Flagship", "Core", "Flagship", "Transit", "Core"] * 3,
    "employee_work_center_id": ["ATL", "DFW", "ATL", "ORD", "CLT"] * 3,
    "tech_id": [f"ID-{i}" for i in range(1, 16)],
    "shift_date": ["2026-04-07"] * 7 + ["2026-04-08"] * 8,
    "shift_length": [8.0, 8.0, 7.5, 4.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0],
    "shift_type": ["Regular", "Regular", "Regular", "OT", "Regular", "Regular", "Relief", "Regular",
                  "Regular", "Regular", "Regular", "OT", "Regular", "Relief", "Regular"]
}

ASSUMPTIONS = [
    ("Regular hourly rate", "$25.00"),
    ("OT multiplier", "1.5×"),
    ("Relief premium", "+30%"),
]

def get_df(uploaded=None):
    if uploaded is not None:
        try:
            if uploaded.name.endswith(".csv"): df = pd.read_csv(uploaded)
            else: df = pd.read_excel(uploaded)
            df.columns = [c.lower().replace(" ", "_").strip() for c in df.columns]
            return df
        except Exception as e:
            st.error(f"Could not parse file: {e}")
    return pd.DataFrame(SAMPLE_DATA)

# ─── DERIVED STATS ────────────────────────────────────────────────────────────

def derive(df):
    required_cols = [
        "major_work_type", "start_time", "employee_title", "work_center_id",
        "contractor_flag", "cluster", "employee_work_center_id", "tech_id",
        "end_time", "shift_date", "shift_length", "shift_type"
    ]
    
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        st.error(f"🚨 Missing required columns: `{', '.join(missing)}`.")
        st.stop()

    rate_str = st.session_state.get("assume_vals", {}).get("Regular hourly rate", "$25.00")
    rate = float(rate_str.replace("$", ""))
    
    df["labor_cost"] = df["shift_length"] * rate
    df.loc[df["shift_type"] == "OT", "labor_cost"] *= 1.5

    total = len(df)
    total_cost = df["labor_cost"].sum()
    avg_cost = round(total_cost / total) if total > 0 else 0
    ot_cost = df[df["shift_type"] == "OT"]["labor_cost"].sum()
    ot_pct = round((ot_cost / total_cost) * 100, 1) if total_cost > 0 else 0

    return dict(
        total=total, 
        total_cost=total_cost, 
        avg_cost=avg_cost,
        ot_pct=ot_pct, 
        total_hc=df["tech_id"].nunique()
    )

# ─── UI COMPONENTS ────────────────────────────────────────────────────────────

def section_header(title):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)

def kpi_row(stats):
    cols = st.columns(4)
    items = [
        ("Total Shifts", str(stats["total"]), "Scheduled Cycle", "good"),
        ("Estimated Cost", f"${stats['total_cost']:,.0f}", f"Avg ${stats['avg_cost']}/shift", "info"),
        ("Active Techs", str(stats["total_hc"]), "Unique IDs Found", "good"),
        ("OT Utilization", f"{stats['ot_pct']}%", "Total Cost Share", "warn" if stats['ot_pct'] > 15 else "good"),
    ]
    for col, (label, val, sub, mood) in zip(cols, items):
        delta_class = "kpi-delta-good" if mood == "good" else ("kpi-delta-warn" if mood == "warn" else "kpi-label")
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value">{val}</div>
                <div class="kpi-label">{label}</div>
                <div class="{delta_class}">{sub}</div>
            </div>""", unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────────────────────────────────

def tab_overview(df, stats):
    """Overview tab with KPIs only (Visualizations removed)"""
    kpi_row(stats)
    st.markdown("---")
    st.info("Upload a new schedule in the sidebar to refresh operational metrics.")

def main():
    st.markdown("""
    <div class="ops-header">
        <div>
            <span class="ops-header-title">🇺🇸 Annual Planning Program Command</span>
            <div style="font-size:.75rem;color:#C0C8D8;letter-spacing:1.5px;margin-top:2px">OPERATIONS INTELLIGENCE</div>
        </div>
        <div style="text-align:right">
            <div class="ops-header-badge">Operations View</div>
            <div style="font-size:.7rem;color:#C0C8D8;margin-top:4px">""" + datetime.now().strftime("%b %d, %Y %H:%M") + """</div>
        </div>
    </div>""", unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### 📁 UPLOAD")
        uploaded = st.file_uploader("Drag file here", type=["csv","xlsx"], label_visibility="collapsed")
        st.markdown("---")
        st.radio("VIEW MODE", ["Operations View","Scheduling View"], label_visibility="collapsed")

    df = get_df(uploaded)
    
    # Initialize assumptions in session state if missing
    if "assume_vals" not in st.session_state:
        st.session_state.assume_vals = {k: v for k, v in ASSUMPTIONS}
        
    stats = derive(df)

    tabs = st.tabs(["📋 Overview", "📊 Breakdown", "👥 Headcount", "💰 Cost Analysis", "🔬 Sensitivity", "🗂 Raw Data", "⚙️ Assumptions", "💬 Comm Hub"])

    with tabs[0]: 
        tab_overview(df, stats)
    
    with tabs[1]: 
        section_header("WORK TYPE KPI BREAKDOWN")
        st.caption("Detailed breakdown content removed.")
    
    with tabs[2]: 
        section_header("HEADCOUNT BY STATION")
        st.caption("Station headcount content removed.")
        
    with tabs[3]: 
        section_header("LABOR COST ANALYSIS")
        st.caption("Labor cost analysis content removed.")
        
    with tabs[4]: 
        section_header("SENSITIVITY ANALYSIS")
        st.caption("Sensitivity analysis content removed.")
        
    with tabs[5]: 
        section_header("RAW DATA EXPLORER")
        st.caption("Raw data content removed.")
        
    with tabs[6]: 
        section_header("SYSTEM ASSUMPTIONS")
        st.caption("Assumptions configuration removed.")
        
    with tabs[7]: 
        section_header("COMMUNICATION HUB")
        st.caption("Communication hub content removed.")

if __name__ == "__main__":
    main()
