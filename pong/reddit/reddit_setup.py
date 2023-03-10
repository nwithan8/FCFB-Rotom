import json
import pathlib
import praw

'''
This is the reddit setup file for the pong bot
'''


def reddit_setup():
    """
    Login to reddit
    :return:
    """

    cur_dir = str(pathlib.Path(__file__).parent.absolute().parent.absolute())
    with open(cur_dir + '/configuration/config.json', 'r') as config_file:
        config_data = json.load(config_file)

    r = praw.Reddit(user_agent=config_data['user_agent'],
                    client_id=config_data['client_id'],
                    client_secret=config_data['client_secret'],
                    username=config_data['username'],
                    password=config_data['password'],
                    subreddit=config_data['subreddit'],
                    check_for_async=False)
    return r
