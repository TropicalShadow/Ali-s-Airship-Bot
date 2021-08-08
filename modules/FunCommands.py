from discord.ext.commands import Cog
from discord.ext import commands
from random import choice
from discord import User

class FunCommands(Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="bonk")
    async def bonk_command(self,ctx, member: User, *args):
        bonks = [
            "{0} bonked {1}",
            "{1} was bonked by {0}",
            "{0} omega bonked {1}",
            "{1} got bink bank bonked by {0}"
        ]
        await ctx.message.delete()
        await ctx.send(choice(bonks).format(ctx.author.mention,member.mention))
    

def setup(bot):
    bot.add_cog(FunCommands(bot))