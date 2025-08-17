import google.generativeai as genai
import streamlit as st

def configure_gemini():
    """Configure Gemini AI with API key"""
    api_key = 'AIzaSyBVZQKiYt42GYvhdzMI7RKawIYSw2i2ga4'
    if not api_key:
        st.error("⚠️ Gemini API key not found. Please set GEMINI_API_KEY in your environment variables.")
        st.info("You can get your API key from: https://makersuite.google.com/app/apikey")
        return None
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')