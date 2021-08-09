from utils.decorators import decorators
from discord.ext.commands import Cog
from discord.ext import commands
from random import choice


class Developer(Cog):
    def __init__(self,bot):
        self.bot = bot

    @decorators.isTrop()
    @commands.command(name='die')
    async def death(self, ctx, *args):
        await ctx.send(content=choice(["Till death do us part","i went bonk",f"{self.bot.user.name} left the chat"]))
        quit()

    @decorators.isTrop()
    @commands.command(name='reload')
    async def mod_reload(self, ctx, module: str):
        extensions = self.bot.extensions
        if module == 'all':
            for extension in extensions:
                self.bot.unload_extension(module)
                self.bot.load_extension(module)
            await ctx.send('Done')
        if module in extensions:
            module = "modules."+module
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
            await ctx.send('Done')
        else:
            await ctx.send('Unknown Module')
    @decorators.isTrop()
    @commands.command(name='load')
    async def mod_load(self, ctx, module: str):
        try:
            module = "modules."+module
            self.bot.load_extension(module)
            await ctx.send('Done')
        except commands.errors.ExtensionNotFound:
            await ctx.send(f'Could not load module: `{module}`')
        except commands.errors.NoEntryPointError:
            await ctx.send('No setup command in `{module}.py` stupid!')
    @decorators.isTrop()
    @commands.command(name='unload')
    async def mod_unfload(self, ctx, module: str):
        try:
            module = "modules."+module
            self.bot.unload_extension(module)
            await ctx.send('Done')
        except commands.errors.ExtensionNotLoaded:
            await ctx.send(
                f'Could not unload module: `{module}` because'
                ' it was not loaded'
            )
    @decorators.isTrop()
    @commands.command(name='listextensions', aliases=['cogs'])
    async def list_extensions(self, ctx):
        extensions_dict = self.bot.extensions
        msg = '```css\n'

        extensions = []

        for b in extensions_dict:
            # print(b)
            extensions.append(b)

        for a in range(len(extensions)):
            msg += f'{a}: {extensions[a]}\n'

        msg += '```'
        await ctx.send(msg)

def setup(bot):
    bot.add_cog(Developer(bot))