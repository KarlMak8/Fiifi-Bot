import discord
from discord.ext import commands
import json
from functions import *
def setup(bot):
    # Command to check user balance and profile
    @bot.command(aliases=["balance", "bal", "stats"])
    async def profile(ctx, user: discord.Member = None):
        if not user:
            user = ctx.message.author
        user_id = str(user.id)
        user_data = await load_user_data()
        await open_account(ctx.author)
        if str(user.id) not in user_data:
            await ctx.reply("This person is not in my database.")
        profile_embed = discord.Embed(title=f":bust_in_silhouette: {user.name}'s Profile", color=discord.Color.blue())
        profile_embed.add_field(name="Balance", value=f"{user_data[user_id]['balance']:,d} credits")
        profile_embed.add_field(name="Profession", value=user_data[user_id]['profession'])
        profile_embed.add_field(name="Level", value=user_data[user_id]['level'])

        experience = user_data[user_id]['experience']
        max_experience = user_data[user_id]['promotion_criteria']  # Adjust this value based on your leveling system

        progress_bar, progress = await progressbar(user)
        hunger_percentage = (user_data[user_id]['hunger'] / 20) * 100
        hunger_bar = ':blue_square:' * int(hunger_percentage / 16) + ':white_large_square:' * (6 - int(hunger_percentage / 16))
        # Add the progress bar to the embed
        profile_embed.add_field(name="Experience", value=f"{experience}/{max_experience}")
        profile_embed.add_field(name="Progress", value=progress_bar)
        
        profile_embed.add_field(name="Hunger", value=hunger_bar)
        await ctx.reply(embed=profile_embed)

    @bot.command(aliases=["pay"])
    async def send(ctx, member: discord.Member, amount=None):
        users = await load_user_data()
        await open_account(ctx.author)
        await open_account(member)
        if amount is None:
            await ctx.reply("Please enter the amount")
            return
        
        bal = users[str(ctx.author.id)]["balance"]

        amount = int(amount)

        if amount > bal:
            await ctx.reply('You do not have sufficient balance')
            return
        if amount < 0:
            await ctx.reply('Amount must be positive!')
            return

        users[str(ctx.author.id)]["balance"] -= amount
        users[str(member.id)]["balance"] += amount
        await save_user_data(users)
        await ctx.send(f'{ctx.author.mention} You gave {member.mention} {amount:,d} credits')
