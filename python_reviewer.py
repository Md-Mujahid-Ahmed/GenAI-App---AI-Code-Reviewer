import streamlit as st
import google.generativeai as ai

# Configure API key (securely)
api_key = 'AIzaSyDHvo2RmhF-0YkXGvbw8uFeLDHL66Gvas0'
ai.configure(api_key=api_key)

# Set up the page configuration
st.set_page_config(page_title="Python Code Reviewer Bot", layout="centered")

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

# Sidebar with information and options
with st.sidebar:
    st.markdown("### About 🐍 Python Code Reviewer Bot")
    st.info(
        """
        This AI-powered bot reviews your Python code, identifies potential issues, 
        and provides suggestions along with corrected versions.
        """
    )
    # Clear chat history
    if st.button("Clear Chat History"):
        st.session_state["chat_history"] = []

# Text area for user input
user_prompt = st.text_area("Paste your Python code here:", height=200)

# Handle AI response when user submits code
if user_prompt:
    st.markdown("### 🚀 Submitted Code")
    st.code(user_prompt, language="python")

    try:
        # Get AI response
        response = ai.chat(
            model="models/text-bison-001",  # Replace with your available model
            messages=[
                {"content": sys_prompt},  # System prompt as context
                {"content": user_prompt}  # User input as prompt
            ]
        )

        # Validate and display AI response
        if response and "candidates" in response and len(response["candidates"]) > 0:
            ai_feedback = response["candidates"][0]["content"]

            # Add to chat history
            st.session_state["chat_history"].append({"role": "user", "content": user_prompt})
            st.session_state["chat_history"].append({"role": "ai", "content": ai_feedback})

            # Display AI feedback
            st.markdown("### 🔍 AI Feedback and Suggestions")
            st.write(ai_feedback)
        else:
            st.error("Failed to get a valid response from the AI.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Display chat history in the sidebar
with st.sidebar:
    st.markdown("### 💬 Conversation History")
    for entry in st.session_state["chat_history"]:
        if entry["role"] == "user":
            st.write(f"**🧑‍💻 You:** {entry['content']}")
        else:
            st.write(f"**🤖 AI:** {entry['content']}")
