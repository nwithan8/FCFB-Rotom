import sys

sys.path.append("..")

from run_rotom import run_rotom
from fcfb.reddit.reddit_setup import reddit_setup

# Main method
if __name__ == '__main__':
    r = reddit_setup()
    run_rotom(r)
    
