import discord
from discord.ext import commands
import DiscordUtils
from DiscordUtils import *

# utils
from utils.truncate import truncate

class Music(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.music = DiscordUtils.Music()

  @commands.Cog.listener()
  async def on_ready(self):
    print('Cogs extension \'Music\' loaded.')

  @commands.command()
  async def join(self, ctx):
      voice_state = ctx.author.voice

      if voice_state is None:
          return await ctx.send('Please join a voice channel before using this command!')

      if ctx.voice_client is not None:
          await ctx.voice_client.disconnect()

      await ctx.author.voice.channel.connect()
      join_emd = discord.Embed(title="<a:nex_tick:887946161275666474> Successfully joined the voice channel!", description="Use `n!play` to play a song!", color=discord.Color.green())
      await ctx.reply(embed=join_emd)

  @commands.command()
  async def leave(self, ctx):
    voice_state = ctx.author.voice
    player = self.music.get_player(guild_id=ctx.guild.id)
    if ctx.voice_client == None:
        # await ctx.voice_client.disconnect()
        not_emd = discord.Embed(title="", color=discord.Color.red(), description="")
        not_emd.description += ("<:nex_cross:887950619950874634> I am not in a voice channel!")
        await ctx.reply(embed=not_emd)

    elif player == None:
        cya_emd = discord.Embed(title="", color=discord.Color.green(), description="<a:nex_tick:887946161275666474> Successfully left the voice channel. Cya later!")
        await ctx.reply(embed=cya_emd)
        return await ctx.voice_client.disconnect()

    else:
        await player.stop()
        if voice_state is None:
            vc_emd = discord.Embed(title="", color=discord.Color.red(), description="<:nex_cross:887950619950874634> You need to be in a voice channel to use this command")
        
            return await ctx.reply(embed=vc_emd)
        if ctx.voice_client is not None:
            await ctx.reply("Cya later!")
            return await ctx.voice_client.disconnect()

  @commands.command()
  async def play(self, ctx, *, inp=None):
    try:
        voice_state = ctx.author.voice
        if voice_state is None:
            vc_none_emd = discord.Embed(title="", color=discord.Color.red(), description="<:nex_cross:887950619950874634> You need to be in a voice channel to use this command")
            return await ctx.send(embed=vc_none_emd)

        if inp == None:
            return await ctx.reply("Provide the name of the track which you want to play.")
        player = self.music.get_player(guild_id=ctx.guild.id)
        if not player:
            player = self.music.create_player(ctx, ffmpeg_error_betterfix=True)
        if not ctx.voice_client.is_playing():
            await player.queue(inp, search=True)
            song = await player.play()
            play_emd = discord.Embed(title="Hello!", color=discord.Color.green(), description=f"Playing song **{song.name}**")
            play_emd.add_field(name="Requested By", value=ctx.author.mention)
            await ctx.send(embed=play_emd)
        else:
            song = await player.queue(inp, search=True)
            queued_emd = discord.Embed(title="Song Queued", color=discord.Color.random(), description=f"Queued song **{song.name}**")
            queued_emd.add_field(name="Requested By", value=ctx.author.mention)
            await ctx.send(embed=queued_emd)
    except NotConnectedToVoice:
        nctv_emd = discord.Embed(title="", color=discord.Color.red(), description="<:nex_cross:887950619950874634> Use `n!join` to add me to the voice channel!")
        await ctx.reply(embed=nctv_emd)

  @commands.command()
  async def pause(self, ctx):
    voice_state = ctx.author.voice
    if voice_state is None:
        vcin_emd = discord.Embed(title="", color=discord.Color.red(), description="<:nex_cross:887950619950874634> You need to be in a voice channel to use this command")
        return await ctx.reply(embed=vcin_emd)
    else:
      player = self.music.get_player(guild_id=ctx.guild.id)
      song = await player.pause()
      
      pause_emd = discord.Embed(title="", description=f"<a:nex_tick:887946161275666474> Paused playback for **[{song.name}]({song.url})**", color=discord.Color.green())

      await ctx.reply(embed=pause_emd)

  @commands.command()
  async def resume(self, ctx):
    voice_state = ctx.author.voice
    if voice_state is None:
        vcin_emd = discord.Embed(title="", color=discord.Color.red(), description="<:nex_cross:887950619950874634> You need to be in a voice channel to use this command")
        return await ctx.reply(embed=vcin_emd)

    else:
        player = self.music.get_player(guild_id=ctx.guild.id)
        song = await player.resume()
        res_emd = discord.Embed(title="", color=discord.Color.green(), description=f"<a:nex_tick:887946161275666474> Resumed playback for **[{song.name}]({song.url})**")
        await ctx.reply(embed=res_emd)

  @commands.command()
  async def stop(self, ctx):
    voice_state = ctx.author.voice
    if voice_state is None:
        return await ctx.send('You need to be in a voice channel to use this command')
    else:
      player = self.music.get_player(guild_id=ctx.guild.id)
      await player.stop()
      await ctx.send("Stopped playback.")

  @commands.command()
  async def loop(self, ctx):
    voice_state = ctx.author.voice
    player = self.music.get_player(guild_id=ctx.guild.id)
    if voice_state is None:
        return await ctx.send('You need to be in a voice channel to use this command')
    elif player == None:
        return await ctx.send('I am not in a voice channel! Use `n!join` to add me in one!')
    else:
        song = await player.toggle_song_loop()
        if song.is_looping:
            await ctx.send(f"Enabled playback loop for **{song.name}**")
        else:
            await ctx.send(f"Disabled platback loop for **{song.name}**")

  @commands.command(aliases=['q'])
  async def queue(self, ctx):
    player = self.music.get_player(guild_id=ctx.guild.id)
    if ctx.voice_client is None:
        await ctx.reply("I am not in a voice channel!")
    else:
        queue_emd = discord.Embed(title=f"Song Queue for {ctx.guild.name}", color=discord.Color.random())
        if player == None:
            return await ctx.reply("No songs in the queue! Use `n!play` to add one!")
        else:
            tot_dur = 0
            index = 0
            for song in player.current_queue():
                index += 1
                queue_emd.add_field(name=f"`{index}`. {song.name}", value=f"{truncate((song.duration/60), 2)} mins", inline=False)
                tot_dur = tot_dur + truncate((song.duration/60), 2)
            queue_emd.set_footer(text=f"Total Duration: {tot_dur} mins")
            await ctx.send(embed=queue_emd)

  @commands.command(aliases=['song', 'np', 'nowplaying'])
  async def now_playing(self, ctx):
    voice_state = ctx.author.voice
    player = self.music.get_player(guild_id=ctx.guild.id)

    if voice_state is None:
        return await ctx.send('You need to be in a voice channel to use this command')
    elif player == None:
        return await ctx.send('Nothing is being played currently!')
    else:
        song = player.now_playing()
        np_emd = discord.Embed(title="Now playing", color=discord.Color.dark_gold())
        np_emd.add_field(name="Song", value=song.name)
        np_emd.add_field(name="Duration", value=f"{truncate((song.duration/60), 2)} mins")
        await ctx.send(embed=np_emd)

  @commands.command(aliases=['force_skip', 'fs'])
  async def forceskip(self, ctx):
    voice_state = ctx.author.voice
    player = self.music.get_player(guild_id =ctx.guild.id)
    if voice_state is None:
        return await ctx.send('You need to be in a voice channel to use this command')
    elif player == None:
        return await ctx.send('Either nothing is currently being played or I am not in a voice channel!')
    else:
        await player.skip(force=True)
        await ctx.send("Force skipped current track!")

  @commands.command()
  async def skip(self, ctx):
    voice_state = ctx.author.voice
    player = self.music.get_player(guild_id=ctx.guild.id)
    if voice_state is None:
        return await ctx.send('You need to be in a voice channel to use this command')
    
    elif player == None:
        return await ctx.send('Either nothing is currently being played or I am not in a voice channel!')

    else:
        await player.skip(force=False)
        await ctx.send("Skipped current track!")

  @commands.command()
  async def volume(self, ctx, vol):
    voice_state = ctx.author.voice
    player = self.music.get_player(guild_id=ctx.guild.id)

    if voice_state is None:
        return await ctx.send('You need to be in a voice channel to use this command')

    elif player == None:
        return await ctx.send('Either nothing is currently being player or I am not in a voice channel!')

    else:
        song, volume = await player.change_volume(float(vol) / 100)
        await ctx.send(f"Changed volume for **{song.name}** to **{volume*100}**%")

  @commands.command(aliases=['r'])
  async def remove(self, ctx, index):
    voice_state = ctx.author.voice
    if voice_state is None:
        return await ctx.send('You need to be in a voice channel to use this command')
    else:
        player = self.music.get_player(guild_id=ctx.guild.id)
        song = await player.remove_from_queue(int(index))
        await ctx.send(f"Removed **{song.name}** from the playback queue")
  
  #Trying to create a program which savs a playlist in a database and plays that database when function "playlist" is called.

  # @commands.command()
  # async def playlist(self, ctx):
  #   userID = ctx.message.author.id
  #   voice_state = ctx.author.voice
  #   player = self.music.create_player(ctx, ffmpeg_error_betterfix=True)
  #   a = 1
  #   if voice_state is None:
  #         return await ctx.send('Please join a voice channel before using this command!')
  #   elif not player:
  #       player = self.music.create_player(ctx, ffmpeg_error_betterfix=True)
  #   if not ctx.voice_client.is_playing():
  #     await player.queue(inp, search=True)
  #     song = await player.play()
  #     play_emd = discord.Embed(title="Hello!", color=discord.Color.green(), description=f"Playing song **{song.name}**")
  #     play_emd.add_field(name="Requested By", value=ctx.author.mention)
  #     await ctx.send(embed=play_emd)
  #   elif:
  #     song = await player.queue(inp, search=True)
  #     queued_emd = discord.Embed(title="Song Queued", color=discord.Color.random(), description=f"Queued song **{song.name}**")
  #     queued_emd.add_field(name="Requested By", value=ctx.author.mention)
  #     await ctx.send(embed=queued_emd)
  #   elif userID in db:
  #     result = db[userID]
  #     result = ', '.join(result)
  #     await ctx.reply(f"Your playlist: \n {result}")
  #   else:
  #     await ctx.reply(f"<:nex_cross:887950619950874634> Playlist not found!")

def setup(bot):
    bot.add_cog(Music(bot))