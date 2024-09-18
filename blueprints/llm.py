from flask import Blueprint, jsonify, request, send_file, session, after_this_request, url_for, current_app as app, \
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
from .models import User, Settings, db, Interaction, Chat, Notification
from .utils import calculate_age, time_difference_from_today, split_message  # Import the decorator
from datetime import date

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
    # Retrieve the user ID from the session
    user_id = session.get('user_id')
    # Get today's date
    today = date.today()
    # Format today's date as a string (e.g., 'September 18, 2024')
    today_str = today.strftime("%B %d, %Y")

    # Check if there's already a chat for today for the current user
    chat = Chat.query.filter(db.func.date(Chat.created_at) == today, Chat.user_id == user_id).first()

    # If no chat exists for today, create a new one
    if not chat:
        chat = Chat(title=f"Chat for {today_str}", user_id=user_id)
        db.session.add(chat)
        db.session.commit()
    data = request.json
    prompt = data['prompt']
    response = get_llm_response(prompt)
    text, metadata = split_message(response)
    interaction = Interaction(
        message=prompt,
        response=text,
        user_id=user_id,
        chat_id=chat.id
    )
    db.session.add(interaction)
    db.session.commit()

    if(metadata):
        topic = metadata.get('topic')
        summary = metadata.get('summary')
        message_type = metadata.get('type')
        notification = Notification(
            message= summary,
            topic=topic,
            notification_type=message_type,
            user_id=user_id,
            chat_id=chat.id,
            interaction_id=interaction.id
        )
        db.session.add(notification)
        db.session.commit()
    # Convert response to speech
    tts = gTTS(text=text, lang='en')

    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
        temp_file_path = temp_file.name
        tts.save(temp_file_path)

    # Start a new thread to play the audio
    threading.Thread(target=play_audio, args=(temp_file_path,)).start()

    return jsonify({'response': text})

# Function to generate a story using Groq API
def get_llm_story(character):
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    child_birthday=user.child_birth_date
    child_age = time_difference_from_today(child_birthday)
    prompt = (
    f"Generate a short, engaging story about {character} that lasts around 1 minute when read aloud. "
    f"A captivating and imaginative story about the character that is both engaging and easy for young children (around {child_age}) to follow. "
    f"This story is for a child with ASD (Autism Spectrum Disorder), so it should be particularly clear, structured, and easy to understand, while still being fun. "
    "The story should be whimsical, age-appropriate, and take approximately 30 seconds to read aloud. "
    "Focus on simple language, a positive message, and a playful tone that will entertain and inspire young minds. "
    "The story should have a clear beginning, middle, and end, with a little adventure or lesson suitable for kids. "
    "Only give me the story without comments or responses, and don't say 'here is the story'."
)
    system_message = (
    f"You are a professional children's storyteller. You are creating a story for a child who's age is around {child_age} and has Autism Spectrum Disorder (ASD). "
    "The child may benefit from stories that are clear, well-structured, and predictable, while still being fun and imaginative. "
    "Craft a concise, engaging story about the character that should take around 1 minute to read aloud. "
    "Ensure the story is easy to follow, with simple language and a gentle pace to accommodate the child's needs."
)
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
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    child_name=user.child_name
    child_birthday=user.child_birth_date
    child_age = time_difference_from_today(child_birthday)
    country = user.country
    settings = Settings.query.filter_by(user_id=user_id).first()

    system_message = (
        f"You are Beemo, a compassionate and supportive mental health assistant. "
        f"You are speaking to a child named {child_name}, who is {child_age} years old, and may have Autism Spectrum Disorder (ASD). "
        f"Please try to address {child_name} by their name often to create a personal connection. "
        "Your role is to provide empathetic and constructive support, ensuring your responses are clear, structured, and calming. "
        "If the child expresses feelings of sadness, hopelessness, or talks about sensitive topics such as suicide, offer care and reassurance in a gentle and supportive manner. "
        "Acknowledge their feelings, remind them that they are not alone, and suggest reaching out to a trusted adult. "
        f"In case of crisis, provide the suicide hotline number for their country, {country}, and encourage them to seek immediate help if necessary."
        "Please avoid using informal or non-professional language such as 'BEEP BEEP' or 'OH NOOO'."
    )

    if settings and settings.banned_topics:
        blocked_topics_list = settings.banned_topics.split(",")  # Assuming banned_topics is a comma-separated string
        banned_topics_formatted = ", ".join(blocked_topics_list)
        system_message += (
            f" Additionally, if the child mentions any of the following banned topics: {banned_topics_formatted}, "
            "do not engage in discussing these topics. Instead, gently redirect the conversation. "
            "You might use phrases such as, 'Let's talk about something else that's really fun!' or 'How about we discuss something different that you enjoy?' "
            "If {child_name} asks specifically about the banned topics or why they can't talk about them, do not respond directly to the question. "
            "Instead, continue the redirection without addressing the topic. "
            "Make sure not to include the banned topic in your response. "
            "For any mention of banned topics, append the following format at the end of your message: "
            "'metadata: [{'topic': 'banned_topic', 'summary': 'brief_summary', 'type': 'banned'}]'. "
            "Replace 'banned_topic' with the actual topic mentioned and provide a brief summary of the discussion prior to redirection."
        )

    if settings and settings.alert_topics:
        alert_topics_list = settings.alert_topics.split(",")  # Assuming alert_topics is a comma-separated string
        alert_topics_formatted = ", ".join(alert_topics_list)
        system_message += (
            f" Additionally, if the child mentions any of the following alert topics: {alert_topics_formatted}, "
            "engage with the child normally, providing reassurance if necessary. "
            "For any mention of alert topics, you have to append the following format at the end of your message: "
            "'metadata: [{'topic': 'alert_topic', 'summary': 'brief_summary', 'type': 'alert'}]'. "
            "Replace 'alert_topic' with the actual mentioned topic and 'brief_summary' with a summary of the discussion."
        )

    stream = client.chat.completions.create(
        messages=[
            {"role": "system",
             "content": system_message},
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




