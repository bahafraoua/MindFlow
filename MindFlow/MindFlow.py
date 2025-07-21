import streamlit as st
from PIL import Image

# Optional: Load a logo
col_left, col_center, col_right = st.columns([1, 2, 1])
logo = Image.open("images\MindFlow.png")
with col_center:
    # Place your image inside the center column
    st.image(logo, width=240)

# Page title
st.title("👋 Welcome to MindFlow")
st.markdown("### Your AI-powered mental well-being companion")
# utils.py
def show_sidebar_logo():
    st.logo(image="images\MindFlowHorizental.png",
        icon_image="images\MindFlow.png")

# Introductory message
st.write("""
MindFlow is an intelligent platform designed to help organizations monitor and enhance employee psychological well-being using advanced AI techniques.

By analyzing **handwriting samples** and **facial expressions**, MindFlow provides insights into emotional states, stress levels, and behavioral trends — all while maintaining privacy and respect for users.
""")

# Divider
st.markdown("---")

# Features overview
st.header("Key Features")
st.markdown("""
-  **Emotion Recognition**: Detects dominant emotions from facial expressions in real-time.
-  **Graphology Analysis**: Analyzes handwriting to assess stress, mood, and personality markers.
-  **Smart Dashboard**: Offers a clear, dynamic view of psychological trends over time.
- **Alerts & Suggestions**: Provides mental health insights and recommendations based on AI analysis.
-  **Privacy-focused**: All data is anonymized and stored securely.
""")

# How to use
st.header("📌 How to Use MindFlow")
st.markdown("""
1. **Upload** a facial image or handwriting sample from the sidebar.
2. The system will automatically analyze the input using AI models.
3. Navigate to the **Dashboard** to see a summary of results.
4. Explore **Detailed Analysis** for emotion trends, stress levels, and recommendations.
5. Download or export reports as needed.

> 🔄 You can run new analyses anytime. It only takes a few seconds!
""")

# CTA
st.markdown("---")
st.success("✅ Ready to get started? Use the sidebar to upload your first sample or view the dashboard.")


