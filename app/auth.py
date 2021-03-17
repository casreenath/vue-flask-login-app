from flask import Blueprint, render_template, jsonify, request, redirect, g
from flask_login import current_user, login_required, login_user, logout_user
from app import db
from .models import User
auth = Blueprint('auth', __name__)


@auth.before_request
def get_current_user():
    g.user = current_user


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('index.html')
    rec_data = request.get_json()
    if current_user.is_authenticated:
        print("Already logged in")
    # print(rec_data)
    username = rec_data['username']
    password = rec_data['password']
    try:
        User.try_login(username, password)
    except Exception as errmsg:
        ret_data = {'status': True, 'loggedin': False,
                    'error': str(errmsg)}
        return jsonify(ret_data)
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username, password)
        db.session.add(user)
        db.session.commit()
    login_user(user)
    ret_data = {'status': True, 'loggedin': True, 'error': ''}
    return jsonify(ret_data)


@auth.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        ret_data = {'status': True, 'loggedin': False, 'error': ''}
    except Exception as errmsg:
        ret_data = {'status': False, 'loggedin': None, 'error': str(errmsg)}
    return jsonify(ret_data)
