import discord;

def command(bot):
    @bot.tree.command(name="queue", description="Show the queue")
    async def run(interaction: discord.Interaction):
        await interaction.response.send_message('Je moeder.')