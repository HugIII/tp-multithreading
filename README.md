## Projet

Ce projet a été réalisé dans le cadre d’un TP sur le multiprocessing en 3ᵉ année du cursus SRI à l’école d’ingénieurs UPSSITECH.
L’objectif est d’explorer différents aspects du multiprocessing en développant un système de type Master-Slave. Dans ce système, les Masters (implémentés dans le script `Boss.py`) génèrent des tâches à réaliser, tandis que les Slaves (scripts `Minions.py` et programme `low_level.cpp`) exécutent ces tâches et renvoient les résultats.
La communication entre les composants repose sur deux queues partagées : l’une pour stocker les tâches en attente et l’autre pour conserver les résultats obtenus. Ces mémoires partagées sont administrées par un gestionnaire, le `QueueManager` (script `manager.py`). Enfin, le script `proxy.py` permet de faire tampon entre le QueueManager et le Minion en C++ (`low_level.cpp`).

## Dépendences
### Librairies Python nécessaires
Les librairies suivantes sont requises :
- `numpy`
- `json`
- `multiprocessing`

Ces dépendances sont listées dans le fichier `requirements.txt` à la racine du projet. Pour les installer, utilisez la commande suivante :
```bash
pip install -r requirements.txt
```

### Librairies C++ nécessaires
Les librairies suivantes sont requises :
- `cpr`
- `cmake`
- `eigen`
- `nlohmann::json`

### Compilation
Pour compiler le code C++ vous devez utiliser les commandes suivantes:
```bash
# configure
cmake -B build -S .
# compile
cmake --build build
# run
./build/low_level
```

## Lancement
### Cas executant en Python
Pour exécuter le cas en Python, suivez les étapes ci-dessous :

1. Premier terminal
   Lancez le script `manager.py` dans un terminal. Ce script gère la coordination globale des tâches.
   ```bash
   python manager.py
   ```

2. Deuxième terminal
   Lancez le script `Boss.py`, qui supervise les tâches assignées aux Minions.
   ```bash
   python Boss.py
   ```

3. Troisième terminal et suivants
   Lancez autant d'instances du script `Minion.py` que souhaité pour effectuer les tâches en parallèle. Chaque Minion exécute une partie des calculs.
   ```bash
   python Minion.py
   ```

### Cas executant en C++
Pour exécuter le cas en C++, suivez les étapes ci-dessous :

1. Premier terminal
   Lancez le script `manager.py` dans un terminal. Ce script gère la coordination globale des tâches.
   ```bash
   python manager.py
   ```

2. Deuxième terminal
   Lancez le script `proxy.py`, qui lance le server pour pouvoir acceder aux queue du QueueManager.
   ```bash
   python proxy.py
   ```

3. Troisième terminal
   Lancez le script `Boss.py`, qui supervise les tâches assignées aux Minions.
   ```bash
   python Boss.py
   ```

4. Quatrième terminal
   Lancez le script `low_level.cpp` dans un terminal. Ce script permet d'effectuer les tâches en parralèlle.
   cf partie [Compilation](#compilation)


## Resultats
Pour comparer les performances des différents implémentations (Python et C++), nous avons fixé plusieurs paramètres dans notre code.

### Paramètres communs
- Taille des matrices : 3000 x 3000.
- Nombre de tâches : 10 par batch de test.

### Résultats obtenus
- Python : Le temps total d'exécution est de 56 secondes.
- C++:
  - En mode Debug, le temps total est de 116 secondes.
  - En mode Release, ce temps diminue à 105 secondes.

### Optimisation des structures de données
Au départ, les résultats étaient stockés dans des matrices `MatrixXd`, privilégiant une haute précision des calculs. Cependant, dans notre cas, une telle précision n’était pas nécessaire, et les priorités étaient la vitesse et la mémoire. Nous avons donc opté pour `MatrixXf`, une structure de données moins gourmande.

Impact du changement :
- Une tâche initialement réalisée en 5 secondes a vu son temps réduit à 2 secondes, ce qui a permis d'améliorer considérablement les performances.

### Optimisation des fonctions de résolution (solve)
En mode Release, nous avons également testé différentes fonctions de résolution bas niveau :
- `ColPivHouseholderQR` : 105 secondes.
- `PartialPivLU` : 25 secondes.
- `HouseholderQR` : 12 secondes.

Les choix des structures de données et des fonctions de résolution jouent un rôle essentiel dans les performances. L’adoption de `MatrixXf` et l’utilisation de `HouseholderQR` en mode Release offrent les meilleures performances, mettant en évidence l'importance de combiner la précision requise avec des solutions adaptées aux contraintes de temps et de mémoire.


### Analyse des résultats

En examinant les résultats, on constate que le C++ est plus rapide, à condition d’être bien optimisé et de faire appel aux fonctions appropriées. On peut alors se demander comment Python parvient à offrir une telle rapidité malgré la complexité des calculs nécessaires. La réponse réside dans l'utilisation de la bibliothèque NumPy. Cette dernière, écrite en C et Fortran, est enveloppée par Python, ce qui lui permet de rivaliser en performances avec Eigen en C++.
