import pathlib
import json
import discord
import sys

print("Current sys.path:", sys.path)

from discord.ext import tasks
from fcfb.discord.commands import add_user_command, delete_me_command, delete_user_command
from fcfb.reddit.reddit_functions import find_plays_and_ping


'''
This is the discord run file for the pong bot
'''


def run_rotom(r):
    """
    Run the discord bot

    :param r:
    :return:
    """

    cur_dir = str(pathlib.Path(__file__).parent.absolute().parent.absolute())
    with open(cur_dir + '/configuration/config.json', 'r') as config_file:
        config_data = json.load(config_file)

    token = config_data['discord']['token']
    prefix = config_data['discord']['prefix']

    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    intents.presences = True
    client = discord.Client(intents=intents)

    @tasks.loop(seconds=10)
    async def reddit_browser():
        await find_plays_and_ping(client, r, config_data)

    @client.event
    async def on_message(message):
        try:
            message_content = message.content.lower()

            if message_content.startswith(prefix + 'add'):
                await add_user_command(r, config_data, message, prefix)

            elif message_content.startswith(prefix + 'delete_me'):
                await delete_me_command(config_data, message)

            elif message_content.startswith(prefix + 'delete'):
                await delete_user_command(config_data, message)
        except Exception as e:
            await message.channel.send(f"{e}")

    @client.event
    async def on_ready():
        print('------')
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')
        reddit_browser.start()

    client.run(token)
