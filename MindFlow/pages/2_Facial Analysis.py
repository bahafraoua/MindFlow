import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Page title
st.title("📷 Facial Analysis")
st.markdown("### Detect emotions in real time from a captured image or webcam")
st.logo(image="images\MindFlowHorizental.png",
        icon_image="images\MindFlow.png")
# Step 1: Choose image source
st.subheader("Step 1: Upload or Capture Image")

option = st.radio("Choose input method:", ["📁 Upload Image", "📸 Use Webcam"])

# Step 2: Image input
image = None

if option == "📁 Upload Image":
    uploaded_file = st.file_uploader("Upload a face image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

elif option == "📸 Use Webcam":
    picture = st.camera_input("Take a picture")
    if picture:
        image = Image.open(picture)
        st.image(image, caption="Captured from Webcam", use_column_width=True)

# Step 3: Analyze emotions
if image:
    st.subheader("Step 2: Emotion Detection")

    # Placeholder for emotion detection (simulate result)
    # You can replace this with your real ML model
    st.write("Running emotion detection model...")

    # For now, simulate detected emotion
    detected_emotion = "😊 Joy (75%)"

    # Show result
    st.success(f"**Detected Emotion:** {detected_emotion}")

    # Optional: Show more breakdown
    st.markdown("#### Emotion Probabilities (Example)")
    st.progress(0.75)  # Joy
    st.text("😊 Joy: 75%")
    st.text("😢 Sadness: 10%")
    st.text("😠 Anger: 5%")
    st.text("😐 Neutral: 10%")

    # Button to analyze again
    st.button("🔄 Run Again")

else:
    st.info("Please upload or capture a facial image to begin analysis.")
