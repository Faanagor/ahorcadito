from flask import Blueprint, request, jsonify
from flask_cors import CORS  # Importa CORS desde flask_cors
from .game import GameManager

api_bp = Blueprint("api", __name__)
CORS(api_bp)  # Aplica CORS al blueprint api_bp

game_manager = GameManager()


@api_bp.route("/iniciar_juego", methods=["POST"])
def iniciar_juego():
    try:
        data = request.get_json()
        longitud_palabra = data.get("longitud")
        idioma = data.get("idioma")

        if not longitud_palabra or not idioma:
            return jsonify({"error": "Se requieren longitud e idioma."}), 400

        juego_id, estado = game_manager.iniciar_juego(longitud_palabra, idioma)

        if juego_id is None:
            return (
                jsonify(
                    {"error": "No se pudo obtener una palabra. Inténtalo de nuevo."}
                ),
                400,
            )

        return jsonify({"juego_id": juego_id, "estado": estado})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/adivinar_letra", methods=["POST"])
def adivinar_letra():
    try:
        data = request.get_json()
        juego_id = data.get("juego_id")
        letra = data.get("letra", "").lower()

        if not juego_id or not letra:
            return jsonify({"error": "Se requieren juego_id y letra."}), 400

        mensaje, estado, intentos_restantes, fin = game_manager.adivinar_letra(
            juego_id, letra
        )

        response = {
            "mensaje": mensaje,
            "estado": estado,
            "intentos_restantes": intentos_restantes,
            "fin": fin,
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
