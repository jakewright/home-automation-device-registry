import markdown
import shelve
import sys

# Import the framework
from flask import Flask
from flask import Markup
from flask import render_template
from flask_restful import Resource, Api, reqparse


# Create the application with the instance config option on
app = Flask(__name__, instance_relative_config=True)

# Load the default configuration
app.config.from_object('config.default')

# Load the file specified by the APP_CONFIG_FILE environment variable
# Variables defined here will override those in the default configuration
app.config.from_envvar('APP_CONFIG_FILE')

# Create the API
api = Api(app)


@app.route("/", methods=['GET'])
def index():
    """Present some documentation"""
    # Open the README file
    with open('/usr/src/app/README.md', 'r') as markdown_file:
        # Read the markdown contents
        content = markdown_file.read()

        # Convert the markdown to HTML and then treat it as actual HTML so it's not escaped
        html = Markup(markdown.markdown(content, extensions=['markdown.extensions.fenced_code']))

    return render_template('index.html', content=html)


class DeviceList(Resource):
    def get(self):
        shelf = shelve.open(app.config['DATABASE'])
        keys = list(shelf.keys())

        if not keys:
            message = 'No devices'
            code = 204
        else:
            message = 'Success'
            code = 200

        devices = []

        for key in keys:
            devices.append(shelf[key])

        return {'message': message, 'value': devices}, code

    def post(self):
        shelf = shelve.open(app.config['DATABASE'])

        parser = reqparse.RequestParser()

        parser.add_argument('identifier')
        parser.add_argument('name')
        parser.add_argument('device-type')
        parser.add_argument('controller-gateway')

        args = parser.parse_args()

        identifier = args['identifier']

        # If the identifier already exists in the database
        if identifier in shelf:
            return {'message': 'Identifier already exists', 'value': identifier}, 409

        shelf[identifier] = args
        print('Registered device: ' + args['identifier'], file=sys.stderr)
        return {'message': 'Device registered', 'value': identifier}, 201


class Device(Resource):
    def get(self, identifier: str):

        # Open the database
        shelf = shelve.open(app.config['DATABASE'])

        # If the key does not exist in the database
        if not(identifier in shelf):
            message = 'Device not found'
            code = 404
            device = {}
        else:
            # Get the data with the given key
            message = 'Device found'
            code = 200
            device = shelf[identifier]

        return {'message': message, 'value': device}, code

    def delete(self, identifier: str):

        # Open the database
        shelf = shelve.open(app.config['DATABASE'])

        # If the key does not exist in the database
        if not (identifier in shelf):
            message = 'Device not found'
            code = 400
        else:
            del shelf[identifier]
            message = 'Device deleted'
            code = 200

        return {'message': message, 'value': True}, code


api.add_resource(DeviceList, '/devices')
api.add_resource(Device, '/device/<string:identifier>')
