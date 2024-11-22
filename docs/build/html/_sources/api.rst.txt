API Documentation
===============

Cette section contient la documentation détaillée de l'API.

.. automodule:: backend.main
   :members:
   :undoc-members:
   :show-inheritance:

API Reference
============

Cette section détaille les endpoints de l'API et leur utilisation.

Endpoint /ask
------------

.. py:function:: ask_question(question: Question) -> Response

   Endpoint principal pour poser une question à l'API.

   :param question: Un objet Question contenant le texte de la question
   :type question: Question
   :return: Un objet Response contenant la réponse, le niveau de confiance et les informations Discogs
   :rtype: Response
   :raises HTTPException: En cas d'erreur lors du traitement de la requête

   Exemple d'utilisation:

   .. code-block:: python

      import httpx

      async with httpx.AsyncClient() as client:
          response = await client.post(
              "http://localhost:8000/ask",
              json={"text": "Quel est le premier album de Pink Floyd?"}
          )
          data = response.json()

   Le processus de traitement se déroule en trois étapes :

   1. Analyse de la question avec Claude pour extraire les informations musicales
   2. Recherche dans la base de données Discogs
   3. Génération de la réponse finale avec Claude

   La réponse inclut :
   
   - La réponse textuelle à la question
   - Un score de confiance basé sur les résultats Discogs
   - Les informations musicales extraites de la question