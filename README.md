# Medical Crawler

Medical Crawler is a web crawling project specifically designed for medical websites. It is developed using the Scrapy framework and utilizes a PostgreSQL database. The crawler is capable of gathering various information from web pages, including URLs, titles, descriptions, and specific text elements. It employs filtering mechanisms to exclude irrelevant sites from the crawl.

The search functionality of Medical Crawler relies on a keyword-based approach, incorporating a spell-checking feature using the "medical-wordlist" project. This enables accurate matching and retrieval of relevant medical content during the crawling process.

The crawling is specifically targeted towards French websites, with the intention of creating a search engine for medical information in the field of medicine in the French language.

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
