from functions import *
import random
from discord.ext import commands
from promote import promote
# Command to earn credits by working
def setup(bot):
    @bot.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def work(ctx):
        await open_account(ctx.author)
        user_id = str(ctx.author.id)
        user_data = await load_user_data()
        if user_data[user_id]['hunger'] < 1:
            await ctx.reply("You are too hungry! Buy some food. (Use the menu command.)") 
        earnings = random.randint(10, 50)
        exp = random.randint(10, 50)
        earnings *= user_data[user_id]["promotion_multiplier"]
        earnings = int(earnings)
        exp *= user_data[user_id]["promotion_multiplier"]
        exp = int(exp)
        user_data[user_id]['balance'] += earnings
        user_data[user_id]['experience'] += exp
        user_data[user_id]['hunger'] -= 1
        await save_user_data(user_data)
        progress_bar, progress = await progressbar(ctx.author)
        hunger_percentage = (user_data[user_id]['hunger'] / 20) * 100
        hunger_bar = ':blue_square:' * int(hunger_percentage / 16) + ':white_large_square:' * (6 - int(hunger_percentage / 16))
        embed = discord.Embed(title=":hammer_and_wrench: Work", description=f"You worked and earned {earnings:,d} credits.\nYou now have {user_data[user_id]['balance']:,d} credits.\nYou earned {exp} xp.", color=discord.Color.green())
        embed.add_field(name="Promotion Progress:", value=f"{progress_bar} - {progress:.2%}")
        embed.add_field(name="Hunger:", value=f"{hunger_bar} - {hunger_percentage}%")
        embed.set_author(name=ctx.author.name)
        await ctx.reply(embed=embed)
        await promote(ctx)
        
    @work.error
    async def work_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title="You're too tired.", color=discord.Color.red())
            em.add_field(name="Time Left:", value=f'{int(error.retry_after)} seconds')
            await ctx.reply(embed=em)