PINGING_OFFENSE = """{team} has submitted their number. Please reply to [this comment]({comment_link}) with your number."""
PINGING_DEFENSE = """The [previous play result]({comment_link}) is in, the difference was **{difference}**. Please respond to [refbot's message]({inbox_link}) with your number."""
PINGING_GAME_START = """The game has started. Please respond to [refbot's message]({inbox_link}) with *heads* or *tails*."""
PINGING_COIN_TOSS_WINNER = """The coin flip result is in, you won the toss. Please respond to [refbot's message]({inbox_link}) with your number."""
REDDIT_PREFIX = "https://old.reddit.com"
REDDIT_INBOX_LINK = f"{REDDIT_PREFIX}/message/unread/"

def build_reddit_comment_link(comment_permalink: str) -> str:
    return f"{REDDIT_PREFIX}{comment_permalink}"

def build_ping_offense_message(team: str, comment_permalink: str) -> str:
    comment_link = build_reddit_comment_link(comment_permalink=comment_permalink)
    return PINGING_OFFENSE.format(team=team, comment_link=comment_link)

def build_ping_defense_message(difference: str, comment_permalink: str) -> str:
    comment_link = build_reddit_comment_link(comment_permalink=comment_permalink)
    return PINGING_DEFENSE.format(difference=difference, comment_link=comment_link, inbox_link=REDDIT_INBOX_LINK)

def build_ping_game_start_message() -> str:
    return PINGING_GAME_START.format(inbox_link=REDDIT_INBOX_LINK)

def build_ping_coin_toss_winner_message() -> str:
    return PINGING_COIN_TOSS_WINNER.format(inbox_link=REDDIT_INBOX_LINK)



