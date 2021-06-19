#taille relatives des planètes du système solaire

import matplotlib.pyplot as plt
from math import *

# diamètre et distance au soleil (*1000) des planètes en km
# source: https://fr.m.wikipedia.org/wiki/Système_solaire
planetes =   ['Mercure', 'Vénus', 'Terre', 'Mars', 'Jupiter', 'Saturne', 'Uranus',   'Neptune']
color_p =    [   'grey',  'gold',  'blue',  'red',  'orange',   'brown',   'cyan',  'darkblue']
diametre_p = [     4878,   12103,   12756,   6792,    142984,    120536,    51118,      49528 ]
dist_p =     [    57909,  108160,  149600, 227990,    778360,   1433500,  2872400,    4498400 ]
revol_p =    [       88,   224.7,  365.25,    687,      4380,     10950,    30660,      60225 ] 
    
DIAM_MAX =         150000
DIST_MAX =        5000000
DIST_MAX_INTERNE = 230000


#liste des orbites représentées par des cercles
orbites_full = [plt.Circle( xy=(0.5, 0.5), #centre des orbites  
                       radius = dist_p[i]/2/DIST_MAX,
                       color = color_p[i],
                       linewidth=1, fill=False)
           for i in range(len(planetes)) ]

#liste des orbites des planètes internes à  moins de DIST_MAX_INTERNE du soleil
orbites_interm = [plt.Circle( xy=(0.5, 0.5), #centre des orbites  
                       radius = dist_p[i]/2/DIST_MAX_INTERNE,
                       color = color_p[i],
                       linewidth=1, fill=False)
           for i in range(len(planetes)) ]

fig = plt.figure(1, figsize=(6,9))
ax = plt.subplot(3,2,1)
fig.suptitle('Orbites et diamètre des planètes')
#1ère ligne, 1ère colonne: toutes les orbites
for i in range(len(planetes)):
    ax.add_artist(orbites_full[i])
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_ylabel('MAX ='+str(int(DIST_MAX/1000)) + ' millions km' )
ax.set_title('Orbites')
ax.set_aspect('equal', adjustable='box')

#1ère ligne, 2ème colonne: les orbites internes
ax = plt.subplot(3,2,2)
for i in range(len(planetes)):
    ax.add_artist(orbites_interm[i])
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_ylabel('MAX ='+str(int(DIST_MAX_INTERNE/1000)) + ' millions km' )
ax.set_title('Orbites internes')
ax.set_aspect('equal', adjustable='box')

#2ème ligne: diamètre des planètes sous forme de bargraph
ax = plt.subplot(3,1,2)
plt.bar(planetes, diametre_p, color = color_p, linewidth=1, edgecolor='grey')
plt.title('diamètre planètes (km)')

#3ème ligne: revolution des planètes
ax = plt.subplot(3,1,3)
plt.bar(planetes, revol_p, color = color_p, linewidth=1, edgecolor='grey')
plt.title('revolution planètes (jours)')


plt.show()
    
