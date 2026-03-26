import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
from datetime import datetime, timedelta

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="B2B Support Analytics | Group 2",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,600&display=swap');

  :root {
    --bg:        #0F1117;
    --surface:   #161B27;
    --surface2:  #1C2333;
    --border:    rgba(255,255,255,0.07);
    --gold:      #C9A84C;
    --gold-dim:  rgba(201,168,76,0.15);
    --gold-line: rgba(201,168,76,0.35);
    --text:      #E8EAF0;
    --muted:     #6B7280;
    --subtle:    #9CA3AF;
    --green:     #4ADE80;
    --red:       #F87171;
    --green-bg:  rgba(74,222,128,0.10);
    --red-bg:    rgba(248,113,113,0.10);
  }

  html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
  }

  .stApp {
    background-color: var(--bg) !important;
  }

  .block-container {
    padding-top: 0 !important;
    padding-bottom: 3rem !important;
    max-width: 100% !important;
  }

  /* ── HEADER ── */
  .header-banner {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 1.6rem 2.8rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 2rem;
  }
  .header-left {}
  .header-title {
    font-family: 'Fraunces', serif;
    font-size: 1.65rem;
    font-weight: 600;
    color: #FFFFFF;
    letter-spacing: -0.3px;
    line-height: 1.15;
    margin: 0;
  }
  .header-sub {
    font-size: 0.75rem;
    color: var(--gold);
    font-weight: 500;
    margin-top: 5px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
  }
  .header-right { display: flex; align-items: center; gap: 1.2rem; }
  .group-badge {
    background: var(--surface2);
    border: 1px solid var(--gold-line);
    border-radius: 8px;
    padding: 0.65rem 1.3rem;
    text-align: right;
  }
  .group-badge .grp-name {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    font-size: 0.82rem;
    color: var(--gold);
    letter-spacing: 1.2px;
    text-transform: uppercase;
  }
  .group-badge .members {
    font-size: 0.70rem;
    color: var(--subtle);
    margin-top: 4px;
    line-height: 1.6;
    font-weight: 400;
  }
  .logo-box {
    width: 62px; height: 62px;
    background: var(--surface2);
    border: 1px solid var(--gold-line);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    flex-direction: column;
    font-family: 'Fraunces', serif;
    font-size: 1rem;
    font-weight: 600;
    color: var(--gold);
    letter-spacing: 0;
  }
  .logo-box span {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.48rem;
    letter-spacing: 2px;
    color: var(--muted);
    text-transform: uppercase;
    margin-top: 1px;
  }

  /* ── KPI CARDS ── */
  .kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.5rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, box-shadow 0.2s;
  }
  .kpi-card:hover {
    border-color: var(--gold-line);
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
  }
  .kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
  }
  .kpi-card.blue::after  { background: #4F7FBF; }
  .kpi-card.teal::after  { background: #3D8C7A; }
  .kpi-card.amber::after { background: var(--gold); }
  .kpi-card.coral::after { background: #C0695A; }

  .kpi-icon { font-size: 1.3rem; margin-bottom: 0.75rem; display: block; opacity: 0.8; }
  .kpi-value {
    font-family: 'Fraunces', serif;
    font-size: 2.1rem;
    font-weight: 600;
    color: #FFFFFF;
    line-height: 1;
    letter-spacing: -0.5px;
  }
  .kpi-label {
    font-size: 0.70rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1.2px;
    font-weight: 600;
    margin-top: 6px;
  }
  .kpi-delta {
    font-size: 0.72rem;
    font-weight: 600;
    margin-top: 8px;
    padding: 3px 9px;
    border-radius: 4px;
    display: inline-block;
    letter-spacing: 0.3px;
  }
  .kpi-delta.up   { background: var(--green-bg); color: var(--green); }
  .kpi-delta.down { background: var(--red-bg);   color: var(--red); }

  /* ── SECTION TITLE ── */
  .section-title {
    font-family: 'Fraunces', serif;
    font-size: 1.0rem;
    font-weight: 400;
    color: var(--text);
    letter-spacing: 0.2px;
    border-left: 2px solid var(--gold);
    padding-left: 12px;
    margin: 1.6rem 0 0.9rem 0;
  }

  /* ── SIDEBAR ── */
  section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
  }
  section[data-testid="stSidebar"] .stMultiSelect label,
  section[data-testid="stSidebar"] .stSelectbox label {
    color: var(--muted) !important;
    font-size: 0.70rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
  }
  section[data-testid="stSidebar"] h2 {
    font-family: 'Fraunces', serif !important;
    font-weight: 400 !important;
    color: var(--text) !important;
    font-size: 1.1rem !important;
  }

  /* Streamlit overrides */
  .stMetric { display: none; }
  div[data-testid="stMetric"] { display: none; }

  /* ── TABS ── */
  .stTabs [data-baseweb="tab-list"] {
    gap: 2px;
    background: var(--surface);
    border-radius: 8px;
    padding: 4px;
    border: 1px solid var(--border);
  }
  .stTabs [data-baseweb="tab"] {
    border-radius: 6px;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    color: var(--muted) !important;
    padding: 7px 18px !important;
    letter-spacing: 0.3px !important;
  }
  .stTabs [aria-selected="true"] {
    background: var(--surface2) !important;
    color: var(--gold) !important;
    border: 1px solid var(--gold-line) !important;
  }
  .stTabs [data-baseweb="tab-panel"] { padding-top: 1rem !important; }

  /* ── INSIGHT CARDS ── */
  .insight-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.9rem;
    transition: border-color 0.2s;
  }
  .insight-card:hover { border-color: var(--gold-line); }
  .insight-card h4 {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: var(--gold);
    margin: 0 0 6px 0;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 700;
  }
  .insight-card p {
    color: var(--subtle);
    font-size: 0.86rem;
    margin: 0;
    line-height: 1.6;
    font-weight: 400;
  }

  /* ── SCROLLBAR ── */
  ::-webkit-scrollbar { width: 5px; }
  ::-webkit-scrollbar-track { background: var(--bg); }
  ::-webkit-scrollbar-thumb { background: var(--surface2); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ─── DATA GENERATION ─────────────────────────────────────────────────────────
@st.cache_data
def generate_data(n=1000):
    random.seed(42)
    np.random.seed(42)

    industries = ["Technology", "Finance", "Healthcare", "Retail", "Manufacturing", "Logistics", "Education"]
    regions    = ["North", "South", "East", "West", "Central"]
    issues     = ["Billing Dispute", "Technical Failure", "Account Access", "Service Delay", "Data Loss", "Integration Error"]
    clients    = [
        "TechNova Corp", "AlphaFinance", "MedCore Labs", "RetailPro Inc", "ManufactX Ltd",
        "FastLog Systems", "EduHub Global", "DataStream Co", "CloudBridge", "PrimeSolutions",
        "Vertex Analytics", "BlueSky Retail", "Nexus Finance", "CoreHealth", "LogiMaster",
    ]

    base_date = datetime(2024, 1, 1)
    dates = [base_date + timedelta(days=random.randint(0, 364)) for _ in range(n)]

    issue_resolution = {
        "Billing Dispute":    (8, 3),
        "Technical Failure":  (12, 4),
        "Account Access":     (4,  2),
        "Service Delay":      (6,  2),
        "Data Loss":          (15, 5),
        "Integration Error":  (10, 3),
    }

    data = []
    for i in range(n):
        industry = random.choice(industries)
        region   = random.choice(regions)
        issue    = random.choice(issues)
        mu_res, sd_res = issue_resolution[issue]
        res_time   = max(1, round(np.random.normal(mu_res, sd_res), 1))
        resp_time  = max(0.5, round(np.random.normal(res_time * 0.3, 1), 1))
        sat_base   = 4.5 - (resp_time * 0.05) - (res_time * 0.02) + np.random.normal(0, 0.5)
        sat_score  = round(np.clip(sat_base, 1, 5), 1)
        data.append({
            "Ticket_ID":        f"TKT-{1000+i:04d}",
            "Client_Name":      random.choice(clients),
            "Industry":         industry,
            "Region":           region,
            "Issue_Type":       issue,
            "Response_Time":    resp_time,
            "Resolution_Time":  res_time,
            "Satisfaction_Score": sat_score,
            "Date":             dates[i],
            "Month":            dates[i].strftime("%b"),
            "MonthNum":         dates[i].month,
        })
    return pd.DataFrame(data)

df_full = generate_data(1000)

# ─── PLOTLY THEME ────────────────────────────────────────────────────────────
COLORS   = ["#4F7FBF", "#C9A84C", "#3D8C7A", "#8A6FBF", "#C0695A", "#6B8FA3"]
BG       = "rgba(0,0,0,0)"
GRIDCOL  = "rgba(255,255,255,0.05)"
FONTCOL  = "#6B7280"
TITLECOL = "#E8EAF0"

def base_layout(**kwargs):
    base = dict(
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(family="Plus Jakarta Sans", color=FONTCOL, size=12),
        margin=dict(l=10, r=10, t=40, b=10),
    )
    # Only set default legend if caller didn't supply one
    if "legend" not in kwargs:
        base["legend"] = dict(bgcolor="rgba(0,0,0,0)", font=dict(color=FONTCOL))
    base.update(kwargs)
    return base

def style_axes(fig, rows=1, cols=1):
    ax_style = dict(
        gridcolor=GRIDCOL,
        linecolor="rgba(255,255,255,0.1)",
        tickfont=dict(color=FONTCOL),
        title_font=dict(color=FONTCOL),
        zerolinecolor="rgba(255,255,255,0.08)"
    )
    for r in range(1, rows+1):
        for c in range(1, cols+1):
            suffix = "" if (r == 1 and c == 1) else f"{(r-1)*cols+c}"
            try: fig.update_xaxes(selector=dict(), **ax_style)
            except: pass
            try: fig.update_yaxes(selector=dict(), **ax_style)
            except: pass
    fig.update_xaxes(**ax_style)
    fig.update_yaxes(**ax_style)
    return fig


# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
  <div class="header-left">
    <p class="header-title">B2B Support Analytics Dashboard</p>
    <p class="header-sub">AI-Based Customer Support Automation &amp; Service Analytics</p>
  </div>
  <div class="header-right">
    <div class="group-badge">
      <div class="grp-name">Group 2 &nbsp;·&nbsp; BBA Rhinos &nbsp;·&nbsp; Semester 4</div>
      <div class="members">
        Mohnish Singh Patwal &nbsp;&nbsp;Shreyas Kandi<br>
        Nihal S Talampally &nbsp;&nbsp;Akash Krishna
      </div>
    </div>
    <div class="logo-box">Jain<span>University</span></div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─── SIDEBAR FILTERS ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="
        background: #1C2333;
        border: 1px solid rgba(201,168,76,0.3);
        border-radius: 10px;
        padding: 1.2rem 1rem;
        margin-bottom: 1.4rem;
        text-align: center;
    ">
        <div style="
            font-family: 'Fraunces', serif;
            font-size: 1.6rem;
            font-weight: 600;
            color: #C9A84C;
            line-height: 1;
            letter-spacing: -0.5px;
        ">Jain</div>
        <div style="
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 0.58rem;
            letter-spacing: 3px;
            color: #6B7280;
            text-transform: uppercase;
            margin-top: 3px;
        ">University</div>
        <div style="
            width: 36px;
            height: 1px;
            background: rgba(201,168,76,0.35);
            margin: 10px auto;
        "></div>
        <div style="
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 0.65rem;
            color: #9CA3AF;
            font-weight: 500;
            line-height: 1.6;
        ">B2B Support Analytics<br>
        <span style='color:#6B7280;font-size:0.60rem;'>Applied Programming Tools</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("## 🔍 Filters")
    st.markdown("---")

    all_regions   = sorted(df_full["Region"].unique())
    all_industries = sorted(df_full["Industry"].unique())
    all_issues    = sorted(df_full["Issue_Type"].unique())

    sel_regions    = st.multiselect("Region",     all_regions,    default=[],
                                    placeholder="All regions")
    sel_industries = st.multiselect("Industry",   all_industries, default=[],
                                    placeholder="All industries")
    sel_issues     = st.multiselect("Issue Type", all_issues,     default=[],
                                    placeholder="All issue types")

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.72rem;color:#475569;line-height:1.7">
    <b style="color:#64748B">DATASET</b><br>
    1,000 synthetic B2B support tickets<br>
    Jan–Dec 2024<br><br>
    <b style="color:#64748B">COURSE</b><br>
    Applied Programming Tools<br>for B2B Business
    </div>
    """, unsafe_allow_html=True)

# ─── FILTER DATA ─────────────────────────────────────────────────────────────
# Empty selection = no filter applied (show all data)
region_filter   = sel_regions    if sel_regions    else all_regions
industry_filter = sel_industries if sel_industries else all_industries
issue_filter    = sel_issues     if sel_issues     else all_issues

df = df_full[
    df_full["Region"].isin(region_filter) &
    df_full["Industry"].isin(industry_filter) &
    df_full["Issue_Type"].isin(issue_filter)
].copy()

if df.empty:
    st.warning("No data matches the selected filters. Please adjust your selections.")
    st.stop()

# ─── KPI CARDS ───────────────────────────────────────────────────────────────
total_tickets  = len(df)
avg_resp       = df["Response_Time"].mean()
avg_res        = df["Resolution_Time"].mean()
avg_sat        = df["Satisfaction_Score"].mean()

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card blue">
      <span class="kpi-icon">🎫</span>
      <div class="kpi-value">{total_tickets:,}</div>
      <div class="kpi-label">Total Tickets</div>
      <span class="kpi-delta up">↑ Active Pipeline</span>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card teal">
      <span class="kpi-icon">⚡</span>
      <div class="kpi-value">{avg_resp:.1f}h</div>
      <div class="kpi-label">Avg Response Time</div>
      <span class="kpi-delta {'up' if avg_resp < 4 else 'down'}">
        {'✓ Within SLA' if avg_resp < 4 else '⚠ Above Target'}
      </span>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card amber">
      <span class="kpi-icon">🔧</span>
      <div class="kpi-value">{avg_res:.1f}h</div>
      <div class="kpi-label">Avg Resolution Time</div>
      <span class="kpi-delta {'up' if avg_res < 10 else 'down'}">
        {'✓ Efficient' if avg_res < 10 else '⚠ Needs Improvement'}
      </span>
    </div>""", unsafe_allow_html=True)

with k4:
    stars = "★" * int(round(avg_sat)) + "☆" * (5 - int(round(avg_sat)))
    st.markdown(f"""
    <div class="kpi-card coral">
      <span class="kpi-icon">😊</span>
      <div class="kpi-value">{avg_sat:.2f}</div>
      <div class="kpi-label">Satisfaction Score</div>
      <span class="kpi-delta {'up' if avg_sat >= 3.5 else 'down'}">
        {stars}
      </span>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊  Overview",
    "🌍  Regional Analysis",
    "⏱  Time & Resolution",
    "💡  Insights"
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    col_a, col_b = st.columns([1.1, 0.9])

    # --- Tickets by Region (horizontal bar) ---
    with col_a:
        st.markdown('<div class="section-title">Tickets by Region</div>', unsafe_allow_html=True)
        reg_data = df.groupby("Region").size().reset_index(name="Count").sort_values("Count")
        fig_reg = go.Figure(go.Bar(
            x=reg_data["Count"], y=reg_data["Region"],
            orientation="h",
            marker=dict(
                color=reg_data["Count"],
                colorscale=[[0,"#1E3A5F"],[0.5,"#2563EB"],[1,"#06B6D4"]],
                showscale=False,
                line=dict(width=0)
            ),
            text=reg_data["Count"],
            textposition="outside",
            textfont=dict(color="#E2E8F0", size=12)
        ))
        fig_reg.update_layout(**base_layout(height=280, title=dict(text="", x=0.5)))
        fig_reg = style_axes(fig_reg)
        st.plotly_chart(fig_reg, use_container_width=True)

    # --- Issue Type Donut ---
    with col_b:
        st.markdown('<div class="section-title">Issue Type Distribution</div>', unsafe_allow_html=True)
        iss_data = df.groupby("Issue_Type").size().reset_index(name="Count")
        fig_donut = go.Figure(go.Pie(
            labels=iss_data["Issue_Type"],
            values=iss_data["Count"],
            hole=0.55,
            marker=dict(colors=COLORS, line=dict(color="#070E1C", width=2)),
            textinfo="percent",
            textfont=dict(size=11, color="#E2E8F0"),
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>"
        ))
        fig_donut.add_annotation(
            text=f"<b>{total_tickets}</b><br><span style='font-size:10px'>tickets</span>",
            x=0.5, y=0.5, font_size=18, showarrow=False,
            font=dict(color="#E2E8F0")
        )
        fig_donut.update_layout(**base_layout(height=280,
            legend=dict(orientation="v", x=1.0, y=0.5, bgcolor="rgba(0,0,0,0)", font=dict(color="#94A3B8"))))
        st.plotly_chart(fig_donut, use_container_width=True)

    # --- Satisfaction by Industry (heatmap-style grouped bar) ---
    st.markdown('<div class="section-title">Satisfaction Score by Industry</div>', unsafe_allow_html=True)
    ind_sat = df.groupby("Industry")["Satisfaction_Score"].mean().reset_index().sort_values("Satisfaction_Score", ascending=False)
    fig_ind = go.Figure(go.Bar(
        x=ind_sat["Industry"],
        y=ind_sat["Satisfaction_Score"],
        marker=dict(
            color=ind_sat["Satisfaction_Score"],
            colorscale=[[0,"#1E3A5F"],[0.4,"#2563EB"],[0.7,"#06B6D4"],[1,"#10B981"]],
            showscale=True,
            colorbar=dict(
                tickfont=dict(color="#64748B"),
                title=dict(text="Score", font=dict(color="#64748B")),
                len=0.8
            ),
            line=dict(width=0)
        ),
        text=ind_sat["Satisfaction_Score"].round(2),
        textposition="outside",
        textfont=dict(color="#E2E8F0"),
    ))
    fig_ind.update_layout(**base_layout(height=300))
    fig_ind = style_axes(fig_ind)
    fig_ind.update_yaxes(range=[0, 5.5])
    st.plotly_chart(fig_ind, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — REGIONAL ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-title">Avg Satisfaction by Region</div>', unsafe_allow_html=True)
        reg_sat = df.groupby("Region")["Satisfaction_Score"].mean().reset_index().sort_values("Satisfaction_Score", ascending=False)
        fig_rs = go.Figure(go.Bar(
            x=reg_sat["Region"], y=reg_sat["Satisfaction_Score"],
            marker=dict(color=COLORS[:len(reg_sat)], line=dict(width=0)),
            text=reg_sat["Satisfaction_Score"].round(2),
            textposition="outside",
            textfont=dict(color="#E2E8F0")
        ))
        fig_rs.update_layout(**base_layout(height=300))
        fig_rs = style_axes(fig_rs)
        fig_rs.update_yaxes(range=[0, 5.5])
        st.plotly_chart(fig_rs, use_container_width=True)

    with c2:
        st.markdown('<div class="section-title">Avg Resolution Time by Region</div>', unsafe_allow_html=True)
        reg_rt = df.groupby("Region")["Resolution_Time"].mean().reset_index().sort_values("Resolution_Time")
        fig_rrt = go.Figure(go.Bar(
            x=reg_rt["Region"], y=reg_rt["Resolution_Time"],
            marker=dict(
                color=reg_rt["Resolution_Time"],
                colorscale=[[0,"#10B981"],[0.5,"#F59E0B"],[1,"#F43F5E"]],
                showscale=False,
                line=dict(width=0)
            ),
            text=reg_rt["Resolution_Time"].round(1),
            textposition="outside",
            textfont=dict(color="#E2E8F0")
        ))
        fig_rrt.update_layout(**base_layout(height=300))
        fig_rrt = style_axes(fig_rrt)
        st.plotly_chart(fig_rrt, use_container_width=True)

    # Stacked bar: issue type breakdown per region
    st.markdown('<div class="section-title">Issue Type Breakdown by Region</div>', unsafe_allow_html=True)
    pivot = df.groupby(["Region","Issue_Type"]).size().reset_index(name="Count")
    fig_stack = px.bar(
        pivot, x="Region", y="Count", color="Issue_Type",
        color_discrete_sequence=COLORS,
        barmode="stack"
    )
    fig_stack.update_layout(**base_layout(height=320,
        legend=dict(orientation="h", y=-0.15, bgcolor="rgba(0,0,0,0)", font=dict(color="#94A3B8"))))
    fig_stack = style_axes(fig_stack)
    fig_stack.update_traces(marker_line_width=0)
    st.plotly_chart(fig_stack, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — TIME & RESOLUTION
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    # Monthly trend
    st.markdown('<div class="section-title">Resolution Time Trend (Monthly Avg)</div>', unsafe_allow_html=True)
    monthly = df.groupby("MonthNum").agg(
        Avg_Resolution=("Resolution_Time","mean"),
        Avg_Response=("Response_Time","mean"),
        Month=("Month","first")
    ).reset_index().sort_values("MonthNum")

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=monthly["Month"], y=monthly["Avg_Resolution"],
        mode="lines+markers",
        name="Avg Resolution Time",
        line=dict(color="#06B6D4", width=2.5),
        marker=dict(size=7, color="#06B6D4"),
        fill="tozeroy",
        fillcolor="rgba(6,182,212,0.08)"
    ))
    fig_trend.add_trace(go.Scatter(
        x=monthly["Month"], y=monthly["Avg_Response"],
        mode="lines+markers",
        name="Avg Response Time",
        line=dict(color="#F59E0B", width=2, dash="dot"),
        marker=dict(size=6, color="#F59E0B"),
    ))
    fig_trend.update_layout(**base_layout(height=320,
        legend=dict(orientation="h", y=1.12, bgcolor="rgba(0,0,0,0)")))
    fig_trend = style_axes(fig_trend)
    st.plotly_chart(fig_trend, use_container_width=True)

    c1, c2 = st.columns(2)

    with c1:
        # Resolution time by Issue Type (box)
        st.markdown('<div class="section-title">Resolution Time by Issue Type</div>', unsafe_allow_html=True)
        fig_box = go.Figure()
        for i, issue in enumerate(df["Issue_Type"].unique()):
            sub = df[df["Issue_Type"] == issue]["Resolution_Time"]
            fig_box.add_trace(go.Box(
                y=sub, name=issue,
                marker_color=COLORS[i % len(COLORS)],
                line=dict(width=1.5),
                boxmean=True
            ))
        fig_box.update_layout(**base_layout(height=340,
            legend=dict(orientation="h", y=-0.2, font=dict(color="#94A3B8", size=10))))
        fig_box = style_axes(fig_box)
        st.plotly_chart(fig_box, use_container_width=True)

    with c2:
        # Scatter: Response Time vs Satisfaction
        st.markdown('<div class="section-title">Response Time vs Satisfaction</div>', unsafe_allow_html=True)
        sample = df.sample(min(300, len(df)), random_state=42)
        fig_scatter = px.scatter(
            sample, x="Response_Time", y="Satisfaction_Score",
            color="Issue_Type",
            color_discrete_sequence=COLORS,
            opacity=0.55,
        )
        fig_scatter.update_traces(marker=dict(size=6))
        # Manual trendline via numpy - no statsmodels needed
        _x = sample["Response_Time"].values
        _y = sample["Satisfaction_Score"].values
        _m, _b = np.polyfit(_x, _y, 1)
        _xl = np.linspace(_x.min(), _x.max(), 100)
        fig_scatter.add_trace(go.Scatter(
            x=_xl, y=_m * _xl + _b,
            mode="lines", name="Trend",
            line=dict(color="#C9A84C", width=2, dash="dot"),
            showlegend=True
        ))
        fig_scatter.update_layout(**base_layout(height=340,
            legend=dict(orientation="h", y=-0.2, font=dict(color="#94A3B8", size=10))))
        fig_scatter = style_axes(fig_scatter)
        st.plotly_chart(fig_scatter, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — INSIGHTS
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    # Compute insights
    slowest_issue = df.groupby("Issue_Type")["Resolution_Time"].mean().idxmax()
    slowest_time  = df.groupby("Issue_Type")["Resolution_Time"].mean().max()
    best_region   = df.groupby("Region")["Satisfaction_Score"].mean().idxmax()
    best_sat      = df.groupby("Region")["Satisfaction_Score"].mean().max()
    corr          = df["Response_Time"].corr(df["Satisfaction_Score"])

    ia, ib = st.columns(2)

    with ia:
        st.markdown('<div class="section-title">📌 Key Findings</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="insight-card">
          <h4>🐢 Slowest Issue Type</h4>
          <p><b style="color:#F59E0B">{slowest_issue}</b> has the longest average resolution time of
          <b style="color:#F59E0B">{slowest_time:.1f} hours</b>. This issue type requires specialised
          technical intervention, often spanning multiple teams.</p>
        </div>
        <div class="insight-card">
          <h4>🏆 Highest Satisfaction Region</h4>
          <p><b style="color:#10B981">{best_region}</b> region leads with an average satisfaction score of
          <b style="color:#10B981">{best_sat:.2f}/5.0</b>. Stronger local support teams and faster escalation
          paths likely drive this outcome.</p>
        </div>
        <div class="insight-card">
          <h4>🔗 Response Time vs Satisfaction</h4>
          <p>Correlation coefficient: <b style="color:#06B6D4">{corr:.3f}</b>.
          {'There is a meaningful negative correlation — faster responses lead to noticeably higher satisfaction scores.' if corr < -0.1 else
           'A slight negative trend suggests response speed has moderate impact on satisfaction.'}
          Each hour saved in response time measurably improves customer experience.</p>
        </div>
        """, unsafe_allow_html=True)

    with ib:
        st.markdown('<div class="section-title">🚀 Recommendations</div>', unsafe_allow_html=True)
        recs = [
            ("1. Prioritise High-Complexity Issues",
             f"Implement a dedicated fast-track queue for '{slowest_issue}' tickets. Assign senior engineers directly and set automated escalation at the 6-hour mark to prevent SLA breaches."),
            ("2. Replicate Best Practices from Top Region",
             f"Conduct a knowledge-transfer workshop from the {best_region} support team. Document their escalation protocols, communication templates, and shift schedules for rollout across all regions."),
            ("3. Automate First-Response with AI",
             "Deploy a Make.com + AI workflow to send an intelligent auto-response within 15 minutes of ticket submission. This sets clear expectations, reduces perceived wait time, and boosts satisfaction scores even before human intervention begins."),
        ]
        for title, body in recs:
            st.markdown(f"""
            <div class="insight-card">
              <h4>{title}</h4>
              <p>{body}</p>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Satisfaction distribution heatmap
    st.markdown('<div class="section-title">Satisfaction Heatmap — Region × Issue Type</div>', unsafe_allow_html=True)
    heat_data = df.groupby(["Region","Issue_Type"])["Satisfaction_Score"].mean().reset_index()
    heat_pivot = heat_data.pivot(index="Region", columns="Issue_Type", values="Satisfaction_Score")
    fig_heat = go.Figure(go.Heatmap(
        z=heat_pivot.values,
        x=heat_pivot.columns.tolist(),
        y=heat_pivot.index.tolist(),
        colorscale=[[0,"#1E3A5F"],[0.4,"#2563EB"],[0.7,"#06B6D4"],[1,"#10B981"]],
        text=np.round(heat_pivot.values, 2),
        texttemplate="%{text}",
        textfont=dict(color="#E2E8F0", size=12),
        hoverongaps=False,
        colorbar=dict(tickfont=dict(color="#64748B"), title=dict(text="Score", font=dict(color="#64748B")))
    ))
    fig_heat.update_layout(**base_layout(height=320))
    fig_heat.update_xaxes(tickfont=dict(color="#94A3B8"))
    fig_heat.update_yaxes(tickfont=dict(color="#94A3B8"))
    st.plotly_chart(fig_heat, use_container_width=True)

# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2rem 0 0.5rem;border-top:1px solid rgba(255,255,255,0.06);
  margin-top:2rem;color:#334155;font-size:0.75rem;">
  B2B Support Analytics Dashboard &nbsp;·&nbsp; Group 2 · BBA Rhinos · Semester 4 &nbsp;·&nbsp;
  Jain University &nbsp;·&nbsp; Applied Programming Tools for B2B Business
</div>
""", unsafe_allow_html=True)