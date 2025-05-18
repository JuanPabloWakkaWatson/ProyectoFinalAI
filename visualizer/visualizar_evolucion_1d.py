# visualizar_evolucion_1d.py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

# ==== SELECCIÓN INTERACTIVA DE CARPETA ====
base_dir = os.path.join("Regla90", "evoluciones_1d")
folders = sorted([f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))])

if not folders:
    raise FileNotFoundError(f"No se encontraron carpetas en {base_dir}")

print("Carpetas disponibles:")
for i, folder in enumerate(folders):
    print(f"{i + 1}. {folder}")

choice = int(input("Selecciona una carpeta por número: ")) - 1
selected_folder = os.path.join(base_dir, folders[choice])
ruta_archivo = os.path.join(selected_folder, "evolution.npy")

if not os.path.exists(ruta_archivo):
    raise FileNotFoundError("No se encontró el archivo evolution.npy en la carpeta seleccionada.")


# ==== Cargar evolución ====
evolution = np.load(ruta_archivo)

# ==== Generar mapa con cambios ====
changes = np.zeros_like(evolution)
for t in range(1, evolution.shape[0]):
    changes[t] = np.bitwise_xor(evolution[t], evolution[t - 1])

# Estado visual combinado (0 = muerto, 1 = vivo estático, 2 = cambio reciente)
visual = evolution.copy()
visual[changes == 1] = 2

# ==== Salida ====
output_dir = os.path.dirname(ruta_archivo)
gif_path = os.path.join(output_dir, "evolution_colored.gif")

# ==== Colormap personalizado ====
from matplotlib.colors import ListedColormap
colors = ["black", "white", "red"]  # muerto, vivo, cambió
cmap = ListedColormap(colors)

# ==== Visualización ====
fig, ax = plt.subplots(figsize=(8, 6))
img = ax.imshow(visual[:1], cmap=cmap, interpolation="nearest", aspect="auto", vmin=0, vmax=2)
ax.set_title("Regla 90 con Cambios de Estado")
ax.axis("off")

def update(frame):
    img.set_data(visual[:frame+1])
    return [img]

ani = animation.FuncAnimation(fig, update, frames=visual.shape[0], interval=100, blit=True)
ani.save(gif_path, writer="pillow", fps=10)

print(f"✅ GIF con colores generado en: {gif_path}")
