from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Settings(db.Model):
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    sleep_time_start = db.Column(db.String(255), nullable=True)
    sleep_time_end = db.Column(db.String(255), nullable=True)
    daily_usage_limit = db.Column(db.Integer, nullable=True)
    education_level = db.Column(db.String(255), nullable=True)
    beemo_voice_tune = db.Column(db.String(255), nullable=True)
    notifications_preferences = db.Column(db.JSON, nullable=True)
    banned_topics = db.Column(db.String(1000), nullable=True)
    alert_topics = db.Column(db.String(1000), nullable=True)
    goals = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Subscription(db.Model):
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Foreign key to User


class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    topic = db.Column(db.String(255), nullable=True)
    notification_type = db.Column(db.String(255), nullable=True)
    viewed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'))
    interaction_id = db.Column(db.Integer, db.ForeignKey('interactions.id'))


class Chat(db.Model):
    __tablename__ = 'chats'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    interactions = db.relationship('Interaction', backref='chat')
    notifications = db.relationship('Notification', backref='chat', lazy=True)


class Interaction(db.Model):
    __tablename__ = 'interactions'

    id = db.Column(db.Integer, primary_key=True)
    interaction_type = db.Column(db.String(255), nullable=True)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    emotion_points = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'))

    notifications = db.relationship('Notification', backref='interaction', lazy=True)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    child_birth_date = db.Column(db.Date, nullable=False)
    child_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    country = db.Column(db.String(50), nullable=False)
    pin_code = db.Column(db.String(50), nullable=True)

    reports = db.relationship('Report', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    chats = db.relationship('Chat', backref='user', lazy=True)
    settings = db.relationship('Settings', backref='user', uselist=False)

    subscriptions = db.relationship('Subscription', backref='user', lazy=True,
                                    foreign_keys='Subscription.user_id')  # One-to-many relationship