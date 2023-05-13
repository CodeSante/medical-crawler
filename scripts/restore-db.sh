#!/bin/bash

# Demande du chemin de l'archive
read -p "Entrez le chemin de l'archive à décompresser : " archive_path

# Vérification de l'existence de l'archive
if [ ! -f "$archive_path" ]; then
    echo "L'archive n'existe pas. Veuillez spécifier un fichier valide."
    exit 1
fi

# Chemin de destination de la décompression
read -p "Entrez le chemin de destination de la décompression : " extract_path

# Vérification de l'existence du répertoire de destination
if [ ! -d "$extract_path" ]; then
    echo "Le répertoire de destination n'existe pas. Veuillez spécifier un répertoire valide."
    exit 1
fi

# Extraction de l'archive
tar -xJf "$archive_path" -C "$extract_path"

# Vérification du statut de l'extraction
if [ $? -eq 0 ]; then
    echo "L'archive a été décompressée avec succès dans le répertoire : $extract_path"
else
    echo "Une erreur s'est produite lors de la décompression de l'archive."
    exit 1
fi

# Configuration de la base de données PostgreSQL
db_host="localhost"
db_port="5432"
db_name="medical-crawler"
db_user="crawler"
db_password="bG9jYWxob3N0"

# Commande pour créer la base de données
create_db_command="createdb -h $db_host -p $db_port -U $db_user $db_name"

# Exécution de la commande de création de la base de données
eval $create_db_command

# Vérification du statut de la commande
if [ $? -eq 0 ]; then
    echo "La base de données PostgreSQL a été créée avec succès : $db_name"
else
    echo "Une erreur s'est produite lors de la création de la base de données PostgreSQL."
    exit 1
fi

# Commande pour restaurer la base de données à partir de l'archive
restore_command="pg_restore -h $db_host -p $db_port -U $db_user -d $db_name $extract_path"

# Exécution de la commande de restauration
eval $restore_command

# Vérification du statut de la commande
if [ $? -eq 0 ]; then
    echo "La base de données PostgreSQL a été restaurée avec succès à partir de l'archive."
else
    echo "Une erreur s'est produite lors de la restauration de la base de données PostgreSQL."
    exit 1
fi