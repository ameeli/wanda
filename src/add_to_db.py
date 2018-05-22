from model import connect_to_db, db, User, TimeWindow, Text, Response
from flask import Flask

def add_to_users(fname, lname, email, password, mobile):
    """Adds new user to users table and returns user id."""

    # instantiate an instance of User
    user = User(fname=fname, 
                lname=lname, 
                email=email, 
                password=password, 
                mobile=mobile)

    db.session.add(user)
    db.session.commit()

    return user.id


def add_to_time_windows(start_time, end_time, day_of_week, user_id):
    """Adds a user's window preferences to time windows table."""

    time_window = TimeWindow(start_time=start_time,
                             end_time=end_time,
                             day_of_week=day_of_week,
                             user_id=user_id)

    db.session.add(time_window)
    db.session.commit()


def add_to_responses(response, timestamp, user_id, text_id):
    """Adds response associated with text to responses table."""

    response = Response(response=response,
                        timestamp=timestamp,
                        user_id=user_id,
                        text_id=text_id)

    db.session.add(response)
    db.session.commit()


if __name__ == "__main__":
    app = Flask(__name__)
    connect_to_db(app)