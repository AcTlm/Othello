import numpy as np
#0 = case vide
#1 = case noire
#2 = case blanche
class Plateau:
    dict_equivalence = {
            0:" ",
            1:"N",
            2:"B"
        }
    def __init__(self) -> None:
        self.board=np.zeros((8,8))
        self.board[3][3]=1
        self.board[4][4]=1
        self.board[3][4]=2
        self.board[4][3]=2


    
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
        
            
            
x=Plateau()
print(x)