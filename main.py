import os
from keep_alive import keep_alive
from discord.ext import commands, tasks
import discord
import psutil
from discord_components import DiscordComponents, Button, ButtonStyle
import asyncio
import discordSuperUtils

bot = commands.Bot(
    command_prefix=["n!", "N!"],
    case_insensitive=True,
    intents = discord.Intents.all()
)

bot.remove_command('help')


@tasks.loop(seconds=60)
async def ch_pr():
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name=f"@Nex"))
    await asyncio.sleep(15)
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name="n!help"))
    await asyncio.sleep(15)


@bot.event
async def on_message(message):
    mention = f'<@!{bot.user.id}>'
    if message.content == mention:
        yo_emd = discord.Embed(
            title="Yo! :wave:",
            color=discord.Color.blurple(),
            description=
            "My prefix is `n!`\nUse `n!help` for a list of all my commands!")
        await message.channel.send(embed=yo_emd)

    await bot.process_commands(message)


@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name="n!help"))
    ch_pr.start()
    DiscordComponents(bot)


@bot.command()
async def ping(ctx):
    await ctx.reply("Pong!")


@bot.command()
async def invite(ctx):
    inv_emd = discord.Embed(
        title="Invite me to your servers!",
        description="Click the button below to invite me to your server!")
    inv_emd.set_footer(text="Thanks! :D")

    await ctx.reply(
        embed=inv_emd,
        components=[
            Button(
                label="Invite Me!",
                url=
                "https://discord.com/api/oauth2/authorize?client_id=884342046956072960&permissions=8&scope=bot",
                style=ButtonStyle.URL)
        ])

# @bot.command()
# async def guilds(ctx):
#     g_emd = discord.Embed(title="Guilds", description="")
#     for guild in bot.guilds:
#         g_emd.description += f"\n{guild}"
#     await ctx.reply(embed=g_emd)

@bot.command(aliases=["statistics"])
async def stats(ctx):
    stats_emd = discord.Embed(title="Nex Stats", color=discord.Color.blue())
    stats_emd.add_field(name="CPU Usage",
                        value=f"{psutil.cpu_percent()}%",
                        inline=False)
    stats_emd.add_field(name="Virtual RAM Usage",
                        value=f"{psutil.virtual_memory().percent}%",
                        inline=False)
    stats_emd.add_field(name="Server Count",
                        value=len(bot.guilds),
                        inline=False)
    stats_emd.add_field(name="User Count",
                        value=sum(g.member_count for g in bot.guilds),
                        inline=False)
    stats_emd.add_field(name="Library", value="`py-cord`", inline=False)

    await ctx.reply(embed=stats_emd)

@bot.command()
async def paginator(ctx):
    messages = [
        discord.Embed(title="Data (1/2)", description="Hello world"),
        discord.Embed(title="Data (2/2)", description="Hello world"),
    ]

    await discordSuperUtils.ButtonsPageManager(ctx, messages, button_color=2).run()

extensions = [
    'cogs.fun', 'cogs.help', 'cogs.github', 'cogs.anime', 'cogs.mod', 'cogs.econ_db', 'cogs.utils', 'cogs.imdbcog', 'cogs.crafts', 'cogs.music', 'cogs.owner'
]

if __name__ == '__main__':  # Ensures this is the file being ran
    for extension in extensions:
        bot.load_extension(extension)  # Loades every extension.

keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET")
bot.run(token)  # Starts the bot
