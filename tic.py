from random import choice

def printGrid():
    global representations
    print representations[1], representations[2], representations[3]
    print representations[4], representations[5], representations[6]
    print representations[7], representations[8], representations[9]

def changeGrid(playerMove, playerTurn):
    global representations
    global available
    playerNumber = int(playerMove)
    #temp = list(representations)
    if playerTurn == 1:
        representations[representations.index(playerNumber)] = [playerNumber]
    else:
        representations[representations.index(playerNumber)] = (playerNumber,)
    print available
    available.remove(playerNumber)

def getPossCombinations(r):
    return [[r[1],r[2],r[3]],[r[4],r[5],r[6]],[r[7],r[8],r[9]],[r[1],r[4],r[7]],[r[2],r[5],r[8]],[r[3],r[6],r[9]],[r[1],r[5],r[9]],[r[3],r[5],r[7]]]
#816
#357
#492

def checkGrid(player):
    global representations
    win = False
    if player == 1:
        test = type([])
    else:
        test = type(())
    possCombinations = getPossCombinations(representations)
    for comb in possCombinations:
        tempList = [x for x in comb if type(x) != test]
        if len(tempList) < 1:
            win = True
    return win
    
def checkOffenseDefense(comb):
    global available
    offense = 0
    #defense = 0
    for number in comb:
        if type(number) ==  list:
            offense += 1
    if offense > 1:
        concern = True
        defenseMove = [x for x in comb if (type(x) != list)][0]
        if defenseMove in available:
            return defenseMove
    return None

def defensive():
    global representations
    global available
    possCombinations = getPossCombinations(representations)
    defenseMove = None
    combNum = 0
    while defenseMove == None and combNum < len(possCombinations):
        comb = possCombinations[combNum]
        combNum +=1
        defenseMove = checkOffenseDefense(comb)
    if defenseMove != None:
        return defenseMove
    else:
        return choice(list(available))

def game(i, agent):
    global representations
    global available
    print "player ", i 
    loop = True
    if agent == 0 or i ==1:
        while loop == True:
            chosenNumber = input("Your turn. Pick a number that is still available")
            if chosenNumber in available:
                loop = False
    elif i == 2:
        chosenNumber = defensive()
    changeGrid(chosenNumber, i)
    printGrid()
    win = checkGrid(i)
    return win

def main(agent):
    global representations
    global available
    win = False
    printGrid()
    i = 1
    numTurns = 0
    while win == False and numTurns != 9:
        win = game(i, agent)
        numTurns += 1
        if i ==1:
            i = 2
        else:
            i = 1
    if win ==True:
        print "game over! Player ", i , " loses."
    else:
        print "its a tie"

representations =   [0,8,1,6,3,5,7,4,9,2]
available = set(representations)

