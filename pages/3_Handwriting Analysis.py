import google.generativeai as genai
import json
import time
import base64
from pydantic import BaseModel, Field, validator, ValidationError
from typing import Literal, Dict, Any
import streamlit as st
from PIL import Image
import io
from io import BytesIO

# --- Pydantic Schema Definitions (re-included for self-contained example) ---
class HandwritingAnalysisSection(BaseModel):
    """Schema for the detailed handwriting analysis sections."""
    Pression: str = Field(..., alias="Pression (Pression)", description="Description de la pression d'écriture et son interprétation psychologique.")
    Inclinaison: str = Field(..., alias="Inclinaison (Inclinaison)", description="Analyse de l'inclinaison des lettres et son interprétation psychologique.")
    Taille: str = Field(..., alias="Taille (Taille)", description="Description de la taille des lettres et son interprétation psychologique.")
    Espacement: str = Field(..., alias="Espacement (Espacement)", description="Observation de l'espacement et son interprétation psychologique.")
    Forme_des_lettres: str = Field(..., alias="Forme des lettres (Forme des lettres)", description="Identification de la forme des lettres et son interprétation psychologique.")
    Flux_et_Continuité: str = Field(..., alias="Flux et Continuité (Flux et Continuité)", description="Description du flux d'écriture et son interprétation psychologique.")
    Structure_et_Organisation: str = Field(..., alias="Structure et Organisation (Structure et Organisation)", description="Analyse de la structure et de l'organisation et son interprétation psychologique.")

class PsychosocialStatus(BaseModel):
    """Schema for the psychosocial status."""
    Niveau_de_stress: Literal["faible", "modéré", "élevé"] = Field(..., alias="Niveau de stress")
    Risque_de_burnout: Literal["faible", "modéré", "élevé"] = Field(..., alias="Risque de burnout")
    Motivation_engagement: Literal["faible", "modéré", "élevé"] = Field(..., alias="Motivation & engagement")
    Adaptabilite: Literal["faible", "modéré", "élevé"] = Field(..., alias="Adaptabilité")
    Tendance_a_l_integration_sociale: Literal["faible", "modéré", "élevé"] = Field(..., alias="Tendance à l'intégration sociale")

class HandwritingAnalysisReport(BaseModel):
    """Main schema for the entire handwriting analysis report."""
    analysis: str = Field(..., description="Contient la description détaillée de chaque caractéristique de l'écriture manuscrite.")
    Statut_Psychosocial: PsychosocialStatus = Field(..., alias="Statut Psychosocial")
    En_resume: str = Field(..., alias="En résumé", description="Paragraphe concis résumant la personnalité globale, l'état émotionnel et le bien-être psychosocial de l'écrivain.")
    Analyse_semantique_et_Signification_cachee: str = Field(..., alias="Analyse sémantique et Signification cachée", description="Analyse du ton, du subtexte émotionnel et des significations non dites du message manuscrit.")

    class Config:
        allow_population_by_field_name = True
# --- End Pydantic Schema Definitions ---


def analyze_handwriting_with_gemini(base64_image_data: str, user_prompt: str) -> Dict[str, Any] | None:
    """
    Analyze a handwriting image and return a structured JSON analysis
    using the google-generativeai library and gemini-1.5-flash model.
    Role: You are a world-class expert in graphology, behavioral psychology, and
    occupational psychosocial assessment, with a specialization in HR risk detection.
    You are skilled at seamlessly incorporating the semantic meaning of written text into
    your handwriting analysis to detect deeper insights, without dedicating a separate
    semantic section in the final report.
    You must carefully observe the handwriting and describe its characteristics in detail,
    including aspects such as pressure, slant, size, spacing, and any other notable features,
    and explain what these characteristics might indicate about the writer.
    Mission: You will analyze the provided handwriting image and produce a highly
    professional, deeply detailed interpretation.
    Language and Formatting:
    - The final report must be written exclusively in formal, professional French, even though
    this prompt is in English.
    - The report structure must follow exactly the format specified below, ensuring each
    section builds logically toward the final summary.
    - Your response should consist *only* of the final analysis report. Do not include any
    introductions, greetings, or task confirmations.
    Report Formatting Rules:
    - Use the exact French section titles.
    - Each section must describe observable handwriting features and link them to a
    psychological and psychosocial interpretation.
    - Use precise, non-generic observations (avoid vague descriptions such as "quite
    heavy").
    - Include explicit psychosocial risk levels where relevant (low / moderate / high).
    - Include a dedicated *Contradictions et Incohérences* section to highlight
    mismatches between handwriting style and the message's meaning.
    - Use the semantic meaning of the text to enhance your interpretations but do not
    create a separate semantic analysis section.
    - The *En résumé* section must be a coherent paragraph, not a bulleted list.
    ---
    *Analyse de l'écriture manuscrite*
    *Pression (Pression)* : Analyze the overall and localized writing pressure (light,
    medium, heavy) based on ink density, stroke depth, and consistency. Explain what this
    suggests about vital energy, determination, resilience, or emotional control.
    *Inclinaison (Inclinaison)* : Analyze the letter slant (left, right, vertical) and any
    significant variations. Interpret what this indicates about interpersonal openness, social
    orientation, or emotional adaptability.
    *Taille (Taille)* : Describe letter size (small, medium, large) and any inconsistencies.
    Link this to cognitive focus, self-perception, and the balance between introspection and
    sociability.
    *Espacement (Espacement)* : Observe the spacing between letters, words, and
    lines. Relate these observations to mental organization, cognitive clarity, a need for
    autonomy, or a tendency toward social engagement or withdrawal.
    *Forme des lettres (Forme des lettres)* : Identify whether letters are rounded,
    angular, or a mix. Link this to creativity, analytical thinking, flexibility, or emotional
    rigidity.
    *Flux et Continuité (Flux et Continuité)* : Describe the writing rhythm (fast, slow,
    regular, irregular) and the connectivity between letters. Interpret these elements in
    terms of decision-making speed, self-confidence, and emotional fluidity.
    *Structure et Organisation (Structure et Organisation)* : Analyze line alignment, the
    overall text layout, and the hierarchy of ideas. Explain what this reveals about logic,
    planning skills, and priority management.
    *Contradictions et Incohérences (Contradictions et Incohérences)* : Highlight
    elements of the handwriting that seem to conflict with each other or with the semantic
    content of the text. Analyze how these tensions may reveal internal conflicts or
    behavioral adjustments.
    *En résumé (En résumé)* : Provide a summary paragraph integrating all observations
    into a coherent personality and emotional profile.
    Explicitly include the following psychosocial indicators:
    - Niveau de stress: faible / modéré / élevé
    - Risque de burnout: faible / modéré / élevé
    - Motivation & engagement: faible / modéré / élevé
    - Adaptabilité: faible / modéré / élevé
    - Tendance à l'intégration sociale: faible / modéré / élevé
        Args:
            base64_image_data: The base64 encoded string of the handwriting image.
            user_prompt: The natural language prompt for the Gemini model to generate the analysis.

        Returns:
            A dictionary containing the parsed JSON analysis, or None if an error occurs.
    """
    # Configure the API key. In a Canvas environment, this might be handled automatically.
    # For local testing, you might need to set genai.configure(api_key="YOUR_API_KEY")
    # For Canvas, leave it as is, as the runtime provides it.
    api_key = 'AIzaSyBVZQKiYt42GYvhdzMI7RKawIYSw2i2ga4'
    if api_key:
        genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-1.5-flash')

    # The prompt should guide the model to produce the analysis in the desired JSON structure.
    # We explicitly ask for a JSON response with a specific schema.
    full_prompt = (
        f"{user_prompt}\n\n"
        "Please respond *strictly in JSON* with the following keys in this order: "
        "\"analysis\", \"Statut Psychosocial\", \"En résumé\", \"Analyse sémantique et Signification cachée\". "
        "Do not include any other text, explanation, or formatting. "
         "Ensure French characters are correctly represented and all values follow the specified enums."
        
    )

    # Prepare the image part for the model
    image_part = {
        "mime_type": "image/jpeg",  # Assuming JPEG. Adjust if other formats are expected.
        "data": base64.b64decode(base64_image_data) # The genai library expects bytes for image data
    }

    # Define the response schema directly for the generation_config
    response_schema = {
        "type": "OBJECT",
        "properties": {
            "analysis": {"type": "STRING"},
            "Statut Psychosocial": {
                "type": "OBJECT",
                "properties": {
                    "Niveau de stress": {"type": "STRING", "enum": ["faible", "modéré", "élevé"]},
                    "Risque de burnout": {"type": "STRING", "enum": ["faible", "modéré", "élevé"]},
                    "Motivation & engagement": {"type": "STRING", "enum": ["faible", "modéré", "élevé"]},
                    "Adaptabilité": {"type": "STRING", "enum": ["faible", "modéré", "élevé"]},
                    "Tendance à l'intégration sociale": {"type": "STRING", "enum": ["faible", "modéré", "élevé"]}
                },
                "required": [
                    "Niveau de stress",
                    "Risque de burnout",
                    "Motivation & engagement",
                    "Adaptabilité",
                    "Tendance à l'intégration sociale"
                ]
            },
            "En résumé": {"type": "STRING"},
            "Analyse sémantique et Signification cachée": {"type": "STRING"}
        },
        "required": [
            "analysis",
            "Statut Psychosocial",
            "En résumé",
            "Analyse sémantique et Signification cachée"
        ]
    }

    try:
        # Use model.generate_content for multi-modal input
        response = model.generate_content(
            contents=[full_prompt, image_part],
            generation_config={
                "response_mime_type": "application/json",
                "response_schema": response_schema
            }
        )

        # The response.text will contain the JSON string
        json_string = response.text
        try:
            parsed_json = json.loads(json_string)
            formatted_json = json.dumps(parsed_json, indent=4, ensure_ascii=False)
            # Optional: Validate with Pydantic schema
            try:
                HandwritingAnalysisReport.parse_obj(parsed_json)
                print("Parsed analysis is valid according to Pydantic schema.")
            except ValidationError as e:
                print("Parsed analysis does NOT conform to Pydantic schema:", e)
                return None # For strict adherence, return None on validation failure
            return formatted_json
        except json.JSONDecodeError as parse_error:
            print(f"Failed to parse JSON response: {parse_error}")
            return None

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None







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
        
            with st.spinner("🤖 Analyse en cours avec Gemini..."):
                # Call the analysis function
                    buffered = io.BytesIO()
                    image.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    analysis_result = analyze_handwriting_with_gemini(img_str, "Analysez cette écriture.")
                # Display the results
                    st.subheader("Résultats de l'analyse:")
                    st.markdown(analysis_result)
