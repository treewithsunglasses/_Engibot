import discord
from util import jsonreader as jReader

config = jReader.read("./data/config.json")

async def collect(ctx):
    person = ctx.message.mentions[0] if ctx.message.mentions else ctx.author
    
    embed = discord.Embed(
        title=f"{person.name}'s Avatar:",
        color=0xFF5733
    )
    embed.set_image(url=person.avatar.url)
    await ctx.send(embed=embed)