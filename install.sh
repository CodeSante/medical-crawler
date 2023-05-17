wget https://raw.githubusercontent.com/CodeSante/medical-wordlist/main/fr/wordlist.fr.txt
mv wordlist.fr.txt keywords.txt
sudo apt install libpq-dev
pip install -r requirements.txt
bash scripts/install-db.sh
