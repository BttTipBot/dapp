
from db.firebase import db

def create_or_update_balance(user_id, currency="BTT", amount=0):
    # Create or update the balance for the user
    balance_ref = db.collection('BALANCE').where('user_id','==', user_id).where('currency', '==', currency)
    balance_data = balance_ref.get()

    if balance_data:
        balance_ref.update({'balance': amount})
    else:
        db.collection('BALANCE').add({
            'user_id': user_id,
            'currency': currency,
            'balance': amount
        })

def create_balance_for_user(user_id, currency="BTT"):
    # Create a balance for the user
    balance_ref = db.collection('BALANCE')
    balance_ref.add({
        'user_id': user_id,
        'currency': currency,
        'balance': 0
    })

def update_balance_by_t_username(t_username, amount):
    # Update the balance based on t_username
    user_ref = db.collection('USERS').where('t_username', '==', t_username).limit(1)
    user_data = user_ref.get()

    if user_data:
        user_id = user_data[0].id
        user_ref.document(user_id).update({'balance': user_data[0].get('balance') + amount})

def update_balance_by_d_username(d_username, amount):
    # Update the balance based on d_username
    user_ref = db.collection('USERS').where('d_username', '==', d_username).limit(1)
    user_data = user_ref.get()

    if user_data:
        user_id = user_data[0].id
        user_ref.document(user_id).update({'balance': user_data[0].get('balance') + amount})


def get_balance_by_d_username(d_username, currency="BTT"):
    # Retrieve the balance based on d_username
    user_ref = db.collection('USERS').where('d_username', '==', d_username).limit(1)
    user_data = user_ref.get()

    if user_data:
        user_id = user_data[0].id
        balance_ref = db.collection('BALANCE').where('user_id','==', user_id).where('currency', '==', currency)
        balance_data = balance_ref.get()
        if len(balance_data) > 0:
            return balance_data[0].get('balance')
    return '0'

def get_balance_by_t_username(t_username, currency="BTT"):
    # Retrieve the balance based on d_username
    user_ref = db.collection('USERS').where('t_username', '==', t_username).limit(1)
    user_data = user_ref.get()

    if user_data:
        user_id = user_data[0].id
        balance_ref = db.collection('BALANCE').where('user_id','==', user_id).where('currency', '==', currency)
        balance_data = balance_ref.get()
        if len(balance_data) > 0:
            return int(balance_data[0].get('balance'))
    return 0

