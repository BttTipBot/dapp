# Import the required libraries
import os

from web3 import Web3
from web3.middleware import geth_poa_middleware

from eth_account import Account

def create_wallet():
    # Generate a new Ethereum account
    account = Account.create()

    # Print the private key (keep this secret!)
    print("create_wallet: Private Key:", account._private_key.hex())

    # Print the Ethereum address
    print("create_wallet: Ethereum Address:", account.address)

    return {
        'pk': account._private_key.hex(),
        'address': account.address
    }


def get_address_and_private_key(private_key):
    # Create an Ethereum account using the provided private key
    print("get_address_and_private_key: Private Key:", private_key)
    account = Account.from_key(private_key)

    print("get_address_and_private_key: Address:", account.address)
    print("get_address_and_private_key: Private Key:", account._private_key.hex())

    # Return the private key and address
    return {
        'pk': private_key,
        'address': account.address
    }

def get_balance(address):
    # Set the Ethereum Testnet RPC URL
    ETH_RPC_URL = os.getenv('ETH_RPC_URL')
    print("getBalance: Address: ", address)

    # Set the Web3 provider
    w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # Get the balance of an Ethereum account
    balance = w3.eth.get_balance(address)
    return w3.from_wei(balance, "ether")

def transfer_eth(sender, receiver, amount, private_key):
    # Set the Ethereum Testnet RPC URL
    ETH_RPC_URL = os.getenv('ETH_RPC_URL')

    # Set the Web3 provider
    w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # Set the Ethereum Testnet private key
    ETH_PRIVATE_KEY = private_key

    # initialize the chain id, we need it to build the transaction for replay protection
    Chain_id = w3.eth.chain_id

    # Set the transaction parameters
    nonce = w3.eth.get_transaction_count(sender)
    gasPrice = w3.eth.gas_price
    addressReceiver = w3.to_checksum_address(receiver)
    value = w3.to_wei(amount, "ether")

    # Build the transaction
    tx = {
        'nonce': nonce,
        'to': addressReceiver,
        'value': value,
        'gas': 2000000,
        'gasPrice': gasPrice,
        'chainId': Chain_id,
    }

    # Sign the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=ETH_PRIVATE_KEY)

    # Send the transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return tx_receipt['transactionHash'].hex()