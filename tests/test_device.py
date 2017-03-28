import unittest
import os
from app import app
import json
from tests import add_device

class TestDevice(unittest.TestCase):

    def setUp(self):
        # Create an instance of the test client
        self.app = app.test_client()

        # Use a temporary file as the database file
        app.config['DATABASE'] = '/tmp/test'

    def tearDown(self):
        # Delete the temporary file
        os.unlink(app.config['DATABASE'] + '.db')

    def test_get_invalid_device(self):
        """Test that getting an invalid device's details will return a 404"""

        # This test will have a new database with no device 1 in it
        response = self.app.get('/device/1')

        # Assert that we get 404 not found
        self.assertEqual(404, response.status_code)

    def test_list_device(self):
        """Test that adding and then getting a device works"""

        # Create a list representing a device
        test_device = {
            'identifier': 'test',
            'name': 'Test',
            'device-type': 'switch',
            'controller-gateway': 'http://gateway'
        }

        # Add the device to the registry
        add_device(test_device['identifier'],
                        test_device['name'],
                        test_device['device-type'],
                        test_device['controller-gateway'])

        # Ask the registry for the device's details
        response = self.app.get('/device/test')

        # Assert that we got an OK response code
        self.assertEqual(200, response.status_code)

        # Decode the json
        decoded_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(test_device, decoded_response['value'])

    def test_delete_device(self):
        """Test that a device is no longer available after deleting it"""

        # Add a device
        add_device('test-del', 'test', 'test', 'http://test')

        # Try to get the device
        response = self.app.get('/device/test-del')
        self.assertEqual(200, response.status_code)

        # Delete the device
        response = self.app.delete('/device/test-del')
        self.assertEqual(200, response.status_code)

        # Try to get the device again
        response = self.app.get('/device/test-del')
        self.assertEqual(404, response.status_code)

    # def add_device(self, identifier, name, device_type, controller_gateway):
    #     """Helper function to post a new device to the registry and return the response."""

    #     return self.app.post('/devices', data={
    #         'identifier': identifier,
    #         'name': name,
    #         'device-type': device_type,
    #         'controller-gateway': controller_gateway
    #     })
