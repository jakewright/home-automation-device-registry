from app import app
import unittest
import tempfile
import os


class TestRegister(unittest.TestCase):

    def setUp(self):
        # Create an instance of the test client
        self.app = app.test_client()

        # Create a temporary file to use as a database and keep a local file descriptor
        self.database_fd, app.config['DATABASE'] = tempfile.mkstemp()

    def tearDown(self):
        # Use the local reference to close the file descriptor
        os.close(self.database_fd)

        # Delete the temporary file
        os.unlink(app.config['DATABASE'])

    def test_register(self):
        # Make a get request to /devices
        response = self.app.get('/devices')

        # Assert that no devices were returned
        assert b'something' in response.data
