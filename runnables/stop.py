import discord;
import playerManager;

def command(bot):
    @bot.tree.command(name="stop", description="Stop playing")
    async def run(interaction: discord.Interaction):
        try:
            playerManager.voiceConnection.stop()
            await interaction.response.send_message('Stopped playing')
        except Exception as e:
            await interaction.response.send_message(e)