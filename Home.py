import streamlit as st
import uuid
import bson
from openai import OpenAI
from pymongo import MongoClient


# Select GPT model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Get a uuid for the session
if "uuid" not in st.session_state:
    unique_id =  bson.Binary.from_uuid(uuid.uuid4())
    st.session_state["uuid"] = unique_id

@st.cache_resource
def get_db():
    mongodb_username = st.secrets["MONGODB_USERNAME"]
    mongodb_password = st.secrets["MONGODB_PW"]
    mongodb_cluster = st.secrets["MONGODB_CLUSTER"]

    db_string = f"mongodb+srv://{mongodb_username}:{mongodb_password}@2025s1.tmkd7de.mongodb.net/?retryWrites=true&w=majority&appName={mongodb_cluster}"

    client = MongoClient(db_string)

    db = client["chat_transcripts"] # chat_transcripts is the database

    return db # Return the collection (part1_transcripts, part2_transcripts, part3_transcripts)


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