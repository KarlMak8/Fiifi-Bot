import discord
import random
import json
from discord.ext import commands, tasks
import time
from functions import load_user_data, save_user_data, open_account, prefix

menu_items = [
    {"name": "🍕 Pizza", "price": 10, "foodpts": 6},
    {"name": "🍔 Burger", "price": 8, "foodpts": 6},
    {"name": "🍣 Sushi", "price": 15, "foodpts": 5},
    {"name": "🍚 Rice", "price": 5, "foodpts": 4},
    {"name": "🍝 Pasta", "price": 12, "foodpts": 6},
    {"name": "🥩 Steak", "price": 20, "foodpts": 6},
    {"name": "🥗 Salad", "price": 6, "foodpts": 3},
    {"name": "🧁 Cupcake", "price": 3, "foodpts": 3},
    {"name": "🍟 Fries", "price": 4, "foodpts": 3},
    {"name": "🍬 Candy", "price": 3, "foodpts": 2},
    {"name": "🌮 Tacos", "price": 10, "foodpts": 5},
    {"name": "🥤 Soda", "price": 2, "foodpts": 2}
]

def setup(bot):
    @bot.command()
    async def menu(ctx):
        await open_account(ctx.author)

        shop_embed = discord.Embed(title="Menu", description="Available Items", color=discord.Color.blue())

        for item in menu_items:
            shop_embed.add_field(name=item['name'], value=f"Price: {item['price']:,d} credits\nRestores: {item['foodpts']}", inline=True)
            shop_embed.set_footer(text="Use the buy command to buy items from the menu.")

        await ctx.reply(embed=shop_embed)

    @bot.command()
    async def buy(ctx, item_name, amount=1):
        await open_account(ctx.author)
        user_id = str(ctx.author.id)
        user_data = await load_user_data()

        found_item = None

        for item in menu_items:
            if item['name'][2:].lower() == item_name.lower():
                found_item = item
                break

        if not found_item:
            embed = discord.Embed(title="Purchase Failed", description="Item not found in the menu.", color=discord.Color.red())
            await ctx.reply(embed=embed)
            return

        total_price = found_item['price'] * amount
        if user_data[user_id]['balance'] < total_price:
            embed = discord.Embed(title="Purchase Failed", description="Insufficient credits to purchase the item(s).", color=discord.Color.red())
            await ctx.reply(embed=embed)
            return

        user_data[user_id]['balance'] -= total_price

        bag = user_data[user_id]['bag']['food']
        found = False

        for i, (item, count) in enumerate(bag):
            if item == found_item['name'][2:]:
                bag[i] = (item, count + amount)
                found = True
                break

        if not found:
            bag.append((found_item['name'][2:], amount))

        await save_user_data(user_data)

        item_plural = "s" if amount > 1 else ""
        purchase_embed = discord.Embed(title="Purchase Summary", description="You have purchased the following item(s):", color=discord.Color.green())
        purchase_embed.add_field(name=f"{found_item['name']} (x{amount})", value=f"Total Price: {total_price} credits", inline=False)
        purchase_embed.set_footer(text="Thank you for your purchase!")
        await ctx.reply(embed=purchase_embed)

    @bot.command(aliases=['food', 'listfood', 'myfood'])
    async def foodlist(ctx):
        await open_account(ctx.author)
        user_id = str(ctx.author.id)
        user_data = await load_user_data()

        bag = user_data[user_id]['bag']['food']

        if len(bag) == 0:
            embed = discord.Embed(title="Food List", description="Your food list is empty.", color=discord.Color.green())
            await ctx.reply(embed=embed)
            return

        food_list_embed = discord.Embed(title="Food List", color=discord.Color.green())

        for item, count in bag:
            item_name = next((menu_item['name'] for menu_item in menu_items if menu_item['name'][2:] == item), "")
            food_list_embed.add_field(name=f"{item_name}", value=f"Quantity: {count}", inline=True)

        food_list_embed.set_footer(text=f"Use '.eat <item>' to eat your food.")
        await ctx.reply(embed=food_list_embed)

    @bot.command()
    async def eat(ctx, item_name, amount=1):
        await open_account(ctx.author)
        user_id = str(ctx.author.id)
        user_data = await load_user_data()
        if item_name is None:
            embed = discord.Embed(title="Eating Failed", description="Please put in the food you want to eat.", color=discord.Color.red())
            await ctx.reply(embed=embed)
            return
        found_item = None

        for item in menu_items:
            if item['name'][2:].lower() == item_name.lower():
                found_item = item
                break
        
        if not found_item:
            embed = discord.Embed(title="Eating Failed", description="Item not found in the menu.", color=discord.Color.red())
            await ctx.reply(embed=embed)
            return

        bag = user_data[user_id]['bag']['food']
        found = False

        for i, (item, count) in enumerate(bag):
            if item == found_item['name'][2:]:
                if count >= amount:
                    bag[i] = (item, count - amount)
                    found = True
                else:
                    embed = discord.Embed(title="Eating Failed", description="You don't have enough of that item.", color=discord.Color.red())
                    await ctx.reply(embed=embed)
                    return
                break

        if not found:
            embed = discord.Embed(title="Eating Failed", description="You don't have that item in your food list.", color=discord.Color.red())
            await ctx.reply(embed=embed)
            return

        hunger = user_data[user_id]['hunger']
        hunger_restored = min(amount * found_item['foodpts'], 20 - hunger)
        user_data[user_id]['hunger'] += hunger_restored

        hunger_percentage = (user_data[user_id]['hunger'] / 20) * 100
        hunger_bar = ':blue_square:' * int(hunger_percentage / 16) + ':white_large_square:' * (6 - int(hunger_percentage / 16))

        if hunger >= 20:
            embed = discord.Embed(title="Eating Failed", description="You are already full!", color=discord.Color.red())
            await ctx.reply(embed=embed)
        else:
            if amount == 1:
                embed = discord.Embed(title="Bon appétit!", description=f"You ate {amount} {found_item['name']}.", color=discord.Color.green())
            else:
                embed = discord.Embed(title="Bon appétit!", description=f"You ate {amount} {found_item['name_plural']}.", color=discord.Color.green())
            embed.add_field(name="Hunger", value=f"{hunger_bar} {hunger_percentage}%", inline=False)
            await ctx.reply(embed=embed)

        if bag[i][1] == 0:
            del bag[i]

        await save_user_data(user_data)
