# visualizar_evolucion.py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
from datetime import datetime

# ==== CARGAR EVOLUCIÓN ====
ruta_archivo = input("Ruta del archivo evolution.npy: ").strip()
if not os.path.exists(ruta_archivo):
    raise FileNotFoundError("No se encontró el archivo especificado.")

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
