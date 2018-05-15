from model import connect_to_db, db, User, TimeWindow, AppText
from flask import Flask
from datetime import datetime
from sqlalchemy import func
from random import randint
from send_texts import send_survey
from time import sleep
import pytz
pacific = pytz.timezone('US/Pacific')

def get_time_windows():
    """Queries time_windows and returns list of time windows for all users today."""

    # query for all time windows in db
    all_time_windows = db.session.query(
        TimeWindow.user_id, 
        TimeWindow.start_time, 
        TimeWindow.end_time,
    ) 

    today = datetime.now(tz=pacific)
    # get number from 0-6 representing day of week 
    # add 1 to match integer column in time_windows table 
    day_of_week = datetime.weekday(today) + 1

    windows_today = all_time_windows.filter(
        TimeWindow.day_of_week==day_of_week
    ).all()

    return windows_today


def get_seconds_since_last_text(user_id):
    """Takes user_id and returns seconds since user's last received text."""

    last_text_time = db.session.query(
        func.max(AppText.sent_time)
    ).filter(
        user_id==user_id
    ).first()

    timedelta = datetime.now(tz=pacific) - last_text_time[0].replace(tzinfo=pacific)
    # datetime.timedelta(days, seconds, microseconds)

    seconds_since_last_text = (timedelta.days * 86400) + timedelta.seconds

    return seconds_since_last_text


def send_text(windows):
    """Sends survey to user based on the time elapsed since last text."""

    for window in windows:
        user_id = window[0]
        start_time = window[1]
        stop_time = window[2]
        now = datetime.now(tz=pacific)

        # check that the current time is within a user's time window
        if now.hour > start_time.hour and now.hour < stop_time.hour:
            seconds_since_last_text = get_seconds_since_last_text(user_id)
            mobile = User.query.filter(User.id==user_id).one().mobile

            # if it's been more than an hour since the last text, send another
            # randomly, 1 in 10 chance 
            if seconds_since_last_text > 3600:
                number = randint(1, 10)

                if number == 10:
                    send_survey(mobile, user_id)


################################################################################


if __name__ == '__main__':
    app = Flask(__name__)
    connect_to_db(app)

    while True:
        windows = get_time_windows()
        send_text(windows)
        sleep(120)

