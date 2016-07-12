# Import the framework
from flask import Flask
from flask_restful import Resource, Api

# Create the application with the instance config option on
app = Flask(__name__, instance_relative_config=True)

# Load the default configuration
app.config.from_object('config.default')

# Load the file specified by the APP_CONFIG_FILE environment variable
# Variables defined here will override those in the default configuration
app.config.from_envvar('APP_CONFIG_FILE')

# Create the API
api = Api(app)


class Devices(Resource):
    def get(self):
        return {"devices": [
            {
                "identifier": "bulb1",
                "deviceType": 'bulb',
                "name": "Coffee table lamp",
                "controllerGateway": "192.168.0.52"
            },
            {
                "identifier": "monitor",
                "deviceType": 'plug',
                "name": "Dell U2410",
                "controllerGateway": "192.168.0.52"
            },
        ]}

api.add_resource(Devices, '/devices')


class Device(Resource):
    def get(self, identifier: str):
        return {
            "identifier": identifier,
            "deviceType": 'plug',
            "name": "Dell U2410",
            "controllerGateway": "192.168.0.52"
        }

api.add_resource(Device, '/device/<string:identifier>')
