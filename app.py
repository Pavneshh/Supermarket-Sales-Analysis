import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Supermarket Sales Intelligence Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #0f1117;
    }

    #MainMenu, footer, header {visibility: hidden;}

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1300px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #262c36;
    }
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #FFFFFF;
    }
    section[data-testid="stSidebar"] label {
        color: #AAB2C0 !important;
        font-weight: 500;
        font-size: 0.85rem;
    }

    /* Multiselect / Selectbox */
    .stMultiSelect div[data-baseweb="select"] > div,
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1a1f29;
        border: 1px solid #262c36;
        border-radius: 8px;
        color: #FFFFFF;
    }
    .stMultiSelect span {
        background-color: rgba(0,229,255,0.15) !important;
        color: #00E5FF !important;
        border: 1px solid rgba(0,229,255,0.3);
        border-radius: 6px;
    }

    /* Hero section */
    .hero-container {
        background: linear-gradient(135deg, #161b22 0%, #1a1f29 100%);
        border: 1px solid #262c36;
        border-radius: 16px;
        padding: 2.2rem 2.5rem;
        margin-bottom: 1.8rem;
        position: relative;
        overflow: hidden;
    }
    .hero-container::before {
        content: "";
        position: absolute;
        top: -60px;
        right: -60px;
        width: 220px;
        height: 220px;
        background: radial-gradient(circle, rgba(0,229,255,0.18) 0%, rgba(0,229,255,0) 70%);
        border-radius: 50%;
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 1rem;
        color: #AAB2C0;
        margin-top: 0.4rem;
        font-weight: 400;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(0,229,255,0.12);
        color: #00E5FF;
        border: 1px solid rgba(0,229,255,0.3);
        border-radius: 20px;
        padding: 0.3rem 0.9rem;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        letter-spacing: 0.3px;
    }

    /* KPI Cards */
    .kpi-card {
        background: #1a1f29;
        border: 1px solid #262c36;
        border-radius: 14px;
        padding: 1.4rem 1.5rem;
        transition: all 0.25s ease;
        position: relative;
        overflow: hidden;
        height: 100%;
    }
    .kpi-card:hover {
        border-color: rgba(0,229,255,0.5);
        box-shadow: 0 0 24px rgba(0,229,255,0.15);
        transform: translateY(-3px);
    }
    .kpi-icon {
        font-size: 1.4rem;
        margin-bottom: 0.6rem;
        display: inline-block;
        background: rgba(0,229,255,0.1);
        padding: 0.5rem 0.65rem;
        border-radius: 10px;
    }
    .kpi-label {
        color: #AAB2C0;
        font-size: 0.82rem;
        font-weight: 500;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }
    .kpi-value {
        color: #FFFFFF;
        font-size: 1.65rem;
        font-weight: 700;
        margin-top: 0.2rem;
        letter-spacing: -0.5px;
    }
    .kpi-delta {
        color: #00E5FF;
        font-size: 0.78rem;
        font-weight: 600;
        margin-top: 0.35rem;
    }

    /* Section headers */
    .section-header {
        color: #FFFFFF;
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
        margin-top: 0.5rem;
    }
    .section-subtext {
        color: #AAB2C0;
        font-size: 0.85rem;
        margin-bottom: 1rem;
    }

    /* Chart container */
    .chart-card {
        background: #1a1f29;
        border: 1px solid #262c36;
        border-radius: 14px;
        padding: 1.2rem 1.3rem 0.6rem 1.3rem;
        margin-bottom: 1.2rem;
    }

    /* Dataframe */
    .stDataFrame {
        border: 1px solid #262c36;
        border-radius: 12px;
        overflow: hidden;
    }

    hr {
        border-color: #262c36;
    }

    ::-webkit-scrollbar { height: 8px; width: 8px; }
    ::-webkit-scrollbar-track { background: #161b22; }
    ::-webkit-scrollbar-thumb { background: #262c36; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA LOADING
# ============================================================
DATA_PATH = "data/final_supermarket_sales.csv"

@st.cache_data(show_spinner=False)
def load_data(path):
    df = pd.read_csv(path)

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    if "Total_Sales" not in df.columns:
        df["Total_Sales"] = df["Quantity Sold (kilo)"] * df["Unit Selling Price (RMB/kg)"]

    if "Month" not in df.columns and "Date" in df.columns:
        df["Month"] = df["Date"].dt.month_name()

    if "Weekday" not in df.columns and "Date" in df.columns:
        df["Weekday"] = df["Date"].dt.day_name()

    if "Hour" not in df.columns and "Time" in df.columns:
        df["Hour"] = pd.to_datetime(df["Time"], errors="coerce").dt.hour

    for col in ["Item Name", "Category Name", "Discount (Yes/No)", "Month", "Weekday"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    return df

try:
    df_raw = load_data(DATA_PATH)
    data_loaded = True
except Exception as e:
    data_loaded = False
    load_error = str(e)

if not data_loaded:
    st.error(f"Could not load dataset from `{DATA_PATH}`. Error: {load_error}")
    st.stop()

# ============================================================
# CACHED AGGREGATIONS
# ============================================================
@st.cache_data(show_spinner=False)
def filter_data(df, months, categories, discounts):
    filtered = df
    if months:
        filtered = filtered[filtered["Month"].isin(months)]
    if categories:
        filtered = filtered[filtered["Category Name"].isin(categories)]
    if discounts:
        filtered = filtered[filtered["Discount (Yes/No)"].isin(discounts)]
    return filtered

@st.cache_data(show_spinner=False)
def compute_kpis(df):
    total_revenue = df["Total_Sales"].sum()
    total_transactions = len(df)
    avg_transaction = df["Total_Sales"].mean() if total_transactions > 0 else 0
    if "Discount (Yes/No)" in df.columns and total_transactions > 0:
        discount_pct = (df["Discount (Yes/No)"].str.lower() == "yes").mean() * 100
    else:
        discount_pct = 0
    return total_revenue, avg_transaction, total_transactions, discount_pct

MONTH_ORDER = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]
WEEKDAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

@st.cache_data(show_spinner=False)
def monthly_revenue_trend(df):
    g = df.groupby("Month", as_index=False)["Total_Sales"].sum()
    g["Month"] = pd.Categorical(g["Month"], categories=MONTH_ORDER, ordered=True)
    g = g.sort_values("Month")
    return g

@st.cache_data(show_spinner=False)
def hourly_revenue(df):
    g = df.groupby("Hour", as_index=False)["Total_Sales"].sum().sort_values("Hour")
    return g

@st.cache_data(show_spinner=False)
def top_categories(df, n=10):
    g = df.groupby("Category Name", as_index=False)["Total_Sales"].sum()
    g = g.sort_values("Total_Sales", ascending=False).head(n)
    return g.sort_values("Total_Sales", ascending=True)

@st.cache_data(show_spinner=False)
def discount_breakdown(df):
    g = df.groupby("Discount (Yes/No)", as_index=False)["Total_Sales"].sum()
    return g

@st.cache_data(show_spinner=False)
def weekday_performance(df):
    g = df.groupby("Weekday", as_index=False)["Total_Sales"].sum()
    g["Weekday"] = pd.Categorical(g["Weekday"], categories=WEEKDAY_ORDER, ordered=True)
    g = g.sort_values("Weekday")
    return g

@st.cache_data(show_spinner=False)
def top_products(df, n=10):
    g = df.groupby("Item Name", as_index=False).agg(
        Revenue=("Total_Sales", "sum"),
        Quantity_Sold=("Quantity Sold (kilo)", "sum")
    )
    g = g.sort_values("Revenue", ascending=False).head(n)
    g["Revenue"] = g["Revenue"].round(2)
    g["Quantity_Sold"] = g["Quantity_Sold"].round(2)
    return g.reset_index(drop=True)

# ============================================================
# PLOTLY THEME HELPERS
# ============================================================
PLOTLY_BG = "#1a1f29"
ACCENT = "#00E5FF"
ACCENT_HOVER = "#00C8E0"
GRID_COLOR = "#262c36"
TEXT_COLOR = "#AAB2C0"

def apply_layout(fig, height=380):
    fig.update_layout(
        plot_bgcolor=PLOTLY_BG,
        paper_bgcolor=PLOTLY_BG,
        font=dict(family="Inter, sans-serif", color=TEXT_COLOR, size=12),
        margin=dict(l=10, r=10, t=10, b=10),
        height=height,
        hoverlabel=dict(bgcolor="#161b22", font_size=12, font_family="Inter", bordercolor=ACCENT),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_COLOR))
    )
    fig.update_xaxes(showgrid=False, color=TEXT_COLOR, linecolor=GRID_COLOR, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor=GRID_COLOR, color=TEXT_COLOR, zeroline=False)
    return fig

# ============================================================
# HERO HEADER
# ============================================================
st.markdown("""
<div class="hero-container">
    <span class="hero-badge">LIVE ANALYTICS</span>
    <div class="hero-title">🛒 Supermarket Sales Intelligence Dashboard</div>
    <div class="hero-subtitle">Interactive Analytics for Retail Performance</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR FILTERS
# ============================================================
with st.sidebar:
    st.markdown("### ⚙️ Filters")
    st.markdown("<div class='section-subtext'>Refine the dataset view</div>", unsafe_allow_html=True)

    available_months = [m for m in MONTH_ORDER if m in df_raw["Month"].unique()]
    selected_months = st.multiselect("📅 Month", options=available_months, default=[])

    available_categories = sorted(df_raw["Category Name"].dropna().unique().tolist())
    selected_categories = st.multiselect("🏷️ Category", options=available_categories, default=[])

    available_discounts = sorted(df_raw["Discount (Yes/No)"].dropna().unique().tolist())
    selected_discounts = st.multiselect("🎯 Discount", options=available_discounts, default=[])

    st.markdown("---")
    st.markdown(
        "<div style='color:#AAB2C0; font-size:0.78rem;'>Dataset: 878,503 records<br>Source: final_supermarket_sales.csv</div>",
        unsafe_allow_html=True
    )

df = filter_data(df_raw, selected_months, selected_categories, selected_discounts)

if len(df) == 0:
    st.warning("No data matches the selected filters. Please adjust your filters.")
    st.stop()

# ============================================================
# KPI SECTION
# ============================================================
total_revenue, avg_transaction, total_transactions, discount_pct = compute_kpis(df)

def format_currency(value):
    if value >= 1_000_000:
        return f"¥{value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"¥{value/1_000:.1f}K"
    return f"¥{value:.2f}"

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">💰</span>
        <div class="kpi-label">Total Revenue</div>
        <div class="kpi-value">{format_currency(total_revenue)}</div>
        <div class="kpi-delta">RMB across {len(df):,} records</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">📊</span>
        <div class="kpi-label">Avg Transaction Value</div>
        <div class="kpi-value">¥{avg_transaction:.2f}</div>
        <div class="kpi-delta">Per transaction</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">🧾</span>
        <div class="kpi-label">Total Transactions</div>
        <div class="kpi-value">{total_transactions:,}</div>
        <div class="kpi-delta">Filtered records</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">🎯</span>
        <div class="kpi-label">Discount Usage</div>
        <div class="kpi-value">{discount_pct:.1f}%</div>
        <div class="kpi-delta">Of all transactions</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 1.6rem;'></div>", unsafe_allow_html=True)

# ============================================================
# ROW 1: REVENUE TREND + HOURLY SALES
# ============================================================
col1, col2 = st.columns([1.3, 1])

with col1:
    st.markdown("<div class='section-header'>📈 Monthly Revenue Trend</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtext'>Total revenue across months</div>", unsafe_allow_html=True)
    mr = monthly_revenue_trend(df)

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=mr["Month"], y=mr["Total_Sales"],
        mode="lines+markers",
        line=dict(color=ACCENT, width=3, shape="spline"),
        marker=dict(size=7, color=ACCENT, line=dict(width=2, color="#0f1117")),
        fill="tozeroy",
        fillcolor="rgba(0,229,255,0.08)",
        hovertemplate="<b>%{x}</b><br>Revenue: ¥%{y:,.0f}<extra></extra>"
    ))
    fig_trend = apply_layout(fig_trend, height=380)
    st.plotly_chart(fig_trend, use_container_width=True)

with col2:
    st.markdown("<div class='section-header'>⏰ Peak Shopping Hours</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtext'>Revenue distribution by hour</div>", unsafe_allow_html=True)
    hr = hourly_revenue(df)

    fig_hour = go.Figure()
    fig_hour.add_trace(go.Bar(
        x=hr["Hour"], y=hr["Total_Sales"],
        marker=dict(
            color=hr["Total_Sales"],
            colorscale=[[0, "#163945"], [1, ACCENT]],
            line=dict(width=0)
        ),
        hovertemplate="<b>Hour %{x}:00</b><br>Revenue: ¥%{y:,.0f}<extra></extra>"
    ))
    fig_hour = apply_layout(fig_hour, height=380)
    st.plotly_chart(fig_hour, use_container_width=True)

# ============================================================
# ROW 2: TOP CATEGORIES + DISCOUNT IMPACT
# ============================================================
col3, col4 = st.columns([1.3, 1])

with col3:
    st.markdown("<div class='section-header'>🏆 Top Categories by Revenue</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtext'>Top 10 performing categories</div>", unsafe_allow_html=True)
    tc = top_categories(df, 10)

    fig_cat = go.Figure()
    fig_cat.add_trace(go.Bar(
        x=tc["Total_Sales"], y=tc["Category Name"],
        orientation="h",
        marker=dict(
            color=tc["Total_Sales"],
            colorscale=[[0, "#163945"], [1, ACCENT]],
            line=dict(width=0)
        ),
        hovertemplate="<b>%{y}</b><br>Revenue: ¥%{x:,.0f}<extra></extra>"
    ))
    fig_cat = apply_layout(fig_cat, height=400)
    fig_cat.update_yaxes(showgrid=False)
    st.plotly_chart(fig_cat, use_container_width=True)

with col4:
    st.markdown("<div class='section-header'>🎯 Discount Impact</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtext'>Discount vs non-discount sales</div>", unsafe_allow_html=True)
    db = discount_breakdown(df)

    fig_donut = go.Figure(data=[go.Pie(
        labels=db["Discount (Yes/No)"],
        values=db["Total_Sales"],
        hole=0.65,
        marker=dict(colors=[ACCENT, "#262c36"], line=dict(color="#1a1f29", width=3)),
        textinfo="percent",
        textfont=dict(color="#FFFFFF", size=13, family="Inter"),
        hovertemplate="<b>%{label}</b><br>Revenue: ¥%{value:,.0f}<extra></extra>"
    )])
    fig_donut.update_layout(
        annotations=[dict(text="Revenue<br>Split", x=0.5, y=0.5, font_size=14,
                           font_color="#FFFFFF", showarrow=False, font_family="Inter")]
    )
    fig_donut = apply_layout(fig_donut, height=400)
    st.plotly_chart(fig_donut, use_container_width=True)

# ============================================================
# ROW 3: WEEKDAY PERFORMANCE
# ============================================================
st.markdown("<div class='section-header'>📅 Weekday Performance Analysis</div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtext'>Sales distribution across the week</div>", unsafe_allow_html=True)

wp = weekday_performance(df)

fig_week = go.Figure()
fig_week.add_trace(go.Bar(
    x=wp["Weekday"], y=wp["Total_Sales"],
    marker=dict(
        color=wp["Total_Sales"],
        colorscale=[[0, "#163945"], [1, ACCENT]],
        line=dict(width=0)
    ),
    hovertemplate="<b>%{x}</b><br>Revenue: ¥%{y:,.0f}<extra></extra>"
))
fig_week = apply_layout(fig_week, height=340)
st.plotly_chart(fig_week, use_container_width=True)

# ============================================================
# ROW 4: TOP PRODUCTS TABLE
# ============================================================
st.markdown("<div class='section-header'>🛍️ Top Products</div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtext'>Top 10 products by revenue</div>", unsafe_allow_html=True)

tp = top_products(df, 10)
tp_display = tp.rename(columns={
    "Item Name": "Product Name",
    "Revenue": "Revenue (¥)",
    "Quantity_Sold": "Quantity Sold (kg)"
})

st.dataframe(
    tp_display.style.format({"Revenue (¥)": "¥{:,.2f}", "Quantity Sold (kg)": "{:,.2f}"}),
    use_container_width=True,
    height=400
)

st.markdown(
    "<div style='text-align:center; color:#AAB2C0; font-size:0.8rem; margin-top:2rem;'>"
    "Built with Streamlit & Plotly · Supermarket Sales Intelligence Dashboard"
    "</div>",
    unsafe_allow_html=True
)