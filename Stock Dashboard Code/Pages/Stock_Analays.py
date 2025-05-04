
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import ta
import datetime

# Setting page config
st.set_page_config(page_title="Stock Analysis", page_icon="📊", layout="wide")

# Title
st.title("Stock Analysis 📊")

# Layout for input fields
col1, col2, col3 = st.columns(3)

# Get today's date
today = datetime.date.today()

with col1:
    ticker = st.text_input("Stock Ticker", "AAPL").upper()
with col2:
    start_date = st.date_input("Choose Start Date", today - datetime.timedelta(days=365))
with col3:
    end_date = st.date_input("Choose End Date", today)

st.write("(Stock Symbols : AAPL, ADANIENT.BO, GOOG, NVDA, TSLA, TCS.NS, TATASTEEL.BO)")

# Fetch stock data
data = yf.download(ticker, start=start_date, end=end_date)

if data.empty:
    st.error("No data found. Please check the stock ticker and date range.")
    st.stop()

# Display stock information
st.subheader(f"{ticker} Stock Overview")
stock = yf.Ticker(ticker)
info = stock.info

if "longBusinessSummary" in info:
    st.write(info["longBusinessSummary"])
if "sector" in info:
    st.write("**Sector:**", info["sector"])
if "fullTimeEmployees" in info:
    st.write("**Employees:**", info["fullTimeEmployees"])
if "website" in info:
    st.write("**Website:**", info["website"])

# Display Market Metrics & Financial Ratios
col1, col2 = st.columns(2)

with col1:
    market_metrics = {
        "Market Cap": info.get("marketCap", "N/A"),
        "Beta": info.get("beta", "N/A"),
        "EPS": info.get("trailingEps", "N/A"),
        "PE Ratio": info.get("trailingPE", "N/A"),
    }
    st.write("### Market Metrics")
    st.table(pd.DataFrame(market_metrics, index=["Value"]).T)

with col2:
    financial_ratios = {
        "Quick Ratio": info.get("quickRatio", "N/A"),
        "Revenue per Share": info.get("revenuePerShare", "N/A"),
        "Profit Margins": info.get("profitMargins", "N/A"),
        "Debt to Equity": info.get("debtToEquity", "N/A"),
        "Return on Equity": info.get("returnOnEquity", "N/A"),
    }
    st.write("### Financial Ratios")
    st.table(pd.DataFrame(financial_ratios, index=["Value"]).T)

# # Display latest price changes
# col1, col2, col3 = st.columns(3)

# if len(data['Close']) >= 2:
#     latest_close = round(float(data['Close'].iloc[-1]), 2)
#     prev_close = round(float(data['Close'].iloc[-2]), 2)
#     daily_change = latest_close - prev_close
#     col1.metric("Last Close Price", f"${latest_close}", f"{daily_change:+.2f}")
# else:
#     col1.warning("Not enough data for daily change.")


# Fetch stock currency
currency = info.get("currency", "USD")  # Default to USD if not found
currency_symbol_map = {
    "USD": "$", "EUR": "€", "GBP": "£", "INR": "₹", "JPY": "¥", "CNY": "¥",
    "AUD": "A$", "CAD": "C$", "CHF": "CHF", "HKD": "HK$", "SGD": "S$"
}
currency_symbol = currency_symbol_map.get(currency, currency)  # Use currency code if symbol not found

# Display latest price changes
col1, col2, col3 = st.columns(3)

if len(data['Close']) >= 2:
    latest_close = round(float(data['Close'].iloc[-1]), 2)
    prev_close = round(float(data['Close'].iloc[-2]), 2)
    daily_change = latest_close - prev_close
    col1.metric("Last Close Price", f"{currency_symbol}{latest_close}", f"{daily_change:+.2f}")
else:
    col1.warning("Not enough data for daily change.")


# Display historical data (Last 10 days)
st.write("### Historical Data (Last 10 Days)")
st.dataframe(data.tail(10).round(2))

# Chart selection
col1, col2, col3 = st.columns([1, 2, 2])

with col1:
    chart_type = st.selectbox("Chart Type", ["Candlestick", "Line"])
    
with col2:
    indicators = st.selectbox("Indicator", ["None", "RSI", "MACD", "Moving Average"])
with col3:
    period = st.selectbox("Time Period", ["5d", "1mo", "6mo", "YTD", "1y", "5y", "max"], index=4)

# Fetch historical data for the selected period
data = stock.history(period=period)

### === DEFINE INDICATOR FUNCTIONS === ###
def compute_rsi(data, window=14):
    """Calculate and plot RSI"""
    data["RSI"] = ta.momentum.RSIIndicator(data["Close"], window=window).rsi()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data["RSI"], mode="lines", name="RSI"))
    fig.update_layout(title="Relative Strength Index (RSI)", yaxis_title="RSI Value")
    return fig

def compute_macd(data):
    """Calculate and plot MACD"""
    macd = ta.trend.MACD(data["Close"])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=macd.macd(), mode="lines", name="MACD"))
    fig.add_trace(go.Scatter(x=data.index, y=macd.macd_signal(), mode="lines", name="Signal Line"))
    fig.update_layout(title="MACD Indicator", yaxis_title="MACD Value")
    return fig

def compute_moving_average(data, window=50):
    """Calculate and plot Moving Average"""
    data[f"SMA_{window}"] = data["Close"].rolling(window=window).mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data["Close"], mode="lines", name="Close Price"))
    fig.add_trace(go.Scatter(x=data.index, y=data[f"SMA_{window}"], mode="lines", name=f"{window}-Day SMA"))
    fig.update_layout(title=f"{window}-Day Moving Average", yaxis_title="Price")
    return fig

# Plot Candlestick Chart
def plot_candlestick(data):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name="Candlestick"
    ))
    fig.update_layout(title="Candlestick Chart", xaxis_title="Date", yaxis_title="Price",  height=600)
    return fig

# Plot Line Chart
def plot_line_chart(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name="Close Price"))
    fig.update_layout(title="Stock Price Trend", xaxis_title="Date", yaxis_title="Price",  height=600)
    return fig

# Display the selected chart
if chart_type == "Candlestick":
    st.plotly_chart(plot_candlestick(data), use_container_width=True)
else:
    st.plotly_chart(plot_line_chart(data), use_container_width=True)

# Display Selected Indicator
if indicators == "RSI":
    st.plotly_chart(compute_rsi(data), use_container_width=True)
elif indicators == "MACD":
    st.plotly_chart(compute_macd(data), use_container_width=True)
elif indicators == "Moving Average":
    st.plotly_chart(compute_moving_average(data, window=50), use_container_width=True)

# Footer
st.markdown("""
    <hr>
    <p style='text-align: center; color: grey;'>© 2025 Stock Vision. All Rights Reserved.</p>
    <p style='text-align: center; color: grey;'>Our model is based on historical data from the last decade. As a result, the predicted prices may not fully capture the impact of other market factors that can influence actual prices.</p>
""", unsafe_allow_html=True)











