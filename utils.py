import discord
from discord import app_commands
from discord.ext import commands

class MyCog(commands.Cog, name="utils"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(name="ping")
    async def my_command(self, interaction: discord.Interaction) -> None:
        """ /command-1 """
        await interaction.response.send_message(f"**{round(self.bot.latency * 1000)}** ms", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MyCog(bot))
