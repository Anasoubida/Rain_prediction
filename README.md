# Prévision des précipitations à New Delhi

L'objectif de ce projet est de prévoir s'il y aura des précipitations à New Delhi à partir de cinq paramètres : 

* Dew point (Température de rosée)
* Humidity (Humidité)
* Month (Mois)
* Pressure (Pression)
* Temperature (Température)
* Wind speed (La vitesse du vent)

J'ai fait de l'analyse de données pour comprendre le dataset, l'apprentissage et j'ai enregistré le meilleur modele, vous trouverez toutes 
ces informations dans ce [notebook]()

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
* rain : precipitations en %

**Précipitations en %**
PP = C x A 

"PP" étant le pourcentage de précipitation.
"C" la confiance que les météorologues ont sur le fait que la pluie va tomber quelque part sur une région géographique donnée.
"A" le pourcentage de zone de cette région qui recevra cette pluie si elle tombe

**Exemple:**

Demain il y aura 60% de risque de pluie en Gironde, cela veut dire qu'il y a 100% de chance qu'il pleuve sur 60% du territoire et pas 60% de chance qu'il pleuve sur l'ensemble de ce même territoire.
En gros, s'il pleut, ça sera sur 60% de la région.

**Difference entre frog (brouillard), mist (la brume), haze (la brume sèche)**

* Le frog (brouillard), mist (la brume) sont produits par l'eau, il s'agit de la suspension dans l'atmosphère de très petites gouttelettes d'eau réduisant la visibilité au sol.

* On parle de mist (brume) lorsque la visibilité est comprise entre 1 et 5 kilomètres, de frog (brouillard) lorsqu'elle est inférieure à 1 kilomètre.

* Toutefois le haze (la brume sèche) est causée par des particules sèches comme la poussière ou la fumée, non de gouttelettes d'eau.

* NB : Ces définitions s'appuie sur les ressources ci-dessous :

	[lien](https://www.metoffice.gov.uk/weather/learn-about/weather/types-of-weather/fog/difference-mist-and-fog)
	
	[lien](https://www.lavionnaire.fr/MeteoBrouillard.php)


# Code

## Presentation des scripts

Vous trouverez dans [notebook]() la partie EDA, training et saving du modele de ML. 

Le script [rain_app.py]() contient le code de l'api. Cet API est composé de trois endpoints : 
* predict_rain : qui permet de faire de la prévision des précipitations en renseignant les diffirents champs nécessaires (Cet endpoint ne pourra pas recevoir de post requests ayant un body)
* predict_rain_body : permet de recevoir un post request à partir d'un script python comme [send_request.py]()
* predict_rain_file : permet de recevoir un fichier csv et va retourner les prévisions en format json

[send_request.py]() permet d'envoyer des requêtes à l'API.

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

Vous pouvez aussi envoyer des requetes à l'aide du script [send_request.py]()

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

Vous pouvez aussi envoyer des requetes à l'aide du script [send_request.py]()



cd C:\CDI\bioceanor\test_technique\test_technique_anas_oubida
docker build -t rain_app .
docker run -p 8000:8000 rain_app