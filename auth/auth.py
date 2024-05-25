# Import necessary modules and components from Flask
from flask import Blueprint, render_template, url_for, request, flash, redirect

# Import validator module for input validation functions
from .validator import *

# Import User model and database instance
from models.model import User
from ext.ext import db 

# Import login and logout functions from Flask-Login
from flask_login import login_user, logout_user, current_user

# Import datetime module for timestamp manipulation
import datetime

# Define a Flask Blueprint for the authentication module
auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")

# Route for user login
@auth.route('/login', methods=['POST','GET'])
def login():
    # Check if the user is already authenticated
    if current_user.is_authenticated:
        flash("Already logged in", 'info')
        return redirect(url_for('auth.home'))
    else:
        # If a POST request is made
        if request.method == 'POST':
            # Retrieve username and password from the form
            username = request.form['username']
            password = request.form['password']
            
            # Query the database for the user with the provided username
            user = User.query.filter_by(username=username).first()

            # If user does not exist, show error message
            if not user:
                flash('username does not exist', 'warning')
                return render_template('login.html', username=username, username_error=True)
            else:
                # If password matches, log in the user and redirect to home page
                if password == user.password:
                    login_user(user)
                    flash('Logged in successfully', 'success')
                    return redirect(url_for('main.add_recipe'))
                else:
                    # If password is incorrect, show error message
                    flash('Password is incorrect', 'danger')
                    return render_template('login.html', username=username, password_error=True)
        return render_template('login.html')

# Route for user registration
@auth.route('/register', methods=['POST', 'GET'])
def register():
    # Check if the user is already authenticated
    if current_user.is_authenticated:
        flash("Already logged in", 'info')
        return redirect(url_for('auth.home'))
    else:
        # If a POST request is made
        if request.method == 'POST':
            # Retrieve name, username, password, and re-entered password from the form
            username = request.form['username']
            password = request.form['password']
            re_password = request.form['re_password']
            
            # Validate name, username format, and password complexity
            if validate_username(username) is not True:
                flash('Name is invalid or less than 3 characters', 'danger')
                return render_template('register.html', username=username, name_error=True)

            if validate_password(password,re_password) is not True:
                flash('Password does not match or less than 8 characters','danger')
                return render_template('register.html', username=username, password_error=True)


            # Check if the username is already in use
            user_exists = User.query.filter_by(username=username).first()
            if user_exists:
                flash("username already taken")
                return render_template('register.html', username=username, username_error=True)
            else:
                # Create a new user and add to the database
                user = User(username=username, password=password)
                db.session.add(user)
                db.session.commit()
                flash('Account created successfully, Log In', 'success')
                return redirect(url_for('auth.login'))
                
        return render_template('register.html')

# Route for user logout
@auth.route('/logout', methods=['POST', 'GET'])
def logout():
    # Check if the user is authenticated
    if current_user.is_authenticated:
        # Log out the user and redirect to login page
        logout_user()
        flash("Logged out successfully", 'success')
        return redirect(url_for('auth.login'))
    return render_template('login.html')

# Route for the home page
@auth.route('/home', methods=['POST', 'GET'])
def home():
    # Get user ID and retrieve user details
    
    return f'<html> username:{current_user.username} <html>'
