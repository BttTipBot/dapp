
from datetime import datetime

from db.history import record_history_transaction
from db.firebase import db
from db.users import get_or_create_user
from db.parameters import get_param
from db.balances import get_balance_by_t_username

from constants.parameters import PARAMETER_WELCOME_BONUS, PARAMETER_TIP_FEE_BTT
from utils.convert import convert_to_int
from utils.shorts import get_short_tx

from constants.globals import TIP_INSUFFICIENT_BALANCE, USER_NOT_FOUND, USER_WELCOME_BONUS_MESSAGE

def record_transaction_by_t_username(t_username, amount, transaction_type='transaction telegram', currency='BTT'):
    user_ref = db.collection('USERS').where('t_username', '==', t_username).limit(1)
    user_data = user_ref.get()

    if user_data:
        user_id = user_data[0].id
        # Record the transaction in the HISTORY collection
        record_history_transaction(user_id, amount, transaction_type)

        # Update the balance in the BALANCE table
        balance_ref = db.collection('BALANCE').where('user_id', '==', user_id).where('currency', '==', currency)
        balance_p = balance_ref.get()[0].reference
        balance_data = balance_ref.get()
        balance_object = balance_data[0].to_dict()
        print(f'balance_data: {balance_data}')
        print(f'balance_ref: {balance_ref}')
        print(f'balance_p: {balance_p}')

        if balance_data:
            balance_p.update({'balance': balance_object.get('balance') + amount})
        else:
            db.collection('BALANCE').add({
                'user_id': user_id,
                'currency': currency,
                'balance': amount
            })

def record_global_top_up_by_t_username(t_username, amount, currency='BTT'):
    user_ref = db.collection('USERS').where('t_username', '==', t_username).limit(1)
    user_data = user_ref.get()

    if user_data:
        user_id = user_data[0].id

        date_recorded = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Add a record in GLoBAL_TOP_UP
        db.collection('GLOBAL_TOP_UP').add({
            'user_id': user_id,
            'currency': currency,
            'amount': amount,
            'date_recorded': date_recorded,
        })

def record_global_withdraw_by_t_username(t_username, amount, currency='BTT'):
    user_ref = db.collection('USERS').where('t_username', '==', t_username).limit(1)
    user_data = user_ref.get()

    if user_data:
        user_id = user_data[0].id

        date_recorded = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Add a record in GLoBAL_TOP_UP
        db.collection('GLOBAL_WITHDRAW').add({
            'user_id': user_id,
            'currency': currency,
            'amount': amount,
            'date_recorded': date_recorded,
        })

def record_transaction_by_d_username(d_username, amount, transaction_type='transaction discord', currency='BTT'):
    # Update the balance based on d_username
    user_ref = db.collection('USERS').where('d_username', '==', d_username).limit(1)
    user_data = user_ref.get()

    if user_data:
        user_id = user_data[0].id
        # Record the transaction in the HISTORY collection
        record_history_transaction(user_id, amount, transaction_type)

        # Update the balance in the BALANCE table
        balance_ref = db.collection('BALANCE').where('user_id', '==', user_id).where('currency', '==', currency)
        balance_data = balance_ref.get()

        if balance_data:
            balance_ref.update({'balance': balance_data[0].get('balance') + amount})
        else:
            db.collection('BALANCE').add({
                'user_id': user_id,
                'currency': currency,
                'balance': amount
            })

def top_up_balance_by_t_username(tx, t_username, amount, currency='BTT'):
    # Record the top up in the HISTORY collection
    record_transaction_by_t_username(t_username, amount, '💳 top up ' + get_short_tx(tx), currency)
    record_global_top_up_by_t_username(t_username, amount, currency)

def withdraw_balance_by_t_username(tx, t_username, amount, currency='BTT'):
    # Record the top up in the HISTORY collection
    record_transaction_by_t_username(t_username, -amount, '🏧 withdraw ' + get_short_tx(tx), currency)
    record_global_top_up_by_t_username(t_username, amount, currency)


def record_tip_by_t_username(t_username_sender, t_username_receiver, amount, currency='BTT'):
    # Record the tip in the HISTORY collection
    sender = get_or_create_user(t_username=t_username_sender)
    receiver = get_or_create_user(t_username=t_username_receiver)

    # balance_sender = get_balance_by_t_username(t_username_sender, currency)
    fee = int(get_param(PARAMETER_TIP_FEE_BTT))

    # if balance_sender + fee < amount:
    #     return TIP_INSUFFICIENT_BALANCE.format(balance=balance_sender, max=balance_sender)
    record_transaction_by_t_username(t_username_sender, -fee, f'you paid a fee for tipping telegram@{t_username_sender} ⛽💸', currency)
    record_transaction_by_t_username(t_username_sender, -amount, f'you tip telegram@{t_username_sender} 💸', currency)
    record_transaction_by_t_username(t_username_receiver, amount, f'you were tip by telegram@{t_username_sender} 🤑', currency)

    return f"Tip successful! @{t_username_sender} tipped @{t_username_receiver} {amount} ${currency}."

def record_welcome_bonus_by_t_username(t_username, currency='BTT'):

    # PARAMETER
    value_param = get_param(PARAMETER_WELCOME_BONUS)
    # Record the welcome bonus in the HISTORY collection
    record_transaction_by_t_username(t_username, value_param, USER_WELCOME_BONUS_MESSAGE.format(amount=value_param) , currency)
