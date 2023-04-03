import pathlib
import json
import discord
import sys
sys.path.append("..")

from discord.ext import tasks
from database.pong_database import add_user_to_db, remove_user_from_db
from reddit.reddit_functions import find_plays_and_ping

'''
This is the discord run file for the pong bot
'''


def run_discord(r):
    """
    Run the discord bot

    :param r:
    :return:
    """

    cur_dir = str(pathlib.Path(__file__).parent.absolute().parent.absolute())
    with open(cur_dir + '/configuration/config.json', 'r') as config_file:
        config_data = json.load(config_file)

    token = config_data['discord_token']
    prefix = config_data['prefix']

    intents = discord.Intents.default()
    intents.message_content = True
    intents.presences = True
    intents.members = True
    
    client = discord.Client(intents=intents)

    @tasks.loop(seconds=10)
    async def reddit_browser():
        await find_plays_and_ping(client, r)

    @client.event
    async def on_message(message):
        message_content = message.content.lower()

        if message_content.startswith(prefix + 'add'):
            if not await add_user_to_db(r, message, prefix):
                print('Error adding user to database')

        if message_content.startswith(prefix + 'delete'):
            if not await remove_user_from_db(r, message, prefix):
                print('Error adding user to database')

    @client.event
    async def on_ready():
        print('------')
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')
        reddit_browser.start()

    client.run(token)