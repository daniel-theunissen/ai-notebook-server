from sentence_transformers import SentenceTransformer
import torch
import numpy as np
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase
cred = credentials.Certificate("server/private_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://notebookai-79e56-default-rtdb.firebaseio.com/'
})

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
    # Calculate embedding for note
    note_embedding = model.encode([note]).tolist()  # Convert to list for Firebase compatibility

    # Save note and its embedding to Firebase
    ref = db.reference('notes')
    ref.push({
        'note': note,
        'embedding': note_embedding
    })

def sync_database(notes):
    """
    Syncs database with the client's notes

    Args:
        notes (list): A list of notes
    
    Returns:
        none
    """
    # Clear existing notes in Firebase
    ref = db.reference('notes')
    ref.delete()  # Deletes all existing notes

    for note in notes:
        add_note(note)

def get_response(question):
    """
    Get the closest match in the database to a question

    Args:
        question (str): String containing the question

    Returns:
        answer (str): String containing the answer 
    """
    # Calculate question embedding
    question_embedding = model.encode([question])

    # Load all notes from Firebase
    ref = db.reference('notes')
    notes_data = ref.get()

    if notes_data is None:
        return "No notes available."

    # Extract embeddings and calculate similarities
    note_embeddings = []
    notes = []
    for key, value in notes_data.items():
        notes.append(value['note'])
        note_embeddings.append(value['embedding'])

    note_embeddings = np.array(note_embeddings, dtype=np.float32)
    note_embeddings = note_embeddings.reshape(note_embeddings.shape[0], -1)  # Reshape to (n, 768)

    print(note_embeddings.shape)
    print(question_embedding.shape)

    # Calculate similarities
    similarities = model.similarity(question_embedding, note_embeddings)
    
    # Find closest match in the database
    max_val, max_idx = similarities.max(1)
    answer = notes[max_idx]
    return answer
