#!/bin/bash

# Delete the file database.pt if it exists
if [ -f "database.pt" ]; then
    rm "database.pt"
    echo "Deleted database.pt"
else
    echo "database.pt does not exist"
fi

# Keep only the first line of database.csv
if [ -f "database.csv" ]; then
    # Create a temporary file to store the first line
    head -n 1 "database.csv" > "temp.csv"
    
    # Move the temporary file back to database.csv
    mv "temp.csv" "database.csv"
    echo "Deleted all but the first line of database.csv"
else
    echo "database.csv does not exist"
fi