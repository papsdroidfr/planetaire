import numpy as np
import math

class Wheels():
    """ classe roues dentées avec méthodes de préalcul des multiplications entre roues (2, 3 ou 4)
        et recherche d'un résultat
    """
    def __init__(self, dmin, dmax):
        """ dmin, dmax: nb de dents min et max pour les roues 
        """
        self.l_wheel = np.arange(dmin,dmax+1,1) #toutes les roues dentées,par défaut de 13 à dmax dents inclus
        #print('liste de', self.l_wheel.size, 'roues dentées:', self.l_wheel)
        self.nb_wheel = self.l_wheel.size
        self.precalc() #precalcule toutes les multiplcations possibles entre 2, 3 ou 4 roues

    #fonctions de multiplication de 2, 3 ou 4 roues, utlisées par np.fromfunction()
    def ord2(self,x,y):
        return self.l_wheel[x]*self.l_wheel[y]
    def ord3(self,x,y,z):
        return self.l_wheel[x]*self.l_wheel[y]*self.l_wheel[z]
    def ord4(self, x,y,z,t):
        return self.l_wheel[x]*self.l_wheel[y]*self.l_wheel[z]*self.l_wheel[t]

    def print_l_ord(self, l_ord):
        """ affiche des indications sur une matrice de multiplications
        """
        size = l_ord.size    # nombre de multiplications générées
        shape = l_ord.shape  # dimensions de la matrice
        l=l_ord.flatten()    # mise à plat des éléments de la matrice
        print('...', size, 'multiplications générées avec',len(shape),'roues,',
          'min=',  l[0],      # multiplicateur min
          'max=',  l[size-1]) # multiplicateur max
        
    def precalc(self):
        #génération de toutes les multiplications possibles entre 2, 3 ou 4 roues dentées
        print('pré-calcul des multiplications avec', self.nb_wheel, 'roues dentées',
              'de', self.l_wheel[0], 'à', self.l_wheel[-1],'dents ...')
        self.l_ord2 = np.fromfunction(self.ord2, (self.nb_wheel,self.nb_wheel), dtype=int)
        self.print_l_ord(self.l_ord2)
        self.l_ord3 = np.fromfunction(self.ord3, (self.nb_wheel,self.nb_wheel,self.nb_wheel), dtype=int)
        self.print_l_ord(self.l_ord3)
        self.l_ord4 = np.fromfunction(self.ord4, (self.nb_wheel,self.nb_wheel,self.nb_wheel,self.nb_wheel), dtype=int)
        self.print_l_ord(self.l_ord4)
        self.l_ord=[None, None, self.l_ord2, self.l_ord3, self.l_ord4] #l_ord[n]=  multiplications ordre n de 2 à 4

class Reduction():
    """ résoud l'equation R = (Z1*Z2*...Zn) / (D1*D2*....*Dn)
        R = rapport de réduction > 1
        Zi dents des roues dentées du numérateur (roues menantes)
        Di: dent des roues dentées du dénominateur (roues menées)
        n: nombre de roues par étage = ordre (2, 3 ou 4 max)
    """
    def __init__(self, wheelsN, wheelsD, R):
        self.wheelsN = wheelsN  # roues du numérateur
        self.wheelsD = wheelsD  # roues du dénominateur
        self.R = R              # rapport de réduction (>1) à obtenir

    def seek_factor(self, R, l_D, precision=0.001):
        """ l_ord vaut Wheels.l_ord2, 3 ou 4: toutes les multiplications possibles entre les roues
            R: rapport de reduction à obtenir (>1)
            l_D: liste des roues du dénominateur (roues menées)
            précision (par défaut 1 pour 1000) : cible les numérateurs à rechercher proches de R*D
            retourne la meilleure combinaison de roues dentées (menantes) dans la liste self.l_wheel
            dont le produit = targ +-delta avec le plus faible écart trouvé
        """
        D = np.prod(np.array(l_D))     # D = multiplication des roues du dénominarteur l_D
        targ = int(R*D)                # target numérateur = produit roues menantes à rechercher
        tmin=int(targ*(1-precision/2)) # target min selon precision pour étendre la recherche
        tmax=int(targ*(1+precision/2)) # target max selon precision pour étendre la recherche
        t='avec 2*'+str(len(l_D))+' roues:'
        l_ord = self.wheelsN.l_ord[len(l_D)]  # l'ordre correspond au nb de roues testée dans l_D
        fact_found = l_ord[ (l_ord>=tmin) & (l_ord<=tmax) ] # liste des multiplications trouvées dans l_ord
        #print('fact_found:', fact_found, 'fact_id',fact_id)
        if len(fact_found)==0:
            #print(t,'aucun résultat!')
            return None, None, 100
        else:
            delta = abs(targ-fact_found)  # évaluation des écarts obtenues en valeur absolue
            delta_min = min(delta)        # plus petit écart trouvé en valeur absolue
            # liste des coordonnées des facteurs correspondant au plus petit écart trouvé
            fact_id = np.where( (l_ord==targ+delta_min) | (l_ord==targ-delta_min))
            # fact_id est de la forme ( np.array[liste x], np.array[liste y], .... np.array[liste t])
            # len(fact_id) = 2, 3 ou 4 selon les dimensions de l_ord passée en paramètre
            # fact_id[i][j] = coordonnées [i] dans l_ord du résultats trouvés n°j
            # fact_id[i].shape[0] = nb de résultats trouvés avec le plus petit écart
            # il y a plusieurs solutions identiques car les multiplications sont commutatives: a*b = b*a etc ....
            # ne retenir que la 1ère, les autres sont identiques.
            best_wheels = [ self.wheelsN.l_wheel[fact_id[i][0]] for i in range(len(fact_id))] #liste des roues dentées qui donnent le meilleur résultat
            best_N = np.prod(np.array(best_wheels)) # produit des roues dentées qui donnent le meilleur résultat
            best_R = best_N/D                       # R obtenu avec les roues best_wheels
            best_deltaR = abs(R - best_R)           # écart en valeur absolue par rapport à R ciblé
            error = 100*best_deltaR/R
            print(t,':', best_wheels, '/' , l_D,
                  '=', "%.9f"%(best_R),
                  'erreur:', "%.9f"%(error),'%'
                  )
            return best_wheels, best_R, error #liste des roues qui donnent l'erreur la plus petite

class Application():
    def __init__(self):
        self.wheelsD = Wheels(13,17) #roues dénominateur (de 13 à 17 dents)
        self.wheelsN = Wheels(18,99) #roues numerateur (de 20 à 99 dents) 
        self.loop()
        
    def loop(self):
        #boucle infinie
        while(True):
            print('------------------------------------------------------------------------------')
            R = float(input('Rapport de réduction (>1) à trouver R=? '))
            S = input('Recherche simple (O/n) ? ')
            rReduc = Reduction(self.wheelsN, self.wheelsD, R)
            best_wheelsN, best_wheelsD, best_r, best_e = None, None, None, 100 # mémomiration meilleur résultat
            
            if S!='n': #limite la recherche avec des roues identiques au dénominateur
                for N in range(2,5,1): #tests avec 2, 3 ou 4 roues par étage
                    for w in self.wheelsD.l_wheel:
                        l_D = N*[w] #toutes les roues du dénominateur identiques
                        fact, r, e = rReduc.seek_factor(R,l_D) #solution avec la plus faible erreur
                        if e < best_e:
                            best_wheelsN, best_wheelsD, best_r, best_e = fact, l_D, r, e
            
            else: #recherche parmis toutes les combinaisons de roues dénominateur possibles
                for N in range(2,5,1): #tests avec 2, 3 ou 4 roues par étage
                    wheels_D_flatten = self.wheelsD.l_ord[N].flatten() #mise à plat de toutes les combinaisons wheels_D
                    D_test = []
                    for D in wheels_D_flatten: # pour chaque combinaison de N roues, (D = multiplication des dents des roues)
                        if D not in D_test:    # dénominateur n'a pas déjà été testé
                            l_D_ids = np.where(self.wheelsD.l_ord[N] == D) #récupération des coordonnées dans tableau
                            l_D = [ self.wheelsD.l_wheel[l_D_ids[i][0]] for i in range(N)] #1ère liste de roues dont le produit = D
                            D_test.append(D) 
                            fact, r, e = rReduc.seek_factor(R,l_D) #solution avec la plus faible erreur
                            if e < best_e:
                                best_wheelsN, best_wheelsD, best_r, best_e = fact, l_D, r, e
            print('------------------------------------------------------------------------------')
            print('Meilleur résutat obtenu:',best_wheelsN,'/',best_wheelsD,
                  '=', "%.9f"%(best_r),
                  'erreur:', "%.9f"%(best_e),'%'
                  )
 
                    
if __name__ == '__main__':
    appl=Application() 
    try:
        appl.loop()
    except KeyboardInterrupt:  # interruption clavier CTRL-C
        print("Bye")