#from random import choice
import states
#import player

def checkGrid(game, state, player):
    grid = state.getGrid()
    selff = player
    opponent = game.getNextPlayer(player)
    win = False
    lose = False
    for i in range(3):
        #horizontal
        if (grid[(i,0)] == selff and grid[(i,1)] == selff and grid[(i,2)] == selff):
            win = True
        elif (grid[(i,0)] == opponent and grid[(i,1)] == opponent and grid[(i,2)] == opponent):
            lose = True
        #verticle
        elif (grid[(0,i)] == selff and grid[(1,i)] == selff and grid[(2,i)] == selff):
            win = True
        elif (grid[(0,i)] == opponent and grid[(1,i)] == opponent and grid[(2,i)] == opponent):
            lose = True
    if (grid[(0,0)] == selff and grid[(1,1)]== selff and grid[(2,2)] == selff):
        win = True
    elif (grid[(0,2)] == selff and grid[(1,1)] == selff and grid[(2,0)] == selff):
        win = True
    elif (grid[(0,0)] == opponent and grid[(1,1)]== opponent and grid[(2,2)] == opponent):
        lose = True
    elif (grid[(0,2)] == opponent and grid[(1,1)] == opponent and grid[(2,0)] == opponent):
        lose = True
    return win,lose

class Game(object):
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

        listOfActions = []
        for x in range(3):
            for y in range(3):
                listOfActions.append((x,y))
        self.actions = listOfActions
       
        self.currentState = states.State(self)
        self.currentPlayer = self.player1
        
    def printGrid(self):
        grid = self.currentState.getGrid()
        for x in range(3):
            rowString = ""
            for y in range(3):
                slot = grid[(x,y)]
                if slot == None:
                    rowString += "  |"
                else:
                    rowString += slot.getType() + " |"
            print "|"+rowString
            print "-----------"

    def getCurrentState(self):
        return self.currentState
        
    def getCurrentPlayer(self):
        return self.currentPlayer

    def getNextPlayer(self, player):
        if player == self.player1:
            return self.player2
        else:
            return self.player1

    def update(self, player, action):
        newState = states.State(self, self.currentState, player, action)
        self.currentState = newState
        self.currentPlayer = self.getNextPlayer(player)

    def getReward(self, state, player):
        win, lose = checkGrid(self, state, player)
        if win == True:
            return 10
        elif lose == True:
            return -10
        else:
            return 0

    def getActions(self):
        return self.actions
                

#816
#357
#492
