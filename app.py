
from __future__ import annotations

import io
import math
from dataclasses import dataclass

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Mastering Returns | Mountain Path Academy",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

NAVY = "#0B2545"
BLUE = "#0B5CAD"
GOLD = "#F3C84B"
DARK_GOLD = "#D4A017"
TEAL = "#13A89E"
GREEN = "#2E8B57"
RED = "#E45756"
PURPLE = "#7C3AED"
ORANGE = "#F28E2B"
SKY = "#5DA5DA"
PALETTE = [BLUE, TEAL, ORANGE, RED, PURPLE, GREEN, SKY, DARK_GOLD]


st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] {font-family:'Inter',sans-serif}
.stApp {background:linear-gradient(180deg,#F8FAFD 0%,#EAF1F7 100%)}
[data-testid="stSidebar"] {background:linear-gradient(180deg,#081F3A,#124A78)}
[data-testid="stSidebar"] {color:#F7FAFC}
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,[data-testid="stSidebar"] li,[data-testid="stSidebar"] small {
 color:#F7FAFC;
}
.hero {background:linear-gradient(120deg,#071A2F 0%,#0B3B67 58%,#A97908 145%);
 padding:30px 34px;border-radius:22px;color:white;box-shadow:0 14px 34px rgba(7,26,47,.22);
 margin-bottom:16px;border:1px solid rgba(243,200,75,.35)}
.hero h1 {font-size:2.25rem;margin:0 0 8px;color:white;font-weight:900}
.hero p {margin:0;color:#DDEAF4;font-size:1.02rem;line-height:1.55}
.eyebrow {color:#F3C84B;text-transform:uppercase;letter-spacing:.14em;font-weight:900;font-size:.76rem;margin-bottom:.55rem}
.section-title {font-size:1.42rem;font-weight:900;color:#0B2545;margin:18px 0 8px}
.sub-title {font-size:1.08rem;font-weight:800;color:#0B3B67;margin:12px 0 6px}
.concept-card {background:white;border:1px solid #D9E5EF;border-top:5px solid #0B5CAD;
 padding:17px 18px;border-radius:15px;box-shadow:0 5px 16px rgba(18,54,84,.07);min-height:145px}
.concept-card h3 {color:#0B2545;font-size:1.05rem;margin:0 0 7px}
.concept-card p {color:#3C5368;font-size:.91rem;line-height:1.45;margin:0}
.formula {background:linear-gradient(135deg,#FFF9E6,#FFF1B8);border:1px solid #E8C45B;
 border-left:6px solid #D4A017;padding:14px 18px;border-radius:12px;color:#3D3006;
 font-weight:800;font-size:1.04rem;margin:8px 0 14px}
.teaching-note {background:#EAF7F5;border-left:5px solid #13A89E;padding:13px 16px;
 border-radius:10px;color:#153C3A;margin:10px 0}
.warning-note {background:#FFF3E8;border-left:5px solid #F28E2B;padding:13px 16px;
 border-radius:10px;color:#57300A;margin:10px 0}
.result-box {background:linear-gradient(135deg,#0B2545,#0B5CAD);padding:16px 18px;border-radius:14px;
 color:white;box-shadow:0 7px 18px rgba(11,37,69,.18)}
.result-box .label {font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;color:#CFE4F5}
.result-box .value {font-size:1.7rem;font-weight:900;color:#F3C84B;margin-top:4px}
.profile-card {background:rgba(255,255,255,.09);border:1px solid rgba(243,200,75,.45);
 padding:16px;border-radius:14px;margin-top:12px}
.profile-card h3 {color:#F3C84B!important;margin:0 0 5px;font-size:1.05rem}
.profile-card p {font-size:.82rem;line-height:1.45;margin:4px 0;color:#EEF7FC!important}
.footer {background:linear-gradient(115deg,#081F3A,#124A78);color:#E6F1F8;padding:22px;
 border-radius:16px;margin-top:28px;text-align:center;border-top:4px solid #F3C84B}
.footer a {color:#F3C84B!important;text-decoration:none;font-weight:800}
.footer-links {display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin:16px 0 6px}
.footer-links a {display:inline-block;background:linear-gradient(135deg,#F3C84B,#D4A017)!important;
 color:#071A2F!important;-webkit-text-fill-color:#071A2F!important;border:2px solid #FFF1AC;
 border-radius:10px;padding:10px 18px;text-decoration:none!important;font-weight:900!important;
 box-shadow:0 5px 14px rgba(0,0,0,.22)}
.footer-links a:hover {background:#FFF1AC!important;transform:translateY(-1px)}
[data-testid="stMetric"] {background:#FFF;border:1px solid #DDE8F1;padding:13px;border-radius:14px;
 box-shadow:0 5px 14px rgba(18,54,84,.06)}
.stTabs [data-baseweb="tab-list"] {gap:9px!important;flex-wrap:wrap!important;background:#D8E3ED!important;
 padding:10px!important;border:1px solid #B9CAD9!important;border-radius:14px!important}
.stTabs button[data-baseweb="tab"] {flex:1 1 175px!important;min-width:155px!important;min-height:52px!important;
 justify-content:center!important;white-space:normal!important;text-align:center!important;background:#0B2545!important;
 border:2px solid #F3C84B!important;border-radius:10px!important;padding:9px 12px!important;color:#F3C84B!important}
.stTabs button[data-baseweb="tab"] p {color:#F3C84B!important;-webkit-text-fill-color:#F3C84B!important;
 font-size:.89rem!important;line-height:1.15!important;font-weight:850!important}
.stTabs button[data-baseweb="tab"][aria-selected="true"] {background:linear-gradient(135deg,#F3C84B,#D4A017)!important;
 border-color:#A97908!important;box-shadow:0 4px 12px rgba(169,121,8,.35)!important}
.stTabs button[data-baseweb="tab"][aria-selected="true"] p {color:#071A2F!important;-webkit-text-fill-color:#071A2F!important;font-weight:900!important}
.stTabs [data-baseweb="tab-highlight"] {display:none!important}
.stButton button,.stDownloadButton button {background:#0B3B67!important;color:white!important;border:1px solid #0B3B67!important;
 border-radius:10px!important;font-weight:800!important;min-height:42px}
.stButton button:hover,.stDownloadButton button:hover {background:#D4A017!important;color:#071A2F!important;border-color:#D4A017!important}
[data-testid="stLinkButton"] a {background:#0B3B67!important;color:white!important;border:2px solid #F3C84B!important;
 border-radius:10px!important;font-weight:850!important;min-height:42px!important;text-decoration:none!important}
[data-testid="stLinkButton"] a:hover {background:#D4A017!important;color:#071A2F!important;border-color:#FFF1AC!important}
[data-testid="stLinkButton"] a p {color:inherit!important;-webkit-text-fill-color:inherit!important;font-weight:850!important}
section[data-testid="stSidebar"] a:not([data-testid]) {
 color:#F3C84B!important;-webkit-text-fill-color:#F3C84B!important;font-weight:850!important;
 text-decoration:underline!important;text-decoration-color:#F3C84B!important;
}
section[data-testid="stSidebar"] a:not([data-testid]):hover {
 color:#FFF1AC!important;-webkit-text-fill-color:#FFF1AC!important;
}
section[data-testid="stSidebar"] label p {color:#F3C84B!important;font-weight:850!important}
section[data-testid="stSidebar"] div[data-testid="stButton"] button {background:linear-gradient(135deg,#F3C84B,#D4A017)!important;
 color:#071A2F!important;border:2px solid #F9DC79!important;font-weight:900!important;min-height:46px}
section[data-testid="stSidebar"] div[data-testid="stButton"] button p {color:#071A2F!important;-webkit-text-fill-color:#071A2F!important}
/* Sidebar selectboxes: keep the closed selected value visible on its white field */
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
 background:#FFFFFF!important;border:2px solid #F3C84B!important;border-radius:10px!important;
}
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [data-baseweb="select"] *,
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [role="combobox"],
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [role="combobox"] *,
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] input {
 color:#0B2545!important;-webkit-text-fill-color:#0B2545!important;opacity:1!important;font-weight:800!important;
 text-shadow:none!important;
}
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [data-baseweb="select"] svg {
 fill:#0B2545!important;color:#0B2545!important;
}
div[data-testid="stSelectbox"] [data-baseweb="select"]>div {background:#FFF!important;border:2px solid #0B3B67!important;border-radius:10px!important}
div[data-testid="stSelectbox"] [data-baseweb="select"] * {color:#0B2545!important;-webkit-text-fill-color:#0B2545!important;font-weight:750!important}
[data-baseweb="popover"] [role="option"] {color:#0B2545!important;-webkit-text-fill-color:#0B2545!important;background:white!important}
[data-baseweb="popover"] [role="option"]:hover,[data-baseweb="popover"] [aria-selected="true"] {background:#0B3B67!important;color:white!important;-webkit-text-fill-color:white!important}
@media (max-width:700px){.hero{padding:22px}.hero h1{font-size:1.7rem}.stTabs button[data-baseweb="tab"]{flex-basis:145px!important}}
</style>
""",
    unsafe_allow_html=True,
)


def pct(x: float, digits: int = 2) -> str:
    return "—" if x is None or not np.isfinite(x) else f"{x:.{digits}%}"


def money(x: float) -> str:
    return f"₹{x:,.2f}"


def metric_box(label: str, value: str) -> None:
    st.markdown(
        f"<div class='result-box'><div class='label'>{label}</div><div class='value'>{value}</div></div>",
        unsafe_allow_html=True,
    )


def section(title: str) -> None:
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)


def teaching_note(text: str, warning: bool = False) -> None:
    cls = "warning-note" if warning else "teaching-note"
    st.markdown(f"<div class='{cls}'>{text}</div>", unsafe_allow_html=True)


def style_fig(fig: go.Figure, height: int = 420) -> go.Figure:
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="white",
        font=dict(family="Inter", color=NAVY),
        title_font=dict(size=19, color=NAVY),
        legend_title_text="",
        margin=dict(l=30, r=25, t=60, b=35),
        hoverlabel=dict(bgcolor="white", font_color=NAVY),
    )
    fig.update_xaxes(gridcolor="#E7EEF4", linecolor="#BFCEDB")
    fig.update_yaxes(gridcolor="#E7EEF4", linecolor="#BFCEDB")
    return fig


def geometric_mean(returns: np.ndarray) -> float:
    if len(returns) == 0 or np.any(returns <= -1):
        return np.nan
    return float(np.prod(1 + returns) ** (1 / len(returns)) - 1)


def harmonic_growth_mean(returns: np.ndarray) -> float:
    relatives = 1 + returns
    if len(relatives) == 0 or np.any(relatives <= 0):
        return np.nan
    return float(len(relatives) / np.sum(1 / relatives) - 1)


def irr(cashflows: list[float]) -> float:
    """Robust educational IRR solver for evenly spaced cash flows."""
    def npv(rate: float) -> float:
        return sum(cf / ((1 + rate) ** i) for i, cf in enumerate(cashflows))

    grid = np.concatenate((np.linspace(-0.999, -0.5, 120), np.linspace(-0.5, 5.0, 1200)))
    previous_rate, previous_value = grid[0], npv(grid[0])
    for rate in grid[1:]:
        value = npv(rate)
        if value == 0:
            return float(rate)
        if np.sign(value) != np.sign(previous_value):
            lo, hi = previous_rate, rate
            for _ in range(100):
                mid = (lo + hi) / 2
                vm = npv(mid)
                if abs(vm) < 1e-11:
                    return float(mid)
                if np.sign(vm) == np.sign(npv(lo)):
                    lo = mid
                else:
                    hi = mid
            return float((lo + hi) / 2)
        previous_rate, previous_value = rate, value
    return np.nan


def concept_card(title: str, body: str, color: str = BLUE) -> str:
    return (
        f"<div class='concept-card' style='border-top-color:{color}'>"
        f"<h3>{title}</h3><p>{body}</p></div>"
    )


with st.sidebar:
    st.markdown("## 📈 Mastering Returns")
    st.caption("An interactive finance learning studio")
    level = st.selectbox("Learning level", ["Foundation", "MBA / Professional", "Advanced revision"])
    show_excel = st.toggle("Show Excel equivalents", value=True)
    st.markdown("---")
    st.markdown("### Suggested journey")
    st.markdown("1. Learn the map\n2. Build HPR\n3. Compare means\n4. Explore scenarios\n5. Separate TWR and MWR\n6. Take the quiz")
    if st.button("↻ Reset learning session", use_container_width=True):
        for key in list(st.session_state):
            if key.startswith(("quiz_", "practice_")):
                del st.session_state[key]
        st.rerun()
    st.markdown(
        """
<div class='profile-card'>
<h3>Prof. V. Ravichandran</h3>
<p>Visiting Professor & Professor of Practice<br>Founder — The Mountain Path Academy</p>
<p>Financial Analytics · Risk Management · Derivatives · Portfolio Management</p>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown("### Connect")
    st.link_button("🌐 Mountain Path Academy", "https://themountainpathacademy.com/", use_container_width=True)
    st.link_button("in  Prof. V. Ravichandran — LinkedIn", "https://www.linkedin.com/in/trichyravis/", use_container_width=True)
    st.link_button("⌂  GitHub — trichyravis", "https://github.com/trichyravis", use_container_width=True)


st.markdown(
    """
<div class="hero">
  <div class="eyebrow">The Mountain Path Academy · Interactive Finance Lab</div>
  <h1>Mastering Returns</h1>
  <p>Learn what each return measure answers, calculate it, visualise it, compare it,
  interpret it and test your understanding—from holding-period return to TWR and MWR.</p>
</div>
""",
    unsafe_allow_html=True,
)

top1, top2, top3, top4 = st.columns(4)
top1.metric("Concepts", "9", "Workbook-aligned")
top2.metric("Interactive Labs", "6", "Change every input")
top3.metric("Worked Examples", "12+", "Step-by-step")
top4.metric("Knowledge Check", "10 MCQs", "Instant feedback")

tabs = st.tabs(
    [
        "🧭 Learning Map",
        "💰 HPR & Annualisation",
        "⚖️ Means Laboratory",
        "🚀 CAGR Explorer",
        "🎯 Expected Return",
        "🔬 Log Returns",
        "⏱️ TWR vs MWR",
        "🧩 Practice Studio",
        "🏆 Quiz",
        "📚 Formula Library",
    ]
)


with tabs[0]:
    section("The central question: What exactly are you trying to measure?")
    st.markdown(
        "A return is not just one number. The correct measure depends on the **time horizon**, "
        "**cash-flow pattern**, **data available**, and **decision being made**."
    )
    cols = st.columns(3)
    cards = [
        ("Holding Period Return", "Income plus price change during one holding period. Start here.", BLUE),
        ("CAGR", "One smooth annual compound rate between a beginning and ending value.", TEAL),
        ("Arithmetic Mean", "Best single-period estimate from a historical return sample.", ORANGE),
        ("Geometric Mean", "Actual average compound growth across several periods.", PURPLE),
        ("Harmonic Mean", "Best for positive ratios, prices and per-unit averaging—not ordinary returns.", RED),
        ("Expected Return", "Probability-weighted forward-looking return across scenarios.", GREEN),
        ("Log Return", "Additive continuously compounded return used in quantitative finance.", SKY),
        ("TWR", "Manager performance after neutralising investor cash-flow timing.", DARK_GOLD),
        ("MWR / IRR", "The investor's actual experience, sensitive to cash-flow timing.", NAVY),
    ]
    for i, (title, body, color) in enumerate(cards):
        with cols[i % 3]:
            st.markdown(concept_card(title, body, color), unsafe_allow_html=True)
            st.write("")

    section("Choose the right measure")
    question = st.selectbox(
        "What is your question?",
        [
            "What did I earn on one investment including dividends?",
            "What annual rate links a beginning value to an ending value?",
            "What is a reasonable one-period estimate from past returns?",
            "What compound rate did wealth actually grow at across periods?",
            "What return should I expect from economic scenarios?",
            "How do I add returns across many time periods?",
            "How well did the portfolio manager perform despite my cash flows?",
            "What did I personally earn given my contribution timing?",
            "How should I average P/E ratios or unit purchase prices?",
        ],
    )
    answers = {
        question: [
            "Holding Period Return (HPR)",
            "CAGR",
            "Arithmetic Mean",
            "Geometric Mean",
            "Expected Return using probabilities",
            "Log Return",
            "Time-Weighted Return (TWR)",
            "Money-Weighted Return (MWR / IRR / XIRR)",
            "Harmonic Mean",
        ][
            [
                "What did I earn on one investment including dividends?",
                "What annual rate links a beginning value to an ending value?",
                "What is a reasonable one-period estimate from past returns?",
                "What compound rate did wealth actually grow at across periods?",
                "What return should I expect from economic scenarios?",
                "How do I add returns across many time periods?",
                "How well did the portfolio manager perform despite my cash flows?",
                "What did I personally earn given my contribution timing?",
                "How should I average P/E ratios or unit purchase prices?",
            ].index(question)
        ]
    }
    metric_box("Recommended return measure", answers[question])
    teaching_note(
        "<b>Master relationship:</b> for the same positive return relatives, "
        "Arithmetic Mean ≥ Geometric Mean ≥ Harmonic Mean. Equality occurs only when every observation is identical."
    )

    section("A unified return journey")
    journey = pd.DataFrame(
        {
            "Stage": ["Observe", "Measure", "Compare", "Compound", "Attribute"],
            "Question": [
                "What changed?",
                "What did the holding earn?",
                "What is typical?",
                "How did wealth grow?",
                "Who caused the outcome?",
            ],
            "Tool": ["Prices & income", "HPR / Log return", "AM / GM / HM", "CAGR / Annualisation", "TWR vs MWR"],
        }
    )
    fig = px.bar(
        journey,
        x="Stage",
        y=[1] * len(journey),
        text="Tool",
        color="Stage",
        color_discrete_sequence=PALETTE,
        hover_data=["Question"],
        title="From raw price movement to performance attribution",
    )
    fig.update_traces(textposition="inside")
    fig.update_yaxes(visible=False)
    st.plotly_chart(style_fig(fig, 320), use_container_width=True)


with tabs[1]:
    section("Holding Period Return: price change + income")
    st.markdown('<div class="formula">HPR = (P₁ − P₀ + Income) ÷ P₀</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    p0 = c1.number_input("Purchase price (P₀)", min_value=0.01, value=100.0, step=5.0)
    p1 = c2.number_input("Selling price (P₁)", min_value=0.0, value=110.0, step=5.0)
    income = c3.number_input("Dividend / coupon", min_value=0.0, value=5.0, step=1.0)
    days = c4.number_input("Days held", min_value=1, value=365, step=1)
    capital_gain = p1 - p0
    total_gain = capital_gain + income
    hpr = total_gain / p0
    dividend_yield = income / p0
    capital_yield = capital_gain / p0
    annualised = (1 + hpr) ** (365 / days) - 1 if hpr > -1 else np.nan

    r1, r2, r3, r4 = st.columns(4)
    with r1:
        metric_box("Holding Period Return", pct(hpr))
    with r2:
        metric_box("Income Yield", pct(dividend_yield))
    with r3:
        metric_box("Capital Gains Yield", pct(capital_yield))
    with r4:
        metric_box("Annualised Return", pct(annualised))

    left, right = st.columns([1.1, 1])
    with left:
        bridge = go.Figure(
            go.Waterfall(
                orientation="v",
                measure=["absolute", "relative", "relative", "total"],
                x=["Initial Investment", "Price Change", "Income", "Ending Wealth"],
                y=[p0, capital_gain, income, 0],
                text=[money(p0), money(capital_gain), money(income), money(p0 + total_gain)],
                textposition="outside",
                connector={"line": {"color": "#8AA3B7"}},
                increasing={"marker": {"color": TEAL}},
                decreasing={"marker": {"color": RED}},
                totals={"marker": {"color": BLUE}},
            )
        )
        bridge.update_layout(title="Return bridge: where did the gain come from?")
        st.plotly_chart(style_fig(bridge), use_container_width=True)
    with right:
        components = pd.DataFrame(
            {"Component": ["Income yield", "Capital gains yield", "Total HPR"], "Return": [dividend_yield, capital_yield, hpr]}
        )
        fig = px.bar(
            components,
            x="Component",
            y="Return",
            color="Component",
            text=components["Return"].map(lambda x: pct(x)),
            color_discrete_sequence=[GOLD, BLUE, TEAL],
            title="Return decomposition",
        )
        fig.update_traces(textposition="outside")
        fig.update_yaxes(tickformat=".1%")
        st.plotly_chart(style_fig(fig), use_container_width=True)

    if days < 90:
        teaching_note(
            "<b>Annualisation warning:</b> a short-period return is being assumed to repeat for a full year. "
            "The mathematics is correct, but the economic assumption may be unrealistic.",
            warning=True,
        )
    else:
        teaching_note(
            "<b>Interpretation:</b> total return equals income yield plus capital gains yield. "
            "Annualisation makes different holding periods comparable, but it assumes reinvestment and repetition."
        )
    if show_excel:
        st.code(
            "HPR: =(SellingPrice-PurchasePrice+Income)/PurchasePrice\n"
            "Annualised: =(1+HPR)^(365/DaysHeld)-1",
            language="text",
        )

    section("Compounding frequency laboratory")
    pc1, pc2 = st.columns(2)
    periodic_rate = pc1.slider("Periodic return", -10.0, 15.0, 1.5, 0.25) / 100
    frequency = pc2.select_slider("Periods per year", options=[1, 2, 4, 12, 52, 252], value=12)
    effective = (1 + periodic_rate) ** frequency - 1
    nominal = periodic_rate * frequency
    periods = np.arange(frequency + 1)
    wealth = 100 * (1 + periodic_rate) ** periods
    fig = px.line(
        x=periods,
        y=wealth,
        markers=True,
        labels={"x": "Period", "y": "Wealth index"},
        title=f"₹100 grows to ₹{wealth[-1]:.2f}: compounding versus simple annualisation",
    )
    fig.add_hline(y=100 * (1 + nominal), line_dash="dash", line_color=ORANGE, annotation_text="Simple annualised endpoint")
    st.plotly_chart(style_fig(fig), use_container_width=True)
    a, b, c = st.columns(3)
    a.metric("Effective annual return", pct(effective))
    b.metric("Simple annualisation", pct(nominal))
    c.metric("Compounding effect", pct(effective - nominal))


with tabs[2]:
    section("Arithmetic, Geometric and Harmonic Means")
    st.markdown(
        "Edit the return series and observe how volatility changes compound wealth—even when the arithmetic mean stays similar."
    )
    preset = st.selectbox(
        "Teaching preset",
        ["Workbook example", "Volatility drag", "Steady growth", "Boom–bust cycle"],
        key="means_preset",
    )
    presets = {
        "Workbook example": [10, 12, 8, 15, 5],
        "Volatility drag": [40, -30, 35, -25, 30],
        "Steady growth": [10, 10, 10, 10, 10],
        "Boom–bust cycle": [60, -45, 50, -35, 20],
    }
    returns_df = pd.DataFrame({"Period": range(1, 6), "Return (%)": presets[preset]})
    edited = st.data_editor(
        returns_df,
        hide_index=True,
        use_container_width=True,
        num_rows="dynamic",
        column_config={"Return (%)": st.column_config.NumberColumn(min_value=-99.0, max_value=500.0, step=1.0)},
        key=f"means_editor_{preset}",
    )
    returns = pd.to_numeric(edited["Return (%)"], errors="coerce").dropna().to_numpy() / 100
    am = float(np.mean(returns)) if len(returns) else np.nan
    gm = geometric_mean(returns)
    hm = harmonic_growth_mean(returns)
    volatility = float(np.std(returns, ddof=1)) if len(returns) > 1 else 0.0
    terminal = 100 * float(np.prod(1 + returns)) if len(returns) else np.nan

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Arithmetic Mean", pct(am))
    m2.metric("Geometric Mean", pct(gm))
    m3.metric("Harmonic Mean*", pct(hm))
    m4.metric("Volatility Drag (AM − GM)", pct(am - gm))
    st.caption("*Harmonic mean is applied to the positive return relatives (1 + R), then converted back to a rate.")

    left, right = st.columns(2)
    with left:
        compare = pd.DataFrame({"Measure": ["Arithmetic", "Geometric", "Harmonic"], "Return": [am, gm, hm]})
        fig = px.bar(
            compare,
            x="Measure",
            y="Return",
            color="Measure",
            text=compare["Return"].map(pct),
            color_discrete_sequence=[ORANGE, PURPLE, RED],
            title="Same observations, three different questions",
        )
        fig.update_traces(textposition="outside")
        fig.update_yaxes(tickformat=".1%")
        st.plotly_chart(style_fig(fig), use_container_width=True)
    with right:
        actual_path = 100 * np.cumprod(np.r_[1, 1 + returns])
        smooth_path = 100 * (1 + gm) ** np.arange(len(returns) + 1) if np.isfinite(gm) else np.repeat(np.nan, len(returns) + 1)
        wealth_df = pd.DataFrame({"Period": range(len(returns) + 1), "Actual path": actual_path, "GM-equivalent path": smooth_path})
        fig = px.line(
            wealth_df,
            x="Period",
            y=["Actual path", "GM-equivalent path"],
            markers=True,
            title="Geometric mean preserves terminal wealth",
            color_discrete_sequence=[BLUE, GOLD],
        )
        st.plotly_chart(style_fig(fig), use_container_width=True)

    teaching_note(
        f"<b>₹100 terminal wealth:</b> {money(terminal)}. "
        f"The arithmetic mean answers a one-period expectation question; the geometric mean is the constant rate "
        f"that exactly recreates this terminal wealth. Sample volatility is {pct(volatility)}."
    )
    if show_excel:
        st.code(
            "Arithmetic Mean: =AVERAGE(return_range)\n"
            "Geometric Mean: =GEOMEAN(1+return_range)-1\n"
            "Harmonic Mean of relatives: =HARMEAN(1+return_range)-1",
            language="text",
        )

    section("Volatility drag simulator")
    vd1, vd2 = st.columns(2)
    mean_input = vd1.slider("Arithmetic mean return", -5.0, 25.0, 10.0, 0.5) / 100
    vol_input = vd2.slider("Volatility", 0.0, 60.0, 20.0, 1.0) / 100
    approximation = mean_input - 0.5 * vol_input**2
    grid = pd.DataFrame(
        {
            "Volatility": np.linspace(0, 0.6, 61),
        }
    )
    grid["Approx. compound growth"] = mean_input - 0.5 * grid["Volatility"] ** 2
    fig = px.line(
        grid,
        x="Volatility",
        y="Approx. compound growth",
        title="Approximation: geometric growth ≈ arithmetic mean − ½σ²",
    )
    fig.add_scatter(x=[vol_input], y=[approximation], mode="markers", marker=dict(size=15, color=RED), name="Your selection")
    fig.update_xaxes(tickformat=".0%")
    fig.update_yaxes(tickformat=".1%")
    st.plotly_chart(style_fig(fig, 350), use_container_width=True)


with tabs[3]:
    section("CAGR: the smooth annual rate between two endpoints")
    st.markdown('<div class="formula">CAGR = (Ending Value ÷ Beginning Value)^(1 ÷ Years) − 1</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    bv = c1.number_input("Beginning value", min_value=0.01, value=10000.0, step=1000.0, key="cagr_bv")
    ev = c2.number_input("Ending value", min_value=0.01, value=16105.0, step=1000.0, key="cagr_ev")
    n = c3.number_input("Years", min_value=0.1, value=5.0, step=0.5, key="cagr_n")
    cagr = (ev / bv) ** (1 / n) - 1
    total_return = ev / bv - 1
    doubling = math.log(2) / math.log(1 + cagr) if cagr > 0 else np.nan
    r1, r2, r3 = st.columns(3)
    r1.metric("CAGR", pct(cagr))
    r2.metric("Cumulative Return", pct(total_return))
    r3.metric("Doubling Time", f"{doubling:.2f} years" if np.isfinite(doubling) else "Not applicable")

    years = np.linspace(0, n, max(20, int(n * 12) + 1))
    smooth = bv * (1 + cagr) ** years
    path = pd.DataFrame({"Year": years, "CAGR-equivalent wealth": smooth})
    fig = px.area(
        path,
        x="Year",
        y="CAGR-equivalent wealth",
        title="The smooth path implied by CAGR",
        color_discrete_sequence=[TEAL],
    )
    fig.add_scatter(x=[0, n], y=[bv, ev], mode="markers+text", text=[money(bv), money(ev)], textposition="top center", name="Observed endpoints")
    st.plotly_chart(style_fig(fig), use_container_width=True)
    teaching_note(
        "<b>Critical insight:</b> CAGR describes the endpoints, not the journey. Two investments can have the same CAGR "
        "but completely different volatility, drawdowns and investor experience."
    )
    if show_excel:
        st.code("Direct formula: =(EndingValue/BeginningValue)^(1/Years)-1\nExcel function: =RRI(Years,BeginningValue,EndingValue)", language="text")

    section("Same CAGR, different journeys")
    rng = np.random.default_rng(42)
    base_growth = np.linspace(0, 1, 61)
    smooth_line = bv * (ev / bv) ** base_growth
    noise = rng.normal(0, 0.10, len(base_growth))
    noise[0] = noise[-1] = 0
    volatile_line = smooth_line * np.exp(noise - np.linspace(noise[0], noise[-1], len(noise)))
    journeys = pd.DataFrame({"Year": base_growth * n, "Smooth journey": smooth_line, "Volatile journey": volatile_line})
    fig = px.line(journeys, x="Year", y=["Smooth journey", "Volatile journey"], color_discrete_sequence=[TEAL, RED])
    fig.update_layout(title="Identical endpoints—and therefore identical CAGR")
    st.plotly_chart(style_fig(fig, 350), use_container_width=True)


with tabs[4]:
    section("Probability-weighted expected return")
    st.markdown('<div class="formula">E(R) = Σ [Probabilityᵢ × Returnᵢ]</div>', unsafe_allow_html=True)
    default_scenarios = pd.DataFrame(
        {
            "Scenario": ["Boom", "Growth", "Normal", "Slowdown", "Recession"],
            "Probability (%)": [10, 20, 40, 20, 10],
            "Return (%)": [25, 15, 10, 0, -10],
        }
    )
    scenarios = st.data_editor(
        default_scenarios,
        hide_index=True,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Probability (%)": st.column_config.NumberColumn(min_value=0.0, max_value=100.0, step=1.0),
            "Return (%)": st.column_config.NumberColumn(min_value=-100.0, max_value=500.0, step=1.0),
        },
        key="scenario_editor",
    )
    probs = pd.to_numeric(scenarios["Probability (%)"], errors="coerce").fillna(0).to_numpy() / 100
    scenario_returns = pd.to_numeric(scenarios["Return (%)"], errors="coerce").fillna(0).to_numpy() / 100
    prob_sum = probs.sum()
    expected = float(np.sum(probs * scenario_returns))
    variance = float(np.sum(probs * (scenario_returns - expected) ** 2))
    std = math.sqrt(variance)
    downside = float(np.sum(probs * np.minimum(scenario_returns, 0)))
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Probability total", pct(prob_sum, 1))
    s2.metric("Expected Return", pct(expected))
    s3.metric("Scenario Risk (σ)", pct(std))
    s4.metric("Expected downside contribution", pct(downside))
    if not math.isclose(prob_sum, 1.0, abs_tol=1e-6):
        teaching_note("Probabilities must total exactly 100%. Correct the table before interpreting the expected return.", warning=True)

    chart_df = scenarios.copy()
    chart_df["Probability"] = probs
    chart_df["Return"] = scenario_returns
    chart_df["Contribution"] = probs * scenario_returns
    left, right = st.columns(2)
    with left:
        fig = px.bar(
            chart_df,
            x="Scenario",
            y="Return",
            color="Probability",
            text=chart_df["Return"].map(pct),
            color_continuous_scale=["#F8D7DA", GOLD, TEAL],
            title="Scenario returns; colour represents probability",
        )
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(style_fig(fig), use_container_width=True)
    with right:
        fig = px.bar(
            chart_df,
            x="Scenario",
            y="Contribution",
            color="Contribution",
            text=chart_df["Contribution"].map(pct),
            color_continuous_scale="RdYlGn",
            title="Each scenario's contribution: Probability × Return",
        )
        fig.add_hline(y=0, line_color=NAVY)
        fig.update_yaxes(tickformat=".1%")
        st.plotly_chart(style_fig(fig), use_container_width=True)

    teaching_note(
        "<b>Expected return is not a promise.</b> It is the probability-weighted centre of the distribution and may not "
        "equal any actual scenario. Pair it with standard deviation and downside analysis."
    )
    if show_excel:
        st.code(
            "Probability check: =SUM(probability_range)\n"
            "Expected return: =SUMPRODUCT(probability_range,return_range)\n"
            "Variance: =SUMPRODUCT(probability_range,(return_range-expected_return)^2)",
            language="text",
        )


with tabs[5]:
    section("Simple returns versus log returns")
    st.markdown('<div class="formula">Simple Return = Pₜ/Pₜ₋₁ − 1 &nbsp;&nbsp; | &nbsp;&nbsp; Log Return = LN(Pₜ/Pₜ₋₁)</div>', unsafe_allow_html=True)
    prices_default = pd.DataFrame({"Day": ["Day 0", "Day 1", "Day 2", "Day 3", "Day 4"], "Closing Price": [100, 105, 102, 108, 110]})
    price_input = st.data_editor(
        prices_default,
        hide_index=True,
        use_container_width=True,
        num_rows="dynamic",
        column_config={"Closing Price": st.column_config.NumberColumn(min_value=0.01, step=1.0)},
        key="log_prices",
    )
    prices = pd.to_numeric(price_input["Closing Price"], errors="coerce").dropna().to_numpy()
    if len(prices) >= 2 and np.all(prices > 0):
        simple = prices[1:] / prices[:-1] - 1
        logs = np.log(prices[1:] / prices[:-1])
        cumulative_simple = prices[-1] / prices[0] - 1
        total_log = float(logs.sum())
        l1, l2, l3 = st.columns(3)
        l1.metric("Cumulative Simple Return", pct(cumulative_simple, 3))
        l2.metric("Sum of Log Returns", pct(total_log, 3))
        l3.metric("EXP(Log Sum) − 1", pct(math.exp(total_log) - 1, 3))
        return_df = pd.DataFrame(
            {
                "Period": price_input["Day"].iloc[1 : len(prices)].astype(str).to_list(),
                "Simple Return": simple,
                "Log Return": logs,
            }
        )
        left, right = st.columns(2)
        with left:
            fig = px.line(
                x=price_input["Day"].iloc[: len(prices)],
                y=prices,
                markers=True,
                labels={"x": "Period", "y": "Closing price"},
                title="Price path",
            )
            fig.update_traces(line_color=BLUE, fill="tozeroy", fillcolor="rgba(11,92,173,.12)")
            st.plotly_chart(style_fig(fig), use_container_width=True)
        with right:
            long = return_df.melt(id_vars="Period", var_name="Return Type", value_name="Return")
            fig = px.bar(long, x="Period", y="Return", color="Return Type", barmode="group", color_discrete_sequence=[ORANGE, PURPLE], title="Simple and log returns by period")
            fig.update_yaxes(tickformat=".1%")
            st.plotly_chart(style_fig(fig), use_container_width=True)
        teaching_note(
            f"The log returns add to {pct(total_log,3)}, exactly LN({prices[-1]:.2f}/{prices[0]:.2f}). "
            f"Convert it back with EXP(r)−1 to recover the actual cumulative return of {pct(cumulative_simple,3)}."
        )
        if show_excel:
            st.code("Log return: =LN(CurrentPrice/PreviousPrice)\nConvert back: =EXP(LogReturn)-1\nAdditivity check: =SUM(log_returns)", language="text")
    else:
        st.error("Enter at least two strictly positive prices.")

    section("Why +50% followed by −50% is not zero")
    up = st.slider("Gain in Period 1", 1, 100, 50, key="updown") / 100
    second = -up
    path_simple = [100, 100 * (1 + up), 100 * (1 + up) * (1 + second)]
    simple_total = path_simple[-1] / 100 - 1
    log_up = math.log1p(up)
    log_down = math.log1p(second) if second > -1 else -np.inf
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=["Start", f"+{up:.0%}", f"−{up:.0%}"], y=path_simple, mode="lines+markers+text", text=[money(x) for x in path_simple], textposition="top center", line=dict(color=RED, width=4)))
    fig.update_layout(title=f"Equal percentage gain and loss leave wealth at {money(path_simple[-1])}")
    st.plotly_chart(style_fig(fig, 330), use_container_width=True)
    teaching_note(f"Total simple return = {pct(simple_total)}. The log moves are {pct(log_up)} and {pct(log_down)}; they are not equal and opposite.")


with tabs[6]:
    section("TWR measures the manager; MWR measures the investor experience")
    st.markdown(
        '<div class="formula">TWR = Π(1+rᵢ) − 1 &nbsp;&nbsp; | &nbsp;&nbsp; MWR = IRR of the investor cash flows</div>',
        unsafe_allow_html=True,
    )
    t1, t2, t3, t4 = st.columns(4)
    start_value = t1.number_input("Start of Year 1", min_value=1.0, value=100000.0, step=5000.0)
    end_y1 = t2.number_input("End of Year 1", min_value=0.0, value=110000.0, step=5000.0)
    contribution = t3.number_input("Contribution before Year 2", min_value=0.0, value=50000.0, step=5000.0)
    end_y2 = t4.number_input("End of Year 2", min_value=0.0, value=152000.0, step=5000.0)
    r_y1 = end_y1 / start_value - 1
    begin_y2 = end_y1 + contribution
    r_y2 = end_y2 / begin_y2 - 1 if begin_y2 else np.nan
    cumulative_twr = (1 + r_y1) * (1 + r_y2) - 1
    annual_twr = (1 + cumulative_twr) ** 0.5 - 1 if cumulative_twr > -1 else np.nan
    mwr = irr([-start_value, -contribution, end_y2])
    gap = annual_twr - mwr
    q1, q2, q3, q4 = st.columns(4)
    q1.metric("Year 1 Return", pct(r_y1))
    q2.metric("Year 2 Return", pct(r_y2))
    q3.metric("Annualised TWR", pct(annual_twr))
    q4.metric("MWR / IRR", pct(mwr))

    left, right = st.columns(2)
    with left:
        flow = go.Figure()
        flow.add_trace(go.Scatter(
            x=["Start Y1", "End Y1", "After contribution", "End Y2"],
            y=[start_value, end_y1, begin_y2, end_y2],
            mode="lines+markers+text",
            text=[money(start_value), money(end_y1), money(begin_y2), money(end_y2)],
            textposition="top center",
            line=dict(color=BLUE, width=4),
            marker=dict(size=[12, 12, 18, 12], color=[BLUE, TEAL, GOLD, PURPLE]),
        ))
        flow.add_annotation(x="After contribution", y=begin_y2, text=f"External cash flow: +{money(contribution)}", showarrow=True, arrowcolor=GOLD, yshift=-55)
        flow.update_layout(title="Portfolio value and the external cash flow")
        st.plotly_chart(style_fig(flow), use_container_width=True)
    with right:
        compare = pd.DataFrame({"Measure": ["Annualised TWR", "MWR / IRR", "Timing Gap"], "Return": [annual_twr, mwr, gap]})
        fig = px.bar(compare, x="Measure", y="Return", color="Measure", text=compare["Return"].map(pct), color_discrete_sequence=[TEAL, PURPLE, ORANGE], title="Performance versus investor experience")
        fig.update_traces(textposition="outside")
        fig.update_yaxes(tickformat=".1%")
        st.plotly_chart(style_fig(fig), use_container_width=True)

    if mwr < annual_twr:
        explanation = "MWR is lower because more money was exposed to the weaker part of the performance path."
    elif mwr > annual_twr:
        explanation = "MWR is higher because more money was exposed to the stronger part of the performance path."
    else:
        explanation = "MWR and TWR are equal because cash-flow timing did not change the investor's experience."
    teaching_note(
        f"<b>Timing gap: {pct(gap)}.</b> {explanation} TWR removes the client's cash-flow decision; MWR incorporates it."
    )
    if show_excel:
        st.code(
            "Sub-period return: =EndingValue/BeginningValue-1\n"
            "Cumulative TWR: =PRODUCT(1+sub_period_returns)-1\n"
            "Annualised TWR: =(1+CumulativeTWR)^(1/Years)-1\n"
            "MWR: =IRR(cash_flows) or =XIRR(cash_flows,dates)",
            language="text",
        )


@dataclass
class PracticeProblem:
    title: str
    question: str
    answer: float
    unit: str
    working: str


def make_practice(kind: str, seed: int) -> PracticeProblem:
    rng = np.random.default_rng(seed)
    if kind == "HPR":
        p0 = int(rng.integers(50, 500))
        p1 = int(round(p0 * rng.uniform(0.85, 1.25)))
        div = int(rng.integers(0, max(2, p0 // 15)))
        ans = (p1 - p0 + div) / p0
        return PracticeProblem("Holding Period Return", f"Buy at ₹{p0}, receive ₹{div}, sell at ₹{p1}. Find HPR.", ans, "%", f"({p1} − {p0} + {div}) ÷ {p0}")
    if kind == "CAGR":
        bv_ = int(rng.integers(5000, 30000))
        years_ = int(rng.integers(3, 9))
        ev_ = int(round(bv_ * rng.uniform(1.25, 2.6)))
        ans = (ev_ / bv_) ** (1 / years_) - 1
        return PracticeProblem("CAGR", f"₹{bv_:,} becomes ₹{ev_:,} in {years_} years. Find CAGR.", ans, "%", f"({ev_}/{bv_})^(1/{years_}) − 1")
    if kind == "Expected Return":
        probs_ = np.array([0.2, 0.5, 0.3])
        rets_ = rng.integers(-10, 31, 3) / 100
        ans = float(probs_ @ rets_)
        return PracticeProblem("Expected Return", f"Returns are {rets_[0]:.0%}, {rets_[1]:.0%}, {rets_[2]:.0%} with probabilities 20%, 50%, 30%. Find E(R).", ans, "%", "SUM(Probability × Return)")
    if kind == "Geometric Mean":
        rets_ = rng.integers(-15, 26, 3) / 100
        ans = geometric_mean(rets_)
        return PracticeProblem("Geometric Mean", f"Returns are {rets_[0]:.0%}, {rets_[1]:.0%}, {rets_[2]:.0%}. Find the compound mean.", ans, "%", "[(1+R₁)(1+R₂)(1+R₃)]^(1/3) − 1")
    p0 = int(rng.integers(50, 200))
    p1 = int(round(p0 * rng.uniform(0.8, 1.3)))
    ans = math.log(p1 / p0)
    return PracticeProblem("Log Return", f"Price moves from ₹{p0} to ₹{p1}. Find the log return.", ans, "%", f"LN({p1}/{p0})")


with tabs[7]:
    section("Practice Studio: solve, check, learn")
    pcol1, pcol2 = st.columns([1, 1])
    kind = pcol1.selectbox("Choose a topic", ["HPR", "CAGR", "Expected Return", "Geometric Mean", "Log Return"])
    if "practice_seed" not in st.session_state:
        st.session_state.practice_seed = 101
    if pcol2.button("🎲 New problem", use_container_width=True):
        st.session_state.practice_seed += 1
        st.session_state.pop("practice_checked", None)
    problem = make_practice(kind, st.session_state.practice_seed)
    st.markdown(concept_card(problem.title, problem.question, PURPLE), unsafe_allow_html=True)
    user_answer = st.number_input("Your answer (%)", value=0.0, step=0.1, format="%.3f", key=f"practice_answer_{kind}_{st.session_state.practice_seed}") / 100
    a, b, c = st.columns(3)
    if a.button("Check my answer", use_container_width=True):
        st.session_state.practice_checked = True
    if b.button("Show hint", use_container_width=True):
        st.info(f"Use: {problem.working}")
    if c.button("Reveal solution", use_container_width=True):
        st.warning(f"Answer: {pct(problem.answer, 3)}\n\nWorking: {problem.working}")
    if st.session_state.get("practice_checked"):
        tolerance = 0.0006
        if abs(user_answer - problem.answer) <= tolerance:
            st.success(f"Excellent—your answer {pct(user_answer,3)} is correct.")
        else:
            st.error(f"Not yet. Your answer is {pct(user_answer,3)}. Recheck the formula and signs.")
    teaching_note("Write the formula first, substitute values second, calculate third, and interpret the number last.")


QUIZ = [
    {
        "q": "A stock bought for ₹100, sold for ₹108, and paying ₹4 dividend has an HPR of:",
        "options": ["8%", "12%", "4%", "16%"],
        "answer": "12%",
        "why": "(108 − 100 + 4) ÷ 100 = 12%.",
    },
    {
        "q": "Which measure best describes actual compound wealth growth across multiple periods?",
        "options": ["Arithmetic mean", "Geometric mean", "Expected return", "Current yield"],
        "answer": "Geometric mean",
        "why": "The geometric mean compounds return relatives and preserves terminal wealth.",
    },
    {
        "q": "The arithmetic mean is most appropriate for:",
        "options": ["A one-period expected return", "Manager attribution with cash flows", "Dated investor cash flows", "Averaging P/E ratios"],
        "answer": "A one-period expected return",
        "why": "It is the best unbiased estimate of a single future period under stable assumptions.",
    },
    {
        "q": "If probabilities sum to 90%, the expected-return calculation is:",
        "options": ["Complete", "Invalid until probabilities total 100%", "A CAGR", "A log return"],
        "answer": "Invalid until probabilities total 100%",
        "why": "The probability distribution must total exactly one.",
    },
    {
        "q": "Periodic log returns are especially useful because they are:",
        "options": ["Always positive", "Additive across time", "Equal to simple returns", "Unaffected by prices"],
        "answer": "Additive across time",
        "why": "Σ LN(Pt/Pt−1) = LN(Ending Price/Beginning Price).",
    },
    {
        "q": "Which return measure neutralises the timing and size of client contributions?",
        "options": ["MWR", "IRR", "TWR", "HPR"],
        "answer": "TWR",
        "why": "TWR chain-links sub-period returns cut at each external cash flow.",
    },
    {
        "q": "A large contribution immediately before a losing period will generally make:",
        "options": ["MWR lower than TWR", "MWR higher than TWR", "CAGR equal zero", "HPR undefined"],
        "answer": "MWR lower than TWR",
        "why": "More investor money is exposed to the weak period, reducing the money-weighted result.",
    },
    {
        "q": "CAGR can be misleading because it:",
        "options": ["Needs every annual return", "Hides the path and volatility", "Cannot compare multi-year growth", "Includes all interim cash flows"],
        "answer": "Hides the path and volatility",
        "why": "CAGR uses only beginning value, ending value and time.",
    },
    {
        "q": "Which mean is appropriate for averaging positive P/E ratios?",
        "options": ["Arithmetic", "Geometric", "Harmonic", "Expected"],
        "answer": "Harmonic",
        "why": "The harmonic mean is appropriate for positive ratios and per-unit rates.",
    },
    {
        "q": "For the same non-identical positive return relatives, the usual ordering is:",
        "options": ["GM ≥ AM ≥ HM", "AM ≥ GM ≥ HM", "HM ≥ GM ≥ AM", "AM = GM = HM"],
        "answer": "AM ≥ GM ≥ HM",
        "why": "The means are equal only when every observation is identical.",
    },
]


with tabs[8]:
    section("Mastering Returns Quiz")
    st.markdown("Select one answer for every question, then submit. Explanations appear after scoring.")
    responses = []
    for i, item in enumerate(QUIZ, 1):
        st.markdown(f"**{i}. {item['q']}**")
        choice = st.radio("Select an answer", ["— Choose —"] + item["options"], key=f"quiz_{i}", label_visibility="collapsed")
        responses.append(choice)
        st.write("")
    if st.button("🏆 Submit quiz", type="primary", use_container_width=True):
        answered = sum(x != "— Choose —" for x in responses)
        if answered < len(QUIZ):
            st.warning(f"Please answer all questions. Completed: {answered}/{len(QUIZ)}.")
        else:
            score = sum(choice == item["answer"] for choice, item in zip(responses, QUIZ))
            percentage = score / len(QUIZ)
            st.progress(percentage)
            if score >= 9:
                st.success(f"Outstanding: {score}/10. You have mastered the return-measure framework.")
            elif score >= 7:
                st.success(f"Strong result: {score}/10. Review the explanations for a complete mastery pass.")
            elif score >= 5:
                st.warning(f"Developing well: {score}/10. Revisit the relevant interactive labs.")
            else:
                st.error(f"Foundation review recommended: {score}/10. Follow the Learning Map from HPR onward.")
            for i, (choice, item) in enumerate(zip(responses, QUIZ), 1):
                icon = "✅" if choice == item["answer"] else "❌"
                with st.expander(f"{icon} Question {i}: correct answer — {item['answer']}"):
                    st.write(item["why"])


with tabs[9]:
    section("Formula and decision library")
    formula_table = pd.DataFrame(
        [
            ["Holding Period Return", "(P₁ − P₀ + Income) / P₀", "One holding period", "=(P1-P0+Income)/P0", "Include both price and income"],
            ["Annualised Return", "(1 + HPR)^(365/days) − 1", "Compare unequal periods", "=(1+HPR)^(365/Days)-1", "Short-period repetition may be unrealistic"],
            ["CAGR", "(EV/BV)^(1/n) − 1", "Multi-year endpoints", "=RRI(n,BV,EV)", "Hides path and volatility"],
            ["Arithmetic Mean", "ΣRᵢ/n", "Single-period estimate", "=AVERAGE(range)", "Do not compound with it"],
            ["Geometric Mean", "[Π(1+Rᵢ)]^(1/n) − 1", "Compound growth", "=GEOMEAN(1+range)-1", "Requires all 1+R to be positive"],
            ["Harmonic Mean", "n / Σ(1/Xᵢ)", "Ratios and per-unit rates", "=HARMEAN(range)", "Positive values only"],
            ["Expected Return", "Σ(Pᵢ×Rᵢ)", "Forward scenarios", "=SUMPRODUCT(probs,returns)", "Probabilities must total 100%"],
            ["Log Return", "LN(Pₜ/Pₜ₋₁)", "Quantitative time series", "=LN(Pt/Pt_1)", "Convert back using EXP(r)-1"],
            ["TWR", "Π(1+rᵢ) − 1", "Manager performance", "=PRODUCT(1+range)-1", "Value at each external cash flow"],
            ["MWR", "IRR of actual cash flows", "Investor experience", "=IRR(values) / =XIRR(values,dates)", "Sensitive to cash-flow timing"],
        ],
        columns=["Measure", "Core Formula", "Best Used For", "Excel Approach", "Key Caution"],
    )
    st.dataframe(
        formula_table,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Measure": st.column_config.TextColumn(width="medium"),
            "Core Formula": st.column_config.TextColumn(width="large"),
            "Best Used For": st.column_config.TextColumn(width="large"),
            "Excel Approach": st.column_config.TextColumn(width="large"),
            "Key Caution": st.column_config.TextColumn(width="large"),
        },
    )
    csv = formula_table.to_csv(index=False).encode()
    st.download_button("⬇ Download Return Formula Cheat Sheet (CSV)", csv, "Mastering_Returns_Formula_Cheat_Sheet.csv", "text/csv", use_container_width=True)

    section("Seven misconceptions to eliminate")
    myths = [
        ("“Average return” is always one concept.", "Arithmetic and geometric means answer different questions."),
        ("CAGR shows how the investment behaved each year.", "It only connects the two endpoints smoothly."),
        ("A +50% gain offsets a −50% loss.", "₹100 becomes ₹75; the net result is −25%."),
        ("Expected return is the most likely outcome.", "It is a probability-weighted average and may never occur."),
        ("Log return is the actual percentage earned.", "Convert it using EXP(r)−1 before client reporting."),
        ("TWR is the investor's personal return.", "TWR evaluates the manager; MWR reflects the investor's money and timing."),
        ("The highest mean is the best measure.", "The right measure depends on the question, not the size of the answer."),
    ]
    for myth, correction in myths:
        with st.expander(f"Myth: {myth}"):
            st.write(f"**Correction:** {correction}")

    section("Export your own mini return report")
    report = pd.DataFrame(
        {
            "Learning Area": ["HPR", "Means", "CAGR", "Expected Return", "Log Return", "TWR vs MWR"],
            "Core Question": [
                "What did the holding earn?",
                "What does average mean here?",
                "What annual rate links the endpoints?",
                "What do scenarios imply?",
                "How can returns add across time?",
                "Manager skill or investor experience?",
            ],
            "Status": ["Explore the lab"] * 6,
        }
    )
    buffer = io.BytesIO()
    report.to_csv(buffer, index=False)
    st.download_button("⬇ Download Learning Checklist", buffer.getvalue(), "Mastering_Returns_Learning_Checklist.csv", "text/csv", use_container_width=True)


st.markdown(
    """
<div class="footer">
  <b style="color:#F3C84B;font-size:1.08rem">The Mountain Path Academy</b><br>
  Prof. V. Ravichandran · Financial Education through Excel, Analytics and Interactive Models<br><br>
  <div class="footer-links">
    <a href="https://themountainpathacademy.com/" target="_blank">🌐 Mountain Path Academy</a>
    <a href="https://www.linkedin.com/in/trichyravis/" target="_blank">in LinkedIn Profile</a>
    <a href="https://github.com/trichyravis" target="_blank">⌂ GitHub Profile</a>
  </div><br>
  <span style="font-size:.78rem;color:#BFD6E6">Educational project · Not investment advice · © 2026 The Mountain Path Academy</span>
</div>
""",
    unsafe_allow_html=True,
)
