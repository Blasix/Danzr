import discord
import utilities.playUrl as playUrl

def command(bot):
    @bot.tree.command(name="skip", description="Skip the current song")
    async def run(interaction: discord.Interaction):
        embed = discord.Embed(
            title = f'⏭️ Skipped the current song ⏭️',
            color = discord.Colour.green()
        )
        voice_state = interaction.guild.get_member(bot.user.id).voice
        if voice_state is None or not voice_state.channel:
            embed.title = '❌ I am not currently connected to a voice channel ❌'
            embed.color = discord.Colour.red()
            await interaction.response.send_message(embed=embed)
            return
        
        await playUrl.nextSong(voice_state.channel)
        await interaction.response.send_message(embed=embed)