#!/usr/bin/env python3
"""
Script to export all MongoDB collections to structured text files.
This script connects to the MongoDB database and exports all collections
to individual text files organized by part in separate folders.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from bson import Binary, ObjectId

# Add the parent directory to the path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db_connection import get_db

def create_export_directory():
    """Create the export directory if it doesn't exist."""
    export_dir = Path("data_export")
    export_dir.mkdir(exist_ok=True)
    return export_dir

def create_part_directory(export_dir, part_name):
    """Create a directory for a specific part."""
    part_dir = export_dir / part_name
    part_dir.mkdir(exist_ok=True)
    return part_dir

def format_transcript_content(doc):
    """Format a transcript document into readable text."""
    content_parts = []
    
    # Add metadata header
    content_parts.append("=" * 60)
    content_parts.append(f"TRANSCRIPT METADATA")
    content_parts.append("=" * 60)
    
    # Add basic metadata
    if '_id' in doc:
        content_parts.append(f"Document ID: {doc['_id']}")
    if 'timestamp' in doc:
        content_parts.append(f"Timestamp: {doc['timestamp']}")
    if 'created_at' in doc:
        content_parts.append(f"Created At: {doc['created_at']}")
    
    content_parts.append("")
    
    # Add sessions/conversations
    if 'sessions' in doc:
        sessions = doc['sessions']
        if isinstance(sessions, list):
            for session_index, session in enumerate(sessions, 1):
                content_parts.append("=" * 60)
                content_parts.append(f"SESSION {session_index}")
                content_parts.append("=" * 60)
                content_parts.append("")
                
                # Add session metadata
                if 'session_id' in session:
                    content_parts.append(f"Session ID: {session['session_id']}")
                if 'date' in session:
                    content_parts.append(f"Date: {session['date']}")
                content_parts.append("")
                
                # Add conversation
                if 'transcript' in session:
                    transcript = session['transcript']
                    if isinstance(transcript, list):
                        for message in transcript:
                            if isinstance(message, dict):
                                role = message.get('role', 'Unknown')
                                content = message.get('content', '')
                                
                                # Format as "Role: [content]"
                                if role.lower() == 'assistant':
                                    content_parts.append(f"Assistant: {content}")
                                elif role.lower() == 'user':
                                    content_parts.append(f"User: {content}")
                                else:
                                    content_parts.append(f"{role.capitalize()}: {content}")
                                content_parts.append("")
                    else:
                        content_parts.append(f"Transcript (raw): {transcript}")
                
                content_parts.append("")
        else:
            content_parts.append(f"Sessions (raw): {sessions}")
    
    # Add messages field if it exists (for backward compatibility)
    elif 'messages' in doc:
        content_parts.append("=" * 60)
        content_parts.append(f"CONVERSATION")
        content_parts.append("=" * 60)
        content_parts.append("")
        
        messages = doc['messages']
        if isinstance(messages, list):
            for message in messages:
                if isinstance(message, dict):
                    role = message.get('role', 'Unknown')
                    content = message.get('content', '')
                    
                    # Format as "Role: [content]"
                    if role.lower() == 'assistant':
                        content_parts.append(f"Assistant: {content}")
                    elif role.lower() == 'user':
                        content_parts.append(f"User: {content}")
                    else:
                        content_parts.append(f"{role.capitalize()}: {content}")
                    content_parts.append("")
        else:
            content_parts.append(f"Messages (raw): {messages}")
    
    # Add any other fields
    other_fields = {k: v for k, v in doc.items() 
                   if k not in ['_id', 'session_number', 'timestamp', 'created_at', 'messages', 'sessions']}
    
    if other_fields:
        content_parts.append("=" * 60)
        content_parts.append(f"ADDITIONAL FIELDS")
        content_parts.append("=" * 60)
        content_parts.append("")
        
        for field_name, field_value in other_fields.items():
            content_parts.append(f"{field_name}:")
            if isinstance(field_value, (dict, list)):
                content_parts.append(json.dumps(field_value, indent=2, default=str))
            else:
                content_parts.append(str(field_value))
            content_parts.append("")
    
    return "\n".join(content_parts)

def get_safe_filename(part_name, doc):
    """Generate a safe filename for the transcript."""
    # Get document ID
    doc_id = str(doc.get('_id', 'unknown_id'))
    
    # Determine session number based on sessions array
    session_num = 1  # Default to 1
    if 'sessions' in doc and isinstance(doc['sessions'], list):
        session_num = len(doc['sessions'])  # Use number of sessions
    
    # Clean the doc_id for filename
    doc_id = doc_id.replace('/', '_').replace('\\', '_').replace(':', '_')
    
    # Create filename
    filename = f"{part_name}_session_{session_num}_id_{doc_id}.txt"
    
    # Ensure filename is not too long
    if len(filename) > 200:
        filename = f"{part_name}_session_{session_num}_id_{doc_id[:50]}.txt"
    
    return filename

def export_collection_to_text_files(collection, collection_name, export_dir):
    """Export a MongoDB collection to individual text files."""
    print(f"Exporting collection: {collection_name}")
    
    # Get all documents from the collection
    documents = list(collection.find({}))
    
    if not documents:
        print(f"  No documents found in {collection_name}")
        return
    
    print(f"  Found {len(documents)} documents")
    
    # Create part directory
    part_dir = create_part_directory(export_dir, collection_name)
    
    # Export each document as a separate text file
    exported_files = []
    for i, doc in enumerate(documents, 1):
        try:
            # Generate filename
            filename = get_safe_filename(collection_name, doc)
            filepath = part_dir / filename
            
            # Format content
            content = format_transcript_content(doc)
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            exported_files.append(filename)
            print(f"  Exported document {i}/{len(documents)}: {filename}")
            
        except Exception as e:
            print(f"  Warning: Could not export document {i} due to: {str(e)}")
            # Create error file
            error_filename = f"{collection_name}_error_doc_{i}.txt"
            error_filepath = part_dir / error_filename
            with open(error_filepath, 'w', encoding='utf-8') as f:
                f.write(f"Error exporting document: {str(e)}\n")
                f.write(f"Document keys: {list(doc.keys()) if isinstance(doc, dict) else 'not_a_dict'}\n")
    
    # Create summary file for this part
    summary_file = part_dir / f"{collection_name}_summary.txt"
    with open(summary_file, 'w') as f:
        f.write(f"Collection: {collection_name}\n")
        f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Documents: {len(documents)}\n")
        f.write(f"Successfully Exported: {len(exported_files)}\n")
        f.write(f"Export Directory: {part_dir.absolute()}\n")
        f.write(f"\nExported Files:\n")
        for filename in exported_files:
            f.write(f"  - {filename}\n")
    
    print(f"  Summary saved to: {summary_file}")
    print(f"  Files saved to: {part_dir.absolute()}")

def export_login_codes_to_csv(collection, export_dir):
    """Export login codes to CSV format (since they're not transcripts)."""
    print(f"Exporting collection: login_codes")
    
    documents = list(collection.find({}))
    
    if not documents:
        print(f"  No documents found in login_codes")
        return
    
    print(f"  Found {len(documents)} documents")
    
    # Convert to simple format for CSV
    csv_data = []
    for doc in documents:
        csv_data.append({
            'code': doc.get('code', ''),
            'created_at': doc.get('created_at', ''),
            'used': doc.get('used', False),
            'used_at': doc.get('used_at', '')
        })
    
    # Create CSV file
    import pandas as pd
    df = pd.DataFrame(csv_data)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"login_codes_{timestamp}.csv"
    csv_filepath = export_dir / csv_filename
    
    df.to_csv(csv_filepath, index=False, encoding='utf-8')
    print(f"  Exported to: {csv_filepath}")
    
    # Create summary
    summary_file = export_dir / "login_codes_summary.txt"
    with open(summary_file, 'w') as f:
        f.write(f"Collection: login_codes\n")
        f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Documents: {len(documents)}\n")
        f.write(f"Columns: {', '.join(df.columns)}\n")

def main():
    """Main function to export all collections."""
    print("Starting MongoDB to structured text files export...")
    print("=" * 60)
    
    try:
        # Create export directory
        export_dir = create_export_directory()
        print(f"Export directory: {export_dir.absolute()}")
        
        # Get database connection
        print("Connecting to MongoDB...")
        db = get_db()
        print(f"Connected to database: {db.name}")
        
        # Get all collections
        collections = db.list_collection_names()
        print(f"Found {len(collections)} collections: {collections}")
        
        # Export each collection
        for collection_name in collections:
            collection = db[collection_name]
            
            if collection_name == 'login_codes':
                # Handle login_codes differently (CSV format)
                export_login_codes_to_csv(collection, export_dir)
            else:
                # Handle transcript collections (text files)
                export_collection_to_text_files(collection, collection_name, export_dir)
            
            print("-" * 40)
        
        # Create overall summary
        summary_file = export_dir / "export_summary.txt"
        with open(summary_file, 'w') as f:
            f.write("MongoDB Export Summary\n")
            f.write("=" * 40 + "\n")
            f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Database: {db.name}\n")
            f.write(f"Collections Exported: {len(collections)}\n")
            f.write(f"Collections: {', '.join(collections)}\n")
            f.write(f"Export Directory: {export_dir.absolute()}\n")
            f.write(f"\nStructure:\n")
            for collection_name in collections:
                if collection_name == 'login_codes':
                    f.write(f"  - {collection_name}/: CSV file in root directory\n")
                else:
                    f.write(f"  - {collection_name}/: Folder with individual transcript files\n")
        
        print(f"Export completed successfully!")
        print(f"All files saved to: {export_dir.absolute()}")
        print(f"Summary file: {summary_file}")
        
    except Exception as e:
        print(f"Error during export: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 