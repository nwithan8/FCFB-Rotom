import sys

from fcfb.api.deoxys.processed_comments import get_processed_comment, add_processed_comment
from fcfb.discord.utils import ping_user

sys.path.append("..")


def parse_user_from_play_comment(comment):
    """
    Parse the user from the comment

    :param comment:
    :return:
    """

    # Get the user from the comment
    user_list = [comment.body.split(" reply")[0].split("u/")[1]]
    return user_list


def parse_multiple_users_from_play_comment(comment):
    """
    Parse multiple users from the comment

    :param comment:
    :return:
    """

    # Get the users from the comment
    user_list = [comment.body.split(" reply")[0].split(" and /u/")[0].split("u/")[1],
                 comment.body.split(" reply")[0].split(" and /u/")[1]]
    return user_list


def parse_team_from_play_comment(comment):
    """
    Parse the team from the comment

    :param comment:
    :return:
    """

    # Get the team from the comment
    team = comment.body.split(" has submitted their number")[0]
    return team


def parse_multiple_users_from_result_comment(comment):
    """
    Parse multiple users from the comment

    :param comment:
    :return:
    """

    # Get the user from the comment
    user_list = [comment.body.split(" [](#datatag")[0].split(" and /u/")[0].split("u/")[1],
                 comment.body.split(" [](#datatag")[0].split(" and /u/")[1]]
    return user_list


def parse_user_from_result_comment(comment):
    """
    Parse the user from the comment

    :param comment:
    :return:
    """

    # Get the user from the comment
    user_list = [comment.body.split(" [](#datatag")[0].split("u/")[1]]
    return user_list


def parse_difference_from_result_comment(comment):
    """
    Parse the difference from the comment

    :param comment:
    :return:
    """

    # Get the difference from the comment
    difference = comment.body.split("Difference: ")[1].split("\n")[0]
    return difference


def parse_user_from_start_comment(comment):
    """
    Parse the coin flip user from the comment

    :param comment:
    :return:
    """

    return comment.body.split("you're home. /u/")[1].split(", you're away")[0]


def parse_user_from_coin_flip_result_comment(comment):
    """
    Parse the coin flip winner from the comment

    :param comment:
    :return:
    """

    return comment.body.split("/u/")[1].split(", ")[0]


async def check_if_latest_comment_in_thread_matches(comment, submission):
    """
    Check if the latest comment in the thread matches the comment

    :param comment:
    :param submission:
    :return:
    """

    # Get the latest comment in the thread
    submission.comments.replace_more(limit=None)
    latest_comment = submission.comments.list()[-1]

    for comment in latest_comment:
        print(comment.body)

    # Check if the latest comment in the thread matches the comment
    if comment.id == latest_comment.id:
        return True
    else:
        return False


async def find_plays_and_ping(client, r, config_data):
    """
    Look for plays in game threads

    :param client:
    :param r:
    :param config_data:
    :return:
    """

    # Get comments from refbot that haven't been processed
    user = r.redditor('NFCAAOfficialRefBot')
    for comment in user.comments.new(limit=20):
        submission_id = comment.link_id.split("_")[1]

        # Filter out processed comments
        if await get_processed_comment(config_data, comment.id) is not None:
            return

        # Handle play pings to the offense
        if "has submitted their number" in comment.body:
            team = parse_team_from_play_comment(comment)
            if comment.body.count("/u/") == 1:
                user_list = parse_user_from_play_comment(comment)
            else:
                user_list = parse_multiple_users_from_play_comment(comment)
            message = (team + " has submitted their number. Please reply to this comment with your number, "
                       + "feel free to ignore this ping if you already have done so: "
                       + "<https://old.reddit.com" + comment.permalink + ">")
            for user in user_list:
                if await ping_user(client, config_data, user, message):
                    await add_processed_comment(config_data, comment.id, submission_id)
        # Handle play result pings to the defense
        elif "Difference" in comment.body:
            if comment.body.count("/u/") == 1:
                user_list = parse_user_from_result_comment(comment)
            else:
                user_list = parse_multiple_users_from_result_comment(comment)
            difference = parse_difference_from_result_comment(comment)
            message = ("The previous play result is in, the difference was " + difference +
                       ". Please respond to refbot's message with your number. You can view the result at the link "
                       + "below, feel free to ignore this ping if you already have done so: "
                       + "<https://old.reddit.com" + comment.permalink + ">")
            for user in user_list:
                if await ping_user(client, config_data, user, message):
                    await add_processed_comment(config_data, comment.id, submission_id)
        # Handle start of game message, the coin flip
        elif "Happy Gameday!" in comment.body:
            user = parse_user_from_start_comment(comment)
            message = ("The game has started, please respond to refbot's message with heads or tails. You can view the "
                       + "result at the link below, feel free to ignore this ping if you already have done so: "
                       + "<https://old.reddit.com" + comment.permalink + ">")
            if await ping_user(client, config_data, user, message):
                await add_processed_comment(config_data, comment.id, submission_id)
        # Handle coin flip result
        elif "won the toss" in comment.body:
            user = parse_user_from_coin_flip_result_comment(comment)
            message = ("The coin flip result is in, you won the toss. Please respond to refbot's message with your "
                        + "number. You can view the result at the link below, feel free to ignore this ping if you "
                        + "already have done so: https://old.reddit.com" + comment.permalink)
            if await ping_user(client, config_data, user, message):
                await add_processed_comment(config_data, comment.id, submission_id)
