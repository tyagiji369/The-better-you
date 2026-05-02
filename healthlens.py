import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
import numpy as np
import random
from datetime import datetime, timedelta

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="HealthLens",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════════════════
# GLOBAL STYLES
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #F7F5F1;
    color: #1A1A1A;
}
.block-container {
    padding: 0 2rem 6rem 2rem;
    max-width: 820px;
}

/* ── Brand header ── */
.brand-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1.5rem 0 1.3rem 0;
    border-bottom: 1px solid #E8E4DC;
    margin-bottom: 2.2rem;
}
.brand-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem; font-weight: 600;
    color: #1A1A1A; letter-spacing: -0.2px;
}
.brand-logo em {
    font-style: italic; color: #2D6A4F;
}
.brand-pill {
    font-size: 0.62rem; font-weight: 600;
    letter-spacing: 2px; text-transform: uppercase;
    color: #fff; background: #1A1A1A;
    padding: 3px 10px; border-radius: 20px;
}

/* ── Progress ── */
.prog-wrap { margin-bottom: 2.4rem; }
.prog-meta { display: flex; justify-content: space-between; margin-bottom: 8px; }
.prog-name { font-size: 0.68rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #1A1A1A; }
.prog-frac { font-size: 0.68rem; color: #B8B0A8; }
.prog-track { display: flex; gap: 4px; }
.prog-seg   { height: 3px; flex: 1; border-radius: 3px; background: #E4E0D8; }
.prog-seg.done   { background: #2D6A4F; }
.prog-seg.active { background: #95C4AA; }

/* ── Page titles ── */
.page-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem; font-weight: 400;
    color: #1A1A1A; letter-spacing: -1px; line-height: 1.13;
    margin-bottom: 0.4rem;
}
.page-title em { font-style: italic; color: #2D6A4F; }
.page-sub {
    font-size: 0.9rem; color: #909090; font-weight: 300;
    line-height: 1.6; margin-bottom: 1.8rem;
}

/* ── Section label ── */
.slabel {
    font-size: 0.62rem; font-weight: 700;
    letter-spacing: 2.5px; text-transform: uppercase;
    color: #B8B0A8; margin: 2rem 0 0.7rem 0;
    display: flex; align-items: center; gap: 8px;
}
.slabel::after {
    content: ''; flex: 1; height: 1px; background: #E8E4DC;
}

/* ── Metric cards ── */
.cards { display: flex; gap: 10px; flex-wrap: wrap; margin: 0.6rem 0 1.6rem 0; }
.card {
    flex: 1; min-width: 130px;
    background: #fff; border: 1px solid #E8E4DC;
    border-radius: 16px; padding: 1.15rem 1.3rem 1.1rem;
    position: relative; overflow: hidden;
}
.card::before {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    border-radius: 16px 16px 0 0;
    background: #E4E0D8;
}
.card.green::before  { background: #2D6A4F; }
.card.amber::before  { background: #B57800; }
.card.red::before    { background: #B92D2D; }
.card.blue::before   { background: #1A56B0; }
.card.dark::before   { background: #1A1A1A; }
.card.purple::before { background: #6B21A8; }

.c-lbl { font-size: 0.61rem; font-weight: 700; letter-spacing: 2.2px; text-transform: uppercase; color: #C0B8B0; margin-bottom: 0.45rem; }
.c-val { font-family: 'Playfair Display', serif; font-size: 2.15rem; font-weight: 600; color: #1A1A1A; line-height: 1; letter-spacing: -1px; }
.c-unit { font-size: 0.76rem; color: #C8C0B8; margin-left: 2px; }
.c-sub  { font-size: 0.74rem; color: #A8A098; margin-top: 0.32rem; line-height: 1.4; }

/* ── Pills ── */
.pill { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 0.69rem; font-weight: 700; margin-top: 0.4rem; letter-spacing: 0.3px; }
.p-green  { background: #DCFCE7; color: #14532D; }
.p-yellow { background: #FEF9C3; color: #713F12; }
.p-orange { background: #FFEDD5; color: #7C2D12; }
.p-red    { background: #FEE2E2; color: #7F1D1D; }

/* ── Alert boxes ── */
.alert { padding: 0.9rem 1.1rem; border-radius: 11px; font-size: 0.87rem; line-height: 1.65; margin: 0.9rem 0; border: 1px solid transparent; }
.a-info    { background: #EFF6FF; color: #1E3A8A; border-color: #93C5FD; }
.a-success { background: #F0FDF4; color: #14532D; border-color: #86EFAC; }
.a-warn    { background: #FFFBEB; color: #713F12; border-color: #FCD34D; }
.a-danger  { background: #FFF1F2; color: #7F1D1D; border-color: #FCA5A5; }
.a-neutral { background: #FAFAF8; color: #3C3C3C; border-color: #D6D3D1; }

/* ── Dark callout block ── */
.callout {
    background: #1A1A1A; color: #F5F5F3;
    border-radius: 16px; padding: 1.4rem 1.6rem;
    margin: 1rem 0 1.6rem 0;
    display: flex; align-items: center; gap: 1.4rem;
}
.callout-big {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem; font-weight: 600;
    letter-spacing: -2px; line-height: 1; white-space: nowrap;
}
.callout-detail { font-size: 0.82rem; color: #999; line-height: 1.6; }
.callout-detail strong { color: #E0DDD8; }

/* ── Chart wrapper ── */
.chart-wrap {
    background: #fff; border: 1px solid #E8E4DC;
    border-radius: 14px; padding: 1.3rem 1.4rem 0.7rem;
    margin: 0.6rem 0 1.3rem 0;
}
.chart-lbl {
    font-size: 0.67rem; font-weight: 700;
    letter-spacing: 1.8px; text-transform: uppercase;
    color: #C0B8B0; margin-bottom: 0.5rem;
}

/* ── Disease tag chips ── */
.disease-tags { display: flex; flex-wrap: wrap; gap: 8px; margin: 0.5rem 0 1rem 0; }
.dtag {
    display: inline-block; padding: 4px 13px;
    border-radius: 20px; font-size: 0.76rem; font-weight: 500;
    background: #FEE2E2; color: #7F1D1D;
    border: 1px solid #FCA5A5;
}
.dtag-none { background: #F0FDF4; color: #14532D; border-color: #86EFAC; }

/* ── Comparison table ── */
.compare-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 10px; margin: 1rem 0 1.5rem 0;
}
.cg-col { background: #fff; border: 1px solid #E8E4DC; border-radius: 12px; padding: 1rem 1.1rem; }
.cg-col.disease { border-color: #FCA5A5; background: #FFF8F8; }
.cg-head {
    font-size: 0.65rem; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; margin-bottom: 0.8rem; padding-bottom: 0.5rem;
    border-bottom: 1px solid #E8E4DC;
}
.cg-head.healthy  { color: #2D6A4F; }
.cg-head.affected { color: #B92D2D; }
.cg-item { font-size: 0.82rem; color: #444; line-height: 1.6; margin-bottom: 0.55rem; padding-left: 0.8rem; position: relative; }
.cg-item::before { content: '—'; position: absolute; left: 0; color: #D0CBC3; }
.cg-item.diff::before { content: '!'; color: #B92D2D; font-weight: 700; }

/* ── Food recommendation cards ── */
.meal-card {
    background: #fff; border: 1px solid #E8E4DC;
    border-radius: 13px; padding: 1rem 1.2rem;
    margin-bottom: 9px;
}
.meal-head {
    font-size: 0.65rem; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; color: #B0A898; margin-bottom: 0.6rem;
}
.meal-item {
    display: flex; justify-content: space-between; align-items: baseline;
    font-size: 0.86rem; color: #333; padding: 0.22rem 0;
    border-bottom: 1px dashed #F0EDE8;
}
.meal-item:last-child { border-bottom: none; }
.meal-qty { font-size: 0.78rem; color: #AAA; white-space: nowrap; margin-left: 8px; }
.meal-kcal { font-size: 0.72rem; color: #2D6A4F; font-weight: 600; min-width: 48px; text-align: right; }

/* ── Rec list ── */
.rec {
    display: flex; gap: 12px; align-items: flex-start;
    padding: 0.9rem 1.1rem; background: #fff;
    border: 1px solid #E8E4DC; border-radius: 11px;
    margin-bottom: 8px; font-size: 0.86rem; color: #444; line-height: 1.6;
}
.rec-n { font-family: 'Playfair Display', serif; font-size: 1.1rem; font-weight: 600; color: #D4CFC8; min-width: 22px; }
.rec.flagged { border-color: #FCA5A5; background: #FFF8F8; }
.rec.flagged .rec-n { color: #FCA5A5; }

/* ── Divider ── */
.div { border: none; border-top: 1px solid #E8E4DC; margin: 2.2rem 0; }

/* ── Buttons ── */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.87rem !important; font-weight: 500 !important;
    border-radius: 10px !important; padding: 0.55rem 1.2rem !important;
    transition: all 0.15s !important;
}
div[data-testid="column"]:last-child .stButton > button {
    background: #1A1A1A !important; color: #F7F5F1 !important;
    border: 1.5px solid #1A1A1A !important;
}
div[data-testid="column"]:last-child .stButton > button:hover {
    background: #2D6A4F !important; border-color: #2D6A4F !important;
}
div[data-testid="column"]:first-child .stButton > button {
    background: transparent !important; color: #1A1A1A !important;
    border: 1.5px solid #D0CBC3 !important;
}
div[data-testid="column"]:first-child .stButton > button:hover { border-color: #888 !important; }

/* ── Inputs ── */
.stNumberInput input, .stTextArea textarea {
    border-radius: 10px !important; border: 1.5px solid #D8D4CC !important;
    background: #fff !important; font-family: 'Inter', sans-serif !important;
}
.stSelectbox > div > div {
    border-radius: 10px !important; border: 1.5px solid #D8D4CC !important;
    background: #fff !important;
}
.stRadio > div { gap: 7px !important; }
.stRadio label {
    font-size: 0.9rem !important; background: #fff;
    border: 1.5px solid #E4E0D8; border-radius: 10px;
    padding: 0.65rem 1rem !important; width: 100%; cursor: pointer;
    transition: border-color 0.15s, background 0.15s;
}
.stRadio label:hover { border-color: #2D6A4F !important; background: #F5FBF7 !important; }
.stMultiSelect > div { border-radius: 10px !important; }

/* ── Footer ── */
.footer {
    text-align: center; font-size: 0.69rem; color: #C8C0B8;
    margin-top: 4rem; padding-top: 1.2rem;
    border-top: 1px solid #E8E4DC; letter-spacing: 0.4px;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# SESSION STATE DEFAULTS
# ═══════════════════════════════════════════════════════════════
DEFAULTS = {
    "page":                 "input",
    "height":               170,
    "weight":               70.0,
    "age":                  22,
    "gender":               "Male",
    "activity":             "Sedentary (desk job, little exercise)",
    "diseases":             [],
    "goal":                 "Maintain Weight",
    "target_weight_change": 5.0,
    "target_weeks":         8,
    "baseline_weights":     [],
    "daily_weight_log":     [],
    "target_calories":      0.0,
    "bmr":                  0.0,
    "tdee":                 0.0,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ═══════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════
PAGES = ["input", "health_screen", "metrics", "goal", "target", "baseline", "tracker", "analysis"]
TOTAL = len(PAGES)
PAGE_NAMES = ["Profile", "Health Check", "Metrics", "Goal", "Target", "Baseline", "Tracker", "Report"]

ACTIVITY_MULT = {
    "Sedentary (desk job, little exercise)": 1.2,
    "Lightly active (1–3 days/week)":        1.375,
    "Moderately active (3–5 days/week)":     1.55,
    "Very active (6–7 days/week)":           1.725,
    "Athlete / physical job":                1.9,
}

ALL_DISEASES = [
    "Type 2 Diabetes",
    "Hypertension (High Blood Pressure)",
    "High Cholesterol (Dyslipidaemia)",
    "Hypothyroidism",
    "Polycystic Ovary Syndrome (PCOS)",
    "Non-Alcoholic Fatty Liver Disease (NAFLD)",
    "Insulin Resistance / Pre-Diabetes",
    "Chronic Kidney Disease (CKD)",
]

# ─── Disease-specific food restrictions & notes ──────────────────
DISEASE_NOTES = {
    "Type 2 Diabetes": {
        "avoid":  ["White rice, white bread, refined flour (maida)", "Sugary drinks, fruit juices, packaged sweets", "Potatoes, deep-fried foods"],
        "prefer": ["Brown rice (½ cup cooked) or oats (40 g dry)", "Lentils / dal (150 g cooked) — high fibre, low GI", "Leafy greens freely — spinach, methi, broccoli"],
        "note":   "Distribute meals into 4–5 smaller portions. Never skip breakfast. Monitor post-meal blood glucose."
    },
    "Hypertension (High Blood Pressure)": {
        "avoid":  ["Table salt, pickles, papad, namkeen snacks", "Processed meats, canned soups, packaged noodles", "Excess caffeine and alcohol"],
        "prefer": ["Banana (1 medium) — high potassium", "Boiled vegetables freely — low sodium", "Oats (40 g dry) — soluble fibre lowers BP"],
        "note":   "Keep sodium below 1,500 mg/day. The DASH diet is clinically recommended for hypertension."
    },
    "High Cholesterol (Dyslipidaemia)": {
        "avoid":  ["Saturated fats — butter, ghee (> 1 tsp/day), coconut oil", "Full-fat dairy, red meat, egg yolk (> 3/week)", "Bakery products, margarine, trans-fat snacks"],
        "prefer": ["Walnuts (30 g / 7 halves) — omega-3 rich", "Oats (40 g dry) — beta-glucan lowers LDL", "Fatty fish like salmon or mackerel 2× a week (100 g serving)"],
        "note":   "Soluble fibre (psyllium husk, oats, legumes) binds cholesterol in the gut — include at every meal."
    },
    "Hypothyroidism": {
        "avoid":  ["Raw goitrogenic vegetables in large amounts — cabbage, cauliflower, soy (cook them instead)", "Excess iodine supplements unless prescribed", "Gluten-heavy meals if sensitivity suspected"],
        "prefer": ["Brazil nuts (2 nuts/day) — high selenium supports thyroid", "Eggs (1–2/day) — iodine + selenium", "Fish (100 g serving, 3×/week) — natural iodine source"],
        "note":   "Take thyroid medication on an empty stomach. Wait 30–60 min before eating. Fibre supplements can interfere with absorption."
    },
    "Polycystic Ovary Syndrome (PCOS)": {
        "avoid":  ["Refined carbohydrates — maida, white rice, sugary cereals", "Dairy in excess if acne is a concern", "Alcohol and high-sugar fruits like mango, grapes in large quantity"],
        "prefer": ["Flaxseeds (1 tbsp ground/day) — anti-androgenic lignans", "Lentils / rajma (150 g cooked) — low GI protein", "Cinnamon (½ tsp/day) — may improve insulin sensitivity"],
        "note":   "Low-GI eating pattern is the most evidence-backed dietary approach for PCOS. Aim for carbs < 40% of total intake."
    },
    "Non-Alcoholic Fatty Liver Disease (NAFLD)": {
        "avoid":  ["Fructose-rich foods — fruit juices, colas, packaged sweets", "Alcohol completely", "Refined carbohydrates and trans fats"],
        "prefer": ["Coffee (2 cups/day without sugar) — shown to reduce liver fibrosis", "Walnuts (30 g/day) — anti-inflammatory omega-3", "Cruciferous vegetables — broccoli, cauliflower (cooked, 150 g)"],
        "note":   "Even a 5–7% reduction in body weight significantly reduces liver fat. Calorie deficit is the primary treatment."
    },
    "Insulin Resistance / Pre-Diabetes": {
        "avoid":  ["All forms of added sugar and sugar-sweetened beverages", "White bread, polished rice, pastries", "Large meals — they spike insulin sharply"],
        "prefer": ["Vinegar (1 tbsp before meals) — blunts post-meal glucose spike", "Legumes (150 g cooked) at every meal — low insulin index", "Methi / fenugreek seeds (1 tsp soaked overnight) — improves sensitivity"],
        "note":   "Resistance training 3×/week is as effective as medication for improving insulin sensitivity."
    },
    "Chronic Kidney Disease (CKD)": {
        "avoid":  ["High-potassium foods — bananas, oranges, potatoes, tomatoes (if CKD stage 3+)", "High-phosphorus foods — dairy, nuts, cola drinks", "High-protein diets — keep to 0.6–0.8 g/kg unless on dialysis"],
        "prefer": ["White rice, white bread (lower potassium/phosphorus than whole grain in CKD)", "Cabbage, green beans, cauliflower — low-potassium vegetables", "Egg whites (2–3/day) — high-quality protein, low phosphorus"],
        "note":   "CKD nutrition must be supervised by a renal dietitian. These are general guidelines only — individual lab values determine exact restrictions."
    },
}

# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS — UI
# ═══════════════════════════════════════════════════════════════
def go(page):
    st.session_state.page = page
    st.rerun()

def brand():
    st.markdown(
        '<div class="brand-header">'
        '<div class="brand-logo">Health<em>Lens</em></div>'
        '<span class="brand-pill">B.Tech Project</span>'
        '</div>',
        unsafe_allow_html=True,
    )

def progress_bar(current_page):
    idx = PAGES.index(current_page)
    segs = "".join(
        f'<div class="prog-seg {"done" if i < idx else "active" if i == idx else ""}"></div>'
        for i in range(TOTAL)
    )
    st.markdown(
        f'<div class="prog-wrap">'
        f'<div class="prog-meta">'
        f'<span class="prog-name">{PAGE_NAMES[idx]}</span>'
        f'<span class="prog-frac">{idx+1} / {TOTAL}</span>'
        f'</div><div class="prog-track">{segs}</div></div>',
        unsafe_allow_html=True,
    )

def title(main, sub=""):
    st.markdown(f'<div class="page-title">{main}</div>', unsafe_allow_html=True)
    if sub:
        st.markdown(f'<p class="page-sub">{sub}</p>', unsafe_allow_html=True)

def slabel(text):
    st.markdown(f'<div class="slabel">{text}</div>', unsafe_allow_html=True)

def alert(msg, kind="neutral"):
    st.markdown(f'<div class="alert a-{kind}">{msg}</div>', unsafe_allow_html=True)

def divider():
    st.markdown('<hr class="div">', unsafe_allow_html=True)

def nav(back_page, next_label="Continue", disabled=False):
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Back", use_container_width=True):
            go(back_page)
    with c2:
        clicked = st.button(next_label, use_container_width=True, disabled=disabled)
    return clicked

def first_nav(next_label="Continue"):
    _, c2 = st.columns([1, 1])
    with c2:
        return st.button(next_label, use_container_width=True)

def chart_start(label=""):
    st.markdown(f'<div class="chart-wrap"><div class="chart-lbl">{label}</div>', unsafe_allow_html=True)

def chart_end():
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS — DOMAIN
# ═══════════════════════════════════════════════════════════════
def calc_bmr(w, h, age, gender):
    return (10*w + 6.25*h - 5*age + 5) if gender == "Male" else (10*w + 6.25*h - 5*age - 161)

def bmi_cat(bmi):
    if bmi < 18.5: return "Underweight",  "p-yellow", "amber"
    if bmi < 25:   return "Normal weight","p-green",  "green"
    if bmi < 30:   return "Overweight",   "p-orange", "amber"
    return               "Obese",         "p-red",    "red"

def rolling_avg(data, w=7):
    return [float(np.mean(data[max(0, i-w+1):i+1])) for i in range(len(data))]

def cal_balance(weights):
    if len(weights) < 2: return 0.0
    w  = min(7, len(weights))
    ra = rolling_avg(weights, w)
    return (ra[-1] - ra[0]) / max(len(ra)-1, 1) * 7700

def smart_ylim(data, pad=0.35):
    mn, mx = min(data), max(data)
    span   = max(mx - mn, 0.8)
    return mn - span*pad, mx + span*pad

def mpl_style(bg="#fff"):
    plt.rcParams.update({
        "figure.facecolor": bg, "axes.facecolor": bg,
        "axes.edgecolor": "#E8E4DC", "axes.linewidth": 0.9,
        "axes.grid": True, "grid.color": "#F0EDE7",
        "grid.linewidth": 0.7, "grid.linestyle": "-",
        "xtick.color": "#B8B0A8", "ytick.color": "#B8B0A8",
        "xtick.labelsize": 8.5, "ytick.labelsize": 8.5,
        "font.family": "sans-serif", "text.color": "#1A1A1A",
        "legend.framealpha": 1, "legend.edgecolor": "#E8E4DC",
        "legend.facecolor": bg, "legend.fontsize": 8,
    })

def make_fig(w=7, h=3.5, bg="#fff"):
    mpl_style(bg)
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(bg)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    return fig, ax

# ═══════════════════════════════════════════════════════════════
# FOOD PLAN BUILDER
# ═══════════════════════════════════════════════════════════════
def build_meal_plan(goal, tdee, target_cal, diseases, weight_kg):
    """
    Returns a dict with breakfast / lunch / dinner / snack items
    tailored to goal and disease conditions.
    """
    intake = int(tdee + target_cal)   # daily kcal target

    has_diabetes   = "Type 2 Diabetes" in diseases or "Insulin Resistance / Pre-Diabetes" in diseases
    has_bp         = "Hypertension (High Blood Pressure)" in diseases
    has_chol       = "High Cholesterol (Dyslipidaemia)" in diseases
    has_thyroid    = "Hypothyroidism" in diseases
    has_pcos       = "Polycystic Ovary Syndrome (PCOS)" in diseases
    has_liver      = "Non-Alcoholic Fatty Liver Disease (NAFLD)" in diseases
    has_ckd        = "Chronic Kidney Disease (CKD)" in diseases

    # ── Staple carb choice
    if has_diabetes or has_pcos or has_liver:
        carb_grain = ("Brown rice / quinoa", "½ cup cooked (90 g)", 165)
    elif has_ckd:
        carb_grain = ("White rice (boiled)", "½ cup cooked (90 g)", 130)
    else:
        carb_grain = ("Whole wheat chapati", "2 medium (60 g)", 160)

    # ── Protein choice
    if has_ckd:
        protein_main = ("Egg whites (boiled)", "3 egg whites", 51)
    elif has_chol:
        protein_main = ("Skinless chicken breast (grilled)", "100 g", 165)
    else:
        protein_main = ("Moong dal / toor dal (cooked)", "150 g (1 katori)", 120)

    # ── Breakfast
    if has_diabetes or has_pcos:
        breakfast = [
            ("Oats (steel-cut, cooked)", "40 g dry / 1 bowl", 150),
            ("Boiled egg", "1 whole + 1 white", 100),
            ("Almonds", "10–12 nuts (15 g)", 90),
        ]
    elif has_thyroid:
        breakfast = [
            ("Poha / upma (wheat semolina)", "1 cup cooked", 180),
            ("Boiled eggs", "2 whole", 140),
            ("Brazil nuts", "2 nuts", 45),
        ]
    elif has_bp:
        breakfast = [
            ("Oats porridge (no salt)", "40 g dry / 1 bowl", 150),
            ("Banana (medium)", "1 fruit (120 g)", 105),
            ("Low-fat yoghurt", "100 g", 60),
        ]
    else:
        breakfast = [
            ("Whole wheat toast", "2 slices (60 g)", 160),
            ("Peanut butter (unsweetened)", "1 tbsp (16 g)", 95),
            ("Mixed fruit (papaya/guava)", "1 cup (150 g)", 65),
        ]

    # ── Lunch
    lunch = [
        carb_grain,
        ("Sabzi / stir-fried vegetables (any)", "1.5 cups cooked", 80),
        protein_main,
        ("Salad (cucumber + tomato + lemon)", "1 bowl, no salt if BP", 30) if has_bp
        else ("Green salad (cucumber + onion)", "1 bowl freely", 30),
    ]
    if has_chol or has_liver:
        lunch.append(("Flaxseed powder (sprinkled)", "1 tsp (5 g)", 27))

    # ── Dinner (lighter)
    if goal == "Lose Weight":
        dinner = [
            ("Moong dal soup (low salt)", "1 bowl (200 ml)", 100),
            ("Stir-fried vegetables", "2 cups freely", 80),
            ("Grilled paneer / tofu", "75 g", 90),
        ]
        if has_diabetes:
            dinner[0] = ("Palak / spinach soup", "1 bowl (200 ml)", 60)
    elif goal == "Gain Weight":
        dinner = [
            carb_grain,
            protein_main,
            ("Rajma / chickpeas (cooked)", "100 g", 170),
            ("Ghee (if no cholesterol issue)", "½ tsp", 20) if not has_chol
            else ("Olive oil drizzle", "½ tsp", 20),
        ]
    else:
        dinner = [
            carb_grain,
            ("Mixed vegetable sabzi", "1.5 cups", 90),
            protein_main,
        ]

    # ── Snacks
    if goal == "Gain Weight":
        snacks = [
            ("Banana + peanut butter", "1 banana + 1 tbsp PB", 195),
            ("Whole milk / soy milk", "1 glass (200 ml)", 120) if not has_chol else ("Skimmed milk", "1 glass (200 ml)", 70),
            ("Mixed nuts", "30 g handful", 180),
        ]
    elif goal == "Lose Weight":
        snacks = [
            ("Buttermilk / chaas (no salt if BP)", "1 glass (200 ml)", 35),
            ("Cucumber + carrot sticks", "freely", 40),
            ("Roasted chana", "20 g (small fistful)", 75),
        ]
    else:
        snacks = [
            ("Fruit (apple / pear / guava)", "1 medium", 80),
            ("Walnuts", "4 halves (15 g)", 98),
        ]
        if has_thyroid:
            snacks[0] = ("Apple (medium)", "1 fruit (150 g)", 78)

    return {
        "Breakfast (~7–9 AM)":  breakfast,
        "Lunch (~1–2 PM)":      lunch,
        "Snacks (~4–5 PM)":     snacks,
        "Dinner (~7–8 PM)":     dinner,
    }, intake

def render_meal_plan(meals, intake):
    slabel("What to eat — daily meal plan")
    st.markdown(
        f'<div class="callout">'
        f'<div class="callout-big">{intake}</div>'
        f'<div class="callout-detail">Target daily intake in <strong>kcal</strong><br>'
        f'Spread across 4 meal slots below.<br>'
        f'Quantities are for a ~70 kg adult — scale proportionally.</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    for meal_name, items in meals.items():
        meal_total = sum(kcal for _, _, kcal in items)
        html = (
            f'<div class="meal-card">'
            f'<div class="meal-head">{meal_name} &nbsp;·&nbsp; ~{meal_total} kcal</div>'
        )
        for food, qty, kcal in items:
            html += (
                f'<div class="meal-item">'
                f'<span>{food}</span>'
                f'<span style="display:flex;gap:10px">'
                f'<span class="meal-qty">{qty}</span>'
                f'<span class="meal-kcal">{kcal} kcal</span>'
                f'</span></div>'
            )
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# DISEASE COMPARISON RENDERER
# ═══════════════════════════════════════════════════════════════
def render_disease_comparison(diseases, goal):
    """Show side-by-side: healthy person rec vs person with conditions."""
    if not diseases:
        return

    slabel("How your conditions change the recommendations")

    for disease in diseases:
        info = DISEASE_NOTES.get(disease, {})
        if not info:
            continue

        st.markdown(
            f'<div style="font-size:0.8rem;font-weight:700;color:#7F1D1D;'
            f'margin:1.2rem 0 0.5rem 0;letter-spacing:0.3px">{disease}</div>',
            unsafe_allow_html=True,
        )

        avoid  = info.get("avoid", [])
        prefer = info.get("prefer", [])
        note   = info.get("note", "")

        html = '<div class="compare-grid">'

        # Healthy column
        html += '<div class="cg-col">'
        html += '<div class="cg-head healthy">Healthy person</div>'
        if goal == "Lose Weight":
            std = ["Moderate calorie deficit (300–500 kcal/day)", "High protein, high fibre", "Any whole grain as carb source", "Fruit freely as snacks"]
        elif goal == "Gain Weight":
            std = ["Calorie surplus (250–500 kcal/day)", "High protein + resistance training", "Whole grains, dairy, nuts, legumes", "3 main meals + 2–3 snacks"]
        else:
            std = ["Maintain TDEE intake", "Balanced macros — 50% carb, 25% protein, 25% fat", "Whole foods, minimal processing", "Hydration 35 ml/kg/day"]
        for s in std:
            html += f'<div class="cg-item">{s}</div>'
        html += "</div>"

        # With condition column
        html += '<div class="cg-col disease">'
        html += f'<div class="cg-head affected">With {disease.split("(")[0].strip()}</div>'
        for p in prefer:
            html += f'<div class="cg-item diff"><strong>Prefer:</strong> {p}</div>'
        for a in avoid:
            html += f'<div class="cg-item diff"><strong>Limit:</strong> {a}</div>'
        html += "</div>"

        html += "</div>"  # close compare-grid
        if note:
            html += f'<div class="alert a-warn" style="margin-top:4px;font-size:0.83rem">{note}</div>'
        st.markdown(html, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# GENERAL RECOMMENDATIONS BUILDER
# ═══════════════════════════════════════════════════════════════
def build_general_recs(goal, diseases, weight_kg):
    """Returns list of (text, is_disease_specific) tuples."""
    recs = []
    has_d = len(diseases) > 0

    if goal == "Lose Weight":
        recs += [
            ("Combine dietary reduction with increased physical activity — neither alone matches the effect of both together.", False),
            (f"Target protein at 1.8 g per kg — roughly <strong>{int(1.8 * weight_kg)} g/day</strong> — to preserve muscle while losing fat.", False),
            ("Walk at least 8,000–10,000 steps/day. A 30-min brisk walk burns ~150 kcal and requires no equipment.", False),
        ]
    elif goal == "Gain Weight":
        recs += [
            ("Eat in a surplus of 250–350 kcal/day. More than this increases fat gain disproportionately.", False),
            (f"Protein target: 2.0 g/kg — roughly <strong>{int(2.0 * weight_kg)} g/day</strong>. Spread across 4+ meals for best absorption.", False),
            ("Combine surplus eating with progressive resistance training 3–4×/week to steer gains towards lean mass.", False),
        ]
    else:
        recs += [
            ("Weigh yourself consistently — same time, same conditions, ideally every morning — to catch drift early.", False),
            ("7–9 hours of sleep is non-negotiable. Chronic sleep deficit raises ghrelin (hunger hormone) by up to 24%.", False),
            ("150 min/week of moderate aerobic exercise maintains cardiovascular health even with stable weight.", False),
        ]

    # Universal
    recs += [
        ("Limit ultra-processed foods — they are engineered to override your satiety signals and are the #1 driver of unintended weight gain.", False),
        (f"Drink roughly <strong>{int(35 * weight_kg)} ml of water/day</strong> ({int(35 * weight_kg / 250)} glasses). Thirst is frequently misread as hunger.", False),
    ]

    # Disease-specific additions
    if "Type 2 Diabetes" in diseases or "Insulin Resistance / Pre-Diabetes" in diseases:
        recs.append(("After every meal, take a 10–15 min walk. Post-meal walks reduce glucose spikes by 20–30% compared to sitting.", True))
        recs.append(("Never skip meals — especially breakfast. Skipping causes compensatory overeating and sharp glucose swings.", True))

    if "Hypertension (High Blood Pressure)" in diseases:
        recs.append(("Reduce sodium to under 1,500 mg/day. A single serving of packaged ramen can contain 2,000 mg — read labels.", True))
        recs.append(("Practice slow, diaphragmatic breathing for 5 min/day. Clinical studies show it lowers systolic BP by 4–7 mmHg.", True))

    if "High Cholesterol (Dyslipidaemia)" in diseases:
        recs.append(("Replace cooking oil with cold-pressed olive or mustard oil. Keep total fat under 25–30% of daily calories.", True))
        recs.append(("30 g of oats daily provides ~3 g of beta-glucan fibre — clinically shown to reduce LDL by 5–10%.", True))

    if "Hypothyroidism" in diseases:
        recs.append(("Take thyroid medication (levothyroxine) at least 30–60 min before food. Even coffee delays absorption.", True))
        recs.append(("Selenium (from 2 Brazil nuts/day) and zinc (from pumpkin seeds, lentils) support thyroid hormone conversion.", True))

    if "Polycystic Ovary Syndrome (PCOS)" in diseases:
        recs.append(("Resistance training 3×/week improves insulin sensitivity and reduces androgen levels more than cardio alone in PCOS.", True))
        recs.append(("Ground flaxseeds (1 tbsp/day in yoghurt or smoothie) provide lignans that help modulate excess androgens.", True))

    if "Non-Alcoholic Fatty Liver Disease (NAFLD)" in diseases:
        recs.append(("Even 5–7% body weight loss significantly reduces liver fat — this is the most impactful intervention for NAFLD.", True))
        recs.append(("Two cups of unsweetened coffee per day is associated with lower liver inflammation and slower fibrosis progression.", True))

    if "Chronic Kidney Disease (CKD)" in diseases:
        recs.append(("All CKD dietary changes must be verified with your nephrologist and a renal dietitian — individual lab values vary widely.", True))
        recs.append(("If on dialysis, protein needs actually increase significantly. Do not restrict without professional guidance.", True))

    return recs

# ═══════════════════════════════════════════════════════════════
# PAGE 1 — PERSONAL DETAILS
# ═══════════════════════════════════════════════════════════════
if st.session_state.page == "input":
    brand()
    progress_bar("input")
    title("Tell us about<br><em>yourself.</em>",
          "Height, weight, age and activity level form your metabolic baseline — the foundation of every recommendation.")

    slabel("Body measurements")
    c1, c2 = st.columns(2)
    with c1:
        height = st.number_input("Height (cm)", 100, 230, int(st.session_state.height), step=1)
        age    = st.number_input("Age",           10, 100, int(st.session_state.age),    step=1)
    with c2:
        weight = st.number_input("Current weight (kg)", 20.0, 300.0,
                                 float(st.session_state.weight), step=0.1, format="%.1f")
        gender = st.selectbox("Biological sex", ["Male", "Female"],
                              index=0 if st.session_state.gender == "Male" else 1)

    slabel("Activity level")
    activity = st.selectbox(
        "How active are you on a typical week?",
        list(ACTIVITY_MULT.keys()),
        index=list(ACTIVITY_MULT.keys()).index(st.session_state.activity)
              if st.session_state.activity in ACTIVITY_MULT else 0,
    )

    divider()
    if first_nav("Continue to health check"):
        st.session_state.height   = height
        st.session_state.weight   = weight
        st.session_state.age      = age
        st.session_state.gender   = gender
        st.session_state.activity = activity
        go("health_screen")

# ═══════════════════════════════════════════════════════════════
# PAGE 2 — LIFESTYLE DISEASE SCREENING  (NEW)
# ═══════════════════════════════════════════════════════════════
elif st.session_state.page == "health_screen":
    brand()
    progress_bar("health_screen")
    title("Do you have any<br><em>existing conditions?</em>",
          "Selecting a condition personalises your food recommendations and flags diet-drug interactions. "
          "Skip this if none apply.")

    alert(
        "This tool does <strong>not</strong> diagnose conditions. "
        "Selections here only adjust dietary guidance. Always follow your doctor's advice.",
        "neutral"
    )

    slabel("Common lifestyle conditions — select all that apply")

    diseases = st.multiselect(
        "Conditions:",
        ALL_DISEASES,
        default=st.session_state.diseases,
        label_visibility="collapsed",
    )

    if diseases:
        tags_html = "".join(f'<span class="dtag">{d}</span>' for d in diseases)
        st.markdown(f'<div class="disease-tags">{tags_html}</div>', unsafe_allow_html=True)
        alert(
            f"<strong>{len(diseases)} condition(s) selected.</strong> Your meal plan, "
            f"food recommendations, and general advice will be adapted accordingly. "
            f"A side-by-side comparison with a healthy person's plan will be shown in the final report.",
            "warn"
        )
    else:
        st.markdown('<div class="disease-tags"><span class="dtag dtag-none">None selected — standard recommendations apply</span></div>', unsafe_allow_html=True)

    divider()
    if nav("input", "Continue to metrics"):
        st.session_state.diseases = diseases
        go("metrics")

# ═══════════════════════════════════════════════════════════════
# PAGE 3 — BMI / BMR / TDEE
# ═══════════════════════════════════════════════════════════════
elif st.session_state.page == "metrics":
    brand()
    progress_bar("metrics")

    h  = st.session_state.height
    w  = st.session_state.weight
    a  = st.session_state.age
    g  = st.session_state.gender
    mult = ACTIVITY_MULT.get(st.session_state.activity, 1.2)

    bmi  = w / (h/100)**2
    bmr  = calc_bmr(w, h, a, g)
    tdee = bmr * mult
    st.session_state.bmr  = bmr
    st.session_state.tdee = tdee

    bmi_lbl, bmi_pill, card_col = bmi_cat(bmi)

    title("Your health<br><em>snapshot.</em>",
          "Three numbers that underpin every recommendation we make.")

    st.markdown(f"""
    <div class="cards">
      <div class="card {card_col}">
        <div class="c-lbl">BMI</div>
        <div class="c-val">{bmi:.1f}</div>
        <span class="pill {bmi_pill}">{bmi_lbl}</span>
        <div class="c-sub">Body mass index</div>
      </div>
      <div class="card">
        <div class="c-lbl">Resting BMR</div>
        <div class="c-val">{int(bmr)}<span class="c-unit">kcal</span></div>
        <div class="c-sub">Calories at complete rest</div>
      </div>
      <div class="card blue">
        <div class="c-lbl">TDEE</div>
        <div class="c-val">{int(tdee)}<span class="c-unit">kcal</span></div>
        <div class="c-sub">Total daily energy with activity</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # BMI spectrum
    slabel("Where you sit on the BMI spectrum")
    chart_start()
    fig_b, ax_b = make_fig(7, 1.05)
    zones = [(15,18.5,"#FEF9C3","Underweight"),(18.5,25,"#D1FAE5","Normal"),(25,30,"#FFEDD5","Overweight"),(30,40,"#FEE2E2","Obese")]
    for lo, hi, col, lbl in zones:
        ax_b.barh(0, hi-lo, left=lo, color=col, height=0.55, edgecolor="#E8E4DC", linewidth=0.6)
        ax_b.text((lo+hi)/2, -0.5, lbl, ha="center", va="top", fontsize=7.5, color="#A09888")
    ax_b.axvline(bmi, color="#1A1A1A", linewidth=2.5, zorder=5)
    ax_b.scatter([bmi], [0], s=80, color="#1A1A1A", zorder=6)
    ax_b.text(bmi, 0.38, f"  {bmi:.1f}", ha="left" if bmi<36 else "right",
              va="bottom", fontsize=9.5, fontweight="bold", color="#1A1A1A")
    ax_b.set_xlim(15,40); ax_b.set_ylim(-0.72,0.6); ax_b.set_yticks([])
    ax_b.set_xticks([18.5,25,30]); ax_b.set_xticklabels(["18.5","25","30"])
    ax_b.grid(False)
    for sp in ax_b.spines.values(): sp.set_visible(False)
    plt.tight_layout(pad=0.3)
    st.pyplot(fig_b, use_container_width=True)
    plt.close()
    chart_end()

    # TDEE donut
    slabel("Daily energy breakdown")
    chart_start()
    fig_d, ax_d = make_fig(4.5, 3.2)
    _, _, autotexts = ax_d.pie(
        [bmr, tdee-bmr],
        labels=["Base metabolism\n(BMR)", "Activity"],
        colors=["#1A1A1A","#C8E6D4"],
        autopct="%1.0f%%", startangle=90,
        wedgeprops={"linewidth":3,"edgecolor":"#fff","width":0.52},
        pctdistance=0.74, textprops={"fontsize":8.5},
    )
    for at in autotexts:
        at.set_color("white"); at.set_fontweight("bold"); at.set_fontsize(8.5)
    ax_d.text(0, 0, f"{int(tdee)}\nkcal", ha="center", va="center",
              fontsize=10, fontweight="bold", color="#1A1A1A", linespacing=1.5)
    plt.tight_layout()
    st.pyplot(fig_d, use_container_width=True)
    plt.close()
    chart_end()

    divider()
    if nav("health_screen", "Set my goal"):
        go("goal")

# ═══════════════════════════════════════════════════════════════
# PAGE 4 — GOAL
# ═══════════════════════════════════════════════════════════════
elif st.session_state.page == "goal":
    brand()
    progress_bar("goal")
    title("What are you<br><em>working towards?</em>",
          "Your goal shapes every calorie target and food recommendation from here on.")

    goal = st.radio(
        "",
        ["Maintain Weight", "Lose Weight", "Gain Weight"],
        index=["Maintain Weight","Lose Weight","Gain Weight"].index(st.session_state.goal),
        label_visibility="collapsed",
    )
    descs = {
        "Maintain Weight": ("info",    "Keep your current weight stable. We will track fluctuations and alert you if the trend drifts."),
        "Lose Weight":     ("success", "Achieve a calorie deficit through diet and movement. Safe upper limit: <strong>1 kg/week</strong>."),
        "Gain Weight":     ("warn",    "Build mass through a controlled surplus. Safe upper limit: <strong>0.5 kg/week</strong> to limit fat gain."),
    }
    k, msg = descs[goal]
    alert(msg, k)

    divider()
    if nav("metrics", "Continue"):
        st.session_state.goal = goal
        go("target")

# ═══════════════════════════════════════════════════════════════
# PAGE 5 — TARGET
# ═══════════════════════════════════════════════════════════════
elif st.session_state.page == "target":
    brand()
    progress_bar("target")
    goal = st.session_state.goal
    title("Define your<br><em>target.</em>",
          "How much do you want to change, and in how long?")

    ok = True
    target_calories = 0.0

    if goal == "Maintain Weight":
        alert(f"No change target needed. Your daily goal equals your TDEE: "
              f"<strong>{int(st.session_state.tdee)} kcal/day</strong>.", "info")
    else:
        slabel("Weight change goal")
        c1, c2 = st.columns(2)
        with c1:
            change = st.number_input("Weight change (kg)", 0.5, 50.0,
                                     float(st.session_state.target_weight_change), step=0.5, format="%.1f")
        with c2:
            weeks = st.number_input("Time frame (weeks)", 1, 104,
                                    int(st.session_state.target_weeks), step=1)

        rate  = change / weeks
        max_r = 1.0 if goal == "Lose Weight" else 0.5

        if rate > max_r:
            alert(f"Rate of <strong>{rate:.2f} kg/week</strong> exceeds safe limit of "
                  f"{max_r} kg/week. Please adjust.", "danger")
            ok = False
        else:
            daily_kcal      = (7700 * change) / (weeks * 7)
            target_calories = -daily_kcal if goal == "Lose Weight" else daily_kcal
            direction       = "deficit" if goal == "Lose Weight" else "surplus"
            intake          = int(st.session_state.tdee + target_calories)
            st.markdown(
                f'<div class="callout">'
                f'<div class="callout-big">{int(abs(daily_kcal))} kcal</div>'
                f'<div class="callout-detail">'
                f'Daily <strong>{direction}</strong> needed<br>'
                f'Target daily intake: <strong>{intake} kcal</strong><br>'
                f'Rate: {rate:.2f} kg/week'
                f'</div></div>',
                unsafe_allow_html=True,
            )
            st.session_state.target_weight_change = change
            st.session_state.target_weeks         = weeks
            st.session_state.target_calories      = target_calories

    divider()
    if nav("goal", "Continue", disabled=not ok):
        if goal == "Maintain Weight":
            st.session_state.target_calories = 0.0
        go("baseline")

# ═══════════════════════════════════════════════════════════════
# PAGE 6 — BASELINE WEIGHT LOG
# ═══════════════════════════════════════════════════════════════
elif st.session_state.page == "baseline":
    brand()
    progress_bar("baseline")
    title("Enter your<br><em>baseline weights.</em>",
          "7–14 days of past readings calibrate your trend accurately. Oldest reading first.")

    alert("Weigh daily at the same time — ideally morning, after bathroom, before eating. "
          "This consistency is more important than the exact time you choose.", "neutral")

    slabel("Daily readings — comma separated, oldest first")
    stored = ", ".join(str(x) for x in st.session_state.baseline_weights)
    raw = st.text_area(
        "Readings (kg):",
        value=stored,
        placeholder="e.g.  73.4, 73.0, 72.8, 73.1, 72.6, 72.4, 72.2",
        height=75,
        label_visibility="collapsed",
    )

    cg, _ = st.columns([1, 2])
    with cg:
        if st.button("Generate sample data", use_container_width=True):
            base  = st.session_state.weight
            trend = -0.07 if st.session_state.goal == "Lose Weight" else \
                     0.04 if st.session_state.goal == "Gain Weight" else 0.0
            sample = [round(base + trend*i + random.gauss(0, 0.22), 1) for i in range(14)]
            st.session_state.baseline_weights = sample
            st.rerun()

    weights, err = [], False
    if raw.strip():
        try:
            weights = [float(x.strip()) for x in raw.split(",") if x.strip()]
            if any(w < 20 or w > 300 for w in weights):
                alert("Some values look unrealistic. Please check.", "danger"); err = True
        except ValueError:
            alert("Could not parse. Use numbers separated by commas.", "danger"); err = True

    if weights and not err:
        n = len(weights)
        st.caption(f"{n} reading{'s' if n!=1 else ''} loaded — roughly {n} day{'s' if n!=1 else ''} of data.")
        if n < 7:
            alert("At least 7 readings give a more reliable trend. You can continue with fewer.", "warn")

        slabel("Baseline preview")
        chart_start("Daily readings + 3-day rolling average")
        d   = list(range(1, n+1))
        ra3 = rolling_avg(weights, min(3, n))
        ylo, yhi = smart_ylim(weights + ra3)

        fig_p, ax_p = make_fig(7, 2.5)
        ax_p.fill_between(d, weights, ylo, alpha=0.06, color="#2D6A4F")
        ax_p.plot(d, weights, color="#C8C3BB", linewidth=1.2, marker="o", markersize=4,
                  markerfacecolor="#2D6A4F", markeredgecolor="#2D6A4F", label="Daily weight")
        ax_p.plot(d, ra3, color="#2D6A4F", linewidth=2.0, label="3-day avg")
        ax_p.set_ylim(ylo, yhi)
        ax_p.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.1f"))
        ax_p.set_xlabel("Day", fontsize=8.5); ax_p.set_ylabel("Weight (kg)", fontsize=8.5)
        ax_p.legend()
        plt.tight_layout()
        st.pyplot(fig_p, use_container_width=True)
        plt.close()
        chart_end()

    divider()
    can_go = len(weights) >= 3 and not err
    if nav("target", "Continue", disabled=not can_go):
        st.session_state.baseline_weights = weights
        if not st.session_state.daily_weight_log:
            st.session_state.daily_weight_log = list(weights)
        go("tracker")
    if not can_go and raw.strip():
        st.caption("Need at least 3 valid readings to continue.")

# ═══════════════════════════════════════════════════════════════
# PAGE 7 — DAILY TRACKER
# ═══════════════════════════════════════════════════════════════
elif st.session_state.page == "tracker":
    brand()
    progress_bar("tracker")
    title("Daily<br><em>tracker.</em>",
          "Log today's weight and get a personalised nudge to stay on track.")

    log    = st.session_state.daily_weight_log
    target = st.session_state.target_calories
    goal   = st.session_state.goal
    diseases = st.session_state.diseases

    slabel("Today's weight reading")
    c_inp, c_btn = st.columns([3, 1])
    with c_inp:
        today_w = st.number_input(
            "Weight (kg)", 20.0, 300.0,
            value=float(log[-1]) if log else float(st.session_state.weight),
            step=0.1, format="%.1f", label_visibility="collapsed",
        )
    with c_btn:
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        if st.button("Log", use_container_width=True):
            st.session_state.daily_weight_log.append(today_w)
            log = st.session_state.daily_weight_log
            st.rerun()

    n = len(log)
    st.markdown(f"<p style='font-size:0.77rem;color:#B0A898;margin-top:-0.3rem'>{n} reading{'s' if n!=1 else ''} total</p>", unsafe_allow_html=True)

    # ── Daily recommendation ──
    if n >= 3:
        balance = cal_balance(log)
        diff    = balance - target
        slabel("Today's recommendation")

        if goal == "Maintain Weight":
            if abs(balance) < 150:
                alert("Your trend is well balanced. Keep your current habits.", "success")
            elif balance > 0:
                alert(f"Slight daily surplus (~<strong>{int(balance)} kcal</strong>). "
                      f"Try adding <strong>{int(balance*20):,} extra steps</strong> today.", "warn")
            else:
                alert(f"Slight daily deficit (~<strong>{int(abs(balance))} kcal</strong>). "
                      f"A small ~{int(abs(balance))} kcal snack would balance it.", "info")

        elif goal == "Lose Weight":
            if abs(diff) < 100:
                alert(f"Right on track. Estimated balance: <strong>{int(balance)} kcal/day</strong> vs target <strong>{int(target)} kcal/day</strong>.", "success")
            elif diff > 0:
                alert(f"Deficit is <strong>~{int(diff)} kcal smaller</strong> than planned. "
                      f"Try <strong>{int(diff*20):,} extra steps</strong> to compensate.", "warn")
            else:
                alert(f"Deficit is <strong>~{int(abs(diff))} kcal deeper</strong> than needed. "
                      f"A ~{int(abs(diff))} kcal protein-rich snack protects muscle mass.", "info")

        else:
            if abs(diff) < 100:
                alert(f"Surplus on target. Estimated: <strong>+{int(balance)} kcal/day</strong> vs target <strong>+{int(target)} kcal/day</strong>.", "success")
            elif diff < 0:
                alert(f"Surplus is <strong>~{int(abs(diff))} kcal lower</strong> than planned. Add a calorie-dense snack.", "warn")
            else:
                alert(f"Surplus is <strong>~{int(diff)} kcal higher</strong> than needed. A 20-min walk will bring it back on target.", "info")

        # Disease-specific daily tip
        if "Type 2 Diabetes" in diseases or "Insulin Resistance / Pre-Diabetes" in diseases:
            alert("Diabetes tip for today: Take a 10–15 min walk within 30 min of each meal to reduce post-meal glucose spikes.", "warn")
        if "Hypertension (High Blood Pressure)" in diseases:
            alert("BP tip for today: Check your sodium intake — aim to stay below 1,500 mg. Avoid pickles, sauces and packaged snacks.", "warn")

    # ── Weight trend chart (fixed y-axis) ──
    if n >= 2:
        slabel("Weight trend so far")
        chart_start("Daily readings + 7-day rolling average")
        ra  = rolling_avg(log, min(7, n))
        d   = list(range(1, n+1))
        ylo, yhi = smart_ylim(log + ra)   # ← zoomed, never starts at zero

        fig_t, ax_t = make_fig(7, 3.2)
        ax_t.fill_between(d, log, ylo, alpha=0.06, color="#2D6A4F")
        ax_t.plot(d, log, color="#C8C3BB", linewidth=1.2, marker="o", markersize=4.5,
                  markerfacecolor="#1A1A1A", markeredgecolor="#1A1A1A", label="Daily weight", zorder=3)
        ax_t.plot(d, ra, color="#1A1A1A", linewidth=2.4, label="7-day rolling avg", zorder=4)
        ax_t.set_ylim(ylo, yhi)           # ← critical: prevents flat-line bug
        ax_t.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.1f"))
        ax_t.set_xlabel("Day", fontsize=8.5); ax_t.set_ylabel("Weight (kg)", fontsize=8.5)
        ax_t.legend(loc="best")
        plt.tight_layout()
        st.pyplot(fig_t, use_container_width=True)
        plt.close()
        chart_end()

    divider()
    ready = n >= 5
    if nav("baseline", "View full report", disabled=not ready):
        go("analysis")
    if not ready:
        st.caption(f"Log {5-n} more reading(s) to unlock the full analysis.")

# ═══════════════════════════════════════════════════════════════
# PAGE 8 — FULL ANALYSIS REPORT
# ═══════════════════════════════════════════════════════════════
elif st.session_state.page == "analysis":
    brand()
    progress_bar("analysis")
    title("Your progress<br><em>report.</em>",
          f"Generated {datetime.today().strftime('%d %B %Y')}  ·  "
          f"{len(st.session_state.daily_weight_log)} days of data")

    log      = st.session_state.daily_weight_log
    target   = st.session_state.target_calories
    goal     = st.session_state.goal
    h        = st.session_state.height
    diseases = st.session_state.diseases
    w_kg     = st.session_state.weight
    tdee     = st.session_state.tdee

    days = list(range(1, len(log)+1))
    ra   = rolling_avg(log, min(7, len(log)))
    z    = np.polyfit(days, log, 1)
    p    = np.poly1d(z)

    total_change = log[-1] - log[0]
    weekly_rate  = (total_change / len(log)) * 7
    balance      = cal_balance(log)
    bmi_cur      = log[-1] / (h/100)**2
    bmi_lbl, bmi_pill, card_col = bmi_cat(bmi_cur)

    # ── Disease tag strip ─────────────────────────────
    if diseases:
        tags = "".join(f'<span class="dtag">{d}</span>' for d in diseases)
        st.markdown(f'<div class="disease-tags" style="margin-bottom:1.5rem">{tags}</div>',
                    unsafe_allow_html=True)

    # ─────────────────────────────────────────────────
    # 1 · WEIGHT TREND CHART
    # ─────────────────────────────────────────────────
    slabel("Weight trend over time")
    chart_start("Daily readings · 7-day rolling average · linear trend")
    all_v = log + ra + list(p(days))
    ylo, yhi = smart_ylim(all_v)

    fig1, ax1 = make_fig(7, 3.8)
    ax1.fill_between(days, log, ylo, alpha=0.05, color="#2D6A4F")
    ax1.plot(days, log, color="#C8C3BB", linewidth=1.2, marker="o", markersize=4.5,
             markerfacecolor="#1A1A1A", markeredgecolor="#1A1A1A",
             label="Daily weight", zorder=3)
    ax1.plot(days, ra, color="#1A1A1A", linewidth=2.6,
             label="7-day rolling avg", zorder=4)
    ax1.plot(days, p(days), linestyle="--", color="#B8B0A8", linewidth=1.2,
             label=f"Linear trend  ({z[0]:+.3f} kg/day)", zorder=2)
    ax1.set_ylim(ylo, yhi)
    ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.1f"))
    ax1.set_xlabel("Day", fontsize=8.5); ax1.set_ylabel("Weight (kg)", fontsize=8.5)
    ax1.legend(loc="best")
    plt.tight_layout()
    st.pyplot(fig1, use_container_width=True)
    plt.close()
    chart_end()

    # ─────────────────────────────────────────────────
    # 2 · SUMMARY CARDS
    # ─────────────────────────────────────────────────
    cc = "green" if (
        (goal=="Lose Weight" and total_change<0) or (goal=="Gain Weight" and total_change>0)
    ) else ("red" if (
        (goal=="Lose Weight" and total_change>0.2) or (goal=="Gain Weight" and total_change<-0.2)
    ) else "")

    st.markdown(f"""
    <div class="cards">
      <div class="card"><div class="c-lbl">Start</div>
        <div class="c-val">{log[0]:.1f}<span class="c-unit">kg</span></div>
        <div class="c-sub">Day 1</div></div>
      <div class="card"><div class="c-lbl">Current</div>
        <div class="c-val">{log[-1]:.1f}<span class="c-unit">kg</span></div>
        <div class="c-sub">Latest reading</div></div>
      <div class="card {cc}"><div class="c-lbl">Total change</div>
        <div class="c-val">{total_change:+.1f}<span class="c-unit">kg</span></div>
        <div class="c-sub">Over {len(log)} days</div></div>
      <div class="card"><div class="c-lbl">Weekly rate</div>
        <div class="c-val">{weekly_rate:+.2f}<span class="c-unit">kg/w</span></div>
        <div class="c-sub">From trend line</div></div>
    </div>
    """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────────
    # 3 · CALORIE BALANCE BAR CHART
    # ─────────────────────────────────────────────────
    slabel("Estimated daily calorie balance")
    wb = 5
    bal_s, bal_d = [], []
    for i in range(wb, len(log)):
        chunk = log[i-wb:i+1]
        bal_s.append((chunk[-1]-chunk[0])/wb * 7700)
        bal_d.append(i+1)

    if bal_s:
        chart_start("Rolling 5-day estimate — green = deficit, red = surplus")
        fig2, ax2 = make_fig(7, 3.2)
        bar_cols = ["#86EFAC" if b<0 else "#FCA5A5" for b in bal_s]
        ax2.bar(bal_d, bal_s, color=bar_cols, width=0.75, edgecolor="none", zorder=3)
        ax2.axhline(0, color="#D0CBC3", linewidth=0.9, zorder=2)
        if target != 0:
            ax2.axhline(target, color="#1A1A1A", linewidth=1.6, linestyle="--",
                        label=f"Target  ({int(target):+d} kcal/day)", zorder=4)
        gp = mpatches.Patch(color="#86EFAC", label="Deficit (losing weight)")
        rp = mpatches.Patch(color="#FCA5A5", label="Surplus (gaining weight)")
        handles = [gp, rp] + (ax2.get_legend_handles_labels()[0] if target!=0 else [])
        ax2.legend(handles=handles)
        ax2.set_xlabel("Day", fontsize=8.5); ax2.set_ylabel("kcal / day", fontsize=8.5)
        plt.tight_layout()
        st.pyplot(fig2, use_container_width=True)
        plt.close()
        chart_end()

    # ─────────────────────────────────────────────────
    # 4 · GOAL PROJECTION
    # ─────────────────────────────────────────────────
    if goal != "Maintain Weight":
        slabel("Goal projection")
        tc     = st.session_state.target_weight_change
        tw     = st.session_state.target_weeks
        t_end  = log[0] + (-tc if goal=="Lose Weight" else tc)
        total_p = tw * 7

        pdays      = list(range(1, total_p+1))
        i_slope    = (-tc if goal=="Lose Weight" else tc) / total_p
        proj_ideal  = [log[0]  + i_slope * d for d in pdays]
        proj_actual = [log[-1] + z[0] * (d - len(log)) for d in pdays]

        all_p = log + proj_ideal + proj_actual + [t_end]
        ylo_p, yhi_p = smart_ylim(all_p, pad=0.15)

        chart_start("Actual · ideal path · current-rate projection")
        fig3, ax3 = make_fig(7, 3.8)
        ax3.axhline(t_end, color="#2D6A4F", linewidth=1.1, linestyle="-.",
                    alpha=0.85, label=f"Goal weight  ({t_end:.1f} kg)", zorder=2)
        ax3.fill_between(days, log, ylo_p, alpha=0.05, color="#1A1A1A")
        ax3.plot(days,  log,         color="#1A1A1A", linewidth=2.8, label="Actual so far", zorder=5)
        ax3.plot(pdays, proj_ideal,  color="#B8B0A8", linewidth=1.4, linestyle="--", label="Ideal path", zorder=3)
        ax3.plot(pdays, proj_actual, color="#B92D2D", linewidth=1.4, linestyle=":",  label="At current rate", zorder=4)
        ax3.axvline(len(log), color="#E4E0D8", linewidth=1.0, zorder=1)
        ax3.text(len(log)+0.4, yhi_p-(yhi_p-ylo_p)*0.05, "today", fontsize=7.5, color="#B8B0A8")
        ax3.set_ylim(ylo_p, yhi_p)
        ax3.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.1f"))
        ax3.set_xlabel("Day", fontsize=8.5); ax3.set_ylabel("Weight (kg)", fontsize=8.5)
        ax3.legend(loc="best")
        plt.tight_layout()
        st.pyplot(fig3, use_container_width=True)
        plt.close()
        chart_end()

        if abs(z[0]) > 0.001:
            dl   = abs((log[-1]-t_end)/z[0])
            pd   = datetime.today() + timedelta(days=dl)
            pl   = total_p - len(log)
            id_  = datetime.today() + timedelta(days=max(pl,0))
            dd   = dl - pl
            if abs(dd) < 7:
                alert(f"At current pace you are <strong>right on schedule</strong> — projected goal date: <strong>{pd.strftime('%d %b %Y')}</strong>.", "success")
            elif dd < 0:
                alert(f"You are <strong>ahead of schedule</strong> — projected: <strong>{pd.strftime('%d %b %Y')}</strong>, planned: {id_.strftime('%d %b %Y')}.", "info")
            else:
                alert(f"Projected goal date: <strong>{pd.strftime('%d %b %Y')}</strong> — {int(dd)} days behind target of {id_.strftime('%d %b %Y')}. A small daily adjustment closes this gap.", "warn")

    # ─────────────────────────────────────────────────
    # 5 · CURRENT HEALTH STATUS
    # ─────────────────────────────────────────────────
    slabel("Current health status")
    st.markdown(f"""
    <div class="cards">
      <div class="card {card_col}">
        <div class="c-lbl">Current BMI</div>
        <div class="c-val">{bmi_cur:.1f}</div>
        <span class="pill {bmi_pill}">{bmi_lbl}</span>
        <div class="c-sub" style="margin-top:0.35rem">Based on latest reading</div>
      </div>
      <div class="card dark">
        <div class="c-lbl">Est. daily balance</div>
        <div class="c-val">{int(balance):+d}<span class="c-unit">kcal</span></div>
        <div class="c-sub">Derived from weight trend</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if bmi_cur < 18.5:
        alert("<strong>Underweight:</strong> Associated with nutritional deficiencies, weakened immunity, and low bone density. Increase intake with nutrient-dense foods, not empty calories.", "warn")
    elif bmi_cur < 25:
        alert("<strong>Healthy weight:</strong> Your BMI is in the normal range. Focus on maintaining this through sustainable habits rather than dramatic changes.", "success")
    elif bmi_cur < 30:
        alert("<strong>Overweight:</strong> Modest cardiovascular and metabolic risk. A 5–10% reduction in body weight produces clinically meaningful benefits.", "warn")
    else:
        alert("<strong>Obese range:</strong> Elevated risk of type 2 diabetes, hypertension, and cardiovascular disease. Structured guidance from a healthcare professional is strongly recommended.", "danger")

    # ─────────────────────────────────────────────────
    # 6 · MEAL PLAN  (NEW — food-specific, with quantities)
    # ─────────────────────────────────────────────────
    meals, intake_target = build_meal_plan(goal, tdee, target, diseases, w_kg)
    render_meal_plan(meals, intake_target)

    # ─────────────────────────────────────────────────
    # 7 · DISEASE COMPARISON  (NEW)
    # ─────────────────────────────────────────────────
    if diseases:
        render_disease_comparison(diseases, goal)

    # ─────────────────────────────────────────────────
    # 8 · GENERAL RECOMMENDATIONS
    # ─────────────────────────────────────────────────
    slabel("General recommendations")
    recs = build_general_recs(goal, diseases, w_kg)
    recs_html = ""
    for i, (text, is_disease) in enumerate(recs, 1):
        cls = "rec flagged" if is_disease else "rec"
        recs_html += (
            f'<div class="{cls}">'
            f'<span class="rec-n">{i:02d}</span>'
            f'<span>{text}</span>'
            f'</div>'
        )
    st.markdown(recs_html, unsafe_allow_html=True)

    if diseases:
        alert("Recommendations highlighted with a red border are specific to your selected condition(s). "
              "Always verify these with your doctor.", "warn")

    # ─────────────────────────────────────────────────
    # Restart
    # ─────────────────────────────────────────────────
    divider()
    _, col_r = st.columns([1, 1])
    with col_r:
        if st.button("Start over with new data", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    st.markdown(
        '<div class="footer">'
        'HEALTHLENS &nbsp;·&nbsp; B.Tech Project &nbsp;·&nbsp; '
        'Not a substitute for professional medical advice'
        '</div>',
        unsafe_allow_html=True,
    )