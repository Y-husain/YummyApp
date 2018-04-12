[![Build Status](https://travis-ci.org/Y-husain/YummyApp.svg?branch=master)](https://travis-ci.org/Y-husain/YummyApp)
[![Coverage Status](https://coveralls.io/repos/github/Y-husain/YummyApp/badge.svg?branch=master)](https://coveralls.io/github/Y-husain/YummyApp?branch=master)
<a href="YummyApp/LICENSE.md">
<img class="notice-badge" src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="Badge"/>
</a>
<a href="https://www.python.org/dev/peps/pep-0008/">
<img class="notice-badge" src="https://img.shields.io/badge/code%20style-pep8-orange.svg" alt="Badge"/>
</a>

<h2>YUMMY RECIPES</h2>

A simple app that uses flask
The Yummy Recipes app has been beautifully designed with a number of functionalities that include: 
creation of new user account, creation of new recipe categories, viewing of recipe categories, updating of recipe categories, deletion of recipe categories, creation of new recipes, viewing of recipes, updating of recipes and deletion of recipes.
Yummy recipes provides a platform for users to keep track of their awesome recipes and share with others if they so wish.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

Prerequisites

A working web browser and or a pc.
If you wish to clone the repo please satisfy the requirements in the requirements.txt

## Installing

```
install python language (preferably version 3.6)

clone the repo to your desktop/laptop

git clone https://github.com/Y-husain/YummyApp.git

## install and run a development environment

apt-get install virtualenv venv
apt-get install -f

```


<ol>
<h5> Navigate to the cloned repo </h5>you should now see a local host 127.0.0.1:5000
Navigate to the local host with your favorite browser 
enjoy
<li> Activate your virtual environment </li>
<p><code>$ source venv/bin/activate</code></p>
<li> You should now see an virtual (venv) environment inside and install </li>
<p><code>$ pip install -r requirements.txt</code></p>
</ol>
 
<span>you should now see a local host ```127.0.0.1:5000```
. Navigate to the local host with your favorite browser 
enjoy</span>

<h3>Running  the test</h3>

<p>Testing has been implemented using the unit testing framework of the Python language. To run tests, use the following command:</p>
<p><code>$ pytest</code></p>

```
#run
pip3 install pytest

pytest /path/to/repo

### Breaking down the tests
These tests ensure login credentials are secure, recipes 
are created, Users are registered
example below

```

<h3>Test Example</h3>


```
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
```
## Need for test

To ensure maintainability of code in future developments
This ensures no new code breaks our already existing code

Note: Travis-ci ensures continous integration and runs test automatically for this build

## Deployment

Heroku app https://yummyrecipeapp2018.herokuapp.com/login

## Built With

* [Html5, css3 python and flask, Materializecss] - The markup and styling sheet
* [Dependencies in requirements.txt] - Dependency Management
* 
## Contributing

Contributions would be highly appreciated, Help out and make a pull request, and the process for submitting pull requests to me.

## Authors

* **YAHYA HUSSEIN** - *Initial work* - [Recipe-challenge](https://github.com/Y-husain/YummyRecipe-Template.git)


## License

This project is licensed under the GNU License - see the [LICENSE.md](LICENSE.md) file for details






