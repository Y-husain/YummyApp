from data import User, user_data
from flask_testing import TestCase
from app.views import app


class AppViewTestCase(TestCase):
    """test for views"""

    def create_app(self):
        """creates app instance"""
        test_app = app
        test_app.config['SECRET_KEY'] = 'sekrit!'
        test_app.config['TESTING'] = True
        test_app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        test_app.config['WTF_CSRF_ENABLED'] = False

        return test_app

    def setUp(self):
        self.user = User('Bo', 'Theo', 'Bo_theo@email.com', 'Bo1995')
        self.test_app = self.create_app()

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

    def test_login_invalid_email(self):
        login = self.app.test_client().post('/login', data={
            "email": 'bo_theo@gmail.com',
            "password": 'Bo1995'}, follow_redirects=True)
        self.assertIn('Invalid email! Please try again', login.data)

    def test_login_invalid_password(self):
        login = self.app.test_client().post('/login', data={
            "email": "Bo_theo@email.com",
            "password": "bo1995"
        }, follow_redirects=True)
        self.assertIn('Invalid password! Please try again', login.data)

    def test_authorized_access_after_login(self):
        login = self.app.test_client().post('/login', data={
            "email": "Bo_theo@email.com",
            "password": "Bo1995",
        }, follow_redirects=True)
        self.assertIn('category', login.data)

    def test_unauthorized_access_to_category(self):
        unauthorized = self.app.test_client().get('/category', follow_redirects=True)
        self.assertIn('Unauthorized to view this view, Please login', unauthorized.data)

    def test_unauthorized_access_to_dashboard(self):
        unauthorized = self.app.test_client().get('/dashboard', follow_redirects=True)
        self.assertIn('Unauthorized to view this view, Please login', unauthorized.data)

    def test_unauthorized_user_access_recipe(self):
        unauthorized = self.app.test_client().get('/my_recipe', follow_redirects=True)
        self.assertIn('Unauthorized to view this view, Please login', unauthorized.data)

    def test_unauthorized_user_edit_recipe(self):
        unauthorized = self.app.test_client().get('/edit_recipe/1', follow_redirects=True)
        self.assertIn('Unauthorized to view this view, Please login', unauthorized.data)

    def test_logout_user(self):
        user_data.clear()
        logout = self.app.test_client().get('/logout', follow_redirects=True)
        self.assertIn('You are now logged out', logout.data)


































