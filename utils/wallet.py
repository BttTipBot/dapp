import os

from db.wallets import get_all_wallets_by_t_username, get_all_wallets_by_d_username

def get_my_wallet_t(t_username, wallet_name):
    wallets = get_all_wallets_by_t_username(t_username)
    return next((wallet for wallet in wallets if wallet['name'] == wallet_name or (wallet['name'] + " (" + wallet['address'] + ")") == wallet_name), None)

def get_my_wallet_d(d_username, wallet_name):
    wallets = get_all_wallets_by_d_username(d_username)
    return next((wallet for wallet in wallets if wallet['name'] == wallet_name or (wallet['name'] + " (" + wallet['address'] + ")") == wallet_name), None)

def get_wallet_full_name(wallet):
    return wallet['name'] + " (" + wallet['address'] + ")"

def get_url_by_tx(tx):
    URL = os.getenv('EXPLORER_TRANSACTION_URL')
    return URL + tx

def get_url_by_address(address):
    URL = os.getenv('EXPLORER_ADDRESS_URL')
    return URL + address

def is_address(address):
    return all(c in '0123456789abcdefxABCDEFX' for c in address) and len(address) == 42 and address[:2] == '0x'