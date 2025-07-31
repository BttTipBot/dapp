from constants.globals import MAIN_SYMBOL


RESPONSE_WALLET_MENU = """
Wallet *{wallet}* 💰 

 `{address}` 
  
Balance: {balance} $""" + MAIN_SYMBOL + """
"""


RESPONSE_WALLET_DEPOSIT = """
Deposit to TipBot SmartContract 📜🤖

You can deposit $""" + MAIN_SYMBOL + """ or any whitelisted ERC20 tokens

Write the amount (could use b, m, k as suffixes) and the token symbol

If you write only the amount, the default token is $""" + MAIN_SYMBOL + """

Example: 1000 $TRX, 1k $USDT, 1m $TIP, 1b $""" + MAIN_SYMBOL + """

"""


RESPONSE_WALLET_WITHDRAW = """
Withdraw from TipBot SmartContract 📜🤖

You can deposit $""" + MAIN_SYMBOL + """ or any whitelisted ERC20 tokens

Write the amount (could use b, m, k as suffixes) and the token symbol

If you write only the amount, the default token is $""" + MAIN_SYMBOL + """

Example: 1000 $TRX, 1k $USDT, 1m $TIP, 1b $""" + MAIN_SYMBOL + """

"""



RESPONSE_WALLET_TOPUP = """
TOP UP from TipBot SmartContract 📜🤖 to 🛫 Telegram Balance

You can deposit $""" + MAIN_SYMBOL + """ or any whitelisted ERC20 tokens

Write the amount (could use b, m, k as suffixes) and the token symbol

If you write only the amount, the default token is $""" + MAIN_SYMBOL + """

Example: 1000 $TRX, 1k $USDT, 1m $TIP, 1b $""" + MAIN_SYMBOL + """

"""

RESPONSE_WALLET_TRANSFER   = """
Transfer on chain ⛓📲 ⛓

You can transfer $""" + MAIN_SYMBOL + """ or any whitelisted ERC20 tokens

Write the address and the amount (could use b, m, k as suffixes) and the token symbol

If you write only the amount, the default token is $""" + MAIN_SYMBOL + """

Example: 1000 $TRX 0xa..., 1k $USDT 0xa..., 1m $TIP 0xa..., 1b $""" + MAIN_SYMBOL + """ 0xa...


"""