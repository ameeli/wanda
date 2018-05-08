from flask import Flask, request, session, render_template
from twilio.twiml.messaging_response import MessagingResponse
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from account_verification_flask.config import config_env_files
# from flask_debugtoolbar import DebugToolbarExtension
# from model import connect_to_db
# from model import *

app = Flask(__name__)
app.secret_key = 'KEY'


@app.route('/')
def hello():
    """Renders homepage.html."""
    return "Hello world!"


@app.route('/home')
def display_homepage():
    """Display homepage."""

    return render_template("homepage.html")


@app.route('/signin')
def show_signin_form():
    """Shows signin page."""

    return render_template("signin_form.html")


@app.route('/signup')
def show_signup_form():
    """Shows signup form."""

    return render_template("signup_form.html")


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

    # connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")