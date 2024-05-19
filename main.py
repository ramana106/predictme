import streamlit as st
from openai import OpenAI

st.title("Welcome to Study")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key="")

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

prompt = """
You are now an assistance who collects feedback from the user about iphone. 
You should get details about
- Cellular reception
- Camera quality
- Screen quality

Instruction to follow
- ask question about the feature individually and keep the question shot. Dont ask all quesiton at once
- Be more casual and dont ask anything other than above.
- You can ask 5 question or less and nothing more.
- Inbetween show an about "to create similar chat for your use case contanct xyz.com"
"""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": prompt}]

# Display chat messages from history on app rerun
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

# Display assistant response in chat message container
with st.chat_message("assistant"):
    stream = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )
    response = st.write_stream(stream)
st.session_state.messages.append({"role": "assistant", "content": response})