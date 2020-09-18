from flask import Blueprint
from flask import flash, render_template, request
from werkzeug.security import check_password_hash, generate_password_hash

import time

from connection import db_users
from packages_learning.auth.forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__, template_folder='./templates')


@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.username.data
        error = None

        user = db_users.find_one({"username": username})

        if user:
            if check_password_hash(user['password'], password):
                return {"token": "xyz"}
            error = "Invalid Password"
        error = "Username is not found"
        
        return render_template("login.html", error=error, title="Sign In", form=form)

    return render_template('login.html', title="Sign In", form=form)


@auth_bp.route('/register', methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        error = ""
        email = form.email.data
        username = form.username.data
        password = generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=32)
        fullname = form.full_name.data
        
        is_username_exists = db_users.find_one({"username": username})
        if is_username_exists:
            error = "username is exists"
            return render_template("register.html", error=error, title="Sign Up", form=form)
        
        data = {
            "email": email,
            "username": username,
            "password": password,
            "full_name": fullname,
            "is_approved" : False,
            "privilage": "user",
            "is_banned": False,
            "created_at": int(time.time()),
            "updated_at": int(time.time())
        }
        try:
            db_users.insert_one(data)
            return render_template('register.html', success=True, title="Sign Up", form=form)
        except Exception as err:
            error = err
            return render_template('register.html', error=error, title="Sign Up", form=form)

    return render_template('register.html', title="Sign Up", form=form)