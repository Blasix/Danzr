import discord;
import playerManager;

def command(bot):
    @bot.tree.command(name="resume", description="Resume playing")
    async def run(interaction: discord.Interaction):
        try:
            playerManager.voiceConnection.resume()
            await interaction.response.send_message('Resumed playing')
        except Exception as e:
            await interaction.response.send_message(e)