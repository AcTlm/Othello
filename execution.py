from board_class import Plateau
from player_class import Joueur

plat=Plateau()
j1=Joueur("Aléatoire",1) #initialise deux joueurs humains j1 et j2 respectivement noirs et blancs
j2=Joueur("Aléatoire",2,1)
compteur_tour=0
print("Bienvenue à Othello le jeu trop rigolo")
while not plat.fin_de_partie(j1,j2):
    print(f"Tour {compteur_tour}")
    print(f"tour du joueur {j1.type_joueur} aux pions noir")
    print(plat)
    print(f"les coups valables sont : {plat.liste_coup_valide(j1)}")
    x1,y1=j1.get_move(plat)
    plat.placer_pion(j1,x1,y1)
    print(f"tour du joueur {j2.type_joueur} aux pions blancs")
    print(plat)
    print(f"les coups valables sont : {plat.liste_coup_valide(j2)}")
    x2,y2=j2.get_move(plat)
    plat.placer_pion(j2,x2,y2)
    compteur_tour+=1
scores_finaux=plat.victoire()
print(f"Avec un score final de {scores_finaux[0]}pour le joueur 1 et de {scores_finaux}pour le joueur 2 le vainqueur est le joueur {scores_finaux[2]}")
