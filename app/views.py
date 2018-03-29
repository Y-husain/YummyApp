from flask import Flask, render_template, flash, url_for, session, logging, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, validators
from werkzeug.security import check_password_hash, generate_password_hash
from data import user_data, User, category_data, Categories
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
        password = generate_password_hash(str(form.password.data))
        User(first_name, last_name, email, password)
        flash('You have successfully registered', 'green')

        return redirect(url_for('index'))
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
        if (email in user_data) and check_password_hash(user_data[email]['Password'], user_password):
            session['logged_in'] = True
            session['email'] = email
            flash('You are now logged in', 'green')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password ! Please try again', 'red')
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













