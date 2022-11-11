from copy import deepcopy
import numpy as np
import player_class
#0 = case vide
#1 = case noire
#2 = case blanche
class Plateau:
    mat_poids=np.array([[120,-20,20,5,5,20,-20,120],
            [-20,-40,-5,-5,-5,-5,-40,-20],
            [20,-5,15,3,3,15,-5,20],
            [5,-5,3,3,3,3,-5,5],
            [5,-5,3,3,3,3,-5,5],
            [20,-5,15,3,3,15,-5,20],
            [-20,-40,-5,-5,-5,-5,-40,-20],
            [120,-20,20,5,5,20,-20,120]])
    dict_couleur_pion_adversaire={
        1:2,
        2:1
    }
    liste_id_joueurs=[1,2]
    liste_directions=[[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
    dict_equivalence = {
            0:" ",
            1:"N",
            2:"B"
        }
    def __init__(self) -> None:
        self.plateau=np.zeros((8,8))
        self.plateau[3][3]=1
        self.plateau[4][4]=1
        self.plateau[3][4]=2
        self.plateau[4][3]=2


    def __str__(self) -> str:        
        ligne_horizontale='  +-+-+-+-+-+-+-+-+'
        ligne_verticale=  '  | | | | | | | | |'
        nombres =         '   0 1 2 3 4 5 6 7'
        str_finale=""
        str_finale+=nombres
        str_finale+="\n"+ligne_horizontale
        for k in range(8):
            ligne_k=[self.dict_equivalence[pion] for pion in self.plateau[k]]
            chaine_k=f" {k}|{ligne_k[0]}|{ligne_k[1]}|{ligne_k[2]}|{ligne_k[3]}|{ligne_k[4]}|{ligne_k[5]}|{ligne_k[6]}|{ligne_k[7]}|"
            str_finale+="\n"+chaine_k
            str_finale+="\n"+ligne_horizontale
        return str_finale
    
    def __repr__(self) -> str:
        return str(self.plateau)
    
    def est_sur_plateau(self,x:int,y:int)-> bool:
        if type(x)==type(y)==int and x in range(8) and y in range(8):
            return True
        return False   
     
    def coup_retourne_un_pion(self,joueur:player_class.Joueur,x:int,y:int) -> bool:
        x_depart,y_depart=x,y
        for direction_x,direction_y in self.liste_directions:
            x,y=x_depart,y_depart
            flag_a_rencontre_autre_couleur=False #Pour retirer le cas "Passe par 0 cases de couleur opposées avant de trouver une case de même couleur"
            x= x + direction_x
            y += direction_y
            if not self.est_sur_plateau(x, y):
                continue
            while self.plateau[y][x] == self.dict_couleur_pion_adversaire[joueur.couleur]:
                x += direction_x
                y += direction_y
                flag_a_rencontre_autre_couleur=True     
                if not self.est_sur_plateau(x, y): # break out of while loop, then continue in for loop
                    break
            if not self.est_sur_plateau(x, y):
                continue
            if self.plateau[y][x] == joueur.couleur and flag_a_rencontre_autre_couleur==True:
                return True
            x,y=x_depart,y_depart
        return False
    
    def est_coup_valide(self,joueur:player_class.Joueur,x:int,y:int)->bool:
        liste_position_cardinales=[[0,-1],[1,0],[0,1],[-1,0]]
        if self.plateau[y][x] in [1,2]: #si la case est déjà occupée le coup est invalide d'office
            return False
        for direction_x,direction_y in self.liste_directions:
            if self.est_sur_plateau(x+direction_x,y+direction_y):
                if self.plateau[y+direction_y][x+direction_x]!=joueur.couleur and self.plateau[y+direction_y][x+direction_x]!=0:
                    if self.coup_retourne_un_pion(joueur,x,y):
                        return True
        return False
    
    def liste_position_occupées(self)->list:
        resultat=np.where((self.plateau==1) | (self.plateau==2))
        return list(zip(resultat[1], resultat[0]))
    
    def fin_de_partie(self,joueur1:player_class.Joueur,joueur2:player_class.Joueur):
        if len(self)==64 or (len(self.liste_coup_valide(joueur1)) == 0 and len(self.liste_coup_valide(joueur2))==0):
            return True
        return False
            
    
    def __len__(self)->int:
        return len(self.liste_position_occupées())
    
    def liste_coup_valide(self,joueur:player_class.Joueur)->list:
        position_occupées = self.liste_position_occupées()
        coups_valides=[]
        for x in range(8):
            for y in range(8):
                if self.est_coup_valide(joueur,x,y) and (x,y) not in position_occupées:
                    coups_valides.append((x,y))
        return coups_valides
    
    def fonction_eval_numpy(self,joueur:player_class.Joueur,matrice=mat_poids)->int:         
        couleur_pion_adversaire=self.dict_couleur_pion_adversaire[joueur.couleur]
        point=np.sum(np.where(self.plateau==joueur.couleur,matrice,0))
        point-=np.sum(np.where(self.plateau==couleur_pion_adversaire,matrice,0))
        return point

    def placer_pion(self,joueur:player_class.Joueur,x:int,y:int)->None:
        self.plateau[y][x]=joueur.couleur
        pion_a_changer=[]
        x_depart,y_depart=x,y
        for direction_x,direction_y in self.liste_directions:
            x=x + direction_x
            y += direction_y
            if not self.est_sur_plateau(x, y):
                continue
            while self.plateau[y][x] == self.dict_couleur_pion_adversaire[joueur.couleur]:
                x += direction_x
                y += direction_y
                if not self.est_sur_plateau(x, y): # sors du while, passe au for suivant
                    break
            if not self.est_sur_plateau(x, y):
                continue
            if self.plateau[y][x] == joueur.couleur:
            # S'il y a des pièces à renverser, aller dans le sens inverse jusqu'à atteindre la pièce d'origine, en notant toutes les cases sur le chemin.
                while True:
                    x -= direction_x
                    y -= direction_y
                    if (x == x_depart and y == y_depart) or not self.est_sur_plateau(x,y):
                        break
                    pion_a_changer.append([x, y])
            x,y=x_depart,y_depart
        if len(pion_a_changer) == 0:
            #print("choix non valide, car ne retourne aucun pion")
            return False
        for pion in pion_a_changer:
            x_pion,y_pion=pion
            self.plateau[y_pion][x_pion]=joueur.couleur
    def retirer_pion(self,x,y)->None:
        self.plateau[y][x]=0
        
    def victoire(self):
        liste_score_joueur=[]
        _,comptage=np.unique(self.plateau,return_counts=True)
        for joueur,score in enumerate(comptage):
            if len(comptage)==3:
                if joueur != 0: #ne compte pas les cases vides
                    liste_score_joueur.append((joueur,score))
            else:
                liste_score_joueur.append((joueur,score))
        vainqueur=max(liste_score_joueur,key=lambda x:x[1]) #selectionne le tuple qui le second élément (ici le score) le plus important     
        return liste_score_joueur[0][1],liste_score_joueur[1][1],vainqueur[0]+1


        