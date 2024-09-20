from flask import Blueprint, render_template, session, flash, request, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, db
user_bp = Blueprint('user', __name__)
from .utils import login_required
@login_required
@user_bp.route('/profile', methods=['POST'])
def update_profile():
    user_id = session.get('user_id')
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Fetching form data
    full_name = request.form.get('full_name', '').strip()
    email = request.form.get('email', '').strip()
    current_password = request.form.get('current_password', '').strip()
    new_password = request.form.get('new_password', '').strip()
    phone = request.form.get('phone', '').strip()
    child_name = request.form.get('child_name', '').strip()
    gender = request.form.get('gender', '').strip()
    child_birth_date = request.form.get('child_birth_date', '').strip()

    # Validating fields are not empty
    if not all([full_name, email, phone, child_name, gender, child_birth_date]):
        return jsonify({"error": "All fields are required"}), 400

    # Updating user information
    user.full_name = full_name
    user.email = email
    user.phone_number = phone
    user.child_name = child_name
    user.gender = gender
    user.child_birth_date = child_birth_date

    # Password check and update
    if current_password and new_password:
        if not check_password_hash(user.password, current_password):
            return jsonify({"error": "Current password is incorrect"}), 400
        user.password = generate_password_hash(new_password)

    # Saving changes to the database
    try:
        db.session.commit()
        return jsonify({"message": "Profile updated successfully", "success": "true"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500