import discord
import random
from config import config
from discord.ext import commands
from discord.ext.commands import has_permissions
from musicbot.commands import DB
from musicbot import gambling_utils

class Gambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='balance')
    async def _balance(self, ctx):
        discord_id = str(ctx.message.author.id)
        if discord_id in DB.get_all_ids():
            await ctx.send(f'Current balance: {DB.BalanceUtilisation.get_balance(discord_id)}$')
        else:
            balance = 1000
            DB.cursor.execute('INSERT INTO user_info (discord_id, balance) VALUES (%s,%s)', (discord_id, balance))
            DB.db.commit()
            await ctx.send(f'{balance}$. were given to {ctx.message.author.mention}. Current balance: {DB.BalanceUtilisation.get_balance(discord_id)}$')

    @commands.command(name='gamble')
    async def _gamble(self, ctx, amount, bet):
        discord_id = str(ctx.message.author.id)
        if discord_id in DB.get_all_ids():
            try:
                new_balance = 0
                amount = int(amount)
                balance = int(DB.BalanceUtilisation.get_balance(discord_id))
                if balance <= 0 or balance < amount:
                    await ctx.send('Not enough balance to make this bet.')
                else:
                    choice = random.choice(gambling_utils.wheel_numbers)
                    await ctx.send(file=discord.File(gambling_utils.get_wheel_number_path(choice)))
                    if bet == 'black' and choice in gambling_utils.wheel_numbers_black:
                        new_balance = balance + amount
                        DB.BalanceUtilisation.new_balance(discord_id, new_balance)
                        await ctx.send(f'{ctx.message.author.mention} won {amount}$')
                    elif bet == 'red' and choice in gambling_utils.wheel_numbers_red:
                        new_balance = balance + amount
                        DB.BalanceUtilisation.new_balance(discord_id, new_balance)
                        await ctx.send(f'{ctx.message.author.mention} won {amount}$')
                    elif bet == 'green' and choice == 0:
                        new_balance = balance + 14 * amount
                        DB.BalanceUtilisation.new_balance(discord_id, new_balance)
                        await ctx.send(f'{ctx.message.author.mention} won {14 * amount}$')
                    elif bet == 'even' and choice in [i for i in range(1, 36) if i % 2 == 0]:
                        new_balance = balance + 2 * amount
                        DB.BalanceUtilisation.new_balance(discord_id, new_balance)
                        await ctx.send(f'{ctx.message.author.mention} won {amount}$')
                    elif bet == 'odd' and choice in [i for i in range(1, 36) if i % 2 != 0]:
                        new_balance = balance + 2 * amount
                        DB.BalanceUtilisation.new_balance(discord_id, new_balance)
                        await ctx.send(f'{ctx.message.author.mention} won {amount}$')
                    else:
                        new_balance = balance - amount
                        DB.BalanceUtilisation.new_balance(discord_id, new_balance)
                        await ctx.send(f'{ctx.message.author.mention} lost {amount}$')

            except Exception:
                await ctx.send('Please type \'.gamble {ammount} {black/red/green}\'')
        else:
            await ctx.send('Type .balance to get your first 1000$')




def setup(bot):
    bot.add_cog(Gambling(bot))