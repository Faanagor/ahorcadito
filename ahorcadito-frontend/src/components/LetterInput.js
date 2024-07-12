import React, { useState } from 'react';

function LetterInput({ onAdiveLetra }) {
  const [letra, setLetra] = useState('');

  const handleChange = (e) => {
    setLetra(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onAdiveLetra(letra);
    setLetra('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={letra}
        onChange={handleChange}
        maxLength="1"
      />
      <button type="submit">Adivinar</button>
    </form>
  );
}

export default LetterInput;
