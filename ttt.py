def createGrid():
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

def checkGrid(player):
    global representations
    win = False
    if player == 1:
        test = type([])
    else:
        test = type(())
    for i in range(3):
        #verticle
        if (type(representations[i + 1]) == test and type(representations[i+4]) == test and type(representations[i+7]) == test):
            win = True
        #horizontal
        elif (type(representations[(i+1)+(2*i)]) ==test and type(representations[(i+1)+(2*i) + 1])==test and type(representations[(i+1)+(2*i) + 2]) ==test):
            win = True
    #diagonals
    if (type(representations[1])== test and type(representations[5])== test and type(representations[9])== test) or (type(representations[3])== test and type(representations[5])== test and type(representations[7])== test):
        win = True
    return win

#816
#357
#492
def heur():
    global representations
    opponent = type([])
    computer = type(())
    possCombinations = [[8,1,6],[3,5,7],[4,9,2],[8,3,4],[1,5,9],[6,7,2],[8,5,9],[6,5,4]] 
    twoOpponentStrikes = False
    #for comb in possCombinations:
        
    

def game(i, agent):
    global representations
    global available
    print "player ", i 
    loop = True
    if agent == 0 or i==1:
        while loop == True:
            chosenNumber = input("Your turn. Pick a number that is still available")
            if chosenNumber in available:
                loop = False
    elif i ==2:
        chosenNumber = heur()
    changeGrid(chosenNumber, i)
    createGrid()
    win = checkGrid(i)
    return win

def main(agent = 0):
    global representations
    global available
    win = False
    createGrid()
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

#816
#357
#492
