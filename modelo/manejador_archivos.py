import json
import os

class ManejadorArchivos:
    @staticmethod
    def guardar_json(ruta_archivo, datos):
        """Guarda datos en un archivo JSON, creando carpetas si no existen."""
        try:
            os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
            with open(ruta_archivo, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar JSON ({ruta_archivo}): {e}")
            return False

    @staticmethod
    def leer_json(ruta_archivo):
        """Lee datos desde un archivo JSON. Retorna None si no existe."""
        if not os.path.exists(ruta_archivo):
            return None
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error al leer JSON ({ruta_archivo}): {e}")
            return None
