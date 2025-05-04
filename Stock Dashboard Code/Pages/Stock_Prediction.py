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
    return tf.keras.models.load_model("Model/lstm_stock_model.keras")

model = load_model()
scaler = MinMaxScaler(feature_range=(0, 1))

def get_stock_data(symbol, start_date, end_date):
    return yf.download(symbol, start=start_date, end=end_date)

def get_stock_details(symbol):
    return yf.Ticker(symbol).info

# Preprocess Data for Prediction
def prepare_data(data):
    data_scaled = scaler.fit_transform(data[['Close']].values.reshape(-1, 1))
    X_test = [data_scaled[i-60:i, 0] for i in range(60, len(data_scaled))]
    return np.array(X_test).reshape(-1, 60, 1)

def predict_stock_price(model, data):
    predictions = model.predict(data)
    return scaler.inverse_transform(predictions)

def predict_future_prices(model, last_60_days, days=5):
    future_prices = []
    input_sequence = last_60_days.copy()
    for _ in range(days):
        input_scaled = scaler.transform(input_sequence.reshape(-1, 1)).reshape(1, 60, 1)
        predicted_price = scaler.inverse_transform(model.predict(input_scaled))[0][0]
        future_prices.append(predicted_price)
        input_sequence = np.roll(input_sequence, -1)
        input_sequence[-1] = predicted_price
    return future_prices

# Streamlit UI Styling
st.markdown("""
    <style>
        .main-title { text-align: center; font-size: 36px; font-weight: bold; color: #2E86C1; }
        .sub-title { text-align: center; font-size: 20px; color: #566573; }
        .stock-card { background-color: #F2F3F4; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>📈 Stock Price Prediction</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='sub-title'>Analyze stock trends and predict future prices.</h3>", unsafe_allow_html=True)

# Section Selection
section = st.radio("Choose Prediction Mode:", ("Auto Price Prediction", "Manual Price Prediction"), horizontal=True)

if section == "Auto Price Prediction":
    col1, col2, col3 = st.columns(3)
    with col1:
        symbol = st.text_input("Stock Symbol", "AAPL")
    with col2:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=3650))
    with col3:
        end_date = st.date_input("End Date", max_value=datetime.today()) #datetime.now()

    st.write("(Stock Symbols : AAPL, ADANIENT.BO, GOOG, NVDA, TSLA, TCS.NS, TATASTEEL.BO)")

    if st.button("🔍 Predict Stock Prices"):
        stock_data = get_stock_data(symbol, start_date, end_date)
        if not stock_data.empty:
            stock_info = get_stock_details(symbol)
            currency_symbol = stock_info.get('currency', 'USD')
            currency_mapping = {"USD": "$", "INR": "₹", "EUR": "€", "GBP": "£", "JPY": "¥", "CNY": "¥", "CAD": "C$"}
            currency_sign = currency_mapping.get(currency_symbol, currency_symbol)

            st.subheader("📜 Stock Details")
            st.write(f"**Currency:** {currency_symbol} ({currency_sign})")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"<div class='stock-card'><b>Name:</b> {stock_info.get('longName', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='stock-card'><b>Sector:</b> {stock_info.get('sector', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='stock-card'><b>Industry:</b> {stock_info.get('industry', 'N/A')}</div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div class='stock-card'><b>Market Cap:</b> {stock_info.get('marketCap', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='stock-card'><b>Previous Close:</b> {stock_info.get('previousClose', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='stock-card'><b>Open Price:</b> {stock_info.get('open', 'N/A')}</div>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<div class='stock-card'><b>52-Week High:</b> {stock_info.get('fiftyTwoWeekHigh', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='stock-card'><b>52-Week Low:</b> {stock_info.get('fiftyTwoWeekLow', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='stock-card'><b>Dividend Yield:</b> {stock_info.get('dividendYield', 'N/A')}</div>", unsafe_allow_html=True)

            st.subheader("📊 Stock Data Preview")
            st.dataframe(stock_data.tail(10))

            X_test = prepare_data(stock_data)
            predictions = predict_stock_price(model, X_test)
            stock_data = stock_data.iloc[60:].copy()
            stock_data['Predicted Close'] = predictions

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(stock_data.index, stock_data['Close'], label="Actual Price", color='blue')
            ax.plot(stock_data.index, stock_data['Predicted Close'], label="Predicted Price", linestyle='dashed', color='red')
            ax.set_title(f"Stock Price Prediction for {symbol}")
            ax.legend()
            st.pyplot(fig)

            st.subheader("📅 Next 5 Trading Days Predicted Prices")
            last_60_days = stock_data['Close'].values[-60:].reshape(-1, 1)
            future_prices = []
            future_dates = []
            next_date = stock_data.index[-1]

            while len(future_prices) < 5:
                next_date += timedelta(days=1)
                if next_date.weekday() < 5:
                    last_60_days_reshaped = last_60_days.reshape(1, 60, 1)
                    predicted_price = predict_future_prices(model, last_60_days_reshaped)
                    if isinstance(predicted_price, (list, np.ndarray)):
                        predicted_price = predicted_price[0]
                    future_prices.append(predicted_price)
                    future_dates.append(next_date)
                    predicted_price = np.array([[predicted_price]])
                    last_60_days = np.append(last_60_days, predicted_price, axis=0)[-60:]

            future_df = pd.DataFrame({"Date": future_dates, f"Predicted Price ({currency_sign})": future_prices})
            future_df["Date"] = future_df["Date"].dt.strftime("%Y-%m-%d")
            st.table(future_df)

            st.subheader("📉 Last 15 Days Actual vs Next 5 Days Predicted Prices")
            last_15_days = stock_data['Close'].tail(15)
            last_15_dates = last_15_days.index
            last_15_prices = last_15_days.values.flatten()
            future_prices = np.array(future_prices).flatten()
            combined_dates = np.concatenate([last_15_dates, future_dates])
            combined_prices = np.concatenate([last_15_prices, future_prices])

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(last_15_dates, last_15_prices, label="Actual Close Price", color='blue', marker='o')
            ax.plot(future_dates, future_prices, label="Predicted Close Price", color='red', linestyle='dashed', marker='o')
            ax.plot([last_15_dates[-1], future_dates[0]], [last_15_prices[-1], future_prices[0]], color='black', linestyle='dotted')
            ax.set_title(f"{symbol} - Last 15 Days Actual & Next 5 Days Predicted Prices")
            ax.set_xlabel("Date")
            ax.set_ylabel(f"Price ({currency_sign})")
            ax.legend()
            ax.grid()
            st.pyplot(fig)

elif section == "Manual Price Prediction":
    st.subheader("Enter Stock Symbol and Date :")

    col1, col2 = st.columns(2)
    with col1:
        manual_symbol = st.text_input("Stock Symbol", "AAPL")
    # with col2:
    #     date_input = st.date_input("Select Date", max_value=datetime.today())

    try:
        # yf.Ticker(manual_symbol).info['regularMarketPrice']
        valid_symbol = True
    except:
        st.warning("⚠️ Invalid stock symbol. Please enter a valid one.")
        valid_symbol = False

    if valid_symbol:
        st.subheader("📌 Input Features for Manual Prediction")
        st.write("⚠️ Don't Enter Random Values ⚠️")
        
        col1, col2 = st.columns(2)
        with col1:
            high = st.number_input("High Price", min_value=0.0)
            open_price = st.number_input("Open Price", min_value=0.0)
        with col2:
            low = st.number_input("Low Price", min_value=0.0)
            volume = st.number_input("Volume", min_value=0.0)

        if st.button("🔮 Predict Closing Price"):
            
            synthetic_close = np.mean([open_price, high, low])
            synthetic_sequence = np.array([synthetic_close for _ in range(60)]).reshape(-1, 1)
            scaled_sequence = scaler.fit_transform(synthetic_sequence).reshape(1, 60, 1)
            predicted_close = model.predict(scaled_sequence)
            predicted_price = scaler.inverse_transform(predicted_close)[0][0]
            st.success(f"📌 Predicted Closing Price: {predicted_price:.2f}")

# Footer
st.markdown("""
    <hr>
    <p style='text-align: center; color: grey;'>© 2025 Stock Vision. All Rights Reserved.</p>
    <p style='text-align: center; color: grey;'>Our model is based on historical data from the last decade. As a result, the predicted prices may not fully capture the impact of other market factors that can influence actual prices.</p>
""", unsafe_allow_html=True)

