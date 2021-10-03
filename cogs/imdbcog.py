import discord
from discord.ext import commands
import imdb

ia = imdb.IMDb()

class ImdbCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs extension \"IMDb\" ready.")

    #search movie/show

    @commands.command(aliases = ["searchimdb", "imdbsearch", "simdb"])
    async def imdb(self, ctx, *, name: str=None):
        if name == None:
            return await ctx.reply("**ERROR**: `MissingParameters` Please provide the name of the movie/show")
        else:
            # accesing imdb
            movie = ia.search_movie(name)
            movieID = movie[0].movieID
            search = ia.get_movie(movieID)
            plot = ia.get_movie(movieID, info=['plot'])

            # getting values
            movieName = movie[0] 
            rating = search.data['rating']
            plot.infoset2keys
            year = search['year']
            try:
                directors_obj = search['directors']
            except:
                directors_obj = None
            casting_obj = search['cast'][:8]
            plot = plot['plot'][0]
            genres = ', '.join(search['genres'])

            casting = []
            for actor in casting_obj:
                casting.append(actor["name"])
            
            directors = []
            if not directors_obj:
                directors = "Not Applicable"
            else:
                for director in directors_obj:
                    directors.append(director["name"])
            
                directors = ', '.join(directors)
            casting = ', '.join(casting)

            # embedding and printing
            imdb_emd = discord.Embed(title=movieName, description=f"IMDb results for search query **`{name}`**", color=discord.Color.random())
            imdb_emd.add_field(name="Rating", value=rating, inline=False)
            imdb_emd.add_field(name="Year", value=year, inline=False)
            imdb_emd.add_field(name="Director(s)", value=directors, inline=False)
            imdb_emd.add_field(name="Cast", value=casting, inline=False)
            imdb_emd.add_field(name="Genre", value=genres, inline=False)
            imdb_emd.add_field(name="Plot", value=plot, inline=False)
            imdb_emd.add_field(name="Credit", value= "All information is extracted from \"IMDbPY\". If you did not find the specific movie you searched for it is either not in imdb or does not exist.", inline=False)
            await ctx.reply(embed=imdb_emd)
    
    #handle errors in search movie command

    @imdb.error
    async def imdberror(self, ctx, error):
        if isinstance(error, IndexError):
            err_emd = discord.Embed(title="", color=discord.Color.red(), description="<:nex_cross:887950619950874634> Invalid name!")
            await ctx.reply(embed=err_emd)
        
        if isinstance(error, commands.CommandInvokeError):
            err_emd = discord.Embed(title="", color=discord.Color.red(), description="<:nex_cross:887950619950874634> Invalid name!")
            await ctx.reply(embed=err_emd)

    @commands.command(aliases = ['sactor', 'aimdb', 'actress'])
    async def actor(self, ctx, *, name=None):
        if name == None:
            return await ctx.reply("**ERROR**: `MissingParameters` Please provide the name of the actor/actress")
        else:
            person = ia.search_person(name)
            actorID = person[0].personID
            actor = ia.get_person(actorID)
            bio = ia.get_person_biography(actorID)
            name = actor['name']
            birthDate = actor['birth date']
            height = actor['height']
            trivia = actor['trivia'][:3]
            
            trivia = ', '.join(trivia)

            titles_refs = bio['titlesRefs']
            titles = []

            for title in titles_refs:
                titles.append(title)
            
            titles = titles[:5]
            titles = ', '.join(titles)

            actor_emd = discord.Embed(title=actor, description =f"IMDb results for search query **`{name}`**",
            color=discord.Color.random())
            actor_emd.add_field(name="DOB", value=birthDate, inline=False)
            actor_emd.add_field(name="Height", value=height, inline=False)
            actor_emd.add_field(name="Trivia", value=trivia, inline=False)
            actor_emd.add_field(name="Titles", value=titles, inline=False)
            actor_emd.add_field(name="Credit", value="All information is extracted from `IMDbPY`. If you did not find the specific actor/actress you searched for, he/she is either not in IMDb or does not exist.", inline=False)
            await ctx.reply(embed=actor_emd)
    
    @actor.error
    async def actorerror(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            ae_emd = discord.Embed(title="", color=discord.Color.red(), description="<:nex_cross:887950619950874634> Invalid name!")
            await ctx.reply(embed=ae_emd)
        
        if isinstance(error, KeyError):
            ae_emd = discord.Embed(title="", color=discord.Color.red(), description="<:nex_cross:887950619950874634> Invalid name!")
            await ctx.reply(embed=ae_emd)
    
def setup(bot):
    bot.add_cog(ImdbCog(bot))