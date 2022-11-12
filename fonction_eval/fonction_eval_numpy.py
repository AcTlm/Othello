import numpy as np  

mat_poids=np.array([[120,-20,20,5,5,20,-20,120],
            [-20,-40,-5,-5,-5,-5,-40,-20],
            [20,-5,15,3,3,15,-5,20],
            [5,-5,3,3,3,3,-5,5],
            [5,-5,3,3,3,3,-5,5],
            [20,-5,15,3,3,15,-5,20],
            [-20,-40,-5,-5,-5,-5,-40,-20],
            [120,-20,20,5,5,20,-20,120]])


######## FONCTION d'EVALUATION TRES BASIQUE #######
point = 0 
def fonction_eval(plateau,mat_poids,couleur_pion_joueur): ### niveau_profondeur
    couleur_pion_adversaire = pion_adversaire(couleur_pion_joueur)
    point=0
    for x in range(8):
        for y in range(8):
            #calculate the point of current player
            if plateau[x][y] == couleur_pion_joueur:
                point += mat_poids[x][y]
            #calculate the point of the pion_adversaire
            elif plateau[x][y] == couleur_pion_adversaire:
                point -= mat_poids[x][y]
    return point

def fonction_eval_numpy(plateau,mat_poids,couleur_pion_joueur): #3 fois plus rapide que celle ci-desssus
    couleur_pion_adversaire = pion_adversaire(couleur_pion_joueur)
    point=np.sum(np.where(plateau==couleur_pion_joueur,mat_poids,0))
    point-=np.sum(np.where(plateau==couleur_pion_adversaire,mat_poids,0))
    return point
