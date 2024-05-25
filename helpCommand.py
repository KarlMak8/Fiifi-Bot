import discord
from functions import getCustomPrefixes
categories = {
    "💰 Economy": {
        "work": {
            "description": "Work your way up from rags to riches. Become the wealthiest person in the server!",
            "usage": f"`work`"
        },
        "profile": {
            "description": "Take a look at your profile and see how far you've come on your economic journey.",
            "usage": f"`profile <mention user>`"
        }
    },
    "🎲 Gambling": {
        "coinflip": {
            "description": "Take a chance and flip a coin. Will luck be on your side?",
            "usage": f"`coinflip <bet amount> <heads or tails>`"
        },
        "gamble": {
            "description": "Feeling lucky? Place a bet and try your luck in this exciting gambling game.",
            "usage": f"`gamble <bet amount>`"
        },
        "slots": {
            "description": "Spin the slots and test your fortune. Will you hit the jackpot?",
            "usage": f"`slots play`"
        }
    },
    "🍔 Food": {
        "menu": {
            "description": "Hungry? Check out the delicious menu options and satisfy your cravings.",
            "usage": "`menu`"
        },
        "buy": {
            "description": "Indulge yourself by purchasing delectable food items from the menu.",
            "usage": "`buy <item> <amount>`"
        },
        "eat": {
            "description": "Eat a food item from your inventory to restore your hunger.",
            "usage": "`eat <item>`"
        },
        "food": {
            "description": "View the list of food items in your inventory.",
            "usage": "`food`"
        }
    },
    "🏦 Bank": {
        "send": {
            "description": "Share your wealth with others by sending money to fellow server members.",
            "usage": f"`send <mention user> <amount>`"
        }
    },
    "🎣 Fishing": {
        "fish": {
            "description": "Grab your fishing rod and head to the nearest body of water. Catch amazing fish and become a master angler.",
            "usage": f"`fish`"
        },
        "bag": {
            "description": "Explore the contents of your fishing bag and admire the variety of fish you've collected.",
            "usage": f"`bag`"
        },
        "sell": {
            "description": "Sell a specific amount of fish and earn some extra credits.",
            "usage": f"`sell <fish name> <amount>`"
        },
        "sellall": {
            "description": "Looking to make a big profit? Sell all the fish in your bag and watch the credits roll in.",
            "usage": f"`sellall`"
        }
    },
    "🔧 Misc.": {
        "prefix": {
            "description": "Customize the bot to your liking by setting a new prefix for commands.",
            "usage": f"`prefix <new prefix>`"
        }
    }
}
command_list = {
        "work": {
            "description": "Work your way up from rags to riches. Become the wealthiest person in the server!",
            "usage": f"`work`"
        },
        "profile": {
            "description": "Take a look at your profile and see how far you've come on your economic journey.",
            "usage": f"`profile <mention user>`"
        },
        "coinflip": {
            "description": "Take a chance and flip a coin. Will luck be on your side?",
            "usage": f"`coinflip <bet amount> <heads or tails>`"
        },
        "gamble": {
            "description": "Feeling lucky? Place a bet and try your luck in this exciting gambling game.",
            "usage": f"`gamble <bet amount>`"
        },
        "slots": {
            "description": "Spin the slots and test your fortune. Will you hit the jackpot?",
            "usage": f"`slots play`"
        },
        "menu": {
            "description": "Hungry? Check out the delicious menu options and satisfy your cravings.",
            "usage": f"`menu`"
        },
        "buy": {
            "description": "Indulge yourself by purchasing delectable food items from the menu.",
            "usage": f"`buy <item> <amount>`"
        },
        "send": {
            "description": "Share your wealth with others by sending money to fellow server members.",
            "usage": f"`send <mention user> <amount>`"
        },
        "fish": {
            "description": "Grab your fishing rod and head to the nearest body of water. Catch amazing fish and become a master angler.",
            "usage": f"`fish`"
        },
        "bag": {
            "description": "Explore the contents of your fishing bag and admire the variety of fish you've collected.",
            "usage": f"`bag`"
        },
        "sell": {
            "description": "Sell a specific amount of fish and earn some extra credits.",
            "usage": f"`sell <fish name> <amount>`"
        },
        "sellall": {
            "description": "Looking to make a big profit? Sell all the fish in your bag and watch the credits roll in.",
            "usage": f"`sellall`"
        },
        "prefix": {
            "description": "Customize the bot to your liking by setting a new prefix for commands.",
            "usage": f"`prefix <new prefix>`"
        },
        "tienlen": {
            "description": "Play tienlen",
            "usage": f"`tienlen`"
        }
    }

def setup(bot):
    @bot.command(aliases=["botinfo"])
    async def help(ctx, *, command_name=None):
        get_prefix = await getCustomPrefixes()
        prefix = get_prefix[str(ctx.guild.id)]

        if command_name is None:
            # Show all categories and commands
            embed = discord.Embed(title="📚 Command Categories", color=0x00ccff)
            
            for category, cmds in categories.items():
                command_list = " ".join([f"`{prefix}{cmd}`" for cmd, cmd_info in cmds.items()])
                embed.add_field(name=f"{category}", value=command_list, inline=False)
            
            embed.set_footer(text=f"For more info on a specific command, use {prefix}help <command>")
            
            await ctx.reply(embed=embed)
        else:
            # Show command details
            command_name = command_name.lower()
            
            for category, cmds in categories.items():
                if command_name in cmds:
                    cmd_info = cmds[command_name]
                    description = cmd_info['description']
                    usage = cmd_info.get('usage', '')
                    embed = discord.Embed(title=f"📝 Command: {prefix}{command_name}", description=description, color=0x00ccff)
                    if usage:
                        embed.add_field(name="Usage", value=(f"{prefix}{usage}"), inline=False)
                    await ctx.reply(embed=embed)
                    return
