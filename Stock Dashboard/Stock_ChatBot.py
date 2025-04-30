import streamlit as st
import google.generativeai as genai

api_key = st.secrets["api_key"]
# Set up Gemini API key
genai.configure(api_key=api_key)

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# Streamlit UI
st.title("💬 Stock Vision Chatbot")
st.write("Ask me anything!")

# User input
user_input = st.text_input("You:", "")

if user_input:
    try:
        response = model.generate_content(user_input)
        st.text_area("Vision:", response.text, height=200)
    except Exception as e:
        st.error(f"Error: {e}")

# Footer
st.markdown("""
    <hr>
    <p style='text-align: center; color: grey;'>© 2025 Stock Vision. All Rights Reserved.</p>
""", unsafe_allow_html=True)