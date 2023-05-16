import requests

def check_urls(filename, output_file):
    with open(filename, 'r') as file:
        urls = file.read().splitlines()

    with open(output_file, 'w') as output:
        for url in urls:
            try:
                response = requests.get(url.strip())
                if response.status_code == 200:
                    print(f"URL: {url} existe (200 OK)")
                    output.write(url + '\n')
                else:
                    print(f"URL: {url} existe mais a renvoyé un code {response.status_code}")
            except requests.exceptions.RequestException:
                print(f"URL: {url} n'est pas accessible")

# Spécifiez le nom de votre fichier contenant les URLs (un URL par ligne)
filename = 'datas/website_list.txt'

# Spécifiez le nom du fichier de sortie pour les URLs existantes
output_file = 'datas/available_websites.txt'

check_urls(filename, output_file)
