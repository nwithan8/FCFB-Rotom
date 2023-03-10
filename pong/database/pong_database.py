import json
import pathlib
import mariadb
import praw
from prawcore.exceptions import NotFound

'''
This is the database functions file for the pong bot
'''


async def connect_to_db():
    """
    Connect to the database

    :return:
    """

    cur_dir = str(pathlib.Path(__file__).parent.absolute().parent.absolute())
    with open(cur_dir + '/configuration/config.json', 'r') as config_file:
        config_data = json.load(config_file)

    # Connect to MariaDB Platform
    try:
        db = mariadb.connect(
            user=config_data['db_user'],
            password=config_data['db_password'],
            host=config_data['db_host'],
            port=int(config_data['db_port']),
            database=config_data['db_name'],
        )

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None

    return db


async def check_if_comment_processed(comment_id, submission_id):
    """
    Check if the comment has already been processed

    :param submission_id:
    :param comment_id:
    :return:
    """

    # Connect to the database
    db = await connect_to_db()
    if db is None:
        print("Error connecting to the database, please try again later")
        return False

    cursor = db.cursor()
    cursor.execute("SELECT * FROM processed_comments_tbl WHERE comment_id = ? AND submission_id = ?", (comment_id,submission_id))
    comment_in_db = cursor.fetchone()
    db.close()

    if comment_in_db is None:
        return False
    else:
        return True


async def check_amount_of_comments_processed(db):
    """
    Check how many comments have been processed

    :param db:
    :return:
    """

    cursor = db.cursor()
    cursor.execute("SELECT * FROM processed_comments_tbl")
    num_comments = cursor.rowcount

    return num_comments


async def mark_comment_processed(comment_id, submission_id):
    """
    Mark a comment as processed

    :param submission_id:
    :param comment_id:
    :return:
    """

    # Connect to the database
    db = await connect_to_db()
    if db is None:
        print("Error connecting to the database, please try again later")
        return False

    cursor = db.cursor()
    cursor.execute("INSERT INTO processed_comments_tbl (comment_id, submission_id) VALUES (?, ?)", (comment_id, submission_id))
    db.commit()

    if await check_amount_of_comments_processed(db) > 200:
        cursor.execute("DELETE FROM processed_comments_tbl WHERE comment_id = (SELECT comment_id FROM "
                       "processed_comments_tbl ORDER BY comment_id ASC LIMIT 1)")
        db.commit()
        print("Deleted oldest comment from processed_comment_tbl")

    db.close()

    return True


async def get_player_discord_id(user):
    """
    Get the discord id of a player via their reddit username

    :param user:
    :return:
    """

    # Connect to the database
    db = await connect_to_db()
    if db is None:
        print("Error connecting to the database, please try again later")
        return False

    cursor = db.cursor()
    cursor.execute("SELECT user_id FROM user_tbl WHERE reddit_username = ?", (user,))
    discord_id = cursor.fetchone()
    db.close()

    if discord_id is None:
        return False
    else:
        return discord_id


async def check_user_in_db(db, user_id):
    """
    Check if user is in the database

    :param db:
    :param user_id:
    :return:
    """

    cursor = db.cursor()
    cursor.execute("SELECT * FROM user_tbl WHERE user_id = ?", (user_id,))
    user_in_db = cursor.fetchone()

    return user_in_db


async def add_user_to_db(r, message, prefix):
    """
    Add a user to the database

    :param r:
    :param prefix:
    :param message:
    :return:
    """

    # Connect to the database
    db = await connect_to_db()
    if db is None:
        await message.channel.send("Error connecting to the database, please try again later")
        return False

    # Get user information
    user = message.author
    discord_username = user.name + "#" + user.discriminator
    user_id = user.id

    reddit_username = message.content.split(prefix + "add ")[1]

    if "/u/" in reddit_username:
        await message.channel.send("Please do not include /u/ in your reddit username")
        print("User tried to add /u/ in their reddit username")
        db.close()
        return False

    # Check if reddit username is valid
    try:
        r.redditor(reddit_username).id
    except NotFound:
        await message.channel.send("The reddit username you are trying to add does not exist!")
        print("User tried to add a non-existing reddit username, " + reddit_username)
        db.close()
        return False

    # Check if user is already in the database
    user_in_db = await check_user_in_db(db, user_id)
    if user_in_db is not None:
        await message.channel.send("The user you are trying to add is already in the database! Please note that you "
                                   + "cannot sign any other user up for game pings but yourself")
        print("User tried to add a user that is already in the database, " + reddit_username)
        db.close()
        return False

    # Add user to the database
    try:
        cursor = db.cursor()
        cursor.execute("INSERT INTO user_tbl (user_id, discord_username, reddit_username) VALUES (?, ?, ?)",
                       (user_id, discord_username, reddit_username))
        db.commit()
        db.close()
        await message.channel.send("User " + reddit_username + " added to the database and is now signed up for pings!")
        print("User " + reddit_username + " added to the database!")
        return True
    except Exception as e:
        await message.channel.send("Error adding user to database, please try again later")
        print("Error adding user to database: " + str(e))
        db.close()
        return False


async def remove_user_from_db(r, message, prefix):
    """
    Remove a user to the database

    :param r:
    :param prefix:
    :param message:
    :return:
    """

    # Connect to the database
    db = await connect_to_db()
    if db is None:
        await message.channel.send("Error connecting to the database, please try again later")
        return False

    # Get user information
    reddit_username = message.content.split(prefix + "delete ")[1]

    # Check if user exists in the database
    user_in_db = await check_user_in_db(db, reddit_username)
    if user_in_db is None:
        await message.channel.send("The user you are trying to remove is not in the database, please verify the "
                                   + "username or alternatively they are already deleted!")
        print("User tried to remove a user that isn't in the database, " + reddit_username)
        db.close()
        return False

    # Remove user to the database
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM user_tbl WHERE reddit_username = ?", (reddit_username,))
        db.commit()
        db.close()
        await message.channel.send("User " + reddit_username + " is removed from the database!")
        print("User " + reddit_username + " removed from the database!")
        return True
    except Exception as e:
        await message.channel.send("Error removing user from database, please try again later")
        print("Error removing user from database: " + str(e))
        db.close()
        return False
