from model import db, TimeWindow, AppText
from flask import Flask
from datetime import datetime
from sqlalchemy import func


def get_time_windows():
    """Queries time_windows and organizes results by day of the week."""

    # query for all time windows in db
    all_time_windows = db.session.query(
        TimeWindow.user_id, 
        TimeWindow.start_time, 
        TimeWindow.end_time,
    ) 

    # get today's datetime
    today = datetime.now()
    # get number from 0-6 representing day of week 
    # add 1 to match integer column in time_windows table 
    day_of_week = datetime.weekday(today) + 1

    today = all_time_windows.filter(
        TimeWindow.day_of_week==day_of_week
    ).all()

    return today # list of time windows for all users for today


def get_last_sent_text(user_id):

    last_text = db.session.query(
        func.max(AppText.sent_time)
    ).filter(
        user_id==user_id
    ).first()

    


################################################################################


def connect_to_db(app):
    """Connect the database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///project'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == '__main__':
    app = Flask(__name__)
    connect_to_db(app)

    print "Connected to DB."


