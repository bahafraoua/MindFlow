import streamlit as st
from PIL import Image
from config.gemini_config import configure_gemini
from middleware.text_to_json import format_text_to_schema
from modules.nav import show_sidebar_logo
from imagehash import average_hash


show_sidebar_logo()

def analyze_handwriting(image, model):
    """Analyze handwriting using Gemini 1.5 Flash and return text response"""
    try:
        prompt = """Role: You are a world-class expert in graphology, behavioral psychology, and occupational psychosocial assessment, with a specialization in HR risk detection.
            You are skilled at seamlessly incorporating the semantic meaning of written text into your handwriting analysis to detect deeper insights, without dedicating a separate semantic section in the final report.
            You must carefully observe the handwriting and describe its characteristics in detail, including aspects such as pressure, slant, size, spacing, and any other notable features, and explain what these characteristics might indicate about the writer.

            Mission: You will analyze the provided handwriting image and produce a highly professional, deeply detailed interpretation.

            Language and Formatting:
            - The final report must be written exclusively in formal, professional French, even though this prompt is in English.
            - The report structure must follow exactly the format specified below, ensuring each section builds logically toward the final summary.
            - Your response should consist **only** of the final analysis report. Do not include any introductions, greetings, or task confirmations.

            Report Formatting Rules:
            - Use the exact French section titles.
            - Each section must describe observable handwriting features and link them to a psychological and psychosocial interpretation.
            - Use precise, non-generic observations (avoid vague descriptions such as "quite heavy").
            - Include explicit psychosocial risk levels where relevant (low / moderate / high).
            - Include a dedicated **Contradictions et Incohérences** section to highlight mismatches between handwriting style and the message's meaning.
            - Use the semantic meaning of the text to enhance your interpretations but do not create a separate semantic analysis section.
            - The **En résumé** section must be a coherent paragraph, not a bulleted list.

            ---

            **Analyse de l'écriture manuscrite**

            **Pression (Pression)** : Analyze the overall and localized writing pressure (light, medium, heavy) based on ink density, stroke depth, and consistency. Explain what this suggests about vital energy, determination, resilience, or emotional control.

            **Inclinaison (Inclinaison)** : Analyze the letter slant (left, right, vertical) and any significant variations. Interpret what this indicates about interpersonal openness, social orientation, or emotional adaptability.

            **Taille (Taille)** : Describe letter size (small, medium, large) and any inconsistencies. Link this to cognitive focus, self-perception, and the balance between introspection and sociability.

            **Espacement (Espacement)** : Observe the spacing between letters, words, and lines. Relate these observations to mental organization, cognitive clarity, a need for autonomy, or a tendency toward social engagement or withdrawal.

            **Forme des lettres (Forme des lettres)** : Identify whether letters are rounded, angular, or a mix. Link this to creativity, analytical thinking, flexibility, or emotional rigidity.

            **Flux et Continuité (Flux et Continuité)** : Describe the writing rhythm (fast, slow, regular, irregular) and the connectivity between letters. Interpret these elements in terms of decision-making speed, self-confidence, and emotional fluidity.

            **Structure et Organisation (Structure et Organisation)** : Analyze line alignment, the overall text layout, and the hierarchy of ideas. Explain what this reveals about logic, planning skills, and priority management.

            **Contradictions et Incohérences (Contradictions et Incohérences)** : Highlight elements of the handwriting that seem to conflict with each other or with the semantic content of the text. Analyze how these tensions may reveal internal conflicts or behavioral adjustments.

            **En résumé (En résumé)** : Provide a summary paragraph integrating all observations into a coherent personality and emotional profile.
            Explicitly include the following psychosocial indicators:
            - Niveau de stress: faible / modéré / élevé
            - Risque de burnout: faible / modéré / élevé
            - Motivation & engagement: faible / modéré / élevé
            - Adaptabilité: faible / modéré / élevé
            - Tendance à l'intégration sociale: faible / modéré / élevé

            ---

            Input: A handwriting image.
            Output: Only the completed French report in the structure above
            """
        
        # Get normal text response
        response = model.generate_content(contents=[prompt, image])
        text_response = response.text
        
        # Format JSON in a separate variable
        json_response = format_text_to_schema(text_response, analysis_type="Handwriting Analysis")
        print(json_response)
        return text_response
            
    except Exception as e:
        return f"Error analyzing image: {str(e)}"
    
def main():
    st.header('✍️ Handwriting Analysis')
    st.markdown("**AI-powered handwriting analysis for workplace well-being assessment**")
    st.divider()
    
    model = configure_gemini()
    if not model:
        return
    
    st.subheader("Upload a Handwriting Image")
    st.markdown("Upload an image of handwriting or signature for analysis")
        
    uploaded_file = st.file_uploader(
            "Choose an image file", 
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
            help="Supported formats: PNG, JPG, JPEG, GIF, BMP"
        )
        
    if uploaded_file is not None:
            image = Image.open(uploaded_file)
            imageHash = average_hash(image)
            print(f"Image Hash: {imageHash}")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(image, caption="Uploaded Image", width=400)
            
            if st.button("🔍 Analyser l'écriture", type="primary"):
                with st.spinner("🤖 Analyzing handwriting with Gemini AI..."):
                    analysis_result = analyze_handwriting(image, model)
                    st.markdown(analysis_result)
    

    st.info("🔒 **Privacy Note**: Images are processed securely and not stored permanently. Analysis is for well-being assessment purposes only.")

if __name__ == '__main__':
    main()
