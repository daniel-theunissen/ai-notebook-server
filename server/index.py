import os
from werkzeug.utils import secure_filename
from flask import Flask, jsonify, request
from server.openai_api import speech_to_text
from server.model.retrieval_model import add_note, get_response, sync_database

app = Flask(__name__)

@app.route('/get_response', methods=['POST'])
def get_response_db():
    json_string = request.get_json()
    question = json_string["question"]
    print(f"Recieved Question: {question}")
    response = get_response(question)
    print(f"Got Response: {response}")
    return jsonify(response), 200

@app.route('/sync_database', methods=['POST'])
def get_client_db():
    json_string = request.get_json()
    notes = json_string["notes"]
    print(notes)
    sync_database(notes)
    return '', 200


@app.route('/add_note', methods=['POST'])
def add_note_db():
    json_string = request.get_json()
    note = json_string["note"]
    print(f"Got Note: {note}")

    add_note(note)
    
    return '', 204


@app.route('/speech_to_text', methods=['POST'])
def speech_to_text_db():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    
    if audio_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save temporarily
    filename = secure_filename(audio_file.filename)
    temp_path = os.path.join('/tmp', filename)
    audio_file.save(temp_path)
    
    # Call speech-to-text function
    text_result = speech_to_text(temp_path)
    
    # Clean up temp file
    os.remove(temp_path)
    
    return jsonify({'text': text_result}), 200
