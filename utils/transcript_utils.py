import datetime

def add_message_to_transcript(transcripts_collection, session_id, user_id, message):
    """
    Add a message to the transcript for a specific session.
    
    Args:
        transcripts_collection: MongoDB collection for transcripts
        session_id: Unique identifier for the session
        user_id: User identifier (login code)
        message: Message to add to the transcript
        
    Returns:
        None
    """
    # Check if the user document exists in the MongoDB collection
    user_doc = transcripts_collection.find_one({"_id": user_id})
    
    if user_doc is None:
        # Create a new document for the user with an empty sessions list
        transcripts_collection.insert_one({
            "_id": user_id,
            "sessions": []
        })
    
    # Check if the session exists in the user's sessions list
    session_exists = False
    if user_doc and "sessions" in user_doc:
        for session in user_doc["sessions"]:
            if session["session_id"] == session_id:
                session_exists = True
                # Add the message to the existing session's transcript
                transcripts_collection.update_one(
                    {"_id": user_id, "sessions.session_id": session_id},
                    {"$push": {"sessions.$.transcript": message}}
                )
                break
    
    if not session_exists:
        # Create a new session in the user's sessions list
        transcripts_collection.update_one(
            {"_id": user_id},
            {"$push": {"sessions": {
                "session_id": session_id,
                "transcript": [message],
                "date": datetime.datetime.now()
            }}}
        )

def save_transcript(transcripts_collection, session_id, user_id, chat_history):
    """
    Save the complete transcript to the database.
    
    Args:
        transcripts_collection: MongoDB collection for transcripts
        session_id: Unique identifier for the session
        user_id: User identifier (login code)
        chat_history: Complete chat history to save
        
    Returns:
        None
    """
    # Check if the user document exists
    user_doc = transcripts_collection.find_one({"_id": user_id})
    
    if user_doc is None:
        # Create a new document for the user with the session
        transcripts_collection.insert_one({
            "_id": user_id,
            "sessions": [{
                "session_id": session_id,
                "transcript": chat_history,
                "date": datetime.datetime.now()
            }]
        })
    else:
        # Check if the session already exists
        session_exists = False
        if "sessions" in user_doc:
            for session in user_doc["sessions"]:
                if session["session_id"] == session_id:
                    session_exists = True
                    # Update the existing session
                    transcripts_collection.update_one(
                        {"_id": user_id, "sessions.session_id": session_id},
                        {"$set": {"sessions.$.transcript": chat_history}}
                    )
                    break
        
        if not session_exists:
            # Add a new session to the user's sessions list
            transcripts_collection.update_one(
                {"_id": user_id},
                {"$push": {"sessions": {
                    "session_id": session_id,
                    "transcript": chat_history,
                    "date": datetime.datetime.now()
                }}}
            ) 