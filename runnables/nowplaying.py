import discord


def command(bot):
    @bot.tree.command(name="nowplaying", description="Get information about the currently playing song")
    async def run(interaction: discord.Interaction):
        await interaction.response.send_message("To be implemented")
