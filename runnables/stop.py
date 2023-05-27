import discord;
import playerManager;

def command(bot):
    @bot.tree.command(name="stop", description="Stop playing and clear the queue")
    async def run(interaction: discord.Interaction):
        try:
            if playerManager.voiceConnection.is_playing():
                playerManager.voiceConnection.stop()
                playerManager.queue = []
                playerManager.playing = False
                await interaction.response.send_message('Stopped playing')
            else:
                await interaction.response.send_message('Nothing is playing')
        except Exception as e:
            await interaction.response.send_message(e)