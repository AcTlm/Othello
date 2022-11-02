from board_class import Plateau
from player_class import Joueur
x=Plateau() #initialise plateau
j1=Joueur("Humain",1) #initialise deux joueurs humains j1 et j2 respectivement noirs et blancs
j2=Joueur("MinMax",2,1)
print(x) #sort le contenu de la méthode __str__
#tests que la fonction est_sur_plateau fonctionne
print(x.est_sur_plateau(8,4))
print(x.est_sur_plateau(7,4))
print(x.est_sur_plateau(7,4.3))
print(x.est_sur_plateau(7,8))
#RAS
print(x.est_mouvement_valide(5,4,j1))
print(x.est_mouvement_valide(5,4,j2))
print(x.liste_mouvement_valide(j1))
print(x.liste_mouvement_valide(j2))
print(x.liste_position_occupées())
print(len(x))