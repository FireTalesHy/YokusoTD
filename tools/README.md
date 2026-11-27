# Outils

Le jeu tient dans un seul fichier, `index.html`. Ces scripts ont servi à produire les images qu'il embarque (en base64) ; ils ne sont pas nécessaires pour jouer.

## `sprites/` : personnages

Découpe la planche `docs/art/planche-personnages.png` (10 classes × 7 sprites : recrue, puis 2 voies × 3 rangs), retire le fond, réduit chaque sprite à l'échelle pixel du jeu (÷3) et assemble l'atlas.

```bash
pip install pillow numpy scipy
python3 tools/sprites/build.py     # écrit atlas.png (56×44 par sprite, pied à (28,41))
```

La 2e planche (`docs/art/planche-personnages-2.png`, 10 nouvelles classes) se découpe avec `build2.py`. Sur sa ligne du bas, chaque voie n'a que 2 rangs : le 2e rang sert aussi pour le niveau 5. Le jeu charge cet atlas à part (`ATLAS2`, palette de 256 couleurs).

```bash
python3 tools/sprites/build2.py    # écrit atlas2.png, même format
```

## `pixelfx/` : animations d'attaque

Précalcule les 14 effets d'attaque (coups de sabre, impacts, explosions, nova de glace…) avec la version JavaScript de [pixelfx](https://github.com/winkidney/pixelfx-godot). Chaque effet devient une bande d'images : couleur en haut, lumière additive en bas.

```bash
git clone https://github.com/winkidney/pixelfx-godot.git
mkdir pixelfx-godot/bake && cp tools/pixelfx/* pixelfx-godot/bake/
cd pixelfx-godot && node bake/bake.mjs "$(cat bake/specs.json)"   # écrit bake/fx.png et bake/fx.json
```
