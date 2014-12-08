import numpy as np
import math
import count2 #for finding combs
import itertools
#from copy import deepcopy
import h

class State(object):
    def __init__(self, literals, id):
        self.literals = literals
        self.id = id
        self.actions = None
    
    def getLiterals(self):
        return self.literals

    def getID(self):
        return self.id

    def getActions(self):
        return self.actions

    def setActions(self, actions):
        self.actions = actions

class Action(object):
    def __init__(self, name, preconditions, outcome):
        self.name = name
        self.preconditions = preconditions
        self.outcome = outcome

    def getPreconditions():
        return self.preconditions

    def getOutcome():
        return self.outcome
        
        

class MDP(object):
    def __init__(self, listOfBlocks):
        self.list = listOfBlocks
        self.goal = None

        #different ways of slicing, different combinations, different permutations
        numBlocks = len(listOfBlocks)
        pileTypes = count2.findCombs(numBlocks)
        states = []
        for pileDistribution in pileTypes:
            differentPiles = []
            listOfPermutations = list(itertools.permutations(self.list, len(self.list)))
            #print "permutations ", listOfPermutations
            for permutation in listOfPermutations:
                oneState = []
                start = 0
                for pileSize in pileDistribution:
                    aPile = permutation[start: start+pileSize]
                    start += pileSize
                    oneState.append(aPile)
                oneState = sorted(oneState)
                if oneState not in states:
                    states.append(oneState)
                        
        
        self.stateObjects = []
        check = []
        self.states = []
        self.actions = {}
        for i in range(len(states)):
            ID = i
            state = []
            for pile in states[i]:
                #print "pile ", pile
                if len(pile) == 1:
                    #print "true "
                    state.append(tuple([('g', pile[0])]))
                else:
                    temp = []
                    for i in range(len(pile) -1):
                        temp.append((pile[i], pile[i+1]))
                    #print "pile here ", pile
                    temp.insert(0, ('g', pile[0]))
                    state.append(tuple(temp))
                    #print "and pile here ", pile
            #print "state ",state
            check.append(tuple(state))
            print "ID ", ID
            sList = h.makeStateList(ID, len(states))
            sMatrix = np.matrix(sList)
            self.states.append(sMatrix)
            self.actions[ID] = [] #things will be added later
            s = State(tuple(state), ID)
            self.stateObjects.append(s)

        print "finalStates ", self.stateObjects
        print "check ", check
            
        actionToStates = {}
        for block1 in self.list:
            tempList = list(self.list)
            tempList.remove(block1)
            for block2 in tempList:
                action = "move"+block1+"to"+block2
                actionToStates[action] = []
                for state in self.stateObjects:
                    stateLiterals = state.getLiterals()
                    nextState = list(stateLiterals)
                    pickUp = False
                    putDown = False
                    
                    for Originalpile in stateLiterals:
                        pile = list(Originalpile)
                        lastBlock = pile[-1][-1]
                        if lastBlock == block1:
                            #nextState = list(stateLiterals)
                            pickUp = True
                            tempp = pile.pop()
                            #print "pile now is ", pile
                            nextState[nextState.index(Originalpile)] = tuple(pile)
                            #print "nextState now is ", nextState
                            if () in nextState:
                                nextState.remove(())
                        #print "and nextState now is ", nextState
                        if lastBlock == block2:
                            putDown = True
                            pile.append((block2, block1))
                            nextState[nextState.index(Originalpile)] = tuple(pile)
                    nextState = tuple(nextState)
                    if pickUp == True and putDown == True:
                        for state2 in self.stateObjects:
                            print "state2 literals are ", state2.getLiterals()
                            print "nextState is ", nextState
                            if set(state2.getLiterals()) == set(nextState):
                                actionToStates[action].append((state.getID(), state2.getID()))
            
            action = "move"+block1+"toFloor"
            actionToStates[action] = []
            for state in self.stateObjects:
                stateLiterals = state.getLiterals()
                nextState = list(stateLiterals)
                pickUp = False
                for Originalpile in stateLiterals:
                    pile = list(Originalpile)
                    lastBlock = pile[-1][-1]
                    if lastBlock == block1 and len(pile) > 1:
                        #nextState = list(stateLiterals)
                        pickUp = True
                        tempp = pile.pop()
                        #print "pile now is ", pile
                        nextState[nextState.index(Originalpile)] = tuple(pile)
                        #print "nextState now is ", nextState
                        if () in nextState:
                            nextState.remove(())
                    else:
                       print "for action ", action, " its false: ", stateLiterals
    

                if pickUp == True:
                    nextState.append((('g',block1),))
                    nextState = tuple(nextState)
                    print "starting state is ", state.getLiterals()
                    print "nextState is ", nextState
                    for state2 in self.stateObjects:
                        print "state2 literals are ", state2.getLiterals()
                        if set(state2.getLiterals()) == set(nextState):
                            print "true"
                            actionToStates[action].append((state.getID(), state2.getID()))
                        else:
                            print "false"
                                #print "and nextState now is ", nextState
            
        
        numStates = len(self.stateObjects)
        self.transitions = {}
        for a in actionToStates.keys():
            fromToStates = actionToStates[a]
            listOfLists = []
            for s in self.stateObjects:
                sID = s.getID()
                for pair in fromToStates:
                    if sID == pair[0]:
                        nextID = pair[1]
                        self.actions[sID].append(a)
                    else:
                        nextID = None
                if nextID == None:
                    row = [0] * numStates
                else:
                    row = ([0] * (nextID)) + [1] + ([0] * (numStates - nextID - 1))
                listOfLists.append(row)
            self.transitions[a] = np.matrix(listOfLists)
            print "actionMatrix ", listOfLists
            print "done"
    
    
    def getStates(self):
        return self.states

    def getActions(self, state):
        stateN = h.getStateNum(state)
        return self.actions[state]

    def getStateObjects(self):
        return self.stateObjects

    def getReward(self): #have to set goal first
        rewardL = [-1] * len(self.states)
        rewardL[self.goal] = 50
        self.reward = np.matrix(rewardL).transpose()
        return self.reward

    def setGoalState(literals):
        for stateObj in self.stateObjects:
            if stateObj.getLiterals() == literals:
                goalNum = stateObj.getID()
        self.goal = goalNum

    def getTransitionProbabilities(self, action):
        return self.transitions[action]
        
    #def main():
a = MDP(["a","b"])
    
    
        
        
    
