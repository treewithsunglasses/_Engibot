import discord
from discord.ext import commands
from discord import utils as dUtils
import actions.Avatar as Avatar
import util.utils_json as jReader
import util.utils_cache as utils_cache
import util.utils_math as uMath
import util.utils_discord as uDiscord
import data.tf2class as tf2class
import actions.Silly as Silly
import actions.Flag as Flag

# VARIABLES
STARBOARD_EMOJI = "⭐"
PREFIX = '-'
STAFFID = 1372047838770626640

# Setup Intents
MYINTENTS = discord.Intents.all()
MYINTENTS.reactions = True
bot = commands.Bot(command_prefix=PREFIX, intents=MYINTENTS)

# Data
utils_cache.starboard_load()
CHANNELS = jReader.read("./data/channels.json")
# SETUP

async def starboard_cache():
    for channel_id in CHANNELS["art"]:
        channel = bot.get_channel(channel_id)
        if channel is None:
            print(f"[LOG] Channel ID {channel_id} not found or not cached")
            continue
        print(f"[LOG] Scanning channel: {channel.name}")

        try:
            async for message in channel.history(limit=None, oldest_first=True):
                MESSAGE_ID = str(message.id)
                if MESSAGE_ID in utils_cache.starred_messages:
                    continue

                if message.attachments:
                    has_image = any(
                        att.content_type and att.content_type.startswith("image/")
                        for att in message.attachments
                    )
                    if has_image:
                        message_id_str = str(message.id)

                        # Check if already reacted with the star emoji by anyone
                        star_reaction = next((r for r in message.reactions if r.emoji == STARBOARD_EMOJI), None)

                        if star_reaction:
                            # Add to cache if not already cached
                            if message_id_str not in utils_cache.starred_messages:
                                print(f"Message {message.id} already has {star_reaction.count} stars; caching it.")
                                utils_cache.starred_messages[message_id_str] = star_reaction.count
                                utils_cache.starboard_save()
                        else:
                            try:
                                await message.add_reaction(STARBOARD_EMOJI)
                                print(f"Starred message {message.id} in #{channel.name}")
                                utils_cache.starred_messages[message_id_str] = 1
                                utils_cache.starboard_save()
                            except Exception as e:
                                print(f"Failed to react to message {message.id}: {e}")

        except Exception as e:
            print(f"Failed to read history in {channel.name}: {e}")

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
    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.Activity(type=discord.ActivityType.listening, name="to Croods while ovulating")
    )
    await starboard_cache()
    Flag.flagCache()

@bot.event
async def on_typing(channel, user: discord.Member, when):
    print(f"{user.name} is speaking")
    if(user.bot) : return
    roll = uMath.roll(95, "Nerd is speaking")
    if not roll : return
    await channel.send(f"Oh look, the nerd {user.name} is speaking...")

@bot.event
async def on_message_delete(message):
    if(uMath.roll(40)) : return
    await message.channel.send("https://tenor.com/view/i-saw-w-gus-fring-gus-gustavo-deleted-gif-25440636")

# COMMANDS
@bot.command()
async def check_role(ctx, member: discord.Member, role_id: int):
    role = dUtils.get(ctx.guild.roles, id=role_id)
    if role is None:
        await ctx.send(f"Role with ID {role_id} not found.")
        return
    if role in member.roles:
        await ctx.send(f"{member.display_name} has the role: {role.name}")
    else:
        await ctx.send(f"{member.display_name} does not have the role: {role.name}")

@bot.command(name='kill')
async def shutdown(ctx):
    role = dUtils.get(ctx.guild.roles, id=STAFFID)
    roles = ctx.author.roles
    if role in roles:
        await ctx.send("Shutting down...")
        await bot.close()
    else:
        await ctx.send('I AM IMMORTAL')

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
        EMBED.set_image(url=CHARACTER.thumbnail)
        await ctx.reply(embed=EMBED)
    except ValueError as e:
        print(e)
        await ctx.reply("You did not provide a valid class!")

@bot.command("avatar")
async def avatar(ctx, args):
    await Avatar.collect(ctx)

@bot.command("flag")
async def flag (ctx, arg1, arg2):
    await Flag.pride(ctx, arg1, arg2)

@bot.command("gif")
async def gif (ctx):
    await Silly.reply_gif(ctx.message)

@bot.command("add")
async def add (ctx, arg1, arg2=""):
    print("Called add")
    match arg1:
        case "gif":
            if not arg2 :
                await ctx.reply("Please provide a gif to add") 
                return
            try: 
                jReader.addList(
                    file_path="./data/responses.json",
                    key_path=["hopOn", "urls"],
                    item=arg2
                    )
                await ctx.reply("Done!")
            except Exception as e:
                await ctx.reply(e)
        case "response":
            if not arg2 :
                await ctx.reply("Please provide a response to add")
                return
            try:
                jReader.addList(
                    file_path="./data/responses.json",
                    key_path=["hopOn", "responses"],
                    item=arg2
                )
                await ctx.reply("Done!")
            except Exception as e:
                await ctx.reply(e)


@bot.command("explode")
async def explode (ctx):
    await ctx.reply("Explodes you")

@bot.command("commands")
async def commands (ctx):
    EMBED : discord.Embed = uDiscord.help()
    await ctx.channel.send(embed=EMBED)

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

    await Silly.reply_tf2(message)
    await Silly.sillyreplies(message)
    await Silly.broWent(message)

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
    PREV_MILESTONE = utils_cache.starred_messages.get(str(MESSAGE_ID), 0)

    # Is this new reaction a star?
    for milestone in sorted(MILESTONES):
        if COUNT >= milestone > PREV_MILESTONE:
            utils_cache.starred_messages[MESSAGE_ID] = milestone
            utils_cache.starboard_save()
    
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