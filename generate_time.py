from model import db, TimeWindow
from flask import Flask
from datetime import datetime

def get_time_windows():
    """Queries time_windows and organizes results by day of the week."""

    # query for all time windows in db
    all_time_windows = db.session.query(TimeWindow.day_of_week, 
                                        TimeWindow.user_id, 
                                        TimeWindow.start_time, 
                                        TimeWindow.end_time) 

    # get all time windows by day of the week as a list of tuples
    # (user_id, start_time as a datetime, end_time as a datetime)
    monday = all_time_windows.filter(TimeWindow.day_of_week==1).all()
    tuesday = all_time_windows.filter(TimeWindow.day_of_week==2).all()
    wednesday = all_time_windows.filter(TimeWindow.day_of_week==3).all()
    thursday = all_time_windows.filter(TimeWindow.day_of_week==4).all()
    friday = all_time_windows.filter(TimeWindow.day_of_week==5).all()
    saturday = all_time_windows.filter(TimeWindow.day_of_week==6).all()
    sunday = all_time_windows.filter(TimeWindow.day_of_week==7).all()

    return monday, tuesday, wednesday, thursday, friday, saturday, sunday


def generate_random_times(windows):
    """Takes return of get_time_windows and generates random times."""

    # get today's datetime
    today = datetime.now()
    # get number from 0-6 representing day of week 
    # add 1 to match integer column in time_windows table 
    day_of_week = datetime.weekday(today) + 1

    # windows right now is tuple of list of tuples
    # per convo w/ Karynn, calculate minutes betweeen each user's window 
    # divide the minutes by the number of texts you will send the user each day
    # and generate random numbers from 0 to (minutes between windows)/frequency




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


























