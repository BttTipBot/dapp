

# Tip Bot using web3 contract available on telegram and discord 


## Description
The bot uses firebase to store the information regarding users. 
As a unique key per user is used the telegram/discord username.

## Prerequisite
1. Create a firestore data and download the json in ./db name firebase.json
2. Initialize the DB (it saves some parameters)
```shell
python initialize.py
```
3. You will need an index on DB - HISTORY so the history is cronological

## Features
1. MultiWallet - you can store multiple wallets using this bot
2. Withdraw to one of your wallets or to an address
3. History
4. Can be used without a wallet


## Runing the bot both telegram and discord

```shell
python main.py
```


## Runing the bot only on telegram

```shell
python my_telegram_bot.py
```

## Runing the bot only on discord

```shell
python my_discord_bot.py
```

