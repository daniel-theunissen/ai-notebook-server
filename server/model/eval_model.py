from retrieval_model import encode_sentence, get_similarities
import torch
import pandas as pd


def eval_model(truth_table):
    """
    Calculate model accuracy given a truth table

    Args:
        truth_table: filepath to truth table csv in Answer,Question format

    Returns:
        accuracy (float): percent accuracy of the model on the truth table
    """

    truth_table_db = pd.read_csv(truth_table)
    truth_table_db = truth_table_db.reset_index() # Make sure indexing works

    note_embeddings = []
    notes = []
    for index, row in truth_table_db.iterrows():
        note_embedding = encode_sentence(row['Answer'])
        note_embeddings.append(note_embedding)
        notes.append(row['Answer'])

    incorrect = 0
    for index, row in truth_table_db.iterrows(): 
        question_embedding = encode_sentence(row['Question']) 
        similarities = get_similarities(question_embedding, note_embeddings)

        # Get the top 3 most similar answers
        top_k = 3
        top_values, top_indices = torch.topk(similarities, top_k)

        top_answers = [notes[i] for i in top_indices[0].tolist()]  # Retrieve top 3 answers

        # Check if the ground truth answer is among the top 3 answers
        if row['Answer'] not in top_answers:
            incorrect += 1
            print("Query: ", row['Question'], "\n")
            print("Model responses: ", top_answers, "\n")
            print("Ground truth: ", row['Answer'], "\n\n")

    total_queries = truth_table_db.shape[0]
    accuracy = ((total_queries - incorrect) / total_queries) * 100

    return accuracy


accuracy = eval_model('server/model/initial_training_data_notetaker.csv')
print(f'Accuracy: {accuracy}')

