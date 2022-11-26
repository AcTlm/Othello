from board_class import Plateau
from player_class import Joueur
from MCTS_Noeud_class import MCTS_Noeud
import random
import numpy as np
import math
import copy

plat=Plateau()
Joueur_=Joueur("Aléatoire",1)
Autre_Joueur=Joueur("Aléatoire",2)

def uct_score(parent_rollouts, enfant_rollouts, victoire_pct):
# fonction qui calcule score uct pour un noeud: tient compte de la performance associée à ce noeud(% de victoires d'un joueur) et de son facteur d'exploration (ici C est racine de 2)
    if enfant_rollouts==0:
        return 1000
    else:    
        exploration=math.sqrt(math.log(parent_rollouts)/enfant_rollouts)
        # return victoire_pct+(math.sqrt(2))*exploration
        return victoire_pct+(5*exploration)

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
                meilleur_enfant.plat=enfant.plat
        return meilleur_enfant

    def Affiche_Arbre(self, noeud=MCTS_Noeud,profondeur=0):
    #affiche pour un noeud ses statistiques MTCS: nombre de rollouts et pourcentage de victoires de chaque joueur
        print(profondeur*"\t",noeud, "issu du coup:", noeud.coup, "nb de rollouts:", (noeud.nombre_rollouts["roll-out"]), "pct gagnant Joueur_:", noeud.pourcentage_de_victoires(Joueur_)*100, "pct gagnant Autre_Joueur:", noeud.pourcentag_de_victoires(Autre_Joueur)*100)
    

    def Select_un_coup (self, plat, Joueur_, Autre_Joueur):
        """Action de l'agent MCTS à partir d'un noeud racine: application de MCTS et selection par UCB et affiche à la fin des rounds les statistiques pour chaque noeud (racine et les enfants) """

        racine=MCTS_Noeud(plat, parent=MCTS_Noeud, coup=[], Joueur_=Joueur_, Autre_Joueur=Autre_Joueur)
        # plat_first=racine.plat
        noeud=racine
        while (noeud.ajout_enfant_possible()):
            nouveau_noeud=noeud.ajout_enfant_aleatoire()

        nouveau_noeud=self.select_un_enfant(noeud)
        # print("Premier noeud selectionné")
        # print(nouveau_noeud.plat)
        plat_origin=copy.deepcopy(nouveau_noeud.plat)
        victoire_=nouveau_noeud.Simuler_jeu_aleatoire(nouveau_noeud.plat, Joueur_, Autre_Joueur, 2)
        vainqueur=victoire_[2]
        if vainqueur==1:
            Vainqueur="Joueur_"
        elif vainqueur==2:
            Vainqueur="Autre_Joueur"
        while nouveau_noeud!=racine:
            nouveau_noeud=nouveau_noeud.enregistre_victoire(vainqueur=Vainqueur)
            nouveau_noeud.plat=plat_origin
            nouveau_noeud=nouveau_noeud.parent
        if nouveau_noeud==racine:
            nouveau_noeud=nouveau_noeud.enregistre_victoire(vainqueur=Vainqueur)
        i=1
        # self.Affiche_Arbre(noeud=racine)
        # for e in (racine.enfants):
        #     self.Affiche_Arbre(noeud=e)
        
        for i in range(1, self.nombre_rounds): 
            noeud=racine
            k=1
            while (noeud.ajout_enfant_possible()==False):
                nouveau_noeud=self.select_un_enfant(noeud)
                noeud=nouveau_noeud
                k+=1
                # print("noeud associé à k=", k,"\n") 
                # print(noeud.plat)
               
            if (noeud.ajout_enfant_possible()):
                if noeud.nombre_rollouts==0:
                    nouveau_noeud=noeud
                    plat_origin=copy.deepcopy(nouveau_noeud.plat)
                    victoire_=nouveau_noeud.Simuler_jeu_aleatoire(nouveau_noeud.plat, Joueur_, Autre_Joueur, (2-k%2))
                    vainqueur=victoire_[2]
                    if vainqueur==1:
                        Vainqueur="Joueur_"
                    elif vainqueur==2:
                        Vainqueur="Autre_Joueur"
                    while nouveau_noeud!=racine:
                        nouveau_noeud=nouveau_noeud.enregistre_victoire(vainqueur=Vainqueur)
                        nouveau_noeud.plat=plat_origin
                        nouveau_noeud=nouveau_noeud.parent
                    if nouveau_noeud==racine:
                        nouveau_noeud=nouveau_noeud.enregistre_victoire(vainqueur=Vainqueur)
                    i+=1
                    # self.Affiche_Arbre(noeud=racine)
                    # for e in (racine.enfants):
                    #     print("enfant")
                    #     self.Affiche_Arbre(noeud=e)
                    #     for f in e.enfants:
                    #         print("petit enfant")
                    #         self.Affiche_Arbre(noeud=f)
                    #         for g in f.enfants:
                    #             print("arriere petit enfant")
                    #             self.Affiche_Arbre(noeud=g)

                else:
                    while noeud.ajout_enfant_possible():
                        nouveau_noeud=noeud.ajout_enfant_aleatoire()
                    nouveau_noeud=self.select_un_enfant(nouveau_noeud)
                    plat_origin=copy.deepcopy(nouveau_noeud.plat)
                    victoire_=nouveau_noeud.Simuler_jeu_aleatoire(nouveau_noeud.plat, Joueur_, Autre_Joueur, 2-k%2)
                    vainqueur=victoire_[2]
                    if vainqueur==1:
                        Vainqueur="Joueur_"
                    elif vainqueur==2:
                        Vainqueur="Autre_Joueur"
                    while nouveau_noeud!=racine:
                        nouveau_noeud=nouveau_noeud.enregistre_victoire(vainqueur=Vainqueur)
                        nouveau_noeud.plat=plat_origin
                        nouveau_noeud=nouveau_noeud.parent
                    if nouveau_noeud==racine:
                        nouveau_noeud=nouveau_noeud.enregistre_victoire(vainqueur=Vainqueur)
                    i+=1
                    # self.Affiche_Arbre(noeud=racine)
                    # for e in (racine.enfants):
                    #     print("enfant")
                    #     self.Affiche_Arbre(noeud=e)
                    #     for f in e.enfants:
                    #         print("petit enfant")
                    #         self.Affiche_Arbre(noeud=f)
                    #         for g in f.enfants:
                    #             print("arriere-petit enfant")
                    #             self.Affiche_Arbre(noeud=g)
        print("*****\n\nresultat final:")
        self.Affiche_Arbre(noeud=racine)
        print("Racine:")
        for e in (racine.enfants):
            print("\tenfant")
            self.Affiche_Arbre(noeud=e)
            # for f in e.enfants:
            #     print("\t\tpetit-enfant")
            #     self.Affiche_Arbre(noeud=f,profondeur=1)
            #     for g in f.enfants:
            #         print("\t\t\tarriere-petit enfant")
            #         self.Affiche_Arbre(noeud=g,profondeur=2)

    
        

            
    
    
                