from flask import Flask, request, jsonify
from datamuse import Datamuse
import random

app = Flask(__name__)


def obtener_palabra_aleatoria(longitud, idioma="es"):
    api = Datamuse()
    results = api.words(sp="?" * longitud, max=1000, v=idioma)
    if results:
        palabra_aleatoria = random.choice(results)["word"]
        return palabra_aleatoria
    return None


juegos = {}


@app.route("/iniciar_juego", methods=["POST"])
def iniciar_juego():
    data = request.json
    longitud_palabra = data["longitud"]
    idioma = data["idioma"]
    juego_id = len(juegos) + 1
    palabra_secreta = obtener_palabra_aleatoria(longitud_palabra, idioma)
    if not palabra_secreta:
        return (
            jsonify({"error": "No se pudo obtener una palabra. Inténtalo de nuevo."}),
            400,
        )

    juego = {
        "palabra_secreta": palabra_secreta,
        "letras_adivinadas": [],
        "intentos_restantes": 6,
    }
    juegos[juego_id] = juego

    return jsonify(
        {"juego_id": juego_id, "estado": mostrar_estado_actual(palabra_secreta, [])}
    )


@app.route("/adivinar_letra", methods=["POST"])
def adivinar_letra():
    data = request.json
    juego_id = data["juego_id"]
    letra = data["letra"].lower()

    if juego_id not in juegos:
        return jsonify({"error": "Juego no encontrado."}), 404

    juego = juegos[juego_id]
    if letra in juego["letras_adivinadas"]:
        return jsonify({"error": "Ya has adivinado esa letra. Intenta con otra."}), 400

    juego["letras_adivinadas"].append(letra)
    if letra in juego["palabra_secreta"]:
        mensaje = "¡Correcto!"
    else:
        juego["intentos_restantes"] -= 1
        mensaje = "Incorrecto. Pierdes un intento."
        if juego["intentos_restantes"] == 0:
            return jsonify(
                {
                    "mensaje": "Has perdido. La palabra era: "
                    + juego["palabra_secreta"],
                    "fin": True,
                }
            )

    estado_actual = mostrar_estado_actual(
        juego["palabra_secreta"], juego["letras_adivinadas"]
    )
    if set(juego["palabra_secreta"]) == set(juego["letras_adivinadas"]):
        return jsonify(
            {
                "mensaje": "¡Felicidades! Has adivinado la palabra: "
                + juego["palabra_secreta"],
                "estado": estado_actual,
                "fin": True,
            }
        )

    return jsonify(
        {
            "mensaje": mensaje,
            "estado": estado_actual,
            "intentos_restantes": juego["intentos_restantes"],
        }
    )


def mostrar_estado_actual(palabra, letras_adivinadas):
    return " ".join([letra if letra in letras_adivinadas else "_" for letra in palabra])


if __name__ == "__main__":
    app.run(debug=True)
