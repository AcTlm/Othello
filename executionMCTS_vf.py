from board_class import Plateau
from player_class import Joueur
from MCTS_Noeud_class import MCTS_Noeud
from MCTSAgent_class import MCTSAgent 
import random
import numpy as np
import time


plat=Plateau()
j1=Joueur("Aléatoire", 1) #initialise deux joueurs aléatoires j1 et j2 respectivement noirs et blancs
j2=Joueur("Aléatoire", 2)
print("Bienvenue à Othello: partie MCTS et UCB")
print("le noeud racine (plateau) sur lequel on lance MCTS est le suivant:")
print(plat)
# start = time.time()
MCTS_A=MCTSAgent(10)
#créé un agent qui va lance le nombre indiqué de rollouts de MCTS 
MCTS_A.Select_un_coup(plat=plat, Joueur_=j1, Autre_Joueur=j2)
#lance les rollouts de MCTS en prenant comme racine le plateau initial
# print(time.time()-start)

