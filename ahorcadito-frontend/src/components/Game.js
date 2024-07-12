import React, { useState } from 'react';
import axios from 'axios';
import LetterInput from './LetterInput';

const API_URL = 'http://localhost:5000';

function Game() {
  const [juegoId, setJuegoId] = useState(null);
  const [estado, setEstado] = useState('');
  const [intentosRestantes, setIntentosRestantes] = useState(6);
  const [mensaje, setMensaje] = useState('');
  const [error, setError] = useState(null);
  const [longitudPalabra, setLongitudPalabra] = useState(5); // Estado para la longitud de la palabra

  const iniciarJuego = async () => {
    try {
      const respuesta = await axios.post(`${API_URL}/iniciar_juego`, {
        longitud: longitudPalabra, // Utiliza la longitud seleccionada por el usuario
        idioma: 'es'
      });
      setJuegoId(respuesta.data.juego_id);
      setEstado(respuesta.data.estado);
      setIntentosRestantes(6);
      setMensaje('');
      setError(null);
    } catch (error) {
      setError('Error al iniciar el juego. Inténtalo de nuevo.');
    }
  };

  const adivinarLetra = async (letra) => {
    try {
      const respuesta = await axios.post(`${API_URL}/adivinar_letra`, {
        juego_id: juegoId,
        letra
      });
      setMensaje(respuesta.data.mensaje);
      setEstado(respuesta.data.estado);
      setIntentosRestantes(respuesta.data.intentos_restantes);
      if (respuesta.data.fin) {
        setJuegoId(null);
      }
      setError(null);
    } catch (error) {
      setError('Error al adivinar la letra. Inténtalo de nuevo.');
    }
  };

  const handleChangeLongitudPalabra = (event) => {
    setLongitudPalabra(parseInt(event.target.value)); // Convierte el valor a entero
  };

  const handleStartGame = () => {
    iniciarJuego();
  };

  return (
    <div>
      <h1>Juego del Ahorcadito</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {!juegoId ? (
        <div>
          <label htmlFor="longitudPalabra">Selecciona la longitud de la palabra:</label>
          <input
            type="number"
            id="longitudPalabra"
            name="longitudPalabra"
            value={longitudPalabra}
            onChange={handleChangeLongitudPalabra}
            min="3" // Establece el mínimo de longitud permitida
            max="10" // Establece el máximo de longitud permitida
          />
          <button onClick={handleStartGame}>Iniciar Juego</button>
        </div>
      ) : (
        <div>
          <p>{estado}</p>
          <p>Intentos restantes: {intentosRestantes}</p>
          <LetterInput onAdiveLetra={adivinarLetra} />
          <p>{mensaje}</p>
        </div>
      )}
    </div>
  );
}

export default Game;
