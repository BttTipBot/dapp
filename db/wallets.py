
from db.firebase import db
from datetime import datetime

def add_wallet_user_id(user_id, wallet_name, wallet_address, wallet_pk):
    # Add a new wallet to the database
    wallet_ref = db.collection('WALLET').document()
    wallet_ref.set({
        'id': wallet_ref.id,
        'user_id': user_id,
        'name': wallet_name,
        'address': wallet_address,
        'pk': wallet_pk
    })

def add_wallet_by_t_username(t_username, wallet_name, wallet_address, wallet_pk):
    # Add a new wallet to the database
    user_ref = db.collection('USERS').where('t_username', '==', t_username).limit(1)
    user_data = user_ref.get()

    if user_data:
        user_id = user_data[0].id
        add_wallet_user_id(user_id, wallet_name, wallet_address, wallet_pk)

def add_wallet_by_d_username(d_username, wallet_name, wallet_address, wallet_pk):
    # Add a new wallet to the database
    user_ref = db.collection('USERS').where('d_username', '==', d_username).limit(1)
    user_data = user_ref.get()

    if user_data:
        user_id = user_data[0].id
        add_wallet_user_id(user_id, wallet_name, wallet_address, wallet_pk)  

def get_all_wallets_by_t_username(t_username):
    # Retrieve all wallets information based on t_username
    user_ref = db.collection('USERS').where('t_username', '==', t_username).limit(1)
    user_data = user_ref.get()

    if user_data:
        user_id = user_data[0].id

        wallet_ref = db.collection('WALLET').where('user_id', '==', user_id)
        wallet_data = wallet_ref.get()

        wallets = []
        for wallet in wallet_data:
            wallets.append({
                'id': wallet.get('id'),
                'name': wallet.get('name'),
                'address': wallet.get('address'),
                'pk': wallet.get('pk')
            })

        return wallets
    else:
        return []

def delete_wallet_name_by_t_username(t_username, wallet_name):
    print("delete_wallet_name_by_t_username: ", t_username, wallet_name)
    # Retrieve all wallets information based on t_username
    user_ref = db.collection('USERS').where('t_username', '==', t_username).limit(1)
    user_data = user_ref.get()

    if user_data:
        user_id = user_data[0].id

        wallet_ref = db.collection('WALLET').where('user_id', '==', user_id).where('name', '==', wallet_name).limit(1)
        wallet_data = wallet_ref.get()
        
        # Save in history
        wallet = wallet_data[0]
        
        date_archive = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        wallet_ref = db.collection('WALLET_HISTORY').document()
        wallet_ref.set({
            'id': wallet.id,
            'user_id': user_id,
            'name': wallet.get('name'),
            'address': wallet.get('address'),
            'archive': date_archive,
            'pk': wallet.get('pk')
        })

        # Delete wallet
        wallet_ref = db.collection('WALLET').document(wallet.id)
        wallet_ref.delete()



    





def get_all_wallets_by_d_username(d_username):
    # Retrieve wallet information based on d_username
    wallet_ref = db.collection('WALLET').where('user_id', '==', d_username)
    wallet_data = wallet_ref.get()

    wallets = []
    for wallet in wallet_data:
        wallets.append({
            'id': wallet.get('id'),
            'name': wallet.get('name'),
            'address': wallet.get('address'),
            'pk': wallet.get('pk')
        })

    return wallets
