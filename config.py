import os

# CONFIG SECTION
class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY')
    REGISTERED_USERS = {
        'moekaid@gmail.com': {
            'name': 'Mohamed Kaid',
            'password': 'test123'
        }

    }