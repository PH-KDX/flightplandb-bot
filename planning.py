import discord
from discord import app_commands
from discord.ext import commands
import flightplandb as fpdb
from pprint import pprint

async def find_plans(departure_icao: str, arrival_icao: str, token: str | None = None) -> list[fpdb.datatypes.Plan]:
    plans = fpdb.plan.search(
        plan_query=fpdb.datatypes.PlanQuery(
            fromICAO=departure_icao,
            toICAO=arrival_icao,
        ),
        include_route=True,
        limit=5,
        key=token
    )
    async for plan in plans:
        yield plan

class PlanningCog(commands.Cog, name="planning"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(name="plan")
    async def my_command(self, interaction: discord.Interaction) -> None:
        """ /command-1 """
        plans = [plan async for plan in find_plans("EHAM", "KJFK", token=self.bot.fpdb_token)]
        pprint(plans)
        await interaction.response.send_message(str([plan.id for plan in plans]))

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PlanningCog(bot))
