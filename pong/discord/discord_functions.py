import json
import pathlib
import sys
sys.path.append("..")

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
    with open(cur_dir + '/configuration/config.json', 'r') as config_file:
        config_data = json.load(config_file)

    # Check if the user is in the database
    discord_id = await get_player_discord_id(user)
    if not discord_id:
        print("User not signed up for pings, do not try to ping them")
        return False
    else:
        print("User is signed up for pings, ping them")
        server_name = client.guild.name
        print(server_name)
        if server_name == "Fake College Football":
            channel = client.get_channel(int(config_data['fbs_channel_id']))
            try:
                user = await client.fetch_user(int(discord_id[0]))
            except:
                return False

            await channel.send(f"{user.mention} {message_content}")
            return True
        elif server_name == "Fake FCS":
            channel = client.get_channel(int(config_data['fcs_channel_id']))
            try:
                user = await client.fetch_user(int(discord_id[0]))
            except:
                return False

            await channel.send(f"{user.mention} {message_content}")
            return True
