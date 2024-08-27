from flask import Blueprint, jsonify, request, send_file, after_this_request,url_for,current_app as app,render_template
import os
import tempfile
from gtts import gTTS
from groq import Groq
import mysql.connector
from mysql.connector import Error
# Initialize Blueprint
llm_bp = Blueprint('llm', __name__)

# Groq API Setup
api_key = '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'
client = Groq(api_key=api_key)



Variable = False;
# Global connection object
connection = None

def create_db_connection():
    global connection
    if connection is None or not connection.is_connected():
        try:
            connection = mysql.connector.connect(
                host='sql7.freesqldatabase.com',
                user='sql7727502',
                password='PwwVKdQe8w',
                database='sql7727502'
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

@llm_bp.route('/get_response', methods=['POST'])
def get_response():
        global Variable,id_last
        data = request.json
        prompt = data['prompt']
        response = get_llm_response(prompt)

        if not Variable:
            id_last = create_new_chat_session()
            if id_last is None:
                return jsonify({'error': 'Failed to create new chat session'}), 500
            Variable = True


        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                # Insert user input and chatbot response into Discussion
                cursor.execute('''
                    INSERT INTO Discussion (ID_ForeignKeyChat_History, user_input, chatbo_output)
                    VALUES (%s, %s, %s)
                ''', (id_last, prompt, response))
                connection.commit()

            except Error as e:
                print(f"The error '{e}' occurred during data insertion")
            finally:
                cursor.close()

        return jsonify({'response': response})



# Function to generate a story using Groq API

def get_llm_story(character):
    prompt = f"Generate a short, engaging story about {character} that lasts around 1 minute when read aloud .captivating, and imaginative story about the character [insert character's name] that is both engaging and easy for young children (ages 4-7) to follow. The story should be whimsical, age-appropriate, and take approximately 30 seconds to read aloud. Focus on simple language, a positive message, and a playful tone that will entertain and inspire young minds. The story should have a clear beginning, middle, and end, with a little adventure or lesson suitable for kids. ONly give me the story without comments and response and don't say here is the story "
    stream = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a professional children's storyteller. Craft a concise and engaging story about the character that should take around 1 minute to read aloud."},
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
            {"role": "system", "content": "You are BMO, a compassionate and supportive mental health assistant. Your role is to provide empathetic and constructive support to users. Please avoid using informal or non-professional language such as 'BEEP BEEP' or 'OH NOOO'."},
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





