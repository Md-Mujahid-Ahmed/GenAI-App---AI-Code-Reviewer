import streamlit as st
import google.generativeai as ai

# Configure API key (securely)
# import os
# api_key = os.getenv("GOOGLE_GEN_AI_API_KEY")
# if not api_key:
#     st.error("API key is not set. Please configure it in environment variables.")
# else:
#     ai.configure(api_key=api_key)
api_key = 'AIzaSyDHvo2RmhF-0YkXGvbw8uFeLDHL66Gvas0'
ai.configure(api_key=api_key)

# # Set up the page configuration
st.set_page_config(page_title="Data Science AI Mentor", layout="centered")

# Title and header
st.title("🐍 Python Code Reviewer Bot")
st.header("by Md Mujahid Ahmed")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
    

# System prompt for the AI model
sys_prompt = """You are an advanced AI specializing in reviewing Python code.
When a user submits Python code, return:
1. A list of issues with the code (e.g., syntax errors, logic flaws, inefficiencies).
2. Suggestions for improvement.
3. A corrected or improved version of the code.
Ensure the feedback is clear and helpful."""

# Initialize the model once
model = ai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=sys_prompt)
chat = model.start_chat(history=[])
 
# # Sidebar with information and options
with st.sidebar:
    st.markdown("### About 🐍 Python Code Reviewer Bot")
    st.info(
        """
        This AI-powered bot reviews your Python code, identifies potential issues, 
        and provides suggestions along with corrected versions.
        """
    )

user_prompt = st.text_area("Paste your Python code here and press Tab:", height=200)

# Handle AI response
if user_prompt:
    st.markdown("### 🚀 Submitted Code")
    st.code(user_prompt, language="python")

    try:
        response = chat.send_message(user_prompt)
        if response and hasattr(response, "text"):
            # Add to chat history
            st.session_state["chat_history"].append({"role": "user", "content": user_prompt})
            st.session_state["chat_history"].append({"role": "ai", "content": response.text})
            # Display AI response
            st.markdown("### 🔍 AI Feedback and Suggestions")
            st.write(response.text)
        else:
            st.error("Failed to get a valid response from the AI.")
    except Exception as e:
        st.error(f"Error: {e}")
