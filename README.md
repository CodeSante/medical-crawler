# Medical Crawler

Medical Crawler est un projet de crawl de sites web médicaux, développé en utilisant le framework Scrapy et la base de données PostgreSQL. Il permet de collecter des informations à partir des pages web, telles que les URL, les titres, les descriptions et les éléments de texte spécifiques, tout en filtrant les sites non pertinents.

## Prérequis

Avant de démarrer le projet, assurez-vous d'avoir les éléments suivants installés :

- Python 3.x
- PostgreSQL
- Scrapy
- BeautifulSoup
- unidecode

Il faut lancer _install.sh_ pour télécharger les mots-clefs et lancer le script _scripts/install-db.sh_ pour installer la BDD.

## Utilisation

```bash
python3 -m scrapy runspider main.py
```