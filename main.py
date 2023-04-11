from env.token import DISCORD_TOKEN, API_TOKEN

import asyncio
import datetime
import logging
import discord
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=None, intents=intents)
bot.fpdb_token = API_TOKEN

log = logging.getLogger("discord")

TEST_GUILD = discord.Object(id=582974704864854016)
TEST_GUILD_TWO = discord.Object(id=1088169718038417501)

extensions = ["utils", "planning"]

@bot.event
async def setup_hook():
    for extension in extensions:
        log.info(f"loading bot extension {extension}")
        await bot.load_extension(extension)

@bot.event
async def on_guild_available(ctx):
    bot.tree.copy_global_to(guild=ctx)
    # for every guild, as it comes ready, the tree is synced for that guild
    log.info(f"starting command tree sync for guild {ctx.id}")
    await bot.tree.sync(guild=ctx)
    log.info(f"command tree sync completed for guild {ctx.id}")

@bot.event
async def on_ready():
    log.info(f"Bot is logged in and ready as {bot.user.name}#{bot.user.discriminator}")

bot.run(token=DISCORD_TOKEN, log_level=logging.INFO)
