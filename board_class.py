from copy import deepcopy
import numpy as np
import player_class
#0 = case vide
#1 = case noire
#2 = case blanche
class Plateau:
    """Classe représentant un othellier, 
    
    Attributs:
    plateau: NDArray
        Matrice Numpy représentant l'othellier, avec 0 correspondant à une case vide,
        1 à une case avec un pion noir et 2 à une case avec un pion blanc
    mat_poids: NDArray
        Matrice Numpy représentant les poids de chaque positions pour la fonction d'évaluation
    dict_couleur_pion_adversaire: dict
        Renvoie la couleur de l'adversaire quand on lui envoie une couleur
    liste_directions: list
        Liste de toutes les directions possibles autour d'une position
    dict_equivalence:
        Pour l'affiche de l'othellier, prends un 0,1 ou 2 et renvoie respectivement un espace vide, N ou B
    

    Returns:
        _type_: _description_
    """    
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
        """Initialise l'othellier avec les 4 pions au centre"""
                
        self.plateau=np.zeros((8,8))
        self.plateau[3][3]=1
        self.plateau[4][4]=1
        self.plateau[3][4]=2
        self.plateau[4][3]=2


    def __str__(self) -> str:
        """Définit le comportement de print sur un objet de type Plateau

        Renvoie:
            str: Un affichage simple de l'othellier, exemple pour le plateau initial :
   0 1 2 3 4 5 6 7
  +-+-+-+-+-+-+-+-+
 0| | | | | | | | |
  +-+-+-+-+-+-+-+-+
 1| | | | | | | | |
  +-+-+-+-+-+-+-+-+
 2| | | | | | | | |
  +-+-+-+-+-+-+-+-+
 3| | | |N|B| | | |
  +-+-+-+-+-+-+-+-+
 4| | | |B|N| | | |
  +-+-+-+-+-+-+-+-+
 5| | | | | | | | |
  +-+-+-+-+-+-+-+-+
 6| | | | | | | | |
  +-+-+-+-+-+-+-+-+
 7| | | | | | | | |
  +-+-+-+-+-+-+-+-+
        """   
                     
        ligne_horizontale='  +-+-+-+-+-+-+-+-+'
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
        """Définit le comportement de repr sur un objet de type Plateau

        Returns:
            str: Un affichage de la matrice numpy liée à l'attribut plateau de l'objet Plateau
        """  
              
        return str(self.plateau)
    
    def __len__(self)->int:
        """Définit le comportement de len sur un objet de type Plateau

        Returns:
            int: La "longueur" du plateau, correspondant au nombre de cases occupées
        """        
        
        return len(self.liste_position_occupées())
    
    def liste_position_occupées(self)->list:
        """Renvoie la liste des cases occupées par des pions

        Returns:
            list: Liste des cases occupées
        """  
              
        resultat=np.where((self.plateau==1) | (self.plateau==2))
        return list(zip(resultat[1], resultat[0]))
    
    def est_sur_plateau(self,x:int,y:int)-> bool:
        """Définit si une position donnée est sur le plateau 

        Args:
            x (int): la position x de l
            y (int): _description_

        Returns:
            bool: _description_
        """        
        if type(x)==type(y)==int and x in range(8) and y in range(8):
            return True
        return False   
     
    def coup_retourne_un_pion(self,joueur:player_class.Joueur,x:int,y:int) -> bool:
        """Permet de savoir si placer un pion d'une couleur donnée à des coordonnées (x,y)
        permet de retourner au moins un pion
    

        Args:
            joueur (player_class.Joueur): Joueur qui joue le pion
            x (int): coordonnée x du pion à vérifier
            y (int): coordonnée y du pion à vérifier

        Returns:
            bool: True si un pion sera retourné, False sinon
        """        
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
        """Pour qu'un coup soit valide dans le jeu d'Othello il doit répondre aux condition suivantes:
        -Évidemment le pion ne peut pas être placé en dehors du plateau ou au dessus d'un pion existant
        -Le pion doit être adjacent à un pion de l'adversaire
        -Le coup doit être tel qu'il retourne au moins un pion adverse
        Cette méthode permet d'évaluer toutes ces règles pour un coup et un joueur donné

        Args:
            joueur (player_class.Joueur): Le joueur pour lequel on veut évaluer la validité du coup
            x (int): coordonnée x du pion à vérifier
            y (int): coordonnée y du pion à vérifier_

        Returns:
            bool: True si le coup est valide selon les règles d'Othello, False sinon
        """        
        if self.plateau[y][x] in [1,2]: #si la case est déjà occupée le coup est invalide d'office
            return False
        for direction_x,direction_y in self.liste_directions:
            if self.est_sur_plateau(x+direction_x,y+direction_y):
                if self.plateau[y+direction_y][x+direction_x]!=joueur.couleur and self.plateau[y+direction_y][x+direction_x]!=0:
                    if self.coup_retourne_un_pion(joueur,x,y):
                        return True
        return False          
    
    def liste_coup_valide(self,joueur:player_class.Joueur)->list:
        """Permet de parcourir le plateau avec la méthode est_coup_valide pour savoir quels sont les
        Args:
            joueur (player_class.Joueur): Joueur dont on veut la liste des coups valides

        Returns:
            list: Une liste de coup valides selon les règles d'othello à un instant t
        """
        position_occupées = self.liste_position_occupées()
        coups_valides=[]
        for x in range(8):
            for y in range(8):
                if (x,y) not in position_occupées:
                    if self.est_coup_valide(joueur,x,y):
                        coups_valides.append((x,y))
        return coups_valides
    
    def fonction_eval_numpy(self,joueur:player_class.Joueur,matrice=mat_poids)->int:
        """Evalue un plateau pour un joueur donné à un instant t

        Args:
            joueur (player_class.Joueur): Le joueur pour lequel on veut évaluer le plateau 
            matrice (NDArray, optional): Matrice (8x8) de poids pour chaque position. Par défaut est l'attribut mat_poids.

        Returns:
            int: Evaluation
        """                 
        couleur_pion_adversaire=self.dict_couleur_pion_adversaire[joueur.couleur]
        point=np.sum(np.where(self.plateau==joueur.couleur,matrice,0))
        point-=np.sum(np.where(self.plateau==couleur_pion_adversaire,matrice,0))
        return point

    def placer_pion(self,joueur:player_class.Joueur,x:int,y:int)->None:
        """Permet de placer un pion à des coordonnées (x,y), et de faire toutes les opérations de retournement de pion nécessaire

        Args:
            joueur (player_class.Joueur): Joueur qui place le pion
            x (int): coordonnée x du pion à placer
            y (int): coordonnée y du pion à placer

        Returns:
            Techniquement ne renvoie rien, mais modifie l'attribut plateau
        """        
        #à refaire
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
        """Retire le pion aux coordonnées (x,y)"""
        self.plateau[y][x]=0
    
    def fin_de_partie(self,joueur1:player_class.Joueur,joueur2:player_class.Joueur)->bool:
        """Permet de savoir si la partie est finie

        Args:
            joueur1 (player_class.Joueur): Un des deux joueurs
            joueur2 (player_class.Joueur): l'autre joueur

        Returns:
            bool: True si le plateau est plein ou si aucun des deux joueurs ne peuvent jouer, False sinon
        """        
        if len(self)==64 or (len(self.liste_coup_valide(joueur1)) == 0 and len(self.liste_coup_valide(joueur2))==0):
            return True
        return False    
    def victoire(self):
        """Permet de savoir, sachant le plateau actuel, le score des deux joueurs et qui est en train de gagner/a gagné 

        Returns:
            tuple: Le premier élément est le score du joueur 1,
            le deuxième le score du joueur 2 
            et le 3ème est le vainqueur de la partie
        """        
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
