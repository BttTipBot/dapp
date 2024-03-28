# Import the required libraries
import os
import json

from web3 import Web3
from web3.middleware import geth_poa_middleware


def tip_call(sender, receiver, amount, pk):
    # Set the Ethereum Testnet RPC URL
    ETH_RPC_URL = os.getenv('ETH_RPC_URL')

    # Set the Ethereum Testnet contract address
    ETH_CONTRACT_ADDRESS = os.getenv('ETH_CONTRACT_ADDRESS')

    # Read the TipBot.json file as a JSON ABI
    with open('./blockchain/abi/TipBot.json', 'r') as file:
        abi = json.load(file)
        ETH_CONTRACT_ABI = abi["abi"]

    # Set the Web3 provider
    w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # initialize the chain id, we need it to build the transaction for replay protection
    Chain_id = w3.eth.chain_id

    # Set the contract
    address = w3.to_checksum_address(ETH_CONTRACT_ADDRESS)
    contract = w3.eth.contract(address=address, abi=ETH_CONTRACT_ABI)

    # Initialize address nonce
    addressSender = w3.to_checksum_address(sender)
    nonce = w3.eth.get_transaction_count(addressSender)
    
    addressReceiver = w3.to_checksum_address(receiver)
    amount_wei = w3.to_wei(amount, 'ether')
    tx_hash = contract.functions.tip(addressReceiver, amount_wei).build_transaction({"chainId": Chain_id, "from": addressSender, "nonce": nonce, "gasPrice": 50000000000000000})

    # Sign transaction
    signed_tx = w3.eth.account.sign_transaction(tx_hash, private_key=pk)
    
    # Send transaction
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    return tx_receipt['transactionHash'].hex()

def get_tip_balance(address_in):
    print("get_tip_balance: address:", address_in)
    # Set the Ethereum Testnet RPC URL
    ETH_RPC_URL = os.getenv('ETH_RPC_URL')

    # Set the Ethereum Testnet contract address
    ETH_CONTRACT_ADDRESS = os.getenv('ETH_CONTRACT_ADDRESS')

    # Read the TipBot.json file as a JSON ABI
    with open('./blockchain/abi/TipBot.json', 'r') as file:
        abi = json.load(file)
        ETH_CONTRACT_ABI = abi["abi"]

    # Set the Web3 provider
    w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # Set the contract
    address = w3.to_checksum_address(ETH_CONTRACT_ADDRESS)
    contract = w3.eth.contract(address=address, abi=ETH_CONTRACT_ABI)

    # Get the balance
    balance = contract.functions.getDepositedBalance(address_in).call()
    print("get_tip_balance: balance:", balance)

    balance = w3.from_wei(balance, 'ether')

    return balance

# Deposit into the TipBot contract
def deposit_tip(amount, address_in, pk):
    # Set the Ethereum Testnet RPC URL
    ETH_RPC_URL = os.getenv('ETH_RPC_URL')

    # Set the Ethereum Testnet contract address
    ETH_CONTRACT_ADDRESS = os.getenv('ETH_CONTRACT_ADDRESS')

    # Read the TipBot.json file as a JSON ABI
    with open('./blockchain/abi/TipBot.json', 'r') as file:
        abi = json.load(file)
        ETH_CONTRACT_ABI = abi["abi"]

    # Set the Web3 provider
    w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # initialize the chain id, we need it to build the transaction for replay protection
    Chain_id = w3.eth.chain_id

    # Set the contract
    address = w3.to_checksum_address(ETH_CONTRACT_ADDRESS)
    contract = w3.eth.contract(address=address, abi=ETH_CONTRACT_ABI)

    # Initialize address nonce
    addressSender = w3.to_checksum_address(address_in)
    nonce = w3.eth.get_transaction_count(addressSender)

    # Build the transaction
    amount_wei = w3.to_wei(amount, 'ether')
    tx_hash = contract.functions.deposit().build_transaction({"chainId": Chain_id, "from": addressSender, "nonce": nonce, "value": amount_wei, "gasPrice": 50000000000000000})

    # Sign the transaction
    signed_tx = w3.eth.account.sign_transaction(tx_hash, private_key=pk)

    # Send the transaction
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    return tx_receipt['transactionHash'].hex()

# Withdraw from the TipBot contract
def withdraw_tip(amount, address_in, pk):
    # Set the Ethereum Testnet RPC URL
    ETH_RPC_URL = os.getenv('ETH_RPC_URL')

    # Set the Ethereum Testnet contract address
    ETH_CONTRACT_ADDRESS = os.getenv('ETH_CONTRACT_ADDRESS')

    # Read the TipBot.json file as a JSON ABI
    with open('./blockchain/abi/TipBot.json', 'r') as file:
        abi = json.load(file)
        ETH_CONTRACT_ABI = abi["abi"]

    # Set the Web3 provider
    w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # initialize the chain id, we need it to build the transaction for replay protection
    Chain_id = w3.eth.chain_id

    # Set the contract
    address = w3.to_checksum_address(ETH_CONTRACT_ADDRESS)
    contract = w3.eth.contract(address=address, abi=ETH_CONTRACT_ABI)

    # Initialize address nonce
    addressSender = w3.to_checksum_address(address_in)
    nonce = w3.eth.get_transaction_count(addressSender)

    # Build the transaction
    amount_wei = w3.to_wei(amount, 'ether')
    tx_hash = contract.functions.withdraw(amount_wei).build_transaction({"chainId": Chain_id, "from": addressSender, "nonce": nonce, "gasPrice": 50000000000000000})

    # Sign the transaction
    signed_tx = w3.eth.account.sign_transaction(tx_hash, private_key=pk)

    # Send the transaction
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    return tx_receipt['transactionHash'].hex()

# Transfer from the TipBot contract

def top_up_tip(amount, address_in, pk):
    # Set the Ethereum Testnet RPC URL
    ETH_RPC_URL = os.getenv('ETH_RPC_URL')

    # Set the Ethereum Testnet contract address
    ETH_CONTRACT_ADDRESS = os.getenv('ETH_CONTRACT_ADDRESS')

    # Read the TipBot.json file as a JSON ABI
    with open('./blockchain/abi/TipBot.json', 'r') as file:
        abi = json.load(file)
        ETH_CONTRACT_ABI = abi["abi"]

    # Set the Web3 provider
    w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # initialize the chain id, we need it to build the transaction for replay protection
    Chain_id = w3.eth.chain_id

    # Set the contract
    address = w3.to_checksum_address(ETH_CONTRACT_ADDRESS)
    contract = w3.eth.contract(address=address, abi=ETH_CONTRACT_ABI)

    # Initialize address nonce
    addressSender = w3.to_checksum_address(address_in)
    nonce = w3.eth.get_transaction_count(addressSender)

    # Build the transaction
    amount_wei = w3.to_wei(amount, 'ether')
    tx_hash = contract.functions.topUp(amount_wei).build_transaction({"chainId": Chain_id, "from": addressSender, "nonce": nonce, "gasPrice": 50000000000000000})

    # Sign the transaction
    signed_tx = w3.eth.account.sign_transaction(tx_hash, private_key=pk)

    # Send the transaction
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    return tx_receipt['transactionHash'].hex()

def withdraw_tip_top_up(receiver, amount):
    print("withdraw_tip_top_up: receiver:", receiver, "amount:", amount)
    # Set the Ethereum Testnet RPC URL
    ETH_RPC_URL = os.getenv('ETH_RPC_URL')

    # Set the Ethereum Testnet contract address
    ETH_CONTRACT_ADDRESS = os.getenv('ETH_CONTRACT_ADDRESS')

    # Read the TipBot.json file as a JSON ABI
    with open('./blockchain/abi/TipBot.json', 'r') as file:
        abi = json.load(file)
        ETH_CONTRACT_ABI = abi["abi"]

    # Set the Ethereum Testnet private key
    ETH_PRIVATE_KEY = os.getenv('ETH_PRIVATE_KEY')

    # Set the Ethereum Testnet account address
    ETH_ACCOUNT_ADDRESS = os.getenv('ETH_ACCOUNT_ADDRESS')

    # Set the Web3 provider
    w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # initialize the chain id, we need it to build the transaction for replay protection
    Chain_id = w3.eth.chain_id

    # Set the contract
    address = w3.to_checksum_address(ETH_CONTRACT_ADDRESS)
    contract = w3.eth.contract(address=address, abi=ETH_CONTRACT_ABI)

    # Initialize address nonce
    addressSender = w3.to_checksum_address(ETH_ACCOUNT_ADDRESS)
    nonce = w3.eth.get_transaction_count(ETH_ACCOUNT_ADDRESS)
    
    addressReceiver = w3.to_checksum_address(receiver)
    amount_wei = w3.to_wei(amount, 'ether')
    tx_hash = contract.functions.tipTopUp(addressReceiver, amount_wei).build_transaction({"chainId": Chain_id, "from": addressSender, "nonce": nonce, "gasPrice": 50000000000000000})

    # Sign transaction
    signed_tx = w3.eth.account.sign_transaction(tx_hash, private_key=ETH_PRIVATE_KEY)
    
    # Send transaction
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    return tx_receipt['transactionHash'].hex()