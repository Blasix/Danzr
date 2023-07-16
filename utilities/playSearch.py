import discord
import yt_dlp
import utilities.playUtils as Utils
import utilities.playUrl as playUrl
import playerManager


async def play(interaction: discord.Interaction, query: str):
    class PlaySearchView(discord.ui.View):
        songs = []

        async def send(self, interaction):
            select_embed = await self.create_embed()
            self.message = await interaction.followup.send(view=self, embed=select_embed)

        async def create_embed(self):
            await self.search_songs()
            if not self.songs:
                return discord.Embed(
                    title="No songs found",
                    color=discord.Colour.red()
                )
            embed = discord.Embed(
                title="Select a song",
                color=discord.Colour.blurple()
            )
            for i, song in enumerate(self.songs):
                embed.add_field(
                    name=f"**{i+1})** {song[1]}",
                    value=f"({song[2]}) - Song by {song[4]}",
                    inline=False,
                )
            await self.add_buttons()
            return embed

        async def search_songs(self):
            yt_dl_opts = {
                'format': 'bestaudio/best',
                'noplaylist': True,
                'skip_download': True,
                'extract_flat': True,
                '--write-thumbnail': True,
                '--no-check-certificate': True,
                '--no-mtime': True,
                '--no-part': True,
                '--socket-timeout': '5',
            }
            with yt_dlp.YoutubeDL(yt_dl_opts) as ytdl:
                data = ytdl.extract_info(
                    f"ytsearch5:{query}", download=False)['entries']
                for song in data:
                    self.songs.append(
                        (song['url'], song['title'], Utils.format_duration(song['duration']), song['thumbnails'][0]['url'], song['uploader'], song['view_count'], interaction.user.name))

        async def add_buttons(self):
            for i in range(1, min(len(self.songs), 5) + 1):
                button = discord.ui.Button(
                    label=str(i), style=discord.ButtonStyle.blurple)
                button.callback = getattr(
                    self, f"button{i}_callback")
                self.add_item(button)

        async def button1_callback(self, interaction: discord.Interaction):
            await self.play_song(interaction, 0)

        async def button2_callback(self, interaction: discord.Interaction):
            await self.play_song(interaction, 1)

        async def button3_callback(self, interaction: discord.Interaction):
            await self.play_song(interaction, 2)

        async def button4_callback(self, interaction: discord.Interaction):
            await self.play_song(interaction, 3)

        async def button5_callback(self, interaction: discord.Interaction):
            await self.play_song(interaction, 4)

        async def play_song(self, interaction: discord.Interaction, index: int):
            await interaction.response.defer()
            voice_channel = interaction.user.voice.channel
            if not playerManager.playing:
                await playUrl.play(self.songs[index][0], voice_channel)
                embed = discord.Embed(
                    title='🎶 Now playing 🎶',
                    description=f'{self.songs[index][1]}',
                    color=discord.Colour.green()
                )
            else:
                playerManager.queue.append(
                    (self.songs[index][0], self.songs[index][1], self.songs[index][2], self.songs[index][6]))
                embed = discord.Embed(
                    title='🎶 Added to queue 🎶',
                    description=f'{self.songs[index][1]}',
                    color=discord.Colour.green()
                )

            embed.set_thumbnail(url=f'{self.songs[index][3]}')
            embed.add_field(name='⏰ Duration',
                            value=f'{self.songs[index][2]}')
            embed.add_field(name='🧑‍🎨 Artist', value=f'{self.songs[index][4]}')
            embed.add_field(name='🔎 Views', value=f'{self.songs[index][5]:,}')
            embed.set_footer(
                text=f'Requested by {interaction.user.name}', icon_url=interaction.user.avatar.url)

            await interaction.edit_original_response(embed=embed, view=None)

    await PlaySearchView(timeout=None).send(interaction)
