import json
import pathlib

from database.pong_database import get_player_discord_id


async def ping_user(client, user, message_content):
    """
    Ping a user in a message

    :param client:
    :param user:
    :param message_content:
    :return:
    """

    cur_dir = str(pathlib.Path(__file__).parent.absolute().parent.absolute())
    with open(cur_dir + '\configuration\config.json', 'r') as config_file:
        config_data = json.load(config_file)

    # Check if the user is in the database
    discord_id = await get_player_discord_id(user)
    if not discord_id:
        print("User not signed up for pings, do not try to ping them")
        return False
    else:
        print("User is signed up for pings, ping them")
        channel = client.get_channel(int(config_data['channel_id']))
        user = await client.fetch_user(int(discord_id[0]))
        await channel.send(f"{user.mention} {message_content}")
        return True
