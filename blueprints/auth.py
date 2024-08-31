from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from .models import db, Client

auth_bp = Blueprint('auth', __name__)


# Load environment variables from .env file
load_dotenv()
# Access environment variables
api_key = os.getenv('API_KEY')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email_address = request.form['email_address']
        password = request.form['password']
        birth_date = request.form['birth_date']
        gender = request.form['gender']
        street_address_1 = request.form['street_address_1']
        street_address_2 = request.form['street_address_2']
        country = request.form['country']
        city = request.form['city']

        hashed_password = generate_password_hash(password)

        new_client = Client(
            full_name=full_name, 
            email_address=email_address, 
            phone_number=hashed_password, 
            birth_date=birth_date, 
            gender=gender, 
            street_address_1=street_address_1, 
            street_address_2=street_address_2, 
            country=country, 
            city=city
        )

        try:
            db.session.add(new_client)
            db.session.commit()
            return redirect(url_for('auth.login'))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        client = Client.query.filter_by(email_address=email).first()

        if client and check_password_hash(client.phone_number, password):
            # Login successful
            return redirect(url_for('main.LoadingHome'))
        else:
            return redirect(url_for('auth.login'))

    return render_template('Login.html')