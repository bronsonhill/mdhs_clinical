import streamlit as st
from pymongo import MongoClient

@st.cache_resource
def get_db():
    mongodb_username = st.secrets["MONGODB_USERNAME"]
    mongodb_password = st.secrets["MONGODB_PW"]
    mongodb_cluster = st.secrets["MONGODB_CLUSTER"]

    db_string = f"mongodb+srv://{mongodb_username}:{mongodb_password}@2025s1.tmkd7de.mongodb.net/?retryWrites=true&w=majority&appName={mongodb_cluster}"

    client = MongoClient(db_string)

    db = client["chat_transcripts"] # chat_transcripts is the database

    return db # Return the collection (part1_transcripts, part2_transcripts, part3_transcripts) 