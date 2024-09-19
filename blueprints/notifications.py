from .models import db, Notification  # Adjust the import according to your project structure
from datetime import datetime

def get_notifications(user_id):
    # Query notifications and order by created_at in descending order
    notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()
    notification_list = []
    unviewed_count = 0
    for notification in notifications:
        # Convert created_at to a datetime object if necessary
        if isinstance(notification.created_at, str):
            created_at = datetime.strptime(notification.created_at, '%Y-%m-%d %H:%M:%S')
        else:
            created_at = notification.created_at

        # Format the created_at timestamp
        formatted_created_at = created_at.strftime('%A, %H:%M')

        notification_data = {
            'id': notification.id,
            'topic': notification.topic,
            'viewed': notification.viewed,
            'message': notification.message,
            'chat_id': notification.chat_id,
            'interaction_id': notification.interaction_id,
            'created_at': formatted_created_at,
            'notification_type': notification.notification_type
        }
        if(notification.viewed == False):
            unviewed_count += 1
        notification_list.append(notification_data)

    

    return notification_list, unviewed_count