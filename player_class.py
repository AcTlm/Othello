from treelib import Tree,Node
import board_class

class Joueur:
    liste_id_joueurs=[1,2]
    #rappel 1 <=> Noir, 2 <=> Blanc
    liste_type_joueur=["Humain","MinMax","AlphaBeta","MCTS"]
    def __init__(self,type_joueur,couleur_booleen,profondeur=3) -> None:
        if couleur_booleen not in self.liste_id_joueurs:
            raise ValueError('Choisissez une valeur valable pour la couleur (1 pour noir,2 pour blanc)')
        elif type_joueur not in self.liste_type_joueur:
            raise ValueError('Choisissez une valeur valable pour le type de joueur (un élément de ["Humain","MinMax","AlphaBeta","MCTS"])')
        else:
            self.type_joueur=type_joueur
            self.couleur=couleur_booleen
            self.profondeur=profondeur
    
    def get_move(self,plateau):
        if self.type_joueur=="Humain":
            validite_mouvement=False
            while validite_mouvement==False:
                print("veuillez entrer xy l'endroit où vous voulez mettre le pion (par exemple 53 pour mettre un pion en (5,3))")
                entree=input()
                if len(entree) == 2 and entree.isnumeric():
                    x=int(entree[0])
                    y=int(entree[1])
                    if (x,y) not in plateau.liste_mouvement_valide(self) :
                        print("mouvement non valide essayez d'autres coordonnées")
                    else:
                        validite_mouvement==True
        if self.type_joueur=="MinMax":
            arbre=Tree()
        
        return x,y            
                        
     
