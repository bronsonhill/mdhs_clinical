import datetime

def add_message_to_transcript(transcripts_collection, session_id, message):
    """
    Add a message to the transcript for a specific session.
    
    Args:
        transcripts_collection: MongoDB collection for transcripts
        session_id: Unique identifier for the session
        message: Message to add to the transcript
        
    Returns:
        None
    """
    # Check if the session exists in the MongoDB collection
    existing_transcript = transcripts_collection.find_one({"_id": session_id})
    if existing_transcript is None:
        transcripts_collection.insert_one({"_id": session_id, "transcript": []})  # Create a new document for the session
    transcripts_collection.update_one({"_id": session_id}, {"$push": {"transcript": message}})  # Append the message to the session's list

def save_transcript(transcripts_collection, session_id, chat_history):
    """
    Save the complete transcript to the database.
    
    Args:
        transcripts_collection: MongoDB collection for transcripts
        session_id: Unique identifier for the session
        chat_history: Complete chat history to save
        
    Returns:
        None
    """
    transcript = {
        "_id": session_id,
        "date": datetime.datetime.now(),
        "transcript": chat_history
    }
    
    transcripts_collection.replace_one(filter={"_id": session_id}, replacement=transcript, upsert=True) 