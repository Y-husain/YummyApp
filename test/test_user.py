import unittest
from data import User, user_data, category_data, recipe_data
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
        category_data.clear()
        recipe_data.clear()

    def signup(self, first_name, last_name, email, password, confirm):
        return self.client.post('/signup', data=dict(
         first_name=first_name, last_name=last_name, email=email,
         password=password, confirm=confirm), follow_redirects=True)

    def login(self, email, password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def dashboard(self):
        return self.client.get('/dashboard', follow_redirects=True)

    def category(self, category_name):
        return self.client.post('/category', data=dict(
            category_name=category_name
        ), follow_redirects=True)

    def edit_category(self, edited_category_name):
        return self.client.post('/edit_category/Breakfast', data=dict(
            category_name=edited_category_name
        ), follow_redirects=True)

    def del_category(self):
        return self.client.post('/delete_category/JunkFood', follow_redirects=True)

    def recipe_dashboard(self,):
        return self.client.get('/dashboard/JunkFood/dashboard_recipe', follow_redirects=True)

    def create_recipe(self, recipe_name, recipe):
        return self.client.post('/my_recipe?val=JunkFood', data=dict(
            recipe_name=recipe_name,
            recipe=recipe,
        ), follow_redirects=True)

    def edit_recipe(self, edited_recipe_name, edited_recipe):
        return self.client.post('/edit_recipe/0?val=JunkFood', data=dict(
            recipe_name=edited_recipe_name,
            recipe=edited_recipe
        ), follow_redirects=True)

    def del_recipe(self):
        return self.client.post('/delete_recipe/0?val=JunkFood', follow_redirects=True)

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

    def test_successful_login(self):
        """test for successful sign in"""
        self.signup('Bo', 'Theo', 'Bo_theo5@example.com', 'Bo1995', 'Bo1995')
        rv = self.login('Bo_theo5@example.com', 'Bo1995')
        self.assertIn(b'You are now logged in', rv.data)

    def test_invalid_email(self):
        """test for invalid email"""
        rv = self.login('Bo_wrong@example.com', 'Bo1995')
        self.assertIn(b'Invalid email! Please try again', rv.data)

    def test_invalid_password(self):
        """test for invalid password"""
        self.signup('Bo', 'Theo', 'Bo_theo5@example.com', 'Bo1995', 'Bo1995')
        rv = self.login('Bo_theo5@example.com', 'Bo1905')
        self.assertIn(b'Invalid password! Please try again', rv.data)

    def test_logout(self):
        """test for logout """
        self.signup('Bo', 'Theo', 'Bo_theo5@example.com', 'Bo1995', 'Bo1995')
        rv = self.logout()
        self.assertIn('You are now logged out', rv.data)

    def test_dashboard(self):
        """test for dashboard page loads"""
        self.signup('Bo', 'Theo', 'Bo_theo5@example.com', 'Bo1995', 'Bo1995')
        rv = self.login('Bo_theo5@example.com', 'Bo1995')
        self.assertIn(b'Create a Recipe Category', rv.data)

    def test_empty_category_dashboard(self):
        """test for empty category in dashboard"""
        self.signup('Bo', 'Theo', 'Bo_theo5@example.com', 'Bo1995', 'Bo1995')
        rv = self.login('Bo_theo5@example.com', 'Bo1995')
        self.assertIn(b'Create a Recipe Category', rv.data)

    def test_blank_category(self):
        """test for blank category"""
        self.signup('Bo', 'Theo', 'Bo_theo5@example.com', 'Bo1995', 'Bo1995')
        self.login('Bo_theo5@example.com', 'Bo1995')
        rv = self.category('')
        self.assertIn(b'Field must be between 1 and 50 characters long.', rv.data)

    def test_add_category(self):
        """test for addition of category"""
        self.signup('Bo', 'Theo', 'Bo_theo5@example.com', 'Bo1995', 'Bo1995')
        self.login('Bo_theo5@example.com', 'Bo1995')
        rv = self.category('Breakfast')
        self.assertIn(b'Category created', rv.data)

    def test_edit_category(self):
        """test for edit category"""
        self.signup('Bo', 'Theo', 'Bo_theo5@example.com', 'Bo1995', 'Bo1995')
        self.login('Bo_theo5@example.com', 'Bo1995')
        self.category('Breakfast')
        rv = self.edit_category('JunkFood')
        self.assertIn(b'Category successfully updated', rv.data)

    def test_delete_category(self):
        """test for delete category"""
        self.signup('Bo', 'Theo', 'Bo_theo5@example.com', 'Bo1995', 'Bo1995')
        self.login('Bo_theo5@example.com', 'Bo1995')
        self.category('JunkFood')
        rv = self.del_category()
        self.assertIn(b'successfully deleted category', rv.data)

    def test_dashboard_recipe_created_with_category(self):
        """test dashboard recipe with category recipe"""
        self.signup('Bo', 'Theo', 'Bo_theo5@example.com', 'Bo1995', 'Bo1995')
        self.login('Bo_theo5@example.com', 'Bo1995')
        self.category('JunkFood')
        rv = self.recipe_dashboard()
        self.assertIn(b'JunkFood', rv.data)

    def test_dashboard_without_recipe(self):
        """test for dashboard recipe without category recipe"""
        self.signup('Bo', 'Theo', 'Bo_theo5@example.com', 'Bo1995', 'Bo1995')
        self.login('Bo_theo5@example.com', 'Bo1995')
        self.category('JunkFood')
        rv = self.recipe_dashboard()
        self.assertIn(b'Please create a category Recipe', rv.data)

    def test_create_recipe_category(self):
        """test for successful creation of recipe category """
        self.signup('Bo', 'Theo', 'Bo_theo5@example.com', 'Bo1995', 'Bo1995')
        self.login('Bo_theo5@example.com', 'Bo1995')
        self.category('JunkFood')
        self.recipe_dashboard()
        rv = self.create_recipe('cakes', 'blah, blah, blah....mix ingredient, heat')
        self.assertIn(b'Recipe created', rv.data)

    def test_edit_recipe_category(self):
        """test for update of recipe category """
        self.signup('Bo', 'Theo', 'Bo_theo5@example.com', 'Bo1995', 'Bo1995')
        self.login('Bo_theo5@example.com', 'Bo1995')
        self.category('JunkFood')
        self.recipe_dashboard()
        self.create_recipe('cakes', 'blah, blah, blah....mix ingredient, heat')
        rv = self.edit_recipe('edited cakes', 'edited blah blah blah spoon , heat')
        self.assertIn(b'Recipe successfully updated', rv.data)

    def test_delete_recipe_category(self):
        """test for deletion of recipe"""
        self.signup('Bo', 'Theo', 'Bo_theo5@example.com', 'Bo1995', 'Bo1995')
        self.login('Bo_theo5@example.com', 'Bo1995')
        self.category('JunkFood')
        self.recipe_dashboard()
        self.create_recipe('cakes', 'blah, blah, blah....mix ingredient, heat')
        self.edit_recipe('edited cakes', 'edited blah blah blah spoon , heat')
        rv = self.del_recipe()
        self.assertIn(b'deleted successfully', rv.data)















