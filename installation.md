## Installation et Déploiement Local

### Cloner le repository :
```bash
git clone <url-du-repo>
cd <dossier-du-repo> 
```
### Créer un environnement virtuel :
```bash python -m venv venv ```
# Sur Unix/Mac
```bash source venv/bin/activate ```
# Sur Windows
```bash venv\Scripts\activate ```

### Installer les dépendances :
```bash pip install -r app/requirements.txt ```
- Lancer l'application localement :
```bash  python app/app.py ```
- Accéder à http://localhost:8050 dans un navigateur.

### Déploiement Docker et AWS
Construire l'image Docker :
```bash docker build -t docker-tba_2024trim2 .```
Pousser sur Docker Hub :
```bash ```
``` docker tag docker-tba_2024trim2 adigeo/docker-tba_2024trim2 ```
``` docker push adigeo/docker-tba_2024trim2  ```

- Déployer sur AWS :

### Connectez-vous au compte AGETIPA sur AWS.
- Mettez à jour l'instance Nano en modifiant le déploiement pour utiliser le nouveau repository adigeo/docker-tba_2024trim2.
- Accéder au dashboard déployé via l'IP statique sur le port 8050.
- Utiliser les mots de passe fournis.
