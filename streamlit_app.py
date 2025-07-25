import streamlit as st
from modules.nav import show_sidebar_logo

show_sidebar_logo()

st.set_page_config(
    layout='centered',
    page_title='MindFlow'
)

def main():
    # Nav()
    st.header('MindFlow')
    st.write("MindFlow is an AI-powered platform that analyzes handwriting and facial expressions to detect emotions and assess psychological well-being in the workplace.")

if __name__ == '__main__':
    main()
