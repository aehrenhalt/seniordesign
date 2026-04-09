"""
BrewOps Command — Operations Intelligence Dashboard
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
    --red:       #C8102E;
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

/* ── Heatmap legend ── */
.hm-legend {
    display: flex; align-items: center; gap: 10px;
    font-size: 0.72rem; color: var(--silver); margin-top: 6px;
}
.hm-gradient {
    width: 120px; height: 10px;
    background: linear-gradient(to right, #132040, #C8102E);
    border-radius: 2px;
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

/* ── Upload success message ── */
.stAlert { border-radius: 3px !important; }

/* ── Misc ── */
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: var(--white) !important;
}
</style>
""", unsafe_allow_html=True)

# ─── DATA LAYER ───────────────────────────────────────────────────────────────

SAMPLE_DATA = {
    "barista_name":  ["Maya Chen","James Okafor","Sofia Reyes","Tom Willis","Aisha Brown",
                      "Carlos Diaz","Priya Nair","Leo Park","Nina Russo","Dave Kim",
                      "Fatima Al-Said","Ryan Torres","Mei Lin","Omar Hassan","Sara Yildiz"],
    "shift_start":   ["06:00","06:00","14:00","06:00","10:00","14:00","22:00","06:00",
                      "06:00","14:00","06:00","10:00","14:00","22:00","06:00"],
    "shift_end":     ["14:00","14:00","22:00","10:00","18:00","22:00","06:00","14:00",
                      "14:00","22:00","14:00","18:00","22:00","06:00","14:00"],
    "location":      ["Downtown","Midtown","Downtown","Airport","Mall","Midtown","Airport",
                      "Mall","Suburb","Suburb","Riverside","Airport","Riverside","Downtown","Mall"],
    "cluster":       ["Flagship","Core","Flagship","Transit","Core","Core","Transit","Core",
                      "Satellite","Satellite","Core","Transit","Core","Flagship","Core"],
    "shift_type":    ["Regular","Regular","Regular","OT","Regular","Regular","Relief","Regular",
                      "Regular","Regular","Regular","OT","Regular","Relief","Regular"],
    "work_type":     ["Full","Full","Full","Part","Full","Full","Full","Full",
                      "Full","Full","Full","Part","Full","Full","Part"],
    "required_hc":   [8, 6, 7, 4, 5, 6, 3, 5, 4, 4, 5, 4, 5, 3, 3],
    "actual_hc":     [8, 7, 6, 4, 5, 6, 3, 4, 4, 5, 5, 3, 5, 3, 3],
    "labor_cost":    [168,168,189,126,160,176,220,152,144,152,160,108,168,220,96],
    "week_hours":    [38, 40, 36, 42, 40, 38, 35, 40, 37, 39, 40, 44, 38, 36, 20],
    "predicted_demand":[10,8,9,5,6,7,4,6,5,5,6,5,6,4,4],
    "date":          ["2026-04-07"]*7 + ["2026-04-08"]*8,
}

SUCCESS_LOG = [
    {"name":"schedule_apr07_v3.csv","date":"Apr 7, 2026","score":98,"kpis":"All 6 KPIs met","status":"green"},
    {"name":"schedule_apr06_v2.csv","date":"Apr 6, 2026","score":95,"kpis":"5 / 6 KPIs met","status":"amber"},
    {"name":"schedule_apr05_v1.csv","date":"Apr 5, 2026","score":97,"kpis":"All 6 KPIs met","status":"green"},
    {"name":"schedule_apr04_v2.csv","date":"Apr 4, 2026","score":100,"kpis":"All 6 KPIs met","status":"green"},
    {"name":"schedule_apr03_v1.csv","date":"Apr 3, 2026","score":88,"kpis":"4 / 6 KPIs met","status":"red"},
]

ISSUES_FILE = "/tmp/brewops_issues.json"
FEATURES_FILE = "/tmp/brewops_features.json"

DEFAULT_ISSUES = [
    {"id":1,"title":"OT threshold exceeded — Airport cluster","priority":"High","status":"Open",
     "desc":"Relief baristas scheduled past 48-hr weekly cap on 3 occasions.","reporter":"Scheduling","date":"Apr 6"},
    {"id":2,"title":"Overnight gap 22:00–06:00 at Midtown","priority":"Med","status":"In Progress",
     "desc":"Logic assigns no coverage for overnight window on weekends.","reporter":"Scheduling","date":"Apr 5"},
    {"id":3,"title":"Monday AM demand underestimated ~15%","priority":"Med","status":"Open",
     "desc":"Predicted demand does not reflect Monday rush patterns.","reporter":"Ops","date":"Apr 3"},
]

DEFAULT_FEATURES = [
    {"rank":1,"name":"Real-time demand feed integration","meta":"Ops team · High · Apr 1","status":"Planned"},
    {"rank":2,"name":"Auto-flag when actual < required HC","meta":"Scheduling · High · Mar 28","status":"In Review"},
    {"rank":3,"name":"Cluster-level cost rollup export (.xlsx)","meta":"Ops team · Med · Mar 20","status":"Backlog"},
    {"rank":4,"name":"Relief pool visibility panel","meta":"Scheduling · Med · Mar 15","status":"Backlog"},
]

ASSUMPTIONS = [
    ("Regular hourly rate",  "$21.00"),
    ("OT multiplier",        "1.5×"),
    ("Relief premium",       "+30%"),
    ("Min shift length",     "4 hrs"),
    ("Max weekly hours",     "48 hrs"),
    ("Coverage target",      "≥ 95%"),
    ("Demand forecast src",  "30-day historical avg"),
    ("OT activation",        "40 hrs / week"),
    ("Scheduling horizon",   "7 days"),
    ("Min rest bet. shifts", "8 hrs"),
]

def load_json(path, default):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f)

def get_df(uploaded=None):
    if uploaded is not None:
        try:
            if uploaded.name.endswith(".csv"):
                return pd.read_csv(uploaded)
            else:
                return pd.read_excel(uploaded)
        except Exception as e:
            st.error(f"Could not parse file: {e}")
    return pd.DataFrame(SAMPLE_DATA)

# ─── DERIVED STATS ────────────────────────────────────────────────────────────

def derive(df):
    total        = len(df)
    total_cost   = df["labor_cost"].sum()
    met          = (df["actual_hc"] >= df["required_hc"]).sum()
    adherence    = round(met / total * 100) if total else 0
    excess       = (df["actual_hc"] - df["required_hc"]).clip(lower=0).sum()
    unmet        = (df["required_hc"] - df["actual_hc"]).clip(lower=0).sum()
    avg_cost     = round(total_cost / total) if total else 0
    ot_pct       = round(df[df["shift_type"]=="OT"]["labor_cost"].sum() / total_cost * 100, 1) if total_cost else 0
    locs         = df["location"].unique().tolist()
    clusters     = df["cluster"].unique().tolist()
    return dict(total=total, total_cost=total_cost, adherence=adherence,
                excess=int(excess), unmet=int(unmet), avg_cost=avg_cost,
                ot_pct=ot_pct, locs=locs, clusters=clusters)

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

def navy_colors(n):
    palette = ["#C8102E","#4472C4","#D4AF37","#6A8E72","#8B6347","#A63D1F","#9C59B6","#2196F3"]
    return palette[:n]

def chart_demand_vs_capacity(df):
    locs = df["location"].unique()
    req  = [df[df.location==l]["required_hc"].sum() for l in locs]
    act  = [df[df.location==l]["actual_hc"].sum() for l in locs]
    fig  = go.Figure()
    fig.add_bar(name="Required HC", x=list(locs), y=req,
                marker_color="#1E3060", marker_line_color="#4472C4", marker_line_width=1)
    fig.add_bar(name="Actual HC",   x=list(locs), y=act,
                marker_color="#C8102E", marker_line_color="#E8193A", marker_line_width=1)
    fig.update_layout(**PLOTLY_LAYOUT, barmode="group", title="",
                      legend=dict(orientation="h", y=1.1))
    return fig

def chart_heatmap(df):
    days   = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    locs   = df["location"].unique().tolist()
    rng    = np.random.default_rng(42)
    z      = [[int(3 + rng.integers(0, 7)) for _ in days] for _ in locs]
    fig    = go.Figure(go.Heatmap(
        z=z, x=days, y=locs,
        colorscale=[[0,"#132040"],[0.5,"#1E3060"],[1,"#C8102E"]],
        showscale=True,
        colorbar=dict(tickfont=dict(color="#C0C8D8"), thickness=10),
    ))
    fig.update_layout(**PLOTLY_LAYOUT, title="")
    return fig

def chart_shift_type_donut(df):
    types  = df["shift_type"].value_counts()
    colors = {"Regular":"#4472C4","OT":"#C8102E","Relief":"#D4AF37"}
    fig    = go.Figure(go.Pie(
        labels=types.index, values=types.values,
        hole=0.55,
        marker_colors=[colors.get(t,"#888") for t in types.index],
        textfont_color="white",
    ))
    fig.update_layout(**PLOTLY_LAYOUT, showlegend=True,
                      legend=dict(orientation="v"),
                      margin=dict(l=10, r=10, t=10, b=10))
    return fig

def chart_cost_breakdown(df):
    types  = ["Regular","OT","Relief"]
    costs  = [df[df.shift_type==t]["labor_cost"].sum() for t in types]
    colors = ["#4472C4","#C8102E","#D4AF37"]
    fig    = go.Figure(go.Bar(
        x=types, y=costs, marker_color=colors,
        text=[f"${c:,}" for c in costs], textposition="auto",
        textfont_color="white",
    ))
    fig.update_layout(**PLOTLY_LAYOUT, title="", showlegend=False)
    return fig

def chart_cluster_cost(df):
    cl  = df.groupby("cluster")["labor_cost"].sum().reset_index()
    fig = go.Figure(go.Bar(
        x=cl["labor_cost"], y=cl["cluster"],
        orientation="h",
        marker_color="#C8102E",
        text=[f"${v:,}" for v in cl["labor_cost"]], textposition="auto",
        textfont_color="white",
    ))
    fig.update_layout(**PLOTLY_LAYOUT, title="", showlegend=False,
                      xaxis=dict(title="", gridcolor="rgba(192,200,216,0.08)"))
    return fig

def chart_demand_vs_predicted(df):
    locs  = df["location"].unique()
    pred  = [df[df.location==l]["predicted_demand"].sum() for l in locs]
    sched = [df[df.location==l]["actual_hc"].sum() for l in locs]
    fig   = go.Figure()
    fig.add_scatter(name="Predicted Demand", x=list(locs), y=pred,
                    mode="lines+markers",
                    line=dict(color="#D4AF37", width=2, dash="dot"),
                    marker=dict(color="#D4AF37", size=7))
    fig.add_scatter(name="Scheduled Capacity", x=list(locs), y=sched,
                    mode="lines+markers",
                    line=dict(color="#C8102E", width=2),
                    marker=dict(color="#C8102E", size=7))
    fig.update_layout(**PLOTLY_LAYOUT, title="",
                      legend=dict(orientation="h", y=1.1))
    return fig

def chart_sensitivity(rate=21.0, ot_mult=1.5, hc_delta=0, df=None):
    if df is None:
        df = pd.DataFrame(SAMPLE_DATA)
    hc_range  = list(range(-30, 35, 5))
    base_cost = df["labor_cost"].sum()
    adh_base  = round((df["actual_hc"] >= df["required_hc"]).sum() / len(df) * 100)
    costs     = [round(base_cost * (rate/21) * (1 + d/100) * ((ot_mult/1.5)*.08+.92)) for d in hc_range]
    covers    = [min(100, max(55, adh_base + round(d * 0.45))) for d in hc_range]
    fig = go.Figure()
    fig.add_bar(name="Projected Cost ($)", x=[f"{d:+}%" for d in hc_range], y=costs,
                marker_color="#1E3060", marker_line_color="#4472C4", marker_line_width=1,
                yaxis="y1")
    fig.add_scatter(name="Coverage (%)", x=[f"{d:+}%" for d in hc_range], y=covers,
                    mode="lines+markers", line=dict(color="#D4AF37", width=2),
                    marker=dict(size=6), yaxis="y2")
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title="",
        yaxis=dict(title="Labor Cost ($)", gridcolor="rgba(192,200,216,0.08)"),
        yaxis2=dict(title="Coverage (%)", overlaying="y", side="right",
                    range=[50, 105], gridcolor="rgba(0,0,0,0)"),
        legend=dict(orientation="h", y=1.1),
        xaxis=dict(title="Headcount Delta"),
    )
    return fig

# ─── UI COMPONENTS ────────────────────────────────────────────────────────────

def section_header(title):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)

def kpi_row(stats, df):
    total_cost = stats["total_cost"]
    reg_cost   = df[df.shift_type=="Regular"]["labor_cost"].sum()
    ot_cost    = df[df.shift_type=="OT"]["labor_cost"].sum()

    cols = st.columns(5)
    items = [
        ("Total Shifts",     str(stats["total"]),         "Scheduled this cycle",     "good"),
        (f"Labor Cost",      f"${total_cost:,}",          f"Avg ${stats['avg_cost']}/shift", "info"),
        ("Logic Adherence",  f"{stats['adherence']}%",
         "✔ On target" if stats["adherence"] >= 90 else "⚠ Below 90%",
         "good" if stats["adherence"] >= 90 else "warn"),
        ("Excess Supply",    str(stats["excess"]),        "Over-placed HC",           "info"),
        ("Unmet Demand",     str(stats["unmet"]),
         "✔ Zero gaps" if stats["unmet"]==0 else "⚠ Gaps present",
         "good" if stats["unmet"]==0 else "warn"),
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

def success_log():
    section_header("SUCCESSFUL RUN LOG")
    color_map = {"green":"#4CAF50","amber":"#FFC107","red":"#C8102E"}
    html = '<div class="panel">'
    for r in SUCCESS_LOG:
        color = color_map[r["status"]]
        score_color = color
        html += f"""
        <div class="log-row">
            <div class="log-dot" style="background:{color}"></div>
            <div style="flex:1">
                <span style="font-size:.88rem;font-weight:600;color:#F0F4FF">{r['name']}</span>
                <span style="font-size:.75rem;color:#C0C8D8;margin-left:10px">{r['date']} · {r['kpis']}</span>
            </div>
            <div style="font-size:.95rem;font-weight:700;color:{score_color}">{r['score']}%</div>
        </div>"""
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

def badge_html(text, kind="gray"):
    return f'<span class="badge badge-{kind}">{text}</span>'

# ─── TABS ─────────────────────────────────────────────────────────────────────

def tab_overview(df, stats):
    kpi_row(stats, df)
    st.markdown("")

    c1, c2 = st.columns([3, 2])
    with c1:
        section_header("DEMAND VS. SCHEDULED CAPACITY")
        st.plotly_chart(chart_demand_vs_predicted(df), use_container_width=True, config={"displayModeBar":False})
    with c2:
        section_header("SHIFT TYPE DISTRIBUTION")
        st.plotly_chart(chart_shift_type_donut(df), use_container_width=True, config={"displayModeBar":False})

    section_header("STAFFING HEATMAP — LOCATIONS × DAY OF WEEK")
    st.plotly_chart(chart_heatmap(df), use_container_width=True, config={"displayModeBar":False})

    c1, c2 = st.columns([3, 2])
    with c1:
        success_log()
    with c2:
        section_header("QUICK STATS")
        ot_cost  = df[df.shift_type=="OT"]["labor_cost"].sum()
        rel_cost = df[df.shift_type=="Relief"]["labor_cost"].sum()
        reg_cost = df[df.shift_type=="Regular"]["labor_cost"].sum()
        wt_full  = len(df[df.work_type=="Full"])
        wt_part  = len(df[df.work_type=="Part"])
        ot_flag  = df[df.week_hours > 40]

        st.markdown(f"""
        <div class="panel">
            <div class="assume-row"><span class="assume-key">Regular cost</span><span class="assume-val">${reg_cost:,}</span></div>
            <div class="assume-row"><span class="assume-key">OT cost</span><span class="assume-val" style="color:#C8102E">${ot_cost:,}</span></div>
            <div class="assume-row"><span class="assume-key">Relief cost</span><span class="assume-val" style="color:#D4AF37">${rel_cost:,}</span></div>
            <div class="assume-row"><span class="assume-key">Full-time workers</span><span class="assume-val">{wt_full}</span></div>
            <div class="assume-row"><span class="assume-key">Part-time workers</span><span class="assume-val">{wt_part}</span></div>
            <div class="assume-row"><span class="assume-key">OT flagged workers</span><span class="assume-val" style="color:#C8102E">{len(ot_flag)}</span></div>
        </div>
        """, unsafe_allow_html=True)

def tab_breakdown(df, stats):
    section_header("MODEL KPIs — CLUSTER, SHIFT TYPE & WORK TYPE SPLITS")
    clusters = df["cluster"].unique()
    cols = st.columns(len(clusters))
    for col, cl in zip(cols, clusters):
        sub = df[df.cluster == cl]
        cost = sub["labor_cost"].sum()
        shifts = len(sub)
        met = int((sub.actual_hc >= sub.required_hc).sum())
        adh = round(met/shifts*100) if shifts else 0
        col.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">${cost:,}</div>
            <div class="kpi-label">{cl}</div>
            <div class="kpi-delta-good">{shifts} shifts · {adh}% adherence</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")
    c1, c2 = st.columns(2)
    with c1:
        section_header("COST BY SHIFT TYPE")
        st.plotly_chart(chart_cost_breakdown(df), use_container_width=True, config={"displayModeBar":False})
    with c2:
        section_header("COST BY CLUSTER")
        st.plotly_chart(chart_cluster_cost(df), use_container_width=True, config={"displayModeBar":False})

    section_header("DEMAND VS. SCHEDULED CAPACITY BY LOCATION")
    st.plotly_chart(chart_demand_vs_capacity(df), use_container_width=True, config={"displayModeBar":False})

    section_header("WORK-TYPE SPLIT")
    wt = df.groupby("work_type").agg(count=("barista_name","count"), cost=("labor_cost","sum")).reset_index()
    cols = st.columns(len(wt))
    for col, row in zip(cols, wt.itertuples()):
        pct = round(row.count / len(df) * 100)
        col.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{pct}%</div>
            <div class="kpi-label">{row.work_type}-time workers</div>
            <div class="kpi-delta-good">{row.count} baristas · ${row.cost:,}</div>
        </div>""", unsafe_allow_html=True)

def tab_headcount(df, stats):
    section_header("DAILY HEADCOUNT — EXCESS SUPPLY & UNMET DEMAND")
    st.markdown(f"""
    <div style="display:flex;gap:12px;margin-bottom:1rem">
        <div class="kpi-card" style="flex:1;text-align:center">
            <div class="kpi-value">{df['required_hc'].sum()}</div>
            <div class="kpi-label">Total Required HC</div>
        </div>
        <div class="kpi-card" style="flex:1;text-align:center">
            <div class="kpi-value">{df['actual_hc'].sum()}</div>
            <div class="kpi-label">Total Scheduled HC</div>
        </div>
        <div class="kpi-card" style="flex:1;text-align:center">
            <div class="kpi-value">{stats['adherence']}%</div>
            <div class="kpi-label">Coverage Rate</div>
        </div>
        <div class="kpi-card" style="flex:1;text-align:center">
            <div class="kpi-value" style="color:#C8102E">{stats['unmet']}</div>
            <div class="kpi-label">Unmet Demand</div>
        </div>
        <div class="kpi-card" style="flex:1;text-align:center">
            <div class="kpi-value" style="color:#D4AF37">{stats['excess']}</div>
            <div class="kpi-label">Excess Supply</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Location detail table
    section_header("HEADCOUNT BY LOCATION")
    loc_tbl = df.groupby("location").agg(
        cluster=("cluster","first"),
        required=("required_hc","sum"),
        actual=("actual_hc","sum"),
    ).reset_index()
    loc_tbl["delta"]  = loc_tbl["actual"] - loc_tbl["required"]
    loc_tbl["status"] = loc_tbl["delta"].apply(
        lambda d: "✔ Met" if d == 0 else ("⚠ Understaffed" if d < 0 else "↑ Overstaffed")
    )
    st.dataframe(
        loc_tbl.rename(columns={"location":"Location","cluster":"Cluster",
                                "required":"Required","actual":"Actual",
                                "delta":"Delta","status":"Status"}),
        use_container_width=True, hide_index=True,
    )

    section_header("HEATMAP — STAFFING LEVELS")
    st.plotly_chart(chart_heatmap(df), use_container_width=True, config={"displayModeBar":False})

def tab_cost(df, stats):
    total_cost = stats["total_cost"]
    reg_cost   = df[df.shift_type=="Regular"]["labor_cost"].sum()
    ot_cost    = df[df.shift_type=="OT"]["labor_cost"].sum()
    rel_cost   = df[df.shift_type=="Relief"]["labor_cost"].sum()

    section_header("LABOR COST BREAKDOWN — REGULAR, OT, RELIEF")
    st.markdown(f"""
    <div style="display:flex;gap:12px;margin-bottom:1rem">
        <div class="kpi-card" style="flex:1;text-align:center">
            <div class="kpi-value">${total_cost:,}</div>
            <div class="kpi-label">Total Labor Cost</div>
        </div>
        <div class="kpi-card" style="flex:1;text-align:center">
            <div class="kpi-value">${reg_cost:,}</div>
            <div class="kpi-label">Regular</div>
            <div class="kpi-delta-good">{round(reg_cost/total_cost*100)}% of total</div>
        </div>
        <div class="kpi-card" style="flex:1;text-align:center">
            <div class="kpi-value" style="color:#C8102E">${ot_cost:,}</div>
            <div class="kpi-label">Overtime</div>
            <div class="kpi-delta-warn">{round(ot_cost/total_cost*100)}% — monitor</div>
        </div>
        <div class="kpi-card" style="flex:1;text-align:center">
            <div class="kpi-value" style="color:#D4AF37">${rel_cost:,}</div>
            <div class="kpi-label">Relief</div>
            <div class="kpi-delta-good">{round(rel_cost/total_cost*100)}% of total</div>
        </div>
        <div class="kpi-card" style="flex:1;text-align:center">
            <div class="kpi-value">${stats['avg_cost']:,}</div>
            <div class="kpi-label">Avg per Shift</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        section_header("COST BY SHIFT TYPE")
        st.plotly_chart(chart_cost_breakdown(df), use_container_width=True, config={"displayModeBar":False})
    with c2:
        section_header("COST BY CLUSTER")
        st.plotly_chart(chart_cluster_cost(df), use_container_width=True, config={"displayModeBar":False})

    section_header("BARISTA-LEVEL COST DETAIL")
    detail = df[["barista_name","location","shift_start","shift_end","shift_type","week_hours","labor_cost"]].copy()
    detail = detail.sort_values("labor_cost", ascending=False)
    detail.columns = ["Barista","Location","Start","End","Type","Week Hrs","Cost ($)"]
    st.dataframe(detail, use_container_width=True, hide_index=True)

def tab_sensitivity(df, stats):
    section_header("COST & COVERAGE SENSITIVITY — RATE / HEADCOUNT CHANGES")

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">ADJUST PARAMETERS</div>', unsafe_allow_html=True)
        rate   = st.slider("Regular hourly rate ($)",   min_value=15, max_value=35, value=21, step=1)
        ot_m   = st.slider("OT multiplier",             min_value=1.0, max_value=3.0, value=1.5, step=0.1)
        hc_d   = st.slider("Headcount delta (%)",       min_value=-30, max_value=30, value=0, step=1)
        rel_p  = st.slider("Relief premium (%)",        min_value=10, max_value=60, value=30, step=5)
        st.markdown("---")

        base_cost = stats["total_cost"]
        proj_cost = round(base_cost * (rate/21) * (1 + hc_d/100) * ((ot_m/1.5)*.08+.92))
        delta_val = proj_cost - base_cost
        cover_est = min(100, max(55, stats["adherence"] + round(hc_d * .45)))
        delta_col = "#C8102E" if delta_val > 0 else "#4CAF50"

        st.markdown(f"""
        <div class="assume-row"><span class="assume-key">Projected cost</span><span class="assume-val">${proj_cost:,}</span></div>
        <div class="assume-row"><span class="assume-key">Cost delta</span><span class="assume-val" style="color:{delta_col}">{'+' if delta_val>=0 else ''}{delta_val:,}</span></div>
        <div class="assume-row"><span class="assume-key">Est. coverage</span><span class="assume-val">{cover_est}%</span></div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        section_header("COST & COVERAGE vs. HEADCOUNT DELTA")
        st.plotly_chart(chart_sensitivity(rate, ot_m, hc_d, df),
                        use_container_width=True, config={"displayModeBar":False})

def tab_rawdata(df):
    section_header(f"RAW DATA — {len(df)} RECORDS")
    c1, c2 = st.columns([3,1])
    with c1:
        search = st.text_input("🔍  Filter by barista name or location", "")
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        buf = io.BytesIO()
        df.to_excel(buf, index=False)
        st.download_button("⬇  Export .xlsx", buf.getvalue(),
                          file_name="schedule_export.xlsx",
                          mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    filtered = df
    if search:
        mask = (df["barista_name"].str.contains(search, case=False, na=False) |
                df["location"].str.contains(search, case=False, na=False))
        filtered = df[mask]

    st.dataframe(filtered, use_container_width=True, hide_index=True)

def tab_assumptions():
    section_header("COST & SENSITIVITY INPUTS")
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">CLICK ANY VALUE TO EDIT — SAVED ON SUBMIT</div>', unsafe_allow_html=True)

    if "assume_vals" not in st.session_state:
        st.session_state.assume_vals = {k: v for k, v in ASSUMPTIONS}

    with st.form("assumptions_form"):
        cols = st.columns(2)
        updated = {}
        for i, (k, v) in enumerate(ASSUMPTIONS):
            with cols[i % 2]:
                updated[k] = st.text_input(k, value=st.session_state.assume_vals.get(k, v))
        submitted = st.form_submit_button("💾  Save Assumptions")
        if submitted:
            st.session_state.assume_vals = updated
            st.success("Assumptions saved. Will recalculate on next upload.")

    st.markdown("</div>", unsafe_allow_html=True)

def tab_comm_hub():
    section_header("COMMUNICATION HUB — THE FEEDBACK LOOP")

    issues   = st.session_state.get("issues",   load_json(ISSUES_FILE,   DEFAULT_ISSUES))
    features = st.session_state.get("features", load_json(FEATURES_FILE, DEFAULT_FEATURES))

    left, right = st.columns(2)

    # ── Left: Issue reporting + open issues
    with left:
        st.markdown('<div class="panel-title">LOG SUSPECTED LOGIC ERROR</div>', unsafe_allow_html=True)
        with st.form("issue_form", clear_on_submit=True):
            title    = st.text_input("Issue title", placeholder="e.g. OT cap exceeded at Airport cluster")
            severity = st.selectbox("Severity", ["High — affects coverage","Med — affects labor cost","Low — minor discrepancy"])
            location = st.text_input("Location / cluster", placeholder="e.g. Airport · Transit cluster")
            expected = st.text_input("Expected behavior", placeholder="What should the logic have done?")
            observed = st.text_area("Observed behavior", placeholder="Describe what you saw vs. expected...", height=90)
            submitted = st.form_submit_button("🚩  Submit Issue")
            if submitted and title.strip():
                new_issue = {
                    "id": len(issues)+1,
                    "title": title,
                    "priority": severity.split(" ")[0],
                    "status": "Open",
                    "desc": observed or "No description.",
                    "reporter": "Scheduling",
                    "date": date.today().strftime("Apr %d"),
                }
                issues = [new_issue] + issues
                st.session_state.issues = issues
                save_json(ISSUES_FILE, issues)
                st.success(f"Issue logged: '{title}'")

        section_header(f"OPEN ISSUES ({len(issues)})")
        pri_color = {"High":"red","Med":"amber","Low":"gray"}
        sta_color = {"Open":"amber","In Progress":"blue","Resolved":"green"}
        for iss in issues:
            pc = pri_color.get(iss["priority"], "gray")
            sc = sta_color.get(iss["status"], "gray")
            st.markdown(f"""
            <div class="issue-item">
                <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:8px;margin-bottom:4px">
                    <div class="issue-title">{iss['title']}</div>
                    <div style="display:flex;gap:5px;flex-shrink:0">
                        {badge_html(iss['priority'], pc)}
                        {badge_html(iss['status'], sc)}
                    </div>
                </div>
                <div class="issue-meta">{iss['desc']} — {iss['reporter']} · {iss['date']}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Right: Feature backlog + request form
    with right:
        st.markdown('<div class="panel-title">FEATURE REQUEST BACKLOG</div>', unsafe_allow_html=True)
        feat_status_color = {"Planned":"blue","In Review":"green","Backlog":"gray"}
        for f in features:
            sc = feat_status_color.get(f["status"], "gray")
            st.markdown(f"""
            <div class="issue-item" style="display:flex;align-items:flex-start;gap:10px">
                <div class="rank-badge">{f['rank']}</div>
                <div style="flex:1">
                    <div class="issue-title">{f['name']}</div>
                    <div class="issue-meta">{f['meta']}</div>
                </div>
                {badge_html(f['status'], sc)}
            </div>
            """, unsafe_allow_html=True)

        section_header("REQUEST A PROGRAM UPDATE")
        with st.form("feature_form", clear_on_submit=True):
            fname    = st.text_input("Feature title", placeholder="Short name for this request")
            fpri     = st.selectbox("Priority", ["High","Medium","Low"])
            fdesc    = st.text_area("Description", placeholder="Describe the requested update and its scheduling impact...", height=80)
            fsub     = st.form_submit_button("➕  Add to Backlog")
            if fsub and fname.strip():
                new_feat = {
                    "rank": len(features)+1,
                    "name": fname,
                    "meta": f"Ops team · {fpri} · {date.today().strftime('Apr %d')}",
                    "status": "Backlog",
                }
                features = features + [new_feat]
                st.session_state.features = features
                save_json(FEATURES_FILE, features)
                st.success(f"Feature '{fname}' added to backlog.")

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────

def sidebar(df):
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:12px 0 16px 0">
            <div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;letter-spacing:3px;color:#F0F4FF">
                🇺🇸 BREWOPS
            </div>
            <div style="font-size:0.65rem;letter-spacing:2px;color:#C0C8D8">COMMAND CENTER</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📁 UPLOAD SCHEDULE")
        uploaded = st.file_uploader(
            "Drag .csv or .xlsx file here",
            type=["csv","xlsx"],
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown("### 📊 VIEW MODE")
        view = st.radio("", ["Operations View","Scheduling View"], label_visibility="collapsed")

        st.markdown("---")
        st.markdown("### ℹ️ DATASET INFO")
        st.markdown(f"""
        <div style="font-size:.8rem;color:#C0C8D8">
            <div class="assume-row"><span class="assume-key">Records</span><span class="assume-val">{len(df)}</span></div>
            <div class="assume-row"><span class="assume-key">Locations</span><span class="assume-val">{df['location'].nunique()}</span></div>
            <div class="assume-row"><span class="assume-key">Clusters</span><span class="assume-val">{df['cluster'].nunique()}</span></div>
            <div class="assume-row"><span class="assume-key">Date range</span><span class="assume-val">{df['date'].min()} – {df['date'].max()}</span></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"""
        <div style="font-size:.7rem;color:#C0C8D8;letter-spacing:1px;text-align:center">
            BREWOPS COMMAND v1.0<br>
            <span style="color:#C8102E">●</span> OPERATIONS VIEW ACTIVE
        </div>
        """, unsafe_allow_html=True)

        return uploaded

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    # Header
    st.markdown("""
    <div class="ops-header">
        <div>
            <span class="ops-header-title">🇺🇸 BrewOps Command</span>
            <div style="font-size:.75rem;color:#C0C8D8;letter-spacing:1.5px;margin-top:2px">
                OPERATIONS INTELLIGENCE DASHBOARD
            </div>
        </div>
        <div style="text-align:right">
            <div class="ops-header-badge">Operations View</div>
            <div style="font-size:.7rem;color:#C0C8D8;margin-top:4px">
                """ + datetime.now().strftime("%b %d, %Y  %H:%M") + """
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded = sidebar(pd.DataFrame(SAMPLE_DATA))
    df = get_df(uploaded)

    if uploaded:
        st.markdown('<div class="success-box">✔ Schedule file loaded — KPIs refreshed from uploaded data.</div>',
                    unsafe_allow_html=True)

    stats = derive(df)

    # Sidebar dataset info update (needs real df)
    # Tab bar
    tabs = st.tabs([
        "📋 Overview",
        "📊 Breakdown KPIs",
        "👥 Headcount",
        "💰 Cost Analysis",
        "🔬 Sensitivity",
        "🗂 Raw Data",
        "⚙️ Assumptions",
        "💬 Comm Hub",
    ])

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
