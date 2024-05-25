import discord
from discord.ext import commands
import random
from functions import *

fish_list = [
    {"name": "Salmon", "rarity": "Common", "emoji": "🐟", "min_price": 10, "max_price": 20},
    {"name": "Tuna", "rarity": "Common", "emoji": "🐠", "min_price": 15, "max_price": 25},
    {"name": "Bass", "rarity": "Common", "emoji": "🎣", "min_price": 12, "max_price": 18},
    {"name": "Trout", "rarity": "Common", "emoji": "🍥", "min_price": 8, "max_price": 15},
    {"name": "Swordfish", "rarity": "Uncommon", "emoji": "🗡️", "min_price": 30, "max_price": 40},
    {"name": "Lobster", "rarity": "Uncommon", "emoji": "🦞", "min_price": 25, "max_price": 35},
    {"name": "Crab", "rarity": "Uncommon", "emoji": "🦀", "min_price": 20, "max_price": 30},
    {"name": "Snapper", "rarity": "Rare", "emoji": "🐌", "min_price": 40, "max_price": 50},
    {"name": "Mackerel", "rarity": "Rare", "emoji": "🐟", "min_price": 35, "max_price": 45},
    {"name": "Grouper", "rarity": "Legendary", "emoji": "🐬", "min_price": 60, "max_price": 80}
]
# Function to retrieve the fish emoji based on the fish name
def get_fish_emoji(fish_name):
    for fish in fish_list:
        if fish["name"] == fish_name:
            return fish["emoji"]

# Function to retrieve the price range of a fish
def get_fish_price(fish_name):
    for fish in fish_list:
        if fish["name"] == fish_name:
            price = f"{fish['min_price']} - {fish['max_price']} credits"
            return price

# Function to sell fish for a random amount within the price range
def sell_fish(fish_name):
    for fish in fish_list:
        if fish["name"] == fish_name:
            min_price = fish["min_price"]
            max_price = fish["max_price"]
            return random.randint(min_price, max_price)
        
def setup(bot):
    @commands.cooldown(1, 10, commands.BucketType.user)
    @bot.command()
    async def fish(ctx):
        user_data = await load_user_data()
        user_id = str(ctx.author.id)
        caught_fish = random.choice(fish_list)
        fish_name = caught_fish["name"]
        rarity = caught_fish["rarity"]
        emoji = caught_fish["emoji"]
        min_price = caught_fish["min_price"]
        max_price = caught_fish["max_price"]
        bag = user_data[user_id]["bag"]["fish"]

        found = False

        for i, (item, count) in enumerate(bag):
            if item == fish_name:
                # If the fish is already in the bag, increase its count by 1
                bag[i] = (item, count + 1)
                found = True
                break

        if not found:
            # If the fish is not in the bag, add it with count 1
            bag.append((fish_name, 1))

        await save_user_data(user_data)

        embed = discord.Embed(title="Fishing Results", color=discord.Color.blue())
        embed.add_field(name="Fish", value=f"{emoji} {fish_name}", inline=False)
        embed.add_field(name="Rarity", value=rarity, inline=False)
        embed.add_field(name="Price Range", value=f"{min_price} - {max_price} credits", inline=False)
        embed.set_footer(text="Happy fishing!")

        await ctx.reply(embed=embed)

    @fish.error
    async def fish_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title="You're too tired.", color=discord.Color.red())
            em.add_field(name="Time Left:", value=f'{int(error.retry_after)} seconds')
            await ctx.reply(embed=em)

    @bot.command()
    async def bag(ctx):
        user_data = await load_user_data()
        user_id = str(ctx.author.id)

        if user_id in user_data:
            bag = user_data[user_id]["bag"]["fish"]
            if not bag:
                await ctx.reply("Your bag is empty.")
            else:
                embed = discord.Embed(title="Your Fish Bag", color=discord.Color.blue())
                for fish in bag:
                    fish_name, count = fish
                    emoji = get_fish_emoji(fish_name)
                    price = get_fish_price(fish_name)
                    embed.add_field(name=f"{emoji} {fish_name} ({count})", value=f"Price: {price}", inline=True)
                await ctx.reply(embed=embed)
        else:
            await ctx.reply("You don't have a bag.")

    @bot.command()
    async def sell(ctx, fish_name, sell_amount: str = "1"):
        user_data = await load_user_data()
        user_id = str(ctx.author.id)
        bag = user_data[user_id]["bag"]["fish"]

        fish_name = fish_name.lower()  # Convert the input fish name to lowercase

        if sell_amount.lower() == "all":
            sell_amount = "all"

        for i, (item, count) in enumerate(bag):
            if item.lower() == fish_name:  # Compare lowercase fish names
                if sell_amount == "all":
                    sell_amount = count
                else:
                    sell_amount = int(sell_amount)
                    if sell_amount > count:
                        await ctx.reply("You don't have enough fish in your bag.")
                        return

                price = sell_fish(item) * sell_amount
                if sell_amount == count:
                    bag.pop(i)
                else:
                    bag[i] = (item, count - sell_amount)
                user_data[user_id]["bag"]["fish"] = bag
                user_data[user_id]["balance"] = user_data[user_id].get("balance", 0) + price  # Add the price to the balance
                
                # Add the fish to the user's account
                for _ in range(sell_amount):
                    user_data[user_id]["bag"]["fish"].append(item)

                await save_user_data(user_data)

                embed = discord.Embed(title="Fish Sold", color=discord.Color.green())
                embed.add_field(name="Fish", value=f"{get_fish_emoji(item)} {item}", inline=False)
                embed.add_field(name="Amount Sold", value=sell_amount, inline=False)
                embed.add_field(name="Total", value=f"{price} credits", inline=False)
                embed.add_field(name="Balance", value=f"{user_data[user_id]['balance']} credits", inline=False)  # Display the user's balance
                embed.set_footer(text="Thank you for selling!")

                await ctx.reply(embed=embed)
                return

        await ctx.reply("You don't have that fish in your bag.")


    @bot.command()
    async def sellall(ctx):
        user_data = await load_user_data()
        user_id = str(ctx.author.id)
        bag = user_data[user_id]["bag"]["fish"]

        if not bag:
            await ctx.reply("Your bag is empty.")
            return

        total_price = 0

        for item, count in bag:
            price = sell_fish(item) * count
            total_price += price

        user_data[user_id]["bag"]["fish"] = []  # Clear the bag
        user_data[user_id]["balance"] = user_data[user_id].get("balance", 0) + total_price  # Add the total price to the balance
        await save_user_data(user_data)

        embed = discord.Embed(title="Fish Sold", color=discord.Color.green())
        embed.add_field(name="Items Sold", value=f"All items in your bag", inline=False)
        embed.add_field(name="Total", value=f"{total_price:,d} credits", inline=False)
        embed.add_field(name="Balance", value=f"{user_data[user_id]['balance']:,d} credits", inline=False)  # Display the user's balance
        embed.set_footer(text="Thank you for selling!")

        await ctx.reply(embed=embed)

