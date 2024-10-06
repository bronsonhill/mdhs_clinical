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

def get_db(part):
    mongodb_username = st.secrets["MONGODB_USERNAME"]
    mongodb_password = st.secrets["MONGODB_PW"]
    mongodb_cluster = st.secrets["MONGODB_CLUSTER"]

    db_string = f"mongodb+srv://{mongodb_username}:{mongodb_password}@{mongodb_cluster}.2pqhy.mongodb.net/?retryWrites=true&w=majority&appName={mongodb_cluster}"

    client = MongoClient(db_string)

    db = client["chat_transcripts"] # chat_transcripts is the database

    return db[part] # Return the collection (part1_transcripts, part2_transcripts, part3_transcripts)


st.title("Home")
st.markdown(
"""
There are three parts to this chatbot activity:
- Part 1: A research problem analysis with a virtual policy analyst. 
- Item 2: Designing a study with a virtual clinical epidemiologist.
- Item 3: Learning to minimise bias with a supervisor.
"""
)