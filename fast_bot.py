import math, random, time

THINK_DUR = 1

class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """
    def __init__(self, move = None, parent = None, state = None):
        self.move = move # the move that got us to this node - "None" for the root node
        self.parentNode = parent # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.who = state.get_whos_turn()
        self.untriedMoves = state.get_moves() # future child nodes
        self.playerJustMoved = state.get_whos_turn() # the only part of the state that the Node needs later

    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.childNodes, key = lambda c: c.wins/c.visits + math.sqrt(2*math.log(self.visits)/c.visits))[-1]
        return s

    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move = m, parent = self, state = s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n

    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(self.untriedMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
             s += c.TreeToString(indent+1)
        return s

    def IndentString(self,indent):
        s = "\n"
        for i in range (1,indent+1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
             s += str(c) + "\n"
        return s


def think(state, quip):
    rootnode = Node(state = state.copy())
    rootnode.visits = 1
    me = state.get_whos_turn()

    def outcome(score, player):
        """if me == 'red':
            return score['red'] - score['blue']
        else:
            return score['blue'] - score['red']"""
        nameDict = { "red": "blue", "blue" : "red"}
        name = nameDict[state.get_whos_turn()]
        if player.parentNode != None:
            return score[player.parentNode.who] - score[name]
        else: return 0

    timeStart = time.time()
    timeDead = timeStart + THINK_DUR
    iterations = 0
    while True:
        iterations += 1

        node = rootnode
        stateCopy = state.copy()

        while node.untriedMoves == [] and node.childNodes != []:
            #print "select"
            node = node.UCTSelectChild()
            stateCopy.apply_move(node.move)

        if node.untriedMoves != []:
            m = random.choice(node.untriedMoves)
            stateCopy.apply_move(m)
            node = node.AddChild(m, stateCopy)

        while stateCopy.get_moves() != []:
            for i in range(5):
                if stateCopy.is_terminal():
                    break
                stateCopy.apply_move(random.choice(stateCopy.get_moves()))

        while node != None:
            me = state.get_whos_turn()
            if node.parentNode == None:
                break
            node.Update(outcome(stateCopy.get_score(), node))
            node = node.parentNode

        timeNow = time.time()
        if timeNow > timeDead:
            break

    sampleRate = float(iterations)/(timeNow - timeStart)
    print sampleRate

    return sorted(rootnode.childNodes, key = lambda c: outcome(stateCopy.get_score(), node)+
                                                       math.sqrt(2*math.log(c.parentNode.visits)/c.visits))[-1].move

