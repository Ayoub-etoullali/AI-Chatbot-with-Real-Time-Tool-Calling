import streamlit as st
import asyncio
import sys

from app import run

# 🎨 Page config
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

# 💡 Custom CSS for styling
st.markdown("""
    <style>
        /* Gradient header */
        .main-header {
            font-size: 2.5em;
            font-weight: bold;
            text-align: center;
            background: linear-gradient(90deg, #4facfe, #00f2fe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 2em;
        }
        .below-header {
            text-align: center;
            margin-bottom: 0.5em;
        }
        /* Footer */
        .footer {
            text-align: center;
            margin-top: 2em;
            font-size: 0.9em;
            color: gray;
        }
    </style>
""", unsafe_allow_html=True)

# 🚀 Header
st.markdown('<div class="main-header"> AI Chatb🤖t with Real-Time Function/Tool Calling</div>', unsafe_allow_html=True)
# st.markdown('<div class="below-header">Built with <b>Streamlit + Open Source LLMs + Python + APIs</b></div>', unsafe_allow_html=True)

# Add an image below the title
# st.image(
#     "../data/images/Function Calling.jpg",
#     caption="Built with Streamlit + Open Source LLMs + Python + APIs",
#     use_container_width=True,
# )

# Session state for messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous messages in a chat format
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box at the bottom (chat style)
if prompt := st.chat_input("Type your question..."):
    # Save and display user message
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Placeholder for assistant response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("Thinking...")

        try:
            # Call your LLM with function calling
            response = asyncio.run(run("llama3.2:3b", prompt))

            if not response:
                placeholder.markdown("⚠️ No response from model.")
                sys.exit()

            # If your run() supports streaming responses
            if hasattr(response, "stream"):
                final_response = response.stream(st.session_state["messages"])
                full_text = st.write_stream(final_response)
            else:
                # Fallback if no streaming
                full_text = response.content if hasattr(response, "content") else str(response)
                placeholder.markdown(full_text)

        except Exception as e:
            full_text = f"⚠️ Error: {e}"
            placeholder.markdown(full_text)

        # Save assistant response
        st.session_state["messages"].append({"role": "assistant", "content": full_text})

# 🖊️ Footer
st.markdown(
    '''
    <div class="footer">
        ⚡ Powered by <a href="https://ayoub-etoullali.netlify.app/" target="_blank" style="color:#FF5733; text-decoration:none; font-weight:bold;">
        Ayoub ETOULLALI</a>
    </div>
    ''',
    unsafe_allow_html=True
)
