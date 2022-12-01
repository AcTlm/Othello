from board_class import Plateau
import board_class
from player_class import Joueur
import random
import numpy as np
import copy

plat=Plateau()
# print(plat)
Joueur_=Joueur("Aléatoire",1)
Autre_Joueur=Joueur("Aléatoire",2)


class MCTS_Noeud:
    
    def __init__(self, plat:Plateau, parent=None, coup=[], Joueur_=Joueur_, Autre_Joueur=Autre_Joueur):
    # Initialisation de la classe noeud pour MCTS, avec un plateau, un parent, une liste d'enfants, une liste de coups possibles à partir du plateau
        self.plat=plat
        self.parent=parent
        self.coup=coup
        self.nombre_victoires = {"Joueur_":0,"Autre_Joueur":0}
        self.nombre_rollouts = {"roll-out":0}
        self.enfants=[]
        self.coups_non_visites=plat.liste_coup_valide(Joueur_)
        self.Joueur_=Joueur_
        self.Autre_Joueur=Autre_Joueur

    def ajout_enfant_aleatoire(self):
    # Creer un enfant aleatoire à partir d'un noeud en faisant l'un des coups possibles pour le "Joueur_" depuis ce noeud 
        index=random.randint(0, len(self.coups_non_visites)-1)
        nouveau_coup=self.coups_non_visites.pop(index)
        nouveau_coup=list(nouveau_coup)
        # print(nouveau_coup)
        origin=copy.deepcopy(self.plat)
        self.plat.placer_pion(self.Joueur_, nouveau_coup[0], nouveau_coup[1])
        # print("voici le plateau noeud fils aleatoire")
        # print(self.plat)
        nouveau_noeud=MCTS_Noeud(self.plat, self, nouveau_coup, self.Autre_Joueur, self.Joueur_)
        nouveau_noeud.parent=self
        self.plat=origin
        self.enfants.append(nouveau_noeud)
        return nouveau_noeud

    def enregistre_victoire(self, vainqueur):
    # actualise dans un noeud le nombre de victoires de chaque joueur et le nombre de rollout de MCTS effectués 
        i=self.nombre_victoires["Joueur_"]
        j=self.nombre_victoires["Autre_Joueur"]
        if vainqueur=='Joueur_':
            self.nombre_victoires={"Joueur_":i+1, "Autre_Joueur":j}
        elif vainqueur=='Autre_Joueur':
            self.nombre_victoires={"Joueur_":i, "Autre_Joueur":j+1}
        k=self.nombre_rollouts["roll-out"]
        self.nombre_rollouts={"roll-out": k+1}
        return self

    def ajout_enfant_possible(self):
    # retourne s'il est possible de créer un enfant à partir d'un noeud (s'il reste des coups non visités)
        self.coups_non_visites=list(self.coups_non_visites)
        if self.coups_non_visites==[] :
            return False
        else:
            return True


    def Est_un_noeud_terminal (self, Joueur_):
    #retourne si un noeud est terminal pour un joueur, i.e. que le joueur n'a aucun coup valide possible
        if plat.liste_coup_valide(Joueur_)==[]:
            return True
        else:
            return False

    def pourcentage_de_victoires (self, Joueur_):
    #calcule le pourcentage de victoires d'un joueur sur l'ensemble des roll-outs effectués
        if self.nombre_rollouts["roll-out"]==0:
            return 0
        else:
            return float(self.nombre_victoires["Joueur_"])/float(self.nombre_rollouts["roll-out"])

    def pourcentag_de_victoires (self, Autre_Joueur):
        if self.nombre_rollouts["roll-out"]==0:
            return 0         
        else:
            return float(self.nombre_victoires["Autre_Joueur"])/float(self.nombre_rollouts["roll-out"])


    def Simuler_jeu_aleatoire (self, plat, Joueur_, Autre_Joueur, tour):
    #simule une partie aléatoire entre les 2 joueurs depuis un noeud jusqu'à la fin de la partie: correspond à un roll-out MCTS
        plat_origin=copy.deepcopy(self.plat)
        #print(plat_origin)
        while plat.fin_de_partie(Joueur_, Autre_Joueur)==False:
            if tour==2:
                L=plat.liste_coup_valide(Autre_Joueur)
                if (L==[] and plat.liste_coup_valide(Joueur_)==[]):
                    victoire_=self.plat.victoire()
                    return victoire_
                elif L==[]:
                    # print("2 ne peut jouer, passe à 1")
                    tour=1
                else:
                    index=random.randint(0, len(L)-1)
                    nouveau_coup=L.pop(index)
                    nouveau_coup=list(nouveau_coup)
                    # print(nouveau_coup, "coups pour 2")
                    self.plat.placer_pion(Autre_Joueur, nouveau_coup[0], nouveau_coup[1])
                    # print("tour passe à 1")
                    tour=1
                if plat.fin_de_partie(Joueur_, Autre_Joueur)==True:
                        victoire_=self.plat.victoire()
                        return victoire_
            elif tour==1:
                L=plat.liste_coup_valide(Joueur_)
                if (L==[] and (plat.liste_coup_valide(Autre_Joueur)==[])):
                    victoire_=self.plat.victoire()
                    return victoire_
                elif L==[]:
                    # print("1 ne peut jouer, passe à 2")
                    tour=2
                else:
                    index=random.randint(0, len(L)-1)
                    nouveau_coup=L.pop(index)
                    nouveau_coup=list(nouveau_coup)
                    # print(nouveau_coup, "coups pour 1")
                    self.plat.placer_pion(Joueur_, nouveau_coup[0], nouveau_coup[1])
                    tour=2
                    # print("tour passe à 2")     
                if plat.fin_de_partie(Joueur_, Autre_Joueur)==True:
                        victoire_=self.plat.victoire()
                        return victoire_
        self.plat=plat_origin
        if plat.fin_de_partie(Joueur_, Autre_Joueur)==True:
                victoire_=self.plat.victoire()
                # print(victoire_)
                return victoire_
        self.plat=plat_origin

    

    






