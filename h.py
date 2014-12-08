'''This is the main homomorphism code that makes an MDP abstract. Although, compare with h_Friday.py'''

import numpy as np
import MDP
import itertools
import util

actionCode = {}
actionCode[0] = 'north'
actionCode[1] = 'south'
actionCode[2] = 'east'
actionCode[3] = 'west'
actionCode[4] = 'exit'

def tupelize(state):
    return tuple((state.transpose().tolist())[0])

def makeStateList(i, numStates):
    return ([0] * i) + [1] + [0] * (numStates - i - 1)

def getCoarsePartitions(R, states):
    states_P = {}
    reward_P = {}
    r_P = {}
    for i in range(R.shape[1]):
        if R.item(i) in reward_P.keys():
            reward_P[R.item(i)].append(states[i])
        else:
            reward_P[R.item(i)] = [states[i]]

    #make a reversed reward dict

    items = reward_P.items() #abstract state to other states and reward
    for i in range(len(reward_P)):
        states_P[i] = reward_P[R.item(i)]
        r_P[i] = R.item(i)

    tempReward = {} #for partitioning
    for item in reward_P.items():
        for state in item[1]:
            tempReward[tupelize(state)] = item[0]
    reward_P = r_P

    return states_P, reward_P, tempReward 

def tempFunc(states): #only for debugging
    states_P = {}
    states_P[0] = []
    for state in states:
        #state = tupelize(state)
        states_P[0].append(state)
    return states_P

def getProbVector(states_P, state, t):
    prob_vector = [0] * len(states_P.keys())
    #print "prob_vector ", prob_vector
    #[2,0,1]
    #[0,1,2]
    for i in states_P.keys():
        prob = 0
        for congruentState in states_P[i]:
            p = (congruentState.transpose() * (t.transpose() * state))[0,0] 
            prob += p
        prob_vector[i] = prob
    prob_vector
    return prob_vector

def getReward(vec, state):
    return (vec * state)[0,0]

def valueFunction(mdp):
    realValues = util.Counter()
    checkPolicy = {}
    discount = 0.8
    rewardVec = mdp.getReward()
    
    for k in range(3):
        for state in mdp.getStates():
            maxSum = float('-inf')
            reward = getReward(rewardVec, state)
            for action in mdp.getActions(state): #iterate through actions
                SuccessorStatesAndProbs = (mdp.getTransitionProbabilities(action)).transpose()
                fromState = SuccessorStatesAndProbs * state
                assert (fromState.sum() == 1 or fromState.sum() ==0)
                sum = 0
                for nextState in mdp.getStates():
                    
                    probability = (nextState.transpose() * fromState)[0,0]
                    nextState = tuple(nextState.transpose().tolist()[0])
                    sum += (probability * (reward + discount*(realValues[nextState])))
                if sum > maxSum:
                    maxSum = sum
                    maxAction = action
            state = tuple(state.transpose().tolist()[0])
            #state = (state.transpose().tolist()[0]).index(1)
            realValues[state] = maxSum
            checkPolicy[state] = maxAction
    return realValues, checkPolicy



#mapping
def getMappedPolicy(stateActToAbsAct,states_abs, absPolicy, mdp):
    global actionCode
    numAbsStates = len(states_abs.keys())
    realPolicy = {}

    states_abs_inverse = {} 
    pairs = states_abs.items()
    for oneItem in pairs:
        for realState in oneItem[1]:
            states_abs_inverse[realState] = oneItem[0]

    for state in mdp.getStates():
        abstractState = states_abs_inverse[state]
        abstractState = makeStateList(abstractState, numAbsStates)
        absAct = absPolicy[tuple(abstractState)]
        actions = mdp.getActions(state)
        for action in actions:
            stateTemp = tuple((state.transpose().tolist())[0])
            t = (stateTemp,action)
            gOfS = stateActToAbsAct[t]
            if gOfS == absAct:
                realPolicy[stateTemp] = actionCode[action]
    return realPolicy

def main(filename):
    mdp = MDP.MDP(filename)
    #realMDP
    realValues, checkPolicy = valueFunction(mdp)
    #print "realValues ", realValues
    #print "checkPolicy", checkPolicy
    R = mdp.getReward()
    states = mdp.getStates()
    #states_P, reward_P, tempReward = getCoarsePartitions(R, states)
    states_P = tempFunc(states)
            
    loop = True
    while loop == True:
        prob_stateAction = {}
        absActionToProb = {}
        absActionToProb_inverse = {}
        absActionsRewardToStates = {}
        actionsAvailable = {}
        stateActToAbsAct = {}
        numAction = 0
        #construct mapping from action predictions to (state,action) labels
        for state in states:
            stateTemp = tupelize(state)
            actionsAvailable[stateTemp] = set([])
            for action in mdp.getActions(state): #change this to getActions(state)
                t = mdp.getTransitionProbabilities(action)
                prob_vector = getProbVector(states_P, state, t) 
                prob_vector = tuple(prob_vector)
                #print "stateAction ", state , " ", action
                #print "prob_vector ", prob_vector
                if prob_vector in prob_stateAction.keys():
                    (prob_stateAction[prob_vector]).append((stateTemp,action))  #have a map from numbers(abstract actions) to state and actions
                else:
                    absActionToProb[numAction] = prob_vector
                    absActionToProb_inverse[prob_vector] = numAction
                    numAction += 1
                    prob_stateAction[prob_vector] = [(stateTemp,action)]
                stateActToAbsAct[(stateTemp, action)] = absActionToProb_inverse[prob_vector] #prob_stateAction_inverse
                actionsAvailable[stateTemp].add(absActionToProb_inverse[prob_vector])

            reward = getReward(R , state)
            actions_available = tuple(actionsAvailable[stateTemp])
            if (actions_available, reward)  in absActionsRewardToStates:
                absActionsRewardToStates[(actions_available, reward)].append(state)
            else:
                absActionsRewardToStates[(actions_available, reward)] = [state]
                
        initialPartitionSize = len(states_P.keys())
        new_states_P = {}
        keys = absActionsRewardToStates.keys() 
        for i in range(len(keys)):
            values = absActionsRewardToStates[keys[i]]
            new_states_P[i] = values

        finalPartitionSize = len(new_states_P.keys())
        #print "newStates ",new_states_P

        if finalPartitionSize == initialPartitionSize:
            loop = False
            reward_P = {}
            absState_to_absActions = {}
            new_states_P = {}
            #print "key ",absActionsRewardToStates.keys()

            states_P_inverse = {}
            for absNum in states_P.keys():
                realStates = states_P[absNum]
                for realState in realStates:
                    states_P_inverse[realState] = absNum
                    
            for actionReward in absActionsRewardToStates.keys():
                stateList = absActionsRewardToStates[actionReward]
                absNum = states_P_inverse[stateList[0]]
                absState_to_absActions[absNum] = actionReward[0]
                reward_P[absNum] = actionReward[1]
        else:
            states_P = new_states_P
            

    absMDP = MDP.AbstractMDP(absState_to_absActions, states_P, reward_P, absActionToProb)
    abstractValues, absPolicy = valueFunction(absMDP)
    realPolicy = getMappedPolicy(stateActToAbsAct,states_P, absPolicy, mdp)
    return mdp, absMDP, states_P, stateActToAbsAct, reward_P

    



    


