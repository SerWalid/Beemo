from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from .models import db, User

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
            return redirect(url_for('auth.login'))
        except Exception as e:
            # Log the error and rollback the transaction
            print(f"Error occurred: {e}")
            db.session.rollback()
            # Optionally, provide feedback to the user
    # Render the registration form
    return render_template('register.html')




@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve form data
        email = request.form['email']
        password = request.form['password']

        # Log the input data for debugging (optional)
        print(f"Login attempt - Email: {email}")

        # Query the user by email
        user = User.query.filter_by(email=email).first()

        # Check if the user exists and if the password is correct
        if user and check_password_hash(user.password, password):
            # Login successful
            print(f"Login successful for user: {user.email}")
            return redirect(url_for('main.LoadingHome'))
        else:
            # Login failed, redirect back to login page
            print(f"Login failed for user: {email}")
            flash('Invalid email or password. Please try again.', 'danger')
            return redirect(url_for('auth.login'))

    # Render the login form
    return render_template('Login.html')
