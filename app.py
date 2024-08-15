from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file,after_this_request
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import Error
from gtts import gTTS
import os
from groq import Groq
import pyttsx3
import tempfile
import requests
import openai



app = Flask(__name__)

# Ensure the 'static/audio' directory exists
os.makedirs('static/audio', exist_ok=True)


# ----------------------------------------------- API -----------------------------------------------
api_key = 'X'
client = Groq(api_key=api_key)


# ----------------------------------------------- Database setup -----------------------------------------------
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Replace with your MySQL host
            user='root',  # Replace with your MySQL username
            password='',  # Replace with your MySQL password
            database='Autism'  # Replace with your MySQL database name
        )
        if connection.is_connected():
            print("Connected to MySQL database")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


def init_db():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS clients (
                id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(255) NOT NULL,
                email_address VARCHAR(255) NOT NULL UNIQUE,
                phone_number VARCHAR(255) NOT NULL,
                birth_date DATE NOT NULL,
                gender VARCHAR(50) NOT NULL,
                street_address_1 VARCHAR(255) NOT NULL,
                street_address_2 VARCHAR(255),
                country VARCHAR(100) NOT NULL,
                city VARCHAR(100) NOT NULL
            )''')
            connection.commit()
        except Error as e:
            print(f"The error '{e}' occurred during table creation")
        finally:
            cursor.close()
            connection.close()


init_db()




# ----------------------------------------------- LLM -----------------------------------------------
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

def get_llm_response(prompt):
    # Create a chat completion request
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

    # Collect the response from the stream
    response = ""
    for chunk in stream:
        delta_content = chunk.choices[0].delta.content
        if delta_content is not None:
            response += delta_content
    return response


# Function to generate images using DALL-E


# ----------------------------------------------- URLs -----------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/PageOff')
def PageOff():
    return render_template('PageOff.html')

@app.route('/Games')
def Games():
    return render_template('Games.html')

@app.route('/painting')
def painting():
    return render_template('painting.html')

@app.route('/Number')
def Number():
    return render_template('Number.html')

@app.route('/MemoryGame')
def MemoryGame():
    return render_template('MemoryGame.html')
@app.route('/emotion')
def emotion():
    return render_template('emotion.html')
@app.route('/chatbotinterface')
def chatbotinterface():
    return render_template('chatbotinterface.html')

@app.route('/EmotionDetection')
def EmotionDetection():
    return render_template('EmotionDetection.html')


@app.route('/ActivitiesMenu')
def ActivitiesMenu():
    return render_template('ActivitiesMenu.html')

@app.route('/Tetris')
def Tetris():
    return render_template('Tetris.html')

@app.route('/Cube')
def Cube():
    return render_template('Cube.html')

@app.route('/GameSelectTest')
def GameSelectTest():
    return render_template('GameSelectTest.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = create_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM clients WHERE email_address = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()

            if user and user['phone_number']== password:
                # Login successful
                return redirect(url_for('PageOff'))
            else:
                return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email_address = request.form['email_address']
        password = request.form['password']
        birth_date = request.form['birth_date']
        gender = request.form['gender']
        street_address_1 = request.form['street_address_1']
        street_address_2 = request.form['street_address_2']
        country = request.form['country']
        city = request.form['city']

        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute('''
                    INSERT INTO clients (
                        full_name, email_address, phone_number, birth_date, gender, 
                        street_address_1, street_address_2, country, city
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (full_name, email_address, password, birth_date, gender, street_address_1, street_address_2,
                      country, city))
                connection.commit()
            except Error as e:
                print(f"The error '{e}' occurred during form submission")
            finally:
                cursor.close()
                connection.close()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/StoryTelling')
def StoryTelling():
    return render_template('StoryTelling.html')


@app.route('/chatbottest_page')
def chatbottest_page():
    return render_template('chatbotTest.html')

@app.route('/Music')
def Music():
    return render_template('Music.html')

@app.route('/PlayStation')
def PlayStation():
    return render_template('PlayStation.html')

@app.route('/BoxCube')
def BoxCube():
    return render_template('BoxCube.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/beemo')
def beemo():
    return render_template('beemo.html')

@app.route('/christmas')
def christmas():
    return render_template('christmas.html')


@app.route('/Campfire')
def Campfire():
    return render_template('Campfire.html')


@app.route('/RelaxMenu')
def RelaxMenu():
    return render_template('RelaxMenu.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.json
    prompt = data['prompt']
    response = get_llm_response(prompt)
    return jsonify({'response': response})


def generate_audio(text, filename):
    from gtts import gTTS  # Import here to ensure it's available when needed
    tts = gTTS(text=text, lang='en')  # Set language to English
    tts.save(filename)


@app.route('/character_story_audio/<character>')
def character_story_audio(character):
    story = get_llm_story(character)
    #story = stories.get(character, "Story not found.")

    # Use a temporary file for the audio
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


if __name__ == '__main__':
    app.run(debug=True)
