import discord.message
import random
from util import utils_math as uMath
from util import jsonreader as jReader

channels = jReader.read("./data/channels.json")

async def reply_tf2(message):
    if message.channel.id in channels["silly"]:
        if(uMath.roll(99)) : return
        if(uMath.roll(99)) : return
        await message.channel.send(f"please twin.... <@{message.author.id}>")
        if(uMath.roll(50)) :
            await message.channel.send("https://tenor.com/view/tf2-team-fortress-2-hop-gif-6374489811387781157")
            return
        else:
            await message.channel.send("https://tenor.com/view/team-fortress-2-tf2-medic-heavy-medic-tf2-gif-2069984277182190933")

async def sillyreplies(message):
    if message.channel.id in channels["silly"]:
        if(uMath.roll(80)) : return
        match message.content.lower():
            case "arasaka":
                await message.reply("Arasaka.....")
            case "ping":
                await message.channel.send("Pong!")
            case "elon":
                await message.reply("Demonic threat detected")