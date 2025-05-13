import discord
from discord.ext import commands
import util.jsonreader as jReader
import util.cache as cache
import util.utils_math as uMath
import actions.silly as silly
import data.tf2class as tf2class

# VARIABLES
STARBOARD_EMOJI = "⭐"

# Setup Intents
MYINTENTS = discord.Intents.all()
MYINTENTS.reactions = True
bot = commands.Bot(command_prefix=':3 ', intents=MYINTENTS)

# Data
cache.starboard_load()
CHANNELS = jReader.read("./data/channels.json")

# BOOL CONDITIONALS
def isValidChannel(id):
    WHITELIST = CHANNELS["whitelist"]
    BLACKLIST = CHANNELS["blacklist"]

    if(WHITELIST) : return checkWhitelist(id)
    if(BLACKLIST) : return checkBlacklist(id)
    return False
 
def checkWhitelist(id):
    channels = CHANNELS["allowed"]
    for c in channels:
        if id == c: return True
    return False

def checkBlacklist(id):
    channels = CHANNELS["disallowed"]
    for c in channels:
        if id == c: return False
    return True  

# EVENTS
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_typing(channel, user, when):
    print(f"{user.name} is speaking")
    if(user.bot) : return
    roll = uMath.roll(5)
    if(roll) : return
    await channel.send("Oh look, the nerd is speaking")

@bot.event
async def on_message_delete(message):
    if(uMath.roll(40)) : return
    await message.channel.send("https://tenor.com/view/i-saw-w-gus-fring-gus-gustavo-deleted-gif-25440636")

# COMMANDS
@bot.command("hello")
async def hello(ctx):
    print(ctx)
    await ctx.reply("i know what kind of man you are")

@bot.command("tf2")
async def tf2(ctx, arg1):
    if(arg1 == "") : 
        await ctx.reply("Please provide a class!")
        return
    try:
        CHARACTER = tf2class.TF2Character(arg1)
        EMBED = discord.Embed(
            title=CHARACTER.name,
            description=CHARACTER.description,
            color=0xFF5733
        )
        EMBED.set_thumbnail(url=CHARACTER.thumbnail)
        await ctx.reply(embed=EMBED)
    except ValueError as e:
        print(e)
        await ctx.reply("You did not provide a valid class!")

# LISTENERS
@bot.listen()
async def on_message(message):
    # Ignore bot and channels im not asked to speak in
    if message.author.bot : return
    #if isValidChannel(message.channel.id) == False : return

    if message.attachments:
        if message.channel.id in CHANNELS["art"]:
            #await message.add_reaction("<:happi:1355706814083371199>")
            await message.add_reaction(STARBOARD_EMOJI)
            return

    await silly.reply_tf2(message)
    await silly.sillyreplies(message)

@bot.listen()
async def on_reaction_add(reaction, user):
    # Return if the user is a bot or if there is no image or the image is not in our art channel
    if(user.bot) : return
    if not reaction.message.attachments : return
    if not reaction.message.channel.id in CHANNELS["art"] : return

    # Variables
    MESSAGE = reaction.message
    MESSAGE_ID = MESSAGE.id
    MESSAGE_CONTENT = MESSAGE.content
    CHANNEL = MESSAGE.channel
    CHANNEL_ID = CHANNEL.id
    COUNT = reaction.count
    MILESTONES = {3, 5, 10, 25, 50, 100}
    PREV_MILESTONE = cache.starred_messages.get(str(MESSAGE_ID), 0)

    # Is this new reaction a star?
    for milestone in sorted(MILESTONES):
        if COUNT >= milestone > PREV_MILESTONE:
            cache.starred_messages[MESSAGE_ID] = milestone
            cache.starboard_save()
    
            # Build the embed to send
            AUTHOR = MESSAGE.author.name
            TITLE= f"Art by {AUTHOR}"
            if MESSAGE.content : TITLE = MESSAGE_CONTENT
            embed = discord.Embed(
                title= TITLE,
                url= MESSAGE.jump_url,
                color= 0x4CE4B1,
                timestamp= MESSAGE.created_at
            )
            embed.set_author(name= AUTHOR, icon_url= MESSAGE.author.avatar.url)
            embed.set_image(url= MESSAGE.attachments[0].url)

            # Send the art in every starboard channel
            for cID in CHANNELS["starboard"]:
                c = bot.get_channel(cID)
                if c.guild != CHANNEL.guild : continue
                await c.send(embed=embed, content=f"{STARBOARD_EMOJI} {COUNT} | <#{CHANNEL_ID}>")

            # Reply in the art channel
            await MESSAGE.reply(f"Wow! This message hit {COUNT} stars!")
            break

# RUN
tok = jReader.read("./data/tokens.json")
bot.run(tok["botToken"])