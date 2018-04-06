from flask import Flask, render_template, flash, url_for, session, logging, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, validators
from werkzeug.security import check_password_hash
from data import user_data, User, category_data, Categories, recipe_data, Recipes
from functools import wraps
app = Flask(__name__)
app.secret_key = 'its-secret'
logged_in = False


@app.route('/')
def index():
    return redirect(url_for('login'))


class SignupForm(FlaskForm):
    """creates a registration form"""
    first_name = StringField('First Name', [validators.length(min=2, max=50), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=2, max=50), validators.DataRequired()])
    email = StringField('Email', [validators.length(min=6, max=30)])
    password = PasswordField('Password', [validators.DataRequired(),
                                          validators.EqualTo('confirm', 'Password do not match')])
    confirm = PasswordField('Confirm Password')


class LoginForm(FlaskForm):
    """Creates sign-in form"""
    email = StringField('Email', [validators.Length(min=6, max=30), validators.data_required()])
    password = PasswordField('Password', [validators.DataRequired(),
                                          validators.EqualTo('confirm', 'Password do not match')])


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    """lets the user signup and stores the data in user-data dictionary
    to be used in login page"""
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        if hash(form.email.data) not in user_data:
            User(first_name, last_name, email, password)
            flash('You have successfully registered', 'green')
            return redirect(url_for('index'))
        else:
            flash('Sorry email already exist', 'red')
            return render_template('signup.html', form=form)
    return render_template('signup.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    """Lets the user sing-in and it should match with the
    registration data from user-data he signup with
    and creates a logged in session  for the  user """

    form = LoginForm(request.form)
    if request.method == 'POST':
        email = request.form['email']
        user_password = request.form['password']
        email = hash(email)
        if email in user_data:
            if check_password_hash(user_data[email]['Password'], user_password):
                session['logged_in'] = True
                session['email'] = email
                flash('You are now logged in', 'green')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid password! Please try again', 'red')
                return redirect(url_for('login'))
        else:
            flash('Invalid email! Please try again', 'red')
            return redirect(url_for('login'))
    return render_template('index.html', form=form)


def is_logged_in(f):
    """Create a decorator @is_logged_in that is a function wrapper that only allow authorized user to access
    else  redirect him to the login page"""
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unathorized, Please login', 'red')
            return redirect(url_for('login'))
    return wrap


@app.route('/logout')
@is_logged_in
def logout():
    """clears the session and redirect the user login page"""
    session.clear()
    flash('You are now logged out', 'green')
    return redirect(url_for('login'))


class CategoryForm(FlaskForm):
    """create categories platform for authorized user"""
    category_name = StringField('Category', [validators.Length(min=1, max=50)])


@app.route('/category', methods=['GET', 'POST'])
@is_logged_in
def category():
    email = session['email']
    form = CategoryForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        category_name = form.category_name.data
        Categories(email, category_name)
        flash('Category created', 'green')
        return redirect(url_for('dashboard'))
    return render_template('categories.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@is_logged_in
def dashboard():
    if category_data:
        email = session['email']
        try:
            return render_template('dashboard.html', category_list=category_data[email], email=email)
        except KeyError:
            flash('Create a Recipe Category', 'red')
            return render_template('dashboard.html')

    else:
        flash('Create a Recipe Category', 'red')
        return render_template('dashboard.html')


@app.route('/dashboard/<string:category_name>/dashboard_recipe')
@is_logged_in
def dashboard_recipe(category_name):
    """Routes the dashboard recipe along with the category name and  users list of recipes
    if exist or else redirect the user to dashboard to create a category"""
    email = session['email']
    index = category_data[email].index(category_name)
    try:
        category_data[email][index]
    except KeyError:
        flash('Category does not exist, Please create a category', 'red')
        return redirect(url_for('dashboard'))
    if recipe_data:
        email = session['email']

        try:
            return render_template('DashboardRecipes.html', recipe_list=recipe_data[email][category_name], email=email,
                                   category_name=category_data[email][index])
        except KeyError:
            flash('Create a  recipe for the category', 'green')
            return render_template('DashboardRecipes.html', category_name=category_name)
    else:
        flash('Please create a category Recipe', 'green')
        return render_template('DashboardRecipes.html', category_name=category_name)


class RecipeForm(FlaskForm):
    recipe_name = StringField('Recipe Name', [validators.Length(min=1, max=50)])
    recipe = TextAreaField('Recipe', [validators.Length(min=2, max=200)])


@app.route('/my_recipe', methods=['GET', 'POST'])
@is_logged_in
def my_recipe():
    """routes my-recipes that let the user post request that is added to added to my my_recipes dict
    as a data and is redirected to dashboard_recipe to viewed by user """
    email = session['email']
    category_name = request.args.get('val', '')
    form = RecipeForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        recipe_name = form.recipe_name.data
        recipe = form.recipe.data
        Recipes(recipe_name, recipe, category_name, email)
        flash('Recipe created', 'green')
        return redirect(url_for('dashboard_recipe', category_name=category_name))
    return render_template('Recipes.html', form=form)


@app.route('/edit_recipe/<int:id_recipe>', methods=['GET', 'POST'])
@is_logged_in
def edit_recipe(id_recipe):
    """routes edit_recipes when the user whats to update his/her recipe"""
    email = session['email']
    category_name = request.args.get('val', '')
    form = RecipeForm(request.form)
    if request.method == 'GET':
        form.recipe_name.data = recipe_data[email][category_name][id_recipe]['Recipe Name']
        form.recipe.data = recipe_data[email][category_name][id_recipe]['Recipe']
        return render_template('edited_recipe.html', form=form)
    if request.method == 'POST' and form.validate_on_submit():
        edited_recipe_name = form.recipe_name.data
        edited_recipe = form.recipe.data
        del recipe_data[email][category_name][id_recipe]
        Recipes(edited_recipe_name, edited_recipe, category_name, email)
        flash('Recipe successfully updated', 'green')
        return redirect(url_for('dashboard_recipe', category_name=category_name))


@app.route('/delete_recipe/<int:id_recipe>', methods=['GET', 'POST'])
@is_logged_in
def delete_recipe(id_recipe):
    email = session['email']
    category_name = request.args.get('val', '')
    del recipe_data[email][category_name][id_recipe]
    flash('deleted successfully', 'green')
    return redirect(url_for('dashboard_recipe', category_name=category_name))


@app.route('/edit_category/<string:category_name>', methods=['GET', 'POST'])
@is_logged_in
def edit_category(category_name):
    email = session['email']
    form = CategoryForm(request.form)
    if request.method == 'GET':
        form.category_name.data = category_name

    if request.method == 'POST' and form.validate_on_submit():
        edited_category_name = form.category_name.data
        del_id = category_data[email].index(category_name)
        del category_data[email][del_id]
        Categories(email, edited_category_name)
        flash('Category successfully updated', 'green')
        return redirect(url_for('dashboard'))
    return render_template('edit_category.html', form=form)


@app.route('/delete_category/<category_name>', methods=['POST'])
@is_logged_in
def delete_category(category_name):
    email = session['email']
    index = category_data[email].index(category_name)
    del category_data[email][index]
    flash('successfully deleted category', 'green')
    return redirect(url_for('dashboard'))






















