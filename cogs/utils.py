import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
import random

# python weather api wrapper
import python_weather

class UtilsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.sniped_msgs = {}
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs extension \"Utils\" ready.")
    
    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        self.bot.sniped_msgs[msg.guild.id] = (msg.content, msg.author, msg.channel.name, msg.created_at)

    @commands.command()
    async def diceroll(self, ctx):
        dice_val = random.randrange(1, 7)
        dice_emd = discord.Embed(title="Dice Roll!", description=f"Dice Value: **{dice_val}**", color=discord.Color.random())
        dice_emd.set_thumbnail(url="https://c.tenor.com/i_L5KauoCcoAAAAi/dice.gif")
        await ctx.reply(embed=dice_emd)
    
    @commands.command(aliases=['sn'])
    async def snipe(self, ctx):
        try:
            content, author, channel_name, time = self.bot.sniped_msgs[ctx.guild.id]
        except:
            return await ctx.reply("oof there's nothing to snipe")

        snipe_emd = discord.Embed(description=content, color=discord.Color.blurple(), timestamp=time)
        snipe_emd.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
        snipe_emd.set_footer(text=f"Deleted in: #{channel_name}")

        await ctx.reply(embed=snipe_emd)
    
    @commands.command(aliases=['pfp'])
    async def avatar(self, ctx, memb: discord.Member=None):
        if not memb:
            memb = ctx.author

        avatar_emb = discord.Embed(title=f"{memb.name}#{memb.discriminator}'s Avatar!", color=discord.Color.random())
        avatar_emb.set_image(url=memb.avatar_url)

        await ctx.reply(embed=avatar_emb)

     

def setup(bot):
    bot.add_cog(UtilsCog(bot))