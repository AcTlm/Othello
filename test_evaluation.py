import timeit
import numpy as np  

mat_poids=np.array([[120,-20,20,5,5,20,-20,120],
            [-20,-40,-5,-5,-5,-5,-40,-20],
            [20,-5,15,3,3,15,-5,20],
            [5,-5,3,3,3,3,-5,5],
            [5,-5,3,3,3,3,-5,5],
            [20,-5,15,3,3,15,-5,20],
            [-20,-40,-5,-5,-5,-5,-40,-20],
            [120,-20,20,5,5,20,-20,120]])
plateau=np.array([["N","N","N","B","B","B","B","B"],
            ["B","B","B","N","N","N","B","B"],
            ["B","N","B","N","N","N","B","B"],
            ["B","N","N","N","N","N","B","B"],
            ["B","B","B","N","N","N","N","B"],
            ["B","B","B","N","N","N","B","B"],
            ["B","B","B","N","N","B","B","B"],
            ["B","B","N","N","N","B","B","N"]])

######## FOCTION d'EVALUATION TRES BASIQUE #######
def pion_adversaire(pion_joueur):
    """ Given a string representing a pion_joueur (must be either "B" or "W"),
        return the opposing pion_joueur """ 
    if pion_joueur == "N":
        return "B"
    elif pion_joueur == "B":
        return "N"
    else:
        return "."

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

def fonction_eval_numpy(plateau,mat_poids,couleur_pion_joueur):
    couleur_pion_adversaire = pion_adversaire(couleur_pion_joueur)
    point=np.sum(np.where(plateau==couleur_pion_joueur,mat_poids,0))
    point-=np.sum(np.where(plateau==couleur_pion_adversaire,mat_poids,0))
    return point


print(timeit.timeit(stmt='fonction_eval(plateau,mat_poids,"N")',setup='from __main__ import fonction_eval',number=5000,globals=globals()))
print(timeit.timeit(stmt='fonction_eval_numpy(plateau,mat_poids,"N")',setup='from __main__ import fonction_eval',number=5000,globals=globals()))