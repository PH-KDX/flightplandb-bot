from env.token import DISCORD_TOKEN

import asyncio
import datetime
import logging
import discord
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=None, intents=intents)

log = logging.getLogger("discord")

TEST_GUILD = discord.Object(id=582974704864854016)
TEST_GUILD_TWO = discord.Object(id=1088169718038417501)

@bot.tree.command(name = "commandname", description = "My first application Command", guild=TEST_GUILD) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def first_command(interaction):
    await interaction.response.send_message("Hello!")

@bot.event
async def on_guild_available(ctx):
    # since on_ready can be called in a restart, the tree sync is run on the first guild join
    log.info(f"starting command tree sync for guild {ctx.id}")
    await bot.tree.sync(guild=ctx)
    log.info(f"command tree sync completed for guild {ctx.id}")


@bot.event
async def on_ready():
    log.info(f"Bot is logged in and ready as {bot.user.name}#{bot.user.discriminator}")

bot.run(token=DISCORD_TOKEN, log_level=logging.INFO)