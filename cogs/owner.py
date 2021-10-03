from discord.ext import commands

class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs extention \"Owner\" ready.")

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.send("Loaded the extension")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')
        await ctx.send("Unloaded the extension")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')
        await ctx.send("Unloaded the extension")
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.send("Loaded the extension")

def setup(bot):
    bot.add_cog(OwnerCog(bot))