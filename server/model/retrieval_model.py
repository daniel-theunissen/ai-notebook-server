from sentence_transformers import SentenceTransformer
import torch
import pandas as pd
import numpy as np
import os
import csv

# Choose sentence transformer (biencoder) model
model = SentenceTransformer("multi-qa-mpnet-base-dot-v1")

def add_note(note):
    """
    Adds a new note to the database

    Args:
        note (str): String containing the note

    Returns:
        none
    """

    # Save text to database
    with open(r'database.csv','a') as fd:
                  writer = csv.writer(fd)
                  writer.writerow([note])

    # Calculate embedding for note
    note_embedding = model.encode([note])

    # Create database if it doesn't exist
    if not os.path.exists("database.pt"):
        torch.save(note_embedding, "database.pt")
        return
        
    else:
        # Add new note to database and save
        database = torch.load("database.pt", weights_only=False)
        database = np.concatenate((database, note_embedding), axis=0)
        torch.save(database, "database.pt")
        return
    
def get_response(question):
    """
    Get the closest match in the database to a question

    Args:
        question (str): String containing the question

    Returns:
        answer (str): String containing the answer 
    """

    # Calculate quesiton embedding
    question_embedding = model.encode([question])

    # Load database and compare using dot product similarity
    database = torch.load("database.pt", weights_only=False)
    similarities = model.similarity(question_embedding, database)

    # Find closest match in the database
    max_val, max_idx = similarities.max(1)
    answer_db = pd.read_csv("database.csv")
    answer = answer_db["Note"][max_idx.item()]
    return answer