import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from modules.nav import show_sidebar_logo
load_dotenv()
# Configure Gemini API
def configure_gemini():
    """Configure Gemini API with the API key"""
    try:
        # Try to get API key from environment variable
        api_key = 'AIzaSyBVZQKiYt42GYvhdzMI7RKawIYSw2i2ga4' or os.getenv('GEMINI_API_KEY')
        if not api_key:
            # If not in environment, check if it's in streamlit secrets
            api_key = st.secrets.get('GEMINI_API_KEY', None)
        
        if api_key:
            genai.configure(api_key=api_key)
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Error configuring Gemini API: {e}")
        return False

def get_gemini_response(prompt, chat_history=None):
    """Get response from Gemini AI"""
    try:
        # Initialize the model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # If there's chat history, use it for context
        if chat_history:
            # Create a conversation context
            conversation = []
            for message in chat_history:
                conversation.append(f"User: {message['user']}")
                conversation.append(f"Assistant: {message['assistant']}")
            
            # Add current prompt
            full_prompt = "\n".join(conversation) + f"\nUser: {prompt}\nAssistant:"
        else:
            full_prompt = prompt
        
        # Generate response
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {e}"

def main():
    """Main chatbot interface"""
    show_sidebar_logo()
    
    st.title("🤖 MindFlow AI Chatbot")
    st.markdown("Ask me anything about handwriting analysis, facial expressions, or psychological insights!")
    
    # Configure Gemini API
    if not configure_gemini():
        st.error("⚠️ Gemini API key not found!")
        st.markdown("""
        To use this chatbot, you need to set up your Gemini API key:
        1. Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Add it as an environment variable: `GEMINI_API_KEY=your_api_key_here`
        3. Or add it to your Streamlit secrets.toml file
        """)
        return
    
    # Initialize session state for chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Initialize previous chats storage
    if "previous_chats" not in st.session_state:
        st.session_state.previous_chats = []
    
    if "current_chat_id" not in st.session_state:
        st.session_state.current_chat_id = 0
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Get response from Gemini
                response = get_gemini_response(prompt, st.session_state.chat_history)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Update chat history for context
        st.session_state.chat_history.append({
            "user": prompt,
            "assistant": response
        })
    
    # Show suggested questions only if chat hasn't started yet
    if len(st.session_state.messages) == 0:
        # Suggested Questions Section (above chat input)
        st.markdown("### 💡 Suggested Questions")
        
        # Create columns for better layout
        col1, col2 = st.columns(2)
        
        suggested_questions = [
            "What can handwriting analysis reveal about personality?",
            "How does facial expression analysis work?",
            "What are the signs of stress in handwriting?",
            "Can you analyze emotional states from facial expressions?",
            "What psychological insights can be gained from writing patterns?"
        ]
        
        for i, question in enumerate(suggested_questions):
            col = col1 if i % 2 == 0 else col2
            with col:
                if st.button(question, key=f"suggestion_{i}", use_container_width=True):
                    # Add the suggestion to the chat
                    st.session_state.messages.append({"role": "user", "content": question})
                    
                    # Generate response
                    response = get_gemini_response(question, st.session_state.chat_history)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    # Update chat history
                    st.session_state.chat_history.append({
                        "user": question,
                        "assistant": response
                    })
                    
                    st.rerun()
        
        st.markdown("---")  # Separator line
    


if __name__ == "__main__":
    main()