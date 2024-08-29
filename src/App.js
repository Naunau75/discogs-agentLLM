import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/ask', { text: question });
      setAnswer(response.data);
    } catch (error) {
      console.error('Erreur lors de la requête:', error);
      setAnswer({ error: 'Une erreur est survenue lors de la recherche.' });
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <header>
        <h1>Discogs Q&A</h1>
      </header>
      <main>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Posez votre question sur Discogs"
            disabled={loading}
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Recherche en cours...' : 'Envoyer'}
          </button>
        </form>
        {answer && (
          <div className="answer">
            <h2>Réponse de Claude :</h2>
            <p>{answer.claude_answer}</p>
            <p>Niveau de confiance : {(answer.confidence * 100).toFixed(2)}%</p>
            <h3>Résultats Discogs :</h3>
            <ul>
              {answer.discogs_results.map((result, index) => (
                <li key={index}>{result.title}</li>
              ))}
            </ul>
            <h3>Données scrapées :</h3>
            <pre>{JSON.stringify(answer.scraped_data, null, 2)}</pre>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;