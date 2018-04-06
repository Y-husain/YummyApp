import unittest
from data import User, user_data, Categories, category_data, Recipes, recipe_data
from flask_testing import TestCase
from app.views import app


class TestUser(unittest.TestCase):

    def setUp(self):
        app.testing = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app
        self.client = app.test_client()
        self.michael = User('Michael', 'Johnson', 'user_1@example.com', 'password2018')

    def tearDown(self):
        user_data.clear()

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

    def test_category_created(self):
        """test if category is created"""
        Categories('user_email', 'HealthyFood')
        self.assertIn(hash('user_email'), category_data)
        self.assertIn('HealthyFood', category_data[hash('user_email')][0])

    def test_recipe_category_created(self):
        """test if recipe created in category"""
        Categories('user_email', 'HealthyFood')
        category_name = category_data[hash('user_email')].index('HealthyFood')
        Recipes('Fruits', 'blah blah blah heat...Eat fruit every morning', category_name, 'user_email')
        self.assertIn('Fruits', recipe_data[hash('user_email')][category_name][0]['Recipe Name'])


class AppViewTestCase(TestCase):
    """test for views"""

    def create_app(self):
        """creates app instance"""
        test_app = app
        test_app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return test_app

    def setUp(self):
        self.user = User('Bo', 'Theo', 'Bo_theo@email.com', 'Bo1995')

    def tearDown(self):
        user_data.clear()

    def test_app_running(self):
        self.app.test_client().get('/login')
        self.assert_template_used('index.html')

    def test_sign_up_page(self):
        rv = self.app.test_client().get('/signup')
        assert b"PLEASE SIGNUP" in rv.data
        self.assert_template_used('signup.html')

    def test_sign_up_data(self):
        user_data.clear()
        rv = self.app.test_client().post('/signup', data={
            "first_name": "Bo",
            "last_name": "Theo",
            "email": "Bo_theo@email.com",
            "password": "Bo1995",
            "confirm": "Bo1995"
        }, follow_redirects=True)
        self.assertIn(b'You have successfully registered', rv.data)























