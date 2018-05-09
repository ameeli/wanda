from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()


class User(db.Model):
    """User of wellness website."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(64))
    lname = db.Column(db.String(64))
    email = db.Column(db.String(64))
    password = db.Column(db.String(64))
    mobile = db.Column(db.String(12))

    time_windows = db.relationship('TimeWindow')
    texts =  db.relationship('AppText')
    responses = db.relationship('Response')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return '<id={} name={} {} email={} mobile={}>'\
                .format(self.id, self.fname, self.lname, self.email, self.mobile)


class TimeWindow(db.Model):
    """User's time window preference."""

    __tablename__ = 'time_windows'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    day_of_week = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return '<id={} start_time={} end_time={} day_of_week={} user_id={}'\
                .format(self.id, self.start_time, self.end_time, self.day_of_week, 
                self.user_id)


class AppText(db.Model):
    """Text that app sends to user."""

    __tablename__ = 'texts'
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sent_time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    responses = db.relationship('Response')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return '<id={} sent_time={} user_id={}>'\
                .format(self.id. self.sent_time, self.user_id)


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

    def __repr__(self):
        """Provide helpful representation when printed."""

        return '<id={} response={} response_type={} timestamp={} user_id={} text_id={}>'\
                .format(self.id, self.response, self.response_type, self.timestamp,
                self.user_id, self.text_id)


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
    db.create_all()

    print "Connected to DB."





















