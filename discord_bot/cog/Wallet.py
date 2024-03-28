import nextcord
from nextcord.ext import commands

class Wallet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wallet(self, ctx):
        await ctx.send('Hello from your wallet!')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if 'hello' in message.content.lower():
            await message.channel.send('Hello there!')