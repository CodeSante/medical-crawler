# Medical Crawler

Medical Crawler is a web crawler project, specially designed for french medical websites. Currently, it is tested exclusively on the vidal.fr website. The project is developed with the Scrapy framework and uses a PostgreSQL database. The crawler is able to collect various information about web pages, including URLs, titles, descriptions and specific text elements. It uses filtering mechanisms to exclude irrelevant sites from the crawl.

Medical Crawler's search functionality is based on a keyword-based approach, incorporating a spell-checking feature using the medical-wordlist project. This allows for accurate matching and retrieval of relevant medical content during the crawling process.

In the future, the project aims to expand its reach and add a total of 320 medical websites to its crawling capabilities. This will allow the search engine to provide comprehensive medical information from a wide range of trusted sources. Please note that the project is currently under development.

## Prerequisites

Before starting the project, make sure you have the following components installed:

- Python 3.x
- PostgreSQL
- pyenv

### Install

```bash
pip3 install scrapy
pip3 install beautifulsoup4
pip3 install unidecode
pip3 install psycopg2
pip3 install flask
bash install.sh
sudo bash scripts/install-db.sh
```

## Usage

```bash
python3 -m scrapy runspider main.py
```
