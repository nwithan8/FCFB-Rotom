import sys

from fcfb.api.deoxys.rotom_users import get_user_by_reddit_username

sys.path.append("..")


async def ping_user(client, config_data, reddit_username, message_content):
    """
    Ping a user in a message

    :param client:
    :param config_data:
    :param reddit_username:
    :param message_content:
    :return:
    """

    # Check if the user is in the database
    user = await get_user_by_reddit_username(config_data, reddit_username)
    if user is None:
        return
    else:
        channel = client.get_channel(int(config_data['discord']['ping_channel_id']))
        try:
            user = await client.fetch_user(int(user["discord_id"]))
            await channel.send(f"{user.mention} {message_content}")
            return
        except Exception as e:
            raise Exception(f"Error pinging user in server: {e}")
