# generar_regla90_mutada.py
import numpy as np
import os
from datetime import datetime

# Este código genera una evolución 1D del autómata Regla 90 con un
# porcentaje configurable de mutaciones aleatorias, y la guarda 
# como archivo .npy.

# Generar la evolución
def generar_regla90(steps=128, width=64, mutation_rate=0.02, output_dir="Regla90/evoluciones_1d/tmp"):
    import numpy as np
    import os

    # Pasos de la evolución 
    def step(current):
        padded = np.pad(current, (1, 1), mode='wrap')
        next_ = np.bitwise_xor(padded[:-2], padded[2:])
        mutation = np.random.rand(len(next_)) < mutation_rate
        return np.logical_xor(next_, mutation).astype(int)

    state = np.zeros(width, dtype=int)
    state[width // 2] = 1
    history = [state]
    for _ in range(steps):
        state = step(state)
        history.append(state.copy())

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "regla90.npy")
    np.save(path, np.array(history))
    return path

# Calcular el siguiente paso
def regla_90_step(current_state):
    """Aplica la regla 90 a una línea 1D."""
    padded = np.pad(current_state, (1, 1), mode='wrap')  # Bordes periódicos
    next_state = np.bitwise_xor(padded[:-2], padded[2:])
    return next_state

# Aplicar las mutaciones en cada paso
def run_automaton_1d(initial_state, steps=128, mutation_rate=0.02):
    history = [initial_state.copy()]
    current_state = initial_state.copy()
    for _ in range(steps):
        # Aplicar regla 90
        next_state = regla_90_step(current_state)

        # Mutación: voltear bits aleatoriamente
        mutation_mask = np.random.rand(len(next_state)) < mutation_rate
        next_state = np.logical_xor(next_state, mutation_mask).astype(int)

        current_state = next_state
        history.append(current_state.copy())
    return np.array(history)

# ==== Configuración general ====
if __name__ == "__main__":
    width = 64
    steps = 128
    mutation_rate = 0.02

    # Crear carpeta de salida
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join("Regla90/evoluciones_1d", f"regla90_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)

    # Estado inicial (1 sola celda viva en el centro)
    initial_state = np.zeros(width, dtype=int)
    initial_state[width // 2] = 1

    evolution = run_automaton_1d(initial_state, steps, mutation_rate)

    # Guardar archivo .npy
    np.save(os.path.join(output_dir, "evolution.npy"), evolution)
    print(f"✅ Evolución guardada en: {os.path.join(output_dir, 'evolution.npy')}")
