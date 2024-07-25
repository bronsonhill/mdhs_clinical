import streamlit as st
from openai import OpenAI


# Select GPT model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"


st.title("Home")
st.markdown(
"""
There are three parts to this chatbot activity:
- Part 1: A research problem analysis with a virtual policy analyst. 
- Item 2: Designing a study with a virtual clinical epidemiologist.
- Item 3: Learning to minimise bias with a supervisor.
"""
)