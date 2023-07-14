import discord


def command(bot):
    @bot.tree.command(name="help", description="Learn how to use the bot")
    async def run(interaction: discord.Interaction):
        await interaction.response.send_message("Help is not implemented yet")
