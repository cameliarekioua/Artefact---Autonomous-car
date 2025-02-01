SUIVI DU PROJET DU GROUPE 32



Commande de connexion à RP : ssh MMCM@32.local
(username: MMCM; hostname: 32)


Clé publique ssh de la carte Raspberry Pi:
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDIg5fgo+naSIED4B+V4XRfmCcXk1I2WLpqvzFEVamoMHz0CSxwcQnzpy6Lap9zKDCRAAfc50Z4cjzEKtE7fAdYgVVc9IUPBOuE3ISIxQ2xbanUr/8qKZdewc+5KBBP39bSYBCkd4DIG7wZv7JBRSyGhqMw73JTfEXub+Y1EDkWjfH9TMmYvf2HT0uSHxGkzn9fMlNW7Crod0TYOHbMDiiCohM0e39FYdcnELtkMVKxhMHFsiqoWWXQrLm5xGQFUtawxCah7qBOKzkXKZctV9yrgVKdrCoUO5zVzTjWDY1nFg/wCA24CUuqFWrCzq4Yj2kc5WRuJP4gEDvKGkeFMZsK5AlaJEMkNeESkt3wkQ6rypfgf3BbaHxRcwCle4ZXpOHsudJ2kh2gAf3WOLQlF/26m/rtz1xEyDA4fVtqG+SIH6970N+kY4eIohhOzrP89ac2E6LqEcks+VfUIGDO34DJxbSQyTX/DjQepRjQVwfnGmKRJObO2RmMGBuJLbZ+gGc= milan@LAPTOP-38BK0S88





//Dites carotte à Milan si vous voyez ce message sur le Git !



Liste des tâches à faire: {responsable}

- {Máel} Contrôle des moteurs (automatisation, programmation de la carte Raspberry Pi)
- {Camelia} Interface web simplifiée
- {Milan} Mini serveur web permettant le contrôle manuel de votre robot
- {Mathis} Dialogue avec le serveur web de suivi de déplacement 6
- {Camelia} Fabrication du robot (découpe de la plaque, assemblage, design)
- {Máel} Reconnaissance des codes ArUco 4 via la caméra, évaluation de la distance
- Autres ?

---------------------------------------------------------------------------------------------------------
Commande utile:
* Connexion à la raspberry : Se connecter à Campus-telecom, commande : ssh MMCM@robotpi-32.enst.fr
* Copier un fichier vers la raspbbery : scp chemin/file.extension MMCM@robotpi-32.enst.fr:~/
---------------------------------------------------------------------------------------------------------


Première séance (20/09):
Présentation du projet, découverte des différents composants, ordonnancement des premières tâches à effectuer.

Deuxième séance (23/09):
Installation de l'OS sur la carte Raspberry Pi, et connexion des 3 membres qui possèdent un ordianteur portable.
Premières recherches dans la documentation du forum, échanges sur la connexion à la carte Arduino depuis un ordinateur depuis Windows.
Début de l'écriture de la documentation du groupe (que vous êtes en train de lire).
Prise en main de Gitlab par les membres.
Assignation de responsables aux différentes tâches principales.

Troisième séance (27/09):
Connexion de la carte Raspberry au réseau Wifi Campus-Telecom.
Réglage de l'heure de la carte à celle de Paris.
Prise de décisions quant à la forme générale du robot.
Visite du FabLab par Camelia et Milan.
Début du dessin pour la découpe de la plaque en bois, avec le logiciel Inkscape, en .svg.
Point relations inter-équipe avec le responsable SES de notre groupe.
Organisation du travail jusqu'à la prochaine séance (dans plus d'une semaine) et dessin d'un graphe récapitulatif des différentes grandes tâches du projet.












Note sur les composantes du robot:
- Batterie: ne pas la laisser branchée si elle est pleine; elle alimente la carte RP et les moteurs