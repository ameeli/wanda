from flask import Flask, flash, session, jsonify
from flask import request, render_template, redirect
from model import connect_to_db, db, User, Text
from send_texts import send_welcome_text
from datetime import datetime
import pytz
from sqlalchemy import func
from chart_data import get_all_responses, get_pie_data, get_mw_graph_data, get_not_mw_graph_data
from add_to_db import add_to_users, add_to_time_windows, add_to_responses

app = Flask(__name__)
app.secret_key = 'KEY'
app.config.from_object(__name__)

@app.route('/')
def display_homepage():
    """Display homepage to user."""
    if 'fname' not in session:
        return render_template("homepage.html")
    else:
        return render_template("profile_overview.html",
                               fname=session['fname'])


@app.route('/register', methods=['GET'])
def show_signup_form():
    """Shows signup form."""
    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def add_user():
    """Adds new user to database and texts confirmation to their mobile."""
    # get form variables from register_form.html
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    password = request.form['password']
    mobile = request.form['mobile']

    user_id = add_to_users(fname, lname, email, password, mobile)
    flash('Wanda welcomes you! Please set up your preferences.')
    # add user's first name and user_id to session
    session['fname'] = fname
    session['user_id'] = user_id
    # send confirmation text to user's mobile using Twilio
    send_welcome_text(mobile, user_id)
    return render_template('/preferences.html')


@app.route('/login', methods=['GET'])
def show_login_form():
    """Shows signin page."""
    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_user():
    """Logs user into app."""
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter(User.email==email).first()

    # if user email is in db and password matches
    if user and user.password == password:
        # add user's first name and user_id to session
        session['fname'] = user.fname
        session['user_id'] = user.id
        return redirect('/')
    else:
        flash('Your email or password was incorrect. Please try again.')
        return redirect('/login')


@app.route('/logout')
def logout_user():
    """Logs user out of app."""
    del session['fname']
    del session['user_id']
    return redirect('/')


@app.route('/preferences')
def show_preferences():
    """Shows user's current preferences and gives option to update."""
    if 'fname' in session:
        return render_template("preferences.html",
                               fname=session['fname'])
    else:
        return redirect('/')


@app.route('/preferences', methods=['POST'])
def update_preferences():
    """Adds user's time window preferences to time_windows table in db."""
    # get 2 lists of start and stop times from preferences.html
    start_times = request.form.getlist('start_time')
    stop_times = request.form.getlist('stop_time')
    days_of_week = [1, 2, 3, 4, 5, 6, 7]
    # zip start_times, stop_times, and days_of_week into list of tuples
    time_windows = zip(start_times, stop_times, days_of_week)

    # for every item in time_window, instantiate an instance of TimeWindow
    for start_time, stop_time, day_of_week in time_windows:
        add_to_time_windows(start_time, stop_time, day_of_week, session['user_id'])
    
    flash('Your time window preferences have been successfully updated!')
    return redirect('/')


@app.route('/sms', methods=['GET', 'POST'])
def incoming_sms():
    """Gets user's responses to app's texts."""
    # Get the message the user sent our Twilio number
    text_body = request.values.get('Body', None)

    mobile = str(request.values.get('From'))[-10:]

    user_id = db.session.query(User.id).filter(User.mobile==mobile).scalar()

    last_text_time = db.session.query(
        func.max(Text.sent_time)).filter(
        Text.user_id==user_id).scalar()

    last_text_id = db.session.query(
        Text.id).filter(
        Text.user_id==user_id, Text.sent_time==last_text_time).scalar()

    pacific = pytz.timezone('US/Pacific')
    add_to_responses(text_body, datetime.now(tz=pacific).replace(tzinfo=None), user_id, last_text_id)


@app.route('/pie-chart.json')
def calculate_mw_percentage():
    """Return percentage of the time a user mindwanders as JSON."""
    responses = get_all_responses()
    pie_data = get_pie_data(responses)
    return jsonify(pie_data)


@app.route('/mw_graph_data.json')
def plot_mw_happiness():
    """Return plot points for happiness while mindwandering graph as JSON."""
    responses = get_all_responses()
    mw_graph_data = get_mw_graph_data(responses)
    return jsonify(mw_graph_data)


@app.route('/not_mw_graph_data.json')
def plot_not_mw_happiness():
    """Return plot points for happiness while not mindwandering graph as JSON."""
    responses = get_all_responses()
    not_mw_graph_data = get_not_mw_graph_data(responses)
    return jsonify(not_mw_graph_data)


if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)
    app.run(host="0.0.0.0")