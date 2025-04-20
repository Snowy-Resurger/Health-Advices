from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

import random

app = Flask(__name__)
app.secret_key = "Hello_World!"  # Replace with a stronger secret key for production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baseinfo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)

# Route: home/intro page
@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

# Route: login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pw = request.form['password']

        user = User.query.filter_by(username=uname).first()
        if user and check_password_hash(user.password, pw):
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

# Route: signup
@app.route('/signup', methods=['POST'])
def signup():
    uname = request.form['newUsername']
    pw = request.form['newPassword']
    email = request.form['email']

    existing_user = User.query.filter((User.username == uname) | (User.email == email)).first()
    if existing_user:
        flash('Username or email already exists.', 'error')
        return redirect(url_for('login'))

    hashed_pw = generate_password_hash(pw)
    new_user = User(username=uname, password=hashed_pw, email=email)
    db.session.add(new_user)
    db.session.commit()

    flash('Signup successful! Please login.', 'success')
    return redirect(url_for('login'))

# Route: logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

# Run server
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates tables if not exist
    app.run(debug=True)
