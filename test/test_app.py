import unittest
from data import User
from app.views import app


class TestUser(unittest.TestCase):

    def setUp(self):
        app.testing = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app
        app.michael = User('Michael', 'Johnson', 'user_1@gmail.com', 'password2018')

    def test_application_running(self):
        """ensures that flask was setup correctly"""
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_logging_running(self):
        """ensures that flask was setup correctly"""
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue(b'PLEASE LOGIN' in response.data)