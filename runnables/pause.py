import discord;
import playerManager;

def command(bot):
    @bot.tree.command(name="pause", description="Pause the music")
    async def run(interaction: discord.Interaction):
        embed = discord.Embed(
            title = f'⏸️ Paused ⏸️',
            color = discord.Colour.green()
        )
        try:
            if playerManager.voiceConnection.is_playing():
                playerManager.voiceConnection.pause()
                await interaction.response.send_message(embed=embed)
            else:
                embed.title = '❌ Nothing is playing ❌'
                embed.color = discord.Colour.red()
                await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(e)