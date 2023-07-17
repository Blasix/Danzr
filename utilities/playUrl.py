import asyncio
import discord
import yt_dlp

import playerManager


async def play(url: str, channel: discord.VoiceChannel):
    if playerManager.voiceConnection is None:
        # Connect to voice channel
        playerManager.voiceConnection = await channel.connect()

    try:
        # Download song
        yt_dl_opts = {'format': 'bestaudio/best'}
        ytdl = yt_dlp.YoutubeDL(yt_dl_opts)
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

        # Play song
        ffmpeg_opts = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        song = data['url']
        player = discord.FFmpegPCMAudio(song, **ffmpeg_opts)
        playerManager.voiceConnection.play(
            player, after=lambda e: sync(channel))
        playerManager.playing = True

        return data

    except Exception as e:
        print(e)
        nextSong(channel)
        return None


def sync(channel):
    async def wrapper(channel):
        await nextSong(channel)
    asyncio.run(wrapper(channel))


async def nextSong(channel):
    if playerManager.voiceConnection.is_playing():
        playerManager.voiceConnection.stop()

    playerManager.playing = False

    if len(playerManager.queue) > 0:
        await play(playerManager.queue[0][0], channel)
        if playerManager.looping == True:
            playerManager.queue.append(playerManager.queue[0])
        playerManager.nowPlaying = playerManager.queue[0]
        playerManager.queue.pop(0)
    else:
        return None
