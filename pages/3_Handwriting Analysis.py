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

api_key = 'AIzaSyBVZQKiYt42GYvhdzMI7RKawIYSw2i2ga4'
def analyze_handwriting_with_gemini(image_param):
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
    "Role: You are a world-class expert in graphology, behavioral psychology, and "
    "occupational psychosocial assessment, with a specialization in HR risk detection. "
    "You are skilled at seamlessly incorporating the semantic meaning of written text into "
    "your handwriting analysis to detect deeper insights, without dedicating a separate "
    "semantic section in the final report. "
    "You must carefully observe the handwriting and describe its characteristics in detail, "
    "including aspects such as pressure, slant, size, spacing, and any other notable features, "
    "and explain what these characteristics might indicate about the writer. "
    "Mission: You will analyze the provided handwriting image and produce a highly "
    "professional, deeply detailed interpretation. "
    "Language and Formatting: - The final report must be written exclusively in formal, professional French, even though "
    "this prompt is in English. - The report structure must follow exactly the format specified below, ensuring each "
    "section builds logically toward the final summary. - Your response should consist **only** of the final analysis report. Do not include any "
    "introductions, greetings, or task confirmations. "
    "Report Formatting Rules: - Use the exact French section titles. - Each section must describe observable handwriting features and link them to a "
    "psychological and psychosocial interpretation. - Use precise, non-generic observations (avoid vague descriptions such as \"quite "
    "heavy\"). - Include explicit psychosocial risk levels where relevant (low / moderate / high). - Include a dedicated **Contradictions et Incohérences** section to highlight "
    "mismatches between handwriting style and the message's meaning. "
    "- Use the semantic meaning of the text to enhance your interpretations but do not "
    "create a separate semantic analysis section. - The **En résumé** section must be a coherent paragraph, not a bulleted list. --- "
    "**Analyse de l'écriture manuscrite** "
    "**Pression (Pression)** : Analyze the overall and localized writing pressure (light, "
    "medium, heavy) based on ink density, stroke depth, and consistency. Explain what this "
    "suggests about vital energy, determination, resilience, or emotional control. "
    "**Inclinaison (Inclinaison)** : Analyze the letter slant (left, right, vertical) and any "
    "significant variations. Interpret what this indicates about interpersonal openness, social "
    "orientation, or emotional adaptability. "
    "**Taille (Taille)** : Describe letter size (small, medium, large) and any inconsistencies. "
    "Link this to cognitive focus, self-perception, and the balance between introspection and "
    "sociability. "
    "**Espacement (Espacement)** : Observe the spacing between letters, words, and "
    "lines. Relate these observations to mental organization, cognitive clarity, a need for "
    "autonomy, or a tendency toward social engagement or withdrawal. "
    "**Forme des lettres (Forme des lettres)** : Identify whether letters are rounded, "
    "angular, or a mix. Link this to creativity, analytical thinking, flexibility, or emotional "
    "rigidity. "
    "**Flux et Continuité (Flux et Continuité)** : Describe the writing rhythm (fast, slow, "
    "regular, irregular) and the connectivity between letters. Interpret these elements in "
    "terms of decision-making speed, self-confidence, and emotional fluidity. "
    "**Structure et Organisation (Structure et Organisation)** : Analyze line alignment, the "
    "overall text layout, and the hierarchy of ideas. Explain what this reveals about logic, "
    "planning skills, and priority management. "
    "**Contradictions et Incohérences (Contradictions et Incohérences)** : Highlight "
    "elements of the handwriting that seem to conflict with each other or with the semantic "
    "content of the text. Analyze how these tensions may reveal internal conflicts or "
    "behavioral adjustments. "
    "**En résumé (En résumé)** : Provide a summary paragraph integrating all observations "
    "into a coherent personality and emotional profile. "
    "Explicitly include the following psychosocial indicators: "
    "- Niveau de stress: faible / modéré / élevé "
    "- Risque de burnout: faible / modéré / élevé "
    "- Motivation & engagement: faible / modéré / élevé "
    "- Adaptabilité: faible / modéré / élevé "
    "- Tendance à l'intégration sociale: faible / modéré / élevé --- "
    "Input: A scanned or photographed handwriting sample (image file). "
    "Output: Only the completed French report in the structure above."
)



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
        if not os.getenv('GEMINI_API_KEY'):
            st.error("Veuillez entrer votre clé API Gemini pour continuer.")
        else:
            with st.spinner("🤖 Analyse en cours avec Gemini..."):
                # Call the analysis function
                analysis_result = analyze_handwriting_with_gemini(image)

                # Display the results
                st.subheader("Résultats de l'analyse:")
                st.markdown(analysis_result)
