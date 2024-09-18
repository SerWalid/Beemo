from flask import Blueprint, jsonify, request, send_file, after_this_request, url_for, current_app as app, \
    render_template
import os
import tempfile
from gtts import gTTS
from groq import Groq
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import threading
import tempfile

import pygame
import time
import base64


# Load environment variables from .env file
load_dotenv()


# Initialize Blueprint
llm_bp = Blueprint('llm', __name__)

# Groq API Setup
# Access environment variables
api_key = os.getenv('API_KEY')
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
db_port = os.getenv('DB_PORT')

client = Groq(api_key=api_key)

Variable = False;
# Global connection object
connection = None

def create_db_connection():
    global connection
    if connection is None or not connection.is_connected():
        try:
            connection = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name,
                port=int(db_port)
            )
            if connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"The error '{e}' occurred while creating the database connection")

def get_db_connection():
    global connection
    if connection is None or not connection.is_connected():
        create_db_connection()
    return connection


def create_new_chat_session():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO Chat_History (timestamp)
                VALUES (NOW())
            ''')
            connection.commit()
            chat_history_id = cursor.lastrowid
            return chat_history_id
        except Error as e:
            print(f"The error '{e}' occurred during chat session creation")
        finally:
            cursor.close()
    return None


import tempfile
import pygame
import time
import threading
from gtts import gTTS
from flask import Blueprint, request, jsonify

llm_bp = Blueprint('llm', __name__)


def play_audio(file_path):
    # Initialize pygame mixer
    pygame.mixer.init()

    # Load and play the MP3 file
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # Wait for the playback to finish
    while pygame.mixer.music.get_busy():
        time.sleep(1)

    # Stop the mixer to release the file
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    # Wait a moment to ensure the file is released
    time.sleep(0.5)

    # Delete the MP3 file after playback
    if os.path.exists(file_path):
        os.remove(file_path)


@llm_bp.route('/get_response', methods=['POST'])
def get_response():
    data = request.json
    prompt = data['prompt']
    response = get_llm_response(prompt)

    # Convert response to speech
    tts = gTTS(text=response, lang='en')

    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
        temp_file_path = temp_file.name
        tts.save(temp_file_path)

    # Start a new thread to play the audio
    threading.Thread(target=play_audio, args=(temp_file_path,)).start()

    return jsonify({'response': response})

# Function to generate a story using Groq API
def get_llm_story(character):
    prompt = f"Generate a short, engaging story about {character} that lasts around 1 minute when read aloud .captivating, and imaginative story about the character [insert character's name] that is both engaging and easy for young children (ages 4-7) to follow. The story should be whimsical, age-appropriate, and take approximately 30 seconds to read aloud. Focus on simple language, a positive message, and a playful tone that will entertain and inspire young minds. The story should have a clear beginning, middle, and end, with a little adventure or lesson suitable for kids. ONly give me the story without comments and response and don't say here is the story "
    stream = client.chat.completions.create(
        messages=[
            {"role": "system",
             "content": "You are a professional children's storyteller. Craft a concise and engaging story about the character that should take around 1 minute to read aloud."},
            {"role": "user", "content": prompt}
        ],
        model="llama3-70b-8192",
        temperature=0.5,
        max_tokens=500,
        top_p=1,
        stop=None,
        stream=True,
    )

    response = ""
    for chunk in stream:
        delta_content = chunk.choices[0].delta.content
        if delta_content is not None:
            response += delta_content
    return response


# Function to generate a response using Groq API
def get_llm_response(prompt):
    stream = client.chat.completions.create(
        messages=[
            {"role": "system",
             "content": "You are BMO, a compassionate and supportive mental health assistant. Your role is to provide empathetic and constructive support to users. Please avoid using informal or non-professional language such as 'BEEP BEEP' or 'OH NOOO'."},
            {"role": "user", "content": prompt}
        ],
        model="llama3-70b-8192",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=True,
    )

    response = ""
    for chunk in stream:
        delta_content = chunk.choices[0].delta.content
        if delta_content is not None:
            response += delta_content
    return response



@llm_bp.route('/transcribe_audio', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']

    if audio_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.m4a') as temp_file:
        temp_file_path = temp_file.name
        audio_file.save(temp_file_path)

    try:
        with open(temp_file_path, 'rb') as file:
            transcription = client.audio.transcriptions.create(
                file=(temp_file_path, file.read()),
                model="distil-whisper-large-v3-en",
                prompt="Specify context or spelling",
                response_format="json",
                language="en",
                temperature=0.0
            )

        return jsonify({'transcription': transcription.text})
    except Exception as e:
        print(f"Error in transcription: {e}")
        return jsonify({'error': 'Error processing audio file'}), 500
    finally:
        # Ensure the file is removed
        try:
            os.remove(temp_file_path)
        except Exception as e:
            print(f"Error removing file: {e}")


def generate_audio(text, filename):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)


# Format the story to wrap each word in span tags
def format_story_with_spans(story):
    words = story.split()
    formatted_story = ""
    for i, word in enumerate(words):
        formatted_story += f"<span id='word{i}'>{word} </span>"
    return formatted_story


# Route to generate story and audio based on character
@llm_bp.route('/character_story_audio/<character>', methods=['GET'])
def character_story_audio(character):
    try:
        # Generate story using LLM (this function needs to be implemented)
        story = get_llm_story(character)

        # Format the story with spans for word highlighting
        formatted_story = format_story_with_spans(story)

        # Use a temporary file for the audio
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            temp_file_name = temp_file.name
            generate_audio(story, temp_file_name)

        # Return both the formatted story and the audio URL
        audio_url = url_for('llm.download_audio', filename=os.path.basename(temp_file_name), _external=True)

        return jsonify({'story': formatted_story, 'audio_url': audio_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Route to handle story generation from user input (POST)
@llm_bp.route('/generate_story', methods=['POST'])
def generate_story():
    try:
        data = request.get_json()
        story_input = data.get('story_input')

        # Validate the input
        if not story_input:
            return jsonify({'error': 'Invalid input'}), 400

        # Generate the story using LLM based on user input (this function needs to be implemented)
        story = get_llm_story(story_input)

        # Format the story with spans for word highlighting
        formatted_story = format_story_with_spans(story)

        # Use a temporary file for the audio
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            temp_file_name = temp_file.name
            generate_audio(story, temp_file_name)

        # Return both the formatted story and the audio URL
        audio_url = url_for('llm.download_audio', filename=os.path.basename(temp_file_name), _external=True)

        return jsonify({'story': formatted_story, 'audio_url': audio_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Serve the audio file
@llm_bp.route('/download_audio/<filename>', methods=['GET'])
def download_audio(filename):
    # Construct the file path from the temporary directory
    file_path = os.path.join(tempfile.gettempdir(), filename)

    try:
        # Ensure the file exists before sending it
        if os.path.exists(file_path):

            # Schedule the file to be deleted after the response is sent
            @after_this_request
            def remove_file(response):
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except Exception as e:
                    # Log the error or handle it
                    app.logger.error(f"Error deleting file: {e}")
                return response

            # Serve the file
            return send_file(file_path, mimetype='audio/mpeg')
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


story_bp = Blueprint('story', __name__)


# Route to serve the Batman story
@llm_bp.route('/batman_story', methods=['GET'])
def batman_story():
    # Simple story text
    story_text = "Once upon a time in Gotham, there was a hero named Batman."

    # Render the story page and pass the simple story text
    return render_template('batman_story.html', story=story_text)



# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

@llm_bp.route('/analyze', methods=['POST'])
def analyze_image():
    # Get the image from the request
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image = request.files['image']

    # Save the image temporarily
    image_path = os.path.join('uploads', image.filename)
    image.save(image_path)

    # Encode the image
    base64_image = encode_image(image_path)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What's in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        model="llava-v1.5-7b-4096-preview",
    )

    # Get the response
    response_text = chat_completion.choices[0].message.content

    # Remove the temporarily saved image
    os.remove(image_path)

    # Return the result as JSON
    return jsonify({'response': response_text})



@llm_bp.route('/analyzeWriting', methods=['POST'])
def analyze_writing_image():
    # Get the image from the request
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image = request.files['image']

    # Save the image temporarily
    image_path = os.path.join('uploads', image.filename)
    image.save(image_path)

    # Encode the image
    base64_image = encode_image(image_path)

    # AI model processing (LLava-1.5)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Evaluate the grammar and rate this essay:"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        model="llava-v1.5-7b-4096-preview",
    )

    # Get the response
    response_text = chat_completion.choices[0].message.content

    # Remove the temporarily saved image
    os.remove(image_path)

    # Return the result as JSON
    return jsonify({'response': response_text})
