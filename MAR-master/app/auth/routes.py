# app/auth/routes.py
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from app.auth import bp
from app.models import User  # Assuming you have a User model
from app import db

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):  # Assuming check_password is a method on User
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid credentials.')
    
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Here you should add checks and save the new user to the database
        new_user = User(email=email)
        new_user.set_password(password)  # Assuming set_password is a method on User
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful!')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')
