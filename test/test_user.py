import unittest
from data import User, user_data, Categories, category_data, Recipes, recipe_data
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

    def signup(self, first_name, last_name, email, password, confirm):
        return self.client.post('/signup', data=dict(
         first_name=first_name, last_name=last_name, email=email,
         password=password, confirm=confirm), follow_redirects=True)

    def login(self, email, password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def category(self, category_name):
        return self.client.post('/category', data=dict(
            category_name= category_name
        ), follow_redirects=True)

    def edit_category(self, edited_category_name):
        return self.client.post('/edit_category', data=dict(
            edited_category_name=edited_category_name
        ), follow_redirects=True)

    def del_category(self):
        self.client.post('/delete_category', follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_application_running(self):
        """ensures that flask was setup correctly"""
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/signup', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_logging_running(self):
        """ensures that flask was setup correctly"""
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue(b'PLEASE LOGIN' in response.data)

    def test_user_registration_successful(self):
        """test for successful registration"""
        rv = self.signup('Bo', 'Theo', 'Bo_theo5@example.com', 'Bo1995', 'Bo1995')
        self.assertIn(b'You have successfully registered', rv.data)

    def test_duplicate_email(self):
        """test for duplicate email that  already exist """
        self.signup('Bo', 'Theo', 'Bo_theo5@example.com', 'Bo1995', 'Bo1995')
        rv = self.signup('Bo', 'Theo', 'Bo_theo5@example.com', 'Bo1995', 'Bo1995')
        self.assertIn(b'Sorry email already exist', rv.data)

    def test_blank_email(self):
        """test for blank email"""
        rv = self.signup('Bo', 'Theo', '', 'Bo1995', 'Bo1995')
        self.assertIn(b'Field must be between 6 and 30 characters long.', rv.data)

    def test_blank_names(self):
        """test for blank first_name and last_ame"""
        rv = self.signup('', '', 'Bo_theo5@example.com', 'Bo1995', 'Bo1995')
        self.assertIn(b'This field is required.', rv.data)

    def test_blank_password(self):
        """test for blank password"""
        rv = self.signup('Bo', 'Theo', 'Bo_theo5@example.com', '', 'Bo1995')
        self.assertIn(b'This field is required.', rv.data)

    def test_mismatch_signup_password(self):
        rv = self.signup('Bo', 'Theo', 'Bo_theo5@example.com', 'Bo1995', 'Bo195')
        self.assertIn(b'Password do not match', rv.data)


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










