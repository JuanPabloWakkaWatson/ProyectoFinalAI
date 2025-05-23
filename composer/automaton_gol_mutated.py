# generar_gol_mutado.py
import numpy as np
import os
from datetime import datetime

# Este código genera una evolución del Game of Life con mutaciones aleatorias

# Generar una evolución del autómata celular de Conway (GoL) 
# con una tasa de mutación configurable y 
# guardar el resultado como un archivo .npy.

def generar_gol(steps=128, grid_size=(32, 32), mutation_rate=0.02, output_dir="GoL/evolucionesGoL/tmp"):
    initial = np.random.choice([0, 1], size=grid_size, p=[0.7, 0.3])

    def count_neighbors(grid, x, y):
        return sum(grid[(x + dx) % grid.shape[0], (y + dy) % grid.shape[1]]
                   for dx in [-1, 0, 1] for dy in [-1, 0, 1] if not (dx == 0 and dy == 0))

    # Pasos que le llevará a la evolución
    def step(grid):
        new_grid = np.zeros_like(grid)
        for x in range(grid.shape[0]):
            for y in range(grid.shape[1]):
                neighbors = count_neighbors(grid, x, y)
                if grid[x, y] == 1 and neighbors in [2, 3]:
                    new_grid[x, y] = 1
                elif grid[x, y] == 0 and neighbors == 3:
                    new_grid[x, y] = 1
        mutation = np.random.rand(*grid.shape) < mutation_rate
        return np.logical_xor(new_grid, mutation).astype(int)

    history = [initial]
    current = initial
    for _ in range(steps):
        current = step(current)
        history.append(current.copy())

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "gol.npy")
    np.save(path, np.array(history))
    return path

# Contar vecinos 
def count_neighbors(grid, x, y):
    total = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = (x + dx) % grid.shape[0], (y + dy) % grid.shape[1]
            total += grid[nx, ny]
    return total

# Evoluciona el modelo
def mutated_game_of_life_step(grid, mutation_rate=0.02):
    new_grid = np.zeros_like(grid)
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            neighbors = count_neighbors(grid, x, y)
            if grid[x, y] == 1 and neighbors in [2, 3]:
                new_grid[x, y] = 1
            elif grid[x, y] == 0 and neighbors == 3:
                new_grid[x, y] = 1
    mutation_mask = np.random.rand(*grid.shape) < mutation_rate
    new_grid = np.logical_xor(new_grid, mutation_mask).astype(int)
    return new_grid

# Simula el GOL y devuelve las matrices de la evolución
def run_automaton(initial_grid, steps=128, mutation_rate=0.02):
    history = [initial_grid.copy()]
    current_grid = initial_grid.copy()
    for _ in range(steps):
        current_grid = mutated_game_of_life_step(current_grid, mutation_rate)
        history.append(current_grid.copy())
    return np.array(history)

# ========= Generación =========

if __name__ == "__main__":
    grid_size = (32, 32)
    steps = 128
    mutation_rate = 0.02

    # Crear carpeta con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join("GoL/evolucionesGoL", f"gol_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)

    # Generar evolución
    initial_grid = np.random.choice([0, 1], size=grid_size, p=[0.7, 0.3])
    evolution = run_automaton(initial_grid, steps, mutation_rate)

    # Guardar archivo
    npy_path = os.path.join(output_dir, "evolution.npy")
    np.save(npy_path, evolution)

    print(f"✅ Evolución guardada en: {npy_path}")
