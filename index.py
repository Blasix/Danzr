import discord;
from discord import app_commands;
from discord.ext import commands;
import json;

import runnables.play as play;

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

#import play command
@bot.tree.command(name='play', description='play a song')
@app_commands.describe(song_url='The song to play')
async def say(interaction: discord.Interaction, song_url: str):
    await play.play(interaction, song_url)

#Load bot
@bot.event
async def on_ready():
    print('Bot is ready')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)

#Login to discord
f = open('data.json')
data = json.load(f)
bot.run(data['token'])
f.close()