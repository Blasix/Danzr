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
                # because playURl already plays the next song we just need to stop the current one
                if playerManager.voiceConnection.is_playing():
                    playerManager.voiceConnection.stop()
                playerManager.playing = False

            # Send embed
            await interaction.response.send_message(embed=embed)

        # Catch errors
        except Exception as e:
            print(e)
