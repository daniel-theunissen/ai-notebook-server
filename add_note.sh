#!/bin/bash

# Check if a note argument is provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <note>"
    exit 1
fi

# Combine all arguments into a single note string
NOTE="$*"

# Send the POST request with the note
# curl -X POST -H "Content-Type: application/json" -d "{\"note\": \"$NOTE\"}" http://localhost:5000/add_note
curl -X POST \
-H "Content-Type: application/json" \
-d '{
    "device_id": "test_user",
    "note": "'"$NOTE"'"
}' http://localhost:5000/add_note
