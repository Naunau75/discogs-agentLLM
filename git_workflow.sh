#!/bin/bash

# Ajouter tous les fichiers modifiés
git add .

# Demander le message de commit à l'utilisateur
echo "Entrez votre message de commit :"
read commit_message

# Effectuer le commit avec le message fourni
git commit -m "$commit_message"

# Pousser les changements vers la branche main
git push -u origin main

# Vérifier automatiquement la création d'une nouvelle release
echo "Vérification de la création d'une nouvelle release..."
owner="votre_nom_utilisateur"
repo="votre_repo"
derniere_release=$(curl -s "https://api.github.com/repos/$owner/$repo/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')

while true; do
    nouvelle_release=$(curl -s "https://api.github.com/repos/$owner/$repo/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
    if [ "$nouvelle_release" != "$derniere_release" ]; then
        echo "Nouvelle release détectée : $nouvelle_release"
        break
    fi
    echo "En attente d'une nouvelle release..."
    sleep 60  # Attendre 60 secondes avant de vérifier à nouveau
done

# Tirer les changements une fois la release créée
git pull origin main

echo "Workflow Git terminé avec succès !"