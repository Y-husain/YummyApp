user_data = {}
category_data = {}
recipe_data = {}


class User:
    """store registration information of users"""
    def __init__(self, first_name, last_name, email, password):
        global user_data
        user_id = hash(email)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        user_data[user_id] = {'First Name': self.first_name,
                              'Last Name': self.last_name,
                              'Email': self.email,
                              'Password': self.password}


class Categories:
    def __init__(self, email, category_name):
        global category_data
        self.user_id = hash(email)
        self.category_name = category_name

        try:
            category_data[self.user_id]
        except KeyError:
            category_data[self.user_id] = []
            category_data[self.user_id].append(self.category_name)
        else:
            category_data[self.user_id].append(self.category_name)


class Recipes:
    """stores recipes """

    def __init__(self, recipe_name, recipe, category_name, email):
        global category_data
        global recipe_data
        self.recipe_name = recipe_name
        self.recipe = recipe
        self.user_id = email
        self.category_name = category_name

        try:
            recipe_data[self.user_id][self.category_name]
        except KeyError:
            recipe_data[self.user_id] = {}
            recipe_data[self.user_id].update({self.category_name: []})
            recipe_data[self.user_id][self.category_name].append({'Recipe Name': self.recipe_name,
                                                                  'My Recipe': self.recipe})
        else:
            recipe_data[self.user_id][self.category_name].append({'Recipe Name': self.recipe_name,
                                                                  'My Recipe': self.recipe})






