import board_class
import random
from copy import deepcopy
import copy
import numpy as np
import math
import sys
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
            vraie_profondeur=min(self.profondeur,64-len(plateau)-1)
            resultat=minmax(plateau,vraie_profondeur,self,adversaire)[0]
            if resultat != None:
                x,y=resultat
            else: #règle le cas de bord du dernier coup
                x,y=random.choice(plateau.liste_coup_valide(self))
        if self.type_joueur=="AlphaBeta":
            vraie_profondeur = min(self.profondeur,64-len(plateau)-1)
            resultat = alphabeta(plateau,vraie_profondeur,self,adversaire,-10000,10000)[0]
            if resultat != None:
                x,y=resultat
            else: #règle le cas de bord du dernier coup
                x,y=random.choice(plateau.liste_coup_valide(self))
        if self.type_joueur=="MCTS":
            MCTS_A=MCTSAgent(self.profondeur,joueur=self,adversaire=adversaire)
            coord,plateau=MCTS_A.Select_un_coup(plateau=plateau)
            x,y=coord

        if self.type_joueur=="Aléatoire":
            coups=plateau.liste_coup_valide(self)
            if len(coups) == 0:
                return False
            x,y = coups[random.randint(0,len(coups) - 1)]
        return x,y
                        
     
infini=100000 #horreur je sais         
def minmax(plateau_actuel,profondeur:int,joueur_actuel:Joueur,adversaire:Joueur):
    #print(f"minmax({'taille du plateau ' + str(len(plateau_actuel))},{'profondeur = '+str(profondeur)},{joueur_actuel},{adversaire})")
    #print(plateau_actuel)
    liste_coup=plateau_actuel.liste_coup_valide(joueur_actuel)
    meilleur_coup=[None,None]
    if profondeur==0 or plateau_actuel.fin_de_partie(joueur_actuel,adversaire):
        return [None,plateau_actuel.fonction_eval_numpy(joueur_actuel)]
 
    maxEval=-infini
    #meilleur_coup=random.choice(plateau_actuel.liste_coup_valide(joueur_actuel))
    for coup in plateau_actuel.liste_coup_valide(joueur_actuel):
        plateau_copy=deepcopy(plateau_actuel)
        plateau_copy.placer_pion(joueur_actuel,coup[0],coup[1])
        #print(plateau_copy)
        #print("profondeur =",profondeur,"len = ",len(plateau_copy))
        evaluation=minmax(plateau_copy,profondeur-1,adversaire,joueur_actuel)[1]        
        plateau_copy.retirer_pion(coup[0],coup[1])
        if evaluation>maxEval:
            maxEval=evaluation
            meilleur_coup=coup
    """if 'meilleur_coup' not in locals() and 'meilleur_coup' not in globals():
        meilleur_coup=False"""
    return [meilleur_coup,maxEval]

def alphabeta(plateau_actuel,profondeur:int,joueur_actuel:Joueur,adversaire:Joueur,alpha,beta):
    liste_coup=plateau_actuel.liste_coup_valide(joueur_actuel)
    meilleur_coup=[None,None]
    if profondeur==0 or plateau_actuel.fin_de_partie(joueur_actuel,adversaire):
            return [None,plateau_actuel.fonction_eval_numpy(joueur_actuel)]
            
    maxEval=-infini
    for coup in plateau_actuel.liste_coup_valide(joueur_actuel):
        plateau_copy=deepcopy(plateau_actuel)
        plateau_copy.placer_pion(joueur_actuel,coup[0],coup[1])
        evaluation=alphabeta(plateau_copy,profondeur-1,adversaire,joueur_actuel,alpha,beta)[1]

        plateau_copy.retirer_pion(coup[0],coup[1])
        maxEval = max(evaluation, maxEval)
        alpha = max(evaluation, alpha)
        if beta <= alpha:
            break
        meilleur_coup=coup
           
    return [meilleur_coup,maxEval]

def uct_score(parent_rollouts, enfant_rollouts, victoire_pct):
# fonction qui calcule score uct pour un noeud: tient compte de la performance associée à ce noeud(% de victoires d'un joueur) et de son facteur d'exploration (ici C est racine de 2)
    if enfant_rollouts==0:
        return 1000
    else:    
        exploration=math.sqrt(math.log(parent_rollouts)/enfant_rollouts)
        # return victoire_pct+(math.sqrt(2))*exploration
        return victoire_pct+(math.sqrt(2)*exploration)


class MCTS_Noeud:
    
    def __init__(self, Joueur_, Autre_Joueur,plat,parent=None, coup=[] ):
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
        nouveau_noeud=MCTS_Noeud(plat=self.plat,parent=self, coup=nouveau_coup, Joueur_=self.Autre_Joueur, Autre_Joueur=self.Joueur_)
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
        if self.plat.liste_coup_valide(Joueur_)==[]:
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
                # print(L)
                if (L==[] and plat.liste_coup_valide(Joueur_)==[]):
                    victoire_=self.plat.victoire()
                    # print(victoire_)
                    self.plat=plat_origin
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
                        # print(victoire_)
                        self.plat=plat_origin
                        return victoire_
            elif tour==1:
                L=plat.liste_coup_valide(Joueur_)
                if (L==[] and (plat.liste_coup_valide(Autre_Joueur)==[])):
                    victoire_=self.plat.victoire()
                    # print(victoire_)
                    self.plat=plat_origin
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
                        # print(victoire_)
                        self.plat=plat_origin
                        return victoire_
        self.plat=plat_origin
        print("bidule")
        #print("voici le plateau d'origine")
        #print(self.plat)
        if plat.fin_de_partie(Joueur_, Autre_Joueur)==True:
                victoire_=self.plat.victoire()
                # print(victoire_)
                self.plat=plat_origin
                return victoire_
        self.plat=plat_origin
        #print("voici le plateau d'origine")
        #print(self.plat)
    

    







class MCTSAgent:
#creation de la classe Agent MCTS qui va appliquer MCTS et UCB sur un nombre défini de rounds 
    def __init__(self, nombre_rounds,joueur,adversaire):
        self.nombre_rounds=nombre_rounds
        self.Joueur_=joueur
        self.Autre_Joueur=adversaire

    def select_un_enfant (self, noeud=MCTS_Noeud):
    #selection du meilleur enfant pour lequel on lancera un roll-out, selection basée sur son score UCB 
        total_rollouts=sum(enfant.nombre_rollouts["roll-out"] for enfant in noeud.enfants)
        meilleur_score=-1
        meilleur_enfant=noeud
        for enfant in noeud.enfants:
            score=uct_score(total_rollouts, enfant.nombre_rollouts["roll-out"], enfant.pourcentage_de_victoires(self.Joueur_))
            if score>meilleur_score:
                meilleur_score=score
                meilleur_enfant=enfant
                meilleur_enfant.plat=enfant.plat
        return meilleur_enfant

    def Affiche_Arbre(self, noeud=MCTS_Noeud,profondeur=0):
    #affiche pour un noeud ses statistiques MTCS: nombre de rollouts et pourcentage de victoires de chaque joueur
        print(profondeur*"\t", "-issu du coup:", noeud.coup, "/", "nb de rollouts:", (noeud.nombre_rollouts["roll-out"]), "/", "% gagnant Joueur_:", noeud.pourcentage_de_victoires(self.Joueur_)*100, "% gagnant Autre_Joueur:", noeud.pourcentag_de_victoires(self.Autre_Joueur)*100)
    

    def Select_un_coup (self, plateau):
        plat_copy=deepcopy(plateau)
        """Action de l'agent MCTS à partir d'un noeud racine: retourne le meilleur coup à jouer pour j1 en applicant MCTS rollouts et selection par UCB """

        racine=MCTS_Noeud(plat=plat_copy, parent=MCTS_Noeud, coup=[], Joueur_=self.Joueur_, Autre_Joueur=self.Autre_Joueur)
        # plat_first=racine.plat
        noeud=racine
        while (noeud.ajout_enfant_possible()):
            nouveau_noeud=noeud.ajout_enfant_aleatoire()

        nouveau_noeud=self.select_un_enfant(noeud)
        # print("Premier noeud selectionné")
        # print(nouveau_noeud.plat)
        plat_origin=copy.deepcopy(nouveau_noeud.plat)
        victoire_=nouveau_noeud.Simuler_jeu_aleatoire(nouveau_noeud.plat, self.Joueur_, self.Autre_Joueur, 2)
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
                if k>30:
                    sys.exit()
                print("noeud associé à k=", k,"\n") 
                #print(noeud.plat)
               
            if (noeud.ajout_enfant_possible()):
                if noeud.nombre_rollouts==0:
                    nouveau_noeud=noeud
                    plat_origin=copy.deepcopy(nouveau_noeud.plat)
                    victoire_=nouveau_noeud.Simuler_jeu_aleatoire(nouveau_noeud.plat, self.Joueur_, self.Autre_Joueur, (2-k%2))
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
                    victoire_=nouveau_noeud.Simuler_jeu_aleatoire(nouveau_noeud.plat, self.Joueur_, self.Autre_Joueur, 2-k%2)
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
        
        maxi=racine.enfants[0]
        for e in (racine.enfants):
            if (e.pourcentage_de_victoires(self.Joueur_)) > (maxi.pourcentage_de_victoires(self.Joueur_)):
                maxi=e
        # print("\n*****\nle meilleur coup à jouer est:", maxi.coup)
        plateau=plat_copy
        return(maxi.coup,plateau)

        # print("\n*****\nresultat final:")
        # print("Racine:")
        # self.Affiche_Arbre(noeud=racine)
        # print("\tEnfants:")
        # for e in (racine.enfants):
            # self.Affiche_Arbre(noeud=e)     
            # for f in e.enfants:
            #     print("\t\tpetit-enfant")
            #     self.Affiche_Arbre(noeud=f,profondeur=1)
            #     for g in f.enfants:
            #         print("\t\t\tarriere-petit enfant")
            #         self.Affiche_Arbre(noeud=g,profondeur=2)

    
        

            
    
    
                