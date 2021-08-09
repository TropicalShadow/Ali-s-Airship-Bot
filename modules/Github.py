from utils.decorators import decorators
from discord.ext.commands import Cog
from discord import Embed, Colour
from discord.ext import commands
from os import environ, system

class Github(Cog):
    def __init__(self,bot):
        self.bot = bot
        self.github_link = "https://github.com/TropicalShadow/Ali-s-Airship-Bot"
        self.pull_link = "git@github.com:TropicalShadow/Ali-s-Airship-Bot.git"

    @commands.command(name="github")
    async def github_command(self,ctx,*args,**kwargs):
        emb = Embed(title="Github",description=f"[here]({self.github_link}) is a link to my code",colour=Colour.blurple())
        await ctx.send(embed=emb)

    @decorators.isTrop()
    @commands.command(name="update_git")
    @decorators.typing
    async def update_git_command(self,ctx,*args,**kwargs):
        emb = Embed(description="Pull request sent....",colour=Colour.red())
        msg = await ctx.send(embed=emb)
        system(f"git pull {self.pull_link}")
        emb.description = "Pull request finished..."
        emb.colour = Colour.green()
        await msg.edit(embed=emb)
        if("--reload" in args):
            emb.description = "Restarting Bot now...."
            emb.colour = Colour.green()
            await msg.edit(emb, delete_after=5)
            quit()

       
       
    

def setup(bot):
    bot.add_cog(Github(bot))