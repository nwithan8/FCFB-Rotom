from pong.discord.run_discord import run_discord
from pong.reddit.reddit_setup import reddit_setup

# Main method
if __name__ == '__main__':
    r = reddit_setup()
    run_discord(r)
