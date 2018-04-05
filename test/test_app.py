import unittest
from data import User, user_data
from app.views import app


class TestUser(unittest.TestCase):

    def setUp(self):
        app.testing = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app
        self.client = app.test_client()
        self.michael = User('Michael', 'Johnson', 'user_1@example.com', 'password2018')
        self.johndoe = User('john', 'Doe', 'user_2@example.com', 'password2018')

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

    def test_user_registration_successful(self):
        """test for successful registration"""
        self.assertTrue(user_data[hash('user_1@example.com')]['Email'], 'user_1@gmail.com')

    def test_user_password_hash(self):
        """test if user password is encrypt"""
        self.assertNotEqual(user_data[hash('user_1@example.com')]['Password'], 'password218')

    def test_user_added(self):
        """test if user is added"""
        self.assertIsInstance(self.michael, User, False)



