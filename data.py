user_data = {}


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

