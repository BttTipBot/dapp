
import sqlite3
import random
import string
from datetime import datetime

def create_tables():
    # SQLite database setup
    conn = sqlite3.connect('balances.db')
    cursor = conn.cursor()

    # Create USERS table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS USERS (
            id INTEGER PRIMARY KEY,
            t_first_name TEXT,
            t_last_name TEXT,
            t_username TEXT,
            t_id_telegram TEXT,
            t_is_bot BOOLEAN,
            d_username TEXT,
            balance INTEGER,
            link_code TEXT,
        )
    ''')

    # Create HISTORY table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS HISTORY (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            amount INTEGER,
            transaction_type TEXT,
            date_recorded TEXT,
            FOREIGN KEY (user_id) REFERENCES USERS(id)
        )
    ''')

    # Create WALLET table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS WALLET (
            id TEXT PRIMARY KEY,
            user_id INTEGER,
            name TEXT,
            address TEXT,
            pk TEXT,
            FOREIGN KEY (user_id) REFERENCES USERS(id)
        )
    ''')

    # Create balances table if not exists
    conn.commit()

def get_link_code_by_t_username(t_username):
    conn = sqlite3.connect('balances.db')
    cursor = conn.cursor()

    # Retrieve the link code based on t_username
    cursor.execute('SELECT link_code FROM USERS WHERE t_username=?', (t_username,))
    link_code = cursor.fetchone()

    if link_code:
        return link_code[0]
    else:
        return None

def get_link_code_by_d_username(d_username):
    conn = sqlite3.connect('balances.db')
    cursor = conn.cursor()

    # Retrieve the link code based on d_username
    cursor.execute('SELECT link_code FROM USERS WHERE d_username=?', (d_username,))
    link_code = cursor.fetchone()

    if link_code:
        return link_code[0]
    else:
        return None

def record_transaction_transaction(user_id, amount, transaction_type):
    conn = sqlite3.connect('balances.db')
    cursor = conn.cursor()

    # Record the transaction in the HISTORY table
    date_recorded = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO HISTORY (user_id, amount, transaction_type, date_recorded)
        VALUES (?, ?, ?, ?)
    ''', (user_id, amount, transaction_type, date_recorded))

    conn.commit()

def record_transaction_by_t_username(t_username, amount, transaction_type='transaction telegram'):
    conn = sqlite3.connect('balances.db')
    cursor = conn.cursor()

    # Update the balance based on t_username
    cursor.execute('UPDATE USERS SET balance = balance + ? WHERE t_username=?', (amount, t_username))

    # Record the transaction in the HISTORY table
    user_id = cursor.execute('SELECT id FROM USERS WHERE t_username=?', (t_username,)).fetchone()[0]
    record_transaction_transaction(user_id, amount, transaction_type)

    conn.commit()

def record_transaction_by_d_username(d_username, amount, transaction_type='transaction discord'):
    conn = sqlite3.connect('balances.db')
    cursor = conn.cursor()

    # Update the balance based on d_username
    cursor.execute('UPDATE USERS SET balance = balance + ? WHERE d_username=?', (amount, d_username))

    # Record the transaction in the HISTORY table
    user_id = cursor.execute('SELECT id FROM USERS WHERE d_username=?', (d_username,)).fetchone()[0]
    record_transaction_transaction(user_id, amount, transaction_type)

    conn.commit()

def get_balance_by_t_username(t_username):
    conn = sqlite3.connect('balances.db')
    cursor = conn.cursor()

    # Retrieve the balance based on t_username
    cursor.execute('SELECT balance FROM USERS WHERE t_username=?', (t_username,))
    user_balance = cursor.fetchone()

    if user_balance:
        return user_balance[0]
    else:
        return None

def update_balance_by_t_username(t_username, amount):
    conn = sqlite3.connect('balances.db')
    cursor = conn.cursor()

    # Update the balance based on t_username
    cursor.execute('UPDATE USERS SET balance = balance + ? WHERE t_username=?', (amount, t_username))

    conn.commit()

def update_balance_by_d_username(d_username, amount):
    conn = sqlite3.connect('balances.db')
    cursor = conn.cursor()

    # Update the balance based on d_username
    cursor.execute('UPDATE USERS SET balance = balance + ? WHERE d_username=?', (amount, d_username))

    conn.commit()

def get_balance_by_d_username(d_username):
    conn = sqlite3.connect('balances.db')
    cursor = conn.cursor()

    # Retrieve the balance based on d_username
    cursor.execute('SELECT balance FROM USERS WHERE d_username=?', (d_username,))
    user_balance = cursor.fetchone()

    if user_balance:
        return user_balance[0]
    else:
        return None

def generate_link_code():
    # Generate a link code in the format "XXX-XXX-XXX"
    link_code = '-'.join([''.join(random.choices(string.digits, k=3)) for _ in range(3)])
    return link_code

def link(t_username, d_username):
    conn = sqlite3.connect('balances.db')
    cursor = conn.cursor()

    # Get the balance of the d_username before linking
    d_username_balance = get_balance_by_d_username(d_username)

    # Update the entry with the given t_username to have the specified d_username
    cursor.execute('UPDATE USERS SET d_username=? WHERE t_username=?', (d_username, t_username))

    # Update the balance of the d_username with the sum of the original balance and the t_username balance
    if d_username_balance is not None:
        record_transaction_by_t_username(t_username, d_username_balance, transaction_type='balance before linking')

    # Delete the entry associated with the d_username
    cursor.execute('DELETE FROM USERS WHERE d_username=?', (d_username,))

    conn.commit()
    print(f"Linked {t_username} with {d_username} and deleted {d_username}.")


def setup_user(t_first_name='', t_last_name='', t_username='', t_id_telegram='', t_is_bot=False, d_username='', balance=0):
    conn = sqlite3.connect('balances.db')
    cursor = conn.cursor()

    # Check if the user already exists
    cursor.execute('SELECT * FROM USERS WHERE t_username=? OR d_username=?', (t_username, d_username))
    existing_user = cursor.fetchone()

    if existing_user:
        print("User already exists.")
    else:
        # Generate a link code
        link_code = generate_link_code()

        # Insert the new user into the USERS table with the generated link code
        cursor.execute('''
            INSERT INTO USERS (t_first_name, t_last_name, t_username, t_id_telegram, t_is_bot, d_username, balance, link_code)
            VALUES (?, ?, ?, ?, ?, ?, 0, ?)
        ''', (t_first_name, t_last_name, t_username, t_id_telegram, t_is_bot, d_username, balance, link_code))

        conn.commit()
        print("User setup complete.")


def get_wallet_by_t_username(t_username):
    conn = sqlite3.connect('balances.db')
    cursor = conn.cursor()

    # Retrieve wallet information based on t_username
    cursor.execute('''
        SELECT WALLET.id, WALLET.name, WALLET.address
        FROM WALLET
        JOIN USERS ON WALLET.user_id = USERS.id
        WHERE USERS.t_username = ?
    ''', (t_username,))

    wallet_info = cursor.fetchone()

    if wallet_info:
        return {
            'id': wallet_info[0],
            'name': wallet_info[1],
            'address': wallet_info[2]
        }
    else:
        return None

def get_wallet_by_d_username(d_username):
    conn = sqlite3.connect('balances.db')
    cursor = conn.cursor()

    # Retrieve wallet information based on d_username
    cursor.execute('''
        SELECT WALLET.id, WALLET.name, WALLET.address
        FROM WALLET
        JOIN USERS ON WALLET.user_id = USERS.id
        WHERE USERS.d_username = ?
    ''', (d_username,))

    wallet_info = cursor.fetchone()

    if wallet_info:
        return {
            'id': wallet_info[0],
            'name': wallet_info[1],
            'address': wallet_info[2]
        }
    else:
        return None
