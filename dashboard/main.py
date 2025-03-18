import streamlit as st
import pandas as pd
import time
import datetime
import matplotlib.pyplot as plt
from src.backend import get_intraday_features, get_daily_features

st.title("📈 Stock Data Live Dashboard")

# User input
symbol = st.text_input("Enter stock symbol", value="IBM")
interval = st.selectbox("Select interval", ["1min", "5min", "15min", "30min", "60min"])

# UI placeholders
intraday_container = st.container()
daily_container = st.container()

# Current time display
current_time = st.empty()

# Function to create price chart
def plot_price_chart(df, title):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df.index, df['close'], label='Close Price', color='blue')
    ax.plot(df.index, df['open'], label='Open Price', color='green', alpha=0.7)
    ax.fill_between(df.index, df['high'], df['low'], alpha=0.2, color='gray', label='High-Low Range')
    ax.set_title(title)
    ax.set_ylabel('Price')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# Function to create volume chart
def plot_volume_chart(df, title):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(df.index, df['volume'].astype(float), color='purple', alpha=0.7)
    ax.set_title(title)
    ax.set_ylabel('Volume')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# Function to update data and charts
def update_dashboard():
    current_time.write(f"Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.write(f"Fetching latest data for {symbol}...")
    
    with intraday_container:
        st.subheader(f"Intraday Data ({interval})")
        intraday_data = get_intraday_features(symbol, interval)
        if intraday_data:
            df_intraday = pd.DataFrame(intraday_data)
            # Convert timestamp to datetime for proper sorting
            df_intraday['timestamp'] = pd.to_datetime(df_intraday['timestamp'])
            df_intraday = df_intraday.sort_values('timestamp', ascending=False)
            df_intraday.set_index('timestamp', inplace=True)
            
            # Convert string values to float for calculations
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df_intraday[col] = df_intraday[col].astype(float)
            
            # Display recent data
            st.dataframe(df_intraday.head(10))
            
            # Display charts
            st.pyplot(plot_price_chart(df_intraday.iloc[::-1].head(30), f"{symbol} Intraday Price"))
            st.pyplot(plot_volume_chart(df_intraday.iloc[::-1].head(30), f"{symbol} Intraday Volume"))
        else:
            st.error(f"Failed to retrieve intraday data for {symbol}")
    
    with daily_container:
        st.subheader("Daily Data")
        daily_data = get_daily_features(symbol)
        if daily_data:
            df_daily = pd.DataFrame(daily_data)
            # Convert date to datetime for proper sorting
            df_daily['date'] = pd.to_datetime(df_daily['date'])
            df_daily = df_daily.sort_values('date', ascending=False)
            df_daily.set_index('date', inplace=True)
            
            # Convert string values to float for calculations
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df_daily[col] = df_daily[col].astype(float)
            
            # Display recent data
            st.dataframe(df_daily.head(5))
            
            # Display charts
            st.pyplot(plot_price_chart(df_daily.iloc[::-1].head(30), f"{symbol} Daily Price (Last 30 Days)"))
            st.pyplot(plot_volume_chart(df_daily.iloc[::-1].head(30), f"{symbol} Daily Volume (Last 30 Days)"))
        else:
            st.error(f"Failed to retrieve daily data for {symbol}")

# Initialize dashboard
update_dashboard()

# Add a refresh button instead of automatic refresh
if st.button("Refresh Data"):
    update_dashboard()

# Schedule next automatic update
next_update = datetime.datetime.now() + datetime.timedelta(days=1)
next_update = next_update.replace(hour=0, minute=0, second=0)
st.info(f"Next automatic update scheduled for: {next_update.strftime('%Y-%m-%d %H:%M:%S')}")

# Only if you need automatic daily refresh (runs once per day)
if st.checkbox("Enable automatic daily refresh", value=False):
    st.write("Automatic daily refresh enabled. The app will refresh once every day.")
    
    # Calculate seconds until midnight
    now = datetime.datetime.now()
    tomorrow = now + datetime.timedelta(days=1)
    midnight = tomorrow.replace(hour=0, minute=0, second=0)
    seconds_until_midnight = (midnight - now).total_seconds()
    
    # Sleep until midnight, then update
    update_dashboard()