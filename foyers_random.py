from collections.abc import Iterable
from math import hypot
from random import randint
from typing import NamedTuple

import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(12, 8))
plt.ylabel("longueur (m)")
plt.xlabel("longueur (m)")
plt.grid()


demi_l = 1000
min_x, max_x = -demi_l, demi_l
min_y, max_y = -demi_l, demi_l

# ==========================================================
# CLASSE ANTENNE
# ==========================================================
class Antenne(NamedTuple) :
    x: int = 0
    y: int = 0
    rayon_emission: float = demi_l / 4


class Foyer(NamedTuple) : 
    nom: str
    x: int = 0
    y: int = 0
    nb_personnes: int = 1


major_yticks = np.arange(0, 2001, 200)
major_xticks = np.arange(0, 2001, 500)
major_ticks = np.arange(min_x, max_x, 200)
minor_ticks = np.arange(min_y, max_y, 25)

m_ax = plt.gca()

# change l'échelle de la grille principale
m_ax.set_aspect("equal")

m_ax.set_xticks(major_ticks)
m_ax.set_xticks(minor_ticks, minor = True)
m_ax.set_yticks(major_ticks)
m_ax.set_yticks(minor_ticks, minor = True)


m_ax.set_xlim(-demi_l, demi_l)
m_ax.set_ylim(-demi_l, demi_l)

# change la couleur de la grille
m_ax.grid(which='minor', alpha=0.2)
m_ax.grid(which='major', alpha=0.4)


def afficher_antennes(liste_antennes: Iterable[Antenne]) -> None:
    for i, a in enumerate(liste_antennes) : 
        circle = plt.Circle((a.x, a.y), a.rayon_emission, fill=False)
        plt.scatter(a.x, a.y, s=(a.rayon_emission) / 100, color='black')
        m_ax.annotate(f"a{i!s}", (a.x, a.y), xytext=(a.x, a.y - 50))
        m_ax.add_artist(circle)


def afficher_foyers(liste_foyers: Iterable[Foyer]) -> None:
    for f in liste_foyers : 
        m_ax.scatter(f.x, f.y, color="red", s=f.nb_personnes * 10)
        m_ax.annotate(f.nom, (f.x, f.y), xytext=(f.x + 2, f.y + 2), textcoords="data")


print("surface =", demi_l ** 2, "m²")

f1 = Foyer("f1", nb_personnes=2)
f2 = Foyer ("f2", 100, 400, nb_personnes=10)

def euc_distance(f1: Foyer, f2: Foyer) -> float: 
    return hypot(f2.x - f1.x, f2.y - f1.y)

def get_max_pop(liste_foyer: list[Foyer]) -> tuple[int, int]: 
    """
    calcule le foyer qui a la population la plus grande
    retourne -1 si la liste de foyers est vide
    gauche nbr max de personne, droite son indice dans foyers
    """
    return max((f.nb_personnes, i) for f, i in enumerate(liste_foyer)) if liste_foyer else (-1, -1)

def placer_antenne_barycentre(f1: Foyer, f2: Foyer) -> Antenne:
    return Antenne((f1.x + f2.x)/2, (f1.y + f2.y)/2)


# vérifie si un foyer est couvert par une antenne et retourne true, l'antenne concernée sinon faux
def est_couvert(antennes: Iterable[Antenne], foyer: Foyer) -> int:
    for i, a in enumerate(antennes):
        if est_couvert_par(a, foyer): 
            return i
    return -1

def est_couvert_par(antenne: Antenne, foyer: Foyer) -> bool:
    return (euc_distance(antenne, foyer) <= antenne.rayon_emission) 


'''essayer une approche avec kruskal en utilisant un graphe pondéré dont les sommets sont 
les foyers, les foyers ont pour étiquette le nombre de personnes qui y habitent et 
comme poids, pour commencer la distance entre eux, sinon la difficulté qu'aurait une 
onde entre les 2 à se propager'''

# m_ax.scatter(f1.x, f1.y, color="red")
# m_ax.annotate(f1.nom, (f1.x, f1.y), xytext=(f1.x + 2, f1.y +2), textcoords="data")

# On créer les foyers
foyers = set()
NB_FOYER = randint(4,10)
while len(foyers) < NB_FOYER:
    foyers.add((randint(min_x, max_x), randint(min_y, max_y)))
foyers = [Foyer(f"f{i!s}", x, y, randint(1, 15)) for i, (x, y) in enumerate(foyers)]


# on place les antennes sur les barycentres des foyers si les foyers sont couverts par cette
# antenne, sinon on le place sur la barcycentre des foyers les plus importants
# et on diminue jusqu'à couvrir dans le pire cas qu'un seul foyer
#antennes = [placer_antenne_barycentre(*foyers[i:i+2]) for i in range(NB_FOYER - 1)]
antennes = []

#O(len(foyers)^3)
for i in range(len(foyers)):
    if est_couvert(antennes, foyers[i]) < 0:
        for j in range(len(foyers)):
            if i != j:
                if euc_distance(foyers[i], foyers[j]) < demi_l / 4:
                    antennes.append(placer_antenne_barycentre(foyers[i], foyers[i]))
                    continue
                if euc_distance(foyers[i], foyers[j]) < demi_l / 2:
                    antennes.append(placer_antenne_barycentre(foyers[i], foyers[j]))
                    continue
        if est_couvert(antennes, foyers[i]) < 0:
            antennes.append(placer_antenne_barycentre(foyers[i], foyers[i]))



# c'est mieux de placer l'antenne entre 2 foyers quand elle peut couvrir les 2
afficher_foyers(foyers)
print(antennes)
afficher_antennes(antennes)
plt.show()