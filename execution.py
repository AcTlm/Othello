from board_class import Plateau
from player_class import Joueur

plat=Plateau()
j1=Joueur("MCTS",1,5) #initialise deux joueurs j1 et j2 respectivement noirs et blancs
j2=Joueur("Aléatoire",2,3)
compteur_tour=0
print("Bienvenue à Othello le jeu trop rigolo")
while not plat.fin_de_partie(j1,j2):
    print(f"Tour {compteur_tour}")
    print(f"tour du joueur {j1.type_joueur} aux pions noir")
    print(plat)
    liste_coup_j1=plat.liste_coup_valide(j1)
    print(f"les coups valables sont : {liste_coup_j1}")
    if len(liste_coup_j1)>0:
        x1,y1=j1.get_move(plat,j2)
        print(x1,y1)
        plat.placer_pion(j1,x1,y1)
    else:
        print("pas de coup possible, sorryyyyyy babe")
    print(f"tour du joueur {j2.type_joueur} aux pions blancs")
    print(plat)
    liste_coup_j2=plat.liste_coup_valide(j2)
    print(f"les coups valables sont : {liste_coup_j2}")
    if len(liste_coup_j2)>0:
        x2,y2=j2.get_move(plat,j1)
        print(x2,y2)
        plat.placer_pion(j2,x2,y2)
    else:
        print("pas de coup possible, sorryyyyyy babe")
    compteur_tour+=1
print("plateau final")
print(plat)
scores_finaux=plat.victoire()
if scores_finaux[0]==scores_finaux[1]:
    print(f"Avec un score final de {scores_finaux[0]} pour le joueur 1 et de {scores_finaux[1]} pour le joueur 2 la partie finit par une égalité")
else:
    print(f"Avec un score final de {scores_finaux[0]} pour le joueur 1 et de {scores_finaux[1]} pour le joueur 2 le vainqueur est le joueur {scores_finaux[2]}")
