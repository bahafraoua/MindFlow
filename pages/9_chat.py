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
        api_key = 'AIzaSyBVZQKiYt42GYvhdzMI7RKawIYSw2i2ga4' or os.getenv('GEMINI_API_KEY')
        if not api_key:
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
        model = genai.GenerativeModel('gemini-1.5-flash')
        if chat_history:
            conversation = []
            for message in chat_history:
                conversation.append(f"User: {message['user']}")
                conversation.append(f"Assistant: {message['assistant']}")
            full_prompt = "\n".join(conversation) + f"\nUser: {prompt}\nAssistant:"
        else:
            full_prompt = prompt
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {e}"

def main():
    """Main chatbot interface"""
    show_sidebar_logo()
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .chat-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .chat-item {
        background: transparent !important;
        box-shadow: none !important;
        padding: 0.5rem 0;
    }
    .chat-button {
        border: none !important;
        background: transparent !important;
        text-align: left !important;
        padding: 0.5rem !important;
    }
    .ellipsis-button {
        border: none !important;
        background: transparent !important;
        color: #666 !important;
        font-size: 1.2rem !important;
    }
    /* Remove all button borders in sidebar */
    .stButton > button {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }
    /* Remove borders specifically for secondary buttons */
    button[kind="secondary"] {
        border: none !important;
        box-shadow: none !important;
        background: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<h1 class="main-header">🤖 MindFlow AI Chatbot</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your intelligent assistant for handwriting analysis, facial expressions, and psychological insights</p>', unsafe_allow_html=True)

    if not configure_gemini():
        st.error("⚠️ Gemini API key not found!")
        st.markdown("""
        <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px; padding: 1rem; margin: 1rem 0;">
        <h4 style="color: #856404; margin-top: 0;">🔑 API Setup Required</h4>
        <p style="color: #856404; margin-bottom: 0;">To use this chatbot, you need to set up your Gemini API key:</p>
        <ol style="color: #856404;">
            <li>Get your API key from <a href="https://makersuite.google.com/app/apikey" target="_blank">Google AI Studio</a></li>
            <li>Add it as an environment variable: <code>GEMINI_API_KEY=your_api_key_here</code></li>
            <li>Or add it to your Streamlit secrets.toml file</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
        return
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "previous_chats" not in st.session_state:
        st.session_state.previous_chats = []
    
    if "current_chat_id" not in st.session_state:
        st.session_state.current_chat_id = 0

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("💬 Ask me about handwriting analysis, facial expressions, or psychological insights..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_gemini_response(prompt, st.session_state.chat_history)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.chat_history.append({
            "user": prompt,
            "assistant": response
        })
    
    # --- COMMENTED OUT: Suggested Questions Section ---
    # Uncomment below to add suggested questions feature back
    # 
    # # Show suggested questions only if chat hasn't started yet
    # if len(st.session_state.messages) == 0:
    #     # Suggested Questions Section (above chat input)
    #     st.markdown("### 💡 Suggested Questions")
    #     
    #     # Create columns for better layout
    #     col1, col2 = st.columns(2)
    #     
    #     suggested_questions = [
    #         "What can handwriting analysis reveal about personality?",
    #         "How does facial expression analysis work?",
    #         "What are the signs of stress in handwriting?",
    #         "Can you analyze emotional states from facial expressions?",
    #         "What psychological insights can be gained from writing patterns?"
    #     ]
    #     
    #     for i, question in enumerate(suggested_questions):
    #         col = col1 if i % 2 == 0 else col2
    #         with col:
    #             if st.button(question, key=f"suggestion_{i}", use_container_width=True):
    #                 # Add the suggestion to the chat
    #                 st.session_state.messages.append({"role": "user", "content": question})
    #                 
    #                 # Generate response
    #                 response = get_gemini_response(question, st.session_state.chat_history)
    #                 st.session_state.messages.append({"role": "assistant", "content": response})
    #                 
    #                 # Update chat history
    #                 st.session_state.chat_history.append({
    #                     "user": question,
    #                     "assistant": response
    #                 })
    #                 
    #                 st.rerun()
    #     
    #     st.markdown("---")  # Separator line
    
    with st.sidebar:
        if st.button("🆕 New Chat", type="primary", use_container_width=True):
            if len(st.session_state.messages) > 0:
                content = st.session_state.messages[0]["content"]
                chat_title = content[:30] if len(content) <= 30 else content[:27] + "..."
                st.session_state.previous_chats.append({
                    "id": st.session_state.current_chat_id,
                    "title": chat_title,
                    "messages": st.session_state.messages.copy(),
                    "chat_history": st.session_state.chat_history.copy()
                })
            
            st.session_state.messages = []
            st.session_state.chat_history = []
            st.session_state.current_chat_id += 1
            st.rerun()

        if len(st.session_state.previous_chats) > 0:
            st.markdown('---')
            st.markdown("### 📚 Chat History")
            for i, chat in enumerate(reversed(st.session_state.previous_chats[-5:])):
                unique_key = f"prev_chat_{i}_{chat['id']}_{len(st.session_state.previous_chats)}"
                delete_key = f"delete_{i}_{chat['id']}_{len(st.session_state.previous_chats)}"
                with st.container():
                    chat_col, delete_col = st.columns([9, 1])
                    
                    with chat_col:
                        if st.button(f"{chat['title']}", key=unique_key, use_container_width=True, type="secondary"):
                            if len(st.session_state.messages) > 0:
                                content = st.session_state.messages[0]["content"]
                                current_title = content[:30] if len(content) <= 30 else content[:27] + "..."
                                current_exists = any(c["id"] == st.session_state.current_chat_id for c in st.session_state.previous_chats)
                                if not current_exists:
                                    st.session_state.previous_chats.append({
                                        "id": st.session_state.current_chat_id,
                                        "title": current_title,
                                        "messages": st.session_state.messages.copy(),
                                        "chat_history": st.session_state.chat_history.copy()
                                    })
                            
                            st.session_state.messages = chat["messages"].copy()
                            st.session_state.chat_history = chat["chat_history"].copy()
                            st.session_state.current_chat_id = chat["id"]
                            st.rerun()
                    
                    with delete_col:
                        if st.button("🗑️", key=delete_key, help="Delete this chat", use_container_width=True, type="secondary"):
                            st.session_state.previous_chats = [c for c in st.session_state.previous_chats if c["id"] != chat["id"]]
                            st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()