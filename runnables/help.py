import discord


def command(bot):
    @bot.tree.command(name="help", description="Learn how to use the bot")
    async def run(interaction: discord.Interaction):
        embed = discord.Embed(color=discord.Color.blurple(),
                              )
        embed.add_field(name="Commands", value="`/play <song>` - Play a song\n`/queue` - Show the queue\n`/nowplaying` - Get information about the currently playing song\n`/skip` - Skip the current song\n`/stop` - Stop the player\n`/pause` - Pause the player\n`/resume` - Resume the player\n`/shuffle` - Shuffle the queue\n`/loop` - Loop the queue\n`/help` - Learn how to use the bot")
        await interaction.response.send_message(embed=embed)
        await interaction.response.send_message(embed=embed)
