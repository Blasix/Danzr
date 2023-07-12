import discord
import playerManager
import utilities.playUrl as playUrl


def command(bot):
    @bot.tree.command(name="skip", description="Skip the current song")
    async def run(interaction: discord.Interaction):
        try:
            # create embed
            embed = discord.Embed(
                title='❌ Nothing is playing ❌',
                color=discord.Colour.red(),
            )

            # Check if bot is playing and execute command
            if playerManager.voiceConnection.is_playing():
                embed.title = f'⏭️ Skipped the current song ⏭️'
                embed.color = discord.Colour.green()
                voice_channel = interaction.user.voice.channel
                await playUrl.nextSong(voice_channel)

            # Send embed
            await interaction.response.send_message(embed=embed)

        # Catch errors
        except Exception as e:
            print(e)
