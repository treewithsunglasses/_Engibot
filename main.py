import os
import sys
import discord
from discord import utils as dUtils
from discord.ext import commands as dCommands
import util.utils_json as ujReader
import util.utils_cache as uCache
import util.utils_math as uMath
import util.utils_discord as uDiscord
import util.utils_string as uString
import util.Response as uResponse
import data.tf2class as dTF2
import actions.Silly as aSilly
import actions.Flag as aFlag
import actions.Avatar as aAvatar
import actions.Starboard as uStarboard

# Data
uCache.starboard_load()
CONFIG = ujReader.read("./data/config.json")
# SETUP

# VARIABLES
STARBOARD_EMOJI = CONFIG["emojis"]["starboard"]
PREFIX = CONFIG["prefix"]
STAFF = CONFIG["roles"]["staff"]
STATUS = CONFIG["status"]

# Setup Bot
MYINTENTS = discord.Intents.all()
MYINTENTS.reactions = True
bot = dCommands.Bot(command_prefix=PREFIX, intents=MYINTENTS)


# Private Methods
async def _load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

# EVENTS
@bot.event
async def on_ready():
    await _load_extensions()

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} application commands.")
    except Exception as e:
        print(f"Sync failed: {e}")

    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.Activity(type=discord.ActivityType.listening, name=STATUS)
    )
    await uStarboard._starboard_cache(bot)
    aFlag.flagCache()

# RUN
tok = ujReader.read("./data/tokens.json")
bot.run(tok["botToken"])