from discord.ext.commands import check, CheckFailure, Context
import functools
from .objects import PermissionLevel

def get_role(guild, level: PermissionLevel):
        if(level == PermissionLevel.MEMBER):
            return guild.member_role_id
        elif(level == PermissionLevel.STAFF):
            return guild.staff_role_id
        elif(level == PermissionLevel.ADMIN):
            return guild.admin_role_id
        else:
            return None

class Decorators:

    def isTrop(self,*args,**kwargs):
        def predicate(ctx):
            if (ctx.author.id in [380068718379663360,615731606677880842]):
                return True
            else:
                raise CheckFailure("is not trop")
                
        return check(predicate)

    def typing(self,func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            context = args[0] if isinstance(args[0], Context) else args[1]
            async with context.typing():
                await func(*args, **kwargs)
        return wrapped

    def restrict(self, level: PermissionLevel): 
        async def predicate(ctx):
            self = ctx.command.cog
            guild = self.bot.guild
            if(guild is None):
                raise CheckFailure("This guild isn't registered with this bot. if you suspect otherwise report to TropicalShadow `RealName_123#2570`")
            else:
                member = ctx.author
                role_id = get_role(guild,level)
                if(role_id == 0):
                    raise CheckFailure("Guild has not been setup correctly in the config,report to TropicalShadow `RealName_123#2570`")
                elif(role_id == None):
                    return True
                role = ctx.guild.get_role(int(role_id))
                if(role is None):
                    raise CheckFailure("This guild isn't fully configured yet, report to TropicalShadow")
                if(member.top_role >= role):
                    return True
                else:
                    raise CheckFailure("You don't have permission to run this command!")
        return check(predicate)

decorators = Decorators()