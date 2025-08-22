import streamlit as st
from config.gemini_config import configure_gemini
from config.database_config import get_firebase_manager
from middleware.text_to_json import format_text_to_schema
from middleware.image_processing import compress_image_to_base64
from PIL import Image
from modules.nav import show_sidebar_logo
import uuid

show_sidebar_logo()

def analyze_facial_expression(image, model):
    """Analyze facial expression using Gemini 1.5 Flash and return both text and JSON formats"""
    try:
        prompt = """Role: You are a world-class expert in facial expression analysis, behavioral psychology, and occupational psychosocial assessment, with a specialization in HR risk detection.  
            You are skilled at observing micro-expressions, muscle tension, eye dynamics, and other facial indicators to detect a wide range of emotional states, including stress, tiredness, depression, fatigue, happiness, and other nuanced emotions.  
            You must carefully describe the observable facial characteristics and explain what these may indicate about the subject's emotional and psychosocial state, supported by a scoring system for each detected emotion.

            Mission: You will analyze the provided facial image or video frame and produce a highly professional, deeply detailed interpretation.

            Language and Formatting:

            - The final report must be written exclusively in formal, professional French, even though this prompt is in English.
            - The report structure must follow exactly the format specified below, ensuring each section builds logically toward the final summary.
            - Your response should consist **only** of the final analysis report. Do not include any introductions, greetings, or task confirmations.

            Report Formatting Rules:

            - Use the exact French section titles.
            - Each section must describe observable facial features and link them to a psychological and psychosocial interpretation.
            - Use precise, non-generic observations (avoid vague descriptions like "seems happy").
            - For each emotion, provide a **score from 0 to 100** indicating the detected intensity.
            - Include explicit psychosocial risk levels where relevant (low / moderate / high).
            - Include a dedicated **Contradictions et Incohérences** section to highlight mismatches between facial expressions and contextual cues (e.g., smiling but with tension around the eyes).
            - The **En résumé** section must be a coherent paragraph, not a bulleted list.

            ---

            **Analyse de l'expression faciale**

            **Tension musculaire (Tension musculaire)** : Analyse the contraction or relaxation of facial muscles (forehead, jaw, cheeks) and interpret what this reveals about stress, determination, or relaxation.

            **Dynamique des yeux (Dynamique des yeux)** : Observe eye openness, blinking rate, micro-movements, and gaze direction. Interpret these in relation to alertness, fatigue, sadness, or engagement.

            **Position et mouvement des sourcils (Sourcils)** : Analyze eyebrow position (raised, furrowed, neutral) and movement patterns. Link to emotions such as surprise, concentration, or concern.

            **Configuration de la bouche (Bouche)** : Examine lip position, curvature, and tension. Interpret signs of happiness, frustration, sadness, or suppression of emotion.

            **Symétrie faciale (Symétrie)** : Observe symmetry in expressions and movements, noting any asymmetry that may indicate emotional suppression or internal conflict.

            **Signes de fatigue (Fatigue)** : Detect dark circles, drooping eyelids, or reduced muscle tone, and explain their link to tiredness or exhaustion.

            **Scoring émotionnel (Scoring émotionnel)** : Provide a score from 0 to 100 for each of the following emotions:  
            - Stress:  /100
            - Fatigue:  /100
            - Dépression:  /100
            - Joie / Bonheur:  /100
            - Colère:  /100
            - Surprise:  /100
            - Calme / Sérénité:  /100
            - Tristesse:  /100
            - Anxiété:  /100
            - Frustration:  /100
            - Enthousiasme:  /100

            **Contradictions et Incohérences (Contradictions et Incohérences)** : Highlight elements of the facial expression that conflict with other visual cues or the context, and analyze what these tensions may reveal about internal states.

            **En résumé (En résumé)** : Provide a coherent summary paragraph integrating all observations into a personality and emotional state profile, explicitly referencing emotional balance, coping capacity, and psychosocial well-being.  
            Include explicit psychosocial indicators:  
            - Niveau de stress: faible / modéré / élevé  
            - Risque de burnout: faible / modéré / élevé  
            - État de motivation: faible / modéré / élevé  
            - Adaptabilité émotionnelle: faible / modéré / élevé  
            - Capacité de régulation émotionnelle: faible / modéré / élevé
            ---

            Input: A facial image or video frame.  
            Output: Only the completed French report in the structure above 
            """
        
        # Get normal text response
        response = model.generate_content(contents=[prompt, image])
        text_response = response.text
        
        # Format JSON in a separate variable
        json_response = format_text_to_schema(text_response, analysis_type="Facial Expression Analysis")
        image_base64, compression_info = compress_image_to_base64(image)
        get_firebase_manager().save_analysis(
            str(uuid.uuid4()),
            image=image_base64,
            analysis_data=json_response,
            compression_info=compression_info,
            analysis_type='facial_analysis'
        )

        return text_response
            
    except Exception as e:
        return f"Error analyzing image: {str(e)}", None


def main():
    st.header('🧠 Facial Analysis')
    st.markdown("**AI-powered facial expression and emotion analysis for workplace well-being assessment**")
    st.divider()
    
    # Initialize session state for user ID
    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())
    
    # Initialize Firebase timestamp
    if 'current_timestamp' not in st.session_state:
        from datetime import datetime
        st.session_state.current_timestamp = datetime.now()
    
    model = configure_gemini()
    if not model:
        return

    tab1, tab2= st.tabs(["📸 Camera Capture", "📁 Upload Image"])
    
    with tab1:
        st.subheader("Take a Photo")
        st.markdown("Use your device's camera to capture a photo for analysis")
        with st.expander("ℹ️ About Camera Permissions"):
            st.markdown("""
            **Why we need camera access:**
            - To capture your photo for facial analysis
            - Images are processed locally and securely
            - Analysis results are stored securely in our database
            
            **If camera doesn't work:**
            - Check if your browser allows camera access for this site
            - Make sure no other applications are using your camera
            - Try refreshing the page and allowing permissions again
            - Use the "Upload Image" tab as an alternative
            """)
        camera_image = st.camera_input("Capture your facial image")
        
        if camera_image is not None:
            image = Image.open(camera_image)
            with st.spinner("🤖 Analyzing facial expression with Gemini AI..."):
                analysis_result= analyze_facial_expression(image, model)
                st.markdown(analysis_result)
    
    with tab2:
        st.subheader("Upload an Image")
        st.markdown("Upload a facial image file for analysis")
        
        uploaded_file = st.file_uploader(
            "Choose an image file", 
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
            help="Supported formats: PNG, JPG, JPEG, GIF, BMP"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(image, caption="Uploaded Image", width=400)
            
            with st.spinner("🤖 Analyzing facial expression with Gemini AI..."):
                analysis_result = analyze_facial_expression(image, model)
                st.markdown(analysis_result)
    
if __name__ == '__main__':
    main()
