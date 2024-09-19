from datetime import datetime, timedelta
from sqlalchemy import func
from flask import session
from .models import db, Interaction  # Adjust the import according to your project structure

def count_interactions_today_yesterday(user_id):
    # Get today's and yesterday's date
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    # Query interactions for today
    today_count = db.session.query(func.count(Interaction.id)).filter(
        func.date(Interaction.created_at) == today,
        Interaction.user_id == user_id
    ).scalar()

    # Query interactions for yesterday
    yesterday_count = db.session.query(func.count(Interaction.id)).filter(
        func.date(Interaction.created_at) == yesterday,
        Interaction.user_id == user_id
    ).scalar()

    # Calculate the rate comparison
    if yesterday_count == 0:
        if today_count > 0:
            percentage_change = float('inf')  # Infinite increase if there were no interactions yesterday
        else:
            percentage_change = 0  # No change if there were no interactions both days
    else:
        percentage_change = ((today_count - yesterday_count) / yesterday_count) * 100

    return today_count, yesterday_count, percentage_change
