import streamlit as st
import uuid
from pymongo import MongoClient
from bson import ObjectId, Binary
from openai import OpenAI
from utils.login_code_generator import verify_login_code


# Generate a unique ID for this session
unique_id = Binary.from_uuid(uuid.uuid4())
st.session_state["uuid"] = unique_id


st.title("Home")
with st.expander("ℹ️ Disclaimer", expanded=True):
    st.caption("Please note that chat transcripts are being stored and may be reviewed for the purposes of improving this tool.")

st.markdown(
"""
There are three parts to this chatbot activity:
- Part 1: A research problem analysis with a virtual policy analyst. 
- Item 2: Designing a study with a virtual clinical epidemiologist.
- Item 3: Learning to minimise bias with a supervisor.
"""
)

st.session_state.login_code = st.text_input("Enter your login code here: ")

if st.session_state.login_code:
    user_id = verify_login_code(st.session_state.login_code)
    if user_id:
        st.session_state["user_id"] = user_id  # Store the login code as the user ID
        st.write("Login successful")
    else:
        st.write("Login code is invalid")
