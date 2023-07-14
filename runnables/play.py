import asyncio
import discord
from discord import app_commands
import yt_dlp
import utilities.playUrl as playUrl
import utilities.playSearch as playSearch
import utilities.playUtils as Utils

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
        if not Utils.is_valid_url(link_or_query):
            print("not url")
            await playSearch.play(interaction, link_or_query)
            return

        # Check if the URL is a playlist
        if 'playlist' in link_or_query:
            # Convert playlist to a list of video URLs
            data = Utils.convert_playlist_to_queue(
                link_or_query, interaction.user.name)

            # Join the voice channel if not already connected
            if playerManager.voiceConnection is None or not playerManager.voiceConnection.is_connected():
                playerManager.voiceConnection = await voice_channel.connect()

            # add playlist to queue
            if not playerManager.playing:
                await playUrl.play(data[0][0], voice_channel)
                playerManager.queue.extend(data[1:])
            else:
                playerManager.queue.extend(data)

            # Create an embed
            embed = discord.Embed(
                title=f'🎶 Playlist added to queue 🎶',
                description=f'{len(data)} videos added from the playlist',
                color=discord.Colour.green()
            )
            embed.set_footer(
                text=f'Requested by {interaction.user.name}', icon_url=interaction.user.avatar.url)
            await interaction.followup.send(embed=embed)

        else:
            print("not playlist")
            # Get video data
            yt_dl_opts = {
                'format': 'bestaudio/best',
                'noplaylist': True,
                'skip_download': True,
                'extract_flat': True,
                '--write-thumbnail': True,
            }
            ytdl = yt_dlp.YoutubeDL(yt_dl_opts)
            data = ytdl.extract_info(link_or_query, download=False)

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
                    (link_or_query, data['title'], Utils.format_duration(data['duration']), interaction.user.name))
                # Create embed
                embed = discord.Embed(
                    title=f'🎶 Added to queue 🎶',
                    description=f'{data["title"]}',
                    color=discord.Colour.green()
                )

            # Add video info
            embed.set_thumbnail(url=data['thumbnail'])
            embed.add_field(name='⏰ Duration',
                            value=Utils.format_duration(data['duration']))
            embed.add_field(name='🧑‍🎨 Artist', value=f'{data["uploader"]}')
            embed.add_field(name='🔎 Views', value=f'{data["view_count"]:,}')
            embed.set_footer(
                text=f'Requested by {interaction.user.name}', icon_url=interaction.user.avatar.url)
            await interaction.followup.send(embed=embed)
