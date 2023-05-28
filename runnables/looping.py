import discord

import playerManager   

def command(bot):
    @bot.tree.command(name="loop", description="Loop the queue")
    async def run(interaction: discord.Interaction):
        playerManager.looping = not playerManager.looping
        await interaction.response.send_message(f"Looping is now {'enabled' if playerManager.looping else 'disabled'}")