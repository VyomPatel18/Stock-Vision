import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta

# Load the trained LSTM model
@st.cache_resource()
def load_model():
    return tf.keras.models.load_model("lstm_stock_model.keras")

model = load_model()
scaler = MinMaxScaler(feature_range=(0, 1))

def get_stock_data(symbol, start_date, end_date):
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    return stock_data

def get_stock_details(symbol):
    stock = yf.Ticker(symbol)
    return stock.info

# Preprocess Data for Prediction
def prepare_data(data):
    data_scaled = scaler.fit_transform(data[['Close']].values.reshape(-1, 1))
    X_test = []
    for i in range(60, len(data_scaled)):
        X_test.append(data_scaled[i-60:i, 0])
    return np.array(X_test).reshape(-1, 60, 1)

def predict_stock_price(model, data):
    predictions = model.predict(data)
    return scaler.inverse_transform(predictions)

# Streamlit UI
st.title("📈 Stock Price Prediction using LSTM")

with st.sidebar:
    symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, TSLA, INFY.NS):", "AAPL")
    start_date = st.date_input("Select Start Date:", datetime.now() - timedelta(days=365))
    end_date = st.date_input("Select End Date:", datetime.now())
    
    if symbol:
        stock_info = get_stock_details(symbol)
        if stock_info:
            st.subheader("Stock Details")
            st.write(f"**Name:** {stock_info.get('longName', 'N/A')}")
            st.write(f"**Sector:** {stock_info.get('sector', 'N/A')}")
            st.write(f"**Industry:** {stock_info.get('industry', 'N/A')}")
            st.write(f"**Market Cap:** {stock_info.get('marketCap', 'N/A')}")
            st.write(f"**Previous Close:** {stock_info.get('previousClose', 'N/A')}")
            st.write(f"**Open Price:** {stock_info.get('open', 'N/A')}")
            st.write(f"**52-Week High:** {stock_info.get('fiftyTwoWeekHigh', 'N/A')}")
            st.write(f"**52-Week Low:** {stock_info.get('fiftyTwoWeekLow', 'N/A')}")
            st.write(f"**Dividend Yield:** {stock_info.get('dividendYield', 'N/A')}")

if st.button("Predict Stock Prices"):
    st.write(f"Fetching data for {symbol}...")
    stock_data = get_stock_data(symbol, start_date, end_date)
    
    if not stock_data.empty:
        st.write("Stock Data Preview:")
        st.dataframe(stock_data.tail(10))
        
        # Preparing data for prediction
        X_test = prepare_data(stock_data)
        predictions = predict_stock_price(model, X_test)
        
        # Append predictions to stock data
        stock_data = stock_data.iloc[60:]
        stock_data['Predicted Close'] = predictions
        
        # Plot Results
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(stock_data.index, stock_data['Close'], label="Actual Price", color='blue')
        ax.plot(stock_data.index, stock_data['Predicted Close'], label="Predicted Price", linestyle='dashed', color='red')
        ax.set_title(f"Stock Price Prediction for {symbol}")
        ax.legend()
        st.pyplot(fig)
    else:
        st.error("Invalid Stock Symbol or No Data Available!")
