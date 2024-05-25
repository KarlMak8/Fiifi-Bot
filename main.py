import discord
import json
from discord.ext import commands, tasks
import gamble, management, slots, income, hunger, fishing, tienlen
import helpCommand
from helpCommand import command_list
from datetime import datetime
from functions import *
import random

log_file = "logs.txt"

# Load the bot token and prefix from a configuration file
with open('config.json', 'r') as f:
    config = json.load(f)
TOKEN = config['token']
PREFIX = config['prefix']

# Define the bot's intents
intents = discord.Intents.all()
    
# Initialize the bot with intents
bot = commands.Bot(command_prefix=".", intents=intents)
# Function to update the presence
@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=discord.Game(name=f"Use .help! - {len(bot.guilds)} Servers"))


@bot.event
async def on_ready():
    change_status.start()
    print(f"Bot connected as {bot.user}")

    # Alter the database to add the "bag" column
    await alter_database()

    user_data = await load_user_data()

    for user in user_data:
        stats = {"balance", "profession", "level", "experience", "promotion_criteria", "promotion_multiplier", "hunger", "in_game", "bag"}
        missing_stats = []
        stat_values = {
            "balance": 2500,
            "profession": "Unemployed",
            "level": 1,
            "experience": 0,
            "promotion_criteria": 2000,
            "promotion_multiplier": 1,
            "hunger": 20,
            "in_game": False,
            "bag": {
                "fish": [],
                "food": []
            }
        }
        bag_items = {"fish": [], "food": []}

        for stat in stats:
            if stat not in user_data[user]:
                missing_stats.append(stat)
                # Add missing stat to user's account with corresponding value
                user_data[user][stat] = stat_values[stat]

        if "bag" not in user_data[user]:
            missing_stats.append("bag")
            user_data[user]["bag"] = bag_items
        else:
            for item in bag_items:
                if item not in user_data[user]["bag"]:
                    missing_stats.append(f"bag:{item}")
                    user_data[user]["bag"][item] = bag_items[item]

        if len(user_data[user].get("bag", {})) == 0:
            missing_stats.append("bag")
            user_data[user]["bag"] = bag_items
        else:
            for item in bag_items:
                if item not in user_data[user].get("bag", {}):
                    missing_stats.append(f"bag:{item}")
                    user_data[user]["bag"][item] = bag_items[item]

        if missing_stats:
            print(f"The following stats/items were missing for user {user} and have been added to their account:")
            for stat in missing_stats:
                print(f"{stat}: {user_data[user].get(stat)}")

    # Save the updated user data after all the missing stats and items have been added
    await save_user_data(user_data)

    for user in user_data:
        if user_data[user].get("in_game"):
            user_data[user]["in_game"] = False

    # Save the updated user data again
    await save_user_data(user_data)

    for user in user_data:
        if user_data[user]["in_game"]:
            user_data[user]["in_game"] = False

    # Save the updated user data again
    await save_user_data(user_data)
    

# Remove help command
bot.remove_command("help")    

management.setup(bot)
gamble.setup(bot)
slots.setup(bot)
helpCommand.setup(bot)
income.setup(bot)
hunger.setup(bot)
fishing.setup(bot)
tienlen.setup(bot)

@bot.event
async def on_guild_join(guild):
    with open('customprefixes.json', 'r') as f:
        prefixes = json.load(f)
    
    prefixes[str(guild.id)] = '.'

    with open("customprefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

@bot.event
async def on_guild_remove(guild):
    with open('customprefixes.json', 'r') as f:
        prefixes = json.load(f)
        
    if str(guild.id) in prefixes:
        prefixes.pop(str(guild.id))

    with open("customprefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)
# Open bank when user says something

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return
    if isinstance(message.channel, discord.abc.PrivateChannel):
        return
    
    prefixes = await getCustomPrefixes()
    server_prefix = prefixes[str(message.guild.id)]
    
    if message.content.startswith(server_prefix):
        await open_account(message.author)
        await bot.process_commands(message)
        # Log messages
        log_message = f"[{datetime.now()}] Message from {message.author} in {message.guild}: {message.content}\n"
        with open(log_file, "a") as f:
            f.write(log_message)
        
        # Advertise bot invite link randomly
        if random.randint(1, 100) <= 4:  # Adjust the probability as desired (5% in this case)
            invite_link = "https://discord.com/oauth2/authorize?client_id=993032065471762502&permissions=2147608640&scope=bot"
            invite_embed = discord.Embed(title="Invite Tao Lao!", description=f"Click [here]({invite_link}) to invite Tao Lao to your server.", color=discord.Color.green())
            invite_embed.set_footer(text="Thank you for using my bot!\nIf you need any help, or if you find a bug, heres my discord: 'goopyahh'")  # Add a footer
            await message.channel.send(embed=invite_embed)
    else:
        return
    
@bot.command(aliases=["prefix"])
@commands.has_permissions(administrator=True)
async def setprefix(ctx, prefix):
    # Update the prefix for the server
    with open("customprefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open("customprefixes.json", "w") as f:
        json.dump(prefixes, f, indent = 4)

    await ctx.send(f"Prefix set to `{prefix}`")
'''
#Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
        print(f"User {ctx.author} ({ctx.author.id}): {error}")


    if isinstance(error, commands.MissingRequiredArgument):
        # Missing required argument for a command
        command_name = ctx.command.name if ctx.command else "unknown command"
        await ctx.reply(f"Missing required argument for command '{command_name}'. If you need help, use the help command.")
    if isinstance(error, commands.CommandInvokeError):
        # Error occurred during command execution
        usage = command_list[str(ctx.command.name)]["usage"]
        await ctx.reply(f"Please use the correct format:\n{usage}")
        print(f"User {ctx.author} ({ctx.author.id}) Incorrect command usage: {ctx.message.content}")
    else:
        return
'''


@bot.command()
@commands.is_owner()
async def addmoney(ctx, id, amt):
    userdata = await load_user_data()
    if id not in userdata:
        await ctx.reply("That user is not in my database.")
    else:
        userdata[str(id)]["balance"] += int(amt)
        await save_user_data(userdata)
        await ctx.reply("Amount updated.")

@bot.command()
@commands.is_owner()
async def addexp(ctx, id, amt):
    userdata = await load_user_data()
    if id not in userdata:
        await ctx.reply("That user is not in my database.")
    else:
        userdata[str(id)]["experience"] += int(amt)
        await save_user_data(userdata)
        await ctx.reply("Amount updated.")

# Run the bot
bot.run(TOKEN)

