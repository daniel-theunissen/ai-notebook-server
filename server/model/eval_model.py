from retrieval_model import get_response, add_note
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

    for index, row in truth_table_db.iterrows():
        add_note(row['Answer'])

    incorrect = 0
    for index, row in truth_table_db.iterrows():  
        answer = get_response(row['Question'])
        if answer != row['Answer']:
            incorrect = incorrect + 1
            print(row['Question'])
            print(answer)
            print(row['Answer'])
    total_queries = truth_table_db.shape[0]
    accuracy = ((total_queries - incorrect) / total_queries) * 100

    return accuracy


accuracy = eval_model('server/model/initial_training_data_notetaker.csv')
print(f'Accuracy: {accuracy}')

