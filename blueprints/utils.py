from functools import wraps
from flask import redirect, url_for, session, redirect
from datetime import datetime, timedelta, date
import re
import json


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