# Journal des modifications

Les changements notables de YokusoTD, du plus récent au plus ancien.

## 1.2.0 · 27 novembre 2026

### Ajouté

- **5 nouveaux coffres** dessinés en pixel art, chacun en version fermée et ouverte : bois, pierre, marbre, rubis et légende.
- **Ouverture de coffre animée** : chute et rebond, rayons à la couleur du coffre, tremblement, éclair, colonne de lumière, pluie de pièces et cartes qui se retournent une à une. Un nouveau personnage a sa grande carte, un halo de sa rareté et un sceau « Nouveau ! ».
- **Amélioration des personnages** : les coffres donnent des cartes en double. Avec ces cartes et des koban, un personnage monte jusqu'au rang 10 (+10 % de dégâts par rang).
- **Écran de fin de combat** refait : sceau, étoiles qui apparaissent une à une, statistiques (vies, vagues, Oni vaincus, durée) et butin illustré avec un bouton pour ouvrir chaque coffre. En cas de défaite, il montre les Oni qui ont percé les défenses, avec un conseil et un lien vers leur fiche.
- Un coffre toutes les 10 vagues en mode infini, de plus en plus rare.
- Nouvelle icône de koban et nouvelle illustration de la monnaie dans les récompenses.

### Modifié

- **Plus de boutique** : les coffres se gagnent uniquement en jouant. Les koban servent à améliorer les personnages et à l'offrande au sanctuaire.
- **Menu Coffres** refait : grand coffre sélectionné, étagère avec les 5 types, offrande et rappel des façons d'en gagner. La liste des personnages n'y figure plus.
- **Menu Équipe** : personnages triés du plus rare au moins rare, débloqués et verrouillés séparés par un trait.
- **Menus plus simples** : le bouton retour de chaque écran ramène au menu principal. La carte n'a plus qu'un bouton Menu et une flèche pour passer à l'autre carte.
- Les coffres des anciennes sauvegardes sont convertis (laque en marbre, or en rubis), et les rangs déjà gagnés sont conservés.

### Corrigé

- Lancer une partie juste après l'ouverture du jeu pouvait charger un autre niveau que celui choisi.
- Le bouton « Niveau suivant » manquait à partir du niveau 10.

## 1.1.1 · 27 novembre 2026

### Modifié

- Sur l'écran titre, les héros se tiennent sur une étagère en bois laqué (plateau clair, filet doré, volutes et ornement central) à la place de la dalle de pierre. Elle s'adapte au nombre de personnages de l'équipe.

## 1.1.0 · 27 novembre 2026

### Ajouté

- **10 nouveaux personnages**, chacun avec une recrue et 2 voies d'évolution :
  - Hawacha (salves de fusées) : Hawacha ardent, Hawacha de siège.
  - Prêtresse shintō (ofuda qui touchent les spectres) : Miko du sanctuaire, Kitsune.
  - Kunoichi (kunaï empoisonnés) : Kunoichi écarlate, Kunoichi au masque.
  - Guerrier onmyōji (sceaux en zone) : Maître des sceaux, Invocateur de shikigami.
  - Lancier sōhei (longue allonge) : Sōhei, Naginata lourde.
  - Chevalier français (anti-boss) : Paladin, Chevalier à la lance.
  - Mousquetaire (tir lourd) : Mousquetaire du roi, Bretteur.
  - Courtisane (repousse les Oni) : Danseuse à l'éventail, Oiran.
  - Condottiere (butin sur chaque Oni achevé) : Capitaine mercenaire, Lansquenet.
  - Troubadour (renforce les alliés) : Ménestrel, Barde de guerre.
- **Nouvelles capacités** : toucher les spectres, poison, percer l'armure, bonus contre les boss, repousser les Oni, butin, pièces gagnées par le charme, chant qui augmente les dégâts ou la cadence des alliés proches.
- **Deuxième carte du pays, « Au-delà de la Porte »**, débloquée en scellant la Porte des Oni. Elle compte 10 nouveaux niveaux de 20 vagues : jardin des glycines, théiers d'Uji, gorges de Kiso, château de Himeji, sources de Hakone, forêt des kodama, dunes de Tottori, glaces d'Ezo, mont Osore et Yomi.
- **Nouveau boss final** : Sōjōbō, roi des tengu (niveau 20). Il vole, se régénère et appelle des corbeaux.
- **Livre des Oni** : une page par Oni et par boss, avec ses statistiques, ses capacités, son niveau de première apparition et des conseils pour le battre. Les Oni pas encore rencontrés restent en silhouette.
- **Sons d'interface** sur les boutons des menus (pack SoundWeaver, licence MIT).
- Outil `tools/sprites/build2.py` pour découper la deuxième planche de personnages.

### Modifié

- **Menu principal refait** : boutons disposés comme dans un jeu de tower defense mobile (gros bouton « Jouer » au centre, raccourcis dans les coins), en laque, feuille d'or et sceaux.
- Ura, roi des Oni, devient le boss du niveau 15. Les sauvegardes existantes débloquent dans le livre les Oni des niveaux déjà gagnés.
- Le compteur d'étoiles et la progression de l'écran titre tiennent compte des 20 niveaux.

## 1.0.0

- Carte du pays illustrée en pixel art pour choisir les niveaux.
- 20 vagues par niveau, mode infini après la 20e vague et raretés des personnages.
- Version à 10 personnages avec 2 voies d'évolution chacun, et publication sur GitHub Pages.
- Première version du jeu, d'abord appelée « Kimon · La Porte des Oni ».
