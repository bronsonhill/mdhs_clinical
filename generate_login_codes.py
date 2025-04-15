import streamlit as st
from utils.db_connection import get_db
from utils.login_code_generator import save_login_codes, get_unused_codes_count

st.title("Login Code Generator")

# Get database connection
db = get_db()

# Display current unused codes count
unused_count = get_unused_codes_count(db)
st.write(f"Current number of unused codes: {unused_count}")

# Input for number of codes to generate
num_codes = st.number_input("Number of codes to generate", min_value=1, max_value=100, value=10)

# Input for code length
code_length = st.number_input("Code length", min_value=4, max_value=12, value=8)

if st.button("Generate Codes"):
    # Generate and save the codes
    generated_codes = save_login_codes(db, num_codes, code_length)
    
    # Display the generated codes
    st.write("Generated Codes:")
    for code in generated_codes:
        st.code(code)
    
    # Update and display the new unused codes count
    new_unused_count = get_unused_codes_count(db)
    st.write(f"New number of unused codes: {new_unused_count}") 