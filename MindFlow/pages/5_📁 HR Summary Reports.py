import streamlit as st
import pandas as pd

# Page title
st.title("📁 HR Summary Reports")
st.markdown("""
Access automatically generated, anonymized psychological well-being reports to support your HR decisions.
""")

# Sample aggregated report data (replace with actual aggregated stats)
summary_stats = {
    "Total Employees Monitored": 120,
    "Average Stress Level (%)": 42,
    "Employees with High Stress Alerts": 15,
    "Most Common Emotion": "Neutral",
    "Reports Generated This Month": 45
}

st.subheader("📊 Key Metrics")
for key, value in summary_stats.items():
    st.metric(label=key, value=value)

# Placeholder: List of generated reports
st.subheader("📂 Available Reports")

reports = [
    {"title": "July 2025 Psychological Well-being Summary", "date": "2025-07-31", "link": "#"},
    {"title": "June 2025 Psychological Well-being Summary", "date": "2025-06-30", "link": "#"},
    {"title": "May 2025 Psychological Well-being Summary", "date": "2025-05-31", "link": "#"},
]

for report in reports:
    st.markdown(f"**{report['title']}** — {report['date']}  [Download PDF]({report['link']})")

# Alert or notes for HR
st.markdown("---")
st.info("""
*Reports are anonymized to protect employee privacy.*  
*For detailed individual analysis, please refer to the employee dashboard.*  
""")

# Optionally, allow filtering reports by month/year
st.subheader("Filter Reports")
selected_month = st.selectbox("Select Month", ["July 2025", "June 2025", "May 2025"])

# You could later add logic to filter and display reports dynamically based on selection

