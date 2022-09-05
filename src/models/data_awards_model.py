from flask_restx import fields
from src.server.instance import server

# ---------------------------------------------------------------------------------------------------------------------#
# Registration of API endpoint templates.
# ---------------------------------------------------------------------------------------------------------------------#

input_data = server.api.model('POST', {
    'year': fields.Integer(title='Award Nomination Year',
                           description='Year the film was nominated for a Golden Raspberry Award',
                           required=True,
                           example='2017'),
    'title': fields.String(title='Movie Name',
                           description='Full movie name',
                           required=False,
                           example='Dunkirk'),
    'studios': fields.String(title='Studio',
                             description='Studio that produced the film',
                             required=False,
                             example='Syncopy, Warner Bros. and Dombey Street Productions'),
    'producers': fields.String(title='Film Producers',
                               description='Full name of producers. It must be separated by commas or "and"',
                               required=True,
                               example='Chistopher Nolan and Emma Thomas'),
    'winner': fields.String(title='Winners',
                            description='Whether the movie was the movie winner or not. Complete with "yes" '
                                        'or an empty string ""',
                            example='yes',
                            required=True)
})
input_data_put = server.api.model('PUT', {
    'id': fields.Integer(title='Index ID',
                         description='Update data ID',
                         required=True,
                         example=0),

    'year': fields.String(title='Award Nomination Year',
                          description='Year the film was nominated for a Golden Raspberry Award\n'
                                      'keeping NONE the data will not be updated',
                          required=False,
                          example='NONE'),

    'title': fields.String(title='Movie Name',
                           description='Full movie name\n'
                                       'keeping NONE the data will not be updated',
                           required=False,
                           example='NONE'),

    'studios': fields.String(title='Studio',
                             description='Studio that produced the film\n'
                                         'keeping NONE the data will not be updated',
                             required=False,
                             example='NONE'),

    'producers': fields.String(title='Film Producers',
                               description='Full name of producers. It must be separated by commas or "and"\n'
                                           'keeping NONE the data will not be updated',
                               required=False,
                               example='NONE'),

    'winner': fields.String(title='Winners',
                            description='Whether the movie was the movie winner or not. Complete with "yes" '
                                        'or an empty string ""\n'
                                        'keeping NONE the data will not be updated',
                            example='NONE',
                            required=False)
})

input_delete = server.api.model('DELETE', {
    'id': fields.Integer(title='DELETE ID',
                         description='ID of the row to be deleted.',
                         example=0,
                         required=True)
})
