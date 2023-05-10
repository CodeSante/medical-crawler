import scrapy
from unidecode import unidecode
from urllib.parse import urlparse

allowed_urls = [
    "vidal.fr"
]

blacklist_keywords = [
    "forum"
]

class MySpider(scrapy.Spider):
    name = "test"
    start_urls = [
            "https://www.vidal.fr/"
    ]
    visited_urls = []

    def __init__(self):
        self.keywords = set()
        with open("keywords.txt") as f:
            for line in f:
                self.keywords.add(self.clean_string(line.strip()))

    def match_patterns(self, patterns, text):
        for pattern in patterns:
            if pattern in text:
                return True
        return False

    def is_french_website(self, url):
        parsed_url = urlparse(url)
        return parsed_url.netloc.endswith(".fr")

    def parse(self, response):
        if response.url in self.visited_urls or not self.is_french_website(response.url):
            return
        self.visited_urls.append(response.url)

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        title = response.css("title::text").extract_first()
        title_ascii = unidecode(title)
        description = response.css("meta[name='description']::attr(content)").extract_first()
        description_ascii = unidecode(description)
        h = response.css("h1::text, h2::text").getall()
        p = response.css("p::text").getall()

        blacklist_keywords_title = self.match_blacklist_keywords(title_ascii)
        blacklist_keywords_description = self.match_blacklist_keywords(description_ascii)
        if len(blacklist_keywords_title) > 0 or len(blacklist_keywords_description) > 0:
            return

        keywords_title = self.match_keywords(title_ascii)
        keywords_description = self.match_keywords(description_ascii)
        keywords_h = self.match_keywords_array_unidecode(h)
        keywords_p = self.match_keywords_array_unidecode(p)

        try:
            if len(keywords_title) > 0 or len(keywords_description) > 0:
                yield {
                    "url": response.url,
                    "title": title_ascii,
                    "description": description_ascii,
                    "keywords_title": keywords_title,
                    "keywords_description": keywords_description,
                    "keywords_h": keywords_h,
                    "keywords_p": keywords_p,
                }
        except:
            self.logger.warning("Ignored for URL: %s", response.url)

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
            'u': 'ùúûü',
            'y': 'ýÿ',
        }
        for k, v in accents.items():
            for accent in v:
                s = s.replace(accent, k)

        # Replace "oe" with "Œ"
        s = s.replace('oe', 'Œ')

        # Convert to lowercase
        s = s.lower()

        return s

    def match_keywords_array_unidecode(self, array_text):
        keywords_match_array = []

        if array_text is None:
            return []
        for text in array_text:
            text_unidecode = unidecode(text)
            keywords = self.match_keywords(text_unidecode)
            keywords_match_array = keywords_match_array + keywords
        return keywords_match_array

    def match_keywords(self, text):
        keywords_match = []
        clean_text = self.clean_string(text)
        clean_text_split = clean_text.split(' ')
        if text is None:
            return []
        for keyword in self.keywords:
            for word in clean_text_split:
                if keyword == word:
                    keywords_match.append(keyword)
        return keywords_match

    def match_blacklist_keywords(self, text):
        keywords_match = []
        if text is None:
            return []
        for keyword in blacklist_keywords:
            if keyword in self.clean_string(text) and len(keyword) > 3:
                keywords_match.append(keyword)
        return keywords_match
