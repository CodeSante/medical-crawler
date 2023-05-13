import time
from bs4 import BeautifulSoup
import scrapy
from unidecode import unidecode
from urllib.parse import urlparse
import psycopg2
import json
import signal

allowed_urls = [
    "vidal.fr"
]

blacklist_keywords = [
    "forum"
]

# Database
db_host = "localhost"
db_port = "5432"
db_name = "medical_crawler"
db_user = "crawler"
db_password = "bG9jYWxob3N0"
conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
cur = conn.cursor()

def handle_signal(self, signum, frame):
    cur.close()
    conn.close()

# Signals
signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)

class MySpider(scrapy.Spider):
    name = "Robot Code Sante - BETA"
    custom_settings = {
        'CONCURRENT_REQUESTS': 10,  # Limite le nombre de requêtes simultanées à 10
        'DOWNLOAD_DELAY': 0.5,  # Délai d'attente de 0.5 seconde entre chaque requête
        'AUTOTHROTTLE_START_DELAY': 0.5,  # Délai initial d'attente de 0.5 seconde
        'HTTPCACHE_ENABLED': True,  # Active la mise en cache des réponses HTTP
        'HTTPCACHE_EXPIRATION_SECS': 86400,  # Expiration du cache après 24 heures (en secondes)
        'HTTPCACHE_DIR': 'httpcache',  # Répertoire de stockage du cache
        'HTTPCACHE_IGNORE_HTTP_CODES': [301, 302, 403, 404, 503],  # Codes HTTP à ignorer dans le cache
        'DEPTH_LIMIT': 3,  # Limite de profondeur de crawl
        'DEPTH_PRIORITY': 1,  # Priorité de profondeur (1 pour le crawl en largeur)
        'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',  # File d'attente disque pour les requêtes
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',  # File d'attente mémoire pour les requêtes
        'MEDIA_ALLOW_REDIRECTS': False,  # Désactiver les redirections pour les médias
        'MEDIA_PIPELINE': None,  # Désactiver le pipeline de traitement des médias
        'RETRY_TIMES': 3,  # Nombre de tentatives de rééssayage des requêtes en échec
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 408]
    }
    start_urls = [
            "https://www.vidal.fr/"
    ]
    visited_urls = []
    visited_urls_limit = 20000

    def __init__(self):

        self.keywords = set()
        with open("keywords.txt") as f:
            for line in f:
                self.keywords.add(self.clean_string(line.strip()))
        self.interrogative_adverbs = set()
        with open("interrogative_adverbs.txt") as f:
            for line in f:
                self.interrogative_adverbs.add(self.clean_string(line.strip()))

    def match_patterns(self, patterns, text):
        for pattern in patterns:
            if pattern in text:
                return True
        return False

    def is_french_website(self, url):
        parsed_url = urlparse(url)
        return parsed_url.netloc.endswith(".fr")
    
    def get_text_dom(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        elements = []
        meta_description = soup.find('meta', attrs={'name': 'description'})
        if meta_description:
            description = meta_description.get('content')
            elements.append(('description', description.strip()))
        
        for element in soup.recursiveChildGenerator():
            if element.name in ['title', 'h1', 'h2', 'p']:
                elements.append((element.name, element.text.strip()))
            elif element.name == 'img' or element.name == 'video':
                #alt_text = element.get('alt', '')
                src_text = element.get('src', '')
                if not src_text.startswith('data:'):
                    elements.append((element.name, src_text))
                    #, alt_text.strip()
        
        return elements

    def parse(self, response):

        # Check if visited URLs limit exceeded
        if len(self.visited_urls) > self.visited_urls_limit:
            self.visited_urls = []

        # Verify is not visited and is french website
        if response.url in self.visited_urls or not self.is_french_website(response.url):
            self.visited_urls.append(response.url)
            return
        
        # Add visited url
        self.visited_urls.append(response.url)

        # Header
        headers = {
            'User-Agent': 'Robot Code Sante - BETA (Linux; Ubuntu 22.04)',
            'Accept-Language': 'fr-FR'
        }

        # Get HTML
        html = response.body
        text_dom = self.get_text_dom(html)

        title = response.css("title::text").extract_first()
        title_ascii = unidecode(title)
        description = response.css("meta[name='description']::attr(content)").extract_first()
        description_ascii = unidecode(description)

        blacklist_keywords_title = self.match_blacklist_keywords(title_ascii)
        blacklist_keywords_description = self.match_blacklist_keywords(description_ascii)
        if len(blacklist_keywords_title) > 0 or len(blacklist_keywords_description) > 0:
            return
        
        dom = self.match_keywords_dom(text_dom)

        try:
            yield {
                "url": response.url,
                "date": time.time(),
                "title": title_ascii,
                "description": description_ascii,
                "dom": dom
            }
        except:
            self.logger.warning("Ignored for URL: %s", response.url)

        # Insert database
        cur.execute("""
            INSERT INTO urls (url, dom)
            VALUES (%s, %s)
            ON CONFLICT (url)
            DO UPDATE SET dom = EXCLUDED.dom
            WHERE urls.url = %s
        """, (response.url, json.dumps(dom), response.url))
        conn.commit()

        # On récupère tous les liens de la page et on les stocke dans la pile
        links = response.css("a::attr(href)").extract()
        for link in links:
            # Si le lien est relatif, on le transforme en absolu
            if not link.startswith("http"):
                link = response.urljoin(link)
            # On vérifie si le lien est allowed
            if link not in self.start_urls and link not in self.visited_urls and self.match_patterns(allowed_urls, link):
                # On envoie une requête à chaque lien dans la pile
                yield scrapy.Request(link, callback=self.parse, headers=headers)

    def clean_string(self, s):
        """
        Trims a string, removes accents, converts to lowercase,
        and replaces "oe" with "Œ".
        """
        # Remove leading/trailing whitespace
        s = s.strip()

        # Remove accents
        accents = {
            'a': 'àáâãäå',
            'c': 'ç',
            'e': 'èéêë',
            'i': 'ìíîï',
            'n': 'ñ',
            'o': 'òóôõö',
            'u': 'úûü', # Revoir pour le ou le u
            'y': 'ýÿ',
            ' ': '-_+/.,!?@#$%&()=\t'
        }
        for k, v in accents.items():
            for accent in v:
                s = s.replace(accent, k)

        # Replace "oe" with "Œ"
        s = s.replace('Œ', 'oe')

        # Convert to lowercase
        s = s.lower()

        return s
    
    def keywords_to_count_dir(self, keywords):
        keyword_counts = {}
        for keyword in keywords:
            if keyword in keyword_counts:
                keyword_counts[keyword] += 1
            else:
                keyword_counts[keyword] = 1
        return keyword_counts

    def match_keywords_dom(self, text_dom):
        dom = []

        if text_dom is None:
            return []
        for element in text_dom:
            if len(element) > 1:
                text = element[1]
                text_unidecode = unidecode(text)

                keywords = self.match_keywords(text_unidecode)

                interrogative_adverbs = self.match_interrogative_adverbs(text_unidecode)
                if keywords:
                    element_keywords = [element[0], keywords]

                    # Interrogative adverbs
                    if interrogative_adverbs:
                        element_keywords.append(interrogative_adverbs)

                    # img src
                    if element[0] == 'img':
                        element_keywords.append(element[1])

                    dom.append(element_keywords)
        return dom

    def match_keywords(self, text):
        if text is None:
            return []
        
        keywords_match = []
        clean_text = self.clean_string(text)
        clean_text_split = clean_text.split(' ')
        for keyword in self.keywords:
            for word in clean_text_split:
                if keyword == word:
                    keywords_match.append(keyword)
        if len(keywords_match) == 0:
            return None
        keywords_dir = self.keywords_to_count_dir(keywords_match)
        return keywords_dir
    
    def match_keywords_pathname(self, pathname):
        if pathname is None:
            return []
        
        keywords_match = []
        clean_pathname = self.clean_string(pathname)
        for keyword in self.keywords:
            if keyword in clean_pathname:
                keywords_match.append(keyword)
        if len(keywords_match) == 0:
            return None
        keywords_dir = self.keywords_to_count_dir(keywords_match)
        return keywords_dir
    
    def match_interrogative_adverbs(self, text):
        if text is None:
            return None
        
        interrogative_adverbs_match = []
        clean_text = self.clean_string(text)
        clean_text_split = clean_text.split(' ')
        for interrogative_adverb in self.interrogative_adverbs:
            for word in clean_text_split:
                if interrogative_adverb == word:
                    interrogative_adverbs_match.append(interrogative_adverb)
        if len(interrogative_adverbs_match) == 0:
            return None
        interrogative_adverbs_dir = self.keywords_to_count_dir(interrogative_adverbs_match)
        return interrogative_adverbs_dir

    def match_blacklist_keywords(self, text):
        keywords_match = []
        if text is None:
            return []
        for keyword in blacklist_keywords:
            if keyword in self.clean_string(text) and len(keyword) > 3:
                keywords_match.append(keyword)
        return keywords_match