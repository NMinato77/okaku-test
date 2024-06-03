import React, { useState } from 'react';
import './App.css';

function App() {
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');
  const [originalText, setOriginalText] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch(`${process.env.REACT_APP_API_URL}process`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ input_text: inputText }),
    });
    const data = await response.json();
    setOutputText(data.result);
    setOriginalText(data.original);
    setInputText('');  // 入力欄をクリア
  };

  const getHighlightedText = (result, original) => {
    let resultComponents = [];
    for (let i = 0; i < result.length; i++) {
      if (result[i] !== original[i]) {
        resultComponents.push(<span key={i} style={{ color: 'red' }}>{result[i]}</span>);
      } else {
        resultComponents.push(<span key={i} style={{ color: 'white' }}>{result[i]}</span>);
      }
    }
    return resultComponents;
  };

  return (
    <div className="App" style={{ backgroundColor: 'black', color: 'white', padding: '20px' }}>
      <form onSubmit={handleSubmit}>
        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          rows="10"
          cols="50"
          style={{ width: '100%', marginBottom: '10px' }}
        />
        <br />
        <button type="submit">Submit Text</button>
      </form>
      <div style={{ marginTop: '20px' }}>
        {outputText && getHighlightedText(outputText, originalText)}
      </div>
    </div>
  );
}

export default App;