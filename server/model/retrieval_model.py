from sentence_transformers import SentenceTransformer
import torch
import pandas as pd
import numpy as np
import os
import csv

model = SentenceTransformer("multi-qa-mpnet-base-dot-v1")

def add_note(note):
    note_embedding = model.encode([note])
    print(note_embedding.shape)
    # print(note_embedding)

    with open(r'database.csv','a') as fd:
                  writer = csv.writer(fd)
                  writer.writerow([note])

    if not os.path.exists("database.pt"):
        torch.save(note_embedding, "database.pt")
        return
        
    else:
        database = torch.load("database.pt", weights_only=False)
        # print(database.shape)

        database = np.concatenate((database, note_embedding), axis=0)
        print(database.shape)
        torch.save(database, "database.pt")
        return
    
def get_response(question):
    question_embedding = model.encode([question])
    database = torch.load("database.pt", weights_only=False)
    similarities = model.similarity(question_embedding, database)
    max_val, max_idx = similarities.max(1)
    print(max_val)
    print(max_idx)
    answer_db = pd.read_csv("database.csv")
    answer = answer_db["Note"][max_idx.item()]
    return answer