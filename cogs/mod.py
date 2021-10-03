import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure

class ModCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.warnings = {}
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Cogs extension \'Mod\' loaded.')

    @commands.command(aliases=['clear'])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit=2):
        await ctx.channel.purge(limit=limit)
        
        purge_emd = discord.Embed(title="Messages Purged", color=discord.Color.orange())
        purge_emd.add_field(name="Amount", value=limit)
        purge_emd.add_field(name="Channel", value=ctx.channel.mention)
        purge_emd.add_field(name="Responsible Moderator", value=ctx.author.mention)

        await ctx.send(embed=purge_emd)
    
    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send(f'{ctx.author.mention} you gotta mention how many messages you wanna purge :/')
        elif isinstance(error, commands.BadArgument):
          await ctx.send(f'{ctx.author.mention} bruh it should be a number')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ctx.author.mention} oof sad you don't have the manage messages permission to use this command")
        else:
          raise error
    
    @commands.command(aliases=['yeet'])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        await member.kick(reason=reason)
        
        kick_emd = discord.Embed(title="Member Kicked", color=discord.Color.red())
        kick_emd.add_field(name="Reason", value=reason)
        kick_emd.add_field(name="Responsible Moderator", value=ctx.author.mention)
        kick_emd.add_field(name="Member", value=member.mention)

        await ctx.send(embed=kick_emd)
    
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send(f'{ctx.author.mention} you gotta mention whom you wanna kick lol')
        elif isinstance(error, commands.BadArgument):
          await ctx.send(f'{ctx.author.mention} bruh it should be an actual member')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ctx.author.mention} oof sad you don't have the kick members permission to use this command")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"{ctx.author.mention} I'm not high enough in the hierarchy to perform this action.")
        else:
          raise error
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        await member.ban(reason=reason)
        
        kick_emd = discord.Embed(title="Member Banned", color=discord.Color.red())
        kick_emd.add_field(name="Reason", value=reason)
        kick_emd.add_field(name="Responsible Moderator", value=ctx.author.mention)
        kick_emd.add_field(name="Member", value=member.mention)

        await ctx.send(embed=kick_emd)
    
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send(f'{ctx.author.mention} you gotta mention whom you wanna ban lol')
        elif isinstance(error, commands.BadArgument):
          await ctx.send(f'{ctx.author.mention} bruh it should be an actual member')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ctx.author.mention} oof sad you don't have the ban members permission to use this command")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"{ctx.author.mention} I'm not high enough in the hierarchy to perform this action.")
        else:
          raise error
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self,ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)

                unban_emd = discord.Embed(title="User Unbanned", color=discord.Color.green())
                unban_emd.add_field(name="User", value=user.mention)
                unban_emd.add_field(name="Responsible Moderator", value=ctx.author.mention)
                await ctx.reply(embed=unban_emd)
                return
            else:
                await ctx.reply("Welp that didn't work! Recheck your inputs and check whether I have permissions to ban and unban users!")
                return
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send(f'{ctx.author.mention} you gotta mention whom you wanna unban lol')
        elif isinstance(error, commands.BadArgument):
          await ctx.send(f'{ctx.author.mention} bruh it should be an actual user')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ctx.author.mention} oof sad you don't have the ban members permission to use this command")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"{ctx.author.mention} I'm not high enough in the hierarchy to perform this action.")
        else:
          raise error

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")
            await ctx.send("I couldn't find a muterole so I created one for the server.")

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, add_reactions=False, view_channel=True)
        else:
            await member.add_roles(mutedRole, reason=reason)

        mute_emd = discord.Embed(title="Member Muted", color=discord.Color.orange())
        mute_emd.add_field(name="Member", value=member.mention)
        mute_emd.add_field(name="Responsible Moderator", value=ctx.author.mention)
        mute_emd.add_field(name="Reason", value=reason)
        await ctx.send(embed=mute_emd)
        await member.send(f"You were muted in the server {guild.name} for reason: {reason}")

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send(f'{ctx.author.mention} you need to mention someone to mute lol')
        elif isinstance(error, commands.BadArgument):
          await ctx.send(f'{ctx.author.mention} there is no such member found :joy:')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ctx.author.mention} you don't have the permissions to use this command ooff")
        else:
          raise error
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")
        await member.remove_roles(mutedRole)

        unmute_emd = discord.Embed(title="Member Unmuted", color=discord.Color.green())
        unmute_emd.add_field(name="Member", value=member.mention)
        unmute_emd.add_field(name="Responsible Moderator", value=ctx.author.mention)
        await ctx.send(embed=unmute_emd)

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send(f'{ctx.author.mention} you need to mention someone to unmute lol')
        elif isinstance(error, commands.BadArgument):
          await ctx.send(f'{ctx.author.mention} there is no such member found :joy:')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ctx.author.mention} you don't have the permissions to use this command ooff")
        else:
          raise error
    
def setup(bot):
    bot.add_cog(ModCog(bot))