# visualizar_evolucion.py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
from datetime import datetime

# ==== SELECCIÓN INTERACTIVA DE CARPETA ====
base_dir = os.path.join("GoL", "evolucionesGoL")
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

# ==== CARGAR EVOLUCIÓN ====
evolution = np.load(ruta_archivo)

# ==== CREAR DIRECTORIO DE SALIDA ====
base_dir = os.path.dirname(ruta_archivo)
gif_path = os.path.join(base_dir, "evolution.gif")

# ==== ANIMACIÓN ====
fig, ax = plt.subplots(figsize=(6, 6))
img = ax.imshow(evolution[0], cmap="Greys", interpolation="nearest")
ax.set_title("Evolución del Autómata Celular (GoL Mutado)")
ax.axis("off")

def update(frame):
    img.set_data(evolution[frame])
    return [img]

ani = animation.FuncAnimation(fig, update, frames=len(evolution), interval=100, blit=True)
ani.save(gif_path, writer="pillow", fps=10)

print(f"✅ GIF generado en: {gif_path}")
