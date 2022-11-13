from board_class import Plateau
from player_class import Joueur
from MCTS_Noeud_class import MCTS_Noeud
import random
import numpy as np
import math
import copy

plat=Plateau()
# print(plat)
Joueur_=Joueur("Aléatoire",1)
Autre_Joueur=Joueur("Aléatoire",2)

def uct_score(parent_rollouts, enfant_rollouts, victoire_pct):
# fonction qui calcule score uct pour un noeud: tient compte de la performance associée à ce noeud(% de victoires d'un joueur) et de son facteur d'exploration (ici C est racine de 2)
    exploration=math.sqrt(math.log(parent_rollouts)/enfant_rollouts)
    return victoire_pct+(math.sqrt(2))*exploration

class MCTSAgent:
#creation de la classe Agent MCTS qui va appliquer MCTS et UCB sur un nombre défini de rounds 
    def __init__(self, nombre_rounds):
        self.nombre_rounds=nombre_rounds

    def select_un_enfant (self, noeud=MCTS_Noeud):
    #selection du meilleur enfant pour lequel on lancera un roll-out, selection basée sur son score UCB 
        total_rollouts=sum(enfant.nombre_rollouts["roll-out"] for enfant in noeud.enfants)
        meilleur_score=-1
        meilleur_enfant=noeud
        for enfant in noeud.enfants:
            score=uct_score(total_rollouts, enfant.nombre_rollouts["roll-out"], enfant.pourcentage_de_victoires(Joueur_))
            if score>meilleur_score:
                meilleur_score=score
                meilleur_enfant=enfant
        # print(meilleur_enfant, meilleur_score)
        return meilleur_enfant

    def Affiche_Arbre(self, noeud=MCTS_Noeud):
    #affiche pour un noeud ses statistiques MTCS: nombre de rollouts et pourcentage de victoires de chaque joueur
        print(noeud, "issu du coup:", noeud.coup, "nombre de rollouts:", (noeud.nombre_rollouts["roll-out"]), "Pourcentage gagnant pour Joueur_:", noeud.pourcentage_de_victoires(Joueur_)*100, "Pourcentage gagnant pour Autre_Joueur:", noeud.pourcentag_de_victoires(Autre_Joueur)*100)
    

    def Select_un_coup (self, plat, Joueur_, Autre_Joueur):
    #Action de l'agent MCTS à partir d'un noeud racine: tant qu'il est possible de créer un noeud enfant 
    #il crée un noeud enfanrt à partir de la racine, et lorsque ce n'est plus possible, il sélectionne le meilleur noeud existant par UCV
    #et lance à partir de ce noeud(enfant créé ou sélectionné) le rollout MCTS jusqu'à la fin de la partie
    #affiche à la fin des rounds les statistiques pour chaque noeud (racine et les enfants)
        # print(plat)
        racine=MCTS_Noeud(plat, parent=MCTS_Noeud, coup=[], Joueur_=Joueur_, Autre_Joueur=Autre_Joueur)
        # print('racine ok')
        i=0
        for i in range(self.nombre_rounds):
            # print(i)
            noeud=racine
            # print("le noeud racine est:", noeud)
            noeud.plat=Plateau()
            # print(noeud.plat)
            # print(noeud.coups_non_visites)
            # print(noeud.ajout_enfant_possible())
            if ((noeud.ajout_enfant_possible()==False) and (noeud.Est_un_noeud_terminal(Joueur_)==False)):
                nouveau_noeud=self.select_un_enfant(noeud)
                print("selectionne le meilleur enfant existant qui est:", nouveau_noeud)
                # print(nouveau_noeud.plat)
            elif noeud.ajout_enfant_possible():
                print('A cette étape, créer un noeud enfant est possible')
                nouveau_noeud=noeud.ajout_enfant_aleatoire(Joueur_, Autre_Joueur)
                print("le noeud créé est:", nouveau_noeud)
                # print("voici le plateau pour lancer le roll-out MCTS")
                # print(nouveau_noeud.plat)
            plat_origin=copy.deepcopy(nouveau_noeud.plat)
            victoire_=nouveau_noeud.Simuler_jeu_aleatoire(nouveau_noeud.plat, Joueur_, Autre_Joueur, 2)
            vainqueur=victoire_[2]
            if vainqueur==1:
                Vainqueur="Joueur_"
            elif vainqueur==2:
                Vainqueur="Autre_Joueur"
            # print(Vainqueur)
            while nouveau_noeud!=racine:
                # print("on n'est pas à la racine")
                nouveau_noeud=nouveau_noeud.enregistre_victoire(vainqueur=Vainqueur)
                #print("nombre de victoires du 1er joueur:", (nouveau_noeud.nombre_victoires["Joueur_"]))
                # print("nombre de victoires du 2e joueur:", (nouveau_noeud.nombre_victoires["Autre_Joueur"]))
                # print("nombre de rollouts:", nouveau_noeud.nombre_rollouts["roll-out"])
                nouveau_noeud.plat=plat_origin
                nouveau_noeud=nouveau_noeud.parent
            if nouveau_noeud==racine:
                # print("on est à la racine")
                nouveau_noeud=nouveau_noeud.enregistre_victoire(vainqueur=Vainqueur)
                # print("nombre de victoires du 1er joueur:", (nouveau_noeud.nombre_victoires["Joueur_"]))
                # print("nombre de victoires du 2e joueur:", (nouveau_noeud.nombre_victoires["Autre_Joueur"]))
                # print("nombre de rollouts:", nouveau_noeud.nombre_rollouts["roll-out"])
            i+=1
            print(i, "eme round fini")
        print("********Résultats des rollouts pour la racine:")
        self.Affiche_Arbre(noeud=racine)
        print("********Résultats des rollouts pour les noeuds enfants de la racine:")
        for e in (racine.enfants):
            self.Affiche_Arbre(noeud=e)
        

            
    
    
                