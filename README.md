# BlogMaster

BlogMaster est une plateforme de blogging robuste et dynamique développée avec le framework **Django**. Ce projet propose une gestion avancée des utilisateurs avec différents rôles (Auteur et Lecteur), permettant la création, la publication et la gestion d'articles et de commentaires. L'interface utilisateur est moderne et réactive, construite avec **Bootstrap**.

## Fonctionnalités Principales

*   **Gestion des Utilisateurs :**
    *   Inscription et authentification sécurisées.
    *   Profils personnalisés avec biographie.
    *   Système de rôles : `Lecteur` (peut lire et commenter) et `Auteur` (peut créer et gérer des articles).
*   **Gestion des Articles :**
    *   Création, édition et suppression d'articles (réservé aux Auteurs).
    *   Gestion des statuts de publication (`Brouillon` ou `Publié`).
    *   Catégorisation des articles via des "Types de Contenu".
*   **Interaction Communautaire :**
    *   Espace commentaires sous chaque article publié pour encourager les discussions.
*   **Interface UI/UX :**
    *   Design responsive, propre et professionnel utilisant **Bootstrap**.
    *   Affichage centralisé et bien structuré des publications par auteur.

## Technologies Utilisées

*   **Backend :** Python, Django
*   **Frontend :** HTML5, CSS3, Bootstrap
*   **Base de données :** MySQL

## Architecture des Modèles (Base de données)

Le projet repose sur 4 modèles principaux :
*   `Utilisateur` : Étend le modèle de base Django avec `biographie` et `role`.
*   `TypeContenu` : Catégorie ou thème d'un article.
*   `Article` : Contient le titre, le contenu, l'auteur, le statut (Brouillon/Publié) et le type de contenu.
*   `Commentaire` : Lié à un utilisateur et à un article pour permettre les retours des lecteurs.
