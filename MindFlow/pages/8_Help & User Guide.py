import streamlit as st

# Page title
st.title("📚 Help & User Guide")
st.logo(image="images\MindFlowHorizental.png",
        icon_image="images\MindFlow.png")
st.markdown("""
Welcome to the MindFlow Help Center. Here you will find tutorials, step-by-step instructions, and answers to common questions.

---

### 📖 Tutorials

- **Getting Started with MindFlow**  
  Learn how to upload images, run analyses, and interpret your results.  
  [Watch tutorial video](https://www.example.com/tutorial) *(replace with your actual link)*

- **Facial Emotion Analysis**  
  Step-by-step guide to capture and analyze emotions using the webcam or image upload.

- **Handwriting Analysis**  
  How to upload handwriting samples and understand graphology results.

---

### 🛠 Instructions

1. **Upload your facial image or handwriting sample from the sidebar.**  
2. **View your psychological state on the Dashboard.**  
3. **Check your history of analyses in the Results page.**  
4. **Download reports for HR or personal use.**  
5. **Adjust your preferences in the Settings page.**

---

### ❓ Frequently Asked Questions (FAQs)

**Q: Is my data private and secure?**  
A: Yes, MindFlow complies with GDPR and anonymizes all data to protect your privacy.

**Q: Can I use MindFlow on my mobile device?**  
A: Yes, the platform is optimized for desktop and mobile browsers.

**Q: How often should I perform new analyses?**  
A: We recommend regular check-ins, at least weekly, to monitor psychological well-being trends.

**Q: Who can access my results?**  
A: Only you and authorized HR personnel (with your consent) can access your reports.

**Q: Can I delete my data?**  
A: Yes, please contact support at [privacy@mindflow.ai](mailto:privacy@mindflow.ai) to request data deletion.

---

If you have any other questions or need help, please contact our support team at:  
**support@mindflow.ai**
""")
