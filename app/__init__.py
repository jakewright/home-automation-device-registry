# Import the framework
from flask import Flask
from flask_restful import Resource, Api, reqparse
import shelve

# Create the application with the instance config option on
app = Flask(__name__, instance_relative_config=True)

# Load the default configuration
app.config.from_object('config.default')

# Load the file specified by the APP_CONFIG_FILE environment variable
# Variables defined here will override those in the default configuration
app.config.from_envvar('APP_CONFIG_FILE')

# Create the API
api = Api(app)


class DeviceList(Resource):
    def get(self):
        shelf = shelve.open(app.config['DATABASE'])
        keys = list(shelf.keys())

        if not keys:
            message = 'No devices'
            code = 204
        else:
            message = 'Devices found'
            code = 200

        return {'message': message, 'value': keys}, code

    def post(self):
        shelf = shelve.open(app.config['DATABASE'])

        parser = reqparse.RequestParser()
        parser.add_argument('identifier')
        parser.add_argument('name')
        parser.add_argument('device-type')
        parser.add_argument('controller-gateway')

        args = parser.parse_args()

        data = {
            'name': args['name'],
            'deviceType': args['device-type'],
            'controllerGateway': args['controller-gateway']
        }

        identifier = args['identifier']

        # If the identifier already exists in the database
        if (identifier in shelf):
            message = 'Identifier already exists'
            code = 409
        else:
            shelf[identifier] = data
            message = 'Device registered'
            code = 201

        return {'message': message, 'value': identifier}, code


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


api.add_resource(DeviceList, '/devices')
api.add_resource(Device, '/device/<string:identifier>')
