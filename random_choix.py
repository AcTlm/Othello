from board_class import Plateau
from player_class import Joueur
board=Plateau()
j1=Joueur("Humain",1) #initialise deux joueurs humains j1 et j2 respectivement noirs et blancs
j2=Joueur("bot",2)

def prochain_coup_random (board, pion_joueur):
    """ Retour un coup valide aléatoire à jouer pour le j2 (bot)"""
    mouvements = []
    for i in range(8):
    	for j in range(8):
        	if board.est_mouvement_valide(board,i,j):
			         mouvements.append((i,j))
    if len(mouvements) == 0:
	   	return "pass"
    meilleur_coup = mouvements[random.randint(0,len(mouvements) - 1)]
    return meilleur_coup