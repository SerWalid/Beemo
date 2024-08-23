from flask import Blueprint, jsonify, request, send_file, after_this_request
import os
import tempfile
from gtts import gTTS
from groq import Groq

# Initialize Blueprint
llm_bp = Blueprint('llm', __name__)

# Groq API Setup
api_key = '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'
client = Groq(api_key=api_key)

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

# Route to handle LLM response
@llm_bp.route('/get_response', methods=['POST'])
def get_response():
    data = request.json
    prompt = data['prompt']
    response = get_llm_response(prompt)
    return jsonify({'response': response})

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
