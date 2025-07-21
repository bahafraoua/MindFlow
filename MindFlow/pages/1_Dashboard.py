import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sample data (replace with your actual analysis output)
recent_data = pd.DataFrame({
    "Date": ["2025-07-17", "2025-07-16", "2025-07-15", "2025-07-14", "2025-07-13"],
    "Dominant Emotion": ["Sadness", "Joy", "Anger", "Fatigue", "Joy"],
    "Stress Level (%)": [72, 28, 65, 80, 35],
    "Comment": ["Signs of fatigue", "Positive interaction", "Agitated behavior", "Needs rest", "Engaged and positive"]
})

# Sidebar

from MindFlow import show_sidebar_logo
show_sidebar_logo()



# Header
st.title("Psychological Overview Dashboard")
st.caption("Last updated: July 17, 2025 – 10:00 AM")

# Psychological Status Summary
st.subheader("Current Status")
st.success("**Overall emotional state:** Positive\n\n**Stress level:** Moderate")

# Metrics / Scorecards
col1, col2, col3 = st.columns(3)
col1.metric("😨 Stress", "57%", "-5% vs yesterday")
col2.metric("😊 Dominant Emotion", "Joy")
col3.metric("📊 Emotional Variability", "Moderate")

# Stress Trend Line Chart
st.subheader("📈 Stress Trend (Last 5 Days)")
fig, ax = plt.subplots()
ax.plot(recent_data["Date"], recent_data["Stress Level (%)"], marker="o", color="#ff6f61")
ax.set_ylabel("Stress Level (%)")
ax.set_xlabel("Date")
ax.set_ylim(0, 100)
ax.set_title("Daily Stress Overview")
ax.invert_xaxis()  # Show most recent day on the left
st.pyplot(fig)

# Recent Analyses Table
st.subheader("🕒 Recent Analyses")
st.dataframe(recent_data, use_container_width=True)

# Alerts and Recommendations
st.subheader("⚠️ Alerts & Suggestions")
st.warning("High stress levels detected multiple times this week.")
st.info("💡 Recommendation: Encourage short breaks or light relaxation activities.")

# Quick Action Buttons
st.subheader("Quick Actions")
colA, colB = st.columns(2)
colA.button("🔍 View Detailed Analysis")
colB.button("📤 Export PDF Report")
