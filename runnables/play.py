import asyncio;
import discord;
import yt_dlp;

async def play(interaction, song_url):
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
        player = discord.FFmpegPCMAudio(song, **ffmpeg_opts)

        vc.play(player)
        await interaction.response.send_message(f'Playing {data["title"]}')
    else:
        await interaction.response.send_message('User is not in a channel.')