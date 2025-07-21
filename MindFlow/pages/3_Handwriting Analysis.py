import streamlit as st
from PIL import Image

# Page title
st.title("✍️ Handwriting Analysis")
st.markdown("### Upload a handwritten sample to extract psychological traits using graphology")
from MindFlow import show_sidebar_logo
show_sidebar_logo()


# Step 1: Upload handwriting image
st.subheader("Step 1: Upload Handwriting Sample")

uploaded_file = st.file_uploader("Upload a handwriting image (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Handwriting Sample", use_column_width=True)

    # Step 2: Analyze the handwriting
    st.subheader("Step 2: Graphological Analysis")

    # Placeholder for real analysis
    st.write("Running graphology analysis...")

    # Simulated psychological traits (you can replace with real ML/NLP-based output)
    st.success("✅ Psychological Profile Extracted:")
    st.markdown("""
    - **Emotional state**: Balanced  
    - **Stress level**: Low  
    - **Self-confidence**: High  
    - **Thinking style**: Analytical  
    - **Sociability**: Moderate  
    - **Discipline**: Strong  
    """)

    # Optional explanation
    with st.expander("ℹ️ What does this mean?"):
        st.write("""
        These traits are inferred based on stroke patterns, spacing, slant, and size of your handwriting. 
        Graphology can offer insight into personality, emotional state, and behavioral tendencies.
        """)

    # CTA button
    st.button("🔄 Analyze Another Sample")

else:
    st.info("Please upload a handwriting image to begin the analysis.")
