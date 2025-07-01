from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials, db
import logging
from server.model.retrieval_model import encode_sentence, get_similarities
from server.model.stt_model import speech_to_text

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("server/private_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://notebookai-79e56-default-rtdb.firebaseio.com/'
})

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

@app.route('/add_note', methods=['POST'])
def add_note_db():
    json_string = request.get_json()
    device_id = json_string.get("device_id")  # Get device ID from the request
    folder = json_string.get("folder")
    notebook = json_string.get("notebook")
    note = json_string.get("note")
    
    if not device_id or not note:
        logger.error("Add Note: Device ID and note are required")
        return jsonify({"error": "Device ID and note are required"}), 400
    
    if not folder:
        logger.warning("Add Note: Folder not found, assigning default")
        folder = "default"
    
    if not notebook:
        logger.warning("Add Note: Notebook not found, assigning defualt")
        notebook = "default"
    
    note_embedding = encode_sentence(note)

    # Save note and its embedding to Firebase
    ref = db.reference(f'notes/{device_id}')
    ref.push({
        'note': note,
        'embedding': note_embedding,
        'folder': folder,
        'notebook': notebook
    })

    logger.info(f"Added Note: {note} for Device ID: {device_id}")

    return '', 204

@app.route('/get_response', methods=['POST'])
def get_response_db():
    json_string = request.get_json()
    device_id = json_string.get("device_id")  # Get device ID from the request
    question = json_string.get("question")
    
    if not device_id or not question:
        logger.error("Ask Question: Device ID and note are required")
        return jsonify({"error": "Device ID and question are required"}), 400
    
    # Load all notes from Firebase
    ref = db.reference(f'notes/{device_id}')
    notes_data = ref.get()

    if notes_data is None:
        logger.warning("Ask Question: No note data found, returning empty list")
        return jsonify([]), 200  # Return an empty list if no notes

    # Extract embeddings and calculate similarities
    question_embedding = encode_sentence(question)

    logger.info(f"Received Question: {question} for Device ID: {device_id}")

    note_embeddings = []
    notes = []
    for key, value in notes_data.items():
        notes.append(value['note'])
        note_embeddings.append(value['embedding'])

    similarities = get_similarities(question_embedding, note_embeddings)
    
    # Find closest match in the database
    max_val, max_idx = similarities.max(1)
    answer = notes[max_idx]


    logger.info(f"Got Response: {answer}")
    return jsonify({"response": answer}), 200

@app.route('/get_user_notes', methods=['GET'])
def get_user_notes():
    device_id = request.args.get('device_id')  # Get device ID from query parameters
    if not device_id:
        logger.error("Get User Notes: Device ID is required")
        return jsonify({"error": "Device ID is required"}), 400

    ref = db.reference(f'notes/{device_id}')
    notes_data = ref.get()

    if notes_data is None:
        logger.warning("Get User Notes: No note data found, returning empty list")
        return jsonify([]), 200  # Return an empty list if no notes

    notes = [{
        'id': key,
        'note': value['note'],
        'folder': value['folder'],
        'notebook': value['notebook']
    } for key, value in notes_data.items()]

    logger.info(f"Get User Notes: Got notes for Device ID: {device_id}")
    
    return jsonify(notes), 200

@app.route('/sync_database', methods=['POST'])
def sync_database_db():
    json_string = request.get_json()
    device_id = json_string.get("device_id")  # Get device ID from the request
    notes = json_string.get("notes")
    
    if not device_id or not isinstance(notes, list):
        logger.error("Sync Database: Device ID and notes list are required")
        return jsonify({"error": "Device ID and notes list are required"}), 400

    logger.info(f"Sync Database: Syncing notes for Device ID: {device_id}")
    
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
        logger.error("STT: No audio file provided")
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    
    if audio_file.filename == '':
        logger.error("STT: No file selected")
        return jsonify({'error': 'No file selected'}), 400
    
    text_result = speech_to_text(audio_file)
    
    return jsonify({'text': text_result}), 200