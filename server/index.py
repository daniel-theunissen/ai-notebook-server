from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials, db
from server.model.retrieval_model import encode_sentence, get_similarities
from server.model.stt_model import speech_to_text

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("server/private_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://notebookai-79e56-default-rtdb.firebaseio.com/'
})

@app.route('/add_note', methods=['POST'])
def add_note_db():
    json_string = request.get_json()
    device_id = json_string.get("device_id")  # Get device ID from the request
    note = json_string.get("note")
    
    if not device_id or not note:
        return jsonify({"error": "Device ID and note are required"}), 400

    print(f"Got Note: {note} for Device ID: {device_id}")
    note_embedding = encode_sentence(note)

    # Save note and its embedding to Firebase
    ref = db.reference(f'notes/{device_id}')
    ref.push({
        'note': note,
        'embedding': note_embedding
    })

    return '', 204

@app.route('/get_response', methods=['POST'])
def get_response_db():
    json_string = request.get_json()
    device_id = json_string.get("device_id")  # Get device ID from the request
    question = json_string.get("question")
    
    if not device_id or not question:
        return jsonify({"error": "Device ID and question are required"}), 400

    print(f"Received Question: {question} for Device ID: {device_id}")

    # Load all notes from Firebase
    ref = db.reference(f'notes/{device_id}')
    notes_data = ref.get()

    if notes_data is None:
        return jsonify([]), 200  # Return an empty list if no notes

    # Extract embeddings and calculate similarities
    question_embedding = encode_sentence(question)

    note_embeddings = []
    notes = []
    for key, value in notes_data.items():
        notes.append(value['note'])
        note_embeddings.append(value['embedding'])

    similarities = get_similarities(question_embedding, note_embeddings)
    
    # Find closest match in the database
    max_val, max_idx = similarities.max(1)
    answer = notes[max_idx]

    print(f"Got Response: {answer}")
    return jsonify({"response": answer}), 200

@app.route('/get_user_notes', methods=['GET'])
def get_user_notes():
    device_id = request.args.get('device_id')  # Get device ID from query parameters
    if not device_id:
        return jsonify({"error": "Device ID is required"}), 400

    ref = db.reference(f'notes/{device_id}')
    notes_data = ref.get()

    if notes_data is None:
        return jsonify([]), 200  # Return an empty list if no notes

    notes = [{'note': value['note'], 'id': key} for key, value in notes_data.items()]
    return jsonify(notes), 200

@app.route('/sync_database', methods=['POST'])
def sync_database_db():
    json_string = request.get_json()
    device_id = json_string.get("device_id")  # Get device ID from the request
    notes = json_string.get("notes")
    
    if not device_id or not isinstance(notes, list):
        return jsonify({"error": "Device ID and notes list are required"}), 400

    print(f"Syncing notes for Device ID: {device_id}")
    
    # Clear existing notes in Firebase
    ref = db.reference(f'notes/{device_id}')
    ref.delete()  # Deletes all existing notes

    for note in notes:
        note_embedding = encode_sentence(note)
        # Save note and its embedding to Firebase
        ref.push({
            'note': note,
            'embedding': note_embedding
        })
    return '', 200

@app.route('/speech_to_text', methods=['POST'])
def speech_to_text_db():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    
    if audio_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    text_result = speech_to_text(audio_file)
    
    return jsonify({'text': text_result}), 200