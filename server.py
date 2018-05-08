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
    """Display homepage."""

    return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def show_signup_form():
    """Shows signup form."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def add_user():
    """Adds new user to database."""

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

    flash("Wanda welcomes you!")

    # send confirmation text to user's mobile using Twilio
    client.messages.create(body="Wanda warmly welcomes you!",
                           from_="+14159156178",
                           to=mobile)

    return redirect('/home') # edit redirect to profile page


@app.route('/login', methods=['GET'])
def show_login_form():
    """Shows signin page."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_user():
    """Logs user into app."""

    email = request.form['email']
    password = request.form['password']

    user = User.query.filter(User.email==email).one()

    if user and user.password == password:
        return redirect('/home') # edit redirect to profile page

    else:
        flash('Your email or password was incorrect. Please try again.')
        return redirect('/login')


@app.route('/home')
def hello():
    """Renders homepage.html."""
    return "Hello world!"


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


if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")