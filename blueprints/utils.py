from functools import wraps
from flask import redirect, url_for, session, redirect
from datetime import datetime, timedelta, date
import re
import json
from .models import Settings


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)

    return decorated_function


def pin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('parent_zone_pin') != '1234':
            return redirect(url_for('main.show_pin_modal'))
        return f(*args, **kwargs)

    return decorated_function


def logged_in_restricted(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' in session:  # or any other condition to check if the user is logged in
            return redirect(url_for('main.Home'))  # redirect to a different page or show an error
        return f(*args, **kwargs)

    return decorated_function


def generate_time_array():
    times = []
    for hour in range(24):
        for minute in range(0, 60, 15):
            time_str = f"{hour:02}:{minute:02}"
            times.append(time_str)
    return times


def calculate_age(birthdate):
    # If the input is a string, convert it to a datetime object
    if isinstance(birthdate, str):
        birthdate = datetime.strptime(birthdate, "%Y-%m-%d").date()

    # Get today's date
    today = date.today()

    # Calculate the difference in years
    age = today.year - birthdate.year

    # Adjust age if the birthdate hasn't occurred yet this year
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1

    return age


def time_difference_from_today(date_input):
    # If the input is a string, convert it to a datetime object
    if isinstance(date_input, str):
        date_input = datetime.strptime(date_input, "%Y-%m-%d").date()

    # Get today's date
    today = date.today()

    # Calculate the difference in years, months, and days
    years_diff = today.year - date_input.year
    months_diff = today.month - date_input.month
    days_diff = today.day - date_input.day

    # Adjust months_diff and years_diff if necessary
    if days_diff < 0:
        months_diff -= 1
        days_diff += (date_input.replace(day=1) - date_input.replace(day=0)).day

    if months_diff < 0:
        years_diff -= 1
        months_diff += 12

    # Determine the appropriate unit to return
    if years_diff > 0:
        return f"{years_diff} year{'s' if years_diff > 1 else ''}"
    elif months_diff > 0:
        return f"{months_diff} month{'s' if months_diff > 1 else ''}"
    elif days_diff > 0:
        return f"{days_diff} day{'s' if days_diff > 1 else ''}"
    else:
        return "Today"


def split_message(response: str) -> tuple:
    """
    Splits the response into actual text and metadata.
    Assumes metadata is appended at the end of the message after 'metadata:'.
    The metadata is expected to be in JSON format inside '[]' brackets.

    This function:
    - Removes leading/trailing spaces.
    - Strips any unnecessary spaces between brackets and content.
    - Removes '//' and parses the metadata into JSON.

    Returns:
    - text: the main part of the message.
    - metadata_json: the parsed JSON object if available, otherwise None.
    """
    metadata_json = None

    # Check if "metadata:" exists in the response
    if "metadata:" in response:
        # Split the response into text and metadata parts
        parts = response.split("metadata:", 1)
        text = parts[0].strip()  # The text part before metadata

        # Process the metadata part
        metadata = parts[1].strip() if len(parts) > 1 else ""

        # Remove any '//' from the metadata and clean up unnecessary spaces
        metadata = metadata.replace("[ ", "[").replace(" ]", "]").replace("[", "").replace("] ", "]").replace("]",
                                                                                                              "").strip()

        metadata = metadata.replace("'", '"')

        # Attempt to parse the cleaned metadata into JSON
        try:
            metadata_json = json.loads(metadata)
        except json.JSONDecodeError:
            # If parsing fails, return the text only without metadata
            return text, None
    else:
        # If no metadata found, return just the text
        text = response.strip()

    return text, metadata_json

def calculate_progress(target, achieved):
    if target == 0:
        return 0  # Avoid division by zero

    progress = (achieved / target) * 100
    if progress > 100:
        return 100
    return int(progress)

def calculate_time_difference_in_seconds(start_time: str, end_time: str) -> int:
    # Define the time format
    time_format = "%H:%M"
    
    # Convert the time strings to datetime objects
    start_time_obj = datetime.strptime(start_time, time_format)
    end_time_obj = datetime.strptime(end_time, time_format)
    
    # Calculate the time difference in seconds
    if end_time_obj >= start_time_obj:
        time_difference = end_time_obj - start_time_obj
    else:
        # If the end time is earlier than the start time, add 24 hours to the end time
        time_difference = (end_time_obj + timedelta(days=1)) - start_time_obj
    
    # Get the total time difference in seconds
    total_seconds = time_difference.seconds
    
    return total_seconds


def is_time_between(check_time: str, start_time: str, end_time: str) -> bool:
    check = datetime.strptime(check_time, "%H:%M")
    start = datetime.strptime(start_time, "%H:%M")
    end = datetime.strptime(end_time, "%H:%M")

    # Handle cases where end time is past midnight
    if end < start:
        end += timedelta(days=1)
        if check < start:
            check += timedelta(days=1)

    return start <= check < end

# The actual decorator
def check_sleep_time(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get user_id from session
        user_id = session['user_id']
        if not user_id:
            # No user session, allow the request to pass
            return f(*args, **kwargs)

        # Retrieve user settings
        settings = Settings.query.filter_by(user_id=user_id).first()

        # Check if settings exist and if sleep times are present
        if settings and settings.sleep_time_start and settings.sleep_time_end:
            # Get the current time in HH:MM format
            current_time = datetime.now().strftime("%H:%M")

            # Check if current time is within the user's sleep time range
            if is_time_between(current_time, settings.sleep_time_start, settings.sleep_time_end):
                # Redirect to 'main.sleep_time' if within sleep time
                return redirect(url_for('main.sleep_time'))

        # Allow access if not in sleep time or if settings are missing
        return f(*args, **kwargs)

    return decorated_function

