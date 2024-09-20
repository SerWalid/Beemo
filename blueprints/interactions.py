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

    return today_count, yesterday_count, round(percentage_change, 2)

def count_interactions_last_7_days(user_id):
    # Get today's date
    today = datetime.now().date()

    # Prepare the list to store interaction data for each day
    interaction_data = []

    # Loop through the last 7 days, including today
    for i in range(7):
        # Calculate the date for the current iteration
        day = today - timedelta(days=i)

        # Query interactions for the specific day
        interaction_count = db.session.query(func.count(Interaction.id)).filter(
            func.date(Interaction.created_at) == day,
            Interaction.user_id == user_id
        ).scalar()

        # Store the date and the count in a dictionary
        interaction_data.append({
            "date": day.strftime("%d %B %Y"),  # Format the date as "25 August 2024"
            "number_of_interaction": interaction_count
        })

    interaction_data.reverse()

    # Return the data as a JSON object
    return interaction_data

def get_interactions_count_today(user_id):
    # Get today's date
    today = datetime.now().date()

    # Query to count interactions for today
    interaction_count = db.session.query(func.count(Interaction.id)).filter(
        func.date(Interaction.created_at) == today,
        Interaction.user_id == user_id
    ).scalar()

    return interaction_count if interaction_count else 0

def get_all_interactions_today(user_id):
    # Get today's date
    today = datetime.now().date()

    # Query to get all interactions for today
    interactions = db.session.query(Interaction).filter(
        func.date(Interaction.created_at) == today,
        Interaction.user_id == user_id
    ).all()

    return interactions