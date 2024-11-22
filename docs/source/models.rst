Modèles de données
=================

Cette section décrit les modèles de données utilisés dans l'API.

Question
--------

.. py:class:: Question

   Modèle représentant une question posée à l'API.

   .. py:attribute:: text
      :type: str

      Le texte de la question posée par l'utilisateur.

DiscogsInfo
-----------

.. py:class:: DiscogsInfo

   Modèle contenant les informations musicales extraites d'une question.

   .. py:attribute:: artist
      :type: Optional[str]

      Le nom de l'artiste extrait de la question.

   .. py:attribute:: title
      :type: Optional[str]

      Le titre de l'album ou de la chanson.

   .. py:attribute:: year
      :type: Optional[int]

      L'année de sortie.

   .. py:attribute:: genre
      :type: Optional[str]

      Le genre musical.

QuestionAnswer
-------------

.. py:class:: QuestionAnswer

   Modèle représentant la réponse générée par Claude.

   .. py:attribute:: answer
      :type: str

      La réponse textuelle générée.

Response
--------

.. py:class:: Response

   Modèle de la réponse finale de l'API.

   .. py:attribute:: answer
      :type: str

      La réponse complète à la question.

   .. py:attribute:: confidence
      :type: float

      Le niveau de confiance dans la réponse (entre 0 et 1).

   .. py:attribute:: discogs_info
      :type: DiscogsInfo

      Les informations musicales extraites. 