import discord
import playerManager


def command(bot):
    @bot.tree.command(name="nowplaying", description="Get information about the currently playing song")
    async def run(interaction: discord.Interaction):
        # create embed
        embed = discord.Embed(
            title='❌ Nothing is playing ❌',
            color=discord.Colour.red(),
        )

        import discord


def command(bot):
    @bot.tree.command(name="nowplaying", description="Get information about the currently playing song")
    async def run(interaction: discord.Interaction):
        # create embed
        embed = discord.Embed(
            title='❌ Nothing is playing ❌',
            color=discord.Colour.red(),
        )

        if playerManager.voiceConnection is not None and playerManager.voiceConnection.is_playing():
            print(playerManager.nowPlaying)

            embed.title = '🎶 Now playing 🎶'
            embed.color = discord.Color.blurple()
            embed.set_thumbnail(url=playerManager.nowPlaying[0])
            embed.description = f"{playerManager.nowPlaying[1]} - {'artist'}"
            embed.add_field(name="Duration", value=playerManager.nowPlaying[2])
            embed.add_field(name="Requested by",
                            value=playerManager.nowPlaying[3])
        await interaction.response.send_message(embed=embed)
