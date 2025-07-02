#!/bin/bash

# Check if at least one note argument is provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <note1> <note2> ... <noteN>"
    exit 1
fi

# Initialize an empty array for notes
NOTES_ARRAY=()

# Loop through all arguments and add them to the array
for NOTE in "$@"; do
    NOTES_ARRAY+=("\"$NOTE\"")  # Add quotes around each note
done

# Join the array into a single string with commas
NOTES_JSON=$(IFS=,; echo "[${NOTES_ARRAY[*]}]")

# Send the POST request with the notes
curl -X POST -H "Content-Type: application/json" -d "{"device_id": "test_user", \"notes\": $NOTES_JSON}" http://localhost:5000/sync_database

