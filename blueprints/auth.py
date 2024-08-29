from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import Error

auth_bp = Blueprint('auth', __name__)

def create_connection():
    """
    Creates a connection to the MySQL database.
    Returns the connection object if successful, None otherwise.
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host='sql7.freesqldatabase.com',  # MySQL host
            user='sql7727502',  # MySQL username
            password='PwwVKdQe8w',  # MySQL password
            database='sql7727502'  # MySQL database name
        )
        if connection.is_connected():
            print("Connected to MySQL database")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


def init_db():
    """
    Initializes the database by creating the 'clients' table if it doesn't exist.
    """
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clients (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    full_name VARCHAR(255) NOT NULL,
                    email_address VARCHAR(255) NOT NULL UNIQUE,
                    phone_number VARCHAR(255) NOT NULL,
                    birth_date DATE NOT NULL,
                    gender VARCHAR(50) NOT NULL,
                    street_address_1 VARCHAR(255) NOT NULL,
                    street_address_2 VARCHAR(255),
                    country VARCHAR(100) NOT NULL,
                    city VARCHAR(100) NOT NULL
                )
            ''')
            connection.commit()
        except Error as e:
            print(f"The error '{e}' occurred during table creation")
        finally:
            cursor.close()
            connection.close()

init_db()






@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login.
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = create_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM clients WHERE email_address = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()

            if user and check_password_hash(user['phone_number'], password):
                # Login successful
                return redirect(url_for('main.LoadingHome'))
            else:
                return redirect(url_for('auth.login'))

    return render_template('Login.html')

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

        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute('''
                    INSERT INTO clients (
                        full_name, email_address, phone_number, birth_date, gender, 
                        street_address_1, street_address_2, country, city
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (full_name, email_address, generate_password_hash(password), birth_date, gender, street_address_1, street_address_2, country, city))
                connection.commit()
            except Error as e:
                print(f"The error '{e}' occurred during form submission")
            finally:
                cursor.close()
                connection.close()

        return redirect(url_for('auth.login'))

    return render_template('register.html')
