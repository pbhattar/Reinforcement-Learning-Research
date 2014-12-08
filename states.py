class State(object):
    def __init__(self, game, prevState = None, player = None, action = None):
        if prevState == None:
            self.grid = {}
            actions = game.getActions()
            for action in actions:
                self.grid[action] = None
        else:
            self.grid = prevState.grid
            self.grid[action] = player

    def getGrid(self):
        return self.grid

    def getActions(self):
        availableActions = []
        for key in self.grid:
            if self.grid[key] == None:
                availableActions.append(key)
        return availableActions

'''
game:
getActions
getPlayerType
'''
