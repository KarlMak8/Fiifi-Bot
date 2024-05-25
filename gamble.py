import discord
import json
import random
from discord.ext import commands
import time
import asyncio
from functions import *


def setup(bot):
    # Command to earn credits by gambling
    @bot.command(aliases=["g"])
    async def gamble(ctx, amount=None):
        user_data = await load_user_data()
        user = ctx.author
        await open_account(ctx.author)

        if user_data[str(user.id)]["in_game"] is True:
            await ctx.reply("You are already in a game.")
            return
        user_data[str(user.id)]["in_game"] = True
        await save_user_data(user_data)

        if amount is None:
            await ctx.reply(f"Please enter the bet amount.")
            return
        amount = int(amount)
        wallet = user_data[str(user.id)]["balance"]
        if amount > wallet:
            await ctx.reply(f"You don't have enough money!")
            return
        if amount < 0:
            await ctx.reply(f"Your number should be positive.")
            return
        if amount < 100:
            await ctx.reply(f"The bet amount should be over 100 credits.")
            return
        
        user_data[str(user.id)]["balance"] -= amount
        await save_user_data(user_data)

        em = discord.Embed(
            title=f"**Gamble** Playing...",
            color=discord.Color.green(),
            description=f"{ctx.author.mention} is playing the Gamble Game",
        )
        em.add_field(name="Bet Amount", value=f"**{amount:,d} credits**", inline=False)
        em.add_field(name="🔵", value=f"2x --- 50% Chance", inline=False)
        em.add_field(name="🟢", value=f"4x --- 25% Chance", inline=False)
        em.add_field(name="🔴", value=f"10x --- 10% Chance", inline=False)
        em.add_field(name="🟡", value=f"100x --- 1% Chance", inline=False)
        em.add_field(name="🚪", value=f"Cancel Game", inline=False)
        em.set_footer(text="Bot made by goopyahh")
        msg = await ctx.reply(embed=em)
        await msg.add_reaction("🔵")
        await msg.add_reaction("🟢")
        await msg.add_reaction("🔴")
        await msg.add_reaction("🟡")
        await msg.add_reaction("🚪")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["🔵", "🟢", "🔴", "🟡", "🚪"]

        while True:
            try:
                reaction, user = await bot.wait_for(
                    "reaction_add", timeout=60, check=check
                )

                if str(reaction.emoji) == "🔵":
                    await msg.remove_reaction(reaction, user)
                    chance = random.randint(1, 2)
                    if chance == 1:
                        user_data[str(user.id)]["balance"] += 2 * amount
                        await save_user_data(user_data)
                        wallet = user_data[str(user.id)]["balance"]
                        embed = discord.Embed(
                            title="You Win!",
                            color=discord.Color.green(),
                            description=f"{ctx.author.mention} won a **50%** chance gamble!",
                        )
                        embed.add_field(name="Bet Amount", value=f"{amount:,d} credits")
                        embed.add_field(name="Balance", value=f"{wallet:,d} credits")
                        embed.add_field(name="Chance to Win", value="50%", inline=False)
                        embed.add_field(name="Reward", value=f"+{amount:,d} credits")
                        await ctx.reply(embed=embed)
                        user_data[str(user.id)]["in_game"] = False 
                        await save_user_data(user_data) 
                        return
                    else:
                        wallet = user_data[str(user.id)]["balance"]
                        await save_user_data(user_data)
                        embed = discord.Embed(
                            title="You Lost.",
                            color=discord.Color.red(),
                            description=f"{ctx.author.mention} lost a **50%** chance gamble.",
                        )
                        embed.add_field(name="Bet Amount", value=f"{amount:,d} credits")
                        embed.add_field(name="Balance", value=f"{wallet:,d} credits")
                        embed.add_field(name="Chance to Win", value="50%")
                        embed.add_field(name="Reward", value=f"-{amount:,d} credits")
                        await ctx.reply(embed=embed)
                        user_data[str(user.id)]["in_game"] = False 
                        await save_user_data(user_data) 
                        return

                if str(reaction.emoji) == "🟢":
                    await msg.remove_reaction(reaction, user)
                    chance = random.randint(1, 4)
                    if chance == 1:
                        user_data[str(user.id)]["balance"] += 4 * amount
                        wallet = user_data[str(user.id)]["balance"]
                        await save_user_data(user_data)
                        embed = discord.Embed(
                            title="You Win!",
                            color=discord.Color.green(),
                            description=f"{ctx.author.mention} won a **25%** chance gamble!",
                        )
                        embed.add_field(name="Bet Amount", value=f"{amount:,d} credits")
                        embed.add_field(name="Balance", value=f"{wallet:,d} credits")
                        embed.add_field(name="Chance to Win", value="25%")
                        embed.add_field(name="Reward", value=f"+{3*amount:,d} credits")
                        await ctx.reply(embed=embed)
                        user_data[str(user.id)]["in_game"] = False 
                        await save_user_data(user_data) 
                        return
                    else:
                        wallet = user_data[str(user.id)]["balance"]
                        await save_user_data(user_data)
                        embed = discord.Embed(
                            title="You Lost.",
                            color=discord.Color.red(),
                            description=f"{ctx.author.mention} lost a **25%** chance gamble.",
                        )
                        embed.add_field(name="Bet Amount", value=f"{amount:,d} credits")
                        embed.add_field(name="Balance", value=f"{wallet:,d} credits")
                        embed.add_field(name="Chance to Win", value="25%")
                        embed.add_field(name="Reward", value=f"-{amount:,d} credits")
                        await ctx.reply(embed=embed)
                        user_data[str(user.id)]["in_game"] = False 
                        await save_user_data(user_data) 
                        return
                if str(reaction.emoji) == "🔴":
                    await msg.remove_reaction(reaction, user)
                    chance = random.randint(1, 10)
                    if chance == 1:
                        user_data[str(user.id)]["balance"] += 10 * amount
                        wallet = user_data[str(user.id)]["balance"]
                        await save_user_data(user_data)
                        embed = discord.Embed(
                            title="You Win!",
                            color=discord.Color.green(),
                            description=f"{ctx.author.mention} won a **10%** chance gamble!",
                        )
                        embed.add_field(name="Bet Amount", value=f"{amount:,d} credits")
                        embed.add_field(name="Balance", value=f"{wallet:,d} credits")
                        embed.add_field(name="Chance to Win", value="10%")
                        embed.add_field(name="Reward", value=f"+{9*amount:,d} credits")
                        await ctx.reply(embed=embed)
                        user_data[str(user.id)]["in_game"] = False 
                        await save_user_data(user_data) 
                        return
                    else:
                        wallet = user_data[str(user.id)]["balance"]
                        await save_user_data(user_data)
                        embed = discord.Embed(
                            title="You Lost.",
                            color=discord.Color.red(),
                            description=f"{ctx.author.mention} lost a **10%** chance gamble.",
                        )
                        embed.add_field(name="Bet Amount", value=f"{amount:,d} credits")
                        embed.add_field(name="Balance", value=f"{wallet:,d} credits")
                        embed.add_field(name="Chance to Win", value="10%")
                        embed.add_field(name="Reward", value=f"-{amount:,d} credits")
                        await ctx.reply(embed=embed)
                        user_data[str(user.id)]["in_game"] = False 
                        await save_user_data(user_data)
                        return
                if str(reaction.emoji) == "🟡":
                    await msg.remove_reaction(reaction, user)
                    chance = random.randint(1, 100)
                    if chance == 1:
                        user_data[str(user.id)]["balance"] += 100 * amount
                        wallet = user_data[str(user.id)]["balance"]
                        user_data[str(user.id)]["profit"] += 99 * amount
                        await save_user_data(user_data)
                        embed = discord.Embed(
                            title="You Win!",
                            color=discord.Color.green(),
                            description=f"{ctx.author.mention} won a **1%** chance gamble!",
                        )
                        embed.add_field(name="Bet Amount", value=f"{amount:,d} credits")
                        embed.add_field(name="Balance", value=f"{wallet:,d} credits")
                        embed.add_field(name="Chance to Win", value="1%")
                        embed.add_field(name="Reward", value=f"+{99*amount:,d} credits")
                        await ctx.reply(embed=embed)
                        user_data[str(user.id)]["in_game"] = False 
                        await save_user_data(user_data) 
                        return
                    else:
                        await msg.remove_reaction(reaction, user)
                        wallet = user_data[str(user.id)]["balance"]
                        await save_user_data(user_data)
                        embed = discord.Embed(
                            title="You Lost.",
                            color=discord.Color.red(),
                            description=f"{ctx.author.mention} lost a **1%** chance gamble.",
                        )
                        embed.add_field(name="Bet Amount", value=f"{amount:,d} credits")
                        embed.add_field(name="Balance", value=f"{wallet:,d} credits")
                        embed.add_field(name="Chance to Win", value="1%")
                        embed.add_field(name="Reward", value=f"-{amount:,d} credits")
                        await ctx.reply(embed=embed)
                        user_data[str(user.id)]["in_game"] = False 
                        await save_user_data(user_data) 
                        return
                if str(reaction.emoji) == "🚪":
                    user_data[str(user.id)]["balance"] += amount
                    await save_user_data(user_data)
                    wallet = user_data[str(user.id)]["balance"]
                    await msg.remove_reaction(reaction, user)
                    embed = discord.Embed(
                        title="Game Canceled",
                        color=discord.Color.blue(),
                        description=f"{ctx.author.mention} has canceled the game.",
                    )
                    embed.add_field(name="Bet Amount", value=f"{amount:,d} credits")
                    embed.add_field(name="Balance", value=f"{wallet:,d} credits")
                    await ctx.reply(embed=embed)
                    user_data[str(user.id)]["in_game"] = False 
                    await save_user_data(user_data)  
                    return

            except asyncio.TimeoutError:
                user_data[str(user.id)]["balance"] += amount
                await save_user_data(user_data)
                wallet = user_data[str(user.id)]["balance"]
                embed = discord.Embed(
                    title="Time's Up!",
                    color=discord.Color.orange(),
                    description=f"{ctx.author.mention} took too long to respond!",
                )
                embed.add_field(name="Bet Amount", value=f"{amount:,d} credits")
                embed.add_field(name="Balance", value=f"{wallet:,d} credits")
                await ctx.reply(embed=embed)
                user_data[str(user.id)]["in_game"] = False 
                await save_user_data(user_data) 
                return
            
    # Command: Coinflip
    @bot.command(aliases=['cf'])
    async def coinflip(ctx, amount=None, side=None):
        await open_account(ctx.author)
        side = side.lower()
        users = await load_user_data()
        user = ctx.author
        if amount == None or side == None:
            em = discord.Embed(title="Error", color=discord.Color.red())
            em.add_field(name="The correct format is:",
                        value=".cf [amount] [side]",
                        inline=False)
            await ctx.reply(embed=em)
            return

        bal = users[str(user.id)]["balance"]

        amount = int(amount)

        if amount > bal:
            await ctx.reply(f"{ctx.author.mention} You don't have enough money.")
            return
        if amount < 0:
            await ctx.reply('Amount must be positive!')
            return
        
        side = side.lower()
        if side == "heads" or side == "tails":
            determine_flip = ["heads", "tails"]
            if random.choice(determine_flip) == side:
                users[str(user.id)]["balance"] += amount
                await save_user_data(users)
                embed = discord.Embed(
                    title=f"You Chose {side.capitalize()} | You Win!",
                    color=discord.Color.green(),
                    description=f"{ctx.author.mention} Won a Coinflip, and **Won** {amount:,d} credits!")
                balance = users[str(user.id)]["balance"]
                embed.add_field(name="Balance", value=f"{balance:,d} credits", inline=False)
                await ctx.reply(embed=embed)
            else:
                users[str(user.id)]["balance"] -= amount
                await save_user_data(users)
                embed = discord.Embed(
                    title=f"You Chose {side.capitalize()} | You Lost!",
                    color=discord.Color.red(),
                    description=f"{ctx.author.mention} Lost a Coinflip, and **Lost** {amount:,d} credits!")
                balance = users[str(user.id)]["balance"]
                embed.add_field(name="Balance", value=f"{balance:,d} credits", inline=False)
                await ctx.reply(embed=embed)
        else:
            em = discord.Embed(title="Error", color=discord.Color.red())
            em.add_field(name="The correct format is:",
                        value=".cf [amount] [side]",
                        inline=False)
            await ctx.reply(embed=em)
            return
