import discord
from discord.ext import commands
from discordTogether import DiscordTogether
import os
import random
import requests
import json

# reddit api wrapper
import asyncpraw

# jokes api
import joke_generator
import pyjokes

# pokemon api
import pypokedex as p

# data
from data.joke_titles import joke_titles, devjoke_titles

os.environ.get("DISCORD_BOT_SECRET")

reddit = asyncpraw.Reddit(client_id="3WCeNBgy8RSogyEmGpzLnw",
                          client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
                          username="staticvoid176",
                          password=os.environ.get("REDDIT_SECRET"),
                          user_agent="nexpraw")

reddit.read_only = True

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs extension \"Fun\" ready.")

    @commands.command()
    async def meme(self, ctx, subreddit="cleanmemes"):
        subreddit = await reddit.subreddit(subreddit)
        top = subreddit.hot(limit=100)
        memes = []

        async for sub in top:
            memes.append(sub)

        random_meme = random.choice(memes)

        name = random_meme.title
        url = random_meme.url

        meme_emd = discord.Embed(title=name)
        meme_emd.set_image(url=url)

        await ctx.reply(embed=meme_emd)

    @commands.command()
    async def joke(self, ctx):
        joke_emd = discord.Embed(title=random.choice(joke_titles),
                                 description=joke_generator.generate(),
                                 color=discord.Color.random())
        await ctx.reply(embed=joke_emd)

    @commands.command(aliases=["projoke", "programmerjoke"])
    async def devjoke(self, ctx):
        devjoke_emd = discord.Embed(title=random.choice(devjoke_titles),
                                    description=pyjokes.get_joke(
                                        language='en', category='neutral'),
                                    color=discord.Color.random())

        await ctx.reply(embed=devjoke_emd)
    
    @commands.command(aliases=["pokemonsearch", "pokemon"])
    async def pokesearch(self, ctx, *, name=None):
        try:
            if name == None:
                await ctx.reply("**ERROR**: `MissingParameters` Please provide the name of the pokemon")
            else:
                pok = p.get(name=name)
        except:
            await ctx.reply("**ERROR**: `CommandInvokeError` Invalid pokemon name!")

        poke_imgurl = pok.sprites.front['default']
        # print(pok.sprites)
        poke_embed = discord.Embed(title=pok.name.capitalize(), color=discord.Color.random())
        poke_embed.set_thumbnail(url=poke_imgurl)
        poke_embed.add_field(name="Weight", value=f'{pok.weight/10} kg', inline=False)
        poke_embed.add_field(name="Type", value=pok.types[0].capitalize(), inline=False)
        poke_embed.add_field(name="Height", value=f'{pok.height/10} m', inline=False)
        poke_embed.add_field(name="Pokedex Number", value=pok.dex, inline=False)
        poke_embed.add_field(name="Base Exp", value=pok.base_experience, inline=False)
        poke_embed.add_field(name="Attack", value=pok.base_stats.attack, inline=False)
        poke_embed.add_field(name="Defense", value=pok.base_stats.defense, inline=False)
        poke_embed.add_field(name="HP", value=pok.base_stats.hp, inline=False)
        poke_embed.add_field(name="Speed", value=pok.base_stats.speed, inline=False)

        await ctx.send(embed=poke_embed)
    
    @commands.command(aliases=['8ball', 'eight_ball'])
    async def eightball(self, ctx, *, q: str=None):
        if q == None:
            await ctx.reply("bruh don't waste my time and give a proper question smh")
        else:
            eightball_resp = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes – definitely', 'You may rely on it', 'As I see it, yes', 'Most likely', 'Outlook good', 'Yes Signs point to yes', 'Reply hazy', 'try again', 'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again', 'Dont count on it', 'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful']

        eightball_f_resp = random.choice(eightball_resp)

        eight_emd = discord.Embed(title="The 8Ball says...", description=eightball_f_resp, color=discord.Color.blue())
        eight_emd.set_thumbnail(url="https://c.tenor.com/r0t5TfKKvJ0AAAAC/magic-eight.gif")
        eight_emd.set_footer(text=f"Your question: {q}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=eight_emd)

    @commands.command(aliases=['howiq', 'bigbrain', 'iqcheck'])
    async def iq(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        
        iq = random.randrange(1, 201)
        iq_txt = ""
        
        if iq <= 70:
            if member == ctx.author:
                iq_txt = "you are dum-dum lol"
            else:
                iq_txt = f"{member.name} is a dum-dum lol"
        else:
            if member == ctx.author:
                iq_txt = "you are bigbrain pog"
            else:
                iq_txt = f"{member.name} is a bigbrain pog"

        iq_emd = discord.Embed(title=f"{member.name}#{member.discriminator}'s IQ", description=iq_txt, color=discord.Color.random())
        iq_emd.add_field(name="IQ", value=f"**`{iq}`**")
        iq_emd.set_thumbnail(url="https://c.tenor.com/QaGZ50VlEPEAAAAC/think-about-it-use-your-brain.gif")
        iq_emd.set_footer(text="Tip: Invite me to your servers using n!invite", icon_url=ctx.author.avatar_url)

        await ctx.reply(embed=iq_emd)

    @commands.command(aliases=['yt'])
    async def youtube(self, ctx):
        togetherControl = DiscordTogether(self.bot)
        if not ctx.author.voice:
            await ctx.reply("You have to be in a voice channel to use this command!")
        else:
            link = await togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
            yt_emd = discord.Embed(title="Watch YouTube with your friends!", description=f"[**Click this link to start watching YouTube!**]({link})", color=discord.Color.dark_magenta())
            await ctx.send(embed=yt_emd)
    
    @commands.command()
    async def chess(self, ctx):
        togetherControl = DiscordTogether(self.bot)
        if not ctx.author.voice:
            await ctx.reply("You have to be in a voice channel to use this command!")
        else:
            link = await togetherControl.create_link(ctx.author.voice.channel.id, 'chess')
            chess_emd = discord.Embed(title="Play chess with your friends!", description=f"[**Click this link to start playing Chess!**]({link})", color=discord.Color.light_gray())
            await ctx.send(embed=chess_emd)

    @commands.command(aliases=['fishingtonio'])
    async def fishing(self, ctx):
        togetherControl = DiscordTogether(self.bot)
        if not ctx.author.voice:
            await ctx.reply("You have to be in a voice channel to use this command!")
        else:
            link = await togetherControl.create_link(ctx.author.voice.channel.id, 'fishing')
            fish_emd = discord.Embed(title="Play `Fishington.io` with your friends!", description=f"[**Click this link to start playing `Fishington.io`!**]({link})", color=discord.Color.blue())
            await ctx.send(embed=fish_emd)
    
    @commands.command(aliases=['betrayalio'])
    async def betrayal(self, ctx):
        togetherControl = DiscordTogether(self.bot)
        if not ctx.author.voice:
            await ctx.reply("You have to be in a voice channel to use this command!")
        else:
            link = await togetherControl.create_link(ctx.author.voice.channel.id, 'betrayal')
            bet_emd = discord.Embed(title="Play `Betrayal.io` with your friends!", description=f"[**Click this link to start playing `Betrayal.io`!**]({link})", color=discord.Color.dark_gold())
            await ctx.send(embed=bet_emd)
    
    @commands.command(aliases=['yomom'])
    async def yomama(self, ctx):
        res = requests.get("https://api.yomomma.info/")
        res_json = res.json()
        yomom_emd = discord.Embed(title="Yo Mama Joke", description=res_json["joke"], color=discord.Color.random())
        yomom_emd.set_footer(text="sheesh", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=yomom_emd)

def setup(bot):
    bot.add_cog(FunCog(bot))