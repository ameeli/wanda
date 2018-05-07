from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    """User of wellness website."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(64))
    lname = db.Column(db.String(64))
    email = db.Column(db.String(64))
    password = db.Column(db.String(64))
    phone = db.Column(db.String(12))
    timezone = db.Column(db.String(64))

    time_windows = db.relationship('TimeWindow')
    texts =  db.relationship('AppText')
    responses = db.relationship('Response')


class TimeWindow(db.Model):
    """User's time window preference."""

    __tablename__ = 'time_windows'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    day_of_week = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Response(db.Model):
    """Each response from user."""

    __tablename__ = 'responses'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    response = db.Column(db.Text())
    response_type = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    text_id = db.Column(db.Integer, db.ForeignKey('texts.id'))

    text = db.relationship('AppText')


class AppText(db.Model):
    """Text that app sends to user."""

    __tablename__ = 'texts'
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sent_time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    responses = db.relationship('Response')


def connect_to_db(app):
    """Connect the database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///project'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    db.create_all()

    print "Connected to DB."





















