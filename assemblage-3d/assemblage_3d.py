#!/usr/bin/env python3
"""Cube de la question 17, Kangourou 2022 E. Python 3 + Tkinter.

Lancer : python3 assemblage_3d.py
Vérifier la géométrie sans ouvrir de fenêtre : python3 assemblage_3d.py --verifier
Les faces cachées constituent une reconstruction compatible avec le dessin.
"""

import argparse
from dataclasses import dataclass
import math
import time


@dataclass(frozen=True)
class Piece:
    nom: str
    cases: tuple
    couleur: str


def pieces_originales():
    pieces = [
        Piece('L1', tuple(sorted({(2, 0, z) for z in range(3)} |
                                  {(2, y, 2) for y in range(3)})), '#bfc8d2'),
        Piece('L2', tuple(sorted({(0, 2, z) for z in range(3)} |
                                  {(x, 2, 0) for x in range(3)})), '#bfc8d2'),
        Piece('P1', tuple((0, 0, z) for z in range(3)), '#647084'),
        Piece('P2', tuple((1, y, 1) for y in range(3)), '#647084'),
    ]
    occupe = {c for p in pieces for c in p.cases}
    for z in range(3):
        for y in range(3):
            for x in range(3):
                if (x, y, z) not in occupe:
                    pieces.append(Piece(f'B{len(pieces)-3}', ((x, y, z),), '#f5f7fb'))
    return pieces


def verifier():
    pieces = pieces_originales()
    cases = [c for p in pieces for c in p.cases]
    assert len(cases) == len(set(cases)) == 27, 'Chevauchement ou trou'
    assert set(cases) == {(x, y, z) for x in range(3)
                          for y in range(3) for z in range(3)}
    assert [len(p.cases) for p in pieces] == [5, 5, 3, 3] + [1] * 11
    types = {c: p.nom[0] for p in pieces for c in p.cases}
    # Contraintes lues sur les trois faces de la figure, lignes du bas vers le haut.
    for z, ligne in enumerate(['PBL', 'PPL', 'PBL']):
        assert ''.join(types[x, 0, z] for x in range(3)) == ligne
    for y, ligne in enumerate(['PBL', 'BBL', 'LBL']):
        assert ''.join(types[x, y, 2] for x in range(3)) == ligne
    for z, ligne in enumerate(['LBL', 'LBB', 'LLL']):
        assert ''.join(types[2, y, z] for y in range(3)) == ligne
    print('Vérifié : 27 cellules, aucun vide ni chevauchement ; trois faces conformes.')
    print('2 pièces en L de 5 cubes + 2 pavés de 3 cubes + 11 cubes blancs.')


# Sommets de chaque face et normale extérieure. Les faces internes à une pièce
# sont supprimées ; une pièce en L demeure un seul objet pendant l'animation.
FACES = [
    ((-1, 0, 0), [(0,0,0),(0,0,1),(0,1,1),(0,1,0)]),
    ((1, 0, 0), [(1,0,0),(1,1,0),(1,1,1),(1,0,1)]),
    ((0,-1, 0), [(0,0,0),(1,0,0),(1,0,1),(0,0,1)]),
    ((0, 1, 0), [(0,1,0),(0,1,1),(1,1,1),(1,1,0)]),
    ((0, 0,-1), [(0,0,0),(0,1,0),(1,1,0),(1,0,0)]),
    ((0, 0, 1), [(0,0,1),(1,0,1),(1,1,1),(0,1,1)]),
]


def scene(width, height, explosion, azimut, elevation, zoom=1, unites=False):
    pieces = pieces_originales()
    if unites:
        pieces = [Piece(f'{p.nom}.{i+1}', (c,), p.couleur)
                  for p in pieces for i, c in enumerate(p.cases)]
    a, e = math.radians(azimut), math.radians(elevation)
    droite = (-math.sin(a), math.cos(a), 0)
    haut = (-math.sin(e)*math.cos(a), -math.sin(e)*math.sin(a), math.cos(e))
    vue = (math.cos(e)*math.cos(a), math.cos(e)*math.sin(a), math.sin(e))
    scale = min(width / 12, height / 10) * zoom

    def proj(v):
        return (width/2 + scale*sum(v[i]*droite[i] for i in range(3)),
                height/2 - scale*sum(v[i]*haut[i] for i in range(3)),
                sum(v[i]*vue[i] for i in range(3)))

    polygons, etiquettes = [], []
    for p in pieces:
        centre = tuple(sum(c[i]+.5 for c in p.cases)/len(p.cases)-1.5
                       for i in range(3))
        deplacement = tuple(2.0*explosion*v for v in centre)
        occupe = set(p.cases)
        for c in p.cases:
            for normale, sommets in FACES:
                if tuple(c[i]+normale[i] for i in range(3)) in occupe:
                    continue
                if sum(normale[i]*vue[i] for i in range(3)) <= 1e-8:
                    continue
                points = [proj(tuple(c[i]+s[i]-1.5+deplacement[i]
                                     for i in range(3))) for s in sommets]
                lumiere = .76 + .20*max(0, normale[2]) + .08*max(0, -normale[1])
                rgb = [min(255, round(int(p.couleur[i:i+2], 16)*lumiere))
                       for i in (1,3,5)]
                couleur = '#%02x%02x%02x' % tuple(rgb)
                polygons.append((sum(pt[2] for pt in points)/4,
                                 [(pt[0], pt[1]) for pt in points], couleur))
        q = proj(tuple(centre[i]+deplacement[i] for i in range(3)))
        etiquettes.append((q[0], q[1], p.nom))
    polygons.sort(key=lambda f: f[0])
    return polygons, etiquettes


class Application:
    def __init__(self):
        import tkinter as tk
        from tkinter import ttk
        self.tk = tk
        self.root = tk.Tk()
        self.root.title('Assemblage 3D — Kangourou 2022, question 17')
        self.root.geometry('1080x800')
        self.root.minsize(800, 650)
        self.root.configure(bg='#101827')
        self.azimut, self.elevation, self.zoom = -65, 25, 1.25
        self.cible = None
        self.boucle = tk.BooleanVar(value=False)
        self.unites = tk.BooleanVar(value=False)
        self.numeros = tk.BooleanVar(value=False)
        self.quantite = tk.DoubleVar(value=0)
        self.vitesse = tk.DoubleVar(value=1)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#101827')
        style.configure('TLabel', background='#101827', foreground='#dfe8f4')
        style.configure('TCheckbutton', background='#101827', foreground='#dfe8f4')
        tk.Label(self.root, text='Un cube, 15 pièces', font=('Helvetica', 23, 'bold'),
                 bg='#101827', fg='white').pack(pady=(18,4))
        ttk.Label(self.root, text='2 pièces en L × 5  +  2 pavés × 3  +  11 cubes blancs  =  27').pack()
        self.canvas = tk.Canvas(self.root, bg='#101827', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True, padx=10, pady=6)
        controls = ttk.Frame(self.root)
        controls.pack(fill='x', padx=25)
        self.statut = ttk.Label(controls, text='Assemblé — 0 %')
        self.statut.pack()
        self.slider = ttk.Scale(controls, from_=0, to=1, variable=self.quantite,
                                command=lambda _: self.dessiner())
        self.slider.pack(fill='x', pady=7)
        self.slider.bind('<ButtonPress-1>', lambda _: self.arreter())
        ligne = ttk.Frame(controls)
        ligne.pack(pady=5)
        for texte, commande in [('Assembler', lambda: self.animer(0)),
                                 ('Éclater', lambda: self.animer(1)),
                                 ('Pause', self.arreter), ('Vue initiale', self.initiale)]:
            ttk.Button(ligne, text=texte, command=commande).pack(side='left', padx=4)
        ttk.Checkbutton(ligne, text='Aller-retour', variable=self.boucle,
                         command=self.changer_boucle).pack(side='left', padx=12)
        ligne2 = ttk.Frame(controls)
        ligne2.pack(pady=7)
        ttk.Checkbutton(ligne2, text='Décomposer en 27 cubes', variable=self.unites,
                         command=self.dessiner).pack(side='left', padx=8)
        ttk.Checkbutton(ligne2, text='Repères des pièces', variable=self.numeros,
                         command=self.dessiner).pack(side='left', padx=8)
        ttk.Label(ligne2, text='Vitesse').pack(side='left', padx=(20,5))
        ttk.Scale(ligne2, from_=.25, to=2, variable=self.vitesse,
                  length=110).pack(side='left')
        ttk.Label(controls, text='Glisser : tourner  •  Molette : zoomer  •  Espace : lecture / pause').pack(pady=4)
        ttk.Label(controls, text='Faces cachées : reconstruction compatible avec la figure. Éclatement illustratif, sans simulation physique.').pack(pady=(2,14))
        self.canvas.bind('<Configure>', lambda _: self.dessiner())
        self.canvas.bind('<ButtonPress-1>', self.debut_rotation)
        self.canvas.bind('<B1-Motion>', self.rotation)
        self.canvas.bind('<MouseWheel>', self.molette)
        self.canvas.bind('<Button-4>', lambda _: self.zoomer(1.08))
        self.canvas.bind('<Button-5>', lambda _: self.zoomer(1/1.08))
        self.root.bind('<space>', self.espace)
        self.dernier = time.monotonic()
        self.root.after(20, self.tick)

    def dessiner(self):
        t = self.quantite.get()
        polys, labels = scene(self.canvas.winfo_width(), self.canvas.winfo_height(),
                              t, self.azimut, self.elevation, self.zoom, self.unites.get())
        self.canvas.delete('all')
        for _, points, couleur in polys:
            self.canvas.create_polygon(*[v for p in points for v in p],
                                       fill=couleur, outline='#283548', width=1.2)
        if self.numeros.get() and t > .2:
            for x, y, nom in labels:
                self.canvas.create_text(x, y, text=nom, fill='#ffcb66',
                                        font=('Helvetica', 11, 'bold'))
        etat = 'Assemblé' if t < .001 else 'Éclaté' if t > .999 else 'Transition'
        self.statut.configure(text=f'{etat} — {round(t*100)} %')

    def animer(self, cible):
        self.cible = cible

    def arreter(self):
        self.cible = None

    def changer_boucle(self):
        if self.boucle.get():
            self.animer(0 if self.quantite.get() >= .999 else 1)

    def espace(self, _):
        if self.cible is not None:
            self.arreter()
        else:
            self.animer(0 if self.quantite.get() >= .999 else 1)
        return 'break'

    def initiale(self):
        self.azimut, self.elevation, self.zoom = -65, 25, 1.25
        self.dessiner()

    def debut_rotation(self, event):
        self.souris = event.x, event.y

    def rotation(self, event):
        self.azimut -= (event.x-self.souris[0])*.45
        self.elevation = max(-85, min(85, self.elevation+(event.y-self.souris[1])*.45))
        self.souris = event.x, event.y
        self.dessiner()

    def zoomer(self, facteur):
        self.zoom = max(.4, min(3, self.zoom*facteur))
        self.dessiner()

    def molette(self, event):
        self.zoomer(1.06 if event.delta > 0 else 1/1.06)

    def tick(self):
        maintenant = time.monotonic()
        dt = min(.1, maintenant-self.dernier)
        self.dernier = maintenant
        if self.cible is not None:
            t, cible = self.quantite.get(), self.cible
            pas = dt*self.vitesse.get()/3
            t = min(cible, t+pas) if cible > t else max(cible, t-pas)
            self.quantite.set(t)
            self.dessiner()
            if t == cible:
                self.cible = 1-cible if self.boucle.get() else None
        self.root.after(20, self.tick)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verifier', action='store_true')
    args = parser.parse_args()
    if args.verifier:
        verifier()
        return
    try:
        app = Application()
    except ImportError:
        parser.exit(1, 'Tkinter manque. Installez Python avec Tk (python.org), ou python3-tk sous Linux.\n')
    app.root.mainloop()


if __name__ == '__main__':
    main()
