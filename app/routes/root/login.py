from app import app, bcrypt
from flask import render_template, request, redirect, url_for, session, flash
from app.models.user import User


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Retrieve the user email from the db

        user=User.query.filter_by(email=email).first()

        # Check for password

        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('login succesful', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
        
    return render_template('root/login.html')

@app.route('/logout')
def logout():

    # To clear the session data of the user
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('home_page'))