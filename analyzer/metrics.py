import numpy as np
from scipy.stats import entropy as shannon_entropy

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

def density_score(grid):
    """Proporción de celdas activas promedio."""
    return np.mean(grid)

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

# (Opcional futuro) puedes añadir:
# def symmetry_score(grid): ...
