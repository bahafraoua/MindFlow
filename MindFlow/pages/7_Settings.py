import streamlit as st

# Page title
st.title("⚙️ Settings")
st.logo(image="images\MindFlowHorizental.png",
        icon_image="images\MindFlow.png")
st.markdown("Configure your preferences and analysis options below.")

# Language selection
st.subheader("🌐 Language")
language = st.selectbox("Choose your preferred language:", ["English", "Français", "Español", "Deutsch", "العربية"])

st.write(f"Selected language: **{language}**")

# Analysis options
st.subheader("🧠 Analysis Options")

stress_threshold = st.slider("Stress alert threshold (%)", min_value=0, max_value=100, value=70, step=5)
st.write(f"Alert threshold is set at **{stress_threshold}%** stress level.")

enable_notifications = st.checkbox("Enable email notifications for alerts", value=True)
st.write("Email notifications:", "Enabled" if enable_notifications else "Disabled")

# User preferences
st.subheader("👤 User Preferences")

dark_mode = st.checkbox("Enable dark mode", value=False)
st.write("Dark mode:", "Enabled" if dark_mode else "Disabled")

data_sharing = st.checkbox("Allow anonymous data sharing for research", value=False)
st.write("Anonymous data sharing:", "Allowed" if data_sharing else "Not allowed")

# Save button (for now just a placeholder)
if st.button("💾 Save Settings"):
    st.success("Settings saved successfully!")

