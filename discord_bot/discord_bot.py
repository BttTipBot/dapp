import nextcord
from nextcord import Intents, Client, Message, Embed, File, ActionRow, ButtonStyle
from nextcord.ui import Button
from nextcord.ext import commands

from .cog.Wallet import Wallet
from .cog.Balance import Balance
from .cog.Start import Start

from typing import Final
from time import sleep
import os
import io
import logging
import random
from random import randint
from dotenv import load_dotenv
from .responses import get_response

from blockchain.tip_contract import tip_call
from charts.my_charts import create_chart
from db.users import get_command_by_t_username, set_command_by_t_username
from db.balances import get_balance_by_d_username

# STEP 0: LOAD OUR TOKEN FROM SOMEWHERE SAFE
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

description = '''Commands for the BTT TIP BOT

Tip, withdraw, deposit, transfer on the go.'''

# STEP 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True
intents.members = True

# client: Client = Client(intents=intents)
bot = commands.Bot(command_prefix='/', description=description, intents=intents)

# STEP 2: MESSAGE FUNCTIONALITY
# async def send_message(message: Message, user_message: str) -> None:
#     if not user_message:
#         print('(Message was empty because intents were not enabled probably)')
#         return

#     if is_private := user_message[0] == '?':
#         user_message = user_message[1:]

#     try:
#         response: str = get_response(user_message)
#         await message.author.send(response) if is_private else await message.channel.send(response)
#     except Exception as e:
#         print(e)


# STEP 3: HANDLING THE STARTUP FOR OUR BOT
@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is now running!')


# STEP 4: HANDLING INCOMING MESSAGES
# @bot.event
# async def on_message(message: Message) -> None:
#     if message.author == bot.user:
#         return

#     username: str = str(message.author)
#     user_message: str = message.content
#     channel: str = str(message.channel)

#     print(f'[{channel}] {username}: "{user_message}"')
#     await send_message(message, user_message)

# class MyView(discord.ui.View):
#     @discord.ui.select( # the decorator that lets you specify the properties of the select menu
#         placeholder = "Choose a Flavor!", # the placeholder text that will be displayed if nothing is selected
#         min_values = 1, # the minimum number of values that must be selected by the users
#         max_values = 1, # the maximum number of values that can be selected by the users
#         options = [ # the list of options from which users can choose, a required field
#             discord.SelectOption(
#                 label="Vanilla",
#                 description="Pick this if you like vanilla!"
#             ),
#             discord.SelectOption(
#                 label="Chocolate",
#                 description="Pick this if you like chocolate!"
#             ),
#             discord.SelectOption(
#                 label="Strawberry",
#                 description="Pick this if you like strawberry!"
#             )
#         ]
#     )
#     async def select_callback(self, interaction, select): # the function called when the user is done selecting options
#         await interaction.response.send_message(f"Awesome! I like {select.values[0]} too!")

# class MyModal(discord.ui.Modal):
#     def __init__(self, *args, **kwargs) -> None:
#         super().__init__(*args, **kwargs)

#         # self.add_item(InputText(label="Short Input"))
#         # self.add_item(InputText(label="Long Input", style=discord.InputTextStyle.long))

#     async def callback(self, interaction: discord.Interaction):
#         embed = discord.Embed(title="Modal Results")
#         embed.add_field(name="Short Input", value=self.children[0].value)
#         embed.add_field(name="Long Input", value=self.children[1].value)
#         await interaction.response.send_message(embeds=[embed])

# @bot.command()
# async def modal_slash(ctx):
#     """Shows an example of a modal dialog being invoked from a slash command."""
#     modal = MyModal(title="Modal via Slash Command")
#     await ctx.send_modal(modal)

# @bot.command()
# async def flavor(ctx):
#     await ctx.send("Choose a flavor!", view=MyView())

# #Define the balance command
# @bot.command(description='Check your balance.')
# async def balance(ctx):
#     """Check the balance of the user."""
#     user = ctx.author
#     balance = get_balance_by_d_username(user)
#     await ctx.send(f"Your balance is {balance} BTT.")

# Define the tip function
@bot.command(description='Tips the user with BTT tokens.')
async def tip(ctx, amount: int, receiver: str):
    """Send a tip to a user."""
    sender = ctx.author
    amount_in_wei = amount * (10 ** 18)
    print(f"Tip: sender={sender} amount={amount_in_wei} receiver={receiver}")
    await ctx.send(
        f"Tip successful! [Transaction explorer!](https://google.com)"
    )

    # tx_receipt = tip_call(receiver, amount_in_wei)

    # tx_link = f"https://bttcscan.com/tx/{tx_receipt['transactionHash'].hex()}"
    # await ctx.send(
    #     f"Tip successful! [Transaction explorer!]({tx_link})"
    # )

@bot.command(description='Just a simple reply on gm')
async def gm(ctx):
    """Send a message when the command /gm is issued."""
    user = ctx.author
    await ctx.send(f"gm {user.mention}!")

@bot.command(description='Simple reply on gn')
async def gn(ctx):
    """Send a message with a good night message and GIF when the command /gn is issued."""
    user = ctx.author
    good_night_messages = [
        "Sweet dreams!",
        "Sleep tight!",
        "Good night!"
    ]
    
    # List of good night GIF URLs (replace with your own URLs)
    gif_urls = [
        "assets/gif/gn.gif",
        "assets/gif/hi.gif",
        "assets/gif/gm.gif",
 
    ]
    
    # Randomly select a good night message
    selected_message = random.choice(good_night_messages)

    # Randomly select a GIF URL
    selected_gif_path = random.choice(gif_urls)

    # Send the embed
    await ctx.send(f"{selected_message} {user.mention}!", file=File(f'{selected_gif_path}'))


@bot.command(description='Just a simple reply on gm')
async def image(ctx):
    """Send a message when the command /gm is issued."""
    user = ctx.author
    imgBytes = create_chart()
    # Create a BytesIO object from the image bytes
    img_bytes_io = io.BytesIO(imgBytes)
    await ctx.send(file=File(fp=img_bytes_io, filename='image.png'))


# # Create a bot command wallet that has two commands: deposit and withdraw
# @bot.waller(description='Your associated wallet.')
# async def wallet(ctx):
    

def run_bot_discord():
    """Run the Discord bot."""
    # Run the bot
    bot.add_cog(Wallet(bot))
    bot.add_cog(Balance(bot))
    bot.add_cog(Start(bot))
    bot.run(TOKEN)