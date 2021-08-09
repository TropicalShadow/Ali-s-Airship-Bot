from discord_components import DiscordComponents
from discord.ext.commands import Cog
from discord import Game, DMChannel
from discord.ext import commands
from re import match

class Events(Cog):
    def __init__(self,bot):
        self.bot = bot
        self.Eyes = "\U0001F440"
        self.ready = False

    @Cog.listener(name="on_message")
    async def eyes(self,message):
        if(self.Eyes in message.content):
            await message.add_reaction(self.Eyes) # Signature reaction
        if (isinstance(message.channel, DMChannel)):
             # Get forwarded dms, both to see when Bot'ed dm advertisers dm the bot
             # And to check if anyone is asking the bot for help doing things.
            if(message.author != self.bot.user):
                await self.bot.get_user(380068718379663360).send(f'{str(message.author)} - {message.content}')

    async def status_task(self):
        await self.bot.wait_until_ready()
        await self.bot.change_presence(activity=Game(name="songs in my head"))


    @Cog.listener(name="on_ready")
    async def whenBotBeReady(self):
        if(self.ready):return
        DiscordComponents(self.bot)
        print("-----------------------")
        print("Bot is ready.")
        print(f"Name: {self.bot.user}")
        print(f"ID: {self.bot.user.id}")
        print("-----------------------")
        self.bot.loop.create_task(self.status_task())
        self.ready = True


    @commands.Cog.listener(name="on_command_error")
    async def onGlobalError(self,ctx,exception):
        if hasattr(ctx.command,"on_error"):
            return
        #Check if cog overrides on error.
        if(ctx.cog):
            if(ctx.cog._get_overridden_method(ctx.cog.cog_command_error) is not None):
                return 
        if(isinstance(exception,commands.errors.CommandNotFound)):# A simple command not found error.
            await ctx.send("That Command was not found!")
            return
        if isinstance(exception, str):
            exception = exception.encode('string-escape')
        if match(r'^The check functions for command.*', str(exception)) is None:
            # Just throw an error out to the user, probs not the nicest of looking, but
            # you shouldn't have code that causes this to happen anyways. Hmm
            # but its a nice thing to see for a developer when they cba looking into console
            await ctx.send(embed=Embed(title="Error",description=f"{exception}",colour=Colour.red()))   

def setup(bot):
    bot.add_cog(Events(bot))