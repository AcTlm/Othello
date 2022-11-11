from board_class import Plateau
import board_class
from player_class import Joueur
import random
import numpy as np

plat=Plateau()
print(plat)
Joueur_=Joueur("Aléatoire",1)
Autre_Joueur=Joueur("Aléatoire",2)


class MCTS_Noeud:
    
    def __init__(self, plat=plat, parent=None, coup=[], Joueur_=Joueur_, Autre_Joueur=Autre_Joueur):
        self.plat=plat
        self.parent=parent
        self.coup=coup
        self.nombre_victoires = {"Joueur_":0,"Autre_Joueur":0}
        self.nombre_rollouts = {"roll-out":0}
        self.enfants=[]
        self.coups_non_visites=plat.liste_coup_valide(Joueur_)

    def ajout_enfant_aleatoire(self, Joueur_, Autre_Joueur):
        index=random.randint(0, len(self.coups_non_visites)-1)
        nouveau_coup=self.coups_non_visites.pop(index)
        nouveau_coup=list(nouveau_coup)
        print(nouveau_coup)
        self.plat.placer_pion(Joueur_, nouveau_coup[0], nouveau_coup[1])
        print(plat)
        nouveau_noeud=MCTS_Noeud(plat, self, nouveau_coup, Joueur_, Autre_Joueur)
        self.enfants.append(nouveau_noeud)
        return nouveau_noeud

    def enregistre_victoire(self, vainqueur):
        i=self.nombre_victoires["Joueur_"]
        j=self.nombre_victoires["Autre_Joueur"]
        if vainqueur==Joueur_:
            self.nombre_victoires["Joueur_"]=i+1
        elif vainqueur==Autre_Joueur:
            self.nombre_victoires["Joueur_"]=j+1
        k=self.nombre_rollouts["roll-out"]
        self.nombre_rollouts["roll-out"]=k+1

    def ajout_enfant_possible(self):
        self.coups_non_visites=list(self.coups_non_visites)
        if self.coups_non_visites==[] :
            return False
        else:
            return True


    def Est_un_noeud_terminal (self, Joueur_):
        if plat.liste_coup_valide(Joueur_)==[]:
            return True
        else:
            return False

    #XXXX def_pourcentage_de_victoires (self, Joueur_)
        #XXXXreturn XXXX


    def Simuler_jeu_aleatoire (self, plat, Joueur_, Autre_Joueur, tour):
        while plat.fin_de_partie(Joueur_, Autre_Joueur)==False:
            if tour==2:
                L=plat.liste_coup_valide(Autre_Joueur)
                print(L)
                if (L==[] and plat.liste_coup_valide(Joueur_)==[]):
                    victoire_=self.plat.victoire()
                    print(victoire_)
                    return victoire_
                elif L==[]:
                    print("1 ne peut jouer, passe à 2")
                    tour=2
                else:
                    index=random.randint(0, len(L)-1)
                    nouveau_coup=L.pop(index)
                    nouveau_coup=list(nouveau_coup)
                    print(nouveau_coup, "coups pour 2")
                    self.plat.placer_pion(Autre_Joueur, nouveau_coup[0], nouveau_coup[1])
                    print("tour passe à 1")
                    tour=1
                if plat.fin_de_partie(Joueur_, Autre_Joueur)==True:
                        victoire_=self.plat.victoire()
                        print(victoire_)
                        return victoire_
            elif tour==1:
                L=plat.liste_coup_valide(Joueur_)
                if (L==[] and (plat.liste_coup_valide(Autre_Joueur)==[])):
                    victoire_=self.plat.victoire()
                    print(victoire_)
                    return victoire_
                elif L==[]:
                    print("2 ne peut jouer, passe à 1")
                    tour=1
                else:
                    index=random.randint(0, len(L)-1)
                    nouveau_coup=L.pop(index)
                    nouveau_coup=list(nouveau_coup)
                    print(nouveau_coup, "coups pour 1")
                    self.plat.placer_pion(Joueur_, nouveau_coup[0], nouveau_coup[1])
                    tour=2
                    print("tour passe à 2")     
                if plat.fin_de_partie(Joueur_, Autre_Joueur)==True:
                        victoire_=self.plat.victoire()
                        print(victoire_)
                        return victoire_
        if plat.fin_de_partie(Joueur_, Autre_Joueur)==True:
                victoire_=self.plat.victoire()
                print(victoire_)
                return victoire_
                
    

    






