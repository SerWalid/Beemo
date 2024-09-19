import json
from flask import Blueprint, render_template, session, flash, request, redirect, url_for, jsonify
from .utils import login_required, pin_required, logged_in_restricted, generate_time_array, calculate_age, \
    time_difference_from_today  # Import the decorator
from .models import User, Settings, db, Chat, Interaction, Notification
from datetime import datetime, timedelta, date
import os
import random
from .settings import create_user_settings
from .notifications import get_notifications
from .interactions import count_interactions_today_yesterday
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


@main_bp.route('/Games')
def Games():
    return render_template('Games.html')



@main_bp.route('/ImageChoice')
@login_required
def ImageChoice():
    return render_template('ImageChoice.html')


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
def Chatbot():
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

    # Pass the chat to the template
    return render_template('test.html', chat=chat)


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


@main_bp.route('/LoaderWriting')
@login_required
def LoaderWriting():
    return render_template('LoaderWriting.html')

@main_bp.route('/writing')
@login_required
def writing():
    return render_template('writing.html')


@main_bp.route('/Vision')
@login_required
def Vision():
    return render_template('vision.html')

@main_bp.route('/GamesSelection')
@login_required
def GamesSelection():
    return render_template('GamesSelection.html')

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
    # Retrieve all chats for the specific user
    today_count, yesterday_count, rate_comparison = count_interactions_today_yesterday(user_id)
    chats = Chat.query.filter_by(user_id=user_id).all()

    # Convert the chats into a JSON-serializable format
    chat_list = []
    for chat in chats:
        chat_data = {
            'id': chat.id,
            'title': chat.title,
        }
        chat_list.append(chat_data)
    child_name = user.child_name
    parent_name = user.full_name
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
            "icon_color": rate_comparison > 0 and "bg-green-500" or "bg-red-500",
            "value": today_count,
            "change_percentage": abs(rate_comparison),
            "change_direction": rate_comparison > 0 and "up" or "down",
            "previous_value": yesterday_count,
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

    notification_list = []
    notification_list, unviewed_count = get_notifications(user_id)

    return render_template('dashboardHome.html', chats=chat_list, child_name=child_name, parent_name=parent_name,
                           goals=goals, beemo_daily_usage_timeline=beemo_daily_usage_timeline,
                           dashboard_stats=dashboard_stats, user=user, notification_list=notification_list, unviewed_count=unviewed_count)





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

@main_bp.route('/mark-notifications-as-read', methods=['POST'])
def mark_notifications_as_read():
    # Get the current user
    user_id = session.get('user_id')  # Implement this according to your authentication system

    # Mark all unread notifications as viewed
    Notification.query.filter_by(user_id=user_id, viewed=False).update({'viewed': True})
    db.session.commit()

    return jsonify({'message': 'Notifications marked as read'}), 200

@main_bp.route('/chats/<int:id>', methods=['GET'])
def get_chat_by_id(id):
    interaction_to_highlight_id = request.args.get('highlight')
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    chats = Chat.query.filter_by(user_id=user_id).all()
    # Convert the chats into a JSON-serializable format
    chat_list = []
    for chat in chats:
        chat_data = {
            'id': chat.id,
            'title': chat.title
        }
        chat_list.append(chat_data)
    # Query the Chat model using the id from the URL
    chat = Chat.query.get(id)

    if not chat:
        return jsonify({"error": "Chat not found"}), 404
    
    notification_list = []
    notification_list, unviewed_count = get_notifications(user_id)
    # Prepare the data to return (you can use the to_dict method if defined)
    interactions = Interaction.query.filter_by(chat_id=chat.id).all()

    chat_data = []
    chat_date = chat.created_at  # Assign default value
    number_of_interactions = 0
    for interaction in interactions:
        interaction_data = {
            'id': interaction.id,
            'interaction_type': interaction.interaction_type,
            'message': interaction.message,
            'response': interaction.response,
            'emotion_points': interaction.emotion_points,
            'created_at': interaction.created_at,
            'updated_at': interaction.updated_at,
        }
        chat_data.append(interaction_data)
        chat_date = chat.created_at
        number_of_interactions = len(interactions)
    return render_template('chat-history.html', interactions=chat_data, user=user, chats=chat_list, chat_date=chat_date,
                           number_of_interactions=number_of_interactions, notification_list=notification_list, interaction_to_highlight_id= interaction_to_highlight_id, unviewed_count = unviewed_count)