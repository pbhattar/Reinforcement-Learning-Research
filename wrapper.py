import game
import states
import player

def updateStats(stats, count, winNum):
    #print "stats ", stats
    #print "count ", count
    if winNum == 2:
        stats[count] = "win"
    return stats

def iterate(graphicalR, numGames):
    #player1 = player.QPlayer(1, graphicalR[0], 0.3, 0.1, 0.1)
    player1 = player.RandomAgent(1, graphicalR[0])
    player2 = player.QPlayer(2, graphicalR[1], 0.4, 0.1, 0.2)
    stats = {}
    countNumGames = 0
    while countNumGames < numGames:
        print "Game ", countNumGames+1
        g = game.Game(player1, player2)
        #print "Player ", p.getID(),"'s turn." 
        #g.printGrid()
        lose = False
        turn = 0
        while lose == False and turn <9:
            state = g.getCurrentState()
            p = g.getCurrentPlayer()
            print ""
            print "Player ", p.getID(),"'s turn." 
            print ""
            g.printGrid()
            print ""
            action = p.getAction(state)
            g.update(p, action)
            if type(p) == player.QPlayer:
                nextState = g.getCurrentState()
                reward = g.getReward(state, p)
                p.updateValues(state, action, nextState, reward)
            turn += 1
            #g.printGrid()
            currentPlayer = g.getCurrentPlayer()
            win, lose = game.checkGrid(g, g.getCurrentState(), currentPlayer)
        g.printGrid()
        if lose ==True:
            winningPlayer = g.getNextPlayer(currentPlayer).getID()
            print "Player ",g.getNextPlayer(currentPlayer).getID()," wins."
            stats = updateStats(stats, countNumGames+1, winningPlayer)
        else:
            print "It is a tie."
        countNumGames += 1
    return stats    

def main():
    loop = 1000
    step = 100
    stats = iterate(("X","O"),loop)
    print stats
    record = {}
    for i in range(step,loop+1,step):
        record[i] = 0
    for key in stats:
        for r in record.keys():
            if key in range(r-step,r):
                record[r]+=1
    print record
        
