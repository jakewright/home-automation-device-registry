import shelve
from flask_restful import Resource, reqparse

data_store = 'devices'


class DeviceList(Resource):

    def get(self):
        shelf = shelve.open(data_store)
        keys = list(shelf.keys())
        return keys, 200

    def post(self):
        shelf = shelve.open(data_store)

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

        shelf[identifier] = data

        return identifier, 201


class Device(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('identifier')
        self.parser.add_argument('name')
        self.parser.add_argument('device-type')
        self.parser.add_argument('controller-gateway')

    def post(self):
        shelf = shelve.open('devices')
        args = self.parser.parse_args()

        data = {
            'name': args['name'],
            'deviceType': args['device-type'],
            'controllerGateway': args['controller-gateway']
        }

        identifier = args['identifier']

        shelf[identifier] = data
        return '', 201
