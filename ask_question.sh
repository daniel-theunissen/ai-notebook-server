#!/bin/bash

# Check if a question argument is provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <question>"
    exit 1
fi

QUESTION="$*"

# Send the POST request with the question and capture the response
# RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"question\": \"$QUESTION\"}" http://localhost:5000/get_response)
RESPONSE=$(curl -X POST \
-H "Content-Type: application/json" \
-d '{
    "device_id": "test_user",
    "question": "'"$QUESTION"'"
}' http://localhost:5000/get_response)


# Print the response
echo "$RESPONSE"
