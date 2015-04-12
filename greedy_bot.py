__author__ = 'abuc_000'
import random
def think(state, quip):
    me = state.get_whos_turn()
    stateCopy = state.copy()
    for each in stateCopy.get_moves():
        stateCopy.apply_move(each)
        if stateCopy.get_score()[state.get_whos_turn()] > state.get_score()[state.get_whos_turn()]:
            return each
    return random.choice(state.get_moves())
    #should this be a random move or the first move if all moves increase the score the same amount


