## Projet

Ce projet a été réalisé dans le cadre du TP de multi-threading en 3ème année en SRI à l'école d'ingénieur UPSSITECH.
Le but de ce TP est de montrer différent aspect du multi-threading.
Pour cela, nous allons réaliser un système Master-Slave.
Les Masters (Boss.py) vont créer des tâches et les Slaves (Minions.py et low_level.cpp) vont résoudre les tâches et transmettre le résultat.
Les deux composants auront deux Queues partagés une avec les tâches à réaliser et une autre avec les tâches réalisés.
Ces mémoires partagées vont être par géré par le QueueManager (manager.py).
Tandis que le proxy.py va permettre de faire tampon entre le QueueManager et le minion C++ (low_level.cpp).

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
Lancer un premier terminal pour executer manager.py
Un deuxieme terminal executant Boss.py
Autant de Minion.py souhaités pour effectuer les tâches en parrallèle.

### Cas executant en C++
Lancer un premier terminal pour executer manager.py
Un deuxieme terminal executant Boss.py
Autant de Minion.py souhaités pour effectuer les tâches en parrallèle.

### Resultats
Pour pouvoir comparer les résultats des différents mignons (python et C++) nous fixer les différentes options de notre code.
Pour la taille des matrices nous avons décidé de mettre 3000 et nous avons décidé de créer 10 tâches par batch de test.

Pour le Python nous avons un temps total de 56 secondes.

Pour le C++, si notre code est compilé en mode debug nous avons un temps total de 116 secondes.

Si le code est compilé en mode release nous tombons à 105 secondes.
Nous avons aussi décidé de tester avec différentes fonctions de solve dans low level en mode release.
Donc avec ColPivHouseholderQR on obtient 105 secondes.
Avec la fonction partialPivLu on obtient 25 secondes.
Et pour finir avec la fonction householderQr on obtient 12 secondes.


### Analyse des résultats

En analysant, les résultats on peut voir que le C++ est plus rapide mais que lorsqu'il est bien optimisé et que les bonnes fonctions sont utilisés. On peut se demander comment le python peut être si rapide alors que le calcul demande beaucoup d'opération, pour solve le problème on utilise la librarie python numpy. Cette librarie est codé en C et en Fortran et est wrappé par le python ce qui explique comment cette librarie rivalise avec Eigen en C++.
