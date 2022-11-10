from treelib import Tree,Node
import board_class
import random
from copy import deepcopy
import numpy as np
class Joueur:
    liste_id_joueurs=[1,2]
    #rappel 1 <=> Noir, 2 <=> Blanc
    liste_type_joueur=["Humain","MinMax","AlphaBeta","MCTS","Aléatoire"]
    def __init__(self,type_joueur,couleur_booleen,profondeur=3) -> None:
        if couleur_booleen not in self.liste_id_joueurs:
            raise ValueError('Choisissez une valeur valable pour la couleur (1 pour noir,2 pour blanc)')
        elif type_joueur not in self.liste_type_joueur:
            raise ValueError('Choisissez une valeur valable pour le type de joueur (un élément de ["Humain","MinMax","AlphaBeta","MCTS"])')
        else:
            self.type_joueur=type_joueur
            self.couleur=couleur_booleen
            self.profondeur=profondeur
    def __str__(self):
        return f"Joueur n°{self.couleur} de type {self.type_joueur} {'' if self.type_joueur=='Humain' else 'avec une profondeur de '+str(self.profondeur)}"
    infini=100000 #horreur je sais
    """def minmax(self,plateau_actuel:board_class.Plateau,profondeur):
        dict_prochain_joueur={
            self:adversaire,
            adversaire:self
        }
        if profondeur==0:
            return plateau_actuel.fonction_eval_numpy(self)
        if adversaire==self:
            maxEval=-self.infini
            for coup in plateau_actuel.liste_coup_valide(self):
                plateau_copy=deepcopy(plateau_actuel)
                plateau_copy.placer_pion(coup[0],coup[1])
                eval=self.minmax(plateau_copy,profondeur-1,adversaire)
                maxEval=max(maxEval,eval)
            return maxEval"""
                
        

    def get_move(self,plateau,adversaire):
        if self.type_joueur=="Humain":
            validite_coup=False
            while validite_coup==False:
                print("veuillez entrer xy l'endroit où vous voulez mettre le pion (par exemple 53 pour mettre un pion en (5,3))")
                entree=input()
                if len(entree) == 2 and entree.isnumeric():
                    x=int(entree[0])
                    y=int(entree[1])
                    if (x,y) not in plateau.liste_coup_valide(self) :
                        print("coup non valide essayez d'autres coordonnées")
                    else:
                        validite_coup==True
                        break
        if self.type_joueur=="MinMax":
            evaluation=minmax(plateau,self.profondeur,self,adversaire)
            x,y=evaluation
        if self.type_joueur=="AlphaBeta":
            pass
        if self.type_joueur=="MCTS":
            pass
        if self.type_joueur=="Aléatoire":
            coups=plateau.liste_coup_valide(self)
            if len(coups) == 0:
                return False
            x,y = coups[random.randint(0,len(coups) - 1)]
        return x,y
                        
     
infini=100000 #horreur je sais         
"""def minmax(plateau_actuel:board_class.Plateau,profondeur:int,joueur_actuel:Joueur,adversaire:Joueur):
    print(f"minmax({'taille du plateau ' + str(len(plateau_actuel))},{'profondeur = '+str(profondeur)},{joueur_actuel},{adversaire})")
    print(plateau_actuel)
    if profondeur==0:
        #print("profondeur =",profondeur,"len = ",len(plateau_actuel))
        #print(plateau_actuel)
        return plateau_actuel.fonction_eval_numpy(adversaire)
    maxEval=-infini
    for coup in plateau_actuel.liste_coup_valide(joueur_actuel):
        plateau_copy=deepcopy(plateau_actuel)
        plateau_copy.placer_pion(joueur_actuel,coup[0],coup[1])
        #print(plateau_copy)
        #print("profondeur =",profondeur,"len = ",len(plateau_copy))
        eval=minmax(plateau_copy,profondeur-1,adversaire,joueur_actuel)
        maxEval=max(maxEval,eval)
    return maxEval"""

def minmax(plateau_actuel,profondeur:int,joueur_actuel:Joueur,adversaire:Joueur):
    print(f"minmax({'taille du plateau ' + str(len(plateau_actuel))},{'profondeur = '+str(profondeur)},{joueur_actuel},{adversaire})")
    #print(plateau_actuel)
    plateaux=[]
    choix=[]
    for move in plateau_actuel.liste_coup_valide(joueur_actuel):
        plateau_copie=deepcopy(plateau_actuel)
        plateau_copie.placer_pion(joueur_actuel,move[0],move[1])
        plateaux.append(plateau_copie)
        choix.append(move)
    #print("plateauuuuuuuuuu",plateaux)
    if profondeur==0:
        #print("eval=",plateau_actuel.fonction_eval_numpy(joueur_actuel,plateau_actuel.mat_poids),None)
        return [plateau_actuel.fonction_eval_numpy(joueur_actuel),None]
    maxEval=-infini
    for plateau in plateaux:
        val=minmax(plateau_actuel,profondeur-1,adversaire,joueur_actuel)[0]
        if val>maxEval:
            maxEval=val
            plateau_actuel=plateau
    #print("choix= ",choix)
    #print(plateaux)
    #print([maxEval,plateau_actuel])
    print(plateau_actuel)
    print(plateau_actuel.liste_coup_valide(joueur_actuel))
    #print(choix[plateaux.index(plateau_actuel)])
    return (choix[plateaux.index(plateau_actuel)])