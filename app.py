"""
Annual Planning Program Program Dash — Operations Intelligence Dashboard
Python / Streamlit  |  USA Theme (Navy & Red)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
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

/* ── Root palette ── */
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

/* ── Global resets ── */
html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
    background-color: var(--navy) !important;
    color: var(--white) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── App container ── */
.block-container {
    padding: 1.5rem 2rem 2rem !important;
    max-width: 1400px !important;
}

/* ── Top header bar ── */
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

/* ── Sidebar ── */
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

/* ── KPI metric cards ── */
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

/* ── Section headers ── */
.section-header {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.3rem;
    letter-spacing: 2px;
    color: var(--white);
    border-left: 4px solid var(--red);
    padding-left: 10px;
    margin: 1.5rem 0 1rem 0;
}

/* ── Cards / panels ── */
.panel {
    background: var(--navy-mid);
    border: 1px solid rgba(192,200,216,0.12);
    border-radius: 4px;
    padding: 1.2rem;
    margin-bottom: 1rem;
}
.panel-title {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    color: var(--silver);
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}

/* ── Status badges ── */
.badge {
    display: inline-block;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 2px 8px;
    border-radius: 2px;
    text-transform: uppercase;
}
.badge-green  { background: rgba(76,175,80,0.2);  color: #81C784; border: 1px solid #4CAF50; }
.badge-red    { background: rgba(200,16,46,0.2);   color: #EF9A9A; border: 1px solid var(--red); }
.badge-amber  { background: rgba(255,193,7,0.15);  color: #FFD54F; border: 1px solid #FFC107; }
.badge-blue   { background: rgba(30,48,96,0.6);    color: #90CAF9; border: 1px solid #1565C0; }
.badge-gray   { background: rgba(192,200,216,0.1); color: var(--silver); border: 1px solid rgba(192,200,216,0.3); }

/* ── Log / list rows ── */
.log-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 0;
    border-bottom: 1px solid rgba(192,200,216,0.08);
    font-size: 0.88rem;
}
.log-row:last-child { border-bottom: none; }
.log-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }

/* ── Issue / feature items ── */
.issue-item {
    background: var(--navy-light);
    border: 1px solid rgba(192,200,216,0.1);
    border-radius: 3px;
    padding: 10px 12px;
    margin-bottom: 8px;
}
.issue-title { font-weight: 600; font-size: 0.9rem; color: var(--white); }
.issue-meta  { font-size: 0.75rem; color: var(--silver); margin-top: 3px; }

/* ── File upload zone ── */
[data-testid="stFileUploader"] {
    background: var(--navy-light) !important;
    border: 2px dashed rgba(200,16,46,0.4) !important;
    border-radius: 4px !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--red) !important;
}

/* ── Streamlit widgets ── */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: var(--navy-light) !important;
    color: var(--white) !important;
    border: 1px solid rgba(192,200,216,0.2) !important;
    border-radius: 3px !important;
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
.stButton > button:hover { background: var(--red-light) !important; }

/* ── Tab bar ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--navy-mid) !important;
    border-bottom: 2px solid rgba(200,16,46,0.3) !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Source Sans 3', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    color: var(--silver) !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    color: var(--white) !important;
    border-bottom: 3px solid var(--red) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: transparent !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    background: var(--navy-mid) !important;
}
iframe { background: var(--navy-mid) !important; }

/* ── Plotly chart bg ── */
.js-plotly-plot { border-radius: 4px; }

/* ── Divider ── */
hr { border-color: rgba(200,16,46,0.2) !important; }

/* ── Form labels ── */
.stTextInput label, .stTextArea label, .stSelectbox label,
.stRadio label, [data-testid="stMarkdownContainer"] p {
    color: var(--silver) !important;
    font-size: 0.85rem !important;
}

/* ── Success box ── */
.success-box {
    background: rgba(76,175,80,0.1);
    border: 1px solid #4CAF50;
    border-radius: 4px;
    padding: 10px 14px;
    font-size: 0.88rem;
    color: #81C784;
    margin: 8px 0;
}

/* ── Metric row ── */
.metric-stripe {
    display: flex; gap: 12px; margin-bottom: 1rem;
}

/* ── Assume table ── */
.assume-row {
    display: grid; grid-template-columns: 200px 1fr;
    border-bottom: 1px solid rgba(192,200,216,0.08);
    padding: 8px 0;
    font-size: 0.88rem;
}
.assume-key { color: var(--silver); }
.assume-val { color: var(--white); font-weight: 600; }

/* ── Stars / rank ── */
.rank-badge {
    width: 24px; height: 24px;
    background: var(--red);
    color: white;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 700;
    flex-shrink: 0;
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

SUCCESS_LOG = [
    {"name":"schedule_apr07_v3.csv","date":"Apr 7, 2026","score":98,"kpis":"All 6 KPIs met","status":"green"},
    {"name":"schedule_apr06_v2.csv","date":"Apr 6, 2026","score":95,"kpis":"5 / 6 KPIs met","status":"amber"},
]

ISSUES_FILE = "/tmp/AAP_issues.json"
FEATURES_FILE = "/tmp/AAP_features.json"

DEFAULT_ISSUES = [{"id":1,"title":"OT threshold exceeded — ATL","priority":"High","status":"Open","desc":"Excessive OT logic.","reporter":"Ops","date":"Apr 6"}]
DEFAULT_FEATURES = [{"rank":1,"name":"Real-time feed","meta":"High · Apr 1","status":"Planned"}]

ASSUMPTIONS = [
    ("Regular hourly rate", "$25.00"),
    ("OT multiplier", "1.5×"),
    ("Relief premium", "+30%"),
]

def load_json(path, default):
    if os.path.exists(path):
        with open(path) as f: return json.load(f)
    return default

def save_json(path, data):
    with open(path, "w") as f: json.dump(data, f)

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
    # Required columns based on user list
    required_cols = [
        "major_work_type", "start_time", "employee_title", "work_center_id",
        "contractor_flag", "cluster", "employee_work_center_id", "tech_id",
        "end_time", "shift_date", "shift_length", "shift_type"
    ]
    
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        st.error(f"🚨 Missing required columns: `{', '.join(missing)}`.")
        st.stop()

    # Calculate labor cost from shift_length and assumptions
    rate_str = st.session_state.get("assume_vals", {}).get("Regular hourly rate", "$25.00")
    rate = float(rate_str.replace("$", ""))
    
    # Simple Cost logic for the dashboard visualization
    df["labor_cost"] = df["shift_length"] * rate
    # Apply OT premium to OT shift types
    df.loc[df["shift_type"] == "OT", "labor_cost"] *= 1.5

    total = len(df)
    total_cost = df["labor_cost"].sum()
    
    # Derive HC by counting unique tech_id per location/date
    hc_summary = df.groupby(["employee_work_center_id", "shift_date", "shift_type"])["tech_id"].nunique().reset_index()
    hc_summary.columns = ["location", "date", "type", "actual_hc"]
    
    # Categorical metadata
    locs = df["employee_work_center_id"].unique().tolist()
    clusters = df["cluster"].unique().tolist()
    
    avg_cost = round(total_cost / total) if total > 0 else 0
    ot_cost = df[df["shift_type"] == "OT"]["labor_cost"].sum()
    ot_pct = round((ot_cost / total_cost) * 100, 1) if total_cost > 0 else 0

    return dict(
        total=total, 
        total_cost=total_cost, 
        avg_cost=avg_cost,
        ot_pct=ot_pct, 
        locs=locs, 
        clusters=clusters,
        total_hc=df["tech_id"].nunique()
    )

# ─── CHART HELPERS ────────────────────────────────────────────────────────────

PLOTLY_LAYOUT = dict(
    paper_bgcolor="#132040",
    plot_bgcolor="#0A1628",
    font=dict(color="#C0C8D8", family="Source Sans 3"),
    margin=dict(l=20, r=20, t=30, b=20),
    showlegend=True,
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    xaxis=dict(gridcolor="rgba(192,200,216,0.08)", linecolor="rgba(192,200,216,0.15)"),
    yaxis=dict(gridcolor="rgba(192,200,216,0.08)", linecolor="rgba(192,200,216,0.15)"),
)

def chart_heatmap(df):
    days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    locs = df["employee_work_center_id"].unique().tolist()
    rng = np.random.default_rng(42)
    z = [[int(3 + rng.integers(0, 7)) for _ in days] for _ in locs]
    fig = go.Figure(go.Heatmap(
        z=z, x=days, y=locs,
        colorscale=[[0,"#132040"],[0.5,"#1E3060"],[1,"#C8102E"]],
        showscale=True, colorbar=dict(tickfont=dict(color="#C0C8D8"), thickness=10),
    ))
    fig.update_layout(**PLOTLY_LAYOUT, title="")
    return fig

def chart_shift_type_donut(df):
    types = df["shift_type"].value_counts()
    fig = go.Figure(go.Pie(
        labels=types.index, values=types.values, hole=0.55,
        marker_colors=["#4472C4","#C8102E","#D4AF37"], textfont_color="white",
    ))
    fig.update_layout(**PLOTLY_LAYOUT, showlegend=True, legend=dict(orientation="v"))
    return fig

def chart_cost_breakdown(df):
    cl = df.groupby("cluster")["labor_cost"].sum().reset_index()
    fig = go.Figure(go.Bar(
        x=cl["cluster"], y=cl["labor_cost"], marker_color="#C8102E",
        text=[f"${v:,.0f}" for v in cl["labor_cost"]], textposition="auto",
    ))
    fig.update_layout(**PLOTLY_LAYOUT, title="")
    return fig

def chart_sensitivity(rate=25.0, df=None):
    hc_range = list(range(-20, 25, 5))
    base_cost = df["labor_cost"].sum()
    costs = [round(base_cost * (1 + d/100)) for d in hc_range]
    fig = go.Figure(go.Bar(x=[f"{d:+}%" for d in hc_range], y=costs, marker_color="#1E3060"))
    fig.update_layout(**PLOTLY_LAYOUT, yaxis=dict(title="Projected Cost ($)"))
    return fig

# ─── UI COMPONENTS ────────────────────────────────────────────────────────────

def section_header(title):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)

def kpi_row(stats, df):
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
    kpi_row(stats, df)
    c1, c2 = st.columns([3, 2])
    with c1:
        section_header("ESTIMATED COST BY CLUSTER")
        st.plotly_chart(chart_cost_breakdown(df), use_container_width=True)
    with c2:
        section_header("SHIFT TYPE MIX")
        st.plotly_chart(chart_shift_type_donut(df), use_container_width=True)
    section_header("STAFFING HEATMAP — STATION × DAY")
    st.plotly_chart(chart_heatmap(df), use_container_width=True)

def tab_breakdown(df, stats):
    section_header("WORK TYPE KPI BREAKDOWN")
    wt = df.groupby("major_work_type").agg(count=("tech_id","count"), cost=("labor_cost","sum")).reset_index()
    cols = st.columns(len(wt))
    for col, row in zip(cols, wt.itertuples()):
        col.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{row.count}</div>
            <div class="kpi-label">{row.major_work_type} Shifts</div>
            <div class="kpi-delta-good">${row.cost:,.0f} Total Est.</div>
        </div>""", unsafe_allow_html=True)

def tab_headcount(df, stats):
    section_header("HEADCOUNT BY STATION (EMPLOYEE WORK CENTER ID)")
    loc_tbl = df.groupby("employee_work_center_id").agg(
        cluster=("cluster","first"),
        unique_techs=("tech_id","nunique"),
        total_hours=("shift_length","sum")
    ).reset_index()
    st.dataframe(loc_tbl, use_container_width=True, hide_index=True)

def tab_cost(df, stats):
    section_header("DETAILED COST LOG")
    detail = df[["tech_id","employee_work_center_id","shift_date","shift_type","shift_length","labor_cost"]].copy()
    detail.columns = ["Tech ID","Station","Date","Type","Hours","Est Cost ($)"]
    st.dataframe(detail.sort_values("Est Cost ($)", ascending=False), use_container_width=True, hide_index=True)

def tab_sensitivity(df, stats):
    section_header("COST SENSITIVITY — HEADCOUNT SCALING")
    st.plotly_chart(chart_sensitivity(df=df), use_container_width=True)

def tab_rawdata(df):
    section_header(f"RAW DATA — {len(df)} RECORDS")
    search = st.text_input("🔍 Filter by Station or Tech ID", "")
    filtered = df
    if search:
        filtered = df[df["employee_work_center_id"].str.contains(search, case=False) | df["tech_id"].str.contains(search, case=False)]
    st.dataframe(filtered, use_container_width=True, hide_index=True)

def tab_assumptions():
    section_header("SIMULATION INPUTS")
    if "assume_vals" not in st.session_state: st.session_state.assume_vals = {k: v for k, v in ASSUMPTIONS}
    with st.form("assumptions_form"):
        cols = st.columns(2)
        updated = {}
        for i, (k, v) in enumerate(ASSUMPTIONS):
            with cols[i % 2]: updated[k] = st.text_input(k, value=st.session_state.assume_vals.get(k, v))
        if st.form_submit_button("💾 Save Assumptions"):
            st.session_state.assume_vals = updated
            st.success("Simulation parameters updated.")

def tab_comm_hub():
    section_header("COMMUNICATION HUB")
    st.info("Feedback loop for Operational Logic Errors and Feature Requests.")

# ─── MAIN ─────────────────────────────────────────────────────────────────────

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
    stats = derive(df)

    tabs = st.tabs(["📋 Overview", "📊 Breakdown", "👥 Headcount", "💰 Cost Analysis", "🔬 Sensitivity", "🗂 Raw Data", "⚙️ Assumptions", "💬 Comm Hub"])

    with tabs[0]: tab_overview(df, stats)
    with tabs[1]: tab_breakdown(df, stats)
    with tabs[2]: tab_headcount(df, stats)
    with tabs[3]: tab_cost(df, stats)
    with tabs[4]: tab_sensitivity(df, stats)
    with tabs[5]: tab_rawdata(df)
    with tabs[6]: tab_assumptions()
    with tabs[7]: tab_comm_hub()

if __name__ == "__main__":
    main()
