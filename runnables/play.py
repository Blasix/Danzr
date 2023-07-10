import asyncio
import discord
from discord import app_commands
from youtube_search import YoutubeSearch
import yt_dlp
import utilities.playUrl as playUrl
import re

import playerManager


def command(bot):
    @bot.tree.command(name="play", description="Play a song or playlist")
    @app_commands.describe(link_or_query='Play a song or playlist from a link or search query')
    async def run(interaction: discord.Interaction, link_or_query: str):
        # Pre-response
        await interaction.response.defer()

        # Check if user is in a voice channel
        if interaction.user.voice is None or interaction.user.voice.channel is None:
            await interaction.followup.send("You are not in a voice channel.")
            return

        # define voice_channel
        voice_channel = interaction.user.voice.channel

        # Check if it is a url
        if not is_valid_url(link_or_query):
            # TODO Make a selection menu for wich song to choose

            # get results
            results = YoutubeSearch(link_or_query, max_results=1).to_dict()
            url = "https://www.youtube.com" + results[0]['url_suffix']

            # Join the voice channel if not already connected
            if playerManager.voiceConnection is None or not playerManager.voiceConnection.is_connected():
                playerManager.voiceConnection = await voice_channel.connect()

            if not playerManager.playing:
                await playUrl.play(url, voice_channel)
                # Create embed
                embed = discord.Embed(
                    title=f'🎶 Now playing 🎶',
                    description=f'{results[0]["title"]}',
                    color=discord.Colour.green()
                )
            else:
                playerManager.queue.append(
                    (url, results[0]["title"], results[0]["duration"], interaction.user.name))
                # Create embed
                embed = discord.Embed(
                    title=f'🎶 Added to queue 🎶',
                    description=f'{results[0]["title"]}',
                    color=discord.Colour.green()
                )

            # Add video info
            embed.set_thumbnail(url=results[0]["thumbnails"][0])
            embed.add_field(name='⏰ Duration',
                            value=f'{results[0]["duration"]}')
            embed.add_field(name='🧑‍🎨 Artist',
                            value=f'{results[0]["channel"]}')
            embed.add_field(name='🔎 Views', value=f'{results[0]["views"]}')
            embed.set_footer(
                text=f'Requested by {interaction.user.name}', icon_url=interaction.user.avatar.url)
            await interaction.followup.send(embed=embed)
            return

        # Check if the URL is a playlist
        if 'playlist' in link_or_query:
            # Convert playlist to a list of video URLs
            video_urls = convert_playlist_to_queue(
                link_or_query, interaction.user.name)
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
            embed.set_footer(
                text=f'Requested by {interaction.user.name}', icon_url=interaction.user.avatar.url)
            await interaction.followup.send(embed=embed)

            # Start playing if not already playing
            if not playerManager.playing:
                await playUrl.nextSong(voice_channel)

        else:
            # Get video data
            yt_dl_opts = {'format': 'bestaudio/best'}
            ytdl = yt_dlp.YoutubeDL(yt_dl_opts)
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(link_or_query, download=False))

            # Join the voice channel if not already connected
            if playerManager.voiceConnection is None or not playerManager.voiceConnection.is_connected():
                playerManager.voiceConnection = await voice_channel.connect()

            if not playerManager.playing:
                await playUrl.play(link_or_query, voice_channel)

                # Create embed
                embed = discord.Embed(
                    title=f'🎶 Now playing 🎶',
                    description=f'{data["title"]}',
                    color=discord.Colour.green()
                )
            else:
                playerManager.queue.append(
                    (link_or_query, data['title'], format_duration(data['duration']), interaction.user.name))
                # Create embed
                embed = discord.Embed(
                    title=f'🎶 Added to queue 🎶',
                    description=f'{data["title"]}',
                    color=discord.Colour.green()
                )

            # Add video info
            embed.set_thumbnail(url=data['thumbnail'])
            embed.add_field(name='⏰ Duration',
                            value=format_duration(data['duration']))
            embed.add_field(name='🧑‍🎨 Artist', value=f'{data["uploader"]}')
            embed.add_field(name='🔎 Views', value=f'{data["view_count"]:,}')
            embed.set_footer(
                text=f'Requested by {interaction.user.name}', icon_url=interaction.user.avatar.url)
            await interaction.followup.send(embed=embed)


def convert_playlist_to_queue(playlist_url, user):
    yt_dl_opts = {
        'extract_flat': 'in_playlist',
        'skip_download': True,
        'quiet': True,
    }
    ytdl = yt_dlp.YoutubeDL(yt_dl_opts)
    playlist_data = ytdl.extract_info(playlist_url, download=False)

    video_urls = []
    for entry in playlist_data['entries']:
        video_urls.append(
            (entry['url'], entry['title'], format_duration(entry['duration']), user))

    return video_urls


def format_duration(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"


def is_valid_url(url):
    url_regex = r"^(http|https)://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(:[0-9]+)?(/[\w\-\.]*)*(\?[^\s]*)?$"
    return re.match(url_regex, url) is not None
