import google.generativeai as genai
import streamlit as st
from PIL import Image
from io import BytesIO


# --- Instructions for the User ---
# 1. Make sure you have the required libraries installed:
#    pip install streamlit pillow google-generativeai
#
# 2. Get your Gemini API Key from Google AI Studio:
#    https://aistudio.google.com/app/apikey
#
# 3. Run the Streamlit app from your terminal:
#    streamlit run your_script_name.py
#
# 4. Paste your API key into the text input field in the web app.
# ---
api_key = "AIzaSyBVZQKiYt42GYvhdzMI7RKawIYSw2i2ga4"
def analyze_handwriting_with_gemini(api_key, image_param):
    """
    Analyzes a handwriting image using the Gemini 1.5 Flash model.

    Args:
        api_key (str): The user's Google Gemini API key.
        image_param (PIL.Image.Image): The handwriting image.

    Returns:
        str: The analysis text from the model, or an error message.
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt_text = (
    "Analysez cette écriture manuscrite ou signature d’un point de vue psychologique. "
    "Déduisez les traits de personnalité, l’état émotionnel, l’état psychologique, la stabilité mentale "
    "et tout signe de stress. Soyez précis. Répondez en français."
)


        # ✅ Directly use the PIL image
        content = [prompt_text, image_param]

        response = model.generate_content(content)
        return response.text

    except Exception as e:
        return f"Erreur pendant l'analyse : {e}"


# --- Streamlit App UI ---

st.set_page_config(layout="wide", page_title="Analyseur d'Écriture Manuscrite")

st.title("✍️ Analyseur d'Écriture Manuscrite avec Gemini AI")
st.markdown("Téléchargez une image de votre écriture ou de votre signature et laissez l'IA de Google l'analyser.")



# File uploader for the image
uploaded_file = st.file_uploader(
    "Choisissez une image d'écriture manuscrite ou de signature.",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    # Display the uploaded image
    st.image(image, caption="Image téléchargée", width=400)

    # Analyze button
    if st.button("Analyser l'écriture manuscrite"):
        if not api_key:
            st.error("Veuillez entrer votre clé API Gemini pour continuer.")
        else:
            with st.spinner("🤖 Analyse en cours avec Gemini..."):
                # Call the analysis function
                analysis_result = analyze_handwriting_with_gemini(api_key, image)

                # Display the results
                st.subheader("Résultats de l'analyse:")
                st.markdown(analysis_result)
