import json
from datetime import date
from .models import db, Report, User, Chat, Notification
from flask import Blueprint, render_template, session, flash, request, redirect, url_for, jsonify
from .notifications import get_notifications

report_bp = Blueprint('report', __name__)

def retrieve_today_report(user_id):
      # Assuming user_id is stored in the session
    today = date.today()
    
    # Query to retrieve today's report for the current user
    report = Report.query.filter(
        db.func.date(Report.created_at) == today,
        Report.user_id == user_id
    ).first()
    
    return report
def retrieve_all_reports(user_id):
    # Query to retrieve today's report for the current user
    reports = Report.query.filter(
        Report.user_id == user_id
    ).all()
    
    return reports
def generate_report(user_id, content):
    report = Report(content=content, user_id=user_id)
    db.session.add(report)
    db.session.commit()
    return report

def retrieve_report_by_id(id, user_id):
  report = Report.query.filter(
        Report.id == id,
        Report.user_id == user_id
    ).first()
    
  return report
@report_bp.route('/reports/<int:id>', methods=['GET'])
def get_report_by_id(id):
    user_id = session.get('user_id')
    report = retrieve_report_by_id(id, user_id)
    print(report)
    if not report:
        return jsonify({"error": "Report not found"}), 404
    report_content = json.loads(report.content)
    report_date = report.created_at.strftime("%B %d, %Y") 
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    chats = Chat.query.filter_by(user_id=user_id).all()
    reports = retrieve_all_reports(user_id)
    # Convert the chats into a JSON-serializable format
    chat_list = []
    for chat in chats:
        chat_data = {
            'id': chat.id,
            'title': chat.title
        }
        chat_list.append(chat_data)
    # Convert the reports into a JSON-serializable format
    report_list = []
    for report in reports:
        report_data = {
            'id': report.id,
            'created_at': report.created_at.strftime("%B %d, %Y"),
        }
        report_list.append(report_data)
    notification_list = []
    notification_list, unviewed_count = get_notifications(user_id)
    # Prepare the data to return (you can use the to_dict method if defined)
    print(report_content)

    return render_template('report-history.html', report=report_content, report_date = report_date, user=user, chats=chat_list, reports=report_list,
                           notification_list=notification_list,
                            unviewed_count=unviewed_count )

