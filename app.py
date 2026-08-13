import streamlit as st
import pandas as pd

# पेज सेटअप
st.set_page_config(page_title="Quantum Terminal", layout="wide", page_icon="📈")

# साइडबार (Settings & Navigation)
st.sidebar.header("⚙️ Broker Settings")
api_key = st.sidebar.text_input("API Key", type="password")
api_secret = st.sidebar.text_input("API Secret", type="password")

if st.sidebar.button("Save Configuration"):
    st.sidebar.success("Credentials Saved. System Ready.")

st.sidebar.markdown("---")
st.sidebar.write("🟢 Status: Live & Connected")
st.sidebar.write("⚡ Mode: Paper Trading")

# मुख्य डैशबोर्ड
st.title("Quantum Terminal")
st.write("Welcome back, Trader.")

# टॉप मेट्रिक्स
col1, col2, col3 = st.columns(3)
col1.metric(label="Total P&L", value="₹24,780", delta="+12%")
col2.metric(label="Available Capital", value="₹2,00,000", delta="100% Free")
col3.metric(label="Active Strategy", value="Options Scalper", delta="Running", delta_color="normal")

st.markdown("---")

# मार्केट वॉचलिस्ट (Live Data UI)
st.subheader("📊 Markets Watchlist")
market_data = pd.DataFrame({
    "Symbol": ["NIFTY 50", "BANKNIFTY", "FINNIFTY"],
    "LTP": ["24,350.10", "52,100.50", "23,110.00"],
    "Change (%)": ["+0.45", "-0.15", "+0.20"]
})
st.dataframe(market_data, use_container_width=True, hide_index=True)

st.markdown("---")

# ट्रेड हिस्ट्री
st.subheader("🚨 Active Live Trades")
st.info("No active positions currently. Waiting for trigger...")
