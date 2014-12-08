import util
import random

class Player(object):
    def __init__(self, i, typeR):
        self.identity = i
        self.typeR = typeR

    def getType(self):
        return self.typeR

    def getID(self):
        return self.identity

class QPlayer(Player):
    def __init__(self, i, typeR, alpha, discount, epsilon):
        self.qValue = util.Counter()
        self.alpha = alpha
        self.discount = discount
        self.typeR = typeR
        self.identity = i
        self.epsilon = epsilon

    def getAction(self, state):
        actions = state.getActions()
        prob = util.flipCoin(self.epsilon)
        if prob:
            chosen = random.choice(actions)
        else:
            print "return action" 
            val = float('-inf')
            for action in actions:
                newVal = self.getQValue((state,action))
                if newVal > val:
                    chosen = action
                    newVal = val
            #print "self.qValue ", self.qValue
        return chosen

    def getQValue(self,(state,action)):
        return self.qValue[(state, action)] 

    def updateValues(self, state, action, nextState, reward):
        nextAction = self.getAction(nextState)
        Qsa = (float)(self.getQValue((state,action)))
        QsaPrime = (float)(self.getQValue((nextState, nextAction)))
        Qsa += self.alpha*((reward + self.discount * QsaPrime) - Qsa)
        self.qValue[(state, action)] = Qsa  

class User(Player):
    def __init__(self, i, typeR):
        self.typeR = typeR
        self.identity = i

    def getAction(self,state):
        availableActions = state.getActions()
        loop = True
        while loop == True:
            chosen = input("Your turn. Pick a slot.")
            if chosen in availableActions:
                loop = False
        return chosen

class RandomAgent(Player):
    def __init__(self, i , typeR):
        self.typeR = typeR
        self.identity = i

    def getAction(self, state):
        availableActions = state.getActions()
        return random.choice(availableActions)
