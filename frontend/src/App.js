import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:8000/ask', { text: question });
      setResponse(res.data);
    } catch (error) {
      console.error('Erreur:', error);
    }
    setLoading(false);
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Assistant Musical Claude</h1>
      <form onSubmit={handleSubmit} className="mb-4">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Posez votre question musicale..."
          className="w-full p-2 border rounded"
        />
        <button
          type="submit"
          disabled={loading}
          className="mt-2 bg-blue-500 text-white p-2 rounded"
        >
          {loading ? 'Chargement...' : 'Envoyer'}
        </button>
      </form>
      {response && (
        <div className="bg-gray-100 p-4 rounded">
          <h2 className="text-xl font-semibold mb-2">Réponse :</h2>
          <p>{response.answer}</p>
          <p className="mt-2">Confiance : {response.confidence * 100}%</p>
          <h3 className="text-lg font-semibold mt-4">Informations Discogs :</h3>
          <ul>
            <li>Artiste : {response.discogs_info.artist}</li>
            <li>Titre : {response.discogs_info.title}</li>
            <li>Année : {response.discogs_info.year}</li>
            <li>Genre : {response.discogs_info.genre}</li>
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;