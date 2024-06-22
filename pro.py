from operator import indexOf
import numpy as np
import random
import copy
from PyQt5.QtCore import QPoint


class Pro:

    matrix = np.array(
        [[x, y] for y in range(16, 420, 100) for x in range(14, 420, 100)]
    ).reshape((5, 5, 2))# (rows, cols, [x, y]) (3D)
    allRowCOl = [[x, y] for x in range(5) for y in range(5)]#[row, column] * 24 index (2D)
    players = [[p0 for p0 in range(13, 25)], [p1 for p1 in range(12)]]#player one=[0] and player two=[1]
    """Track list for one turn indexes:
      allIndex: [index 0 for player1 or index 1 for player2, index from 0 to 24]
      playersIndex: index from 0 to 11 for player 1 or 2
      [0]: selected rock = allIndex
      [1]: removed rocks = [[allIndex, playersIndex], ..]
      [2]: double jump = [True or False] only one index
    """
    track = []
    disabledRocks = []# [playerIndex, playerIndex, ..] -> list of lists
    rocks = [[], []]# index 0 for player1 label list and index 1 for player2 label list
    buttons = []# index 0 for player 1 and index 1 for player 2 (only users)
    popupMessage = ""
    locTrack = QPoint(0, 0)
    # playTurn = 0 or 1 (1 for player 1 turn and 0 for player 2 turn)
    playTurn = 1
    """menuResult: 
      index 0 = if 1: User vs Computer (One player). if 2: user vs user (Two player)
      index 1 = if 0: Easy. if 1: Normal. if 2: Hard
    """
    menuResult = [2, 0]
    imgPath = ["rock1.png", "rock2.png"]
    hovImgPath = ["rock11.png", "rock21.png"]
    buttonsText = ["Player one end turn", "Player two end turn"]
    resButtons = ["Restart game", "Back to menu", "EXIT"]
    fMenuBttns = ["One player", "Two player", "Exit"]
    sMenuBttns = ["Easy", "Normal", "Hard", "Back"]
    startTurn = ["    PLAYER TWO TURN    ", "    PLAYER ONE TURN    "]
    resultMsg = "Game over"
    plHoSty = """
        PlaceHolder {
            background:transparent;
            background-repeat: no-repeat; 
            background-position: center;
        }
        """
    drLabSty = """
        DragableLabel {
            background:transparent;
        }
        """
    bttnSty = """
        QPushButton {
        background-color: #07193b;
        color: #8c8c5f;
        border-style: outset;
        padding: 2px;
        font: italic 25px;
        border-width: 4px;
        border-radius: 20px;
        border-color: #0a2454;
        }
        QPushButton:hover {
            background-color: #020d21;
            border-color: #03173d;
            color: #c1c284;
        }
        """
    reBttnSty = """
        QPushButton {
        background:transparent;
        color: #060c1f;
        border-style: outset;
        padding: 5px;
        font: bold 33px;
        border-width: 4px;
        border-radius: 30px;
        border-color: #597be3;
        }
        QPushButton:hover {
            border-color: #466bdb;
            color: #020717;
        }
        """
    menuBttnSty = """
        QPushButton {
        background:transparent;
        color: #d1d1d1;
        border-style: outset;
        padding: 5px;
        font: bold 33px;
        border-width: 6px;
        border-radius: 30px;
        border-color: #919191;
        }
        QPushButton:hover {
            border-color: #bdbdbd;
            color: #e8e8e8;
        }
        """
    bckBttnSty = """
        QPushButton {
        background-color: #15364d;
        color: #93b5cc;
        border-style: outset;
        padding: 2px;
        font: italic 15px;
        border-width: 6px;
        border-radius: 35px;
        border-color: #0a2454;
        }
        QPushButton:hover {
            background-color: #072e47;
            border-color: #03173d;
            color: #a9c0cf;
        }
        """
    msgSty = """
        QLabel {
            color: cyan;
            font: italic 16px;
            padding: 5px;
            border-style: outset;
            border-radius: 15px;
            border-width: 3px;
            border-color: #0a2454;
        }
        """
    rMsgSty = """
        QLabel {
            color: #010a26;
            font: bold 50px;
        }
        """
    gNameSty = """
        QLabel {
            color: #e8e8e8;
            font: bold 50px;
        }
        """

    def resetValues():
        Pro.playTurn = 1
        Pro.track.clear()
        Pro.rocks = [[], []]
        Pro.players = [[p0 for p0 in range(13, 25)], [p1 for p1 in range(12)]]
        Pro.disabledRocks.clear()
        Pro.buttons.clear()
    # valX and valY are location x and y (like: 14, 16)
    def getPlayerIndex(valX, valY):
        return indexOf(Pro.allRowCOl,
                        [Pro.getRowColIndex(valX, valY)[0], Pro.getRowColIndex(valX, valY)[1]])

    def getRowColIndex(valX, valY):
        row, col = np.where((Pro.matrix[:, :, 0] == valX) & (Pro.matrix[:, :, 1] == valY))
        return [int(row[0]), int(col[0])]

    # playerIndex = [0 for player1 or 1 for player2, value from 0 to 24]
    # playersCopy is a copy of Pro.players. To use in advaValu function only
    def playerRowCol(playerIndx, playersCopy = []):
        plRowCol = []
        players = Pro.players
        if playersCopy:
            players = playersCopy
        for p in players[playerIndx[0]]:
            if p == -1: continue
            plRowCol.append(Pro.allRowCOl[p])
        return plRowCol
    
    # playerIndex = [0 for player1 or 1 for player2, value from 0 to 24]
    def indxToRowCol(playerIndx):
        return Pro.allRowCOl[playerIndx[1]]
    
    # playerIndex = [0 for player1 or 1 for player2, value from 0 to 24]
    def getLocation(playerIndx):
        loc = Pro.matrix[Pro.allRowCOl[playerIndx[1]][0], Pro.allRowCOl[playerIndx[1]][1]]
        return QPoint(loc[0], loc[1])
    
    # playerIndex = [0 for player1 or 1 for player2, value from 0 to 24]
    # getPlaIndx = index to use in players list and rocks list
    def getPlaIndx(playerIndx):
        return indexOf(Pro.players[playerIndx[0]], playerIndx[1])

    def findNeighbors(rowColIndx, nearOrFar):# near = 1, far = 2
        neighbors = []
        for i in range(2):
            if rowColIndx[i]-nearOrFar >= 0:
                neighbors.append([rowColIndx[i] - nearOrFar, rowColIndx[i-1]][::(i+1)+(i*-3)])
            if rowColIndx[i]+nearOrFar <= 4:
                neighbors.append([rowColIndx[i] + nearOrFar, rowColIndx[i-1]][::(i+1)+(i*-3)])
        return neighbors
    
    # playersCopy is a copy of Pro.players. To use in advaValu function only
    def possibleMove(playerIndx, playersCopy = []):
        locations = []
        rowCol = Pro.playerRowCol(playerIndx, playersCopy)
        oRowCol = Pro.playerRowCol([Pro.playTurn, 0], playersCopy)
        for n in Pro.findNeighbors(Pro.indxToRowCol(playerIndx), 1):
            if n not in rowCol and n not in oRowCol:
                locations.append(n)
        return locations
    
    # playersCopy is a copy of Pro.players. To use in advaValu function only
    def possibleJump(playerIndx, playersCopy = []):
        locations = []
        rowCol = Pro.playerRowCol(playerIndx, playersCopy)
        oRowCol = Pro.playerRowCol([Pro.playTurn, 0], playersCopy)
        for n in Pro.findNeighbors(Pro.indxToRowCol(playerIndx), 1):
            if n not in oRowCol:
                continue
            for f in Pro.findNeighbors(Pro.indxToRowCol(playerIndx), 2):
                if f in rowCol or f in oRowCol:
                    continue
                if (n[1] == f[1] and (n[0]+1 == f[0] or n[0]-1 == f[0])) or (
                    n[0] == f[0] and (n[1]+1 == f[1] or n[1]-1 == f[1])):
                    locations.append([n, f])# Every element in this list contain list of row and column
                    # n: neighbor(other player rock) to jump over . f: empty destination to land
        return locations
    
    def illegalMove(playerIndx):
        return not Pro.possibleMove(playerIndx) and not Pro.possibleJump(playerIndx)
    
    # targeted function is for use inside valuation and advanceVal function only
    # To check if a Computer's rock is targeted by User's rock for jump vice versa
    def targeted(plIndx, playersCopy = []):
        players = Pro.players
        if playersCopy:
            players = playersCopy
        for pl in players[0]:
            jump = Pro.possibleJump([Pro.playTurn, pl], playersCopy)
            if not jump:
                continue
            for j in jump:
                if (j[0][0]*5)+j[0][1] == plIndx:
                    return True
        return False
    
    # advaValu = advanced valuation
    # Check what will happen after possible play in one step or multiple steps
    def advaValu(plIndx, des, isJump):# returns int
        userCopy = copy.deepcopy(Pro.players[0])
        cpuCopy = copy.deepcopy(Pro.players[1])
        value = 0
        # Computer rock index first value
        cpuIndx = plIndx
        
        # Change only the copy of players list
        if isJump:# First jump
            userCopy[userCopy.index((des[0][0]*5)+des[0][1])] = -1
            cpuCopy[cpuCopy.index(cpuIndx)] = (des[1][0]*5)+des[1][1]
            cpuIndx = (des[1][0]*5)+des[1][1]
        else:
            cpuCopy[cpuCopy.index(cpuIndx)] = (des[0]*5)+des[1]
            cpuIndx = (des[0]*5)+des[1]

        if isJump:# second jump
            jump = Pro.possibleJump([1, cpuIndx], [userCopy, cpuCopy])
            if jump:
                value += 5
                if Pro.menuResult[1] == 2:
                    # Change cpuIndx and players copy lists for the Hard mode
                    userCopy[userCopy.index((jump[0][0][0]*5)+jump[0][0][1])] = -1
                    cpuCopy[cpuCopy.index(cpuIndx)] = (jump[0][1][0]*5)+jump[0][1][1]
                    cpuIndx = (jump[0][1][0]*5)+jump[0][1][1]
        # Change Pro.playTurn to 1 like its User turn
        Pro.playTurn = 1
        # Check if Computer rocks is targeted
        for cpu in cpuCopy:
            if Pro.targeted(cpu, [userCopy, cpuCopy]):
                value -= 1
        # Restore Pro.playTurn to original value
        Pro.playTurn = 0

        if Pro.menuResult[1] == 1:
            return value

        thirdJump = False
        if isJump:# third jump
            jump = Pro.possibleJump([1, cpuIndx], [userCopy, cpuCopy])
            if jump:
                value += 5
                thirdJump = True
                # Change cpuIndx and players copy lists for the Hard mode
                userCopy[userCopy.index((jump[0][0][0]*5)+jump[0][0][1])] = -1
                cpuCopy[cpuCopy.index(cpuIndx)] = (jump[0][1][0]*5)+jump[0][1][1]
                cpuIndx = (jump[0][1][0]*5)+jump[0][1][1]

        # Possible move or jump for User player
        for user in userCopy:
            if user == -1:
                continue
            Pro.playTurn = 1
            move = Pro.possibleMove([0, user], [userCopy, cpuCopy])
            jump = Pro.possibleJump([0, user], [userCopy, cpuCopy])
            Pro.playTurn = 0
            if move:
                for m in move:
                    # m = list of int
                    # m[0] = int -row
                    # m[1] = int -column
                    newDes = (m[0]*5)+m[1]
                    userCopy[userCopy.index(user)] = newDes
                    if Pro.targeted(newDes, [userCopy, cpuCopy]):
                        value += 2
                    userCopy[userCopy.index(newDes)] = user
            if jump and thirdJump:
                for j in jump:
                    # j = list of two lists
                    # j[0] = list of int -Computer rock to remove (row, col)
                    # j[1] = list of int -Emty destination to land (row, col)
                    value -= 2
                    newDes = (j[1][0]*5)+j[1][1]
                    rmdRock = (j[0][0]*5)+j[0][1]
                    rmdIndx = cpuCopy.index(rmdRock)
                    userCopy[userCopy.index(user)] = newDes
                    cpuCopy[rmdIndx] = -1
                    if Pro.targeted(newDes, [userCopy, cpuCopy]):
                        value += 2
                    userCopy[userCopy.index(newDes)] = user
                    cpuCopy[rmdIndx] = rmdRock

        return value
    
    # valuation function is for use inside cpuChoice function only
    # To valuate destination (possible move or jump) for Computer player rock
    # plIndx = only the index in Pro.players[1]
    def valuation(plIndx, des, isJump):#returns list of int
        values = []
        if not des:
            return values
        
        for d in des:
            # d: if move = list of 1 row and 1 column
            # d: if jump = list of 2 lists of 1 row and 1 column
            value = 5# In case the valuation (advaValu) drop the value to 0 (minimum must be 0)
            if isJump:
                value += 5
            # Change Pro.playTurn to maked like User player turn (for targeted function to work)
            Pro.playTurn = 1
            if Pro.targeted(plIndx):
                value += 2
            # Restore Pro.playTurn to original value
            Pro.playTurn = 0
            # Valuation for one step a head (normal mode)
            if Pro.menuResult[1] == 1:
                value += Pro.advaValu(plIndx, d, isJump)
            # Valuation for two steps a head (hard mode)
            elif Pro.menuResult[1] == 2:
                value += Pro.advaValu(plIndx, d, isJump)
            values.append(value)
            
        return values

    # dblJmp: double jump (true or false)
    def cpuChoice(dblJmp = False):# Return list: [playerIndex, location: QPoint, isJump]
        # des = destination
        # possDes = possible destination (all possible move and jump distination)

        # roMove = possible moves for one rock (list of integer)
        # moveValue = values for every move (list of interger)

        # roJump = possible jumps for one rock (list of lists of integer)
        # jumpValue = values for every jump (list of interger)

        # len(desMove) == len(Pro.players[1])
        # desMove: [[roMove, moveValue], ..] (list of lists of lists of integer)
        desMove = []# 3D
        # len(desJump) == len(Pro.players[1])
        # desJump: [[roJump, jumpValue], ..] (list of lists of lists of integer and list of integer)
        desJump = []# 4D
        # possDes: [[playerIndex, des, isJump, valuation], ..]
        # (list of lists of: list of integer, QPoint, boolean, integer)
        possDes = []# 2D
        
        for pl in Pro.players[1]:
            # Removed rocks value in the Pro.players = -1
            if pl == -1:
                # Append empty lists to keep index intact
                desMove.append([[], []])
                desJump.append([[], []])
                continue
            # append roMove and moveValue to desMove
            roMove = Pro.possibleMove([1 ,pl])
            desMove.append([roMove, Pro.valuation(pl, roMove, False)])

            # append roJump and jumpValue to desJump
            roJump = Pro.possibleJump([1, pl])
            desJump.append([roJump, Pro.valuation(pl, roJump, True)])

        for i, jump in enumerate(desJump):
            if not jump[0]:
                continue
            for j, jmp in enumerate(jump[0]):
                possDes.append([[1, i], QPoint(
                    Pro.matrix[jmp[1][0], jmp[1][1], 0],
                    Pro.matrix[jmp[1][0], jmp[1][1], 1]), True, jump[1][j]])
            
        for i, move in enumerate(desMove):
            if not move[0]:
                continue
            for j, mv in enumerate(move[0]):
                possDes.append([[1, i], QPoint(
                    Pro.matrix[mv[0], mv[1], 0],
                    Pro.matrix[mv[0], mv[1], 1]), False, move[1][j]])

        if dblJmp:# Double jump
            possDesCopy = copy.deepcopy(possDes)
            for poss in possDesCopy:
                # Remove other rocks and move lists
                if poss[0] != Pro.track[0] or not poss[2]:
                    possDes.remove(poss)
            if possDes:
                choice = random.choice(possDes)
                # Change the rock to jump over in track list in index 1
                Pro.track[1] = [0, 
                                (desJump[
                                    choice[0][1]][0][0][0][0]*5)+desJump[choice[0][1]][0][0][0][1]]
            else:
                choice = []
            return choice
        # Filter possDes list by using index 3 of every list
        # use max value to filter inside for loop
        maxVal = 0# In normal and hard mode make sure that the minimum value is equal to 0
        possDesCopy = copy.deepcopy(possDes)
        for poss in possDes:
            if poss[3] < maxVal:
                continue
            maxVal = poss[3]
        for des in possDesCopy:
            if des[3] < maxVal:
                possDes.remove(des)
        if not possDes:
            return []# Something went wrong!
        choice = random.choice(possDes)
        if choice[2]:# if jump
            if not Pro.track:
                # Nightmare index
                Pro.track = [choice[0],
                             [0, 
                              (desJump[choice[0][1]][0][0][0][0]*5)+desJump[choice[0][1]][0][0][0][1]]]
        else:
            if not Pro.track:
                Pro.track.append(choice[0])
        
        return choice