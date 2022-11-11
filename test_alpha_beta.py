from board_class import Plateau
from player_class import Joueur,alpha_beta
from copy import deepcopy
plat=Plateau()
j1=Joueur("Humain",1) #initialise deux joueurs j1 et j2 respectivement noirs et blancs
j2=Joueur("AlphaBeta",2,1)
liste_coup_j2=plat.liste_coup_valide(j2)
a=alpha_beta(plat,1,j1,j2, -10000 , +10000)
print(a)
