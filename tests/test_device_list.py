from app import app
import os
import unittest
from tests import add_device

class TestDeviceList(unittest.TestCase):

    def setUp(self):
        # Create an instance of the test client
        self.app = app.test_client()

        # Use a temporary file as the database file
        app.config['DATABASE'] = '/tmp/test'

    def tearDown(self):
        # Delete the temporary file
        os.unlink(app.config['DATABASE'] + '.db')

    def test_no_devices(self):
        """Test that the correct response code is given when there are no devices known by the registry."""

        # Make a get request to /devices
        response = self.app.get('/devices')

        # Assert that the response code is correct for no data
        self.assertEqual(204, response.status_code)

    def test_add_device(self):
        """Test that a new device can be added to the registry."""

        # Add a new device and get the response
        response = add_device(
            'device1',
            'device 1',
            'switch',
            'http://192.168.0.1'
        )

        # Assert that the response code is 201
        self.assertEqual(201, response.status_code)

        # Assert that the device identifier is returned in the response
        self.assertIn(b'registered', response.data)
        self.assertIn(b'device1', response.data)

    def test_add_duplicate_device(self):
        """Test that adding a device with an identifier that is already used returns an error"""

        # Add the same device twice
        add_device('device1', 'device 1', 'switch', 'http://192')
        response = add_device('device1', 'device 1', 'switch', 'http://192')

        # Assert that we get a 409 conflict response code
        self.assertEqual(409, response.status_code)

    # def add_device(self, identifier, name, device_type, controller_gateway):
    #     """Helper function to post a new device to the registry and return the response."""

    #     # Mock the request module
    #     with requests_mock.Mocker() as m:

    #         # Mock the response of the request
    #         m.get(controller_gateway + '/device/' + identifier + '/ping', text="pong")

    #         return self.app.post('/devices', data={
    #             'identifier': identifier,
    #             'name': name,
    #             'device-type': device_type,
    #             'controller-gateway': controller_gateway
    #         })

