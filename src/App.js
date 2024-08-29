import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/ask', { text: question });
      setAnswer(response.data.answer);
    } catch (error) {
      console.error('Erreur:', error);
      setAnswer('Une erreur est survenue lors de la communication avec le serveur.');
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <h1>Assistant Discogs</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Posez votre question sur Discogs"
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Chargement...' : 'Envoyer'}
        </button>
      </form>
      {answer && (
        <div className="answer">
          <h2>Réponse :</h2>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}

export default App;