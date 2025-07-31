from constants.globals import MAIN_SYMBOL

WALLET_NOT_FOUND = "Wallet not found {wallet}. Please select one of the available wallets or create a new one. 🤕 \n"
INSUFFICIENT_BALANCE = "Insufficient balance 🤕 \n"
INSUFFICIENT_INPUT_AMOUNT = "Insufficient input amount 🤕 \n"
INVALID_INPUT_AMOUNT = "Invalid input amount 🤕 \n"
INVALID_ADDRESS_PROVIDED = "Invalid address provided 🤕 \n"
TEXT_INVALID_AMOUNT = "The {text} could not be parsed as a valid amount. 🤕 \n"
TEXT_INVALID_TOKEN_SYMBOL = "The {text} could not be parsed as a valid whitelisted symbol. 🤕 \n"
TEXT_INVALID_AMOUNT_ADDRESS = "The {text} could not be parsed as a valid address fallowed by a valid amount. 🤕 \n"
TEXT_INVALID_AMOUNT_ADDRESS_SYMBOL = "The {text} could not be parsed as a valid address fallowed by a valid amount and a valid symbol. 🤕 \n"

EXAMPLE_AMOUNT = "\n\n Example: 1000, 1k, 1m, 1b \n"
EXAMPLE_AMOUNT_SYMBOL = "\n\n Example: 1000 $USDT, 1k $" + MAIN_SYMBOL + ", 1m $USDT, 1b $USDC \n"
EXAMPLE_ADDRESS = "\n\n Example: 0x1234... \n"
EXAMPLE_ADDRESS_AMOUNT = "\n\n Example: 0x1234... 1000 \n"
EXAMPLE_ADDRESS_AMOUNT_SYMBOL = "\n\n Example: '0x1234... 1m $USDT', '0x1234... 10k $" + MAIN_SYMBOL + "' \n"


# Messages Wallet
RESPONSE_WALLET_DEPOSIT_SUCCESS = """
💰✅

Deposit successful. 🎉

Amount: {amount} {symbol}

<a href='{url}'> View transaction </a>

"""

RESPONSE_WALLET_WITHDRAW_SUCCESS = """
📥✅

Withdraw successful. 🎉

Amount: {amount} {symbol}

<a href='{url}'> View transaction </a>

"""


RESPONSE_WALLET_TRANSFER_SUCCESS = """
📲✅

Transfer successful. 🎉

Amount: {amount} {symbol}

<a href='{url}'> View transaction </a>

"""

RESPONSE_WALLET_TOPUP_SUCCESS = """
💳✅

Topup successful. 🎉

Amount: {amount} {symbol}

<a href='{url}'> View transaction </a>

"""

RESPONSE_WALLET_EXPORT= """
🗝️ Your wallet PK is `{pk}`  

🔒 Do not share your private key with anyone
❌ DO NOT SHARE your pk with ANYONE


💣💣💣 Message self destructs in 10 seconds
After that you will automatically be redirected to reselect the wallet

"""

RESPONSE_WALLET_DEPOSIT_FAILED = """
💰❌

Deposit failed. 🤕

Amount: {amount} {symbol}

<a href='{url}'> View transaction </a>

"""

RESPONSE_WALLET_WITHDRAW_FAILED = """
📥❌

Withdraw failed. 🤕

Amount: {amount} {symbol}

<a href='{url}'> View transaction </a>

"""


RESPONSE_WALLET_TRANSFER_FAILED = """
📲❌

Transfer failed. 🤕

Amount: {amount} {symbol}

<a href='{url}'> View transaction </a>

"""

RESPONSE_WALLET_TOPUP_FAILED = """
💳❌

Transfer failed. 🤕

Amount: {amount} {symbol}

<a href='{url}'> View transaction </a>

"""

RESPONSE_WALLET_DELETE_SUCCESS = """
🗑️✅

Wallet {wallet} deleted. 🎉

"""

# Messages Withdraw
RESPONSE_WITHDRAW_OPTIONS = """
Withdraw 📥 $""" + MAIN_SYMBOL + """ to your wallet⛓️. 

Withdrawal options:
- Withdraw to an address (provide an address)
- Withdraw to a wallet (select one of your wallets)

Withdrawing $""" + MAIN_SYMBOL + """ comes with a fee of 5% of the amount.
"""

RESPONSE_WITHDRAW_MINIMUM = """
The minimum amount to withdraw is {amount} $""" + MAIN_SYMBOL + """ 
You have {balance} $""" + MAIN_SYMBOL + """ \n\n\n

This amount is for paying the fee
Insufficient balance. 🤕 \n\n\n
"""

RESPONSE_WITHDRAW_INPUT_AMOUNT = """
🏧 Withdraw 📥 $""" + MAIN_SYMBOL + """ & ERC20 tokens to your wallet⛓️. \n\n\n

Provide the amount you want to withdraw.
""" + EXAMPLE_AMOUNT


RESPONSE_WITHDRAW_INPUT_AMOUNT_SYMBOL = """
🏧 Withdraw 📥 $""" + MAIN_SYMBOL + """ & ERC20 tokens to your wallet⛓️. \n\n\n

Provide the amount you want to withdraw and the symbol.
""" + EXAMPLE_AMOUNT_SYMBOL

RESPONSE_WITHDRAW_INPUT_AMOUNT_ADDRESS = """
🏧 Withdraw 📥 $""" + MAIN_SYMBOL + """ & ERC20 tokens to your wallet⛓️. \n\n\n

Provide the address and the amount you want to withdraw.
""" + EXAMPLE_ADDRESS_AMOUNT

RESPONSE_WITHDRAW_INPUT_AMOUNT_ADDRESS_SYMBOL = """
🏧 Withdraw 📥 $""" + MAIN_SYMBOL + """ & ERC20 tokens to your wallet⛓️. \n\n\n

Provide the address and the amount and the symbol you want to withdraw.
""" + EXAMPLE_ADDRESS_AMOUNT_SYMBOL

RESPONSE_WITHDRAW_SUCCESS = """
🏧✅

Withdrawal successful. 🎉

Amount: {amount} {symbol}

<a href='{url}'> View transaction </a>
"""

RESPONSE_WITHDRAW_FAILED = """
🏧❌

Withdrawal failed. 🤕

Your amount is SAFU {amount} {symbol}
It is still in your wallet.

<a href='{url}'> Failed transaction </a>
"""

# Messages Balance
RESPONSE_BALANCE_MAIN = """
💰 Balance Telegram
- used for /tip
- used for /airdrop
- used for /rain

Your balance is {balance} $""" + MAIN_SYMBOL + """
"""

RESPONSE_BALANCE_MAIN_ONCHAIN = """
---------------------------------
💰⛓ Balance on #""" + MAIN_SYMBOL + """ Network
- used for /tipOnChain 5% fee for $TIP plus blockchain fees
- used for /airdropOnChain 5% fee for $TIP plus blockchain fees
- used for /rainOnChain 5% fee for $TIP plus blockchain fees

Wallets 👛 """

RESPONSE_BALANCE_MAIN_ONCHAIN_WALLET = """

⛓🔒 Your #{wallet} 
    Balance is {balance} $""" + MAIN_SYMBOL + """
"""

RESPONSE_BALANCE_MAIN_ONCHAIN_TIPBOT = """

    TipBot SmartContract 📜🤖
    Balance is {balance} $""" + MAIN_SYMBOL + """
"""
RESPONSE_BALANCE_ERC20_TELEGRAM = \
"""🛫{balance} {symbol} \n"""

RESPONSE_BALANCE_ERC20 = \
"""    ⛓{balance} {symbol} \n"""


RESPONSE_BALANCE_ERC20_TIPBOT = \
"""        🤖{balance} {symbol} \n"""



# Message Help
RESPONSE_HELP_MAIN = """
❓ Help
Tip BOT 🤖 is a bot that allows tips within groups.
It uses multi wallets and the """ + MAIN_SYMBOL + """ token to send tips on chain. 

Commands 👾:
/tip amount @user - tip a user
/tipOnChain amount @user - you must have an wallet with $TIP tokens
/help - provides the help menu
/balance - shows your balance

You can deposit, withdraw, topUp all in private.
<a href='{urlbot}'>Send me a private message </a>.

If you need help, please contact the admin.
"""