import streamlit as st
import json
import uuid
from pymongo import MongoClient
from bson import ObjectId, Binary
from openai import OpenAI
from utils.db_connection import get_db
from utils.transcript_utils import add_message_to_transcript, save_transcript
from utils.login_code_generator import verify_login_code

# Check for login code
if "login_code" not in st.session_state or not st.session_state["login_code"]:
    st.warning("Please enter your login code on the home page to access this content.")
    st.stop()

# Set up OpenAI API client
client = OpenAI(api_key=st.secrets["OPENAI_API_1"])

# Select GPT model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Get the collection for this part
transcripts = get_db()["part1_transcripts"]

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

    # Use the modularized function to add messages to the transcript
    session_id = st.session_state["uuid"]  # Use the existing UUID for session management
    user_id = st.session_state.get("user_id", "anonymous")  # Get user ID from session state, default to "anonymous"
    add_message_to_transcript(transcripts, session_id, user_id, {"role": "user", "content": prompt})
    add_message_to_transcript(transcripts, session_id, user_id, {"role": "assistant", "content": response})

    # Save the complete transcript
    save_transcript(transcripts, session_id, user_id, st.session_state["chat_history_1"])