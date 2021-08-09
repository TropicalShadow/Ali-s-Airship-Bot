from discord.ext.commands import Cog
from discord.ext import commands
from discord import Embed, Colour, File, Invite, AuditLogAction, Member
from datetime import datetime
from typing import List

class JoinLeaveManager(Cog):
    def __init__(self,bot):
        self.bot = bot
        self.GuildInvites = []
        self.LastInvitesUpdate = datetime.now().timestamp()
        self.joinleave_channel_id = 874069123531931669


    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(self.bot.server)
        allInvites = await guild.invites()
        self.GuildInvites = allInvites
        self.LastInvitesUpdate = datetime.now().timestamp()

    def makeEmbed(self,author=None,title=None,description=None,Colour=None):
        emb = Embed(timestamp=datetime.now(),title=title,description=description,colour=Colour)
        emb.set_footer(icon_url=self.bot.user.avatar_url,text=f"{self.bot.user.id}")
        return emb

    @commands.Cog.listener(name="on_member_remove")
    async def WhenSomeoneLeaves(self,member):
        emb = Embed(
                description=f"{member.mention} `{str(member)}` left {member.guild}",
                colour=Colour.red(),
                timestamp=datetime.now(timezone.utc)
            )
        emb.set_author(name=f'{str(member)}',
                        icon_url=member.avatar_url)
        emb.set_footer(
            text=f"RealName_123#3570 | {self.bot.user.name} Bot", icon_url=self.bot.user.avatar_url)
        for i in self.joinLeaveStaffChannel:
            await self.bot.get_channel(i).send(embed=emb)

    async def bot_join(self, bot):
        embed = self.makeEmbed(title="Bot Joined",description=f"{bot} has joined the server.",Colour=Colour.blurple())

    @commands.Cog.listener(name="on_member_join")
    async def AightRegisterThisKid(self,member):
        err = []
        if(member.bot):
            await self.bot_join(member)
            return
        lastUpdate = self.LastInvitesUpdate
        invs: List[Invite] = await member.guild.invites()
        oldInvs: List[Invite] = self.GuildInvites

        self.GuildInvites = invs
        self.LastInvitesUpdate = datetime.now().timestamp()

        if(oldInvs is None):
            print("errr while Adding Member OldInvites invalid")
            return
        inviteCodeUsed = self.compareInvites(oldInvs,invs)
        if(len(inviteCodeUsed)==0):
            logs = await member.guild.audit_logs(action=AuditLogAction.invite_create,limit=50).flatten()
            if(not logs is None and len(logs)>=1):
                createdCodes = []
                for log in [i.target for i in logs if i.created_at.timestamp > lastUpdate and i.target.code not in [invite.code for invite in invs]]:
                    theInvite = await self.bot.fetch_invite(log.code)
                    if(theInvite):
                        createdCodes.append(theInvite)
                inviteCodeUsed.extend(createdCodes.code)
                invs.extend(createdCodes)

        #VANITY URL CHECK NOT NEEDED NOW.

        if(len(inviteCodeUsed)==0):
            channel = self.bot.get_channel(self.joinleave_channel_id)
            emb = self.makeEmbed(title=f"{member.display_name} Joined - unable to find who invited them",description=f"Member: {member.mention}\nMember_id: {member.id}\nJoinTime: {member.joined_at}",Colour=Colour.green())
            await channel.send(embed=emb)
        exactMatchCode = None
        if(len(inviteCodeUsed) == 1):
            exactMatchCode = inviteCodeUsed[0]
        
        updatedCode = []
        newAndUsedCode = []
        for usedInvite in inviteCodeUsed:
            invite = [i for i in invs if i.code == usedInvite]
            if(len(invite)>=1):
                newAndUsedCode.append(invite[0])
            else:
                updatedCode.append(usedInvite)
        tempInvs = invs
        for invite in invs:
            invitesFromOld = [i for i in oldInvs if i.code ==invite.code]
            tempInvs = [i for i in invs if i.code not in invitesFromOld]
        newAndUsedCode.extend(tempInvs)

        self.GuildInvites = newAndUsedCode
        
        AllInviteFromGuild =  await member.guild.invites()
        theInvite: Invite = await self.bot.fetch_invite(exactMatchCode)
        

        Joinchannel = self.bot.get_channel(self.joinleave_channel_id)
        if(theInvite is None):
            emb = self.makeEmbed(title=f"{member.display_name} Joined - unable to find who invited them",description=f"Member: {member.mention}\nMember_id: {member.id}\nJoinTime: {member.joined_at}",Colour=Colour.orange())
            await Joinchannel.send(embed=emb)
            return
        theInvite = list([invite for invite in AllInviteFromGuild if invite.code==theInvite.code])[0]
        if(theInvite.inviter is None):
            emb = self.makeEmbed(title=f"{member.display_name} Joined - Via Widget?",description=f"Member: {member.mention}\nMember_id: {member.id}\nJoinTime: {member.joined_at}",Colour=Colour.orange())
            await Joinchannel.send(embed=emb)
            return
        inviter = theInvite.inviter
        if(not inviter and theInvite.inviter):
            inviter = await member.guild.get_member(theInvite.inviter)
        
        emb =self.makeEmbed(title=f"{member.display_name} Joined from {inviter.display_name}",description=f"Member: {member.mention}\nMember_id: {member.id}\nJoinTime: {member.joined_at}\nCode: {theInvite.code}\nlink: [{theInvite.url}]({theInvite})\nuses: {theInvite.uses}/{theInvite.max_uses if theInvite.max_uses != 0 else 'inf' }\n{'|'.join(err)}",Colour=Colour.green())
        emb.set_thumbnail(url=member.avatar_url)

        await Joinchannel.send(embed=emb)

    @commands.Cog.listener(name="on_invite_create")
    async def sendInviteLinkDetails(self, invite):
        if(invite.inviter is None):
            return

        emb = Embed(
            description=f"{invite.inviter.mention} `{str(invite.inviter)}` has created {str(invite)}",
            colour=Colour.blue(),
            timestamp=datetime.now()
        )
        emb.set_author(name=f'{str(invite.inviter)}',
                       icon_url=invite.inviter.avatar_url)
        emb.set_footer(
            text=f"RealName_123#3570 | {self.bot.user.name} Bot", icon_url=self.bot.user.avatar_url)

        emb.add_field(name='Invite Link', value=f'{invite.url}')

        emb.add_field(name='Invite Infomation',
                      value=f'Expires in {"Never" if invite.max_age ==0 else invite.max_age}\
                                  \nUses | {invite.uses}/{invite.max_uses}\
                                  \nDate Created | {invite.created_at} \
                                  \nTemporary | {"Yes" if invite.temporary else "No"} \
                                  \nInviter | {str(invite.inviter)}',inline=False)
        channel = self.bot.get_channel(self.joinleave_channel_id)
        await channel.send(embed=emb)
    @commands.Cog.listener(name="on_invite_delete")
    async def deleteInviteLinkFromChannel(self, invite):
        for channel in [self.joinleave_channel_id]:
            channel = self.bot.get_channel(channel)
            messages = await channel.history(limit=123).flatten()
            for i in messages:
                if(len(i.embeds)):
                    if (str(invite) in i.embeds[0].description):
                        await i.delete()

    def compareInvites(self,OldCodes:List[Invite], NewCodes:List[Invite]) -> List[str]:
        CodesToReturn = []

        NewCodes = {i.code:i for i in NewCodes}
        OldCodes = {i.code:i for i in OldCodes}
        
        for key in NewCodes.keys():
            if(NewCodes[key].uses != 0 and (key not in list(OldCodes.keys()) or OldCodes[key].uses < NewCodes[key].uses)):
                CodesToReturn.append(key)
        if(len(CodesToReturn)==0):
            for key in OldCodes.keys():
                if(key not in list(NewCodes.keys()) and OldCodes[key].uses == OldCodes[key].max_uses-1):
                    CodesToReturn.append(key)
        return CodesToReturn
def setup(bot):
    bot.add_cog(JoinLeaveManager(bot))