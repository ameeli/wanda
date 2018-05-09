# import flask libraries
from flask import Flask, flash, session
from flask import request, render_template, redirect
# from flask_debugtoolbar import DebugToolbarExtension

# download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

# import objects and classes from model.py
from model import connect_to_db, db, User

import os
# my Account Sid and Auth Token from twilio.com/console
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])

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
        session['user_id'] = user.user_id

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




# this route is an example from Twilio of how to respond to a user text
@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    """Respond to incoming messages with a friendly SMS."""
    # Start our response

    # binding resp to the class MessagingResponse()
    resp = MessagingResponse() 

    # give text to message attribute of resp
    resp.message("Ahoy! Thanks so much for your message.")

    return str(resp)


def send_welcome_text(mobile):
    """Sends user welcome text message."""

    client.messages.create(body="Wanda warmly welcomes you!",
                           from_="+14159156178",
                           to=mobile)


if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")