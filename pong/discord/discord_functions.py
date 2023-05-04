import json
import pathlib
import sys

sys.path.append("..")

from database.pong_database import get_player_discord_id, get_player_server_to_ping


async def ping_user(client, user, message_content):
    """
    Ping a user in a message

    :param client:
    :param user:
    :param message_content:
    :return:
    """

    cur_dir = str(pathlib.Path(__file__).parent.absolute().parent.absolute())
    with open(cur_dir + '/configuration/config.json', 'r') as config_file:
        config_data = json.load(config_file)

    # Check if the user is in the database
    discord_id = await get_player_discord_id(user)
    if not discord_id:
        print("User not signed up for pings, do not try to ping them")
        return False
    else:
        print("User is signed up for pings, ping them")
        server_to_ping = await get_player_server_to_ping(user)
        if not server_to_ping:
            server_to_ping = 0
        else:
            server_to_ping = server_to_ping[0]
        for guild in client.guilds:
            server_name = guild.name
            if server_name == "Fake College Football" and (server_to_ping == 1 or server_to_ping == 0):
                channel = client.get_channel(int(config_data['fbs_channel_id']))
                try:
                    user = await client.fetch_user(int(discord_id[0]))
                    await channel.send(f"{user.mention} {message_content}")
                except:
                    print("Error pinging user in main server")
                    continue

            elif server_name == "Fake FCS" and (server_to_ping == 2 or server_to_ping == 0):
                channel = client.get_channel(int(config_data['fcs_channel_id']))
                try:
                    user = await client.fetch_user(int(discord_id[0]))
                    await channel.send(f"{user.mention} {message_content}")
                except:
                    print("Error pinging user in FCS server")
                    continue

        return True
