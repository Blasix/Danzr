import asyncio;
import discord;
from discord import app_commands;
import yt_dlp;
import time;
import utilities.playUrl as playUrl;

import playerManager;

def command(bot):
    @bot.tree.command(name="play", description="Play a song")
    @app_commands.describe(url='The url of the song or playlist')
    async def run(interaction: discord.Interaction, url: str):
        
        #Pre response
        await interaction.response.defer()

        #Get video data
        yt_dl_opts = {'format': 'bestaudio/best'}
        ytdl = yt_dlp.YoutubeDL(yt_dl_opts)
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

        #Check if user is in a voice channel
        if interaction.user.voice != None:
            if (playerManager.playing == False):
                await playUrl.play(url, interaction.user.voice.channel)

<<<<<<< HEAD
            #Connect to voice channel
            voice_channel = interaction.user.voice.channel
            voice = discord.utils.get(bot.voice_clients, guild=interaction.guild)
            if voice == None:
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
                title = f'🎶 Now playing: 🎶',
                description = f'{data["title"]}',
                color = discord.Colour.green()
            )
=======
                #Create embed
                embed = discord.Embed(
                    title = f'🎶 Now playing 🎶',
                    description = f'{data["title"]}',
                    color = discord.Colour.green()
                )
            else:
                playerManager.queue.append(url)
                #Create embed
                embed = discord.Embed(
                    title = f'🎶 Added to queue 🎶',
                    description = f'{data["title"]}',
                    color = discord.Colour.green()
                )

            #Add video info
>>>>>>> c63bec5d2f37af2b0e4b7e42fa1c3e12cc6c0d90
            embed.set_thumbnail(url=data['thumbnail'])
            embed.add_field(name='⏰ Duration', value=time.strftime('%H:%M:%S', time.gmtime(data['duration'])))
            embed.add_field(name='🧑‍🎨 Artist', value=f'{data["uploader"]}')
            embed.add_field(name='🔎 Views', value=f'{data["view_count"]:,}')
<<<<<<< HEAD
            embed.set_footer(text=f'Requested by {interaction.user.name}', icon_url=interaction.user.avatar.url)

            await interaction.response.send_message(embed=embed)
=======
            embed.set_footer(text=f'🗣️ Requested by {interaction.user.name}', icon_url=interaction.user.avatar.url)
            await interaction.followup.send(embed=embed)
>>>>>>> c63bec5d2f37af2b0e4b7e42fa1c3e12cc6c0d90
        else:
            await interaction.response.send_message('User is not in a channel.')