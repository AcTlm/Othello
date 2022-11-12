
# LIEN : https://github.com/JRChow/Reversi
# LIEN https://github.com/yuxuan006/Othello/blob/master/yuchai.py
# LIEN: STRATEGIE DE l'HEURISTIQUE  https://www.samsoft.org.uk/reversi/strategy.htm#evaporate
# REFERENCES dans le lien 


######################################
###### FOCTION d'EVALUATION COMPLEXE 
######################################

### H1 = Plus le joeur  N a de pièces et moins B en a *
def diff_pions_point(plateau,couleur_pion_joueur) : 
    couleur_pion_adversaire = pion_adversaire(couleur_pion_joueur)
    return  100 * sum(np.where(plateau==couleur_pion_joueur)) - sum(np.where(plateau == couleur_pion_adversaire))


### H2 : Measures the difference in the choice_diff in terms of available choices
def contraindre_choix_adversaire(plateau):
    nb_mouvements_noirs = len(liste_coup_valide(plateau,'N'))
    nb_mouvements_blancs = len(liste_coup_valide(plateau,'B'))
    if (nb_mouvements_noirs + nb_mouvements_blancs) != 0 
        return 100 * (nb_mouvements_noirs - nb_mouvements_blancs) / (nb_mouvements_noirs + nb_mouvements_blancs)
    else : 
        return 0 

### H3:  ## Measures the difference in the number of corners captured."""
def diff_point_coin(plateau) #### OK 
    coin_noir = 0
    coin_blanc = 0

    for x in plateau[1,1]:
        if x == 'N':
            coin_noir +=1
        elif x == 'B'
            coin_blanc += 1
        else : 
            print("nope")
     
    for x in plateau[1,8]:
        if x == 'N':
            coin_noir +=1
        elif x == 'B'
            coin_blanc += 1
        else : 
            print("nope")
    
    for x in plateau[8,1]:
        if x == 'N':
            coin_noir +=1
        elif x == 'B'
            coin_blanc += 1
        else : 
            print("nope")

    for x in plateau[8,8]:
        if x == 'N':
            coin_noir +=1
        elif x == 'B'
            coin_blanc += 1
        else : 
            print("nope")
    
    if (coin_noir + coin_blanc) != 0:
            return 100 * (coin_noir - coin_blanc) / (coin_noir + coin_blanc)
        else:
            return 0

#### HEURISTIQUE FINALE 
def fonction_eval(self, plateau, coup, couleur_pion_joueur):
        # Game ends.
        if len(coup) == 0:
            return +100 if couleur_pion_joueur == 'B' else -100
        else:
            return 0.15 * self.diff_pions_point(plateau,couleur_pion_joueur) + \
                   0.15 * self.contraindre_choix_adversaire(plateau) + \
                   0.7 * self.diff_point_coin(plateau)


'''
def diff_pions_point(plateau,couleur_pion_joueur)  ### OK 
### Measures the difference in the number of pieces on plateau
        #return 100 * (sum(x == 'N' for x in plateau.values()) - sum(x == 'B' for x in plateau.values())) / len(plateau)
        couleur_pion_adversaire = pion_adversaire(couleur_pion_joueur)
        return  100 * sum(np.where(plateau==couleur_pion_joueur)) - sum(np.where(plateau == couleur_pion_adversaire))

heuristique 2: augmenter sa flexibilité en termes de choix et à contraindre les choix de coups valides de l'adversaire.
def diff_choix_point(self, plateau): ### Measures the difference in the choice_diff in terms of available choices."""
        black_moves_num = len(self.get_valid_moves(plateau, 'N'))
        white_moves_num = len(self.get_valid_moves(plateau, 'B'))
        if (black_moves_num + white_moves_num) != 0:
            return 100 * (black_moves_num - white_moves_num) / (black_moves_num + white_moves_num)
        else:
            return 0


def contraindre_choix_adversaire (plateau):
    nb_mouvements_noirs = len(liste_coup_valide(plateau,'N'))
    nb_mouvements_blancs = len(liste_coup_valide(plateau,'B'))
    if (nb_mouvements_noirs + nb_mouvements_blancs) != 0 
        return 100 * (nb_mouvements_noirs - nb_mouvements_blancs) / (nb_mouvements_noirs + nb_mouvements_blancs)
    else : 
        return 0 


heuristque 3: un coin capruré ne peut être repris par l'adversaire
    def diff_coin_point(self, plateau): ### Measures the difference in the number of corners captured."""
        corner = [plateau.get((1, 1)), plateau.get((1, self.height)), plateau.get((self.width, 1)),
                  plateau.get((self.width, self.height))]
        black_corner = corner.count('N')
        white_corner = corner.count('B')
        if (black_corner + white_corner) != 0:
            return 100 * (black_corner - white_corner) / (black_corner + white_corner)
        else:
            return 0

def diff_point_coin(plateau) #### OK 
    coin_noir = 0
    coin_blanc = 0

    for x in plateau[1,1]:
        if x == 'N':
            coin_noir +=1
        elif x == 'B'
            coin_blanc += 1
        else : 
            print("nope")
     
    for x in plateau[1,8]:
        if x == 'N':
            coin_noir +=1
        elif x == 'B'
            coin_blanc += 1
        else : 
            print("nope")
    
    for x in plateau[8,1]:
        if x == 'N':
            coin_noir +=1
        elif x == 'B'
            coin_blanc += 1
        else : 
            print("nope")

    for x in plateau[8,8]:
        if x == 'N':
            coin_noir +=1
        elif x == 'B'
            coin_blanc += 1
        else : 
            print("nope")
    
    if (coin_noir + coin_blanc) != 0:
            return 100 * (coin_noir - coin_blanc) / (coin_noir + coin_blanc)
        else:
            return 0

heuristique de stabilité

HEURISTQIUE FINALE
def fonction_eval(self, board, moves, player):
        # Game ends.
        if len(moves) == 0:
            return +100 if player == 'B' else -100
        else:
            return 0.15 * self.coin_diff(board) + \
                   0.15 * self.choice_diff(board) + \
                   0.7 * self.corner_diff(board)

''' 
