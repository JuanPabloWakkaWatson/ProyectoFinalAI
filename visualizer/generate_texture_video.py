import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import Normalize
from matplotlib.animation import FFMpegWriter
import matplotlib.cm as cm
import wave

def cargar_automatas(session_path):
    def expand_regla90(arr, shape2d):
        return np.repeat(np.expand_dims(np.repeat(arr[:, np.newaxis], shape2d[0], axis=1), axis=1), shape2d[1], axis=2)

    gol1 = np.load(os.path.join(session_path, "gol1", "gol.npy"))
    gol2 = np.load(os.path.join(session_path, "gol2", "gol.npy"))
    r90 = np.load(os.path.join(session_path, "regla90", "regla90.npy"))

    if r90.ndim == 2:
        h, w = gol1.shape[1:]
        r90_expanded = np.repeat(r90[:, np.newaxis, :], h, axis=1)  # (steps, h, w)
        if r90_expanded.shape[2] != w:
            r90_expanded = r90_expanded[:, :, :w]  # cortar si es más grande
        r90 = r90_expanded

    return gol1, gol2, r90

def duracion_wav_segundos(wav_path):
    with wave.open(wav_path, "rb") as wav:
        frames = wav.getnframes()
        rate = wav.getframerate()
        return frames / float(rate)

def generar_visual(session_path, gol1, gol2, r90, colormap="inferno", fps=15):
    combined = 0.4 * gol1 + 0.4 * gol2 + 0.2 * r90
    steps, height, width = combined.shape

    wav_path = os.path.join(session_path, "render.wav")
    if os.path.exists(wav_path):
        dur_audio = duracion_wav_segundos(wav_path)
        steps_requeridos = int(dur_audio * fps)
        if steps_requeridos > steps:
            ultimo = combined[-1]
            padding = np.tile(ultimo[np.newaxis, :, :], (steps_requeridos - steps, 1, 1))
            combined = np.concatenate([combined, padding], axis=0)
            steps = steps_requeridos
            print(f"🔁 Se extendieron los frames de {steps} a {steps_requeridos} para igualar audio ({dur_audio:.1f}s).")
    else:
        print("⚠️ No se encontró archivo .wav para ajustar duración.")

    fig, ax = plt.subplots(figsize=(6, 6))
    cmap = plt.colormaps.get_cmap(colormap)
    norm = Normalize(vmin=0, vmax=1.2)
    img = ax.imshow(combined[0], cmap=cmap, norm=norm, interpolation="bicubic")
    ax.axis("off")

    def update(t):
        img.set_array(combined[t])
        return [img]

    ani = animation.FuncAnimation(fig, update, frames=steps, blit=True)
    writer = FFMpegWriter(fps=fps)

    output_mp4 = os.path.join(session_path, "visual_texture.mp4")
    temp_mp4 = output_mp4.replace(".mp4", "_temp.mp4")

    ani.save(temp_mp4, writer=writer)
    plt.close(fig)

    if os.path.exists(wav_path):
        os.system(f'ffmpeg -y -i "{temp_mp4}" -i "{wav_path}" -shortest -c:v libx264 -c:a aac -b:a 192k "{output_mp4}"')
        os.remove(temp_mp4)
        print(f"✅ Video con audio generado: {output_mp4}")
    else:
        os.rename(temp_mp4, output_mp4)
        print(f"✅ Video sin audio generado: {output_mp4}")

def main():
    base_dir = "compositions"
    composiciones = sorted([d for d in os.listdir(base_dir) if d.startswith("composicion_")])
    if not composiciones:
        print("❌ No hay composiciones.")
        return

    for i, name in enumerate(composiciones):
        print(f"{i+1}. {name}")
    choice = int(input("Selecciona una composición por número: ")) - 1
    seleccionada = os.path.join(base_dir, composiciones[choice])

    colormap = input("🎨 Elige colormap (inferno/plasma/viridis): ").strip().lower()
    if colormap not in ["inferno", "plasma", "viridis"]:
        print("⚠️ Colormap no válido. Usando 'inferno'.")
        colormap = "inferno"

    fps = int(input("🎥 FPS del video (default 15): ") or 15)

    for session_name in sorted(os.listdir(seleccionada)):
        session_path = os.path.join(seleccionada, session_name)
        if not os.path.isdir(session_path) or not session_name.startswith("session_"):
            continue
        print(f"\n🎞️ Procesando {session_name}")
        gol1, gol2, r90 = cargar_automatas(session_path)
        generar_visual(session_path, gol1, gol2, r90, colormap, fps)

if __name__ == "__main__":
    main()
