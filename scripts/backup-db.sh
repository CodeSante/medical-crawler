#!/bin/bash

# Demande du chemin de sauvegarde
read -p "Entrez le chemin de sauvegarde : " backup_dir

# Vérification de l'existence du répertoire de sauvegarde
if [ ! -d "$backup_dir" ]; then
    echo "Le répertoire de sauvegarde n'existe pas. Veuillez spécifier un répertoire valide."
    exit 1
fi

# Configuration de la base de données PostgreSQL
db_host="localhost"
db_port="5432"
db_name="medical_crawler"
db_user="crawler"
db_password="bG9jYWxob3N0"

# Nom du fichier de sauvegarde
current_date=$(date +"%Y-%m-%d_%H-%M-%S")
backup_file="$backup_dir/$db_name_$current_date.sql.gz"

# Commande pour effectuer la sauvegarde et la compression
backup_command="pg_dump -h $db_host -p $db_port -U $db_user -Fc $db_name | gzip > $backup_file"

# Exécution de la commande de sauvegarde et compression
eval $backup_command

# Vérification du statut de la commande
if [ $? -eq 0 ]; then
    echo "La sauvegarde de la base de données PostgreSQL a été effectuée avec succès : $backup_file"
else
    echo "Une erreur s'est produite lors de la sauvegarde de la base de données PostgreSQL."
fi