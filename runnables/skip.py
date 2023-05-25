import discord;
import utilities.playUrl as playUrl;


def command(bot):
    @bot.tree.command(name="skip", description="Skip the current song")
    async def run(interaction: discord.Interaction):
        await playUrl.nextSong(interaction.user.voice.channel)