from flask import Blueprint, render_template, session, flash, request, redirect, url_for, jsonify
from .utils import login_required, pin_required, logged_in_restricted  # Import the decorator
from .models import User
from datetime import datetime, timedelta
import os
import random

main_bp = Blueprint('main', __name__, static_folder='static')



# Ensure the uploads directory exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

questions = [
    {"emotion": "happy", "images": ["happykid1.jpg", "happykid2.jpg"]},
    {"emotion": "sad", "images": ["sadkid1.jpg", "sadkid2.jpg"]},
    {"emotion": "surprised", "images": ["surprisekid1.jpg", "surprisekid2.jpg"]},
    {"emotion": "angry", "images": ["angrykid1.jpg", "angrykid2.jpg"]},
    {"emotion": "fear", "images": ["fearkid1.jpg", "fearkid2.jpg"]}
]



@main_bp.route('/')
@logged_in_restricted
def index():
    return render_template('index.html')

@main_bp.route('/PageOff')
@logged_in_restricted
def PageOff():
    return render_template('PageOff.html')

@main_bp.route('/LoaderWriting')
@login_required
def LoaderWriting():
    return render_template('LoaderWriting.html')

@main_bp.route('/Games')
def Games():
    return render_template('Games.html')

@main_bp.route('/painting')
def painting():
    return render_template('painting.html')

@main_bp.route('/art')
@login_required
def art():
    return render_template('art.html')


@main_bp.route('/ImageChoice')
@login_required
def ImageChoice():
    return render_template('ImageChoice.html')





@main_bp.route('/Number')
def Number():
    return render_template('Number.html')


@main_bp.route('/EvaluatePainting')
def EvaluatePainting():
    return render_template('EvaluatePainting.html')

@main_bp.route('/MemoryGame')
def MemoryGame():
    return render_template('MemoryGame.html')

@main_bp.route('/emotion')
def emotion():
    return render_template('emotion.html')

@main_bp.route('/chatbotinterface')
def chatbotinterface():
    return render_template('ChatBotInterface.html')

@main_bp.route('/EmotionDetection')
def EmotionDetection():
    return render_template('EmotionDetection.html')

@main_bp.route('/ActivitiesMenu')
def ActivitiesMenu():
    return render_template('ActivitiesMenu.html')

@main_bp.route('/Tetris')
def Tetris():
    return render_template('Tetris.html')

@main_bp.route('/Cube')
def Cube():
    return render_template('Cube.html')

@main_bp.route('/GameSelectTest')
def GameSelectTest():
    return render_template('GameSelectTest.html')

@main_bp.route('/StoryTelling')
def StoryTelling():
    return render_template('StoryTelling.html')

@main_bp.route('/chatbottest_page')
def chatbottest_page():
    return render_template('chatbotTest.html')

@main_bp.route('/Music')
def Music():
    return render_template('Music.html')

@main_bp.route('/PlayStation')
def PlayStation():
    return render_template('PlayStation.html')

@main_bp.route('/BoxCube')
def BoxCube():
    return render_template('BoxCube.html')

@main_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/beemo')
def beemo():
    return render_template('beemo.html')


@main_bp.route('/game-zone')
@login_required
def game_zone():
    return render_template('First.html')

@main_bp.route('/chat')
@login_required
def Chat():
    return render_template('test.html')

@main_bp.route('/writing')
@login_required
def writing():
    return render_template('writing.html')

@main_bp.route('/home')
@login_required
def Home():
    return render_template('homePage.html')
@main_bp.route('/story-time')
@login_required
def Story():
    return render_template('storyTime.html')


@main_bp.route('/batman_story')
@login_required
def batman_story():
    return render_template('batman_story.html')


@main_bp.route('/spiderman-story')
@login_required
def spiderman_story():
    return render_template('spiderman_story.html')


@main_bp.route('/tom-and-jerry-story')
@login_required
def tom_and_jerry_story():
    return render_template('tom_and_jerry_story.html')

@main_bp.route('/LoadingHome')
@login_required
def LoadingHome():
    return render_template('LoadingHome.html')

@main_bp.route('/LearnEmotions')
@login_required
def LearnEmotions():
    return render_template('LearnEmotions.html')

@main_bp.route('/quiz')
@login_required
def quiz():
    return render_template('quiz.html')

@main_bp.route('/Vision')
@login_required
def Vision():
    return render_template('vision.html')

@main_bp.route('/dashboardActivities')
@login_required
def dashboardActivities():
    return render_template('dashboardActivities.html')


@main_bp.route('/parent')
@login_required
@pin_required
def parent():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    print("parent_zone_pin", session.get('parent_zone_pin'))

    child_name="Alex"
    parent_name="John"
    goals = [
    {
        "name": "Learn new Words: 12/12",
        "progress": 100
    },
    {
        "name": "Read For 240 Minutes: 240/180",
        "progress": 75
    },
    {
        "name": "Have 10 Interactive Sessions: 10/10",
        "progress": 100
    }
]
    beemo_daily_usage_timeline = [
    {
        "time": "08:00 AM",
        "event": "Morning Greeting",
        "activity": f"Beemo greeted {child_name} with a cheerful 'Good morning!'",
        "emotion_detected": "Neutral",
        "duration": "5 minutes",
        "notes": f"{child_name} responded positively and engaged in a short conversation about today’s plans."
    },
    {
        "time": "09:30 AM",
        "event": "Educational Game: Counting Numbers",
        "activity": f"Played a counting game focused on numbers 1-10 with {child_name}.",
        "emotion_detected": "Happy",
        "duration": "15 minutes",
        "progress": f"Successfully counted up to 7 without assistance.",
        "notes": f"Beemo praised {child_name} for their effort."
    },
    {
        "time": "11:00 AM",
        "event": "Storytime",
        "activity": f"Beemo read a short story, 'The Brave Little Fox,' to {child_name}.",
        "emotion_detected": "Engaged",
        "duration": "10 minutes",
        "notes": f"{child_name} showed interest and answered questions about the story."
    },
    {
        "time": "12:30 PM",
        "event": "Lunchtime Reminder",
        "activity": f"Beemo reminded {child_name} that it was time for lunch.",
        "emotion_detected": "Neutral",
        "duration": "2 minutes",
        "notes": f"{child_name} acknowledged the reminder and went to eat."
    },
    {
        "time": "02:00 PM",
        "event": "Mood Check-In",
        "activity": f"Beemo asked {child_name} how they were feeling.",
        "emotion_detected": "Sad",
        "duration": "5 minutes",
        "notes": f"Beemo comforted {child_name} and suggested listening to their favorite song."
    },
    {
        "time": "02:30 PM",
        "event": "Music Time",
        "activity": f"Listened to favorite songs with Beemo.",
        "emotion_detected": "Happy",
        "duration": "20 minutes",
        "notes": f"{child_name} danced along to the music, and Beemo joined in by clapping."
    },
    {
        "time": "04:00 PM",
        "event": "Creative Drawing Activity",
        "activity": f"Beemo encouraged {child_name} to draw a picture of their favorite animal.",
        "emotion_detected": "Excited",
        "duration": "25 minutes",
        "outcome": f"{child_name} drew a picture of a cat and proudly showed it to Beemo.",
        "notes": f"Beemo praised the drawing and suggested adding colors next time."
    },
    {
        "time": "06:00 PM",
        "event": "Social Interaction Role-Play",
        "activity": f"Practiced a role-play scenario where {child_name} introduced themselves to a new friend.",
        "emotion_detected": "Anxious",
        "duration": "15 minutes",
        "notes": f"{child_name} was initially hesitant, but Beemo provided encouragement and tips."
    },
    {
        "time": "07:30 PM",
        "event": "Evening Reflection",
        "activity": f"Beemo asked {child_name} to reflect on their day and share a highlight.",
        "emotion_detected": "Calm",
        "duration": "10 minutes",
        "notes": f"{child_name} mentioned enjoying the drawing activity the most."
    },
    {
        "time": "08:00 PM",
        "event": "Bedtime Story",
        "activity": f"Beemo read a calming bedtime story, 'The Sleepy Bear,' to {child_name}.",
        "emotion_detected": "Relaxed",
        "duration": "15 minutes",
        "notes": f"{child_name} appeared relaxed and ready for bed after the story."
    }
]
    dashboard_stats = [
    {
        "title": "Today's Total Interactions",
        "icon_color": "bg-gray-500",
        "value": 36,
        "change_percentage": 1.7,
        "change_direction": "up",
        "previous_value": 30,
        "previous_period": "Yesterday"
    },
    {
        "title": "Current Plan",
        "icon_color": "bg-green-500",
        "value": "Normal Plan",
        "renewal_date": "August 1, 2024"
    },
    {
        "title": "New Words Learnt",
        "icon_color": "bg-green-500",
        "value": 14,
        "change_percentage": 5.6,
        "change_direction": "up",
        "previous_value": 10,
        "previous_period": "Last week"
    }
]

    return render_template('dashboardHome.html', child_name=child_name, parent_name=parent_name, goals=goals, beemo_daily_usage_timeline=beemo_daily_usage_timeline, dashboard_stats=dashboard_stats, user=user)

@main_bp.route('/settings')
@login_required
def settings():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    selected_topics = [
        {'id': '1', 'topic': 'Hate'},
        {'id': '2', 'topic': 'Sadness'},
        # Add more selected topics as needed
    ]
    return render_template('settings.html', selected_topics=selected_topics, user=user)

@main_bp.route('/show-pin-modal', methods=['GET', 'POST'])
def show_pin_modal():
    if request.method == 'POST':
        entered_pin = ''.join(request.form.getlist('pin'))
        if entered_pin == '1234':
            session['parent_zone_pin'] = entered_pin
            return redirect(url_for('main.parent'))
        else:
            flash('Invalid PIN code. Please try again.')
    
    return render_template('pinModal.html')