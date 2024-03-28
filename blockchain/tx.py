# Import the required libraries
import os
import json

from web3 import Web3
from web3.middleware import geth_poa_middleware

#Check if a transaction is successful
def check_tx_status(tx_hash):
    print("check_tx_status: tx_receipt:", tx_hash)

    # Set the Ethereum Testnet RPC URL
    ETH_RPC_URL = os.getenv('ETH_RPC_URL')

    # Set the Web3 provider
    w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # Check if the transaction was successful
    if tx_receipt['status'] == 1:
        return True
    else:
        return False