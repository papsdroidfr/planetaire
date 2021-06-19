# excentricité des orbites du système solaire

from matplotlib import patches
import matplotlib.pyplot as plt
from math import *

#excentricités orbitale des planètes
# source: https://fr.m.wikipedia.org/wiki/Excentricité_orbitale
planetes = ['Mercure', 'Vénus', 'Terre', 'Mars', 'Jupiter', 'Saturne', 'Uranus', 'Neptune' ]
color_p =  [   'grey',  'gold',  'blue',  'red',  'orange',   'brown',   'cyan', 'darkblue']
ex_planetes = [0.206,   0.007 ,   0.017,  0.093,     0.048,     0.054,    0.047,     0.009 ]

WIDTH=0.9    #taille max des ellipses
PAS = 1/10   #variation petit axe des ellipses

def calc_e(a,b):
    '''calcule l'excentricité d'une ellipse: e = sqrt(1 - a²/b²)
        a : grand axe
        b : petit axe   
    '''
    if b > a:
        a,b = b,a
    return sqrt(1 - (b**2/a**2))

def calc_b(a,ex):
    ''' calcule le petit axe en fonction du grand axe et de l'excentricité
        b = a*sqrt(1-ex²)
    '''
    return a*sqrt(1-ex**2)


#ellipses témoins, grand axe = 1 et petit axe varie par PAS
ellps_tests = [ patches.Ellipse(xy=(0.5, 0.5),
                                width=WIDTH,
                                height=WIDTH-i*PAS,
                                linewidth=2, fill=False)
                for i in range(len(planetes))]

#excentricités des ellipses ellps_tests
ext_tests = [ round(calc_e(a=WIDTH, b=WIDTH-i*PAS),2) for i in range(len(planetes))]

#ellipses orbitales des planètes du système solaire
ellps_orbitales = [ patches.Ellipse(xy=(0.5, 0.5),
                                width=WIDTH,
                                height=calc_b(a=WIDTH, ex=ex_planetes[i]),
                                linewidth=2, fill=False, edgecolor = color_p[i])
         for i in range(len(planetes))]

# sous-graphe 2 lignes * NUM colonnes
fig, axs = plt.subplots(2, len(planetes), subplot_kw={'aspect': 'equal'}, sharey=True, figsize=(15,5))

#1ère ligne du sous_graphe: les ellipes tests
for i in range(len(planetes)):
    axs[0,i].add_patch(ellps_tests[i]) 
    axs[0,i].set_xticklabels([])
    axs[0,i].set_xlabel('e='+str(ext_tests[i])) # excentricité de l'ellipse
axs[0,0].set_title('cercle temoin')

#2ème ligne du sous_graphe: les ellipes orbitales des planètes
for i in range(len(planetes)):
    p = planetes[i]
    axs[1,i].add_patch(ellps_orbitales[i])
    axs[1,i].set_title(p) #titre = nom de la planète
    axs[1,i].set_xticklabels([])
    axs[1,i].set_xlabel('e='+str(ex_planetes[i])) # excentricité
    
   
plt.show()