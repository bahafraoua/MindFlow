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

  


if __name__ == '__main__':
    main()
