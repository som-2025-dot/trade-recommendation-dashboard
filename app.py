import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Telegram Bot Config
TELEGRAM_TOKEN = '8156042184:AAFwGAVgTL_A9k-khKet1fvrNk9lhLaHH3A'
TELEGRAM_CHAT_ID = '1111276484'

# Correct Google Sheet CSV Export Link
CSV_URL = 'https://docs.google.com/spreadsheets/d/1-J665_oi273DOwAX0lvSGWcx5pwPZ0A2RazLnrqGlKk/export?format=csv'

# Load data with cache
@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(CSV_URL)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['recommendation'] = df['recommendation'].fillna('None')
    return df

# Send Telegram alert
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        st.error(f"Failed to send Telegram message: {e}")

# UI Starts
st.title("📈 Live Trade Recommendation Dashboard")

df = load_data()

# Show Table
st.subheader("Latest Recommendations")
st.dataframe(df.style.set_properties(subset=["recommendation"], **{'white-space': 'nowrap'}), use_container_width=True)

# Plot Timeline Chart
st.subheader("Recommendation Timeline")
color_map = {'Buy': 'green', 'Hold': 'blue', 'Sell': 'red', 'None': 'gray'}

fig = px.scatter(
    df,
    x='datetime',
    y='recommendation',
    color='recommendation',
    color_discrete_map=color_map,
    title="Timeline of Buy/Hold/Sell Signals",
)

st.plotly_chart(fig, use_container_width=True)

# Telegram Alerts for New Recommendations
if 'last_count' not in st.session_state:
    st.session_state['last_count'] = 0

current_count = df.shape[0]

if current_count > st.session_state['last_count']:
    new_recos = current_count - st.session_state['last_count']
    send_telegram_message(f"🚨 {new_recos} New Recommendation(s) Added!")
    st.session_state['last_count'] = current_count

# Auto Refresh using meta tag
st.markdown(
    """
    <meta http-equiv="refresh" content="30">
    """,
    unsafe_allow_html=True
)

# Fix white patch via CSS
st.markdown(
    """
    <style>
    .dataframe td {
        background-color: transparent !important;
        color: white !important;
        max-width: 150px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    </style>
    """, unsafe_allow_html=True
)
