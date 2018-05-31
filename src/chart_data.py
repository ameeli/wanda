from flask import Flask
from model import connect_to_db, db, Response

def get_all_responses():
    """Queries db to get response column of all responses."""
    responses = db.session.query(Response.response).all()

    return responses


def get_pie_data(responses):
    """Takes all responses and formats into dictionary."""
    wandering_counter = 0
    not_wandering_counter = 0

    for response in responses:
        mind_wandering_response = int(response[0][0])
        if mind_wandering_response == 1:
            wandering_counter +=1
        else:
            not_wandering_counter += 1

    pie_data = [{
                 'mw': 'Wandering',
                 'occurrence': wandering_counter
                },
                {
                 'mw': 'Focusing',
                 'occurrence': not_wandering_counter
                }]
    
    return pie_data


def get_mw_graph_data(responses):
    """Takes responses and creates frequency counter for every happiness level
    while mind wandering."""
    happiness_frequency = {}
    mw_graph_data = []

    for i in range(1, 11):
        happiness_frequency[i] = 0

    for response in responses:
        happiness_level = int(response[0][3])
        happiness_frequency[happiness_level] += 1

    for key in happiness_frequency:
        formatted_data = {'happiness': key, 'frequency': happiness_frequency[key]}
        mw_graph_data.append(formatted_data)

    return mw_graph_data


def get_not_mw_graph_data(responses):
    """Takes responses and creates frequency counter for every happiness level
    while not mind wandering."""
    happiness_frequency = {}
    not_mw_graph_data = []

    for i in range(1, 11):
        happiness_frequency[i] = 0

    for response in responses:
        happiness_level = int(response[0][3])
        happiness_frequency[happiness_level] += 1

    for key in happiness_frequency:
        formatted_data = {'happiness': key, 'frequency': happiness_frequency[key]}
        not_mw_graph_data.append(formatted_data)

    return not_mw_graph_data


if __name__ == '__main__':
    app = Flask(__name__)
    connect_to_db(app)

