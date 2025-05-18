import os
import json
import numpy as np
from metrics import calculate_entropy, density_score, variation_score

def analizar_archivo(path):
    arr = np.load(path)
    return {
        "entropia": round(calculate_entropy(arr), 4),
        "densidad": round(density_score(arr), 4),
        "variacion": round(variation_score(arr), 4)
    }

def analizar_sesion(session_path):
    resultados = {}
    archivos = {
        "gol1": os.path.join(session_path, "gol1", "gol.npy"),
        "gol2": os.path.join(session_path, "gol2", "gol.npy"),
        "regla90": os.path.join(session_path, "regla90", "regla90.npy"),
    }

    for nombre, path in archivos.items():
        if os.path.exists(path):
            resultados[nombre] = analizar_archivo(path)

    metadata_path = os.path.join(session_path, "metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(resultados, f, indent=2)
    print(f"✅ Guardado: {metadata_path}")

def analizar_composicion(composicion_path):
    for session_name in sorted(os.listdir(composicion_path)):
        session_path = os.path.join(composicion_path, session_name)
        if os.path.isdir(session_path):
            analizar_sesion(session_path)

# === MAIN ===
if __name__ == "__main__":
    base = "compositions"
    composiciones = sorted([d for d in os.listdir(base) if d.startswith("composicion_")])
    if not composiciones:
        print("❌ No se encontraron composiciones.")
        exit()

    for i, name in enumerate(composiciones):
        print(f"{i + 1}. {name}")
    choice = int(input("Selecciona una composición por número: ")) - 1
    seleccionada = os.path.join(base, composiciones[choice])

    analizar_composicion(seleccionada)
