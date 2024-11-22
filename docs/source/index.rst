Bienvenue dans la documentation de DISCOGS-AGENTLLM
=================================================

.. toctree::
   :maxdepth: 2
   :caption: Contenu:

   api
   models
   installation

Introduction
-----------

DISCOGS-AGENTLLM est une API qui combine l'intelligence artificielle de Claude 3.5 Sonnet avec la base de données musicale Discogs pour répondre à des questions sur la musique.

Caractéristiques principales
---------------------------

* Traitement des questions en langage naturel
* Extraction intelligente des informations musicales
* Intégration avec l'API Discogs
* Réponses générées par IA avec niveau de confiance
* API RESTful avec FastAPI

Installation
-----------

Pour installer le projet, suivez ces étapes :

.. code-block:: bash

   # Cloner le dépôt
   git clone https://github.com/votre-username/discogs-agentllm.git
   cd discogs-agentllm

   # Installer les dépendances
   pip install -r requirements.txt

   # Configurer les variables d'environnement
   cp .env.example .env
   # Éditer .env avec vos clés API

Configuration
------------

Le projet nécessite les variables d'environnement suivantes :

* ``ANTHROPIC_API_KEY`` : Clé API pour Claude 3.5 Sonnet
* ``DISCOGS_API_KEY`` : Clé API Discogs
* ``DISCOGS_API_SECRET`` : Secret API Discogs
