from flask import Blueprint, jsonify, request, send_file, after_this_request
import os
import tempfile
from gtts import gTTS
from groq import Groq
import mysql.connector
from mysql.connector import Error
# Initialize Blueprint
llm_bp = Blueprint('llm', __name__)

# Groq API Setup
api_key = 'X'
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
    prompt = f"Generate a short, engaging story about {character} that lasts around 30 seconds when read aloud."
    stream = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a professional children's storyteller. Craft a concise and engaging story about the character that should take around 30 seconds to read aloud."},
            {"role": "user", "content": prompt}
        ],
        model="llama3-70b-8192",
        temperature=0.5,
        max_tokens=64,
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

# Utility function to generate audio file
def generate_audio(text, filename):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)

# Route to generate and serve audio file for a story
@llm_bp.route('/character_story_audio/<character>')
def character_story_audio(character):
    story = get_llm_story(character)

    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
        temp_file_name = temp_file.name
        generate_audio(story, temp_file_name)

    @after_this_request
    def cleanup(response):
        try:
            os.remove(temp_file_name)
        except Exception as e:
            print(f'Failed to delete {temp_file_name}. Reason: {e}')
        return response

    return send_file(temp_file_name)



