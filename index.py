import discord;
from discord.ext import commands;
import json;

import commandLoader;

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

#Load commands
commandLoader.loadCommands(bot)

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