import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page title
st.title("📊 Results History")
st.markdown("### View all past emotion and handwriting analyses")
from MindFlow import show_sidebar_logo
show_sidebar_logo()



# Sample data (replace with real stored data)
analysis_history = pd.DataFrame({
    "Date": ["2025-07-17", "2025-07-16", "2025-07-15", "2025-07-14", "2025-07-13"],
    "Type": ["Facial", "Handwriting", "Facial", "Handwriting", "Facial"],
    "Dominant Emotion": ["Sadness", "-", "Anger", "-", "Joy"],
    "Stress (%)": [72, 35, 65, 28, 30],
    "Interpretation": [
        "High fatigue, signs of emotional strain.",
        "Confident and structured personality.",
        "Agitated state, elevated stress response.",
        "Calm, balanced handwriting traits.",
        "Positive, engaged emotional tone."
    ]
})

# Show the table
st.subheader("📝 Analysis Log")
st.dataframe(analysis_history, use_container_width=True)

# Plot: Stress over time
st.subheader("📈 Stress Trend Over Time")
fig, ax = plt.subplots()
facial_data = analysis_history[analysis_history["Type"] == "Facial"]
ax.plot(facial_data["Date"], facial_data["Stress (%)"], marker="o", color="#ff9f43")
ax.set_title("Stress Levels from Facial Analysis")
ax.set_ylabel("Stress (%)")
ax.set_xlabel("Date")
ax.set_ylim(0, 100)
ax.invert_xaxis()  # Most recent on left
st.pyplot(fig)

# Expandable section for detailed interpretations
st.subheader("🔍 Detailed Interpretations")
for index, row in analysis_history.iterrows():
    with st.expander(f"{row['Date']} – {row['Type']} Analysis"):
        st.markdown(f"**Dominant Emotion:** {row['Dominant Emotion']}")
        st.markdown(f"**Stress Level:** {row['Stress (%)']}%")
        st.markdown(f"**Interpretation:** {row['Interpretation']}")

# Export button (placeholder)
st.markdown("---")
st.button("📄 Export All Results to PDF")
