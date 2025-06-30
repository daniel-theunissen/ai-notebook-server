import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def speech_to_text(audio_file):
    # Save temporarily
    filename = secure_filename(audio_file.filename)
    temp_path = os.path.join('/tmp', filename)
    audio_file.save(temp_path)
    
    # Call speech-to-text function
    text_result = make_OpenAI_call(temp_path)
    
    # Clean up temp file
    os.remove(temp_path)

    return text_result

def make_OpenAI_call(file_path):
    audio_file= open(file_path, "rb")

    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )

    return transcription.text