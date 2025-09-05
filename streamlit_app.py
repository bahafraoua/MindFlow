import streamlit as st
import uuid
from modules.nav import show_sidebar_logo

show_sidebar_logo()

st.set_page_config(
    layout='centered',
    page_title='MindFlow'
)

def main():
    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())

    with st.sidebar:
        st.write(f"**User ID:** `{st.session_state.user_id[:8]}...`")
        if st.button("🔄 New User Session"):
            st.session_state.user_id = str(uuid.uuid4())
            st.rerun()
    
    st.header('MindFlow')
    st.write("MindFlow is an AI-powered platform that analyzes handwriting and facial expressions to detect emotions and assess psychological well-being in the workplace.")
    
    st.info("💡 Each user session has a unique ID. All your analyses are stored under your user ID in the database structure: `users/{user_id}/analysis/{analysis_id}`")

if __name__ == '__main__':
    main()
