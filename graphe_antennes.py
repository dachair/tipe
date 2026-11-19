import numpy as np
import matplotlib.pyplot as plt


# ==========================================================
# CLASSE ANTENNE
# ==========================================================
class Antenne:
    def __init__(self, x, y, h, Pt_dBm, G_dB, f_MHz):
        self.x = x      # km
        self.y = y      # km
        self.h = h      # m
        self.Pt = Pt_dBm
        self.G = G_dB
        self.f = f_MHz


# ==========================================================
# DISTANCE 3D
# ==========================================================
def distance_3D(a1, a2):
    dx = a2.x - a1.x
    dy = a2.y - a1.y
    dh = (a2.h - a1.h) / 1000  # m -> km
    return np.sqrt(dx**2 + dy**2 + dh**2)


# ==========================================================
# HORIZON RADIO
# ==========================================================
def horizon_radio(a1, a2, k=4/3):
    R = 6371
    h1 = a1.h / 1000
    h2 = a2.h / 1000
    return np.sqrt(2*k*R*h1) + np.sqrt(2*k*R*h2)  # km


# ==========================================================
# PUISSANCE RECUE (Friis + pertes)
# ==========================================================
def puissance_recue_dBm(a1, a2):

    d = distance_3D(a1, a2)
    d = max(d, 0.001)

    # coupure horizon
    if d > horizon_radio(a1, a2):
        return -10e6

    # FSPL
    FSPL = 20*np.log10(d) + 20*np.log10(a1.f) + 32.44

    # atténuation supplémentaire (formule pour le moment inconnue, recherche en cours (formule COST-231 Hata),
    # alpha mis un peu au hazard pour se rapprocher des conditions reel)
    alpha_att = 1.8  # dB/km

    Pr = a1.Pt + a1.G + a2.G - FSPL - alpha_att * d

    return Pr


# ==========================================================
# COUVERTURE
# ==========================================================
def afficher_couverture(antenne, antennes, rayon=100, resolution=400):

    X = np.linspace(antenne.x - rayon, antenne.x + rayon, resolution)
    Y = np.linspace(antenne.y - rayon, antenne.y + rayon, resolution)
    X, Y = np.meshgrid(X, Y)

    d = np.sqrt((X - antenne.x)**2 + (Y - antenne.y)**2)
    d = np.maximum(d, 0.001)

    # FSPL
    FSPL = 20*np.log10(d) + 20*np.log10(antenne.f) + 32.44

    alpha_att = 1.8
    Z = antenne.Pt + antenne.G + antenne.G - FSPL - alpha_att * d

    # masque circulaire
    Z[d > rayon] = np.nan

    # affichage
    plt.figure(figsize=(9, 8))

    im = plt.imshow(
        Z,
        extent=(X.min(), X.max(), Y.min(), Y.max()),
        origin='lower',
        cmap='turbo',
        vmin=-115,
        vmax=-40
    )

    # contours (zones radio)
    contours = plt.contour(
        X, Y, Z,
        levels=[-110, -100, -90, -80, -70],
        colors='white',
        linewidths=0.8
    )
    plt.clabel(contours, inline=True, fontsize=8)

    # antennes
    for i, ant in enumerate(antennes):
        if ant == antenne:
            plt.scatter(ant.x, ant.y, color='cyan', s=140, edgecolors='black')
        else:
            plt.scatter(ant.x, ant.y, color='black', s=70)

        plt.text(ant.x + 0.5, ant.y + 0.5, f"A{i+1}")

    cbar = plt.colorbar(im)
    cbar.set_label("Puissance reçue (dBm)")

    plt.xlabel("Distance (km)")
    plt.ylabel("Distance (km)")
    plt.title("Couverture radio isotrope")
    plt.axis('equal')
    plt.show()


# ==========================================================
# LIENS
# ==========================================================
def afficher_liens(antennes, seuil_dBm=-110):

    plt.figure(figsize=(9, 8))
    plt.gca().set_facecolor("#f7e7c6")

    for i, ant in enumerate(antennes):
        plt.scatter(ant.x, ant.y, color='black', s=80)
        plt.text(ant.x + 0.5, ant.y + 0.5, f"A{i+1}")

    for i, a1 in enumerate(antennes):
        for j, a2 in enumerate(antennes):

            if i < j:
                Pr = puissance_recue_dBm(a1, a2)

                if Pr >= seuil_dBm:

                    alpha_visu = min(max((Pr + 120)/80, 0.2), 1)
                    linewidth = max(1, (Pr + 120)/10)

                    plt.plot(
                        [a1.x, a2.x],
                        [a1.y, a2.y],
                        color='darkred',
                        linewidth=linewidth,
                        alpha=alpha_visu
                    )

                    xm = (a1.x + a2.x)/2
                    ym = (a1.y + a2.y)/2

                    plt.text(xm, ym, f"{Pr:.1f} dBm", fontsize=8)

    plt.title("Liens réseau 3G")
    plt.xlabel("Distance (km)")
    plt.ylabel("Distance (km)")
    plt.axis('equal')
    plt.show()


# ==========================================================
# CONFIGURATION 3G pour le moment 
# ==========================================================

frequence = 900  # MHz
puissance = 43    # dBm
gain = 17        # dB

a1 = Antenne(0, 0, 35, puissance, gain, frequence)
a2 = Antenne(41.6, -10, 30, puissance, gain, frequence)
a3 = Antenne(-33, 2, 30, puissance, gain, frequence)
a4 = Antenne(0, 36, 25, puissance, gain, frequence)
a5 = Antenne(25, -38, 25, puissance, gain, frequence)
a6 = Antenne(10, 10, 25, puissance, gain, frequence)
a7 = Antenne(-50, -12, 25, puissance, gain, frequence)
a8 = Antenne(-28, -33, 25, puissance, gain, frequence)
a9 = Antenne(-15, 10, 30000, puissance, gain, frequence)

antennes = [a1,a2,a3,a4,a5,a6,a7,a8,a9]


# ==========================================================
# EXECUTION
# ==========================================================

afficher_couverture(a1, antennes)
afficher_liens(antennes, seuil_dBm=-110)