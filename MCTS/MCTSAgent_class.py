from board_class import Plateau
from player_class import Joueur
from MCTS_Noeud_class import MCTS_Noeud
import random
import numpy as np

plat=Plateau()
print(plat)
Joueur_=Joueur("Aléatoire",1)
Autre_Joueur=Joueur("Aléatoire",2)

class MCTSAgent:

    def __init__(self, nombre_rounds):
        self.nombre_rounds=nombre_rounds

    def Select_un_coup (self, plat, Joueur_, Autre_Joueur):
        print(plat)
        racine=MCTS_Noeud(plat, parent=None, coup=[], Joueur_=Joueur_, Autre_Joueur=Autre_Joueur)
        print('racine ok')
        i=0
        for i in range(self.nombre_rounds):
            print(i)
            noeud=racine
            print(noeud.coups_non_visites)
            print(noeud.ajout_enfant_possible())
            #xxxwhile ((not ajout_enfant_possible()) and (not Est_un_noeud_terminal())):
            if noeud.ajout_enfant_possible():
                print('possible')
                noeud.ajout_enfant_aleatoire(Joueur_, Autre_Joueur)
                victoire_=noeud.Simuler_jeu_aleatoire(plat, Joueur_, Autre_Joueur, 2)
                vainqueur=victoire_[2]
                if vainqueur==1:
                    vainqueur=Joueur_
                elif vainqueur==2:
                    vainqueur=Autre_Joueur
                while noeud!=None:
                    print("on n'est pas à la racine")
                    noeud.enregistre_victoire(vainqueur)
                    print('%d', (noeud.nombre_victoires["Joueur_"]))
                    print('%d', (noeud.nombre_victoires["Autre_Joueur"]))
                    noeud=noeud.parent
                i+=1
            else:
                print("problem")
        for e in (racine.enfants):
            print ('%d', (e.nombre_rollouts["roll-out"]))
                