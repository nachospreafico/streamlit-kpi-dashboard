import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------
# Page setup (theme-friendly)
# -----------------------------
st.set_page_config(
    page_title="Business KPI Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Header
# -----------------------------
st.title("📊 Business KPI Dashboard")
st.subheader("Monitor key performance indicators like revenue, profit, and conversion over time.")
st.write(
    "A simple interactive dashboard that tracks key business metrics — revenue, profit, and conversion rate — "
    "over time. Built with Streamlit to demonstrate real-time data updates and visualization fundamentals."
)

# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.header("Controls")
window_label = st.sidebar.selectbox(
    "Time window",
    ["Last 7 days", "Last 14 days", "Last 30 days", "All"],
    index=2
)

# Optional: regenerate the mock dataset for demo purposes
if "seed" not in st.session_state:
    st.session_state.seed = 42
if st.sidebar.button("🔄 Regenerate Data"):
    st.session_state.seed += 1

rng = np.random.default_rng(st.session_state.seed)

# -----------------------------
# Generate mock data (Oct 2025)
# -----------------------------
dates = pd.date_range(start="2025-10-01", end="2025-10-31")
df = pd.DataFrame({
    "Date": dates,
    "Revenue": rng.integers(3000, 8000, size=len(dates)),
    "Profit": rng.integers(500, 2000, size=len(dates)),
    "Conversion Rate": rng.uniform(2, 8, size=len(dates)).round(2),
})

# -----------------------------
# Time-window filtering
# -----------------------------
window_days = {"Last 7 days": 7, "Last 14 days": 14, "Last 30 days": 30, "All": None}[window_label]
if window_days is None:
    df_f = df.copy()
else:
    start_date = df["Date"].max() - pd.Timedelta(days=window_days - 1)
    df_f = df[df["Date"] >= start_date].copy()

st.caption(f"Showing: **{window_label}** — Range: {df_f['Date'].min().date()} → {df_f['Date'].max().date()}")

# -----------------------------
# KPI row (today vs yesterday)
# -----------------------------
if len(df_f) >= 2:
    today_row = df_f.iloc[-1]
    yday_row = df_f.iloc[-2]

    rev_today, rev_yday = today_row["Revenue"], yday_row["Revenue"]
    prof_today, prof_yday = today_row["Profit"], yday_row["Profit"]
    conv_today, conv_yday = today_row["Conversion Rate"], yday_row["Conversion Rate"]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Revenue", f"{rev_today:,.0f}", f"{(rev_today - rev_yday):+,.0f}")
    with col2:
        st.metric("Profit", f"{prof_today:,.0f}", f"{(prof_today - prof_yday):+,.0f}")
    with col3:
        st.metric("Conversion Rate", f"{conv_today:.2f}%", f"{(conv_today - conv_yday):+.2f} pp")
else:
    col1, col2, col3 = st.columns(3, border=True)
    with col1: st.metric("Revenue", "—", "—")
    with col2: st.metric("Profit", "—", "—")
    with col3: st.metric("Conversion Rate", "—", "—")

st.divider()

# -----------------------------
# Trend charts (theme-friendly)
# -----------------------------
left, right = st.columns([2, 1])

with left:
    st.subheader("Revenue & Profit (Trend)")
    st.line_chart(df_f.set_index("Date")[["Revenue", "Profit"]])

with right:
    st.subheader("Conversion Rate (Trend)")
    st.line_chart(df_f.set_index("Date")[["Conversion Rate"]])

st.divider()

# -----------------------------
# Data table + download
# -----------------------------
st.subheader("Underlying Data")
st.dataframe(df_f.assign(Date=df_f["Date"].dt.strftime("%Y-%m-%d")))
csv = df_f.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "kpi_data.csv", "text/csv")

# -----------------------------
# About / Footer
# -----------------------------
st.divider()
with st.expander("ℹ️ About this mini-project", expanded=False):
    st.markdown(
        """
**What this shows:**  
- Streamlit layout basics (`columns`, `sidebar`, `expander`)  
- KPI cards with deltas (`st.metric`)  
- Interactive filtering (time window)  
- Line charts driven by a filtered `DataFrame`  
- CSV download for reproducibility

**Tech:** Python · pandas · NumPy · Streamlit

**Try it yourself:** Clone, run `streamlit run app.py`, and tweak ranges/metrics.
        """
    )
