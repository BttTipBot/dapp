
USER_NOT_FOUND = "User not found! Call /start to register."
USER_NO_TRANSACTION = "No transactions found! Call /tip to send a tip."
USER_SENSITIVE_INFORMATION = "Click on my profile and <a href='https://t.me/bttc_tip_bot'>send me a private message </a>."


# BUTTONS
WALLET_BUTTON = "👛 Wallets"
WALLET_SELECT_BUTTON = "🔍 Select Wallet "
WALLET_DEPOSIT_BUTTON = "🛍️ Deposit "
WALLET_TOPUP_BUTTON = "💳 Topup Wallet "
WALLET_WITHDRAW_BUTTON = "💸 Withdraw "
WALLET_EXPORT_BUTTON = "📤 Export Wallet "
WALLET_ONCHAIN_TRANSFER_BUTTON = "➡️ Transfer "
WALLET_DELETE_BUTTON = "🗑️ Delete Wallet "
WALLET_GO_BACK_BUTTON = "🔙 Go Back"

WALLET_NEW_BUTTON = "🆕 New Wallet"
WALLET_GENERATE_BUTTON = "🔑 Generate Wallet"
WALLET_IMPORT_BUTTON = "📥 Import Wallet"
WALLET_PK_PROVIDED = "🔑 Private Key Provided"


WITHDRAW_BUTTON = "🏧 Withdraw BTT"
WITHDRAW_BUTTON_ON_ADDRESS = "✍🏻 Give your address"
WITHDRAW_BUTTON_ON_ACCOUNT = "📤 Use withdraw address "



USER_WALLET_TIP_BUTTON = "💸 Tip On Chain"
USER_HELP_BUTTON = "❓ Help"
USER_BALANCE_BUTTON = "💰 Balance"
USER_HISTORY_BUTTON = "📜 History"
USER_MAIN_MENU_BUTTON = "🏠 Main Menu"

# Users
USER_NEW_USER_ADDED = "CREATED"
USER_ERROR_USER_EXISTS = "User already exists."
USER_WELCOME_BONUS_MESSAGE = "🎉 You received a welcome bonus of {amount} BTT!"

# Tips Messages
TIP_RECEIVED_MESSAGE = "🎉 You received a tip of {amount} BTT from @{sender}!"
TIP_WELCOME_AMOUNT = "🎉 You received a welcome tip of {amount} BTT!"
TIP_INSUFFICIENT_BALANCE = "Insufficient balance. 🤕 \n\n\n Your balance is {balance} {symbol}. Provide a number smaller than {max}"
RAIN_INSUFFICIENT_BALANCE = "Insufficient balance. 🤕 \n\n\n Your balance is {balance} $BTT. Provide a number smaller than {max}"
AIRDROP_INSUFFICIENT_BALANCE = "Insufficient balance. 🤕 \n\n\n Your balance is {balance} $BTT. Provide a number smaller than {max}"

# Mesaages Wallet
MESSAGE_NO_WALLET = "You don't have a wallet. Please create one."
MESSAGE_CHOSE_WALLET = "Choose your wallet:"
MESSAGE_WALLET_NOT_FOUND = "Wallet not found '{wallet}'. Please select one of the available wallets or create a new one."
MESSAGE_WALLET_MENU = "Wallet *{wallet}* 💰  \n\n Address `{address}` \n\n  Balance of {balance} $BTT \n\n 💵 Balance Tips on Chain: {balance_tips} $TIP"
MESSAGE_WALLET_INSUFFICIENT_FEE = "Insufficient balance. 🤕 \n\n\n  You need to have at least {fee} $BTT in your wallet for transaction fee."
MESSAGE_WALLET_INSUFFICIENT_BALANCE = """
Insufficient balance. 🤕 

Your balance is {balance} {symbol}
🙏🏼 Please provide a number within your balance.
"""

MESSAGE_WALLET_DEPOSIT = """
Deposit to your wallet $TIP. 
 1 $BTT = 1 $TIP \n\n Please write how many $BTT you want to deposit. 
  
 You could use also b (billion), m (million) or k (thousand) as suffixes. 

 Example: 1000, 1k, 1m, 1b
"""
MESSAGE_WALLET_WITHDRAW = "Withdraw to your wallet $BTT from $TIP. \n\n 1 $BTT = 1 $TIP \n\n Please write how many $TIP you want to withdraw. \n\n You could use also b (billion), m (million) or k (thousand) as suffixes. \n\n Example: 1000, 1k, 1m, 1b"

MESSAGE_WALLET_INSUFFICIENT_TIP = """
Insufficient balance. 🤕
 
Your balance is {balance} {symbol}
🙏🏼 Please provide a number within your balance.
"""
MESSAGE_WALLET_TRANSFER_ON_CHAIN = "Transfer $BTT to another wallet. Please write the address to transfer the $BTT and the amount. \n\n Example: 0x1234... 1000"
MESSAGE_WALLET_TOP_UP = "Top up your telegram/discord wallet with tips.\n\n We will withdraw the amount from chain and bring it to your balance. \n\n Please write the amount to top up. \n\n Example: 1000, 1k, 1m, 1b"

# Default values:
DEFAULT_WELCOME_BACK_MESSAGE = "👋 Welcome back @{user} to the BTT TIP community!"
DEFAULT_WELCOME_MESSAGE = "👋 Welcome to the BTT TIP community @{user}!"
DEFAULT_NO_FALLBACK_MESSAGE = "Sorry, I didn't understand that command."
