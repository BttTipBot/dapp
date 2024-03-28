
from nextcord.ext import commands

from db.balances import get_balance_by_d_username
from constants.responses import RESPONSE_BALANCE_MAIN

class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def balance(self, ctx):
        user = ctx.author
        print(f'user="{user}"')
        balance = get_balance_by_d_username(user.name)
        await ctx.send(RESPONSE_BALANCE_MAIN.format(balance=balance))