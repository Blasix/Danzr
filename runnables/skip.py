import discord
import utilities.playUrl as playUrl

def command(bot):
    @bot.tree.command(name="skip", description="Skip the current song")
    async def run(interaction: discord.Interaction):
        voice_state = interaction.guild.get_member(bot.user.id).voice
        if voice_state is None or not voice_state.channel:
            await interaction.response.send_message("I am not currently connected to a voice channel.")
            return
        
        await playUrl.nextSong(voice_state.channel)
        await interaction.response.send_message("Skipped the current song.")