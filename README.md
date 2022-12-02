# Othello

Groupe de Noémie Jacquet, Amine Kabèche, Nora Picaut et Anne-Cécile Toulemonde

## Fonctionnement:

* Pour lancer une simple partie, lancez _execution.py_. Actuellement ce programme est reglé pour lancer une partie entre un joueur noir piloté par un humain et un joueur utilisant l'algorithme MinMax avec une profondeur de 2.  
Pour changer ces réglages, changez les valeurs des variables j1 et j2, en particulier les arguments de la classe Joueur.  
Les arguments disponibles pour "type_joueur" sont:  
  * Humain
  * Aléatoire
  * MinMax
  * AlphaBeta
  * MCTS  
  
  Les arguments disponibles pour "profondeur" sont bien sûr tous les entiers supérieurs à 1.  
  Cependant pour MinMax et AlphaBeta il est conseillé de ne pas aller au delà de 5 pour garder des temps d'exécution raisonnables. MCTS n'est actuellement pas entièrement fonctionnel (cesse de fonctionner en fin de partie), mais l'argument profondeur correspond pour cet algorithme au nombre de rounds joués.

  Il est préférable de ne pas toucher à l'argument "couleur_booleen".
* Pour lancer plusieurs parties afin de récupérer des statistiques sur ces parties on utilise _execution_stat.py_  
Celui-ci fonctionne de manière similaire à _execution.py_ , et donc changer le type de joueurs impliqués fonctionne de la même manière.  

  Il y a un paramètre supplémentaire: "nombre_repetitions"  qui correspond au nombre de partie que l'on veut exécuter.   
  

  Une fois que toutes les parties sont finies, ou qu'un crash arrive, un fichier .csv contenant les informations suivantes pour chaque partie est créé :  
  * Numéro de la partie
  * score du joueur 1
  * score du joueur 2
  * vainqueur de la partie
  * Temps d'exécution de la partie  
  
  Ce module est actuellement réglé pour jouer 10 parties de 2 joueurs jouant au hasard 
  
* Enfin une preuve de concept de l'algorithme MCTS a été fournie avec le module _executionMCTS_vf.py_ , qui utilise les modules _MCTS_Noeud_class.py_ et _MCTSAgent_class.py_.  
Nous avons isolé cette preuve de concept, car les versions des classes contenues dans _MCTS_Noeud_class.py_ et _MCTSAgent_class  sont bien plus verbeuses que serait raisonnable dans un algorithme d'execution d'une partie normale.