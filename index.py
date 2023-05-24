# This example requires the 'message_content' intent.

import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import yt_dlp

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print('Bot is ready')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)


@bot.tree.command(name='hello', description='Says hello to you')
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hello {interaction.user.mention}!')


@bot.tree.command(name='play', description='play a song')
@app_commands.describe(song_url='The song to play')
async def say(interaction: discord.Interaction, song_url: str):
    yt_dl_opts = {'format': 'bestaudio/best'}
    ytdl = yt_dlp.YoutubeDL(yt_dl_opts)

    ffmpeg_opts = {'options': "-vn"}

    voice_channel = interaction.user.voice.channel
    if voice_channel != None:
        vc = await voice_channel.connect()

        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(song_url, download=False))

        # insall ffmpeg to use this
        song = data['url']
        player = discord.FFmpegPCMAudio(
            song, **ffmpeg_opts, executable='C:/FFMPEG/ffmpeg.exe')

        vc.play(player)
        await interaction.response.send_message(f'Playing {data["title"]}')
    else:
        await interaction.response.send_message('User is not in a channel.')

bot.run("TOKEN")
