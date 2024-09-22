import os
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import or_
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from config import Config
from models import db, User, Homework  # Import db and models from models.py
from forms import RegistrationForm


app = Flask(__name__)
app.config.from_object(Config)

app.config['FREEZER_RUN'] = False


def freezer_url_for(endpoint, **values):
    url = url_for(endpoint, **values)
    if app.config.get('FREEZER_RUN', False):
        # Remove query parameters
        url = url.split('?')[0]
        # Remove leading slash
        if url.startswith('/'):
            url = url[1:]
        # Append '.html' if not a static file and no extension
        if not url.startswith('static/') and '.' not in url:
            url += '.html'
    return url


# Replace the default `url_for` with the custom one in the Jinja environment
app.jinja_env.globals['url_for'] = freezer_url_for

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/signup.html", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route("/login.html", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        identifier = request.form['identifier']
        password = request.form['password']
        user = User.query.filter(
            or_(User.username == identifier, User.email == identifier)
        ).first()
        if user is None or not user.check_password(password):
            flash('Invalid username/email or password', 'danger')
            return redirect(url_for('login'))
        login_user(user)
        flash('Logged in successfully.', 'success')
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route("/homework.html", methods=['GET', 'POST'])
@login_required
def homework():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_homework = Homework(title=title, content=content, author=current_user)
        db.session.add(new_homework)
        db.session.commit()
        flash('Your homework has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('homework.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)