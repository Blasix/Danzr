import discord
import playerManager


def command(bot):
    @bot.tree.command(name="loop", description="Loop the queue")
    async def run(interaction: discord.Interaction):
        playerManager.looping = not playerManager.looping
        # create embed
        embed = discord.Embed(
            title=f"Looping is now {'enabled' if playerManager.looping else 'disabled'}",
            color=discord.Colour.blurple(),
        )
        await interaction.response.send_message(embed=embed)
