import streamlit as st
import time  # For loading animation
from PIL import Image

# Set Streamlit Page Config
st.set_page_config(
    page_title="Stock Vision",  
    page_icon="📉",  
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Custom CSS for Styling
st.markdown("""
    <style>
        body {
            background-color: #f5f5f5;
        }
        .main-title {
            text-align: center;
            color: #2E3B55;
            font-size: 45px;
            font-weight: bold;
        }
        .sub-title {
            text-align: center;
            font-size: 22px;
            color: #555;
            margin-bottom: 30px;
        }
        .service-card {
            background-color: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            text-align: center;
        }
        .service-card h4 {
            color: #2E3B55;
            font-size: 22px;
        }
        .service-card p {
            font-size: 16px;
            color: #666;
        }
        .footer {
            text-align: center;
            color: grey;
            margin-top: 50px;
            font-size: 14px;
        }
    </style>
""", unsafe_allow_html=True)

# Title Section with Animation
with st.empty():
    for _ in range(2):
        st.markdown("<h1 class='main-title'>Stock Vision Guide 📊</h1>", unsafe_allow_html=True)
        time.sleep(0.5)
        st.markdown("", unsafe_allow_html=True)
        time.sleep(0.5)

st.markdown("<h1 class='main-title'>Stock Vision Guide 📊</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='sub-title'>Get all the insights you need before investing in stocks!</h3>", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.header("📌 Navigation")
page = st.sidebar.radio("", ["🏠 Home", "📈 Stock Information", "🔮 Stock Prediction"])

# Display Stock Image
st.image("stock_market_image.png", use_container_width=True)

# Display Services
st.markdown("## 🌟 Our Key Services")
col1, col2 = st.columns(2)

services = [
    ("📈 Stock Information", "Access detailed stock data to make informed investment decisions."),
    ("🔮 Stock Prediction", "Explore 38-day predicted closing prices based on historical stock data.")
]

with col1:
    st.markdown(f"""
        <div class='service-card'>
            <h4>{services[0][0]}</h4>
            <p>{services[0][1]}</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class='service-card'>
            <h4>{services[1][0]}</h4>
            <p>{services[1][1]}</p>
        </div>
    """, unsafe_allow_html=True)

# Stock Information Section
if page == "📈 Stock Information":
    st.markdown("## 📈 Stock Information")
    st.write("##### Stock market investments require a deep understanding of market trends, company performance, and financial indicators. This page provides real-time stock data, historical performance, and analytical insights to help investors make informed decisions.")

    st.markdown("### 🔹 Key Features")
    st.markdown("📊 **Live & Historical Stock Data**")
    st.markdown("- Fetch **real-time stock prices, volume, and market trends** using Yahoo Finance API.")
    st.markdown("- Access **historical price movements** for trend analysis.")

    st.markdown("📈 **Technical Indicators & Market Trends**")
    st.markdown("- Analyze stock trends with **Moving Averages (SMA & EMA)** and **Relative Strength Index (RSI)**.")
    st.markdown("- Use **MACD and Bollinger Bands** for deeper market insights.")

    st.markdown("📌 **Stock Performance Tracking**")
    st.markdown("- Compare **multiple stocks** across different time periods.")
    st.markdown("- Identify **high/low price movements** and **volatility patterns**.")

    st.markdown("📊 **Interactive Data Visualization**")
    st.markdown("- Display **candlestick charts, line graphs, and moving averages** for better trend analysis.")
    st.markdown("- Use **interactive plots** to examine stock performance over custom date ranges.")

    st.markdown("📑 **Fundamental Data & Insights**")
    st.markdown("- Retrieve **market capitalization, P/E ratio, dividend yield, and earnings data**.")
    st.markdown("- Analyze **company performance metrics** alongside stock trends.")

    st.markdown("🔹 **Stay ahead of the market with real-time stock insights!**")



# Stock Prediction Section
if page == "🔮 Stock Prediction":
    st.markdown("## 🔮 Stock Prediction")
    st.write("##### Stock price prediction is a crucial tool for investors and traders to anticipate market movements. Using **AI-powered models**, we provide accurate and data-driven forecasts based on historical trends, technical indicators, and market patterns.")

    st.markdown("### 🔹 Key Features")
    st.markdown("- **AI-Based Stock Price Prediction**: Predicts future stock prices using an **LSTM (Long Short-Term Memory) model**.")
    st.markdown("- **User-Defined Stock Analysis**: Input stock symbol, select date range, and adjust model parameters.")
    st.markdown("- **Historical & Predicted Data Visualization**: Compare actual vs. predicted prices using interactive line charts.")
    st.markdown("- **Market Sentiment & External Factors**: Analyzes financial news, social media trends, and economic indicators.")
    st.markdown("- **Risk Assessment & Decision Support**: Evaluates stock volatility and provides buy/sell recommendations.")

    st.markdown("### 🔹 How to Use This Page?")
    st.markdown("1. **Enter a Stock Symbol** – Choose the stock you want to analyze.")
    st.markdown("2. **Select Date Range** – Choose a historical period for analysis and forecasting.")
    st.markdown("3. **Adjust Model Parameters** – Fine-tune the AI model for better accuracy.")
    st.markdown("4. **View Predictions** – Get AI-generated future stock price trends.")
    st.markdown("5. **Analyze Trends & Make Decisions** – Use insights for smarter investments.")

# Footer
st.markdown("""
    <hr>
    <p style='text-align: center; color: grey;'>© 2025 Stock Vision. All Rights Reserved.</p>
    <p style='text-align: center; color: grey;'>Our model is based on historical data from the last decade. As a result, the predicted prices may not fully capture the impact of other market factors that can influence actual prices.</p>
""", unsafe_allow_html=True)

