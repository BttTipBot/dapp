# Import the required libraries
import os
import json

from .token_erc20 import approve_erc20
from .tx import check_tx_status

from web3 import Web3
from web3.middleware import geth_poa_middleware

cache_tipbot_abi = None
cache_erc20_abi = None


def tip_call(sender, receiver, amount, pk):
    global cache_tipbot_abi
    # Set the Ethereum Testnet RPC URL
    ETH_RPC_URL = os.getenv('ETH_RPC_URL')

    # Set the Ethereum Testnet contract address
    ETH_CONTRACT_ADDRESS = os.getenv('ETH_CONTRACT_ADDRESS')

    # Read the TipBot.json file as a JSON 
    if cache_tipbot_abi is None:
        print("tip_call: Reading TIPBOT ABI")
        with open('./blockchain/abi/TipBot.json', 'r') as file:
            abi = json.load(file)

    # Set the Web3 provider
    w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # initialize the chain id, we need it to build the transaction for replay protection
    Chain_id = w3.eth.chain_id

    # Set the contract
    address = w3.to_checksum_address(ETH_CONTRACT_ADDRESS)
    contract = w3.eth.contract(address=address, abi=cache_tipbot_abi)

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
    global cache_tipbot_abi
    print("get_tip_balance: address:", address_in)
    # Set the Ethereum Testnet RPC URL
    ETH_RPC_URL = os.getenv('ETH_RPC_URL')

    # Set the Ethereum Testnet contract address
    ETH_CONTRACT_ADDRESS = os.getenv('ETH_CONTRACT_ADDRESS')

    # Read the TipBot.json file as a JSON ABI
    if cache_tipbot_abi is None:
        print("get_tip_balance: Reading TIPBOT ABI")
        with open('./blockchain/abi/TipBot.json', 'r') as file:
            abi = json.load(file)
            cache_tipbot_abi = abi["abi"]

    # Set the Web3 provider
    w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # Set the contract
    address = w3.to_checksum_address(ETH_CONTRACT_ADDRESS)
    contract = w3.eth.contract(address=address, abi=cache_tipbot_abi)

    # Get the balance
    balance = contract.functions.getDepositedBalance(address_in).call()
    print("get_tip_balance: balance:", balance)

    balance = w3.from_wei(balance, 'ether')

    return balance

# Deposit into the TipBot contract
def deposit_tip(amount, address_in, pk):
    global cache_tipbot_abi
    # Set the Ethereum Testnet RPC URL
    ETH_RPC_URL = os.getenv('ETH_RPC_URL')

    # Set the Ethereum Testnet contract address
    ETH_CONTRACT_ADDRESS = os.getenv('ETH_CONTRACT_ADDRESS')

    # Read the TipBot.json file as a JSON 
    if cache_tipbot_abi is None:
        print("deposit_tip: Reading TIPBOT ABI")
        with open('./blockchain/abi/TipBot.json', 'r') as file:
            abi = json.load(file)
            cache_tipbot_abi = abi["abi"]

    # Set the Web3 provider
    w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # initialize the chain id, we need it to build the transaction for replay protection
    Chain_id = w3.eth.chain_id

    # Set the contract
    address = w3.to_checksum_address(ETH_CONTRACT_ADDRESS)
    contract = w3.eth.contract(address=address, abi=cache_tipbot_abi)

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
    global cache_tipbot_abi
    # Set the Ethereum Testnet RPC URL
    ETH_RPC_URL = os.getenv('ETH_RPC_URL')

    # Set the Ethereum Testnet contract address
    ETH_CONTRACT_ADDRESS = os.getenv('ETH_CONTRACT_ADDRESS')

    # Read the TipBot.json file as a JSON ABI
    if cache_tipbot_abi is None:
        print("withdraw_tip: Reading TIPBOT ABI")
        with open('./blockchain/abi/TipBot.json', 'r') as file:
            abi = json.load(file)
            cache_tipbot_abi = abi["abi"]

    # Set the Web3 provider
    w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # initialize the chain id, we need it to build the transaction for replay protection
    Chain_id = w3.eth.chain_id

    # Set the contract
    address = w3.to_checksum_address(ETH_CONTRACT_ADDRESS)
    contract = w3.eth.contract(address=address, abi=cache_tipbot_abi)

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
    global cache_tipbot_abi
    # Set the Ethereum Testnet RPC URL
    ETH_RPC_URL = os.getenv('ETH_RPC_URL')

    # Set the Ethereum Testnet contract address
    ETH_CONTRACT_ADDRESS = os.getenv('ETH_CONTRACT_ADDRESS')

    # Read the TipBot.json file as a JSON 
    if cache_tipbot_abi is None:
        print("top_up_tip: Reading TIPBOT ABI")
        with open('./blockchain/abi/TipBot.json', 'r') as file:
            abi = json.load(file)
            cache_tipbot_abi = abi["abi"]

    # Set the Web3 provider
    w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # initialize the chain id, we need it to build the transaction for replay protection
    Chain_id = w3.eth.chain_id

    # Set the contract
    address = w3.to_checksum_address(ETH_CONTRACT_ADDRESS)
    contract = w3.eth.contract(address=address, abi=cache_tipbot_abi)

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
    global cache_tipbot_abi
    print("withdraw_tip_top_up: receiver:", receiver, "amount:", amount)
    # Set the Ethereum Testnet RPC URL
    ETH_RPC_URL = os.getenv('ETH_RPC_URL')

    # Set the Ethereum Testnet contract address
    ETH_CONTRACT_ADDRESS = os.getenv('ETH_CONTRACT_ADDRESS')

    # Read the TipBot.json file as a JSON ABI
    if cache_tipbot_abi is None:
        print("withdraw_tip_top_up: Reading TIPBOT ABI")
        with open('./blockchain/abi/TipBot.json', 'r') as file:
            abi = json.load(file)
            cache_tipbot_abi = abi["abi"]

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
    contract = w3.eth.contract(address=address, abi=cache_tipbot_abi)

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




############## ERC20 TOKENS ####################

def get_tip_erc20_balance(token, address_in):
    global cache_erc20_abi
    global cache_tipbot_abi
    print("get_tip_balance: address:", address_in)
    # Set the Ethereum Testnet RPC URL
    ETH_RPC_URL = os.getenv('ETH_RPC_URL')

    # Set the Ethereum Testnet contract address
    ETH_CONTRACT_ADDRESS = os.getenv('ETH_CONTRACT_ADDRESS')

    # Read the TipBot.json file as a JSON ABI
    if cache_tipbot_abi is None:
        print("get_tip_erc20_balance: Reading TIPBOT ABI")
        with open('./blockchain/abi/TipBot.json', 'r') as file:
            abi = json.load(file)
            cache_tipbot_abi = abi["abi"]

    if cache_erc20_abi is None:
        print("get_tip_erc20_balance: Reading ERC20 ABI")
        with open('./blockchain/abi/ERC20.json', 'r') as file:
            abi_ec20 = json.load(file)
            cache_erc20_abi = abi_ec20

    # Set the Web3 provider
    w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # Set the contract
    address = w3.to_checksum_address(ETH_CONTRACT_ADDRESS)
    contract = w3.eth.contract(address=address, abi=cache_tipbot_abi)

    token_address = w3.to_checksum_address(token)
    token_contract = w3.eth.contract(address=token_address, abi=cache_erc20_abi)

    # Get the balance
    balance = contract.functions.getDepositedBalanceERC20(token_address, address_in).call()
    print("get_tip_balance: balance:", balance)

    decimals = token_contract.functions.decimals().call()

    balance = balance / 10**decimals

    return balance



# Deposit into the TipBot contract
def deposit_erc20(amount, address_in, pk, token):
    global cache_erc20_abi
    global cache_tipbot_abi
    # Set the Ethereum Testnet RPC URL
    ETH_RPC_URL = os.getenv('ETH_RPC_URL')

    # Set the Ethereum Testnet contract address
    ETH_CONTRACT_ADDRESS = os.getenv('ETH_CONTRACT_ADDRESS')

    # Go and approve first
    tx = approve_erc20(token, ETH_CONTRACT_ADDRESS, amount, address_in, pk)

    if check_tx_status(tx) == False:
        # The approval failed return the failed approve transaction
        return tx
    # Read the TipBot.json file as a JSON 
    if cache_tipbot_abi is None:
        print("deposit_erc20: Reading TIPBOT ABI")
        with open('./blockchain/abi/TipBot.json', 'r') as file:
            abi = json.load(file)
            cache_tipbot_abi = abi["abi"]

    if cache_erc20_abi is None:
        print("deposit_erc20: Reading ERC20 ABI")
        with open('./blockchain/abi/ERC20.json', 'r') as file:
            abi_ec20 = json.load(file)
            cache_erc20_abi = abi_ec20

    # Set the Web3 provider
    w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # initialize the chain id, we need it to build the transaction for replay protection
    Chain_id = w3.eth.chain_id

    # Set the contract
    address = w3.to_checksum_address(ETH_CONTRACT_ADDRESS)
    contract = w3.eth.contract(address=address, abi=cache_tipbot_abi)

    # Initialize address nonce
    addressSender = w3.to_checksum_address(address_in)
    nonce = w3.eth.get_transaction_count(addressSender)

    # Build the transaction
    token_address = w3.to_checksum_address(token)
    token_contract = w3.eth.contract(address=token_address, abi=cache_erc20_abi)
    decimals = token_contract.functions.decimals().call()

    amount_wei = amount * 10**decimals
    tx_hash = contract.functions.depositERC20(token_address, amount_wei).build_transaction({"chainId": Chain_id, "from": addressSender, "nonce": nonce, "gasPrice": 50000000000000000})

    # Sign the transaction
    signed_tx = w3.eth.account.sign_transaction(tx_hash, private_key=pk)

    # Send the transaction
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    return tx_receipt['transactionHash'].hex()


# Deposit into the TipBot contract
def withdraw_erc20(amount, address_in, pk, token):
    global cache_erc20_abi
    global cache_tipbot_abi
    # Set the Ethereum Testnet RPC URL
    ETH_RPC_URL = os.getenv('ETH_RPC_URL')

    # Set the Ethereum Testnet contract address
    ETH_CONTRACT_ADDRESS = os.getenv('ETH_CONTRACT_ADDRESS')

    # Read the TipBot.json file as a JSON 
    if cache_tipbot_abi is None:
        print("withdraw_erc20: Reading TIPBOT ABI")
        with open('./blockchain/abi/TipBot.json', 'r') as file:
            abi = json.load(file)
            cache_tipbot_abi = abi["abi"]

    if cache_erc20_abi is None:
        print("withdraw_erc20: Reading ERC20 ABI")
        with open('./blockchain/abi/ERC20.json', 'r') as file:
            abi_ec20 = json.load(file)
            cache_erc20_abi = abi_ec20

    # Set the Web3 provider
    w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # initialize the chain id, we need it to build the transaction for replay protection
    Chain_id = w3.eth.chain_id

    # Set the contract
    address = w3.to_checksum_address(ETH_CONTRACT_ADDRESS)
    contract = w3.eth.contract(address=address, abi=cache_tipbot_abi)

    # Initialize address nonce
    addressSender = w3.to_checksum_address(address_in)
    nonce = w3.eth.get_transaction_count(addressSender)

    token_address = w3.to_checksum_address(token)

    # Build the transaction
    token_contract = w3.eth.contract(address=token_address, abi=cache_erc20_abi)
    decimals = token_contract.functions.decimals().call()

    amount_wei = amount * 10**decimals
    tx_hash = contract.functions.withdrawERC20(token_address, amount_wei).build_transaction({"chainId": Chain_id, "from": addressSender, "nonce": nonce, "gasPrice": 50000000000000000})

    # Sign the transaction
    signed_tx = w3.eth.account.sign_transaction(tx_hash, private_key=pk)

    # Send the transaction
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    return tx_receipt['transactionHash'].hex()



# Deposit into the TipBot contract
def top_up_erc20(amount, address_in, pk, token):
    global cache_erc20_abi
    global cache_tipbot_abi
    # Set the Ethereum Testnet RPC URL
    ETH_RPC_URL = os.getenv('ETH_RPC_URL')

    # Set the Ethereum Testnet contract address
    ETH_CONTRACT_ADDRESS = os.getenv('ETH_CONTRACT_ADDRESS')

    # Read the TipBot.json file as a JSON 
    if cache_tipbot_abi is None:
        print("top_up_erc20: Reading TIPBOT ABI")
        with open('./blockchain/abi/TipBot.json', 'r') as file:
            abi = json.load(file)
            cache_tipbot_abi = abi["abi"]

    if cache_erc20_abi is None:
        print("top_up_erc20: Reading ERC20 ABI")
        with open('./blockchain/abi/ERC20.json', 'r') as file:
            abi_ec20 = json.load(file)
            cache_erc20_abi = abi_ec20

    # Set the Web3 provider
    w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # initialize the chain id, we need it to build the transaction for replay protection
    Chain_id = w3.eth.chain_id

    # Set the contract
    address = w3.to_checksum_address(ETH_CONTRACT_ADDRESS)
    contract = w3.eth.contract(address=address, abi=cache_tipbot_abi)

    # Initialize address nonce
    addressSender = w3.to_checksum_address(address_in)
    nonce = w3.eth.get_transaction_count(addressSender)

    token_address = w3.to_checksum_address(token)

    # Build the transaction
    token_contract = w3.eth.contract(address=token_address, abi=cache_erc20_abi)
    decimals = token_contract.functions.decimals().call()

    amount_wei = amount * 10**decimals
    tx_hash = contract.functions.topUpERC20(token_address, amount_wei).build_transaction({"chainId": Chain_id, "from": addressSender, "nonce": nonce, "gasPrice": 50000000000000000})

    # Sign the transaction
    signed_tx = w3.eth.account.sign_transaction(tx_hash, private_key=pk)

    # Send the transaction
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    return tx_receipt['transactionHash'].hex()


def tip_erc20_call(amount, address_in, receiver, pk, token):
    global cache_erc20_abi
    global cache_tipbot_abi
    # Set the Ethereum Testnet RPC URL
    ETH_RPC_URL = os.getenv('ETH_RPC_URL')

    # Set the Ethereum Testnet contract address
    ETH_CONTRACT_ADDRESS = os.getenv('ETH_CONTRACT_ADDRESS')

    # Read the TipBot.json file as a JSON 
    if cache_tipbot_abi is None:
        print("top_up_erc20: Reading TIPBOT ABI")
        with open('./blockchain/abi/TipBot.json', 'r') as file:
            abi = json.load(file)
            cache_tipbot_abi = abi["abi"]

    if cache_erc20_abi is None:
        print("top_up_erc20: Reading ERC20 ABI")
        with open('./blockchain/abi/ERC20.json', 'r') as file:
            abi_ec20 = json.load(file)
            cache_erc20_abi = abi_ec20

    # Set the Web3 provider
    w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # initialize the chain id, we need it to build the transaction for replay protection
    Chain_id = w3.eth.chain_id

    # Set the contract
    address = w3.to_checksum_address(ETH_CONTRACT_ADDRESS)
    contract = w3.eth.contract(address=address, abi=cache_tipbot_abi)

    # Initialize address nonce
    addressSender = w3.to_checksum_address(address_in)
    nonce = w3.eth.get_transaction_count(addressSender)

    token_address = w3.to_checksum_address(token)
    receiverAddress = w3.to_checksum_address(receiver)

    # Build the transaction
    token_contract = w3.eth.contract(address=token_address, abi=cache_erc20_abi)
    decimals = token_contract.functions.decimals().call()

    amount_wei = amount * 10**decimals
    tx_hash = contract.functions.tipERC20(token_address, receiverAddress, amount_wei).build_transaction({"chainId": Chain_id, "from": addressSender, "nonce": nonce, "gasPrice": 50000000000000000})

    # Sign the transaction
    signed_tx = w3.eth.account.sign_transaction(tx_hash, private_key=pk)

    # Send the transaction
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    return tx_receipt['transactionHash'].hex()


def withdraw_top_up_erc20_tip(receiver, amount, token):
    global cache_erc20_abi
    global cache_tipbot_abi
    # Set the Ethereum Testnet RPC URL
    ETH_RPC_URL = os.getenv('ETH_RPC_URL')

    # Set the Ethereum Testnet contract address
    ETH_CONTRACT_ADDRESS = os.getenv('ETH_CONTRACT_ADDRESS')
    
    # Set the Ethereum Testnet private key
    ETH_PRIVATE_KEY = os.getenv('ETH_PRIVATE_KEY')

    # Set the Ethereum Testnet account address
    ETH_ACCOUNT_ADDRESS = os.getenv('ETH_ACCOUNT_ADDRESS')

    # Read the TipBot.json file as a JSON 
    if cache_tipbot_abi is None:
        print("top_up_erc20: Reading TIPBOT ABI")
        with open('./blockchain/abi/TipBot.json', 'r') as file:
            abi = json.load(file)
            cache_tipbot_abi = abi["abi"]

    if cache_erc20_abi is None:
        print("top_up_erc20: Reading ERC20 ABI")
        with open('./blockchain/abi/ERC20.json', 'r') as file:
            abi_ec20 = json.load(file)
            cache_erc20_abi = abi_ec20

    # Set the Web3 provider
    w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # initialize the chain id, we need it to build the transaction for replay protection
    Chain_id = w3.eth.chain_id

    # Set the contract
    addressContract = w3.to_checksum_address(ETH_CONTRACT_ADDRESS)
    contract = w3.eth.contract(address=addressContract, abi=cache_tipbot_abi)

    # Initialize address nonce
    addressSender = w3.to_checksum_address(ETH_ACCOUNT_ADDRESS)
    nonce = w3.eth.get_transaction_count(addressSender)

    token_address = w3.to_checksum_address(token)
    receiverAddress = w3.to_checksum_address(receiver)

    # Build the transaction
    token_contract = w3.eth.contract(address=token_address, abi=cache_erc20_abi)
    decimals = token_contract.functions.decimals().call()

    amount_wei = amount * 10**decimals
    tx_hash = contract.functions.tipTopUpERC20(token_address, receiverAddress, amount_wei).build_transaction({"chainId": Chain_id, "from": addressSender, "nonce": nonce, "gasPrice": 50000000000000000})

    # Sign the transaction
    signed_tx = w3.eth.account.sign_transaction(tx_hash, private_key=ETH_PRIVATE_KEY)

    # Send the transaction
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    return tx_receipt['transactionHash'].hex()