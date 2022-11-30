from board_class import Plateau
from player_class import Joueur
import time
import csv

j1=Joueur("AlphaBeta",1,3) #initialise deux joueurs j1 et j2 respectivement noirs et blancs
j2=Joueur("Aléatoire",2,3)
print("Bienvenue à Othello le jeu trop rigolo (version statistiques avancées)")
nombre_repetitions = 10
description_joueur_1=j1.type_joueur if j1.type_joueur in ["Aléatoire"] else f"{j1.type_joueur}_{j1.profondeur}"
description_joueur_2=j2.type_joueur if j2.type_joueur in ["Aléatoire"] else f"{j2.type_joueur}_{j2.profondeur}"
colonnes=["Partie",description_joueur_1,description_joueur_2,"Vainqueur","Temps d'exécution"]
equivalence_joueur_description={
    1:description_joueur_1,
    2:description_joueur_2
}
lignes=[]
try:
    for k in range(nombre_repetitions):
        plat=Plateau()
        t1=time.time()
        while not plat.fin_de_partie(j1,j2):
            liste_coup_j1=plat.liste_coup_valide(j1)
            if len(liste_coup_j1)>0:
                x1,y1=j1.get_move(plat,j2)
                #print(x1,y1)
                plat.placer_pion(j1,x1,y1)
            else:
                pass
            print(f"{len(plat)} pions sur le plateau")
            liste_coup_j2=plat.liste_coup_valide(j2)
            if len(liste_coup_j2)>0:
                x2,y2=j2.get_move(plat,j1)
                #print(x2,y2)
                plat.placer_pion(j2,x2,y2)
            else:
                pass
            print(f"{len(plat)} pions sur le plateau")
        print("plateau final")
        print(plat)
        scores_finaux=plat.victoire()
        if scores_finaux[0]==scores_finaux[1]:
            print(f"Avec un score final de {scores_finaux[0]} pour le joueur 1 et de {scores_finaux[1]} pour le joueur 2 la partie finit par une égalité")
        else:
            print(f"Avec un score final de {scores_finaux[0]} pour le joueur 1 et de {scores_finaux[1]} pour le joueur 2 le vainqueur est le joueur {scores_finaux[2]}")
        lignes.append([k,scores_finaux[0],scores_finaux[1],"egalité" if scores_finaux[0]==scores_finaux[1] else equivalence_joueur_description[scores_finaux[2]],time.time()-t1])
except:
    pass
with open(f"{description_joueur_1}_vs_{description_joueur_2}_{nombre_repetitions}_repetitions.csv",'w',newline="") as f:
    write =csv.writer(f,delimiter=";")
    write.writerow(colonnes)
    write.writerows(lignes)
print(lignes)