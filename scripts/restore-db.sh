#!/bin/bash

# Demande du chemin de la sauvegarde compressée
read -p "Entrez le chemin de la sauvegarde compressée : " backup_file

# Vérification de l'existence du fichier de sauvegarde
if [ ! -f "$backup_file" ]; then
    echo "Le fichier de sauvegarde compressée n'existe pas. Veuillez spécifier un fichier valide."
    exit 1
fi

# Nom du fichier de restauration
restore_file="${backup_file%.gz}"

# Commande pour effectuer la décompression de la sauvegarde
decompress_command="gunzip -c $backup_file > $restore_file"

# Exécution de la commande de décompression
eval $decompress_command

# Vérification du statut de la commande
if [ $? -eq 0 ]; then
    echo "La décompression de la sauvegarde a été effectuée avec succès : $restore_file"
else
    echo "Une erreur s'est produite lors de la décompression de la sauvegarde."
    exit 1
fi

# Commande pour restaurer la base de données à partir de la sauvegarde en utilisant l'utilisateur postgres
restore_command="sudo -u postgres psql -f $restore_file"

# Exécution de la commande de restauration
eval $restore_command

# Vérification du statut de la commande
if [ $? -eq 0 ]; then
    echo "La restauration de la base de données PostgreSQL à partir de la sauvegarde a été effectuée avec succès."
else
    echo "Une erreur s'est produite lors de la restauration de la base de données PostgreSQL."
    exit 1
fi

# Suppression du fichier de restauration
rm $restore_file

echo "La sauvegarde compressée a été décompressée et la base de données a été restaurée avec succès."