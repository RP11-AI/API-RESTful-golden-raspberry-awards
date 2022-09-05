from flask_restx import Api, Resource, reqparse
from src.server.instance import server
from src.models.data_awards_model import input_data, input_data_put, input_delete
from src.data.data_processing import Clustering
from src.data.data_change_request import RequestCSV
import json

with open('src\\config\\config.json', 'r') as f:
    config = json.load(f)
app, api = server.app, server.api


@api.route('/awards')
class Awards(Resource):
    # Decorate a view function to register it with the given URL rule and options. Calls :meth:`add_url_rule`, which has
    # more details about the implementation.
    @staticmethod
    def get():
        return Clustering().list_2_json()


@api.route('/csv')
class CSV(Resource):
    # Decorate a view function to register it with the given URL rule and options. Calls :meth:`add_url_rule`, which has
    # more details about the implementation.
    @staticmethod
    def get():
        return RequestCSV().csv_2_list(), 200

    @api.expect(input_data, validate=True)
    @api.marshal_with(input_data)
    def post(self):
        response = api.payload  # PAYLOAD
        # handling of user response to avoid database input errors ----------------------------------------------------#
        info = None
        if type(response['year']) != int:
            info = '<p>The year entered must be valid</p>'
        else:
            df = ['title', 'studios', 'producers', 'winner']
            for i in df:
                if type(response[i]) != str:
                    info = '<p>Insert only a string into the variable</p>'
                elif config['delimiter'] in response[i]:
                    info = '<p>semicolon in string is not accepted</p>'
        # -------------------------------------------------------------------------------------------------------------#
        if info is None:
            # Action request in the database
            RequestCSV().csv_post(response['year'],
                                  response['title'],
                                  response['studios'],
                                  response['producers'],
                                  response['winner'])
            return response, 201
        else:
            return response, 400

    @api.expect(input_data_put, validate=True)
    @api.marshal_with(input_data_put)
    def put(self):
        response = api.payload  # PAYLOAD
        # handling of user response to avoid database input errors ----------------------------------------------------#
        info = None
        if type(response['id']) != int:
            info = '<p>the id entered must be valid</p>'
        else:
            if not response['year'].isdigit() and response['year'] != "NONE":
                info = '<p>the year entered must be valid</p>'
            else:
                df = ['title', 'studios', 'producers', 'winner']
                for i in df:
                    if type(response[i]) != str:
                        info = '<p>Insert only a string into the variable</p>'
                    elif config['delimiter'] in response[i]:
                        info = '<p>semicolon in string is not accepted</p>'
            # ---------------------------------------------------------------------------------------------------------#

        if info is None:
            # Action request in the database
            RequestCSV().csv_put(response['id'],
                                 response['year'],
                                 response['title'],
                                 response['studios'],
                                 response['producers'],
                                 response['winner'])
            return response, 202
        else:
            return response, 400

    @api.expect(input_delete, validate=True)
    @api.marshal_with(input_delete)
    def delete(self):
        response = api.payload  # PAYLOAD
        # handling of user response to avoid database input errors ----------------------------------------------------#
        if type(response['id']) != int:
            return response, 400
        else:
            # Action request in the database
            RequestCSV().csv_delete(response['id'])
            return response, 202
        # -------------------------------------------------------------------------------------------------------------#
