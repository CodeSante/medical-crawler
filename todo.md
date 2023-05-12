- Faire mini DOM de keywords pour title,description,h1,h2,p
- Ajouter nombre plutot que repetition des keywords
- Utiliser les 5W (5W-keywords, medical-keywords)

dom
	h1
		keywords-medical
			hepatite: 5
			cataracte: 2
		keywords-5W
			comment: 2

	p
		keywords-medical
			cataracte: 1
		keywords-5W
			qui: 1

- Detecter les pages souvent mises a jour via un hash et un iter

update
	last-hash (hash du dom)
	update-nb
	datetime

- Ecrire en BDD (Postgresql / mixe JSON)

urls:
id, url, dom-id, update-id

doms:
id, dom-json, url-id

updates:
id, last-hash, update-nb, datetime, url-id
