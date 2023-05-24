# This example requires the 'message_content' intent.

import discord
from discord import app_commands
from discord.ext import commands


# class MyClient(discord.Client):
#     async def on_ready(self):
#         print(f'Logged on as {self.user}!')

#     async def on_message(self, message):
#         print(f'Message from {message.author}: {message.content}')


# intents = discord.Intents.default()
# intents.message_content = True

# client = MyClient(intents=intents)
# client.run('ODgxMDg5OTI2NzY5MjgzMDky.Gx9LC0.k2dS2eAhPe4mSoCGlAaM-KYsbbgz7MlzKarzcs')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print('Bot is ready')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)


@bot.tree.command(name='hello', description='Says hello to you')
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hello {interaction.user.mention}!')

bot.run('ODgxMDg5OTI2NzY5MjgzMDky.Gx9LC0.k2dS2eAhPe4mSoCGlAaM-KYsbbgz7MlzKarzcs')
