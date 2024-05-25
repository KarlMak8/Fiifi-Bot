from functions import *

# Modify the user's profession based on the new level
profession_data = {
    2: ("Server", 1200, 1.5),
    3: ("Bartender", 2000, 2),
    4: ("Host/Hostess", 2800, 2.5),
    5: ("Line Cook", 4000, 3),
    6: ("Sous Chef", 5200, 3.5),
    7: ("Pastry Chef", 6400, 4),
    8: ("Restaurant Manager", 7600, 4.5),
    9: ("Sommelier", 8800, 5),
    10: ("Head Chef", 10000, 5.5),
    11: ("Restaurant Consultant", 11200, 6),
    12: ("Food and Beverage Manager", 12400, 6.5),
    13: ("Executive Chef", 13600, 7),
    14: ("Restaurant Owner", 14800, 7.5),
    15: ("Catering Manager", 16000, 8),
    16: ("Restaurant General Manager", 17200, 8.5),
    17: ("Restaurant Marketing Manager", 18400, 9),
    18: ("Menu Developer", 19600, 9.5),
    19: ("Restaurant Inspector", 20800, 10),
    20: ("Master Chef", 22000, 10.5)
}


async def promote(ctx):
    user_id = str(ctx.author.id)
    user_data = await load_user_data()
    if user_data[user_id]['level'] == 20:
        return
    # Check if the user meets the promotion criteria
    if user_data[user_id]['experience'] >= user_data[user_id]['promotion_criteria']:
        user_data[user_id]['level'] += 1
        user_data[user_id]['experience'] = 0
        
        level = user_data[user_id]['level']
        if level in profession_data:
            profession, promotion_criteria, promotion_multiplier = profession_data[level]
            user_data[user_id]['profession'] = profession
            user_data[user_id]['promotion_criteria'] = promotion_criteria
            user_data[user_id]['promotion_multiplier'] = promotion_multiplier
        # Add more cases for additional levels and professions
        await save_user_data(user_data)

        if user_data[user_id]['level'] == 20:
            embed = discord.Embed(
                title=":arrow_up: Promotion",
                description="Congratulations! You have reached the highest level.",
                color=discord.Color.gold()
            )
            embed.set_author(name=ctx.author.name)
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                title=":arrow_up: Promotion",
                description="Congratulations! You have been promoted.",
                color=discord.Color.green()
            )
            embed.set_author(name=ctx.author.name)
            await ctx.reply(embed=embed)
    else:
        return
