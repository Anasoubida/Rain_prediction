# Prévision des précipitations à New Delhi

L'objectif de ce projet est de prévoir s'il y aura des précipitations à New Delhi à partir de cinq paramètres : 

* Dew point (Température de rosée)
* Humidity (Humidité)
* Month (Mois)
* Pressure (Pression)
* Temperature (Température)
* Wind speed (La vitesse du vent)

J'ai fait de l'analyse de données pour comprendre le dataset, l'apprentissage et j'ai enregistré le meilleur modele, vous trouverez toutes 
ces informations dans ce [notebook](https://github.com/Anasoubida/Rain_prediction/blob/master/notebook.ipynb)

J'ai crée aussi un api avec Fastapi qui wrap le modèle de ML, je l'ai mis dans un docker container, et j'ai tout déployé dans un EC2 instance sur AWS.

## Description du dataset :

* Dew point : Le point de rosée ou température de rosée est la température sous laquelle la rosée se dépose naturellement.
* fog : brouillard.
* hail : grêle.
* Heat index : L'indice de chaleur est la température apparente qui tient compte à la fois la température et l'humidité relative.
* hum : humidité.
* thunder : tonnerre.
* vism : la visibilité est la distance horizontale maximale observée.
* wdird : direction du vent en degrés.
* wdire : direction du vent.
* wspdm : vitesse du vent en mile/h .
* tempm : temperature en °C.
* pressurem : pression en hpa.
* hum : humidité en %
* rain : precipitations (1=Oui, 0=Non)


**Difference entre frog (brouillard), mist (la brume), haze (la brume sèche)**

* Le frog (brouillard), mist (la brume) sont produits par l'eau, il s'agit de la suspension dans l'atmosphère de très petites gouttelettes d'eau réduisant la visibilité au sol.

* On parle de mist (brume) lorsque la visibilité est comprise entre 1 et 5 kilomètres, de frog (brouillard) lorsqu'elle est inférieure à 1 kilomètre.

* Toutefois le haze (la brume sèche) est causée par des particules sèches comme la poussière ou la fumée, non de gouttelettes d'eau.

* NB : Ces définitions s'appuie sur les ressources ci-dessous :

	[lien](https://www.metoffice.gov.uk/weather/learn-about/weather/types-of-weather/fog/difference-mist-and-fog)
	
	[lien](https://www.lavionnaire.fr/MeteoBrouillard.php)


# Code

## Presentation des scripts

Vous trouverez dans [notebook](https://github.com/Anasoubida/Rain_prediction/blob/master/notebook.ipynb) la partie EDA, training et saving du modele de ML. 

Le script [rain_app.py](https://github.com/Anasoubida/Rain_prediction/blob/master/rain_app.py) contient le code de l'api. Cet API est composé de trois endpoints : 
* predict_rain : qui permet de faire de la prévision des précipitations en renseignant les diffirents champs nécessaires (Cet endpoint ne pourra pas recevoir de post requests ayant un body)
* predict_rain_body : permet de recevoir un post request à partir d'un script python comme [send_request.py]()
* predict_rain_file : permet de recevoir un fichier csv et va retourner les prévisions en format json

[send_request.py](https://github.com/Anasoubida/Rain_prediction/blob/master/send_request.py) permet d'envoyer des requêtes à l'API.

## Faire tourner l'API en local

### 1) installer les librairies necessaires : 

```bash
pip install pipenv
```

```bash
pipenv install
```

### 2) Lancer l'API en local

```bash
uvicorn rain_app:app --reload
```

Et après il va falloir taper cette adresse : http://127.0.0.1:8000/docs

Vous pouvez aussi envoyer des requetes à l'aide du script [send_request.py](https://github.com/Anasoubida/Rain_prediction/blob/master/send_request.py)

## Deployer avec docker

### 1) Construction du docker container

```bash
docker build -t rain_app .
```

### 2) Lancement du docker container en local

```bash
docker run -p 8000:8000 rain_app
```

Et après il va falloir taper cette adresse : http://localhost:8000/docs

Vous pouvez aussi envoyer des requetes à l'aide du script [send_request.py](https://github.com/Anasoubida/Rain_prediction/blob/master/send_request.py)

### 3) deploiement avec une instance ec2 sur aws

#### 1) il faudra lancer une instance ec2 

*Dans ce tuto j'utilise une instance avec ubuntu*
* Pensez bien à créer la paire de clés pour pouvoir se connecer en ssh au serveur (de préférence en format .ppk)

#### 2) Installer putty pour se connecter en ssh

#### 3) se connecter à ec2 instance avec putty

* Ouvrir putty et rensigner le host name (il s'agit de l'Adresse IPv4 publique)
* Uploader la pari key dans putty (aller sur ssh ==> Auth ==> Credentials)
* Allez dans putty sur connection ==> data ==> rensigner Auto-login username

#### 4) Setup l'environnement sur ubuntu

```bash
sudo apt-get update
```

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

```bash
apt-cache madison docker-ce
```
```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io
```
```bash
sudo apt install docker.io
```
```bash
sudo usermod -aG docker <username>
```

Se deconnecter et puis se reconnecter à l'ec2 instance

#### 6) Installation/setup de nginx

* Pour installer nginx: 

```bash
sudo apt install nginx
```

* Après il faudra créer un fichier pour le setup de nginx

```bash
sudo vi /etc/nginx/sites-enabled/fastapi-demo
```

La commande ci-dessus va créer un fichier fastapi-demo dans lequel on va coller cela (en remplaçant PUBLIC_IP par l'Adresse IPv4 publique) : 

server {
    listen 80;
    server_name <PUBLIC_IP>;
    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}

#### 5) Build and run the docker container

docker build -t rain_app .
docker run -p 8000:8000 rain_app


#### 6) Accéder à l'API 

On pourra accéder à l'API en copiant et collant l'Adresse IPv4 publique de l'instance ec2 en collant à coté le port 8000, exemple :
http://0.0.0.0:8000
