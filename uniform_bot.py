__author__ = 'abuc_000'
import random
#testing github

def think(state, quip):
    print state.get_score()
    return random.choice(state.get_moves())
