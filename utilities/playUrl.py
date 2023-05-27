import asyncio;
import discord;
import yt_dlp;
import time;

import playerManager;

async def play(url : str, channel : discord.VoiceChannel):

    if (playerManager.voiceConnection == None):
        #Connect to voice channel
        playerManager.voiceConnection = await channel.connect()

    #Download song
    yt_dl_opts = {'format': 'bestaudio/best'}
    ytdl = yt_dlp.YoutubeDL(yt_dl_opts)
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

    #Play song
    ffmpeg_opts = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    song = data['url']
    player = discord.FFmpegPCMAudio(song, **ffmpeg_opts)
    playerManager.voiceConnection.play(player, after=lambda e: await nextSong(channel))
    playerManager.playing = True

    return data

async def nextSong(channel):
    if (playerManager.voiceConnection.is_playing()):
        playerManager.voiceConnection.stop()
    
    playerManager.playing = False

    if (len(playerManager.queue) > 0):
        await play(playerManager.queue[0], channel)
        playerManager.queue.pop(0)
    else:
        return None