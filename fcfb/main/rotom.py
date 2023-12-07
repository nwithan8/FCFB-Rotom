import sys

print("Current sys.path:", sys.path)

from run_rotom import run_rotom
from fcfb.reddit.reddit_setup import reddit_setup

print("Current sys.path:", sys.path)
sys.path.append("..")

# Main method
if __name__ == '__main__':
    r = reddit_setup()
    run_rotom(r)
    
