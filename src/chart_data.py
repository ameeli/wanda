from flask import Flask
from model import connect_to_db, db, User, TimeWindow, Text, Response

def get_all_responses():
    """Queries db to get response column of all responses."""

    response = db.session.query(Response.response).all()

    return response


def get_pie_data(responses):
    """Takes all responses and formats into dictionary."""

    wandering_counter = 0
    not_wandering_counter = 0

    for response in responses:
        if int(response[0][0]) == 1:
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


mw_graph_data = [{
                  'letter': '1',
                  'frequency': 0.0
                 },

                 {
                  'letter': '2',
                  'frequency': 0.0
                 },

                 {
                  'letter': '3',
                  'frequency': 0.04
                 },

                 {
                  'letter': '4',
                  'frequency': 0.04
                 },

                 {
                  'letter': '5',
                  'frequency': 0.16
                 },
                
                 {
                  'letter': '6',
                  'frequency': 0.42
                 },

                 {
                  'letter': '7',
                  'frequency': 0.26
                 },

                 {
                  'letter': '8',
                  'frequency': 0.06
                 },

                 {
                  'letter': '9',
                  'frequency': 0.02
                 },

                 {
                  'letter': '10',
                  'frequency': 0.0
                 }]

not_mw_graph_data = [{
                  'letter': '1',
                  'frequency': 0.0
                 },

                 {
                  'letter': '2',
                  'frequency': 0.016
                 },

                 {
                  'letter': '3',
                  'frequency': 0.0
                 },

                 {
                  'letter': '4',
                  'frequency': 0.016
                 },

                 {
                  'letter': '5',
                  'frequency': 0.096
                 },
                
                 {
                  'letter': '6',
                  'frequency': 0.258
                 },

                 {
                  'letter': '7',
                  'frequency': 0.290
                 },

                 {
                  'letter': '8',
                  'frequency': 0.226
                 },

                 {
                  'letter': '9',
                  'frequency': 0.080
                 },

                 {
                  'letter': '10',
                  'frequency': 0.016
                 }]

if __name__ == '__main__':
    app = Flask(__name__)
    connect_to_db(app)

