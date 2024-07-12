from datamuse import Datamuse
import random


class GameManager:
    def __init__(self):
        self.juegos = {}

    def obtener_palabra_aleatoria(self, longitud, idioma="es"):
        api = Datamuse()
        results = api.words(sp="?" * longitud, max=1000, v=idioma)
        if results:
            palabra_aleatoria = random.choice(results)["word"]
            return palabra_aleatoria
        return None

    def iniciar_juego(self, longitud_palabra, idioma):
        palabra_secreta = self.obtener_palabra_aleatoria(longitud_palabra, idioma)
        if not palabra_secreta:
            return None, None
        juego_id = len(self.juegos) + 1
        juego = {
            "palabra_secreta": palabra_secreta,
            "letras_adivinadas": [],
            "intentos_restantes": 6,
        }
        self.juegos[juego_id] = juego
        estado = self.mostrar_estado_actual(palabra_secreta, [])
        return juego_id, estado

    def mostrar_estado_actual(self, palabra, letras_adivinadas):
        return " ".join(
            [letra if letra in letras_adivinadas else "_" for letra in palabra]
        )

    def adivinar_letra(self, juego_id, letra):
        juego = self.juegos.get(juego_id)
        if not juego:
            return "Juego no encontrado.", "", 0, True
        if letra in juego["letras_adivinadas"]:
            return (
                "Ya has adivinado esa letra. Intenta con otra.",
                self.mostrar_estado_actual(
                    juego["palabra_secreta"], juego["letras_adivinadas"]
                ),
                juego["intentos_restantes"],
                False,
            )
        juego["letras_adivinadas"].append(letra)
        if letra in juego["palabra_secreta"]:
            mensaje = "¡Correcto!"
        else:
            juego["intentos_restantes"] -= 1
            mensaje = "Incorrecto. Pierdes un intento."
            if juego["intentos_restantes"] == 0:
                return (
                    "Has perdido. La palabra era: " + juego["palabra_secreta"],
                    self.mostrar_estado_actual(
                        juego["palabra_secreta"], juego["letras_adivinadas"]
                    ),
                    juego["intentos_restantes"],
                    True,
                )
        estado_actual = self.mostrar_estado_actual(
            juego["palabra_secreta"], juego["letras_adivinadas"]
        )
        if set(juego["palabra_secreta"]) == set(juego["letras_adivinadas"]):
            return (
                "¡Felicidades! Has adivinado la palabra: " + juego["palabra_secreta"],
                estado_actual,
                juego["intentos_restantes"],
                True,
            )
        return mensaje, estado_actual, juego["intentos_restantes"], False
