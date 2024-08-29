from flask import Blueprint, render_template

# Create the blueprint for the story
story_bp = Blueprint('story', __name__)

# Route to serve the Batman story
@story_bp.route('/batman_story', methods=['GET'])
def batman_story():
    # Simple story text
    story_text = "Once upon a time in Gotham, there was a hero named Batman."

    # Render the story page and pass the simple story text
    return render_template('batman_story.html', story=story_text)