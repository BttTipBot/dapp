
import random
import string

from db.firebase import db
from constants.globals import USER_NEW_USER_ADDED, USER_ERROR_USER_EXISTS
from db.balances import create_or_update_balance

def get_link_code_by_t_username(t_username):
    # Retrieve the link code based on t_username
    user_ref = db.collection('USERS').where('t_username', '==', t_username).limit(1)
    user_data = user_ref.get()

    if user_data:
        return user_data[0].get('link_code')
    else:
        return None

def get_link_code_by_d_username(d_username):
    # Retrieve the link code based on d_username
    user_ref = db.collection('USERS').where('d_username', '==', d_username).limit(1)
    user_data = user_ref.get()

    if user_data:
        return user_data[0].get('link_code')
    else:
        return None

def generate_link_code():
    # Generate a link code in the format "XXX-XXX-XXX"
    link_code = '-'.join([''.join(random.choices(string.digits, k=3)) for _ in range(3)])
    return link_code


def setup_user(t_first_name='', t_last_name='', t_username='', t_id_telegram='', t_is_bot=False, d_username=''):
    # Check if the user already exists
    user_ref = db.collection('USERS').where('t_username', '==', t_username).limit(1)
    existing_user = user_ref.get()

    if existing_user:
        return USER_ERROR_USER_EXISTS
    else:
        # Generate a link code
        link_code = generate_link_code()

        # Insert the new user into the USERS collection with the generated link code
        new_user_ref = db.collection('USERS').add({
            't_first_name': t_first_name,
            't_last_name': t_last_name,
            't_username': t_username,
            't_id_telegram': t_id_telegram,
            't_is_bot': t_is_bot,
            'd_username': d_username,
            'command': 'start',
            'link_code': link_code
        })
        # Get from reference the user id
        user_id = new_user_ref[1].id
        create_or_update_balance(user_id)
        return USER_NEW_USER_ADDED


def get_or_create_user(t_first_name='', t_last_name='', t_username='', t_id_telegram='', t_is_bot=False, d_username=''):
    # Check if the user already exists
    user_ref = db.collection('USERS').where('t_username', '==', t_username).limit(1)
    existing_user = user_ref.get()

    if existing_user:
        return existing_user[0].to_dict()
    else:
        # Generate a link code
        link_code = generate_link_code()

        # Insert the new user into the USERS collection with the generated link code
        new_user_ref = db.collection('USERS').add({
            't_first_name': t_first_name,
            't_last_name': t_last_name,
            't_username': t_username,
            't_id_telegram': t_id_telegram,
            't_is_bot': t_is_bot,
            'd_username': d_username,
            'command': 'start',
            'link_code': link_code
        })

        # Retrieve the newly created user data
        user_id = new_user_ref[1].id
        create_or_update_balance(user_id)
        return USER_NEW_USER_ADDED

#Get the command of the user
def get_command_by_t_username(t_username):
    # Retrieve the command based on t_username
    user_ref = db.collection('USERS').where('t_username', '==', t_username).limit(1)
    user_data = user_ref.get()

    if user_data:
        return user_data[0].get('command')
    else:
        return None

def get_command_by_d_username(d_username):
    # Retrieve the command based on d_username
    user_ref = db.collection('USERS').where('d_username', '==', d_username).limit(1)
    user_data = user_ref.get()

    if user_data:
        return user_data[0].get('command')
    else:
        return None

#Set the command of the user
def set_command_by_t_username(t_username, command):
    # Set the command based on t_username
    user_ref = db.collection('USERS').where('t_username', '==', t_username).get()[0].reference
    user_data = user_ref.get()

    if user_data:
        user_ref.update({'command': command})
        return True
    else:
        return False

def set_command_by_d_username(d_username, command):
    # Set the command based on d_username
    user_ref = db.collection('USERS').where('d_username', '==', d_username).get()[0].reference
    user_data = user_ref.get()

    if user_data:
        user_ref.update({'command': command})
        return True
    else:
        return False