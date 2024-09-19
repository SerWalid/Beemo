import json
from .models import db, Settings  # Adjust the import according to your project structure
from flask import Blueprint, render_template, session, flash, request, redirect, url_for, jsonify
from .utils import login_required, pin_required, logged_in_restricted, generate_time_array, calculate_age, \
    time_difference_from_today  # Import the decorator

from .models import User, Settings, db, Chat, Interaction, Notification

from .notifications import get_notifications
from .interactions import count_interactions_today_yesterday


# Create the Blueprint
settings_bp = Blueprint('settings', __name__)
def create_user_settings(user_id):
    goals = {
        "wordGoal": 1,
        "readingTimeGoal": 1,
        "sessionsPerWeekGoal": 1
    }

    # Convert the object to a JSON-formatted string
    goals_string = json.dumps(goals)
    
    notifications_preferences_to_set = {
        "highEmotionalEngagement": "none",
        "repetitiveQuestions": "none",
        "agitatedBehavior": "none"
    }
    
    notifications_preferences_string = json.dumps(notifications_preferences_to_set)
    
    settings = Settings(user_id=user_id, goals=goals_string, notifications_preferences=notifications_preferences_string)
    
    db.session.add(settings)
    db.session.commit()


@settings_bp.route('/settings')
@login_required
def setting():
    user_id = session.get('user_id')
    user = User.query.get(user_id)

    # Retrieve the user's settings
    settings = Settings.query.filter_by(user_id=user_id).first()
    if settings is None:
        settings = create_user_settings(user_id)
    # If `banned_topics` exists in settings, convert it to an array of dictionaries
    if settings.banned_topics:
        topics_list = settings.banned_topics.split(',')  # Split string by commas
        selected_topics = [{'id': str(i + 1), 'topic': topic.strip()} for i, topic in enumerate(topics_list)]
    else:
        # Default or empty banned topics list if none exist
        selected_topics = []

    # Reset specific settings if they are null
    if settings.sleep_time_start is None:
        sleep_time_start = ""  # Default start time
    else:
        sleep_time_start = settings.sleep_time_start
    if settings.sleep_time_end is None:
        sleep_time_end = ""  # Default end time
    else:
        sleep_time_end = settings.sleep_time_end
    if settings.daily_usage_limit is None:
        daily_usage_limit = ""
    else:
        daily_usage_limit = settings.daily_usage_limit
    if settings.goals is not None:
        # Parse the JSON string into a Python dictionary (object)
        goals_object = json.loads(settings.goals)
        word_goal = goals_object.get('wordGoal')
        reading_time_goal = goals_object.get('readingTimeGoal')
        sessions_per_week_goal = goals_object.get('sessionsPerWeekGoal')
    if settings.notifications_preferences is not None:
        notifications_preferences = json.loads(settings.notifications_preferences)
        high_emotional_engagement = notifications_preferences.get('highEmotionalEngagement')
        repetitive_questions = notifications_preferences.get('repetitiveQuestions')
        agitated_behavior = notifications_preferences.get('agitatedBehavior')

    if settings.alert_topics:
        alert_topics_list = settings.alert_topics.split(',')  # Split string by commas
        alert_topics = [{'id': str(i + 1), 'topic': topic.strip()} for i, topic in enumerate(alert_topics_list)]
    else:
        # Default or empty banned topics list if none exist
        alert_topics = []

    time_array = generate_time_array()
    # Retrieve all chats for the specific user
    chats = Chat.query.filter_by(user_id=user_id).all()

    # Convert the chats into a JSON-serializable format
    chat_list = []
    for chat in chats:
        chat_data = {
            'id': chat.id,
            'title': chat.title
        }
        chat_list.append(chat_data)

    notification_list = []
    notification_list, unviewed_count = get_notifications(user_id)

    return render_template('settings.html', chats=chat_list, banned_topics=selected_topics, user=user,
                           time_array=time_array, sleep_time_start=sleep_time_start, sleep_time_end=sleep_time_end,
                           daily_usage_limit=daily_usage_limit, word_goal=word_goal,
                           reading_time_goal=reading_time_goal, sessions_per_week_goal=sessions_per_week_goal,
                           alert_topics=alert_topics, high_emotional_engagement=high_emotional_engagement,
                           repetitive_questions=repetitive_questions, agitated_behavior=agitated_behavior,
                           notification_list=notification_list, unviewed_count=unviewed_count)


@settings_bp.route('/save-settings', methods=['POST'])
@login_required
def save_settings():
    # Get the user ID from the session
    user_id = session.get('user_id')

    # Find or create the settings record for the user
    settings = Settings.query.filter_by(user_id=user_id).first()

    if not settings:
        # Create new settings if none exists for the user
        settings = create_user_settings(user_id)

    # Get the JSON data sent from the frontend
    data = request.get_json()
    # Update the settings with non-empty values
    if 'startTime' in data:
        settings.sleep_time_start = data['startTime']
    if 'endTime' in data:
        settings.sleep_time_end = data['endTime']
    if 'dailyUsageLimit' in data:
        settings.daily_usage_limit = data['dailyUsageLimit']
    if 'education_level' in data:
        settings.education_level = data['education_level']
    if 'beemo_voice_tune' in data:
        settings.beemo_voice_tune = data['beemo_voice_tune']
    if 'notificationsPreferences' in data:
        settings.notifications_preferences = data['notificationsPreferences']
    if 'bannedTopics' in data:
        settings.banned_topics = data['bannedTopics']
    if 'goals' in data:
        settings.goals = data['goals']
    if 'alertTopics' in data:
        settings.alert_topics = data['alertTopics']
    if 'notificationPreferences' in data:
        settings.notifications_preferences = data['notificationPreferences']

    # Commit the changes to the database
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Settings saved successfully'}), 200


@settings_bp.route('/chats/<int:id>', methods=['GET'])
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
                           number_of_interactions=number_of_interactions, notification_list=notification_list,
                           interaction_to_highlight_id=interaction_to_highlight_id, unviewed_count=unviewed_count)