import discord;
import playerManager;

def command(bot):
    @bot.tree.command(name="queue", description="Show the queue")
    async def run(interaction: discord.Interaction):
        if not playerManager.queue:
            await interaction.response.send_message("The queue is currently empty.")
        else:
            queue_embed = discord.Embed(
                title="Current Queue",
                description="\n".join([f"{index+1}. {song}" for index, song in enumerate(playerManager.queue)]),
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=queue_embed)
