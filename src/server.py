"""from flask_debugtoolbar import DebugToolbarExtension"""
# import flask libraries
from flask import Flask, flash, session
from flask import request, render_template, redirect
# import objects and classes from model.py
from model import connect_to_db, db, User, TimeWindow, AppText, Response
from send_texts import send_welcome_text
from datetime import datetime
# from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
app.secret_key = 'KEY'


@app.route('/')
def display_homepage():
    """Display homepage to user."""

    # check if user is logged in
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

    # instantiate an instance of User
    user = User(fname=fname, 
                lname=lname, 
                email=email, 
                password=password, 
                mobile=mobile)

    # add user to db
    db.session.add(user)
    db.session.commit()

    flash('Wanda welcomes you! Please set up your preferences.')

    # add user's first name and user_id to session
    session['fname'] = fname
    session['user_id'] = user.id
    
    # send confirmation text to user's mobile using Twilio
    send_welcome_text(mobile)

    return redirect('/preferences') # edit redirect to profile page


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


@app.route('/preferences')
def show_preferences():
    """Shows user's current preferences and gives option to update."""

    return render_template("preferences.html",
                            fname=session['fname'])


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
    for window in time_windows:
        time_window = TimeWindow(start_time=window[0],
                                 end_time=window[1],
                                 day_of_week=window[2],
                                 user_id=session['user_id'])

        # add time_window to database
        db.session.add(time_window)

    db.session.commit()

    flash('Your time window preferences have been successfully updated!')

    return redirect('/')


# this is an example from Twilio of how to respond to a user text
# @app.route("/sms", methods=['GET', 'POST'])
# def incoming_sms():
#     """Gets user's responses to app's texts."""

#     # Get the message the user sent our Twilio number
#     body = request.values.get('Body', None)

#     # instantiate instance of Response class
#     text = Response(response=body,
#                     response_type=,
#                     timestamp=datetime.now(),
#                     user_id=session['user_id'],
#                     text_id=)

#     db.session.add(text)
#     db.session.commit()




################################################################################


if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)
    app.run(host="0.0.0.0")






























