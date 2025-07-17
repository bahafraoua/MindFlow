import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sample data (replace with your model's output)
recent_data = pd.DataFrame({
    "Date": ["17/07/2025", "16/07/2025", "15/07/2025", "14/07/2025", "13/07/2025"],
    "Émotion dominante": ["Tristesse", "Joie", "Colère", "Fatigue", "Joie"],
    "Stress (%)": [72, 28, 65, 80, 35],
    "Commentaire": ["Signes de fatigue", "Bonne interaction", "Comportement agité", "Besoin de repos", "Engagement positif"]
})

# Sidebar
st.sidebar.title(" MindFlow")

st.sidebar.button(" Dashboard")
st.sidebar.button("Analyse détaillée")
st.sidebar.button("Export PDF")

st.logo(image="images/streamlit-logo-primary-colormark-lighttext.png", 
        icon_image="images/streamlit-mark-color.png")

# Header
st.title("Vue d’ensemble psychologique")
st.caption("Dernière mise à jour : 17/07/2025 - 10:00")

# Psychological Status Summary
st.subheader("Statut actuel")
st.success("**État émotionnel global** : Positif\n\n**Niveau de stress** : Modéré")

# Metrics / Scorecards
col1, col2, col3 = st.columns(3)
col1.metric("😨 Stress", "57%", "-5% vs hier")
col2.metric("😊 Émotion dominante", "Joie")
col3.metric("📊 Variabilité émotionnelle", "Modérée")

# Stress Trend Line Chart
st.subheader("📈 Évolution du stress (5 derniers jours)")
fig, ax = plt.subplots()
ax.plot(recent_data["Date"], recent_data["Stress (%)"], marker="o", color="#ff6f61")
ax.set_ylabel("Stress (%)")
ax.set_xlabel("Date")
ax.set_ylim(0, 100)
ax.set_title("Stress au fil des jours")
ax.invert_xaxis()  # Most recent on the left
st.pyplot(fig)

# Recent Analyses Table
st.subheader("🕒 Dernières analyses")
st.dataframe(recent_data, use_container_width=True)

# Alerts and Recommendations
st.subheader("⚠️ Alertes et recommandations")
st.warning("Niveau de stress élevé détecté plusieurs fois cette semaine.")
st.info("💡 Suggestion : Encouragez des pauses ou une activité relaxante.")

# CTA Buttons
st.subheader("Actions rapides")
colA, colB = st.columns(2)
colA.button("🔍 Voir l’analyse détaillée")
colB.button("📤 Exporter en PDF")
