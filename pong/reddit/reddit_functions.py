from database.pong_database import mark_comment_processed, check_if_comment_processed
from discord.discord_functions import ping_user


def parse_user_from_play_comment(comment):
    """
    Parse the user from the comment

    :param comment:
    :return:
    """

    # Get the user from the comment
    user = comment.body.split(" reply")[0].split("u/")[1]
    return user


def parse_team_from_play_comment(comment):
    """
    Parse the team from the comment

    :param comment:
    :return:
    """

    # Get the team from the comment
    team = comment.body.split(" has submitted their number")[0]
    return team


def parse_user_from_result_comment(comment):
    """
    Parse the user from the comment

    :param comment:
    :return:
    """

    # Get the user from the comment
    user = comment.body.split(" [](#datatag")[0].split("u/")[1]
    return user


def parse_difference_from_result_comment(comment):
    """
    Parse the difference from the comment

    :param comment:
    :return:
    """

    # Get the difference from the comment
    difference = comment.body.split("Difference: ")[1].split("\n")[0]
    return difference


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


async def find_plays_and_ping(client, r):
    """
    Look for plays in game threads

    :param client:
    :param r:
    :return:
    """

    # Get comments from refbot that haven't been processed
    user = r.redditor('NFCAAOfficialRefBot')
    for comment in user.comments.new(limit=20):
        submission_id = comment.link_id.split("_")[1]

        if await check_if_comment_processed(comment.id, submission_id):
            return

        # Ignore situations when the comment is not the latest in the thread
        # if not await check_if_latest_comment_in_thread_matches(comment, r.submission(id=comment.link_id.split("_")[1])):
        #     return

        # Handle play pings to the offense
        if "has submitted their number" in comment.body:
            team = parse_team_from_play_comment(comment)
            user = parse_user_from_play_comment(comment)
            message = ("The " + team + " have submitted their number. Please reply to this comment with your number, "
                       + "feel free to ignore this ping if you already have done so: "
                       + "https://www.old.reddit.com" + comment.permalink)
            if await ping_user(client, user, message):
                await mark_comment_processed(comment.id, submission_id)
        # Handle play result pings to the defense
        elif "Difference" in comment.body:
            user = parse_user_from_result_comment(comment)
            difference = parse_difference_from_result_comment(comment)
            message = ("The previous play result is in, the difference was " + difference +
                       ". Please respond to refbot's message with your number. You can view the result at the link "
                       + "below, feel free to ignore this ping if you already have done so: "
                       + "https://www.old.reddit.com" + comment.permalink)
            if await ping_user(client, user, message):
                await mark_comment_processed(comment.id, submission_id)
