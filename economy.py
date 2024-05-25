import discord
import random
from discord.ext import commands
import time
from functions import load_user_data, save_user_data, progressbar, open_account

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
            await ctx.reply("This person is not in my database. (Use .work)")
        profile_embed = discord.Embed(title=f":bust_in_silhouette: {user.name}'s Profile", color=discord.Color.blue())
        profile_embed.add_field(name="Balance", value=f"{user_data[user_id]['balance']:,d} credits")
        profile_embed.add_field(name="Profession", value=user_data[user_id]['profession'])
        profile_embed.add_field(name="Level", value=user_data[user_id]['level'])

        experience = user_data[user_id]['experience']
        max_experience = user_data[user_id]['promotion_criteria']  # Adjust this value based on your leveling system

        progress_bar, progress = await progressbar(user)
        
        # Add the progress bar to the embed
        profile_embed.add_field(name="Experience", value=f"{experience}/{max_experience}")
        profile_embed.add_field(name=f"Progress-{progress:.2%}", value=progress_bar)
        
        profile_embed.add_field(name="Promotion Criteria", value=user_data[user_id].get('promotion_criteria', 'N/A'))
        await ctx.reply(embed=profile_embed)

    @bot.command()
    async def menu(ctx):
        await open_account(ctx.author)
        menu_items = [
            {"name": "🍕 Pizza", "price": 10},
            {"name": "🍔 Burger", "price": 8},
            {"name": "🍣 Sushi", "price": 15},
            {"name": "🍦 Ice Cream", "price": 5},
            {"name": "🍝 Pasta", "price": 12},
            {"name": "🥩 Steak", "price": 20},
            {"name": "🥗 Salad", "price": 6},
            {"name": "🧁 Cupcake", "price": 3},
            {"name": "🍟 Fries", "price": 4},
            {"name": "☕️ Coffee", "price": 3},
            {"name": "🌮 Tacos", "price": 10},
            {"name": "🥤 Soda", "price": 2}
        ]

        shop_embed = discord.Embed(title="Menu", description="Available Items", color=discord.Color.blue())

        for item in menu_items:
            shop_embed.add_field(name=item['name'], value=f"Price: {item['price']:,d} credits", inline=True)


        await ctx.reply(embed=shop_embed)

    @bot.command()
    async def buy(ctx, item_name):
        await open_account(ctx.author)
        user_id = str(ctx.author.id)
        user_data = await load_user_data()
        menu_items = [
            {"name": "🍕 Pizza", "price": 10},
            {"name": "🍔 Burger", "price": 8},
            {"name": "🍣 Sushi", "price": 15},
            {"name": "🍦 Ice Cream", "price": 5},
            {"name": "🍝 Pasta", "price": 12},
            {"name": "🥩 Steak", "price": 20},
            {"name": "🥗 Salad", "price": 6},
            {"name": "🧁 Cupcake", "price": 3},
            {"name": "🍟 Fries", "price": 4},
            {"name": "☕️ Coffee", "price": 3},
            {"name": "🌮 Tacos", "price": 10},
            {"name": "🥤 Soda", "price": 2}
        ]
        # Find the item in the shop based on the provided item_name

        for item in menu_items:
            if item['name'][2:].lower() == item_name.lower():
                # Item found
                break
            else:
                # Item not found
                item = None

        if not item:
            await ctx.reply("Item not found in the menu.")
            return

        # Check if the user has enough credits to purchase the item
        if user_data[user_id]['balance'] < item['price']:
            await ctx.reply("Insufficient credits to purchase the item.")
            return

        # Deduct the item price from the user's balance and save the updated data
        user_data[user_id]['balance'] -= item['price']
        await save_user_data(user_data)

        await ctx.reply(f"Congratulations! You have purchased {item['name']} for {item['price']} credits.")