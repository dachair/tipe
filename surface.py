import matplotlib.pyplot as plt
import numpy as np




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
    for a in liste_antennes : 
        circle = plt.Circle((a.x, a.y), a.rayon_emission, fill=False)
        plt.scatter(a.x, a.y, s=(a.rayon_emission)/100, color='black')
        m_ax.add_artist(circle)

a1 = antenne(x=demi_l/4, y=0)
a2 = antenne(x=2*demi_l/4, y=0)


print("surface =", demi_l**2, "m²")

afficher_antennes([a0, a1, a2])
plt.show()


