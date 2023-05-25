import discord;

def command(bot):
    @bot.tree.command(name="shuffle", description="Shuffle the queue")
    async def run(interaction: discord.Interaction):
        await interaction.response.send_message('Je moeder.')