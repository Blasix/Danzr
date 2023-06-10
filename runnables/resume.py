import discord;
import playerManager;

def command(bot):
    @bot.tree.command(name="resume", description="Resume playing")
    async def run(interaction: discord.Interaction):
        try:
            embed = discord.Embed(
                title = f'▶️ Resumed Playing ▶️',
                color = discord.Colour.green()
            )
            if playerManager.voiceConnection.is_paused():
                playerManager.voiceConnection.resume()
                await interaction.response.send_message(embed=embed)
            else:
                embed.title = '❌ The player is not paused ❌'
                embed.color = discord.Colour.red()
                await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(e)