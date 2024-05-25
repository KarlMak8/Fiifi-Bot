import discord
import random
import asyncio
from functions import *

# Define the payouts for different symbol combinations
payouts = {
    ('💎', '💎', '💎'): 2500,     # Three diamonds
    ('⭐', '⭐', '⭐'): 1000,       # Three stars
    ('🔔', '🔔', '🔔'): 400,      # Three bells
    ('🍇', '🍇', '🍇'): 200,      # Three grapes
    ('🍊', '🍊', '🍊'): 100,       # Three oranges
    ('🍒', '🍒', '🍒'): 50,       # Three cherries
    ('🍒', '🍒', None): 7,       # Two cherries
    ('🍒', None, None): 5,      # One cherry
    ('💰', '💰', '💰'): 50000,    # Jackpot: Three money bags
}

payouts_display = {
    ('💎', '💎', '💎'): 2500,     # Three diamonds
    ('⭐', '⭐', '⭐'): 1000,       # Three stars
    ('🔔', '🔔', '🔔'): 400,      # Three bells
    ('🍇', '🍇', '🍇'): 200,      # Three grapes
    ('🍊', '🍊', '🍊'): 100,       # Three oranges
    ('🍒', '🍒', '🍒'): 50,       # Three cherries
    ('🍒', '🍒'): 7,       # Two cherries
    ('🍒'): 5,      # One cherry
    ('💰', '💰', '💰'): 50000,    # Jackpot: Three money bags
}

def setup(bot):
    # Slot machine command
    @bot.command()
    async def slots(ctx, ready=None):
        await open_account(ctx.author)
        symbols = ['💎', '⭐', '🔔', '🍇', '🍊', '🍒', '💰']
        if ready is None or ready.lower() != "play":
            embed = discord.Embed(title="Slot Machine Payouts", description="Here are the payouts for the slot machine:")
            for symbols, payout in payouts_display.items():
                symbol_str = ' '.join(symbols) if len(symbols) > 1 else symbols[0]
                embed.add_field(name=symbol_str, value=f"Payout: {payout} credits", inline=False)
            get_Prefixes = await getCustomPrefixes()
            embed.set_footer(text=f"Use '{get_Prefixes[str(ctx.guild.id)]}slots play' to play.")
            # Customize the appearance of the embed
            embed.color = discord.Color.blue()
            # Send the embed message
            await ctx.reply(embed=embed)

        if ready is not None and ready.lower() == "play":
            user_data = await load_user_data()
            user = ctx.author
            if user_data[str(user.id)]["in_game"]:
                await ctx.reply("You are already in a game.")
                return
            user_data[str(user.id)]["in_game"] = True
            await save_user_data(user_data)
            # Check if the user has enough credits to play
            if user_data[str(user.id)]["balance"] < 5:
                await ctx.reply("You do not have enough credits to play slots. (5 credits)")
                user_data[str(user.id)]["in_game"] = False
                await save_user_data(user_data)
                return

            # Create the initial slot machine embed message
            embed = discord.Embed(title="Slot Machine", description=":question: :question: :question:", color=discord.Color.blue())

            # Add the exit button
            embed.add_field(name="Exit", value=":x:", inline=True)

            # Send the initial embed message
            result_message = await ctx.reply(embed=embed)

            # Add the reaction button to the message
            await result_message.add_reaction("🎰")

            # Add the exit button reaction
            await result_message.add_reaction("❌")

            # Wait for the user to press a reaction button
            def check(reaction, user):
                return user == ctx.author and reaction.message.id == result_message.id and (
                        reaction.emoji in str(reaction.emoji) == "🎰" or str(reaction.emoji) == "❌")

            while True:
                try:
                    reaction, _ = await bot.wait_for("reaction_add", timeout=60.0, check=check)

                    # Check if the user clicked the exit button
                    if str(reaction.emoji) == "❌":
                        await result_message.edit(content="Slot machine game has been exited.")
                        user_data[str(user.id)]["in_game"] = False
                        await save_user_data(user_data)
                        break
                    if str(reaction.emoji) == "🎰":
                        if user_data[str(user.id)]["balance"] < 5:
                            await ctx.reply("You do not have enough credits to play slots. (5 credits)")
                            user_data[str(user.id)]["in_game"] = False
                            await save_user_data(user_data)
                            return
                        user_data[str(user.id)]["balance"] -= 5
                        await save_user_data(user_data)
                        # Generate three random symbols
                        result = [random.choice(symbols) for _ in range(3)]
                        # Format the result as a string
                        result_string = ' '.join(result)

                        # Calculate the payout based on the result
                        payout = 0
                        if tuple(result) in payouts:
                            payout = payouts[tuple(result)]
                        elif result.count('🍒') == 2:
                            payout = payouts[('🍒', '🍒', None)]
                        elif result.count('🍒') == 1:
                            payout = payouts[('🍒', None, None)]
                        elif tuple(result) == ('💰', '💰', '💰'):  # Check for jackpot
                            payout = payouts[('💰', '💰', '💰')]


                        # Update the user's balance
                        user_data[str(user.id)]["balance"] += payout
                        await save_user_data(user_data)

                        # Create the updated slot machine embed message
                        updated_embed = discord.Embed(title="Slot Machine", color=discord.Color.blue())
                        updated_embed.add_field(name=result_string, value="\u200b", inline=False)
                        updated_embed.add_field(name="Balance", value=f"Your balance: {user_data[str(user.id)]['balance']:,d} credits", inline=False)

                        if payout > 0:
                            updated_embed.add_field(name="Congratulations!", value=f"You won {payout:,d} credits! 💰💰💰", inline=False)
                            if tuple(result) == ('💰', '💰', '💰'):  # Check for jackpot
                                updated_embed.add_field(name="JACKPOT!", value="You hit the jackpot! 🎉🎉🎉", inline=False)
                                print(f"!!! {ctx.author.name}({ctx.author.id}) WON THE JACKPOT!!!")
                        else:
                            updated_embed.add_field(name="Better Luck Next Time!", value=f"Sorry, no winning combination. 😢", inline=False)


                        # Update the message with the result and balance
                        await result_message.edit(embed=updated_embed)

                        # Remove the user's reaction
                        await result_message.remove_reaction(reaction.emoji, user)

                except asyncio.TimeoutError:
                    await result_message.edit(content="Slot machine session has timed out.")
                    user_data[str(user.id)]["in_game"] = False
                    await save_user_data(user_data)
                    break