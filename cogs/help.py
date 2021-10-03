from discord.ext import commands
import discord
from discord_components import Select, SelectOption

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs extension \"Help\" ready.")

    @commands.command()
    async def help(self, ctx: commands.Context):
        page1 = discord.Embed(title='Fun Commands!', description='Jokes, memes & all the other fun stuff\n[] = Not Required <> = Required', color=discord.Color.blue())
        page1.add_field(name='`meme`', value='Displays a meme fetched from Reddit. \n**Default subreddit** = `r/CleanMemes`\n**Params**=`[subreddit_name]`,\n **Aliases**=`none`')
        page1.add_field(name='`devjoke`', value='Jokes for developers/programmers :sunglasses:\n**Params**=`none`\n**Aliases**=`projoke`, `programmerjoke`')
        page1.add_field(name='`joke`', value='COOL JOKES YEAAHH\n**Params**=`none`\n**Aliases**=`none`')
        page1.add_field(name='`pokesearch`', value='Search for all yo fav pokemon\n**Params**=`pokesearch <pokemon_name>`\n**Aliases**=`pokemon`, `pokemonsearch`')
        page1.add_field(name='`8ball`', value='scuffed answers for your questions :]\n**Params**=`none`\n**Aliases**=`eightball`, `eight_ball`')
        page1.add_field(name="`iq`", value="**totally not rigged** like **totally** ;)\n**Params**=`iq [@member]`\n**Aliases**=`howiq`, `bigbrain`, `iqcheck`")
        page1.add_field(name="`youtube`", value="Watch YouTube with friends!\n**Params**=`none`\n**Aliases**=`yt`")
        page1.add_field(name="`chess`", value="OMG CHESS POG\n**Params**=`none`\n**Aliases**=`none`") 
        page1.add_field(name="`fishing`", value="~~phishing~~ fishing.io in discord!\n**Params**=`none`\n**Aliases**=`fishingtonio`") 
        page1.add_field(name="`betrayal`", value="betrayal.io in discord!\n**Params**=`none`\n**Aliases**=`betrayalio`")
        page1.add_field(name='`yomama`', value='Displays a yomama joke\n**Params**=`None`\n **Aliases**=`yomom`') 
        page1.set_footer(text="Page 2 of 9")

        page2 = discord.Embed(title='General Commands', description='some.. *general* stuff?\n[] = Not Required <> = Required', color=discord.Color.blue())
        page2.add_field(name='`help`', value='Shows this help embed\n**Aliases**=`none`\n**Params**=`none`', inline=False)
        page2.add_field(name='`invite`', value='Invite me to your servers!\n**Aliases**=`none`\n**Params**=`none`', inline=False)
        page2.add_field(name='`stats`', value='Some nerdy stats i guess\n**Aliases**=`statistics`\n**Params**=`none`', inline=False)
        page2.set_footer(text="Page 1 of 9")

        page3 = discord.Embed(title='GitHub Commands', description='Commands to fetch some GitHub stuff!\n[] = Not Required <> = Required', color=discord.Color.random())
        page3.add_field(name='`ghuser`', value='Search for github users\n**Params**=`ghuser <github_username>`\n**Aliases**=`none`', inline=False)
        page3.add_field(name='`ghrepo`', value='Search for github repositories\n**Params**=`ghrepo <gh_reponame>`\n**Aliases**=`none`', inline=False)
        page3.set_footer(text="Page 3 of 9")

        page4 = discord.Embed(title='Anime Commands', description='Some weeby commands lol!\n[] = Not Required <> = Required', color=discord.Color.random())
        page4.add_field(name='`animechar`', value='Search for an anime character\n**Params**=`animechar <character_name>`\n**Aliases**=`none`', inline=False)
        page4.add_field(name='`animesearch`', value='Search for Anime shows!\n**Params**=`animesearch <anime_name>`\n**Aliases**=`asearch`', inline=False)
        page4.set_footer(text="Page 4 of 9")

        page5 = discord.Embed(title='Mod Commands', description='All of these commands require permissions to run.\n[] = Not Required <> = Required', color=discord.Color.random())
        page5.add_field(name='`purge`', value='Delete a set of messages\n**Params**=`purge <amount>`\n**Aliases**=`clear`')
        page5.add_field(name='`kick`', value='Kick a member from the guild\n**Params**=`kick <@name> [reason]`\n**Aliases**=`yeet`')
        page5.add_field(name='`ban`', value='Ban a member from the guild\n**Params**=`ban <@name> [reason]`\n**Aliases**=`none`')
        page5.add_field(name='`unban`', value='Unban a member from the guild\n**Params**=`unban <name#discriminator>`\n**Aliases**=`none`')
        page5.add_field(name='`mute`', value='Mute a member\n**Params**=`mute <@member> [reason]`\n**Aliases**=`none`')
        page5.add_field(name='`unmute`', value='Unmute a member\n**Params**=`unmute <@member>`\n**Aliases**=`none`')
        page5.set_footer(text="Page 5 of 9")

        page6 = discord.Embed(title='Music Commands', description='Some of these commands are still in development and might contain some bugs!\n[] = Not Required <> = Required', color=discord.Color.random())
        page6.add_field(name='`join`', value='Add Nex to the voice channel you\'re currently in\n**Params**=`none`\n**Aliases**=`none`')
        page6.add_field(name='`play`', value='Search and play a track\n**Params**=`play <track_name>`\n**Aliases**=`none`')
        page6.add_field(name='`queue`', value='Shows the queued tracks\n**Params**=`none`\n**Aliases**=`q`')
        page6.add_field(name='`now_playing`', value='Shows the track being played\n**Params**=`none`\n**Aliases**=`np`, `nowplaying`')
        page6.add_field(name='`remove`', value='Removes a song from the queue\n**Params**=`remove <track_index>`\n**Aliases**=`r`')
        page6.add_field(name='`leave`', value='Remove Nex from the voice channel\n**Params**=`none`\n**Aliases**=`disconnect`')
        page6.add_field(name='`loop`', value='Toggle loop for the current track\n**Params**=`none`\n**Aliases**=`disconnect`')
        page6.add_field(name='`skip`', value='Skip the current track\n**Params**=`none`\n**Aliases**=`none`')
        page6.add_field(name='`forceskip`', value='Force skip the current track\n**Params**=`none`\n**Aliases**=`fs`, `force_skip`')
        page6.add_field(name='`volume`', value='Set the volume for the current track\n**Params**=`volume <volume_percentage>`\n**Aliases**=`none`')
        page6.set_footer(text="Page 6 of 9")

        page7 = discord.Embed(title="Utility Commands", description="Some of these commands are still in development and might contain some bugs!\n[] = Not Required <> = Required", color=discord.Color.random())
        page7.add_field(name="`avatar`", value='View someone\'s avatar\n**Params**=`avatar [@user]`\n**Aliases**=`pfp`', inline=False)
        page7.add_field(name="`snipe`", value='View the latest deleted message in a channel\n**Params**=`none`\n**Aliases**=`sn`', inline=False)
        page7.add_field(name="`diceroll`", value='Well- rOlL a DiCe\n**Params**=`none`\n**Aliases**=`none`', inline=False)
        page7.set_footer(text="Page 7 of 9")

        page8 = discord.Embed(title="Economy Commands", description="The Nex economy system! (More commands are added daily!)\n[] = Not Required <> = Required", color=discord.Color.random())
        page8.add_field(name="`balance`", value='Check someone\'s wallet and bank balance\n**Params**=`balance [@user]`\n**Aliases**=`bal`')
        page8.add_field(name="`beg`", value='beg people for some money lol\n**Params**=`none`\n**Aliases**=`none`')
        page8.add_field(name="`share`", value='share coins with someone else!\n**Params**=`share <@user> <amount>`\n**Aliases**=`send`')
        page8.add_field(name="`deposit`", value='Deposit coins from your wallet to your bank\n**Params**=`deposit <amount>`\n**Aliases**=`dep`')
        page8.add_field(name="`withdraw`", value='Withdraw coins from your bank to your wallet\n**Params**=`withdraw <amount>`\n**Aliases**=`with`')
        page8.add_field(name="`rob`", value='steal coins from someone else\'s wallet!\n**Params**=`rob <@user>`\n**Aliases**=`steal`')
        page8.add_field(name="`leaderboard`", value='View the top richest people!\n**Params**=`leaderboard [number]`\n**Aliases**=`lb`')
        page8.add_field(name="`sell`", value='Sell an item!\n**Params**=`sell <item> [amount]`\n**Aliases**=`none`')
        page8.add_field(name="`shop`", value='A list of all the items you can get!\n**Params**=`none`\n**Aliases**=`none`')
        page8.add_field(name="`postmemes`", value='Post a meme with a laptop to the Internet and hopefully earn some coins!\n**Params**=`none`\n**Aliases**=`pm`')
        page8.add_field(name="`dig`", value='Dig around with a shovel to get coins or items!\n**Params**=`none`\n**Aliases**=`none`')
        page8.add_field(name="`mine`", value='Mine with a drill **or** a pickaxe to get some minerals!\n**Params**=`none`\n**Aliases**=`none`')
        page8.add_field(name="`cut`", value='Cut trees to get sticks or coins!\n**Params**=`none`\n**Aliases**=`none`')
        page8.add_field(name="`craft` (In Development)", value='Craft special items to get better luck in some commands!\n**Params**=`craft <category> <item>`\n**Aliases**=`none`')
        page8.set_footer(text="Page 8 of 9")

        page9 = discord.Embed(title="IMDb Commands", description="Get information about movies, shows and actors/actresses!\n[] = Not Required <> = Required", color=discord.Color.random())
        page9.add_field(name="`imdb`", value='Get info on a movie or a show!\n**Params**=`imdb <movie/show>`\n**Aliases**=`searchimdb`, `imdbsearch`, `simdb`')
        page9.add_field(name="`actor`", value='Get info on an actor or an actress!\n**Params**=`actor <actor/actress>`\n**Aliases**=`sactor`, `aimdb`, `actress`')
        page9.set_footer(text="Page 9 of 9")

        def_emd = discord.Embed(title="Nex Commands List", description="A list of all of Nex's commands! Choose a category to view it's respective commands!", color=discord.Color.blue())

        await ctx.send(
            embed=def_emd,
            components = [
                Select(
                    placeholder = "Choose a category",
                    options = [
                        SelectOption(label = "General Commands", value = "A", description="Some general commands"),
                        SelectOption(label = "Fun Commands", value = "B", description="Random fun stuff!"),
                        SelectOption(label = "GitHub Commands", value = "C", description="Github search commands"),
                        SelectOption(label = "Anime Commands", value = "D", description="Only for weebs i guess"),
                        SelectOption(label = "Moderation Commands", value = "E", description="Mod commands (you need permissions to run these)"),
                        SelectOption(label = "Music Commands", value = "F", description="listen to music with Nex!"),
                        SelectOption(label = "Utility Commands", value = "G", description="Helpful utility commands"),
                        SelectOption(label = "Economy Commands", value = "H", description="Virtual currency system in Nex!"),
                        SelectOption(label = "IMDb Commands", value = "I", description="Get information about movies, shows, actors and actresses using my IMDb commands!"),
                    ]
                )
            ]
        )

        while True:
            interaction = await self.bot.wait_for("select_option")
            if interaction.values[0] == "A":
                await interaction.send(embed=page2)
            if interaction.values[0] == "B":
                await interaction.send(embed=page1)
            if interaction.values[0] == "C":
                await interaction.send(embed=page3)

            if interaction.values[0] == "D":
                await interaction.send(embed=page4)

            if interaction.values[0] == "E":
                await interaction.send(embed=page5)
            if interaction.values[0] == "F":
                await interaction.send(embed=page6)
            if interaction.values[0] == "G":
                await interaction.send(embed=page7)
            if interaction.values[0] == "H":
                await interaction.send(embed=page8)
            if interaction.values[0] == "I":
                await interaction.send(embed=page9)

def setup(bot):
    bot.add_cog(HelpCog(bot))