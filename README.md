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
* les engrenages simples (2 roues dentées) ne permettent pas d'obtenir de gros rapport de réduction R = -d1/d2 (avec 2 roues) ou R=-d1/d3 (avec 3 roues: le nombre de dents de la roue intermédiaire ne compte pas dans le rapport de réduction)
* les engrenages à étage permettent d'aller chercher les gros rapports de réduction selon l'équation:

R = (-1)^y * (Z1 * Z2 *..* Zn) / (D1 * D2 * ... * Dm)
* y est le nombre de contacts entre les dents.
* Zi, Dj le nombre de dents d'une roue.
* n le nombre de roue menantes.
* m le nombre de roue menées.

 ... conception en cours ...



