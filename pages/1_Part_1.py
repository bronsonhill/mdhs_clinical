import streamlit as st
from openai import OpenAI
import json


# Set up OpenAI API client
client = OpenAI(api_key=st.secrets["OPENAI_API_1"])

# Select GPT model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

st.title("Part 1")

def setprompt(part):
    if "system_prompt" not in st.session_state:
        st.session_state["system_prompt"] = ""

    with open("parts.json", "r") as file:
        data = json.load(file)
        st.session_state["system_prompt"] = data[part]

setprompt("part1")


if "chat_history_1" not in st.session_state:
    st.session_state["chat_history_1"] = []

if not st.session_state["chat_history_1"]:
    greeting = """Hello. Let's discuss the research context."""
    st.session_state.chat_history_1 = [{"role": "assistant", "content": greeting}]

# Write chat history
for message in st.session_state.chat_history_1:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat logic
if prompt := st.chat_input("Ask the supervisor questions"):
    st.session_state.chat_history_1.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        messages_with_system_prompt = [{"role": "system", "content": st.session_state["system_prompt"]}] + [
            {"role": m["role"], "content": m["content"]}
        for m in st.session_state.chat_history_1
        ]

        stream = client.chat.completions.create(
            model = st.session_state["openai_model"],
            messages = messages_with_system_prompt,
            stream = True,
        )
        response = st.write_stream(stream)

    st.session_state.chat_history_1.append({"role": "assistant", "content": response})