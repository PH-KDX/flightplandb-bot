import discord
from discord import app_commands, ui, Embed
from discord.ext import commands
import flightplandb as fpdb

async def find_plans(departure_icao: str, arrival_icao: str, token: str | None = None, real_only: bool = True) -> list[fpdb.datatypes.Plan]:
    plans = fpdb.plan.search(
        plan_query=fpdb.datatypes.PlanQuery(
            fromICAO=departure_icao,
            toICAO=arrival_icao,
            tags=("real" if real_only else None),
        ),
        include_route=True,
        limit=5,
        key=token
    )
    async for plan in plans:
        yield plan

class PlanSearchView(discord.ui.View):
    def __init__(self, *args, fpdb_token=None, dep_icao=None, arr_icao=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fpdb_token = fpdb_token
        self.dep_icao = dep_icao
        self.arr_icao = arr_icao

    async def disable_components(self) -> None:
        # disable any buttons and menus
        for item in self.children:
            item.disabled = True

        # then apply the view with the disabled components
        await self.message.edit(view=self)

    async def on_timeout(self) -> None:
        await self.disable_components()

    async def format_results_embed(self, plan_search_results: list[fpdb.datatypes.Plan]) -> Embed:
        message_embed = Embed(title="Plan search results", description="The top 5 results are shown in the format 'ID: route'")
        for result in plan_search_results:
            message_embed.add_field(
                name=result.id,
                value=" ".join([wpt.ident for wpt in result.route.nodes]),
                inline=False,
            )
        return message_embed

    @discord.ui.button(label="Search for real plans with these parameters")
    async def real_plans_search(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.disable_components()
        plan_search_results = [plan async for plan in find_plans(departure_icao=self.dep_icao, arrival_icao=self.arr_icao, token=self.fpdb_token, real_only=True)]
        if not plan_search_results:
            await interaction.response.send_message(
                "Unfortunately, no real-world plans were found for this route. Would you like to generate a plan instead?.",
                ephemeral=True,
            )
        else:
            message_embed = await self.format_results_embed(plan_search_results)
            await interaction.response.send_message(embed=message_embed, ephemeral=True)

    @discord.ui.button(label="Search for generated plans with these parameters")
    async def generated_plans_search(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.disable_components()
        plan_search_results = [plan async for plan in find_plans(departure_icao=self.dep_icao, arrival_icao=self.arr_icao, token=self.fpdb_token, real_only=False)]
        if not plan_search_results:
            await interaction.response.send_message(
                "Unfortunately, no generated plans were found for this route.",
                ephemeral=True,
            )
        else:
            message_embed = await self.format_results_embed(plan_search_results)
            await interaction.response.send_message(embed=message_embed, ephemeral=True)

class PlanSearchModal(ui.Modal):
    def __init__(self, fpdb_token=None) -> None:
        super().__init__(title='Plan search')
        self.fpdb_token = fpdb_token

    dep_icao = ui.TextInput(label='Departure ICAO', required=True)
    arr_icao = ui.TextInput(label='Arrival ICAO', required=True)
    async def on_submit(self,interaction: discord.Interaction):
        view = PlanSearchView(fpdb_token=self.fpdb_token, dep_icao=self.dep_icao.value, arr_icao=self.arr_icao.value, timeout=30)
        inputted_data_embed = Embed(title="Plan search")
        inputted_data_embed.add_field(name="Departure ICAO", value=self.dep_icao)
        inputted_data_embed.add_field(name="Arrival ICAO", value=self.arr_icao)
        await interaction.response.send_message(
            embed=inputted_data_embed,
            view=view,
            ephemeral=True,
        )
        view.message = await interaction.original_response()

class PlanningCog(commands.Cog, name="planning"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(name="plan")
    async def my_command(self, interaction: discord.Interaction) -> None:
        """ Search for plans """
        await interaction.response.send_modal(PlanSearchModal(fpdb_token=self.bot.fpdb_token))

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PlanningCog(bot))
