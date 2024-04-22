
# Import the required libraries
import os
import json

from web3 import Web3
from web3.middleware import geth_poa_middleware
cache_erc20_abi = None


def get_erc20_balance(token_address, address_in):
    global cache_erc20_abi
    print("get_erc20_balance: address:", address_in)
    # Set the Ethereum Testnet RPC URL
    ETH_RPC_URL = os.getenv('ETH_RPC_URL')

    # Read the ERC20.json file as a JSON ABI
    if cache_erc20_abi is None:
        print("get_erc20_balance: Reading ERC20 ABI")
        with open('./blockchain/abi/ERC20.json', 'r') as file:
            abi_ec20 = json.load(file)
            cache_erc20_abi = abi_ec20

    # Set the Web3 provider
    w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # Set the contract
    token  = w3.to_checksum_address(token_address)
    contract = w3.eth.contract(address=token, abi=cache_erc20_abi)

    # Get the balance
    balance = contract.functions.balanceOf(address_in).call()
    decimals = contract.functions.decimals().call()

    balance = balance / 10**decimals
    print("get_erc20_balance: balance:", balance)

    return balance

def transfer_erc20_balance(erc20, sender, receiver, amount, pk):
    global cache_erc20_abi
    print("get_erc20_balance: sender:", sender)
    # Set the Ethereum Testnet RPC URL
    ETH_RPC_URL = os.getenv('ETH_RPC_URL')

    # Read the ERC20.json file as a JSON ABI
    if cache_erc20_abi is None:
        print("get_erc20_balance: Reading ERC20 ABI")
        with open('./blockchain/abi/ERC20.json', 'r') as file:
            abi_ec20 = json.load(file)
            cache_erc20_abi = abi_ec20

    # Set the Web3 provider
    w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # initialize the chain id, we need it to build the transaction for replay protection
    Chain_id = w3.eth.chain_id

    # Set the contract
    token  = w3.to_checksum_address(erc20)
    contract = w3.eth.contract(address=token, abi=cache_erc20_abi)

    # Get the balance
    decimals = contract.functions.decimals().call()
    amount = amount * 10**decimals

    addressReceiver = w3.to_checksum_address(receiver)
    addressSender = w3.to_checksum_address(sender)

    nonce = w3.eth.get_transaction_count(addressSender)
    tx_hash = contract.functions.transfer(addressReceiver, amount).build_transaction({"chainId": Chain_id, "from": addressSender, "nonce": nonce, "gasPrice": 50000000000000000})

    # Sign the transaction
    signed_tx = w3.eth.account.sign_transaction(tx_hash, private_key=pk)

    # Send the transaction
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    return tx_receipt['transactionHash'].hex()

def approve_erc20(token_address, ca, amount, address_in, pk):
    global cache_erc20_abi
    print("get_erc20_balance: address:", address_in)
    # Set the Ethereum Testnet RPC URL
    ETH_RPC_URL = os.getenv('ETH_RPC_URL')

    # Read the ERC20.json file as a JSON ABI
    if cache_erc20_abi is None:
        print("get_erc20_balance: Reading ERC20 ABI")
        with open('./blockchain/abi/ERC20.json', 'r') as file:
            abi_ec20 = json.load(file)
            cache_erc20_abi = abi_ec20

    # Set the Web3 provider
    w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # initialize the chain id, we need it to build the transaction for replay protection
    Chain_id = w3.eth.chain_id

    # Set the contract
    token  = w3.to_checksum_address(token_address)
    contract = w3.eth.contract(address=token, abi=cache_erc20_abi)

    # Get the balance
    decimals = contract.functions.decimals().call()
    amount = amount * 10**decimals
    addressSender = w3.to_checksum_address(address_in)
    contractAddress = w3.to_checksum_address(ca)
    nonce = w3.eth.get_transaction_count(addressSender)
    tx_hash = contract.functions.approve(contractAddress, amount).build_transaction({"chainId": Chain_id, "from": addressSender, "nonce": nonce, "gasPrice": 50000000000000000})

    # Sign the transaction
    signed_tx = w3.eth.account.sign_transaction(tx_hash, private_key=pk)

    # Send the transaction
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    return tx_receipt['transactionHash'].hex()