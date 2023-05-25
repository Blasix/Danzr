import asyncio;
import discord;
import yt_dlp;
import time;

import playerManager;

def command(bot):
    @bot.tree.command(name="play", description="Play a song")
    async def run(interaction: discord.Interaction, url: str):
        yt_dl_opts = {'format': 'bestaudio/best'}
        ytdl = yt_dlp.YoutubeDL(yt_dl_opts)

        #Check if user is in a voice channel
        if interaction.user.voice != None:

            #Connect to voice channel
            voice_channel = interaction.user.voice.channel
            playerManager.voiceConnection = await voice_channel.connect()

            #Download song
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            #Play song
            ffmpeg_opts = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            song = data['url']
            player = discord.FFmpegPCMAudio(song, **ffmpeg_opts)
            playerManager.voiceConnection.play(player)

            #Create embed
            embed = discord.Embed(
                title = f'🎶 Now playing 🎶',
                description = f'{data["title"]}',
                color = discord.Colour.green()
            )
            embed.set_thumbnail(url=data['thumbnail'])
            embed.add_field(name='⏰ Duration', value=time.strftime('%H:%M:%S', time.gmtime(data['duration'])))
            embed.add_field(name='🧑‍🎨 Artist', value=f'{data["uploader"]}')
            embed.add_field(name='🔎 Views', value=f'{data["view_count"]:,}')
            embed.set_footer(text=f'🗣️ Requested by {interaction.user.name}', icon_url=interaction.user.avatar.url)

            await interaction.channel.send(embed=embed)
        else:
            await interaction.response.send_message('User is not in a channel.')