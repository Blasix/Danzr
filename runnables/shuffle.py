import discord
import random

import playerManager

def command(bot):
    @bot.tree.command(name="shuffle", description="Shuffle the queue")
    async def run(interaction: discord.Interaction):
        queue = playerManager.queue
        random.shuffle(queue)

        await interaction.response.send_message("Queue shuffled!")