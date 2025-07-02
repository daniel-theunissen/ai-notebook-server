# ai-notebook-server

Simple server to interface with our AI Notebook Model

## Installation

1. Clone the repository `git clone https://github.com/daniel-theunissen/ai-notebook-server.git`
2. Install dependencies in a new virtual environment
```
pip install pandas
pip install numpy
pip install flask
pip install pipenv
pip install dotenv
pip install openai
```
3. Install PyTorch for your platform

[Instructions here](https://pytorch.org/get-started/locally/)

4. Install the Sentence Transformers module
```
pip install "transformers[torch]"
pip install -U sentence-transformers
```

## Usage

Start the server using `./start_server.sh`

The server should be hosted locally on port 5000

Store a new note using `./add_note "<note>"`

Query the database using `./ask_question "<question>"`

Get all notes for a user using `./get_user_notes <user>`

Delete all database note entries for a user using `./delete_user_data <user>`

Force sync the database using `./sync_database "<note1>" ... "<noteN>"`

Get the audio transcription of an audio file using `./speech_to_text "/path/to/file"`

## API Endpoint Docs
### 1. Add Note
- **Endpoint:** `/add_note`
- **Method:** `POST`
- **Description:** Adds a new note to the database for a specific device.
- **Request Body:**
  ```json
  {
      "device_id": "string",  // Required: Unique identifier for the device
      "folder": "string",      // Optional: Folder name for the note
      "notebook": "string",    // Optional: Notebook name for the note
      "note": "string"         // Required: The content of the note
  }
  ```

#### Responses:
- `204 No Content`: Note added successfully.
- `400 Bad Request`: Device ID and note are required.
- `409 Conflict`: Duplicate note found.
- `500 Internal Server Error`: Error checking for existing notes.

### 2. Get Response
- **Endpoint:** `/get_response`
- **Method:** `POST`
- **Description:** Retrieves a response based on a question by finding the most similar note.
- **Request Body:**
    ```json
    {
        "device_id": "string",  // Required: Unique identifier for the device
        "question": "string"     // Required: The question to ask
    }
    ```

#### Responses:
- `200 OK`: Returns the most relevant note as a response.
- `400 Bad Request`: Device ID and question are required.

### 3. Get User Notes
- **Endpoint:** `/get_user_notes`
- **Method:** `GET`
- **Description:** Retrieves all notes associated with a specific device.
- **Query Parameters:**
    - `device_id`: Unique identifier for the device (required).
#### Responses:
- `200 OK`: Returns a list of notes.
- `400 Bad Request`: Device ID is required.

### 4. Sync Database
- **Endpoint:** `/sync_database`
- **Method:** `POST`
- **Description:** Syncs notes for a specific device by replacing existing notes with a new list.
- **Request Body:**
    ``` json
    {
        "device_id": "string",  // Required: Unique identifier for the device
        "notes": ["string"]      // Required: List of notes to sync
    }
    ```
#### Responses:
- `200 OK`: Notes synced successfully.
- `400 Bad Request`: Device ID and notes list are required.

### 5. Speech to Text
- **Endpoint:** `/speech_to_text`
- **Method:** `POST`
- **Description:** Converts audio input to text.
- **Request Body:**
    -  Form Data:
        - audio: Path to audio file to be processed (required).

#### Responses:
- `200 OK`: Returns the transcribed text.
- `400 Bad Request`: No audio file provided or no file selected.

6. Delete Notes
- **Endpoint:** `/delete_notes/<device_id>`
- **Method:** `DELETE`
- **Description:** Deletes all notes associated with a specific device.
- **Path Parameters:**
    - `device_id   `: Unique identifier for the device (required).

#### Responses:
- `204 No Content`: All notes deleted successfully.
- `500 Internal Server Error`: Failed to delete notes.
