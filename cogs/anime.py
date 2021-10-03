import discord
from discord.ext import commands

# myanimelist api wrapper
import animec

class AnimeCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs extension \"Anime\" ready.")

    @commands.command()
    async def animechar(self, ctx, *, name=None):
        try:
            if name == None:
                await ctx.reply("**ERROR**: `MissingParameters` Please provide a name input")
            else:
                result = animec.Charsearch(name)
        except:
            await ctx.reply("**ERROR**: `CommandInvokeError` Invalid name!")

        animec_emd = discord.Embed(title=result.title, description=f"Search results for anime character `{name}`", color=discord.Color.random())
        animec_emd.set_thumbnail(url=result.image_url)
        animec_emd.add_field(name="References", value=result.references, inline=False)
        animec_emd.add_field(name="More", value=f"[MyAnimeList.net]({result.url})")

        await ctx.reply(embed=animec_emd)
    
    @commands.command(aliases=['asearch'])
    async def animesearch(self, ctx, *, name=None):
        try:
            if name == None:
                await ctx.reply("**ERROR**: `MissingParameters` Please provide a name input.")
            else:
                result = animec.anicore.Anime(name)
        except:
            await ctx.reply("**ERROR**: `CommandInvokeError` Invalid anime name!")

        genres = ', '.join(result.genres)
        anime_emd = discord.Embed(title=result.title_english, description=f"Search results for anime `{name}`", color=discord.Color.random())
        anime_emd.set_thumbnail(url=result.poster)
        anime_emd.add_field(name="Description", value=f"{result.description[:997]}...", inline=False)
        anime_emd.add_field(name="Genres", value=genres, inline=False)
        anime_emd.add_field(name="Type", value=result.type, inline=False)
        anime_emd.add_field(name="Aired", value=result.aired, inline=False)
        anime_emd.add_field(name="Episodes", value=result.episodes, inline=False)
        anime_emd.add_field(name="Rating", value=result.rating, inline=False)
        anime_emd.add_field(name="Popularity", value=result.popularity, inline=False)
        anime_emd.add_field(name="Status", value=result.status, inline=False)
        anime_emd.add_field(name="Broadcast", value=result.broadcast, inline=False)

        await ctx.reply(embed=anime_emd)

def setup(client):
    client.add_cog(AnimeCog(client))