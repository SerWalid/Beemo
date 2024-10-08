import json
import requests
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
from .models import User, Settings, db, Interaction, Chat, Notification, Report
from .utils import calculate_age, time_difference_from_today, split_message  # Import the decorator
from datetime import date
from .interactions import get_all_interactions_today
from .report import retrieve_today_report
import pygame
import time
import base64
import openai



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
a2sv_api_key = os.getenv('A2SV_API_KEY')



client = Groq(api_key=api_key)



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
        model="llama-3.1-70b-versatile",
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

    if(settings and settings.parent_instructions):
        system_message += (
        f" Important: The following instructions come directly from {child_name}'s parents. These instructions are crucial and must be followed strictly and without exception: {settings.parent_instructions}. "
        "Your adherence to these parental instructions is essential, and you should prioritize them above all else in your interactions with the child."
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
        model="llama-3.2-90b-text-preview",
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


@llm_bp.route('/generate_story', methods=['POST'])
def generate_story():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    try:
        # Get the story input from the user
        data = request.get_json()
        story_input = data.get('story_input')

        # Validate input
        if not story_input:
            return jsonify({'error': 'Invalid input'}), 400

        # Define the image prompt using the story input
        image_prompt = (f"Create a vibrant and whimsical children's book illustration about '{story_input}', "
                        "designed with a hand-drawn or watercolor aesthetic. The image should be high resolution, "
                        "with expressive characters and intricate background details. Use a colorful palette and "
                        "soft, warm lighting that feels inviting and suitable for kids. Ensure the composition feels "
                        "like a scene from a storybook, with playful, imaginative elements.")

        # Generate the story using LLM based on user input
        story = get_llm_story(story_input)  # Ensure this function is defined

        # Format the story with spans for word highlighting
        formatted_story = format_story_with_spans(story)  # Ensure this function is defined

        # Generate the audio for the story
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            temp_file_name = temp_file.name
            generate_audio(story, temp_file_name)  # Ensure this function is defined

        # Generate the image based on the image prompt
        image_response = openai.Image.create(
            model="dall-e-3",
            prompt=image_prompt,
            n=1,
            size="1024x1024"
        )
        image_url = image_response['data'][0]['url']  # Extract image URL

        # Get the audio URL for the story
        audio_url = url_for('llm.download_audio', filename=os.path.basename(temp_file_name), _external=True)
        if user:
            user.reading_time += 1
            db.session.commit()

        # Return the formatted story, audio URL, and image URL in the response
        return jsonify({'story': formatted_story, 'audio_url': audio_url, 'image_url': image_url}), 200

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
@llm_bp.route('/generate_report', methods=['GET'])
def generate_report_api():
    user_id = session.get('user_id')
    today_report = retrieve_today_report(user_id)
    if(today_report):
        return jsonify(
            {'content': today_report.content}
        )
    today_interactions = get_all_interactions_today(user_id)
    if(not today_interactions):
        return jsonify(
            {'content': 'No interactions found for today.'}
        )

    today_interactions_list = [
        {
            "message": interaction.message,
            "response": interaction.response,
            "created_at": interaction.created_at.isoformat()  # Convert datetime to ISO 8601 string
        }
        for interaction in today_interactions
    ]
    interactions_str = json.dumps(today_interactions_list, indent=2)


    content = generate_report(interactions_str)
    response_text = content['response']['messages'][0]['content']
    if( response_text):
        report = Report(
            content=response_text,
            user_id=user_id,
        )
    db.session.add(report)
    db.session.commit()
    
    return jsonify(
        {'content': response_text}
    )

def generate_report(prompt):
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    child_name=user.child_name
    child_birthday=user.child_birth_date
    child_age = time_difference_from_today(child_birthday)
    country = user.country
    parent_name = user.full_name
    system_content = f"""
    You are Beemo, a compassionate and supportive mental health assistant designed to interact with {child_name}, a child who is {child_age} years old from {country} with ASD. Your task is to generate a structured report in JSON format, containing the following sections:

    1. **Overview of the Day**: Summarize {child_name}'s interactions today, focusing on significant emotional trends.
    2. **Emotional State**: Provide a detailed description of {child_name}'s emotional state, highlighting any observed patterns or shifts.
    3. **Behaviors**: Note any proactive or concerning behaviors observed during interactions.
    4. **Communication Skills**: Describe {child_name}'s communication strengths or challenges.
    5. **Notable Moments**: List any particularly special moments or decisions {child_name} made today.
    6. **Recommendations**: Provide supportive recommendations for {parent_name} on encouraging {child_name}'s progress or addressing areas of concern.

    Return the output as a structured JSON object with the format:
    {{
        "overview": "Summary paragraph...",
        "emotional_state": "Detailed paragraph...",
        "behaviors": "Detailed paragraph...",
        "communication_skills": "Detailed paragraph...",
        "notable_moments": ["Moment 1...", "Moment 2..."],
        "recommendations": "Supportive paragraph..."
    }}

    If there are no interactions recorded, inform {parent_name} by responding: "There are no interactions recorded yet."
    """


    headers = {
        'Content-Type': 'application/json',
        'api_token': a2sv_api_key,
    }
    payload = {
        'model': 'gpt-4',
        'messages': [{"role": "system", "content": system_content}, {"role": "user", "content": prompt}],
        'max_token': 1024,
        'temperature': 0.7,
        'response_format': 'text/plain',
        'user_id': 'the champs'     
    }
    response = requests.post('https://api.afro.fit/api_v2/api_wrapper/chat/completions', json=payload, headers=headers)
    return response.json()

    return jsonify({'response': response_text})
