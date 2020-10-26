#Othello AI v0.1

from bangtal import *
from enum import Enum

setGameOption(GameOption.ROOM_TITLE, False)
setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)

scene = Scene('Othello','images/background.png')

class State(Enum):
    BLANK = 0
    POSSIBLE = 1
    BLACK = 2
    WHITE = 3

class Turn(Enum):
    BLACK = 1
    WHITE = 2
turn = Turn.BLACK

def setState(x, y, s):
    object = board[y][x]
    object.state = s
    if s == State.BLANK:
        object.setImage('images/blank.png')
    elif s == State.BLACK:
        object.setImage('images/black.png')
    elif s == State.WHITE:
        object.setImage('images/white.png')
    else:
        if turn == Turn.BLACK:
            object.setImage('images/black possible.png')
        else:
            object.setImage('images/white possible.png')

def stone_onMouseAction(x, y):
    global turn
    object = board[y][x]
    if turn == Turn.BLACK:
        if object.state == State.POSSIBLE:
            setState(x, y, State.BLACK)
            reverse_xy(x, y)
            turn = Turn.WHITE
            turnCom()
            turn = Turn.BLACK
            setPossible()

def setPossible_xy_dir(x, y, dx, dy):
    if turn == Turn.BLACK:
        mine = State.BLACK
        others = State.WHITE
    else:
        mine = State.WHITE
        others = State.BLACK

    possible = False
    while True:
        x = x+dx
        y = y+dy

        if x<0 or x>7: return False
        elif y<0 or y>7: return False

        object = board[y][x]
        if object.state == others:
            possible = True
        elif object.state == mine:
            return possible
        else: return False

def setPossible_xy(x, y):
    object = board[y][x]
    if object.state == State.BLACK : return False
    if object.state == State.WHITE: return False
    setState(x, y, State.BLANK)

    if setPossible_xy_dir(x, y, 0, 1): return True
    if setPossible_xy_dir(x, y, 1, 1): return True
    if setPossible_xy_dir(x, y, 1, 0): return True
    if setPossible_xy_dir(x, y, 1, -1): return True
    if setPossible_xy_dir(x, y, 0, -1): return True
    if setPossible_xy_dir(x, y, -1, -1): return True
    if setPossible_xy_dir(x, y, -1, 0): return True
    if setPossible_xy_dir(x, y, -1, 1): return True
    return False

def reverse_xy_dir(x, y, dx, dy):
    if turn == Turn.BLACK:
        mine = State.BLACK
        others = State.WHITE
    else:
        mine = State.WHITE
        others = State.BLACK

    possible = False
    while True:
        x = x+dx
        y = y+dy

        if x<0 or x>7: return
        elif y<0 or y>7: return

        object = board[y][x]
        if object.state == others:
            possible = True
        elif object.state == mine:
            if possible:
                while True:
                    x = x-dx
                    y = y-dy

                    object = board[y][x]
                    if object.state == others:
                        setState(x, y, mine)
                    else: return
        else: return

def reverse_xy(x, y):
    reverse_xy_dir(x, y, 0, 1)
    reverse_xy_dir(x, y, 1, 1)
    reverse_xy_dir(x, y, 1, 0)
    reverse_xy_dir(x, y, 1, -1)
    reverse_xy_dir(x, y, 0, -1)
    reverse_xy_dir(x, y, -1, -1)
    reverse_xy_dir(x, y, -1, 0)
    reverse_xy_dir(x, y, -1, 1)
    return False

possibleStone = 0
def setPossible():
    global possibleStone
    possibleStone = 0
    for y in range(8):
        for x in range(8):
            if setPossible_xy(x, y):
                setState(x, y, State.POSSIBLE)
                possibleStone += 1
    checkGame()

def com_xy_dir(x, y, dx, dy):
    mine = State.WHITE
    others = State.BLACK
    possible = False
    cnt=0
    while True:
        x = x+dx
        y = y+dy

        if x<0 or x>7: return 0
        elif y<0 or y>7: return 0

        object = board[y][x]
        if object.state == others:
            possible = True
        elif object.state == mine:
            if possible:
                while True:
                    x = x-dx
                    y = y-dy

                    object = board[y][x]
                    if object.state == others:
                        return cnt
                    else: return 0
        else: return 0

def com_xy(x, y):
    cnt1 = com_xy_dir(x, y, 0, 1)
    cnt2 = com_xy_dir(x, y, 1, 1)
    cnt3 = com_xy_dir(x, y, 1, 0)
    cnt4 = com_xy_dir(x, y, 1, -1)
    cnt5 = com_xy_dir(x, y, 0, -1)
    cnt6 = com_xy_dir(x, y, -1, -1)
    cnt7 = com_xy_dir(x, y, -1, 0)
    cnt8 = com_xy_dir(x, y, -1, 1)
    result = cnt1+cnt2+cnt3+cnt4+cnt5+cnt6+cnt7+cnt8
    return result

def turnCom():
    best = 0
    bestx = besty = 0
    for y in range(8):
        for x in range(8):
            if setPossible_xy(x, y):
                num = com_xy(x, y)
                if best<=num:
                    best = num
                    bestx = x
                    besty = y
    setState(bestx, besty, State.WHITE)
    reverse_xy(bestx, besty)


def scoreChange(black, white):
    black10 = int(black/10)
    black1 = int(black%10)
    white10 = int(white/10)
    white1 = int(white%10)
    
    if black10==0:  blackScore10.setImage('images/L0.png')
    elif black10==1:  blackScore10.setImage('images/L1.png')
    elif black10==2:  blackScore10.setImage('images/L2.png')
    elif black10==3:  blackScore10.setImage('images/L3.png')
    elif black10==4:  blackScore10.setImage('images/L4.png')
    elif black10==5:  blackScore10.setImage('images/L5.png')
    elif black10==6:  blackScore10.setImage('images/L6.png')
    elif black10==7:  blackScore10.setImage('images/L7.png')
    elif black10==8:  blackScore10.setImage('images/L8.png')
    elif black10==9:  blackScore10.setImage('images/L9.png')
    if black1==0:  blackScore1.setImage('images/L0.png')
    elif black1==1:  blackScore1.setImage('images/L1.png')
    elif black1==2:  blackScore1.setImage('images/L2.png')
    elif black1==3:  blackScore1.setImage('images/L3.png')
    elif black1==4:  blackScore1.setImage('images/L4.png')
    elif black1==5:  blackScore1.setImage('images/L5.png')
    elif black1==6:  blackScore1.setImage('images/L6.png')
    elif black1==7:  blackScore1.setImage('images/L7.png')
    elif black1==8:  blackScore1.setImage('images/L8.png')
    elif black1==9:  blackScore1.setImage('images/L9.png')
    
    if white10==0:  whiteScore10.setImage('images/L0.png')
    elif white10==1:  whiteScore10.setImage('images/L1.png')
    elif white10==2:  whiteScore10.setImage('images/L2.png')
    elif white10==3:  whiteScore10.setImage('images/L3.png')
    elif white10==4:  whiteScore10.setImage('images/L4.png')
    elif white10==5:  whiteScore10.setImage('images/L5.png')
    elif white10==6:  whiteScore10.setImage('images/L6.png')
    elif white10==7:  whiteScore10.setImage('images/L7.png')
    elif white10==8:  whiteScore10.setImage('images/L8.png')
    elif white10==9:  whiteScore10.setImage('images/L9.png')
    if white1==0:  whiteScore1.setImage('images/L0.png')
    elif white1==1:  whiteScore1.setImage('images/L1.png')
    elif white1==2:  whiteScore1.setImage('images/L2.png')
    elif white1==3:  whiteScore1.setImage('images/L3.png')
    elif white1==4:  whiteScore1.setImage('images/L4.png')
    elif white1==5:  whiteScore1.setImage('images/L5.png')
    elif white1==6:  whiteScore1.setImage('images/L6.png')
    elif white1==7:  whiteScore1.setImage('images/L7.png')
    elif white1==8:  whiteScore1.setImage('images/L8.png')
    elif white1==9:  whiteScore1.setImage('images/L9.png')

blackScore10 = Object('images/L0.png')
blackScore10.locate(scene, 750, 220)
blackScore10.show()
blackScore1 = Object('images/L2.png')
blackScore1.locate(scene, 830, 220)
blackScore1.show()

whiteScore10 = Object('images/L0.png')
whiteScore10.locate(scene, 1070, 220)
whiteScore10.show()
whiteScore1 = Object('images/L2.png')
whiteScore1.locate(scene, 1150, 220)
whiteScore1.show()

def checkGame():
    global possibleStone
    black = white = 0
    for y in range(8):
        for x in range(8):
            object = board[y][x]
            if object.state == State.BLACK:
                black += 1
            elif object.state == State.WHITE:
                white += 1

    scoreChange(black, white)

    if black == 0:
        showMessage("흰돌 승리!!!")
    elif white == 0:
        showMessage("검은돌 승리!!!")
    elif (black+white==64) or (possibleStone==0):
        if black > white:
            showMessage("검은돌 승리!!!")
        elif black < white:
            showMessage("흰돌 승리!!!")
        else:
            showMessage("무승부!")


board = []
for y in range(8):
    board.append([])
    for x in range(8):
        object = Object('images/blank.png')
        object.locate(scene, 40 + x * 80,40 + y * 80)
        object.show()
        object.onMouseAction = lambda mx, my, action, ix = x, iy = y: stone_onMouseAction(ix, iy)
        object.state = State.BLANK

        board[y].append(object) 

setState(3, 3, State.BLACK)
setState(4, 4, State.BLACK)
setState(4, 3, State.WHITE)
setState(3, 4, State.WHITE)

setPossible()

startGame(scene)