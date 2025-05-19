import numpy as np
from scipy.stats import entropy as shannon_entropy

# Este código define métricas cuantitativas para analizar la evolución de 
# patrones generados por autómatas celulares

# mide la cantidad de desorden o aleatoriedad en cada paso del tiempo
def calculate_entropy(grid):
    """Calcula la entropía promedio de una evolución."""
    if grid.ndim == 3:
        # GoL: media por frame
        return np.mean([shannon_entropy(np.bincount(frame.flatten(), minlength=2), base=2)
                        for frame in grid])
    elif grid.ndim == 2:
        # Regla 90
        return np.mean([shannon_entropy(np.bincount(row, minlength=2), base=2)
                        for row in grid])
    else:
        return 0.0

# calcula la proporción de celdas activas (1) a lo largo de la evolución
def density_score(grid):
    """Proporción de celdas activas promedio."""
    return np.mean(grid)

# mide cuánto cambia el patrón entre pasos sucesivos
def variation_score(grid):
    """Porcentaje de frames que cambian significativamente."""
    if grid.ndim == 3:
        diffs = [np.count_nonzero(grid[t] != grid[t - 1]) / grid[t].size
                 for t in range(1, grid.shape[0])]
    elif grid.ndim == 2:
        diffs = [np.count_nonzero(grid[t] != grid[t - 1]) / grid.shape[1]
                 for t in range(1, grid.shape[0])]
    else:
        return 0.0
    return np.mean(diffs)

# evalúa cuánto se parece el patrón a su reflejo horizontal
def symmetry_score(grid):
    """Mide cuán simétrico es el patrón por reflexión horizontal."""
    if grid.ndim == 3:
        scores = []
        for frame in grid:
            left = frame[:, :frame.shape[1] // 2]
            right = np.fliplr(frame[:, frame.shape[1] // 2:])
            min_cols = min(left.shape[1], right.shape[1])
            score = np.mean(left[:, :min_cols] == right[:, :min_cols])
            scores.append(score)
        return np.mean(scores)
    elif grid.ndim == 2:
        left = grid[:, :grid.shape[1] // 2]
        right = np.fliplr(grid[:, grid.shape[1] // 2:])
        min_cols = min(left.shape[1], right.shape[1])
        return np.mean(left[:, :min_cols] == right[:, :min_cols])
    else:
        return 0.0
