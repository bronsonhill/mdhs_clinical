# Scripts Directory

This directory contains utility scripts for the MDHS Clinical project.

## Setup Script

### `setup_export_environment.py`

This script helps verify that your environment is properly configured for running the MongoDB export script.

#### Usage:

```bash
# From the project root directory
python scripts/setup_export_environment.py
```

#### What it checks:
- Python version compatibility (3.8+)
- Required packages installation
- Project structure integrity
- Streamlit secrets configuration

#### Features:
- Interactive setup assistance
- Automatic creation of sample secrets file
- Detailed error reporting
- Environment validation

## MongoDB Export Script

### `export_mongodb_to_csv.py`

This script exports all collections from the MongoDB database to structured text files and CSV files.

#### Features:
- Exports transcript collections to individual text files organized by part
- Exports login_codes to CSV format
- Creates structured directory layout with folders for each part
- Generates descriptive filenames with session numbers and document IDs
- Handles nested JSON structures and binary data
- Creates summary files with metadata for each part
- Formats transcript content in readable text format

#### Prerequisites:
- MongoDB connection configured in `utils/db_connection.py`
- Required packages installed (see `requirements.txt`)
- Streamlit secrets configured for MongoDB credentials

#### Usage:

```bash
# From the project root directory
python scripts/export_mongodb_to_csv.py
```

#### Output:
The script creates a `data_export/` directory containing:
- `{part_name}/` - Folders for each transcript part
- `{part_name}_session_{session}_id_{doc_id}.txt` - Individual transcript files
- `{part_name}_summary.txt` - Summary files for each part
- `login_codes_{timestamp}.csv` - Login codes in CSV format
- `export_summary.txt` - Overall export summary

#### Example Output Structure:
```
data_export/
├── part1_transcripts/
│   ├── part1_transcripts_session_1_id_ABC123.txt
│   ├── part1_transcripts_session_2_id_DEF456.txt
│   └── part1_transcripts_summary.txt
├── part2_transcripts/
│   ├── part2_transcripts_session_1_id_GHI789.txt
│   └── part2_transcripts_summary.txt
├── part3_transcripts/
│   ├── part3_transcripts_session_1_id_JKL012.txt
│   └── part3_transcripts_summary.txt
├── login_codes_20241201_143022.csv
└── export_summary.txt
```

#### Example Transcript Format:
```
============================================================
TRANSCRIPT METADATA
============================================================
Document ID: ABC123

============================================================
SESSION 1
============================================================

Session ID: b'...'
Date: 2025-04-15 11:27:30.382000

Assistant: Hello. Let's discuss the research context.

User: Hi

Assistant: Please feel free to ask any relevant questions...
```

#### Data Handling:
- **Transcript Files**: Formatted as readable text with metadata headers
- **Conversation Structure**: Messages formatted as "Assistant: [content]" and "User: [content]"
- **Session Data**: Multiple sessions per document, each with its own section
- **Session Numbers**: Based on the number of sessions in the document (index + 1)
- **Binary Data**: Converted to descriptive text (e.g., `[Binary data: 123 bytes]`)
- **Login Codes**: Exported as CSV for easy analysis

#### Error Handling:
- Graceful handling of empty collections
- Connection error reporting
- File write error handling
- Detailed logging throughout the process
- Individual document error handling with error files

## Data Viewer Script

### `view_export_data.py`

This script provides a quick way to inspect the structure and sample data from the exported CSV files.

#### Usage:

```bash
# From the project root directory
python scripts/view_export_data.py
```

#### Features:
- Lists all exported CSV files
- Shows data shape and column information
- Displays data types for each column
- Shows sample data (first 3 rows)
- Provides statistics for numeric columns
- Easy-to-read formatted output 