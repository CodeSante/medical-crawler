# Medical Crawler

Medical Crawler is a web crawling project specifically designed for medical websites. It is developed using the Scrapy framework and utilizes a PostgreSQL database. The crawler is capable of gathering various information from web pages, including URLs, titles, descriptions, and specific text elements. It employs filtering mechanisms to exclude irrelevant sites from the crawl.

The search functionality of Medical Crawler relies on a keyword-based approach, incorporating a spell checking feature using the "medical-wordlist" project. This enables accurate matching and retrieval of relevant medical content during the crawling process.

## Prerequisites

Before starting the project, make sure you have the following components installed:

- Python 3.x
- PostgreSQL
- Scrapy
- BeautifulSoup
- unidecode

You need to run the _install.sh_ script to download the keywords and execute the _scripts/install-db.sh_ script to install the database.

## Usage

```bash
python3 -m scrapy runspider main.py
```
