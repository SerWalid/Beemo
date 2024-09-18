from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from .models import db, User, Settings
import json


auth_bp = Blueprint('auth', __name__)


# Load environment variables from .env file
load_dotenv()
# Access environment variables
api_key = os.getenv('API_KEY')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Retrieve form data
        full_name = request.form['full_name']
        email_address = request.form['email_address']
        password = request.form['password']
        child_birth_date = request.form['birth_date']
        gender = request.form['gender']  # Removed the comma to fix the issue
        child_name = request.form['child_full_name']
        country = request.form['country']
        phone_number = request.form['phone_number']
        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create a new User instance
        new_client = User(
            full_name=full_name,
            email=email_address,
            password=hashed_password,
            child_birth_date=child_birth_date,
            gender=gender,
            child_name=child_name,
            country=country,
            phone_number=phone_number
        )

        try:
            # Add the new user to the session and commit to the database
            db.session.add(new_client)
            db.session.commit()
            goals = {
            "wordGoal": 1,
            "readingTimeGoal": 1,
            "sessionsPerWeekGoal": 1}
    
            # Convert the object to a JSON-formatted string
            goals_string = json.dumps(goals)
            settings = Settings(user_id=new_client.id, daily_usage_limit=0, goals=goals_string)        
            
            db.session.add(settings)
            db.session.commit()

            return redirect(url_for('auth.login'))
        except Exception as e:
            # Log the error and rollback the transaction
            print(f"Error occurred: {e}")
            db.session.rollback()
            # Optionally, provide feedback to the user
    # Render the registration form
    african_countries = [
    "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", 
    "Cabo Verde", "Cameroon", "Central African Republic", "Chad", "Comoros", 
    "Democratic Republic of the Congo", "Republic of the Congo", "Djibouti", 
    "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia", 
    "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Ivory Coast", 
    "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", 
    "Mali", "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", 
    "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe", "Senegal", 
    "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan", 
    "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"
]
    return render_template('register.html', countries=african_countries)




@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve form data
        email = request.form['email']
        password = request.form['password']

        # Query the user by email
        user = User.query.filter_by(email=email).first()

        # Check if the user exists and if the password is correct
        if user and check_password_hash(user.password, password):
            # Store user information in the session
            session['user_id'] = user.id
            session['user_email'] = user.email

            print(f"Login successful for user: {user.email}")

            # Redirect to the home page or another route
            return redirect(url_for('main.LoadingHome'))
        else:
            # Login failed, redirect back to login page
            return redirect(url_for('auth.login'))

    # Render the login form
    return render_template('Login.html')

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # Clear user information from the session
    session.pop('user_id', None)
    session.pop('user_email', None)

    # Optionally, you can clear the entire session
    # session.clear()

    # Redirect to login page or homepage after logout
    return redirect(url_for('auth.login'))