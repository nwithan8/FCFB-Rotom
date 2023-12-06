
from fcfb.api.deoxys.rotom_users import add_user, delete_user, get_user_by_reddit_username


async def add_user_command(r, config_data, message, prefix):
    """
    Add a user to the database

    :param r:
    :param config_data:
    :param message:
    :param prefix:
    :return:
    """

    try:
        # Get user information
        user = message.author
        discord_id = user.id
        if user.discriminator is None:
            discord_username = user.name
        else:
            discord_username = user.name + "%23" + user.discriminator

        reddit_username = message.content.split(prefix + "add ")[1]

        # Remove /u/ from reddit username if it exists
        if reddit_username.startswith("/u/"):
            reddit_username = reddit_username.replace("/u/", "")
        elif reddit_username.startswith("u/"):
            reddit_username = reddit_username.replace("u/", "")


        # Check if reddit username is valid
        try:
            r.redditor(reddit_username).id
        except Exception as e:
            raise Exception("User tried to add a non-existing reddit username, " + reddit_username)

        # Check if user is already in the database
        user = await get_user_by_reddit_username(config_data, reddit_username)
        if user is not None:
            raise Exception("User tried to add a user that is already in the database, " + reddit_username)

        # Add user to the database
        user = await add_user(config_data, discord_id, discord_username, reddit_username)
        if user is not None:
            if "%23" in discord_username:
                discord_username = discord_username.replace("%23", "#")
            await message.channel.send(f"Reddit user {reddit_username} added to the database and "
                                       f"tied to {discord_username}!")
            print("User added to the database, " + reddit_username)
            return
    except Exception:
        raise Exception(f"There was an issue adding the user to the database: {e}")


async def delete_me_command(config_data, message):
    """
    Delete the user who sent the request from the database

    :param config_data:
    :param message:
    :return:
    """

    try:
        # Get user information
        user = message.author
        discord_id = user.id
        if user.discriminator is None:
            discord_username = user.name
        else:
            discord_username = user.name + "#" + user.discriminator

        # Delete user from the database
        if await delete_user(config_data, discord_id) is True:
            await message.channel.send(f"User {discord_username} deleted from the database!")
            print("User deleted from the database, " + discord_username)
            return
    except Exception as e:
        raise Exception(f"There was an issue deleting the user who sent the request from the database: {e}")


async def delete_user_command(config_data, message):
    """
    Delete a user from the database based on their reddit username

    :param config_data:
    :param message:
    :return:
    """

    try:
        reddit_username = message.content.split(config_data["prefix"] + "delete ")[1]

        # Remove /u/ from reddit username if it exists
        if reddit_username.startswith("/u/"):
            reddit_username = reddit_username.replace("/u/", "")
        elif reddit_username.startswith("u/"):
            reddit_username = reddit_username.replace("u/", "")

        user = await get_user_by_reddit_username(config_data, reddit_username)
        if user is None:
            raise Exception("User tried to delete a user that is not in the database, " + reddit_username)
            return

        discord_id = user["discord_id"]
        discord_username = user["discord_username"]
        # Delete user from the database
        if await delete_user(config_data, discord_id) is True:
            await message.channel.send(f"User {discord_username} deleted from the database!")
            print("User deleted from the database, " + discord_username)
            return
    except Exception as e:
        raise Exception(f"There was an error deleting the user from the database: {e}")


