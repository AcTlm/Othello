def alphabeta(plateau_actuel,profondeur:int,joueur_actuel:Joueur,adversaire:Joueur,alpha,beta):
    liste_coup=plateau_actuel.liste_coup_valide(joueur_actuel)
    meilleur_coup=[None,None]
    if profondeur==0 or plateau_actuel.fin_de_partie(joueur_actuel,adversaire):
            return [None,plateau_actuel.fonction_eval_numpy(joueur_actuel)]

    maxEval=-infini
    for coup in plateau_actuel.liste_coup_valide(joueur_actuel):
        plateau_copy=deepcopy(plateau_actuel)
        plateau_copy.placer_pion(joueur_actuel,coup[0],coup[1])
        #print(plateau_copy)
        #print("profondeur =",profondeur,"len = ",len(plateau_copy))
        evaluation=minmax(plateau_copy,profondeur-1,adversaire,joueur_actuel,alpha,beta)[1]
        #print(evaluation)

        plateau_copy.retirer_pion(coup[0],coup[1])
        if evaluation>maxEval:
            maxEval=evaluation
            alpha > evaluation ### add
            if beta <= alpha:
                break
            meilleur_coup=coup
           

    return [meilleur_coup,maxEval]
