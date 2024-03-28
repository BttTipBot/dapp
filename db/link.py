

from db.firebase import db
from db.transactions import record_transaction_by_t_username
from db.balances import get_balance_by_d_username

def link(t_username, d_username):
    # Get the balance of the d_username before linking
    d_username_balance = get_balance_by_d_username(d_username)

    # Update the entry with the given t_username to have the specified d_username
    user_ref_t = db.collection('USERS').where('t_username', '==', t_username).limit(1)
    user_data_t = user_ref_t.get()
    if user_data_t:
        user_id_t = user_data_t[0].id
        user_ref_t.document(user_id_t).update({'d_username': d_username})

        # Record the transaction in the HISTORY collection
        # if d_username_balance is not None:
        #     record_transaction_by_t_username(t_username, d_username_balance, transaction_type='discord balance before linking')

    # Delete the entry associated with the d_username
    user_ref_d = db.collection('USERS').where('d_username', '==', d_username).limit(1)
    user_data_d = user_ref_d.get()
    if user_data_d:
        user_id_d = user_data_d[0].id
        user_ref_d.document(user_id_d).delete()

    print(f"Linked {t_username} with {d_username} and deleted {d_username}.")