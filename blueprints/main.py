import json
from flask import Blueprint, render_template, session, flash, request, redirect, url_for, jsonify
from .utils import login_required, pin_required, logged_in_restricted, generate_time_array, calculate_age, calculate_progress, time_difference_from_today, calculate_time_difference_in_seconds, check_sleep_time  # Import the decorator
from .models import User, Settings, db, Chat, Interaction, Notification
from datetime import datetime, timedelta, date
import os
import random
from .settings import create_user_settings
from .report import retrieve_all_reports
from .notifications import get_notifications
from .interactions import count_interactions_today_yesterday, count_interactions_last_7_days, get_interactions_count_today
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


@main_bp.route('/LANDPAGE')
@logged_in_restricted
def LANDPAGE():
    return render_template('LANDPAGE.html')

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
@check_sleep_time
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
@check_sleep_time
def Cube():
    return render_template('Cube.html')


@main_bp.route('/GameSelectTest')
@check_sleep_time
def GameSelectTest():
    return render_template('GameSelectTest.html')


@main_bp.route('/StoryTelling')
def StoryTelling():
    reset_parent_pin_code()
    return render_template('StoryTelling.html')


@main_bp.route('/chatbottest_page')
def chatbottest_page():
    return render_template('chatbotTest.html')


@main_bp.route('/BoxCube')
@check_sleep_time
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
    reset_parent_pin_code()
    return render_template('First.html')


@main_bp.route('/chat')
@check_sleep_time
@login_required
def Chatbot():
    reset_parent_pin_code()
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
@check_sleep_time
@login_required
def Home():
    reset_parent_pin_code()
    return render_template('homePage.html')


@main_bp.route('/story-time')
@check_sleep_time
@login_required
def Story():
    reset_parent_pin_code()
    return render_template('storyTime.html')


@main_bp.route('/GamesLoading')
@login_required
def GamesLoading():
    return render_template('GamesLoading.html')

@main_bp.route('/LoadingHome')
@login_required
def LoadingHome():
    return render_template('LoadingHome.html')


@main_bp.route('/LearnEmotions')
@check_sleep_time
@login_required
def LearnEmotions():
    reset_parent_pin_code()
    return render_template('LearnEmotions.html')


@main_bp.route('/quiz')
@check_sleep_time
@login_required
def quiz():
    reset_parent_pin_code()
    return render_template('quiz.html')


@main_bp.route('/LoaderWriting')
@login_required
def LoaderWriting():
    return render_template('LoaderWriting.html')

@main_bp.route('/writing')
@check_sleep_time
@login_required
def writing():
    reset_parent_pin_code()
    return render_template('writing.html')


@main_bp.route('/Vision')
@check_sleep_time
@login_required
def Vision():
    reset_parent_pin_code()
    return render_template('vision.html')

@main_bp.route('/GamesSelection')
@check_sleep_time
@login_required
def GamesSelection():
    reset_parent_pin_code()
    return render_template('GamesSelection.html')


@main_bp.route('/parent')
@login_required
@pin_required
def parent():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    # Retrieve all chats for the specific user
    today_count, yesterday_count, rate_comparison = count_interactions_today_yesterday(user_id)
    chats = Chat.query.filter_by(user_id=user_id).all()
    reports = retrieve_all_reports(user_id)
    settings = Settings.query.filter_by(user_id=user_id).first()
    user_goals = {
        "wordGoal": 1,
        "readingTimeGoal": 1,
        "sessionsPerWeekGoal": 1
    }
    if (settings.goals is not None):
        user_goals = json.loads(settings.goals)        
        user_goals = {key: int(value) for key, value in user_goals.items()}


    number_of_interactions_today = get_interactions_count_today(user_id)

    # Convert the chats into a JSON-serializable format
    chat_list = []
    for chat in chats:
        chat_data = {
            'id': chat.id,
            'title': chat.title,
        }
        chat_list.append(chat_data)
    # Convert the reports into a JSON-serializable format
    report_list = []
    for report in reports:
        report_data = {
            'id': report.id,
            'content': report.content,
            'created_at': report.created_at.strftime("%B %d, %Y")
        }
        report_list.append(report_data)

    child_name = user.child_name
    parent_name = user.full_name
    goals = [
        {
            "name": "Learn new Words",
            "target": user_goals.get("wordGoal"),
            "achieved": 0,
            "progress": calculate_progress(user_goals.get("wordGoal"), 0),
        },
        {
            "name": f"Read For {user_goals.get('readingTimeGoal')} Minutes",
            "target": user_goals.get("readingTimeGoal"),
            "achieved": user.reading_time,
            "progress": calculate_progress(user_goals.get("readingTimeGoal"), user.reading_time),
        },
        {
            "name": f"Have {user_goals.get('sessionsPerWeekGoal')} Interactive Sessions",
            "target": user_goals.get("sessionsPerWeekGoal"),
            "achieved": number_of_interactions_today,
            "progress": calculate_progress(user_goals.get("sessionsPerWeekGoal"), number_of_interactions_today),
        }
    ]
    goals_left = len([goal for goal in goals if goal["progress"] != 100])
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
    interactions_last_7_days = count_interactions_last_7_days(user_id)
    notification_list = []
    notification_list, unviewed_count = get_notifications(user_id)

    return render_template('dashboardHome.html', chats=chat_list, reports=report_list, child_name=child_name, parent_name=parent_name,
                           goals=goals,
                           dashboard_stats=dashboard_stats, user=user, notification_list=notification_list, unviewed_count=unviewed_count, goals_left = goals_left)


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


@main_bp.route('/sleep-time')
@login_required
def sleep_time():
    reset_parent_pin_code()
    user_id = session['user_id']
    settings = Settings.query.filter_by(user_id=user_id).first()
    time_difference_in_seconds = 0
    if settings is not None and settings.sleep_time_start is not None and settings.sleep_time_end is not None:
        current_time = datetime.now().strftime("%H:%M")
        time_difference_in_seconds = calculate_time_difference_in_seconds(current_time, settings.sleep_time_end)
    print(time_difference_in_seconds)
    
    return render_template('sleep-time.html', time_difference_in_seconds=time_difference_in_seconds)


@main_bp.route('/set-pin', methods=['POST'])
def set_pin_code():
    entered_pin = request.form['pin']
    if entered_pin == '1234':
        session['parent_zone_pin'] = entered_pin
        return jsonify({'status': 'success', 'message': 'PIN code set successfully'}), 200
    else:
        return jsonify({'status': 'failure', 'message': 'Invalid PIN code'}), 401


@main_bp.route('/mark-notifications-as-read', methods=['POST'])
def mark_notifications_as_read():
    # Get the current user
    user_id = session.get('user_id')  # Implement this according to your authentication system

    # Mark all unread notifications as viewed
    Notification.query.filter_by(user_id=user_id, viewed=False).update({'viewed': True})
    db.session.commit()

    return jsonify({'message': 'Notifications marked as read'}), 200

@main_bp.route('/get-interaction-last-7-days', methods=['GET']) 
@login_required
def get_interaction_last_7_days():
    user_id = session.get('user_id')
    interactions_last_7_days = count_interactions_last_7_days(user_id)
    return jsonify(interactions_last_7_days), 200

def reset_parent_pin_code():
    if (session.get('parent_zone_pin') is not None):
        session.pop('parent_zone_pin', None)