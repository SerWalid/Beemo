import json
from .models import db, Settings  # Adjust the import according to your project structure

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