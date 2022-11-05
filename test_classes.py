from board_class import Plateau
from player_class import Joueur
x=Plateau() #initialise plateau
j1=Joueur("Humain",1) #initialise deux joueurs humains j1 et j2 respectivement noirs et blancs
j2=Joueur("Humain",2,1)
print(x) #sort le contenu de la méthode __str__
#tests que la fonction est_sur_plateau fonctionne
print(x.est_sur_plateau(8,4))
print(x.est_sur_plateau(7,4))
print(x.est_sur_plateau(7,4.3))
print(x.est_sur_plateau(7,8))
x.liste_coup_valide(j1)
#RAS
print(x.est_coup_valide(j1,5,4))
print(x.est_coup_valide(j2,5,4))
print(x.liste_coup_valide(j1))
print(x.liste_coup_valide(j2))
print(x.liste_position_occupées())
a1=2
a2=4
a,b=a1,a2
a+=3
print(a1)
print(x.fonction_eval_numpy(j1))
"""x1,y1=j1.get_move(x)"""
x.placer_pion(j1,2,4)
print(x)
print(x.fonction_eval_numpy(j1))
x.placer_pion(j2,1,4)
print(x)
print(repr(x))
print(x.coup_retourne_un_pion(j1,0,4))
print(x.liste_coup_valide(j1))
