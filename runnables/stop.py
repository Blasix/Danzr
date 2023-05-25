import discord;
import playerManager;

def command(bot):
    @bot.tree.command(name="stop", description="Stop playing")
    async def run(interaction: discord.Interaction):
        try:
            if playerManager.voiceConnection.is_playing():
                playerManager.voiceConnection.stop()
                await interaction.response.send_message('Stopped playing')
            else:
                await interaction.response.send_message('Nothing is playing')
        except Exception as e:
            await interaction.response.send_message(e)