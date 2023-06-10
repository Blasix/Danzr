import asyncio
import discord
from discord import app_commands
import yt_dlp
import time
import utilities.playUrl as playUrl
import re

import playerManager

def command(bot):
    @bot.tree.command(name="play", description="Play a song")
    @app_commands.describe(url='The URL of the song or playlist')
    async def run(interaction: discord.Interaction, url: str):
        # Pre-response
        await interaction.response.defer()

        # Check if user is in a voice channel
        if interaction.user.voice is None or interaction.user.voice.channel is None:
            await interaction.response.send_message("You are not in a voice channel.")
            return

        voice_channel = interaction.user.voice.channel

        # Check if the URL is a playlist
        if 'playlist' in url:
            # Convert playlist to a list of video URLs
            video_urls = convert_playlist_to_queue(url)
            playerManager.queue.extend(video_urls)

            # Join the voice channel if not already connected
            if playerManager.voiceConnection is None or not playerManager.voiceConnection.is_connected():
                playerManager.voiceConnection = await voice_channel.connect()

            # Create an embed
            embed = discord.Embed(
                title=f'🎶 Playlist added to queue 🎶',
                description=f'{len(video_urls)} videos added from the playlist',
                color=discord.Colour.green()
            )
            embed.set_footer(text=f'Requested by {interaction.user.name}', icon_url=interaction.user.avatar.url)
            await interaction.followup.send(embed=embed)

            # Start playing if not already playing
            if not playerManager.playing:
                await playUrl.nextSong(voice_channel)
            
        else:
            # Check if the URL is a valid YouTube URL
            if not is_valid_youtube_url(url):
                await interaction.response.send_message("Invalid YouTube URL.")
                return

            # Get video data
            yt_dl_opts = {'format': 'bestaudio/best'}
            ytdl = yt_dlp.YoutubeDL(yt_dl_opts)
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            # Join the voice channel if not already connected
            if playerManager.voiceConnection is None or not playerManager.voiceConnection.is_connected():
                playerManager.voiceConnection = await voice_channel.connect()

            if not playerManager.playing:
                await playUrl.play(url, voice_channel)

                # Create embed
                embed = discord.Embed(
                    title=f'🎶 Now playing 🎶',
                    description=f'{data["title"]}',
                    color=discord.Colour.green()
                )
            else:
                playerManager.queue.append(url)
                # Create embed
                embed = discord.Embed(
                    title=f'🎶 Added to queue 🎶',
                    description=f'{data["title"]}',
                    color=discord.Colour.green()
                )

            # Add video info
            embed.set_thumbnail(url=data['thumbnail'])
            embed.add_field(name='⏰ Duration', value=time.strftime('%H:%M:%S', time.gmtime(data['duration'])))
            embed.add_field(name='🧑‍🎨 Artist', value=f'{data["uploader"]}')
            embed.add_field(name='🔎 Views', value=f'{data["view_count"]:,}')
            embed.set_footer(text=f'Requested by {interaction.user.name}', icon_url=interaction.user.avatar.url)
            await interaction.followup.send(embed=embed)

def convert_playlist_to_queue(playlist_url):
    yt_dl_opts = {
        'extract_flat': 'in_playlist',
        'skip_download': True,
        'quiet': True,
    }
    ytdl = yt_dlp.YoutubeDL(yt_dl_opts)
    playlist_data = ytdl.extract_info(playlist_url, download=False)

    video_urls = []
    for entry in playlist_data['entries']:
        if 'url' in entry:
            video_urls.append(entry['url'])

    return video_urls

def is_valid_youtube_url(url):
    youtube_regex = r"(?:https?://)?(?:www\.)?youtu(?:\.be/|be\.com/(?:watch\?(?:.*&)?v=|v/|embed/|.*[?&]v=))([^?&]{11})"
    match = re.match(youtube_regex, url)
    return match is not None