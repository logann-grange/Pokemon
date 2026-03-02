# Pokémon Projet

Un jeu vidéo Pokémon développé en Python avec Pygame, inspiré des jeux classiques de la franchise. Le projet propose une aventure complète : exploration, combats, gestion d’équipe, Pokédex, évolutions, et bien plus !

## Fonctionnalités principales
- **Menu principal interactif** : Jouer, charger une partie, options audio, quitter.
- **Exploration de la carte** : Déplacement du joueur sur différentes maps (village, forêt, labo, etc.).
- **Combats Pokémon** : Système de combat au tour par tour avec gestion des types, attaques, PV, XP, etc.
- **Gestion d’équipe** : Ajout, suppression, évolution et sauvegarde des Pokémon de l’équipe.
- **Pokédex** : Consultation des Pokémon rencontrés/capturés, recherche et affichage détaillé.
- **Système d’évolution** : Animation et logique d’évolution des Pokémon.
- **Sauvegarde/Chargement** : Sauvegarde automatique et manuelle de la progression.
- **Options audio** : Réglage du volume de la musique et des effets sonores.
- **Interface graphique complète** : Menus, boutons, animations, effets visuels et sonores.

## Système de combat
Le jeu propose un système de combat au tour par tour inspiré des jeux Pokémon classiques :
- **Déroulement** : Chaque Pokémon attaque à son tour. Les dégâts, la précision et l’efficacité dépendent du type et des statistiques.
- **Types et efficacité** : Les attaques tiennent compte des types (eau, feu, plante, etc.) et appliquent des multiplicateurs d’efficacité (super efficace, peu efficace, etc.).
- **Gestion des PV** : Les PV sont mis à jour en temps réel, avec affichage graphique de la barre de vie.
- **Capture** : Il est possible de capturer des Pokémon sauvages et de les ajouter à l’équipe si une place est disponible.
- **Gain d’expérience** : Après chaque victoire, le Pokémon ayant combattu gagne de l’XP.

## Système de niveau et montée de niveau (XP / Level Up)
- **Gain d’XP** : Un Pokémon gagne de l’expérience (XP) après chaque combat remporté. Le gain dépend du niveau de l’adversaire.
- **Montée de niveau** : Quand l’XP atteint un certain seuil ($XP \geq 1000 \times \text{niveau} \times 0.5$), le Pokémon monte d’un niveau :
    - Son niveau augmente de 1
    - Ses statistiques (PV, attaque, défense) sont recalculées
    - Il peut évoluer si les conditions sont réunies (ex : tous les 25 niveaux)
- **Calcul des statistiques** :
    - PV : $PV = \left\lfloor \frac{HP_{base} \times 2 \times \text{niveau}}{100} \right\rfloor + 10 + \text{niveau}$
    - Attaque : $Attaque = \left\lfloor \frac{Attaque_{base} \times 2 \times \text{niveau}}{100} \right\rfloor + 5$
    - Défense : $Défense = \left\lfloor \frac{Défense_{base} \times 2 \times \text{niveau}}{100} \right\rfloor + 5$
- **Évolution** : Certains Pokémon évoluent automatiquement tous les 25 niveaux si une évolution est définie.

Ces systèmes rendent la progression fidèle à l’expérience Pokémon tout en étant adaptés à ce projet Python.

## Installation
1. **Prérequis** :
   - Python 3.8 ou supérieur
   - [Pygame](https://www.pygame.org/) (`pip install pygame`)
   - [Pillow](https://pypi.org/project/Pillow/) (`pip install pillow`)

2. **Cloner le projet** :
   ```bash
   git clone https://github.com/logann-grange/Pokemon/tree/master
   cd Pokemon_projet
   ```

3. **Lancer le jeu** :
   ```bash
   python main.py
   ```

## Organisation des dossiers
```
Pokemon_projet/
│   main.py                # Point d'entrée du jeu
│   options.json           # Options audio globales
│
├── Asset/                 # Ressources graphiques et sonores
│   ├── menue/             # Images et sons des menus
│   ├── front/             # Images diverses
│   ├── image/             # Images de la carte et du Pokédex
│   ├── map/               # Fichiers .tmx et tilesets
│   └── sons/              # Musiques et effets sonores
│
├── combat/                # Modules liés aux combats
│   ├── graphic/           # Interface graphique de combat
│   └── logic/             # Logique des combats
│
├── data/                  # Données sauvegardées (équipe, options, pokédex, sauvegarde)
│
├── evolution/             # Système d’évolution (graphique et logique)
│
├── game/                  # Logique principale du jeu
│   ├── graphic/           # Affichage, animations, gestion écran
│   └── logic/             # Entités, maps, sauvegarde, etc.
│
├── menue/                 # Menus principaux et options
│   ├── events/            # Gestion des événements des menus
│   ├── graphic/           # Rendu graphique des menus
│   └── options.json       # Options spécifiques aux menus
│
├── Pokedex/               # Modules du Pokédex (logique et interface)
│
└── README.md              # Ce fichier
```

## Utilisation
- **Lancer le jeu** : `python main.py`
- **Naviguer dans les menus** avec la souris.
- **Déplacer le joueur** : ZQSD (ou flèches selon config)
- **Ouvrir le Pokédex** : touche `P` en jeu
- **Accéder au PC** : touche `F` en jeu
- **Sauvegarder** : automatique ou via menu

## Dépendances
- Python 3.8+
- pygame
- pillow

## Crédits
- Développement : Mohamed Mahamoud, Logann Grange , Clément Koch
- Ressources graphiques et sonores : voir dossier Asset/
- Basé sur l’univers Pokémon (© Nintendo/Game Freak)

---
Projet réalisé à but éducatif, non commercial.
