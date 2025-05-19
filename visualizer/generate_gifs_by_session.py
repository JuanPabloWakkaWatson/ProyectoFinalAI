import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap

# Este código genera animaciones en formato GIF a partir de 
# archivos .npy que contienen la evolución temporal de autómatas 
# celulares GOL1 y 2 y Regla 90

# GOL es bidimensional y R90 es unidimensional
def generar_gif_gol(path_npy, output_path):
    evolution = np.load(path_npy)

    fig, ax = plt.subplots(figsize=(5, 5))
    img = ax.imshow(evolution[0], cmap="Greys", interpolation="nearest")
    ax.set_title("GoL Evolution")
    ax.axis("off")

    def update(frame):
        img.set_data(evolution[frame])
        return [img]

    ani = animation.FuncAnimation(fig, update, frames=len(evolution), interval=100, blit=True)
    ani.save(output_path, writer="pillow", fps=10)
    plt.close(fig)

def generar_gif_r90(path_npy, output_path):
    evolution = np.load(path_npy)

    # Marcar cambios para efecto visual
    changes = np.zeros_like(evolution)
    for t in range(1, evolution.shape[0]):
        changes[t] = np.bitwise_xor(evolution[t], evolution[t - 1])
    visual = evolution.copy()
    visual[changes == 1] = 2

    fig, ax = plt.subplots(figsize=(8, 5))
    cmap = ListedColormap(["black", "white", "red"])
    img = ax.imshow(visual[:1], cmap=cmap, interpolation="nearest", aspect="auto", vmin=0, vmax=2)
    ax.set_title("Regla 90 Evolution")
    ax.axis("off")

    def update(frame):
        img.set_data(visual[:frame+1])
        return [img]

    ani = animation.FuncAnimation(fig, update, frames=visual.shape[0], interval=100, blit=True)
    ani.save(output_path, writer="pillow", fps=10)
    plt.close(fig)

# El resultado se guarda como un .GIF
def procesar_composicion(composicion_dir):
    for session_name in sorted(os.listdir(composicion_dir)):
        session_path = os.path.join(composicion_dir, session_name)
        if not os.path.isdir(session_path):
            continue
        if not session_name.startswith("session_"):
            continue

        print(f"🎞️ Procesando {session_name}")

        paths = {
            "gol1": os.path.join(session_path, "gol1", "gol.npy"),
            "gol2": os.path.join(session_path, "gol2", "gol.npy"),
            "regla90": os.path.join(session_path, "regla90", "regla90.npy"),
        }

        if os.path.exists(paths["gol1"]):
            output_gif = os.path.join(session_path, "gol1", "gol.gif")
            print(f"📤 Guardando GIF en: {output_gif}")
            generar_gif_gol(paths["gol1"], output_gif)

        if os.path.exists(paths["gol2"]):
            output_gif = os.path.join(session_path, "gol2", "gol.gif")
            print(f"📤 Guardando GIF en: {output_gif}")
            generar_gif_gol(paths["gol2"], output_gif)

        if os.path.exists(paths["regla90"]):
            output_gif = os.path.join(session_path, "regla90", "regla90.gif")
            print(f"📤 Guardando GIF en: {output_gif}")
            generar_gif_r90(paths["regla90"], output_gif)


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

    procesar_composicion(seleccionada)
