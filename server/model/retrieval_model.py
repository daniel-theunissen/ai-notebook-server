from sentence_transformers import SentenceTransformer
import numpy as np

# Choose sentence transformer (biencoder) model
model = SentenceTransformer("all-mpnet-base-v2")

def encode_sentence(sentence):
    """
    Encodes a sentence based on a model definition

    Args:
        sentence (str): String containing the sentence to be encoded

    Returns:
        embedding (list): List containing embedding data
    """
    # Calculate embedding for sentence
    embedding = model.encode([sentence]).tolist()  # Convert to list for Firebase compatibility

    return embedding


def get_similarities(question_embedding, note_embeddings):
    """
    Get the list of similarity scores given the question and note embeddings

    Args:
        question_embedding (list): List containing the question embedding data
        note_embeddings (list): List containing the note embedding data

    Returns:
        similarities (list): List containing the similarity scores 
    """
    note_embeddings = np.array(note_embeddings, dtype=np.float32)
    note_embeddings = note_embeddings.reshape(note_embeddings.shape[0], -1)  # Reshape to (n, 768)

    
    # Calculate similarities
    similarities = model.similarity(question_embedding, note_embeddings)
    
    
    return similarities
