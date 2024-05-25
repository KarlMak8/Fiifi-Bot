import discord
from discord.ext import commands
from discord.ui import Button, View

def create_lobby(ctx, num_players: int):
    lobby = Lobby()
    lobby.num_players = num_players
    player_names = lobby.collect_players(ctx)
    ctx.send("Lobby created with players: " + ", ".join(player_names))

class Lobby:
    def __init__(self):
        self.players = []
        self.num_players = 0

    async def collect_players(self, ctx):
        player_names = []
        for i in range(1, self.num_players + 1):
            await ctx.send(f"Click the button to join as player {i}")
            button_view = ButtonView(self, i)
            player_name = await button_view.send_initial_message(ctx)
            player_names.append(player_name)
        return player_names

class Player:
    def __init__(self, name):
        self.name = name

class ButtonView(View):
    def __init__(self, lobby, player_number):
        super().__init__(timeout=None)
        self.lobby = lobby
        self.player_number = player_number

    async def on_timeout(self):
        self.lobby.players = [player for player in self.lobby.players if player.name != self.author.display_name]
        await self.message.edit(content="Lobby creation timed out.", view=None)

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id and interaction.message.id == self.message.id

    @discord.ui.button(label="Join", style=discord.ButtonStyle.green)
    async def join_button(self, interaction: discord.Interaction, button: discord.Button,):
        player_name = interaction.user.display_name
        self.lobby.players.append(Player(player_name))
        await interaction.response.edit_message(content=f"{player_name} joined as player {self.player_number}.", view=None)
        return player_name
