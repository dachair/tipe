import matplotlib.pyplot as plt
import numpy as np
from math import sqrt  




plt.figure(figsize=(12, 8))
plt.ylabel ("longueur (m)")
plt.xlabel ("longueur (m)")
plt.grid()


demi_l = 1000  

# ==========================================================
# CLASSE ANTENNE
# ==========================================================
class antenne :
    def __init__ (self, x = 0, y = 0, rayon_emission = demi_l/4) : 
        self.x = x
        self.y = y 
        self.rayon_emission = rayon_emission


class foyer : 
    def __init__(self, nom, x = 0, y = 0, nb_personnes = 1) :
        self.nom = nom
        self.x = x
        self.y = y
        self.nb_personnes = nb_personnes


a0 = antenne(x=demi_l, y=demi_l)


major_yticks = np.arange(0, 2001, 200)
major_xticks = np.arange(0, 2001, 500)
major_ticks = np.arange(-demi_l, demi_l, 200)
minor_ticks = np.arange(-demi_l, demi_l, 25)

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


def afficher_antennes (liste_antennes : []):
    for i, a in enumerate(liste_antennes) : 
        circle = plt.Circle((a.x, a.y), a.rayon_emission, fill=False)
        plt.scatter(a.x, a.y, s=(a.rayon_emission)/100, color='black')
        m_ax.annotate("a"+str(i), (a.x, a.y), xytext=(a.x, a.y-50))
        m_ax.add_artist(circle)


def afficher_foyers (liste_foyers) :
    for f in liste_foyers : 
        m_ax.scatter(f.x, f.y, color="red", s=f.nb_personnes*10)
        m_ax.annotate(f.nom, (f.x, f.y), xytext=(f.x + 2, f.y +2), textcoords="data")


print("surface =", demi_l**2, "m²")


f1 = foyer("f1", nb_personnes=2)
f2 = foyer ("f2", 100, 400, nb_personnes= 10)

def euc_distance (f1, f2) : 
    x1 = f1.x
    x2 = f2.x
    y1 = f1.y
    y2 = f2.y
    return (sqrt((x2 -x1)**2 + (y2 -y1)**2))


#calcule le foyer qui a la population la plus grande
#retourne -1 si la liste de foyers est vide
def get_max_pop (foyers) : 
    m, i = (-1, -1) #gauche nbr max de personne, droite son indice dans foyers
    for c, f in enumerate(foyers): 
        if f.nb_personnes > m : 
            m, i = (f.nb_personnes, c) 
    return (m, i)


def placer_antenne (foyers : list, antennes : list) :
    max_i = get_max_pop(foyers)[1]
    max_x, max_y = (foyers[max_i].x, foyers[max_i].y)
    antennes.append(antenne(x=max_x, y=max_y))


#vérifie si un foyer est couvert par une antenne et retourne true, l'antenne concernée sinon faux
def est_couvert (antennes, foyer) :
    for i, a in enumerate(antennes):
        if (euc_distance(a, foyer) <= a.rayon_emission) : 
            return (True, i)
    return False


#m_ax.scatter(f1.x, f1.y, color="red")
#m_ax.annotate(f1.nom, (f1.x, f1.y), xytext=(f1.x + 2, f1.y +2), textcoords="data")

foyers = [f1, f2]
antennes = [a0]
placer_antenne(foyers, antennes)

a1 = antennes[1]
a1.x = (f1.x + f2.x)/2
a1.y = (f1.y + f2.y)/2
#c'est mieux de placer l'antenne entre 2 foyers quand elle peut couvrir les 2


afficher_foyers(foyers)

afficher_antennes(antennes)
plt.show()


