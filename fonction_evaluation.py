
# LIEN : https://github.com/JRChow/Reversi
# LIEN https://github.com/yuxuan006/Othello/blob/master/yuchai.py
# LIEN: STRATEGIE DE l'HEURISTIQUE  https://www.samsoft.org.uk/reversi/strategy.htm#evaporate
# REFERENCES dans le lien 


import numpy as np  

mat_poids=np.array([[120,-20,20,5,5,20,-20,120],
            [-20,-40,-5,-5,-5,-5,-40,-20],
            [20,-5,15,3,3,15,-5,20],
            [5,-5,3,3,3,3,-5,5],
            [5,-5,3,3,3,3,-5,5],
            [20,-5,15,3,3,15,-5,20],
            [-20,-40,-5,-5,-5,-5,-40,-20],
            [120,-20,20,5,5,20,-20,12]])


######## FOCTION d'EVALUATION TRES BASIQUE #######
def pion_adversaire(pion_joueur):
	""" Given a string representing a pion_joueur (must be either "B" or "W"),
		return the opposing pion_joueur """ 
	if x == "N":
		return "B"
	elif x == "B":
		return "N"
	else:
		return "."

point = 0 
def fonction_eval(mat_poids,couleur_pion_joueur): ### niveau_profondeur

    couleur_pion_adversaire = pion_adversaire(couleur_pion_joueur)
    for x in range(8):
        for y in range(8):
            #calculate the point of current player
            if plateau[x][y] == couleur_pion_joueur:
                point += mat_poids[x][y]
            #calculate the point of the pion_adversaireonent
            elif plateau[x][y] == couleur_pion_adversaire:
                point -= mat_poids[x][y]
    return point


######################################
###### FOCTION d'EVALUATION COMPLEXE  - HEURISTQIEU COMPOSEE 
######################################


''' Heuristique = compile de 3 sous heuristiques '''

''' heuristique 1: Plus le joeur  N a de pièce et moins B en a '''
def diff_pions_point(plateau):
        """Measures the difference in the number of pieces on plateau."""
        return 100 * (sum(x == 'N' for x in plateau.values()) - sum(x == 'B' for x in plateau.values())) / len(plateau)


''' heuristique 2: augmenter sa flexibilité en termes de choix et à contraindre les choix de coups valides de l'adversaire.'''
    def diff_choix_point(self, plateau):
        """Measures the difference in the choice_diff in terms of available choices."""
        black_moves_num = len(self.get_valid_moves(plateau, 'N'))
        white_moves_num = len(self.get_valid_moves(plateau, 'B'))
        if (black_moves_num + white_moves_num) != 0:
            return 100 * (black_moves_num - white_moves_num) / (black_moves_num + white_moves_num)
        else:
            return 0

''' heuristque 3: un coin capruré ne peut être repris par l'adversaire '''
    def diff_coin_point(self, plateau):
        """Measures the difference in the number of corners captured."""
        corner = [plateau.get((1, 1)), plateau.get((1, self.height)), plateau.get((self.width, 1)),
                  plateau.get((self.width, self.height))]
        black_corner = corner.count('N')
        white_corner = corner.count('B')
        if (black_corner + white_corner) != 0:
            return 100 * (black_corner - white_corner) / (black_corner + white_corner)
        else:
            return 0


''' heuristique de stabilité'''

''' HEURISTQIUE FINALE '''
def fonction_eval(self, board, moves, player):
        # Game ends.
        if len(moves) == 0:
            return +100 if player == 'B' else -100
        else:
            return 0.15 * self.coin_diff(board) + \
                   0.15 * self.choice_diff(board) + \
                   0.7 * self.corner_diff(board)




###########################################
########## ALGORITHME D'APPRNETISSAGE 
###########################################

##### PROFONEUR DE RECHERCHE ##############
niv_profondeur = 5 ### entre 3 et 5 
