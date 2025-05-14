import discord
from util import utils_math as uMath
from util import utils_json as jReader
from util import utils_time as uTime
import datetime
import re

CHANNELS = jReader.read("./data/channels.json")
RESPONSES = jReader.read("./data/responses.json")

def first_to_third_person(text, third_subject="they"):
    pronoun_map = {
        r"\bI\b": third_subject,
        r"\bme\b": "them",
        r"\bmy\b": "their",
        r"\bmine\b": "theirs",
        r"\bmyself\b": "themselves"
    }

    # Replace each first-person pronoun with third-person
    for pattern, replacement in pronoun_map.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text

async def reply_tf2(message):

    if message.channel.id in CHANNELS["silly"]:
        if uMath.roll(95, "Response"):
            RESPONSE = uMath.randElement(RESPONSES["hopOn"]["responses"])
            URL = uMath.randElement(RESPONSES["hopOn"]["urls"])

            await message.channel.send(RESPONSE)
            if(uMath.roll(50, "Send Gif")) : await message.channel.send(URL)

async def reply_gif(message):
    RESPONSE = uMath.randElement(RESPONSES["hopOn"]["responses"])
    URL = uMath.randElement(RESPONSES["hopOn"]["urls"])
    await message.channel.send(RESPONSE)
    await message.channel.send(URL)

async def sillyreplies(message: discord.Message):
    if message.channel.id in CHANNELS["silly"]:
        if(uMath.roll(60)) : return
        match message.content.lower():
            case "arasaka":
                await message.reply("Arasaka.....")
            case "ping":
                await message.channel.send("Pong!")
            case "elon":
                await message.reply("Demonic threat detected")
            
async def broWent(message: discord.Message, force=False):

    CHANCE = 70

    # Amayah
    if message.author.id == 1058073516186026095 : CHANCE = CHANCE - 30
    # June
    if message.author.id == 752989978535002134 : CHANCE = 10
    # If forced
    if force : CHANCE = 0

    if uMath.roll(CHANCE, "Bro Went") : return
    if not message.channel.id in CHANNELS["silly"]: 
        if force : await message.reply("I'm not meant to be silly here </3")
        return

    HASACTION = False
    ACTION = ""
    KEYWORDS = [
        "so i",
        "and i",
        "then i",
        "until i"
    ]

    PATH = "./data/assets/bro.jpg"
    with open(PATH, 'rb') as f:
        IMG = discord.File(f)

    for key in KEYWORDS:
        if key in message.content.lower():
            HASACTION = True
            PARTS = message.content.split(key, 1)
            ACTION = PARTS[1].strip()
    if HASACTION : 
        await message.channel.send(content=f"Bro {ACTION}", file=IMG)