from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Informations de connexion à la base de données PostgreSQL
db_host = "localhost"
db_port = "5432"
db_name = "medical_crawler"
db_user = "crawler"
db_password = "bG9jYWxob3N0"

@app.route('/urls', methods=['GET'])
def get_urls():
    try:
        # Connexion à la base de données
        conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
        cursor = conn.cursor()

        # Récupération des URLs et des champs "dom" à partir de la table "urls"
        cursor.execute("SELECT url, dom, turn FROM urls")
        rows = cursor.fetchall()

        # Fermeture de la connexion à la base de données
        cursor.close()
        conn.close()

        # Conversion des résultats en une liste de dictionnaires
        urls_list = [{'url': row[0], 'dom': row[1], 'turn': row[2]} for row in rows]

        # Retourne les URLs sous forme de JSON
        return jsonify(urls_list)

    except (Exception, psycopg2.Error) as error:
        print("Erreur lors de la connexion à PostgreSQL :", error)
        return jsonify({'error': 'Erreur lors de la connexion à la base de données'})
    
@app.route('/urls/without-dom', methods=['GET'])
def get_urls_without_dom():
    try:
        # Connexion à la base de données
        conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
        cursor = conn.cursor()

        # Récupération des URLs et des champs "dom" à partir de la table "urls"
        cursor.execute("SELECT url, turn FROM urls")
        rows = cursor.fetchall()

        # Fermeture de la connexion à la base de données
        cursor.close()
        conn.close()

        # Conversion des résultats en une liste de dictionnaires
        urls_list = [{'url': row[0], 'turn': row[1]} for row in rows]

        # Retourne les URLs sous forme de JSON
        return jsonify({'pages_nb': len(urls_list), 'urls': urls_list})

    except (Exception, psycopg2.Error) as error:
        print("Erreur lors de la connexion à PostgreSQL :", error)
        return jsonify({'error': 'Erreur lors de la connexion à la base de données'})

if __name__ == '__main__':
    app.run(debug=True)