from flask import Blueprint, render_template, request, jsonify
from openai import OpenAI  # Import the updated OpenAI client
import os

# Create the blueprint for the story
story_bp = Blueprint('story', __name__, template_folder='templates')

# Set your OpenAI API key from the environment variable
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Route to serve the Batman story
@story_bp.route('/batman_story', methods=['GET'])
def batman_story():
    # Simple story text
    story_text = "Once upon a time in Gotham, there was a hero named Batman."

    # Render the story page and pass the simple story text
    return render_template('batman_story.html', story=story_text)

# Route to generate an image based on a prompt
@story_bp.route('/story/generate_image', methods=['POST'])
def generate_image():
    data = request.json
    prompt = data.get('prompt', '')

    try:
        # Request to OpenAI for image generation using the new method
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
            
        )

        # Extract the image URL correctly from the response
        image_url = response.data[0].url  # Use attribute access instead of subscript

        return jsonify({'image_url': image_url})

    except Exception as e:
        # Log the error to help diagnose the issue
        print(f"Error generating image: {e}")
        return jsonify({'error': str(e)}), 500
