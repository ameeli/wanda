from datetime import datetime
from random import randint

from model import Text, Response, connect_to_db, db
from server import app
from responses import combined_pairs


text_times = ['text']
response_times = ['response']


def load_texts():
    """Loads texts into db."""

    i = 0
    while i < 112:
        day = randint(1, 30)
        hour = randint(8, 19)
        minute = randint(0, 54)
        second = randint(0, 59)

        text = Text(sent_time=datetime(
                    2018, 4, day, hour, minute, second, 670712),
                    user_id=1)

        db.session.add(text)
        text_times.append(datetime(2018, 4, day, hour, minute, second, 670712))
        response_times.append(datetime(2018, 4, day, hour, minute + 5, second, 670712))
        i += 1

    db.session.commit()


def load_responses(combined_pairs):
    """Loads responses into db."""

    i = 1
    for pair in combined_pairs:
        response = Response(response=pair,
                            timestamp=response_times[i],
                            user_id=1,
                            text_id=i)

        db.session.add(response)
         
        response_times[i], i
        i += 1

    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_texts()
    load_responses(combined_pairs)