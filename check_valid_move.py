#plateau=Plateau()
#print(plateau)

direction = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]] # 8 directions 
print (direction) 


def check_valid_move(plateau, tmp, x_start, y_start):
    if y >= 0 and y <=7 and x >= 0 and x <= 7 : ## les rgles du jeu ne permettent pas un déplacemnt vers ces coordonnées 
        return False 
    if plateau[x_start][y_start]!= 0 : ## vérifier que les coordonnées saisies  sont sur le plateau donc diff de 0 
        return False 

    plateau[x_start][y_start]= tmp # placement temporaire du pion 
    
    if tmp == 'N':
        tmp_adrversaire = 'B' ## tmp_adrversaire = tuile de l'autre joueur 
    else:
        tmp_adrversaire = 'N'
    return_tmp= []

    for x_dir, y_dir in direction : 
        x = x_start
        y = y_start

        x += x_dir
        y += y_dir

        if plateau[x][y] == tmp_adrversaire and y >= 0 and y <=7 and x >= 0 and x <= 7 :
            x += x_dir
            y += y_dir
            if not (y >= 0 and y <=7 and x >= 0 and x <= 7) :
                continue 

            while plateau[x][y] == tmp_adrversaire:
                x += x_dir
                y += y_dir
                if not (y >= 0 and y <=7 and x >= 0 and x <= 7) :
                        break 

            if not (y >= 0 and y <=7 and x >= 0 and x <= 7) :
                continue 
        
            if plateau[x][y] == tmp: ## y a t-il des pièces a retourner ? 
                while True:
                    x = x - x_dir
                    y = y - y_dir
                    if x == x_start and y == y_start:
                        break
                    return_tmp.append([x, y])
           
    plateau[x_start][y_start] = ' '  #" suppresion du placement temporaire"
    if len(return_tmp) == 0 : 
        return False
    return return_tmp
