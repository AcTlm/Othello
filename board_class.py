import numpy as np
#0 = case vide
#1 = case noire
#2 = case blanche
class Plateau:
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
            ligne_k=[self.dict_equivalence[pion] for pion in self.board[k]]
            chaine_k=f" {k}|{ligne_k[0]}|{ligne_k[1]}|{ligne_k[2]}|{ligne_k[3]}|{ligne_k[4]}|{ligne_k[5]}|{ligne_k[6]}|{ligne_k[7]}|"
            str_finale+="\n"+chaine_k
            str_finale+="\n"+ligne_horizontale
        return str_finale
    
    def est_sur_plateau(self,x,y)-> bool:
        if type(x)==type(y)==int and x in range(8) and y in range(8):
            return True
        return False    
    
    def est_mouvement_valide(self,x,y)->bool:
        #/!\ATTENTION NE PRENDS PAS EN COMPTE LA CONDITION "le mouvement doit retourner au moins un pion", à faire dans placer_pion
        liste_position_cardinales=[[0,-1],[1,0],[0,1],[-1,0]]
        for direction_x,direction_y in liste_position_cardinales:
            if self.est_sur_plateau(x+direction_x,y+direction_y):
                if self.plateau[x+direction_x][y+direction_y] != self.plateau[x][y] and self.plateau[x+direction_x][y+direction_y]!=0:
                    return True
        return False
    
    def placer_pion(self,joueur_id,x,y)->None:
        pass
            
x=Plateau() #initialise plateau
print(x) #sort le contenu de la méthode __str__
#tests que la fonction est_sur_plateau fonctionne
print(x.est_sur_plateau(8,4))
print(x.est_sur_plateau(7,4))
print(x.est_sur_plateau(7,4.3))
print(x.est_sur_plateau(7,8))
#RAS
