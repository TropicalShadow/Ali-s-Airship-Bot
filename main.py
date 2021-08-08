from discord import __version__, Intents
from utils.objects import AliBot
from os import listdir

with open("TOKEN.key","r") as fp:
    TOKEN = fp.readline()

description = """When you just wanna go bonk."""
command_prefix = ("-",)

intents = Intents.all()
bot = AliBot(command_prefix=command_prefix,description=description,intents=intents)

print ("Discord Version:",__version__)
print ("Loading Bot, Please Wait")

@bot.command(pass_context=True)
async def ping(ctx,*args,**kwargs):
    await ctx.message.delete()
    await ctx.send(content=f'Pong',delete_after=3)

cogs = sorted(listdir("./modules"))
for cog in cogs:
      if cog.endswith(".py"):
         try:
            cog = f"modules.{cog.replace('.py','')}"
            bot.load_extension(cog)
            print(f"loaded {cog}")
         except Exception as e:
            print(f"{cog} can not be loaded")
            print(e)

bot.run(TOKEN,bot=True,reconnect=True)