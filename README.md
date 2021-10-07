# planétaire

![système solaire](_gitdoc/solar-system.jpg)

Ce projet consiste à réaliser un planétaire mécanique à l'échelle d'un bureau, à base d'impression 3D et d'électronique (Raspberry pico)

## cadrage du projet 

Quelques bases concernant [les dimensions](https://www.papsdroid.fr/post/planetaire) du système solaire

Notre planétaire mécanique à l'échelle d'un bureau va:
* représenter les orbites sous forme de cercles
* tricher sur les proportions des orbites et taille de Jupiter et Saturne (et du soleil)
* intégrer les 6 planètes visibles à l’œil nu: Mercure, Vénus, la Terre (et son satellite la lune), Mars, Jupiter et Saturne.

Un peu de théorie avec [les engrenages](https://www.papsdroid.fr/post/planetaire-engrenages)
* les roues dentées utlisées doivent être limitées en nombre de dents (de 13 à 100)
* les engrenages simples (2 roues dentées) ne permettent pas d'obtenir de gros rapport de réduction R = -d1/d2 (avec 2 roues) ou R = +d1/d3 (avec 3 roues: le nombre de dents de la roue intermédiaire ne compte pas dans le rapport de réduction)
* les engrenages à étage permettent d'aller chercher les gros rapports de réduction selon l'équation:

```python
R = (-1)^y * (Z1 * Z2 *..* Zn) / (D1 * D2 * ... * Dm)
```

* y est le nombre de contacts entre les dents.
* Zi, Dj le nombre de dents d'une roue.
* n le nombre de roue menantes.
* m le nombre de roue menées.


## calcul des réduction d'engrenages 

le programme **engrenage_reduction.py** (dossier /python) calcule la meilleure solution d'engenages sur 2, 3 ou 4 étages pour obtenir un rapport de réduction R donné. Plus de détail dans [cet article](https://www.papsdroid.fr/post/planetaire-calcul-engrenages).

## Conception des étages d'engrenages par planète

### Mercure
La conception du prototype en 3D est expliquée [ici](https://www.papsdroid.fr/post/mercure)

![Mercure](_gitdoc/Mercure.jpg)

Ce premier prototype utilise un mécanismue de réduction 1/7 avec une roue de 13 dents contre une roue de 13*7=91 dents afin d'avoir un premier axe qui représente une jounée (celui où l'on retrouve la manivelle) et un second qui représente une semaine. Tous les mécanismes vont partir de l'axe des semaines, les rapports sont donc tous réduits par 7 dès le départ.

Mercure tourne autour du soleil en 87,969 jours ( =12,567 semaines). En utilisant des roues menantes de 14  et 15 dents contre des roues menées de 29 et 91 dents j'obtiens un rapport de réduction de 87,967.


### Vénus
conception du modèle 3D: [ici](https://www.papsdroid.fr/post/venus)

![Venus](_gitdoc/Venus.jpeg)

Tous les mécanismes partent désormais de l'axe des semaines avec une réduction de 1/7 dès le départ.
On retrouve donc sur le premier plateau les roues de 14,15, 29 et 91 dents pour obtenir le rapport de réduction 87,967 propre à Mercure 
Le second plateau est quand à lui composé de 2 roues menantes de 16 dents contre des roues menées de 83 et 99 dents afin d'obtenir un rapport de réduction de 224.684 pour Vénus (Vénus tourne autour du soleil en 224,700 jours). On pourrait obtenir une meilleure précision en ajoutant un 3ème étage mais ce gain de précision n'en vaut pas la peine pour cette maquette qui n'a pas vocation à faire des prédictions.
Toutes les planètes sont positionnées sur des plateaux centrés sur des axes creux qui s'emboitent les uns dans les autres.

... construction en cours ...
