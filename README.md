# Medical Crawler

Medical Crawler is a web crawler project, specially designed for french medical websites. Currently, it is tested exclusively on the vidal.fr website. The project is developed with the Scrapy framework and uses a PostgreSQL database. The crawler is able to collect various information about web pages, including URLs, titles, descriptions and specific text elements. It uses filtering mechanisms to exclude irrelevant sites from the crawl.

Medical Crawler's search functionality is based on a keyword-based approach, incorporating a spell-checking feature using the [medical-wordlist](https://github.com/CodeSante/medical-wordlist) project. This allows for accurate matching and retrieval of relevant medical content during the crawling process.

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

### Backup

Create a backup from database :

```bash
sudo -u postgres pg_dump -U crawler -h localhost -p 5432 -d medical_crawler -F c > backup
```

Restore a backup :

```bash
sudo -u postgres pg_restore -U crawler -h localhost -p 5432 -d medical_crawler -F c backup
```
Default password is *bG9jYWxob3N0*

## Demo

```bash
python3 api.py
```

At _http://127.0.0.1:5000/urls_

```
  {
    "dom": [
      [
        "title",
        {
          "phytotherapie": 1
        }
      ],
      [
        "h1",
        {
          "phytotherapie": 1
        }
      ],
      [
        "p",
        {
          "patient": 1
        }
      ],
      [
        "p",
        {
          "plante": 1
        },
        {
          "qui": 1
        }
      ],
      [
        "p",
        {
          "cholesterol": 1,
          "diarrhees": 1
        }
      ],
      [
        "p",
        {
          "cholesterol": 2
        },
        {
          "qui": 1
        }
      ],
      [
        "p",
        {
          "diarrhees": 1
        },
        {
          "qui": 1
        }
      ],
      [
        "p",
        {
          "maladie": 2
        },
        {
          "qui": 1
        }
      ]
    ],
    "url": "https://www.vidal.fr/parapharmacie/phytotherapie-plantes/germe-ble-triticum-vulgaris.html"
  },
  {
    "dom": [
      [
        "description",
        {
          "constipation": 1,
          "phytotherapie": 1
        }
      ],
      [
        "title",
        {
          "phytotherapie": 1
        }
      ],
      [
        "h1",
        {
          "phytotherapie": 1
        }
      ],
      [
        "p",
        {
          "patient": 1
        }
      ],
      [
        "p",
        {
          "bile": 1,
          "constipation": 1,
          "foie": 1,
          "medicaments": 1,
          "phytotherapie": 1
        }
      ],
      [
        "p",
        {
          "bile": 1,
          "foie": 1,
          "maladie": 1,
          "phytotherapie": 1,
          "plante": 1
        }
      ],
      [
        "p",
        {
          "medicaments": 1
        },
        {
          "qui": 1
        }
      ],
      [
        "p",
        {
          "bile": 1
        }
      ],
      [
        "p",
        {
          "gastro": 1
        }
      ],
      [
        "p",
        {
          "gastro": 1
        }
      ],
      [
        "p",
        {
          "foie": 1,
          "phytotherapie": 1,
          "vesicule": 1
        }
      ],
      [
        "p",
        {
          "foie": 1,
          "maladie": 1,
          "medecin": 1,
          "plante": 1
        },
        {
          "qui": 3
        }
      ],
      [
        "p",
        {
          "anticoagulants": 1,
          "medicaments": 1,
          "sang": 1,
          "warfarine": 1
        }
      ],
      [
        "p",
        {
          "constipation": 2,
          "phytotherapie": 1
        },
        {
          "qui": 1
        }
      ]
    ],
    "url": "https://www.vidal.fr/parapharmacie/phytotherapie-plantes/boldo-peumus-boldus.html"
  },
```

At _http://127.0.0.1:5000/urls/without-dom_ you can display all crawled URLs.
