from discord.run_discord import run_discord
from reddit.reddit_setup import reddit_setup

# Main method
if __name__ == '__main__':
    r = reddit_setup()
    run_discord(r)
