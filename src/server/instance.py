from flask import Flask
from flask_restx import Api

# ---------------------------------------------------------------------------------------------------------------------#
# Server startup and other specifications.
# ---------------------------------------------------------------------------------------------------------------------#


class Server:
    def __init__(self, ) -> None:
        self.app = Flask(__name__)
        self.api = Api(
            self.app,
            version='1.0',
            title='API RESTful - Golden Raspberry Awards',
            description='Reading and processing of data from the csv file '
                        'referring to the nominees and winners of the '
                        'Golden Raspberry Awards',
            contact_email='romulopauliv@bk.ru',
            default_mediatype="application/json",
            doc='/'
        )

    def run(self):
        # If the RESTful API is deployed, it is necessary to disable debug mode!
        self.app.run(debug=True)


server = Server()
