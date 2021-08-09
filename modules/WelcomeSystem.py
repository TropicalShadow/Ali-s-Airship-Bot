from datetime import datetime
from io import BytesIO

from discord import Colour, Embed, File, Guild, Object, Member
from discord.ext import commands
from discord.ext.commands import Cog
from discord_components import Button, ButtonStyle, Component
from discord_components.message import Message
from discord_components.component import ActionRow
from discord_components.interaction import Interaction, InteractionType
from discord_components import ComponentMessage
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from discord import TextChannel
from utils.decorators import decorators
from utils.objects import PermissionLevel


class WelcomeSystem(Cog):
    def __init__(self,bot):
        self.bot = bot
        self.Custom_id = "VerificationSystem"
        self.Verify_id = "Verify"
        self.rules_channel_id = 874030899803598909
        self.verify_channel_id = 874040139561717770
        self.lockdowns = {}

   

    @decorators.restrict(PermissionLevel.STAFF)
    @commands.command(name="lockdown",aliases=['raid'])
    async def lockdown_command(self,ctx,*args,**kwargs):
        guild = ctx.guild
        if(guild.id in self.lockdowns ):
            msg: Message = self.lockdowns[guild.id]
            if(not msg.author.bot or len(msg.embeds)<=0):return
            comps = msg.components
            for i,comp in enumerate(comps):
                component = comp
                for comp in component.components:
                    if(type(comp) is not Button): continue
                    comp: Button = comp
                    if(comp.custom_id != self.Verify_id and comp.custom_id != self.Custom_id): continue
                    comp.disabled = not comp.disabled
                    if(comp.disabled == True):
                        comp.label = "Lockdown"
                        comp.style = ButtonStyle.red
                    else:
                        if(guild.id in self.lockdowns):
                            del self.lockdowns[guild.id]
                        comp.label = "Verify"
                        comp.style = ButtonStyle.green
                    comps[i] = comp
                    await msg.edit(components = comps)
                    self.lockdowns[guild.id] = msg
        else:
            changed = False
            channel = self.bot.get_channel(self.verify_channel_id)
            async for msg in channel.history(limit=50):
                if(not msg.author.bot or len(msg.embeds)<=0):continue
                comps = msg.components
                for i,comp in enumerate(comps):
                    component = comp
                    for comp in component.components:
                        if(type(comp) is not Button): continue
                        comp: Button = comp
                        if(comp.custom_id != self.Verify_id and comp.custom_id != self.Custom_id): continue
                        comp.disabled = not comp.disabled
                        if(comp.disabled == True):
                            comp.label = "Lockdown"
                            comp.style = ButtonStyle.red
                        else:
                            if(guild.id in self.lockdowns):
                                del self.lockdowns[guild.id]
                            comp.label = "Verify"
                            comp.style = ButtonStyle.green
                        comps[i] = comp
                        await msg.edit(components = comps)
                        self.lockdowns[guild.id] = msg
                        changed = True
            if(not changed):
                await ctx.send("To init a lockdown run that command in the Verifiy channel with the bots message!!!")
        await ctx.message.delete()

    @decorators.restrict(PermissionLevel.ADMIN)
    @commands.command(name="sendVerify")
    async def sendVerify_command(self,ctx,*args,**kwargs):
        components = [
            Button(label="Verify",style=ButtonStyle.green, custom_id=self.Custom_id, id=self.Verify_id,emoji="\u2705"),
        ]
        Intro_or_Welcome_Channel = None
        Rules_Channel = None

        for channel in ctx.guild.channels:
            name = channel.name.lower() 
            if(name == "unverified-introduction" or name == "unverified-welcome"):
                Intro_or_Welcome_Channel = channel
            elif(name == "unverified-rules"):
                Rules_Channel = channel
            
        #"Make sure to check out "
        msg = f"Hey you, Welcome to {ctx.guild}.\n\n"
        if(Rules_Channel):
            msg += f"Make sure to read the rules in {Rules_Channel.mention}\n"
        if(Intro_or_Welcome_Channel):
            msg += f"If you want to know more check out {Intro_or_Welcome_Channel.mention}"
        emb = Embed(description=msg.strip(),colour=Colour.blurple())
        emb.set_footer(text=f"{self.bot.user.name} Bot | 0",icon_url=ctx.guild.icon_url)
        await ctx.send(embed=emb,components=components)
    
    @Cog.listener(name="on_button_click")
    async def verify_clicked(self, res: Interaction):
        if (res.custom_id != self.Custom_id and res.custom_id != self.Verify_id): return
        msg = res.message
        clicked = res.user
        embeds = msg.embeds
        if(len(embeds)>0):
            emb = embeds[0]
            url = emb.footer.icon_url
            emb.set_footer(text=f"{self.bot.user.name} Bot | {clicked.id}", icon_url=url)
            embeds[0] = emb
        member_role = None
        for role in res.guild.roles:
            name = role.name.lower()
            if(name == "member"):
                member_role = role
        if(member_role is None):
            emb = Embed(title="Error",description="Member role was not found.",colour=Colour.red(),delete_after=5)
            await res.channel.send(embed=emb)
        else:
            member = res.guild.get_member(clicked.id)
            await member.add_roles(member_role,reason="Verified")
        await res.respond(type=InteractionType.UpdateMessage,embeds=embeds)
   
    @decorators.isTrop()
    @commands.command("simjoin")
    async def Simulate_Join_command(self,ctx,member:Member=None):
        await self.sendWelcomeMessage(ctx.author if member is None else member)

    async def sendWelcomeCard(self,member, channel):
        img = Image.open("./assets/WelcomeCard.jpg").convert("RGBA")
        mainImageFile = BytesIO()
        titleFont = ImageFont.truetype("./assets/WelcomeCardFont.ttf", 65)
        nameFont = ImageFont.truetype("./assets/impact.ttf", 60)
        
        msg = f"Welcome to {str(member.guild)}."
        name = f"{member}"

        d = ImageDraw.Draw(img)
        w, h = d.textsize(msg, font=titleFont)
        d.text(((img.size[0]-w)/2, 0), msg, fill=(200, 200, 200, 240), font=titleFont)
        w, h = d.textsize( name, font=nameFont)
        d.text(((img.size[0]-w)/2, (img.size[1]-h)-15), name, fill=(200, 200, 200, 240), font=nameFont)

        avatar = BytesIO()
        asset = member.avatar_url_as( format="png", size=256)
        await asset.save(avatar, seek_begin=True)
        avatarImg = Image.open(avatar)
        avatarImg.resize((img.size[0],img.size[1]),Image.LANCZOS)
        #########################
        offset=0
        
        mask = Image.new("L", avatarImg.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((offset, offset, avatarImg.size[0] - offset, avatarImg.size[1] - offset), fill=255)
        #mask = mask.filter(ImageFilter.GaussianBlur(1))
        avatarImg = avatarImg.copy()
        avatarImg.putalpha(mask)

        #########################
        tempImage = Image.new("RGBA",img.size)

        Image.Image.paste(tempImage,avatarImg,(int(img.size[0]/2-avatarImg.size[0]/2),int(img.size[1]/2-avatarImg.size[1]/2)))
        img.paste(tempImage,None,tempImage)
        img.save(mainImageFile,'PNG')
        mainImageFile.seek(0)
        return File(mainImageFile,"Welcome.png")

    @commands.Cog.listener(name="on_member_update")
    async def sendWelcomeMessage(self,before, join):
        if((before.pending == after.pending) or after.pending == False)
        guild = member.guild
        WelcomeChannel = guild.system_channel
        emb = Embed(timestamp=datetime.utcnow(),description=f"Please read the {self.bot.get_channel(self.rules_channel_id).mention} to avoid getting banned.",color=Colour.green())
        try:
            file = await self.sendWelcomeCard(member,WelcomeChannel)
        except Exception as e:
            print(e)
        #emb.set_thumbnail(url=member.avatar_url)
        emb.set_footer(text=f"{member.id}",icon_url=guild.icon_url)
        emb.set_image(url="attachment://Welcome.png")
        await WelcomeChannel.send(embed=emb,file=file)
    
def setup(bot):
    bot.add_cog(WelcomeSystem(bot))
