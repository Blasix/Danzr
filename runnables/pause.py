import discord;
import playerManager;

def command(bot):
    @bot.tree.command(name="pause", description="Pause the music")
    async def run(interaction: discord.Interaction):
        try:
            if playerManager.voiceConnection.is_playing():
                playerManager.voiceConnection.pause()
                await interaction.response.send_message('Paused')
            else:
                await interaction.response.send_message('Nothing is playing')
        except Exception as e:
            await interaction.response.send_message(e)