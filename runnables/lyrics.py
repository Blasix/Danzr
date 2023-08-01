# https://www.youtube.com/watch?v=XP6IPsQh79Y
import discord


def command(bot):
    @bot.tree.command(name="lyrics", description="Get the lyrics of the currently playing song")
    async def run(interaction: discord.Interaction):
        await interaction.response.send_message('Coming soon!')
