wget https://raw.githubusercontent.com/CodeSante/medical-wordlist/main/fr/wordlist.fr.txt
mv wordlist.fr.txt keywords.txt
sudo apt install libpq-dev
pip3 install bs4
pip3 install scrapy
pip3 install unidecode
pip3 install psycopg2
bash scripts/install-db.sh
