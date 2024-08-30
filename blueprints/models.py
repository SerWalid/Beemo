from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Client(db.Model):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email_address = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    street_address_1 = db.Column(db.String(255), nullable=False)
    street_address_2 = db.Column(db.String(255))
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)

    def __init__(self, full_name, email_address, phone_number, birth_date, gender, street_address_1, street_address_2, country, city):
        self.full_name = full_name
        self.email_address = email_address
        self.phone_number = phone_number
        self.birth_date = birth_date
        self.gender = gender
        self.street_address_1 = street_address_1
        self.street_address_2 = street_address_2
        self.country = country
        self.city = city
