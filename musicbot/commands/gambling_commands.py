import discord
from config import config
from discord.ext import commands
from discord.ext.commands import has_permissions
import DB


class Gambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='balance')
    async def _balance(self, ctx):
        balance = 1000
        DB.cursor.execute('INSERT INTO user (discord_id, balance) VALUES (%s,%s,%s)', (ctx.message.author.id, balance))
        DB.db.commit()
        await ctx.send(f'{balance}lv were given to {ctx.message.author.mention}')


