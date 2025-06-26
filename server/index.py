from flask import Flask, jsonify, request
from server.model.retrieval_model import add_note, get_response

app = Flask(__name__)

@app.route('/get_response', methods=['POST'])
def get_response_db():
    json_string = request.get_json()
    question = json_string["question"]
    response = get_response(question)
    print(response)
    return jsonify(response), 200


@app.route('/add_note', methods=['POST'])
def add_note_db():
    json_string = request.get_json()
    note = json_string["note"]
    print(note)

    add_note(note)
    
    return '', 204