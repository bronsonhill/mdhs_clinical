import secrets
import string
import datetime
from pymongo import MongoClient
import streamlit as st
import sys
import os
import csv
from pathlib import Path

# Import get_db from the new module
from .db_connection import get_db

def generate_login_code(length=8):
    """
    Generate a random login code of specified length.
    
    Args:
        length: Length of the login code (default: 8)
        
    Returns:
        str: Generated login code
    """
    # Define the character set for the login code
    characters = string.ascii_uppercase + string.digits
    
    # Generate a random code
    code = ''.join(secrets.choice(characters) for _ in range(length))
    return code

def save_login_codes(db, num_codes, length=8):
    """
    Generate and save a specified number of login codes to the database and export to CSV.
    
    Args:
        db: MongoDB database instance
        num_codes: Number of codes to generate
        length: Length of each code (default: 8)
        
    Returns:
        list: List of generated codes
    """
    # Get or create the login_codes collection
    login_codes = db["login_codes"]
    
    generated_codes = []
    current_time = datetime.datetime.now()
    
    for _ in range(num_codes):
        code = generate_login_code(length)
        # Create document for the code
        code_doc = {
            "code": code,
            "created_at": current_time,
            "used": False,
            "used_at": None
        }
        
        # Insert the code into the database
        login_codes.insert_one(code_doc)
        generated_codes.append(code)
    
    # Export codes to CSV
    export_dir = Path("exports")
    export_dir.mkdir(exist_ok=True)
    
    timestamp = current_time.strftime("%Y%m%d_%H%M%S")
    csv_filename = export_dir / f"login_codes_{timestamp}.csv"
    
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Code', 'Created At', 'Used', 'Used At'])
        for code in generated_codes:
            writer.writerow([code, current_time, 'False', ''])
    
    return generated_codes

def verify_login_code(code):
    """
    Verify if a login code is valid and mark it as used.
    
    Args:
        code: Login code to verify
        
    Returns:
        str or bool: The login code if valid and unused, False otherwise
    """
    db = get_db()
    login_codes = db["login_codes"]
    
    result = login_codes.find_one({"code": code})
    
    if result:
        # Mark the code as used
        login_codes.update_one(
            {"_id": result["_id"]},
            {"$set": {"used": True, "used_at": datetime.datetime.now()}}
        )
        return code  # Return the code itself as the user ID
    return False

def get_unused_codes_count(db):
    """
    Get the count of unused login codes.
    
    Args:
        db: MongoDB database instance
        
    Returns:
        int: Number of unused codes
    """
    login_codes = db["login_codes"]
    return login_codes.count_documents({"used": False})


# Only run this code when the script is run directly, not when imported as a module
if __name__ == "__main__":
    print("Generating 30 login codes...")
    save_login_codes(get_db(), 30)
    print("Login codes generated successfully!")