import requests_mock
from app import app

def add_device(identifier, name, device_type, controller_gateway):
    """Helper function to post a new device to the registry and return the response."""

    # Create a test client
    with app.test_client() as c:

        # Mock the request module
        with requests_mock.Mocker() as m:

            # Mock the response of the request
            m.get(controller_gateway + '/device/' + identifier + '/ping', text="pong")

            return c.post('/devices', data={
                'identifier': identifier,
                'name': name,
                'device-type': device_type,
                'controller-gateway': controller_gateway
            })
