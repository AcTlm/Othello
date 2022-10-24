''' OTHELLO IA_SOLVE '''

import turtle as t
from random import randint
import math
import os
import time

### CREATION DU BOARD 
n = 8 # taille board 
board = [['0' for x in range(n)] for y in range(n)]
print(board)

#### Initialisation du board 
#initialiseBoard(n) returns the initial board for an Othello game of size n where 2 Blaxk and two white are centered 
def initialiseBoard(n):
    board = [[0 for i in range(n)] for j in range(n)]
    pos = int(n/2)
    board[pos-1][pos-1] = 1
    board[pos-1][pos] = -1
    board[pos][pos-1] = -1
    board[pos][pos] = 1
    return board


### couleur des pions 
BLACK = '\u26AB'
WHITE = '\u26AA'
EMPTY = '\u2B1c'

### Position d'un nouveau pion 
new_pos_pion = ((0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1))
print(new_pos_pion)

def move(b, m, p):
    r = m[0]
    c = m[1]
    if (len(m[2]) == 0):
        return
    else:
        for move in m[2]:
            newR = r + move[0]
            newC = c + move[1]
            while (b[newR][newC] != abs(b[newR][newC])*p):
                b[newR][newC] = (abs(b[newR][newC]) + 1) * p
                newR = newR + move[0]
                newC = newC + move[1]
        b[r][c] = p
        placePiece() ### fonction placement de pion
        ### update screen 


def placePiece():
