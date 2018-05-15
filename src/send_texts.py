
# download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
from model import connect_to_db, db, AppText
from datetime import datetime
from flask import Flask
import pytz

import os
# my Account Sid and Auth Token from twilio.com/console
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])


def send_welcome_text(mobile):
    """Sends user welcome text message."""

    client.messages.create(body="Wanda warmly welcomes you!",
                           from_="+14159156178",
                           to=mobile)


def send_survey(mobile, user_id):
    """Sends user message with 3 survey questions."""

    text = ("Hi there! This is your Wanda check in. " 
            "Please respond to these 3 questions with 3 integers, separated by commas."
            "\n\n1. Was your mind wandering right before this text?"
            "\n2. What activity were you doing?"
            "\n3. On a scale of 1 to 10, how are you feeling?")

    client.messages.create(body=text,
                           from_="+14159156178",
                           to=mobile)

    pacific = pytz.timezone('US/Pacific')
    text = AppText(sent_time=datetime.now(tz=pacific).replace(tzinfo=None),
                   user_id=user_id)

    db.session.add(text)
    db.session.commit()


def send_reminder(mobile):
    """Sends user reminder to reply to survey text."""

    text = ("Psst, Wanda here! Gentle reminder to reply to my last message.")
    
    client.messages.create(body=text,
                           from_="+14159156178",
                           to=mobile)  


# this is an example from Twilio of how to respond to a user text
from twilio.twiml.messaging_response import MessagingResponse
def sms_ahoy_reply():
    """Respond to incoming messages with a friendly SMS."""

    # binding resp to the class MessagingResponse()
    resp = MessagingResponse() 

    # give text to message attribute of resp
    resp.message("Ahoy! Thanks so much for your message.")

    return str(resp)


################################################################################


if __name__ == '__main__':
    app = Flask(__name__)
    connect_to_db(app)

