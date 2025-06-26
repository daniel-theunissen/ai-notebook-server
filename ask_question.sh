#!/bin/bash

# Check if a question argument is provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <question>"
    exit 1
fi

QUESTION="$*"

# Send the POST request with the question
curl -X POST -H "Content-Type: application/json" -d "{\"question\": \"$QUESTION\"}" http://localhost:5000/get_response