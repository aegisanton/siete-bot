"""
Discord bot for GBF crew Luminosity. Author: Anton#9396
Parts of code borrowed from Krypton's bot template: https://github.com/kkrypt0nn
"""

import os
import json
import sys
import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Bot

DEBUG = False

if DEBUG:
    if not os.path.isfile('config.json'):
        sys.exit('config.json is required!')
    else:
        with open('config.json') as f:
            config = json.load(f)
            TOKEN = config['token']
            PREFIX = config['prefix']
else:
    TOKEN = os.environ['discord_token']
    PREFIX = os.environ['prefix']
    
intents = disnake.Intents.default()
bot = Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    """
    """
    print(f'{bot.user.name} connected to Discord')

@bot.event
async def on_message(message):
    """
    """
    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)

@bot.event
async def on_slash_command(interaction) -> None:
    """
    The code in this event is executed every time a slash command has been *successfully* executed
    :param interaction: The slash command that has been executed.
    """
    print(
        f"Executed {interaction.data.name} command in {interaction.guild.name} (ID: {interaction.guild.id}) by {interaction.author} (ID: {interaction.author.id})")

def init_commands(command_type):
    for file in os.listdir(f'./cogs/{command_type}'):
        if file.endswith('.py'):
            file_name = file[:-3]
            try:
                bot.load_extension(f'cogs.{command_type}.{file_name}')
                print(f'Loaded extension {file_name}')
            except Exception as e:
                error = f'{type(e).__name__}: {e}'
                print(f'Failed to load extension {file_name}')
                
if __name__ == '__main__':
    init_commands('slash')
    #init_commands('normal')
    
bot.run(TOKEN)


