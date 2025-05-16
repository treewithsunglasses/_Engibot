import os
import sys
import discord
from discord import utils as dUtils
from discord.ext import commands as dCommands
import util.utils_json as ujReader
import util.Response as uResponse

CONFIG = ujReader.read("./data/config.json")
# VARIABLES
STARBOARD_EMOJI = CONFIG["emojis"]["starboard"]
PREFIX = CONFIG["prefix"]
STAFF = CONFIG["roles"]["staff"]
STATUS = CONFIG["status"]

class hStaff(dCommands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @dCommands.hybrid_group(name="staff", with_app_command=True, invoke_without_command=True)
    async def staff(self, ctx):
        RESPONSE, URL = uResponse.getRandom("failedKill")
        await ctx.send(RESPONSE)
        await ctx.defer()

    @staff.command(name='kill', with_app_command=True)
    async def shutdown(self, ctx):
        RESPONSE, URL = uResponse.getRandom("failedKill")
        role = dUtils.get(ctx.guild.roles, id=STAFF)
        roles = ctx.author.roles
        if role in roles:
            await ctx.send("Shutting down...")
            await self.bot.close()
        else:
            await ctx.send(RESPONSE)
        await ctx.defer()

    @staff.command(name="restart", with_app_command=True)
    async def restart(self, ctx):
        RESPONSE, URL = uResponse.getRandom("failedKill")
        role = dUtils.get(ctx.guild.roles, id=STAFF)
        roles = ctx.author.roles
        if role in roles:
            await ctx.send("Restarting...")
            await self.bot.close()
            os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            await ctx.send(RESPONSE)
        await ctx.defer()

    @staff.command(name="check_role", with_app_command=True)
    async def check_role(self, ctx, member: discord.Member, role_id: float):
        role = dUtils.get(ctx.guild.roles, id=role_id)
        if role is None:
            await ctx.send(f"Role with ID {role_id} not found.")
            return
        if role in member.roles:
            await ctx.send(f"{member.display_name} has the role: {role.name}")
        else:
            await ctx.send(f"{member.display_name} does not have the role: {role.name}")
        await ctx.defer()

async def setup(bot):
    await bot.add_cog(hStaff(bot))
