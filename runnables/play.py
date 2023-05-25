import asyncio;
import discord;
import yt_dlp;
import time;
import utilities.playUrl as playUrl;

import playerManager;

def command(bot):
    @bot.tree.command(name="play", description="Play a song")
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
            embed.set_thumbnail(url=data['thumbnail'])
            embed.add_field(name='⏰ Duration', value=time.strftime('%H:%M:%S', time.gmtime(data['duration'])))
            embed.add_field(name='🧑‍🎨 Artist', value=f'{data["uploader"]}')
            embed.add_field(name='🔎 Views', value=f'{data["view_count"]:,}')
            embed.set_footer(text=f'🗣️ Requested by {interaction.user.name}', icon_url=interaction.user.avatar.url)
            await interaction.followup.send(embed=embed)
        else:
            await interaction.response.send_message('User is not in a channel.')