import discord
import yt_dlp
import utilities.playUtils as Utils
import utilities.playUrl as playUrl
import playerManager


async def play(interaction: discord.Interaction, query: str):
    class PlaySearchView(discord.ui.View):
        songs = []

        # send message
        async def send(self, interaction):
            selectEmbed = await self.createEmbed()
            self.message = await interaction.followup.send(view=self, embed=selectEmbed)

        # create embed
        async def createEmbed(self):
            await self.searchSongs()
            if len(self.songs) == 0:
                return discord.Embed(
                    title="No songs found",
                    color=discord.Colour.red()
                )
            embed = discord.Embed(
                title="Select a song",
                color=discord.Colour.blurple()
            )
            for i in range(len(self.songs)):
                embed.add_field(
                    name=f"**{i+1})** {self.songs[i][1]}",
                    value=f"({self.songs[i][2]}) - Song by {self.songs[i][4]}",
                    inline=False,
                )
            await self.addButtons()
            return embed

        # search for songs, collect data
        async def searchSongs(self):
            yt_dl_opts = {
                'format': 'bestaudio/best',
                'noplaylist': True,
                'skip_download': True,
                'extract_flat': True,
                '--write-thumbnail': True,
            }
            with yt_dlp.YoutubeDL(yt_dl_opts) as ytdl:
                # Get video data
                data = ytdl.extract_info(
                    f"ytsearch5:{query}", download=False)['entries']
                for i in range(len(data)):
                    self.songs.append(
                        (data[i]['url'], data[i]['title'], Utils.format_duration(data[i]['duration']), data[i]['thumbnails'][0]['url'], data[i]['uploader'], data[i]['view_count'], interaction.user.name))

        # add buttons
        async def addButtons(self):
            for i in range(1, min(len(self.songs), 5) + 1):
                button = discord.ui.Button(
                    label=str(i), style=discord.ButtonStyle.blurple)
                button.callback = getattr(
                    self, f"button{i}_callback")
                self.add_item(button)

        # button callbacks
        async def button1_callback(self, interaction: discord.Interaction):
            await self.playSong(interaction, 0)
            pass

        async def button2_callback(self, interaction: discord.Interaction):
            await self.playSong(interaction, 1)
            pass

        async def button3_callback(self, interaction: discord.Interaction):
            await self.playSong(interaction, 2)
            pass

        async def button4_callback(self, interaction: discord.Interaction):
            await self.playSong(interaction, 3)
            pass

        async def button5_callback(self, interaction: discord.Interaction):
            await self.playSong(interaction, 5)
            pass

        # play song
        async def playSong(self, interaction: discord.Interaction, index: int):
            await interaction.response.defer()
            voice_channel = interaction.user.voice.channel
            if not playerManager.playing:
                await playUrl.play(self.songs[index][0], voice_channel)
                # Create embed
                embed = discord.Embed(
                    title=f'🎶 Now playing 🎶',
                    description=f'{self.songs[index][1]}',
                    color=discord.Colour.green()
                )
            else:
                playerManager.queue.append(
                    (self.songs[index][0], self.songs[index][1], self.songs[index][2], self.songs[index][6]))
                # Create embed
                embed = discord.Embed(
                    title=f'🎶 Added to queue 🎶',
                    description=f'{self.songs[index][1]}',
                    color=discord.Colour.green()
                )

            # Add video info
            embed.set_thumbnail(url=f'{self.songs[index][3]}')
            embed.add_field(name='⏰ Duration',
                            value=f'{self.songs[index][2]}')
            embed.add_field(name='🧑‍🎨 Artist', value=f'{self.songs[index][4]}')
            embed.add_field(name='🔎 Views', value=f'{self.songs[index][5]:,}')
            embed.set_footer(
                text=f'Requested by {interaction.user.name}', icon_url=interaction.user.avatar.url)

            await interaction.edit_original_response(embed=embed, view=None)

    await PlaySearchView(timeout=None).send(interaction)
