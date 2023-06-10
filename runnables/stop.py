import discord;
import playerManager;

def command(bot):
    @bot.tree.command(name="stop", description="Stop playing and clear the queue")
    async def run(interaction: discord.Interaction):
        try:
            embed = discord.Embed(
                title = f'🛑 Stopped playing 🛑',
                color = discord.Colour.green()
            )
            if playerManager.voiceConnection.is_playing():
                playerManager.voiceConnection.stop()
                playerManager.queue = []
                playerManager.playing = False
                await interaction.response.send_message(embed=embed)
            else:
                embed.title = '❌ Nothing is playing ❌'
                embed.color = discord.Colour.red()
                await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(e)