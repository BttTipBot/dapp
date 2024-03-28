
from datetime import datetime

from db.firebase import db
from constants.globals import USER_NOT_FOUND, USER_NO_TRANSACTION

def record_history_transaction(user_id, amount, transaction_type, currency="BTT"):
    # Record the transaction in the HISTORY collection
    date_recorded = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    history_ref = db.collection('HISTORY')
    history_ref.add({
        'user_id': user_id,
        'amount': amount,
        'currency': currency,
        'transaction_type': transaction_type,
        'date_recorded': date_recorded
    })


def get_history_by_t_username(t_username):
    user_ref = db.collection('USERS').where('t_username', '==', t_username).limit(1)
    user_data = user_ref.get()
    if user_data:
        user_id = user_data[0].id
        # Retrieve the history based on t_username
        history_ref = db.collection('HISTORY').where('user_id', '==', user_id).order_by('date_recorded', direction='DESCENDING')
        history_data = history_ref.get()
        if history_data:
            str = f"@{t_username} history\n"
            for trx in history_data:
                str += f"{trx.get('amount')} ${trx.get('currency')} {trx.get('transaction_type')} {trx.get('date_recorded')}\n"
            return str
        else:
            return USER_NO_TRANSACTION
    else:
        return USER_NOT_FOUND
